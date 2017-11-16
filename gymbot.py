import os, time, re
from slackclient import SlackClient

# bot's ID is currently retrieved from environment variables.
# TODO merge ID retriever from the other file to keep env variables to a minimum
BOT_ID = os.environ.get("BOT_ID")

# constants
AT_BOT = "<@" + BOT_ID + ">"
AT_BOT_ALT = "/gym"
HELP_COMMAND = "help"
ATTENDANCE_REGXP = re.compile("^\+[0-9]{1,1}$")

# response messages
INVALID_MSG = "Not sure what you mean. Use the *" + HELP_COMMAND + \
				   "* command for more information."
LIST_HEADER = "\n==GYM ATTENDANCE RANKINGS==\n"
ADD_MSG1 = "went to the gym"
ADD_MSG2 = "additional times! "
DONE_MSG = "Very good! Unfortunately I cannot yet register your attendance. Try again later!"
WELCOME_MSG = "HELLO! Machu is here to help you get fit. Use the *" + HELP_COMMAND + \
				   "* command for more information."
HELP_MSG = "Hi, I'm Machu. My job is to keep track of gym attendance and leaderboards!\n\n"+\
					"Available actions:\n"+\
					"• *leaderboards* *_x_* to check the top _x_ members for gym attendance\n"+\
					"• *done* to let me know you went to the gym again (identical to +1)\n"+\
					"• *+y* to let me know you went to the gym _y_ additional times\n"
#TABLE_HEADER = "\nMember | Today | Total\n"+\
#				"------- | ------ | ------\n"

# instantiate Slack & Twilio clients
slack_client = SlackClient(os.environ.get('SLACK_BOT_TOKEN'))

def handle_command(user, command, channel,eventtype):
	"""
		Receives commands directed at the bot and determines if they
		are valid commands. If so, then acts on the commands. If not,
		returns back what it needs for clarification.
	"""

	print(eventtype)
	response = ''
	if eventtype == 'member_joined_channel':
		response = WELCOME_MSG

	elif eventtype == 'message' and command:

		# split by whitespace	
		separatecommand = command.split()

		# get attendance indicator, if possible
		m = ATTENDANCE_REGXP.match(separatecommand[0])

		if separatecommand[0] == 'help':
			response = HELP_MSG

		elif separatecommand[0] == 'leaderboards':

			# if len(separatecommand) > 1
			# access [1] to get limit
			# else do top 10
			response = LIST_HEADER + "1. " +"Fulano " + "(32)" # TODO replace with DB or text file source
			#TABLE_HEADER + "Placeholder User | No | 34\n" #replace with DB or text file source

		elif m:
			n = int(m.group(0)[1])
			if n == 0:
				response = "Do you even lift bruh?"
			else:
				response = ADD_MSG1 + ' ' + str(n) + ' ' + ADD_MSG2 + ' ' + DONE_MSG

		elif separatecommand[0] == 'done':

			response = DONE_MSG

		else:
			response = INVALID_MSG

	# @ back at the source with the chosen response message
	slack_client.api_call("chat.postMessage", link_names=1, channel=channel,
						  text="@" + user + " " + response, as_user=True)


def parse_slack_output(slack_rtm_output):
	"""
		The Slack Real Time Messaging API is an events firehose.
		this parsing function returns None unless a message is
		directed at the Bot, based on its ID.
	"""
	output_list = slack_rtm_output
	print (output_list)
	if output_list and len(output_list) > 0:
		for output in output_list:
			# For each object in the list
			# 	Valid messages:
			#		- Contain the 'type' and 'user' fields
			#		- 'type' is one of the supported event types
			#			- 'message','member_joined_channel'
			#		- 'user' is NOT the bot itself
			if output and 'type' in output and output['type'] in ('message','member_joined_channel') and 'user' in output and output['user'] != BOT_ID:

				print("This is a valid message for bot")
				text = ''
				sourceuser = ''

				if output['type'] == "message" and 'text' in output:

					#'message' type specifics

					# get text after the @ mention or / invocation, whitespace removed
					if AT_BOT_ALT in output['text']:
						text = output['text'].split(AT_BOT_ALT)[1].strip().lower()
					elif AT_BOT in output['text']:
						text = output['text'].split(AT_BOT)[1].strip().lower()
					else:
						# This message has no mention of our bot. Ignore.
						continue
				
				# TODO is there an easier way to get the username?
				users_api_call = slack_client.api_call("users.list")
				if users_api_call.get('ok'):
					# retrieve all users so we can find the source
					tempusers = users_api_call.get('members')
					for user in tempusers:
						if 'name' in user and user.get('id') == output['user']:
							sourceuser = user.get('name')
				else:
					sourceuser = "Unknown"

				
				return sourceuser, \
						text, \
						output['channel'], output['type']

	return None, None, None, None

if __name__ == "__main__":
	READ_WEBSOCKET_DELAY = 1 # 1 second delay between reading from firehose
	if slack_client.rtm_connect():
		print("StarterBot connected and running!")
		while True:
			user,command,channel,eventtype = parse_slack_output(slack_client.rtm_read())
			print("Parsed:")
			print(user,command,channel,eventtype)
			if user and channel and eventtype in ("message","member_joined_channel"):
				handle_command(user, command, channel,eventtype)
			time.sleep(READ_WEBSOCKET_DELAY)
	else:
		print("Connection failed. Invalid Slack token or bot ID?")
