# from app import app
import re

GLOBAL_START_TIME = 480
DEFAULT_ROUND = 15

class STTime():

	def __init__(self, mins=0, secs=0, fmt=None):
		temp = int(mins) + int(secs/60)
		if fmt: # re.match('\d\d:\d\d', fmt):
			s1, s2 = fmt.split(':')
			self.mins = int(s1)*60 + int(s2) - GLOBAL_START_TIME
		else:
			self.mins = int(mins) + int(secs/60)

	def __repr__(self):
		return self.round_fmt_time()

	def __int__(self):
		return self.round_mins()

	def __sub__(self,other):
		return STInterval(self.round_mins() - other.round_mins())

	def get_mins(self):
		return self.mins

	def get_fmt_time(self):
		(q,r) = divmod(self.mins,60)
		return "{0:0>2d}:{1:0>2d}".format(q,r)

	def round_mins(self, rnd=DEFAULT_ROUND):
		if (self.mins == 0):
			return 0
		temp = self.mins - 1
		return temp - (temp%rnd) + rnd

	def round_fmt_time(self, rnd=DEFAULT_ROUND):
		temp = self.round_mins(rnd)
		(q,r) = divmod(temp+GLOBAL_START_TIME,60)
		return "{0:0>2d}:{1:0>2d}".format(q,r)
	

class STInterval(STTime):

	def __repr__(self):
		return self.round_fmt_interval()

	def round_fmt_interval(self, rnd=DEFAULT_ROUND):
		temp = self.round_mins(rnd)
		(q,r) = divmod(temp,60)
		return ("{0}hr {1}min".format(q,r) if q else "{1}min".format(q,r))


class STLocation():

	count = 0

	def __init__(self, pretty, index=-1):
		self.pretty = pretty
		self.fmt = pretty.replace(',', '').replace(' ','+')
		self.index = index
		STLocation.count += 1

	def __repr__(self):
		return self.pretty

	# def __str__(self):
	# 	return self.fmt

	def get_fmt_location(self):
		return self.fmt

	def get_pretty(self):
		return self.pretty


class STDistance():

	def __init__(self, meters):
		self.meters = meters

	def __repr__(self):
		return self.get_fmt_miles()

	def __int__(self):
		return self.meters

	def get_fmt_meters(self):
		return '{0}m'.format(self.meters)

	def get_miles(self):
		return self.meters*0.00062137

	def get_fmt_miles(self):
		return '{0:.1f}mi'.format(self.meters*0.00062137)


class STRoute():

	def __init__(self):
		self.stops = []

	def __getitem__(self, key):
		return self.stops[key]

	def __len__(self):
		return len(self.stops)

	def add_stop(self, stop):
		self.stops.append(stop)

	def is_empty(self):
		return (len(self) <= 2)

	def calc_time(self, first=0, last=-1):
		assert len(self) >= last
		return self[last][1] - self[first][1]

	def calc_distance(self, dm, first=0, last=-1):
		assert len(self) >= last
		total = 0
		if (last == -1):
			last = len(self)
		for i in range(first, last):
			if (i == first):
				continue
			total = total + int(dm[self[i][0]][self[i-1][0]])
		return STDistance(total)
