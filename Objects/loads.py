#
#
#	loads.py
#  ----------
#
#	This file holds the load objects. They take information from
#	the FEModel object about loads, and calculate the load vectors
#	to be used in the analysis.
#


from math import sqrt
import numpy as np





class Load(object):
	'''
Base class for loads.
'''
	def __init__(self,name,nodeset):
		self.name = name
		self.nodes = nodeset




class Force(Load):
	'''
Class for one force vector uniformly
distributed on a set of nodes.
'''
	def __init__(self,name,nodeset,force,v1,v2,v3=0.0):
		self.type = 'Force'
		self.force = force
		self.vector = [[float(v1)],[float(v2)],[float(v3)]]
		super(Force,self).__init__(name,nodeset)


	def calcDegreeOfFreedomForces(self,nDOFs,NFMT):
		'''
	Calculate the force contribution on each individual
	degree of freedom based on affected nodes, force and
	force vector.
	self.F = force vector
	nDOFs  = number of degrees of freedom (in FE-model)
	NFMT   = node freedom map table
	'''
		self.F = np.zeros((nDOFs,1))

		number_of_nodes = len(self.nodes)
		vectMag = sqrt(self.vector[0][0]**2 + self.vector[1][0]**2 + self.vector[2][0]**2)
		f1_cos = self.vector[0][0]/vectMag
		f2_cos = self.vector[1][0]/vectMag
		f3_cos = self.vector[2][0]/vectMag

		for i in range(number_of_nodes):
			self.F[NFMT[self.nodes[i]]] = (self.force*f1_cos)/number_of_nodes
			self.F[NFMT[self.nodes[i]]+1] = (self.force*f2_cos)/number_of_nodes
			if self.vector[2][0] != 0.0:
				self.F[NFMT[self.nodes[i]]+2] = (self.force*f3_cos)/number_of_nodes




class ForceConcentrated(Load):
	'''
Class for one force vector applied
individually to each node in nodeset.
'''
	def __init__(self,name,nodeset,force,v1,v2,v3=0.0):
		self.type = 'ForceConcentrated'
		self.force = force
		self.vector = [[float(v1)],[float(v2)],[float(v3)]]
		super(ForceConcentrated,self).__init__(name,nodeset)


	def calcDegreeOfFreedomForces(self,nDOFs,NFMT):
		'''
	Apply the force contribution on each individual
	degree of freedom separately.
	self.F = force vector
	nDOFs  = number of degrees of freedom (in FE-model)
	NFMT   = node freedom map table
	'''
		self.F = np.zeros((nDOFs,1))

		number_of_nodes = len(self.nodes)
		vectMag = sqrt(self.vector[0][0]**2 + self.vector[1][0]**2 + self.vector[2][0]**2)
		f1_cos = self.vector[0][0]/vectMag
		f2_cos = self.vector[1][0]/vectMag
		f3_cos = self.vector[2][0]/vectMag

		for i in range(number_of_nodes):
			self.F[NFMT[self.nodes[i]]] = self.force*f1_cos
			self.F[NFMT[self.nodes[i]]+1] = self.force*f2_cos
			if self.vector[2][0] != 0.0:
				self.F[NFMT[self.nodes[i]]+2] = self.force*f3_cos




class ForceDynamic(Load):
	'''
Class for one dynamic force vector applied
uniformly distributed on a set of nodes.
'''
	def __init__(self,name,nodeset,force,v1,v2,v3=0.0):
		self.type = 'ForceDynamic'
		self.force = force
		self.vector = [[float(v1)],[float(v2)],[float(v3)]]
		super(ForceDynamic,self).__init__(name,nodeset)


	def calcDegreeOfFreedomForces(self,nDOFs,NFMT):
		'''
	Calculate the force contribution on each individual
	degree of freedom based on affected nodes, force and
	force vector.
	self.F = force vector
	nDOFs  = number of degrees of freedom (in FE-model)
	NFMT   = node freedom map table
	'''
		self.F = np.zeros((nDOFs,1))

		number_of_nodes = len(self.nodes)
		vectMag = sqrt(self.vector[0][0]**2 + self.vector[1][0]**2 + self.vector[2][0]**2)
		f1_cos = self.vector[0][0]/vectMag
		f2_cos = self.vector[1][0]/vectMag
		f3_cos = self.vector[2][0]/vectMag

		for i in range(number_of_nodes):
			self.F[NFMT[self.nodes[i]]] = (self.force*f1_cos)/number_of_nodes
			self.F[NFMT[self.nodes[i]]+1] = (self.force*f2_cos)/number_of_nodes
			if self.vector[2][0] != 0.0:
				self.F[NFMT[self.nodes[i]]+2] = (self.force*f3_cos)/number_of_nodes




class Acceleration(Load):
	'''
Class for one dynamic acceleration vector applied
to all nodes in specified nodeset.
'''
	def __init__(self,name,nodeset,factor,v1,v2,v3=0.0):
		self.type = 'Acceleration'
		self.accel_factor = factor
		self.vector = [[float(v1)],[float(v2)],[float(v3)]]
		super(Acceleration,self).__init__(name,nodeset)


	def calcDegreeOfFreedomForces(self,nDOFs,NFMT):
		'''
	Calculate the force contribution on each individual
	degree of freedom based on affected nodes, force and
	force vector.
	self.F = acceleration vector
	nDOFs  = number of degrees of freedom (in FE-model)
	NFMT   = node freedom map table
	'''
		self.F = np.zeros((nDOFs,1))

		number_of_nodes = len(self.nodes)
		vectMag = sqrt(self.vector[0][0]**2 + self.vector[1][0]**2 + self.vector[2][0]**2)
		f1_cos = self.vector[0][0]/vectMag
		f2_cos = self.vector[1][0]/vectMag
		f3_cos = self.vector[2][0]/vectMag

		for i in range(number_of_nodes):
			self.F[NFMT[self.nodes[i]]] = (self.accel_factor*f1_cos)
			self.F[NFMT[self.nodes[i]]+1] = (self.accel_factor*f2_cos)
			if self.vector[2][0] != 0.0:
				self.F[NFMT[self.nodes[i]]+2] = (self.accel_factor*f3_cos)




class Torque(Load):
	'''
Class for concentrated torque load
applied to each individual node in
specified nodeset.
'''
	def __init__(self,name,nodeset,torque,m1,m2,m3):
		self.type = 'Torque'
		self.torque = torque
		self.moment = [[float(m1)],[float(m2)],[float(m3)]]
		super(Torque,self).__init__(name,nodeset)


	def calcDegreeOfFreedomForces(self,nDOFs,NFMT,nodes):
		'''
	Apply the force contribution on each individual
	degree of freedom separately.
	self.F 			= force vector
	nDOFs  			= number of degrees of freedom (in FE-model)
	NFMT			= node freedom map table
	nodes[node].NFS = node freedom signature
	'''
		self.F = np.zeros((nDOFs,1))

		number_of_nodes = len(self.nodes)
		momentMag = sqrt(self.moment[0][0]**2 + self.moment[1][0]**2 + self.moment[2][0]**2)
		m1_cos = self.moment[0][0]/momentMag
		m2_cos = self.moment[1][0]/momentMag
		m3_cos = self.moment[2][0]/momentMag

		for i in range(number_of_nodes):
			if 1 not in nodes[self.nodes[i]].NFS[3:]:
				print('\n\tWARNING!!! \n\tCannot apply moment to node '+str(self.nodes[i])+'.',
					  'It only has translational DOFs.')
			elif nodes[self.nodes[i]].NFS == [1,1,0,0,0,1]:
				self.F[NFMT[self.nodes[i]]+2] = self.torque*m3_cos
			elif nodes[self.nodes[i]].NFS == [1,1,1,1,1,1]:
				self.F[NFMT[self.nodes[i]]+3] = self.torque*m1_cos
				self.F[NFMT[self.nodes[i]]+4] = self.torque*m2_cos
				self.F[NFMT[self.nodes[i]]+5] = self.torque*m3_cos
			else:
				print('\n\tWARNING!!! \n\tUnknown DOFs for node '+str(self.nodes[i])+'.',
					  'No torque applied.')




class Pressure(Load):	# NOT READY TO BE USED
	'''
Class for pressure load applied
to a set of plate elements.
'''
	def __init__(self,name,nodes,pressure,v1,v2,v3=0.0):
		self.type = 'Pressure'
		self.pressure = pressure
		self.vector = [[float(v1)],[float(v2)],[float(v3)]]
		super(Pressure,self).__init__(name,nodes)




class ForceDistributed(Load):
	'''
Class for distributed load applied
to a set of beam elements.
'''
	def __init__(self,name,elementset,force,v1,v2,v3=0.0):
		self.type = 'ForceDistributed'
		self.force = force
		self.elementset = elementset
		self.vector = [[float(v1)],[float(v2)],[float(v3)]]
		super(ForceDistributed,self).__init__(name,elementset)


	def calcDegreeOfFreedomForces(self,nDOFs,NFMT,elements,fixedDOFs,MPCs):
		'''
	Apply the force contribution on each individual
	degree of freedom separately.
	self.F = force vector
	nDOFs  = number of degrees of freedom (in FE-model)
	NFMT   = node freedom map table
	'''
		self.F = np.zeros((nDOFs,1))

		vectMag = sqrt(self.vector[0][0]**2 + self.vector[1][0]**2 + self.vector[2][0]**2)
		distForce = [self.force*self.vector[0][0]/vectMag,
					 self.force*self.vector[1][0]/vectMag,
					 self.force*self.vector[2][0]/vectMag]

		is2D = False
		self.nodes = {}
		for element in self.elementset:
			if elements[element].type == 'BEAM2N2D':
				elmDOFs = 6
				is2D = True
			else:
				elmDOFs = 12
			# check if node DOFs are free or not
			freeDOFs = [0]*elmDOFs
			# first check if both nodes are connected to other elements
			for element2 in elements:
				if element2 != element:
					if elements[element2].nodes[0].number == elements[element].nodes[0].number or \
								elements[element2].nodes[1].number == elements[element].nodes[0].number:
						if elmDOFs == 6:
							freeDOFs[0] = freeDOFs[1] = freeDOFs[2] = 1
						if elmDOFs == 12:
							freeDOFs[0] = freeDOFs[1] = freeDOFs[2] = freeDOFs[3] = freeDOFs[4] = freeDOFs[5] = 1
					if elements[element2].nodes[0].number == elements[element].nodes[1].number or \
								elements[element2].nodes[1].number == elements[element].nodes[1].number:
						if elmDOFs == 6:
							freeDOFs[3] = freeDOFs[4] = freeDOFs[5] = 1
						if elmDOFs == 12:
							freeDOFs[6] = freeDOFs[7] = freeDOFs[8] = freeDOFs[9] = freeDOFs[10] = freeDOFs[11] = 1
			# if not, check if nodes are restrained by boundary conditions or constraints (and in which DOFs)
			if 0 in freeDOFs:
				n1_dofs = [NFMT[elements[element].nodes[0].number]+i for i in range(int(elmDOFs/2))]
				for i, dof in enumerate(n1_dofs):
					if dof in fixedDOFs:
						freeDOFs[i] = 1
					else:
						for mpc in MPCs:
							if dof in MPCs[mpc]:
								freeDOFs[i] = 1
				n2_dofs = [NFMT[elements[element].nodes[1].number]+i for i in range(int(elmDOFs/2))]
				for i, dof in enumerate(n2_dofs):
					if dof in fixedDOFs:
						freeDOFs[i+int(elmDOFs/2)] = 1
					else:
						for mpc in MPCs:
							if dof in MPCs[mpc]:
								freeDOFs[i+int(elmDOFs/2)] = 1

			elements[element].calcEquivalentNodalForces(distForce,freeDOFs)
			if is2D:
				if elements[element].nodes[0].number not in self.nodes:
					self.nodes[elements[element].nodes[0].number] = elements[element].eqNodeForces[:3]
				else:
					self.nodes[elements[element].nodes[0].number] += elements[element].eqNodeForces[:3]
				if elements[element].nodes[1].number not in self.nodes:
					self.nodes[elements[element].nodes[1].number] = elements[element].eqNodeForces[3:]
				else:
					self.nodes[elements[element].nodes[1].number] += elements[element].eqNodeForces[3:]
			else:
				if elements[element].nodes[0].number not in self.nodes:
					self.nodes[elements[element].nodes[0].number] = elements[element].eqNodeForces[:6]
				else:
					self.nodes[elements[element].nodes[0].number] += elements[element].eqNodeForces[:6]
				if elements[element].nodes[1].number not in self.nodes:
					self.nodes[elements[element].nodes[1].number] = elements[element].eqNodeForces[6:]
				else:
					self.nodes[elements[element].nodes[1].number] += elements[element].eqNodeForces[6:]

		for node in self.nodes:
			if is2D:
				self.F[NFMT[node]] += self.nodes[node][0]
				self.F[NFMT[node]+1] += self.nodes[node][1]
				self.F[NFMT[node]+2] += self.nodes[node][2]
			else:
				self.F[NFMT[node]] += self.nodes[node][0]
				self.F[NFMT[node]+1] += self.nodes[node][1]
				self.F[NFMT[node]+2] += self.nodes[node][2]
				self.F[NFMT[node]+3] += self.nodes[node][3]
				self.F[NFMT[node]+4] += self.nodes[node][4]
				self.F[NFMT[node]+5] += self.nodes[node][5]




class Gravity(Load):
	'''
Class for gravity load applied to
a set of elements.
'''
	def __init__(self,name,elementset,acceleration,v1,v2,v3=0.0):
		self.type = 'Gravity'
		self.acceleration = acceleration
		self.elementset = elementset
		self.vector = [[float(v1)],[float(v2)],[float(v3)]]
		super(Gravity,self).__init__(name,elementset)


	def calcDegreeOfFreedomForces(self,nDOFs,NFMT,elements):
		'''
	Apply the force contribution on each individual
	degree of freedom separately.
	self.F = force vector
	nDOFs = number of degrees of freedom (in FE-model)
	NFMT = node freedom map table
	'''
		self.F = np.zeros((nDOFs,1))

		self.nodes = {}
		for element in self.elementset:
			if hasattr(elements[element],'M'):
				pass
			else:
				elements[element].calcMassMatrix()
			for node in elements[element].nodes:
				if node.number in self.nodes:
					self.nodes[node.number] += elements[element].M[0][0]
				else:
					self.nodes[node.number] = elements[element].M[0][0]

		vectMag = sqrt(self.vector[0][0]**2 + self.vector[1][0]**2 + self.vector[2][0]**2)
		f1_cos = self.vector[0][0]/vectMag
		f2_cos = self.vector[1][0]/vectMag
		f3_cos = self.vector[2][0]/vectMag

		for node in self.nodes:
			self.F[NFMT[node]] = self.acceleration*self.nodes[node]*f1_cos
			self.F[NFMT[node]+1] = self.acceleration*self.nodes[node]*f2_cos
			if self.vector[2][0] != 0.0:
				self.F[NFMT[node]+2] = self.acceleration*self.nodes[node]*f3_cos

		




