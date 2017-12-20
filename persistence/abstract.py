import abc
from abc import ABCMeta,abstractmethod

class Persistence(object):
	__metaclass__ = ABCMeta

	@abstractmethod
	def leaderboards(self,x=10,user=''):
		"""Retrieve data from leaderboards (top x by default)."""
		return

	@abstractmethod
	def updateAttendance(self,userID,user,timeswent=1):
		"""Update user's gym attendence by timeswent additional times (1 by default)"""
		return