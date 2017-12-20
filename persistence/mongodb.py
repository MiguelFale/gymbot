# Needs abc in abstract & subclasses
# Subclass needs mongo driver
import abc,pymongo,sys,os
from pymongo import MongoClient
from pymongo.errors import ConnectionFailure
from pymongo.errors import OperationFailure

# Import abstract class
from persistence.abstract import Persistence


class MongoDBPersistence(Persistence):

	#db = None

	def __init__(self):
		print("Attempting connection with mongoDB server")
		client = MongoClient(host='localhost',
							port=27017,
							username=os.environ.get('MONGODB_USER'),
							password=os.environ.get('MONGODB_PASSWD'),
							authSource='gym_database',
                            authMechanism='DEFAULT')
		try:
			print(client.test_database)
			# The ismaster command is cheap and does not require auth.
			client.admin.command('ismaster')
			#db = 
			setattr(self, 'db', client['gym_database'])
		except ConnectionFailure:
			print("Server not available")
			sys.exit(1)
		except Exception as e:
			print("EXCEPTION: "+str(e))
			sys.exit(1)

	def leaderboards(self,x=10,user=''):

		try:
			if user == '':
				return getattr(self,"db").users.find().sort('timeswent',pymongo.ASCENDING).limit(x)
			else:
				return getattr(self,"db").users.find().sort('timeswent',pymongo.ASCENDING)
		except Exception as e:
			print("EXCEPTION: "+str(e))
			sys.exit(1)

	def updateAttendance(self,userID,user,timeswent=1):
		return getattr(self,"db").users.update_one({'slackID': userID}, {'$inc': {'timeswent': timeswent}})
