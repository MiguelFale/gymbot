import abc,pymongo,persistence
from abc_base import Persistence
from pymongo import MongoClient

class MongoDBPersistence(Persistence):

	db = None

	def __init__(self):
		client = MongoClient('localhost', 27017)
		db = client['gym-database']
    
    def leaderboards(self,x=10):
    	return db.users.find().sort('timeswent',pymongo.ASCENDING).limit(10)

    def updateAttendance(self,user,timeswent=1):
    	return db.users.update_one({'user': user}, {'$inc': {'timeswent': timeswent}}
