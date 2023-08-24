#
#
#	boundaries.py
#  ---------------
#
#	This file holds the boundary objects. They take input about 
#	boundary conditions from the FEModel objects and associates
#	them with the appropriate degrees of freedom.
#





class Boundary(object):
	'''
Base class for boundary conditions.
'''
	def __init__(self,name,nodeset):
		self.name = name
		self.nodeset = nodeset




class Displacement(Boundary):
	'''
Class for applied boundary displacements.
'''
	def __init__(self,name,nodeset,disp,DOFs):
		self.displacement = disp
		self.DOFs = DOFs
		super(Displacement,self).__init__(name,nodeset)


	def setDegreeOfFreedomBoundary(self,mesh):
		'''
	Set up a dictionary with global degrees of freedom
	and their prescribed displacements.
	self.fixed = fixed degrees of freedom in global
				 displacement vector
	NFMT = node freedom map table
	'''
		self.fixed = {}
		number_of_nodes = len(self.nodeset)

		for node in range(number_of_nodes):
			dof = 1
			for nfs in range(6):
				if mesh.nodes[self.nodeset[node]].NFS[nfs] == 1:
					if (nfs+1) in self.DOFs:
						self.fixed[mesh.NFMT[self.nodeset[node]]+dof-1] = self.displacement
					dof += 1




class Heatsink(Boundary):	# NOT READY TO BE USED
	'''
Class for heat dissipation to boundary.
'''
	def __init__(self,name,nodeset,tempr):
		self.temperature = tempr
		super(Heatsink,self).__init__(name,nodeset)





