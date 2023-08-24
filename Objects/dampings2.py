#
#
#	dampings.py
#  -------------
#
#	This file holds the damping objects. These are applied to
#	solutions using modal dynamics. There are two types of
#	damping; one damping ratio for all modes, or different
#	damping ratios for different frequency ranges.
#





class Damping(object):
	'''
Base class for damping properties.
'''
	def __init__(self,name):
		self.name = name




class Viscous(Damping):
	'''
Viscous damping with a fixed
damping ratio.
'''
	def __init__(self,name,ratio):
		self.type = 'Viscous'
		self.dampRatio = ratio
		super(Viscous,self).__init__(name)




class Frequency(Damping):
	'''
Frequency damping with viscous
damping changing by frequency.
'''
	def __init__(self,name,ratio=1.0):
		self.type = 'Frequency'
		self.dampRatio = ratio
		super(Frequency,self).__init__(name)




