from abc import ABCMeta

class Persistence:
    __metaclass__ = ABCMeta

    @abstractmethod
    def leaderboards(self,x=10):
    	"""Retrieve data from leaderboards (top x by default)."""
    	return

	@abstractmethod
    def updateAttendance(self,user,timeswent=1):
    	"""Update user's gym attendence by timeswent additional times (1 by default)"""
    	return