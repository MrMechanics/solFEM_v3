#
#
#	constraints.py
#  ---------------
#
#	This file holds the constraint objects. They take input about 
#	constraints from the FEModel objects and sets up lagrange
#	multipliers on the appropriate degrees of freedom.
#


import numpy as np




class Constraint(object):
	'''
Base class for constraints.
'''
	def __init__(self,name,nodeset1,nodeset2,DOFs):
		self.name = name
		self.nodeset1 = nodeset1
		self.nodeset2 = nodeset2
		self.NFS = [0,0,0,0,0,0]
		for dof in range(6):
			if dof+1 in DOFs:
				self.NFS[dof] = 1


	def lagrangeMultipliers(self,mesh):
		'''
	Set up a dictionary with lagrange multiplier
	pairs to be added to the global stiffness matrix.
	NFMT = node freedom map table
	'''
		self.lagrange = {}
		lagrange_count = 0
		compatibility_warning = False
		for nodes in range(len(self.nodePairs)):
			compatibility = False
			if mesh.nodes[self.nodePairs[nodes][0]].NFS == mesh.nodes[self.nodePairs[nodes][1]].NFS:
				compatibility = True
			if compatibility == False and compatibility_warning == False:
				print('\n\tWARNING!!! \n\tNodes', self.nodePairs[nodes][0], 'and', self.nodePairs[nodes][1],
					  'do not have the same number of degrees of freedom.')
				print('\tUser may have to put fixed boundary conditions on free DOFs manually.\n')
				compatibility_warning = True
			for dof in range(6):
				if mesh.nodes[self.nodePairs[nodes][1]].NFS[dof] == 1 and self.NFS[dof] == 1:
					self.lagrange[lagrange_count] = [mesh.NFMT[self.nodePairs[nodes][0]]+dof, \
													 mesh.NFMT[self.nodePairs[nodes][1]]+dof]
					lagrange_count += 1





class TouchLock(Constraint):
	'''
Class for locking one set of nodes to another.
It searches through two nodesets and pairs
up those nodes that lie within the specified
tolerance distance of each other.
'''
	def __init__(self,name,nodeset1,nodeset2,DOFs,tolerance):
		super(TouchLock,self).__init__(name,nodeset1,nodeset2,DOFs)
		self.tolerance = tolerance


	def setupNodePairs(self,mesh):
		'''
	Set up a dictionary with all nodepairs that will
	be used to set up the lagrange multipliers.
	'''
		self.nodePairs = {}
		pair = 0
		for node1 in self.nodeset1:
			for node2 in self.nodeset2:
				if np.sqrt((mesh.nodes[node1].coord[0][0] - mesh.nodes[node2].coord[0][0])**2 + \
							(mesh.nodes[node1].coord[1][0] - mesh.nodes[node2].coord[1][0])**2 + \
							(mesh.nodes[node1].coord[2][0] - mesh.nodes[node2].coord[2][0])**2) < self.tolerance:
					self.nodePairs[pair] = [node1, node2]
					pair += 1





class NodeLock(Constraint):
	'''
Class for locking a set of nodes to
one specified node.
'''
	def __init__(self,name,nodeset1,nodeset2,DOFs):
		super(NodeLock,self).__init__(name,nodeset1,nodeset2,DOFs)


	def setupNodePairs(self,mesh):
		'''
	Set up a dictionary with all nodepairs that will
	be used to set up the lagrange multipliers.
	'''
		self.nodePairs = {}
		pair = 0
		for node1 in self.nodeset1:
			for node2 in self.nodeset2:
				self.nodePairs[pair] = [node1, node2]
				pair += 1






