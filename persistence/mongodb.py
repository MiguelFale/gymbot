# Needs abc in abstract & subclasses
# Subclass needs mongo driver
import abc,pymongo,sys
from pymongo import MongoClient
from pymongo.errors import ConnectionFailure
from pymongo.errors import OperationFailure

# Import abstract class
from persistence.abstract import Persistence


class MongoDBPersistence(Persistence):

	db = None

	def __init__(self):
		print("Attempting connection with mongoDB server")
		client = MongoClient('localhost', 27017)
		try:
			# The ismaster command is cheap and does not require auth.
			client.admin.command('ismaster')
			db = client['gym-database']
		except ConnectionFailure:
			print("Server not available")
			sys.exit(1)
		except Exception as e:
			print("EXCEPTION: "+str(e))
			sys.exit(1)

	def leaderboards(self,x=10,user=''):

		try:
			if user == '':
				return db.users.find().sort('timeswent',pymongo.ASCENDING).limit(x)
			else:
				return db.users.find().sort('timeswent',pymongo.ASCENDING)
		except Exception as e:
			print("EXCEPTION: "+str(e))
			sys.exit(1)

	#def updateAttendance(self,userID,user,timeswent=1):
	#	return db.users.update_one({'slackID': userID}, {'$inc': {'timeswent': timeswent}})