# Needs abc in abstract & subclasses
# Subclass needs mongo driver
import abc,pymongo,sys,os
from pymongo import MongoClient
from pymongo.errors import ConnectionFailure
from pymongo.errors import OperationFailure

# Import abstract class
from persistence.abstract import Persistence


class MongoDBPersistence(Persistence):

	def __init__(self):
		'''Initialize mongoDB database connection'''
		print("Attempting connection with mongoDB server")
		try:
            #use authentication database 'test'
			client = MongoClient('localhost',
			username=os.environ.get('MONGODB_USER'),
			password=os.environ.get('MONGODB_PASSWD'),
			authSource='test',
			authMechanism='SCRAM-SHA-1')

            #test server availability (triggers ConnectionFailure)
			client.admin.command('ismaster')

            #THEN use normal database 'gym_database'
			setattr(self, 'db', client.get_database('gym_database'))

		except ConnectionFailure:
			print("Server not available")
			sys.exit(1)
		except Exception as e:
			print("EXCEPTION: "+str(e))
			sys.exit(1)

	def leaderboards(self,x=10,user=''):

		if user == '':
			return getattr(self,"db").users.find().sort('timeswent',pymongo.ASCENDING).limit(x)
		else:
			return getattr(self,"db").users.find().sort('timeswent',pymongo.ASCENDING)

	def updateAttendance(self,userID,user,timeswent=1):
		return getattr(self,"db").users.update_one({'slackID': userID,'name': user}, {'$inc': {'timeswent': timeswent}}, upsert = True)
