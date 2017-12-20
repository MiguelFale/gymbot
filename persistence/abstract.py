import abc
from abc import ABC,abstractmethod

class Persistence(ABC):
	
	@abstractmethod
	def leaderboards(self,x=10,user=''):
		"""Retrieve data from leaderboards (top x by default)."""
		pass

	@abstractmethod
	def updateAttendance(self,userID,user,timeswent=1):
		"""Update user's gym attendence by timeswent additional times (1 by default)"""
		pass