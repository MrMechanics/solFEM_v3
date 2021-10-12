#
#
#	nodes.py
#  ----------
#
#	The node object is used to hold coordinates and
#	information about what degrees of freedom to activate.
#	It is also used to store results when used in the
#	*.out-file read by viewFEM to plot results.
#	





class Node(object):
	'''
Base class for all nodes. Stores coordinates,
information on active degrees of freedom and
results (displacement, acceleration...).
'''
	def __init__(self,n,x,y,z=0):
		self.number = n
		self.coord = [[float(x)],[float(y)],[float(z)]]
		self.NFS = [0,0,0,0,0,0]
		self.solutions = {}


	def translate(self,x,y,z):
		'''
	Takes new coordinates for node
	object and applies them to
	self.coord.
	'''
		self.coord = [[float(x)],[float(y)],[float(z)]]






