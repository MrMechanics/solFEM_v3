#
#
#	mesh.py
#  ---------
#	Mesh object holding all nodes and elements 
#	used in finite element model, containing assembly
#	and type information. Also used to store results.
#	





class Mesh(object):
	'''
Class for mesh. Holds information on node coordinates
(also generalized coordinates for modal analysis),
element nodes, element type, and analysis results.
It is stored to binary file for easy access of results
to viewFEM.py.
'''
	def __init__(self,nodes,elements):
		self.nodes = nodes
		self.elements = elements
		self.solutions = []





