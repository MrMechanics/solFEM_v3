#
#
#	elements.py
#  -------------
#
#	This file holds the element objects. Element objects calculate
#	element stiffness matrices which are used in the global stiffness
#	matrix. They also use displacements from the solution to calculate
#	stress and strain values.
#


import numpy as np
from math import sqrt






class GaussQuad(object):
	'''
Gauss integration rules listed for easy
access to individual element integration
- quad for quad and hex elements
- tri for triangle elements
- tet for tetrahedral elements
'''
	def __init__(self):
		self.quad_p1 = [[0.0,2.0],]
		self.quad_p2 = [[-0.5773502691896258, 1.0], [0.5773502691896258, 1.0]]
		self.quad_p3 = [[-0.7745966692414834, 0.5555555555555556],
						[0.0, 0.8888888888888888],
						[0.7745966692414834, 0.5555555555555556]]
		self.quad_p4 = [[-0.8611363115940526, 0.34785484513745385],
			 			[-0.3399810435848563, 0.65214515486254610],
			 			[ 0.3399810435848563, 0.65214515486254610],
			 			[ 0.8611363115940526, 0.34785484513745385]]
		self.tri_p3 = [[0.666666667, 0.166666667, 0.166666667],
					   [0.166666667, 0.666666667, 0.166666667],
					   [0.166666667, 0.166666667, 0.666666667],
					    0.333333333]
		self.tet_p4 = [[0.585410196624968, 0.138196601125011, 0.138196601125011, 0.138196601125011],
					   [0.138196601125011, 0.585410196624968, 0.138196601125011, 0.138196601125011],
					   [0.138196601125011, 0.138196601125011, 0.585410196624968, 0.138196601125011],
					   [0.138196601125011, 0.138196601125011, 0.138196601125011, 0.585410196624968], 
					    0.25]





class Element(object):
	'''
Base class for all elements. Contains elements number,
section properties and nodes listed in an array.
'''
	def __init__(self,number,sect,nodes):
		self.number = number
		self.section = sect
		self.nodes = nodes
		self.solutions = {}


	def elementFreedomTable(self,NFAT,NFMT):
		'''
	Create element freedom table for mapping element
	stiffness (or mass) matrix into global stiffness
	(or mass) matrix.
	self.EFT		- element freedom table
	self.EFS		- element freedom signature
	self.nodes.NFS	- node freedom signature
	NFMT			- nodes freedom map table
	'''
		nodeNum = len(self.nodes)
		self.EFT = []
		for j in range(nodeNum):
			n = 0
			for k in range(6):
				if NFAT[self.nodes[j].number][k] == 1:
					if self.EFS[j][k] == 1:
						self.EFT.append(NFMT[self.nodes[j].number]+n)
					n += 1





class MASS1N(Element):	# NOT READY TO BE USED
	'''
Class for 1 node point arbitrary mass element.
Has between 1 and 6 active degrees of freedom.
'''
	def __init__(self,number,sect,nodes,mass):
		super(MASS1N,self).__init__(number,sect,nodes)
		self.EFS = [[1,1,0,0,0,0],]*1
		self.nodeFreedomSignature()
		self.type = 'MASS1N'


	def nodeFreedomSignature(self):
		'''
	Update node freedom signature for nodes in element.
	'''
		for i in range(len(self.nodes[0])):
			if self.nodes[0].NFS[i] == 0:
				self.nodes[0].NFS[i] = 1





class DAMP2N(Element):	# NOT READY TO BE USED
	'''
Class for 2 node arbitrary damping element.
Has between 2 and 12 active degrees of freedom.
'''
	def __init__(self,number,sect,nodes,stiffness,damping):
		super(DAMP2N,self).__init__(number,sect,nodes)
		self.EFS = [[1,1,0,0,0,0],]*2
		self.nodeFreedomSignature()
		self.type = 'DAMP2N'


	def nodeFreedomSignature(self):
		'''
	Update node freedom signature for nodes in element.
	'''
		for i in range(len(self.nodes)):
			if self.nodes[i].NFS[0] == 0:
				self.nodes[i].NFS[0] = 1





class STIFF2N(Element):	# NOT READY TO BE USED
	'''
Class for 2 node arbitrary stiffness element.
Has between 2 and 12 active degrees of freedom.
'''
	def __init__(self,number,sect,nodes,stiffness):
		super(DAMP2N,self).__init__(number,sect,nodes)
		self.EFS = [[1,1,0,0,0,0],]*2
		self.nodeFreedomSignature()
		self.type = 'STIFF2N'


	def nodeFreedomSignature(self):
		'''
	Update node freedom signature for nodes in element.
	'''
		for i in range(len(self.nodes)):
			if self.nodes[i].NFS[0] == 0:
				self.nodes[i].NFS[0] = 1




class ROD2N2D(Element):
	'''
Class for 2D rod element.
Has two active degrees of freedom per node.
2 nodes gives 4 degrees of freedom total.
'''
	def __init__(self,number,sect,nodes):
		super(ROD2N2D,self).__init__(number,sect,nodes)
		self.EFS = [[1,1,0,0,0,0],]*2
		self.nodeFreedomSignature()
		self.type = 'ROD2N2D'
		self.setOrientation()



	def setOrientation(self,orient='None'):
		'''
	Sets the element orientation which is used
	when rendering element in viewer if cross
	section has been specified for section.
	
	If orient == 'None', the orientation is set
	to a default, where the two nodes define the
	local x-vector to be [x2-x1, y2-y1].
	
	orient = {'x-vec': [x, y]}	x-vector specified by user
	'''
		x21 = self.nodes[1].coord[0][0]-self.nodes[0].coord[0][0]
		y21 = self.nodes[1].coord[1][0]-self.nodes[0].coord[1][0]

		self.length = sqrt(x21**2 + y21**2)

		if orient != 'None':
			if x21 < 0. and orient['x-vec'][0] < 0.:
				xv = np.array([x21, y21, 0.])
			elif x21 >= 0. and orient['x-vec'][0] >= 0.:
				xv = np.array([x21, y21, 0.])
			else:
				self.nodes[0], self.nodes[1] = self.nodes[1], self.nodes[0]
				x21 = self.nodes[1].coord[0][0]-self.nodes[0].coord[0][0]
				y21 = self.nodes[1].coord[1][0]-self.nodes[0].coord[1][0]
				xv = np.array([x21, y21, 0.])
			xu = xv/self.length
		else:
			xv = np.array([x21, y21, 0.])
			xu = xv/self.length

		zu = np.array([0.,0.,1.])
		yu = np.cross(zu,xu)
		self.orientation = {'x-vec': xu,
							'y-vec': yu,
							'z-vec': zu}


	def nodeFreedomSignature(self):
		'''
	Update node freedom signature for nodes in element.
	'''
		for i in range(len(self.nodes)):
			if self.nodes[i].NFS[0] == 0:
				self.nodes[i].NFS[0] = 1
			if self.nodes[i].NFS[1] == 0:
				self.nodes[i].NFS[1] = 1


	def calcStiffnessMatrix(self):
		'''
	Calculate the element stiffness matrix.
	'''
		dx = self.nodes[1].coord[0][0]-self.nodes[0].coord[0][0]
		dy = self.nodes[1].coord[1][0]-self.nodes[0].coord[1][0]

		self.length = sqrt(dx**2 + dy**2)
		c = dx/self.length
		s = dy/self.length

		self.T_elm = np.array([[ c**2,   c*s, -c**2,  -c*s],
							   [  c*s,  s**2,  -s*c, -s**2],
							   [-c**2,  -s*c,  c**2,   s*c],
							   [ -s*c, -s**2,   s*c,  s**2]])

		self.K = self.T_elm*(self.section.material.elastMod*self.section.area/self.length)


	def calcMassMatrix(self):
		'''
	Calculate the element mass matrix using the
	lumped mass matrix method.
	'''
		self.M = np.identity(4)*(self.section.material.density*self.section.area*self.length*0.5)


	def calcForces(self,u,sol):
		'''
	Calculate the internal element forces using
	the element stiffness matrix and the
	displacement vector.
	'''
		dx = self.nodes[1].coord[0][0]-self.nodes[0].coord[0][0]
		dy = self.nodes[1].coord[1][0]-self.nodes[0].coord[1][0]
		dxu = u[2] - u[0]
		dyu = u[3] - u[1]
		strain = dx*dxu + dy*dyu
		nodeforce = self.K.dot(u)
		self.solutions[sol]['elementforce'] = [0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0.]
		if strain < 0:
			self.solutions[sol]['elementforce'][0] = -sqrt(abs(nodeforce[0]**2 + nodeforce[1]**2))
		else:
			self.solutions[sol]['elementforce'][0] = sqrt(abs(nodeforce[0]**2 + nodeforce[1]**2))


	def calcStrain(self,u,calcStrain,calcStress,sol):
		'''
	Calculate the element stress and/or strain.
	'''
		dx = self.nodes[1].coord[0][0]-self.nodes[0].coord[0][0]
		dy = self.nodes[1].coord[1][0]-self.nodes[0].coord[1][0]
		dxu = u[2] - u[0]
		dyu = u[3] - u[1]
		strain = abs(dx*dxu + dy*dyu)
		stress = strain*self.section.material.elastMod
		if calcStrain == True:
			self.solutions[sol]['strain'] = {'nodal': {}}
			self.solutions[sol]['strain']['nodal'][1] = {'VonMises': strain, 'MaxPrinc': strain, 'MinPrinc': strain/2., 'MaxShear': strain/2.}
			self.solutions[sol]['strain']['nodal'][2] = {'VonMises': strain, 'MaxPrinc': strain, 'MinPrinc': strain/2., 'MaxShear': strain/2.}
		if calcStress == True:
			self.solutions[sol]['stress'] = {'nodal': {}}
			self.solutions[sol]['stress']['nodal'][1] = {'VonMises': stress, 'MaxPrinc': stress, 'MinPrinc': stress/2., 'MaxShear': stress/2.}
			self.solutions[sol]['stress']['nodal'][2] = {'VonMises': stress, 'MaxPrinc': stress, 'MinPrinc': stress/2., 'MaxShear': stress/2.}




class BEAM2N2D(Element):
	'''
Class for 2D beam element.
Has three active degrees of fredom per node.
2 nodes gives 6 degrees of freedom total.
'''
	def __init__(self,number,sect,nodes):
		super(BEAM2N2D,self).__init__(number,sect,nodes)
		self.EFS = [[1,1,0,0,0,1],]*2
		self.nodeFreedomSignature()
		self.type = 'BEAM2N2D'


	def setOrientation(self,orient='None'):
		'''
	Sets the element orientation which is used
	when calculating the stiffness matrix.
	
	If orient == 'None', the orientation is set
	to a default, where the two nodes define the
	local x-vector to be [x2-x1, y2-y1].
	
	orient = {'x-vec': [x, y]}	x-vector specified by user
	'''
		x21 = self.nodes[1].coord[0][0]-self.nodes[0].coord[0][0]
		y21 = self.nodes[1].coord[1][0]-self.nodes[0].coord[1][0]

		self.length = sqrt(x21**2 + y21**2)

		if orient != 'None':
			if x21 < 0. and orient['x-vec'][0] < 0.:
				xv = np.array([x21, y21, 0.])
			elif x21 >= 0. and orient['x-vec'][0] >= 0.:
				xv = np.array([x21, y21, 0.])
			else:
				self.nodes[0], self.nodes[1] = self.nodes[1], self.nodes[0]
				x21 = self.nodes[1].coord[0][0]-self.nodes[0].coord[0][0]
				y21 = self.nodes[1].coord[1][0]-self.nodes[0].coord[1][0]
				xv = np.array([x21, y21, 0.])
			xu = xv/self.length
		else:
			xv = np.array([x21, y21, 0.])
			xu = xv/self.length

		zu = np.array([0.,0.,1.])
		yu = np.cross(zu,xu)
		self.orientation = {'x-vec': xu,
							'y-vec': yu,
							'z-vec': zu}

		txx = xu[0]
		txy = xu[1]
		tyx = yu[0]
		tyy = yu[1]
		self.T_elm = np.array([[txx, txy, 0,   0,   0, 0],
							   [tyx, tyy, 0,   0,   0, 0],
							   [  0,   0, 1,   0,   0, 0],
							   [  0,   0, 0, txx, txy, 0],
							   [  0,   0, 0, tyx, tyy, 0],
							   [  0,   0, 0,   0,   0, 1]])


	def nodeFreedomSignature(self):
		'''
	Update node freedom signature for nodes in element.
	'''
		for i in range(len(self.nodes)):
			if self.nodes[i].NFS[0] == 0:
				self.nodes[i].NFS[0] = 1
			if self.nodes[i].NFS[1] == 0:
				self.nodes[i].NFS[1] = 1
			if self.nodes[i].NFS[5] == 0:
				self.nodes[i].NFS[5] = 1


	def calcStiffnessMatrix(self):
		'''
	Calculate the element stiffness matrix.
	'''
		L = self.length
		EA_L  = (self.section.material.elastMod*self.section.area)/self.length
		EI_L3 = (self.section.material.elastMod*self.section.Izz)/(self.length**3)

		K_beam1 = EA_L*np.array([[ 1, 0, 0,-1, 0, 0],
							     [ 0, 0, 0, 0, 0, 0],
							     [ 0, 0, 0, 0, 0, 0],
							     [-1, 0, 0, 1, 0, 0],
							   	 [ 0, 0, 0, 0, 0, 0],
							     [ 0, 0, 0, 0, 0, 0]]) 
		K_beam2 = EI_L3*np.array([[ 0,   0,      0, 0,    0,      0],
							      [ 0,  12,    6*L, 0,  -12,    6*L],
							      [ 0, 6*L, 4*L**2, 0, -6*L, 2*L**2],
							      [ 0,   0,      0, 0,    0,      0],
							   	  [ 0, -12,   -6*L, 0,   12,   -6*L],
							      [ 0, 6*L, 2*L**2, 0, -6*L, 4*L**2]])
		K_beam = K_beam1+K_beam2

		self.K = ((self.T_elm.transpose().dot(K_beam)).dot(self.T_elm))


	def calcMassMatrix(self):
		'''
	Calculate the element mass matrix using the
	lumped mass matrix method.
	'''
		self.M = np.identity(6)*(self.section.material.density*self.section.area*self.length*0.5)
		self.M[2][2] = self.M[2][2]*((self.length**2)/12)
		self.M[5][5] = self.M[5][5]*((self.length**2)/12)


	def calcEquivalentNodalForces(self,distForce,freeDOFs):
		'''
	Calculate the equivalent nodal forces from
	a distributed load on element.
	distForce 			   - force vector per element length
	self.eqNodeForcesLocal - equivalent node forces in local
							 reference frame
	self.eqNodeForces	   - equivalent node forces in global
							 reference frame
	'''
		F = np.dot(self.T_elm[:3,:3],distForce)
		if freeDOFs in [[1,1,1,1,1,1],[0,0,0,1,1,1],[1,1,1,0,0,0]]:
			self.eqNodeForcesLocal = [ F[0]*self.length/2.,		   # fx1
									   F[1]*self.length/2.,		   # fy1
									   F[1]*(self.length**2)/12.,  # mz1
									   F[0]*self.length/2.,		   # fx2
									   F[1]*self.length/2.,		   # fy2
								 	  -F[1]*(self.length**2)/12. ] # mz2
		elif freeDOFs in [[1,1,1,1,1,0],[1,1,1,1,0,0],[1,1,1,0,1,0]]:
			self.eqNodeForcesLocal = [ F[0]*self.length/2.,		   # fx1
									   F[1]*self.length*5./8.,	   # fy1
									   F[1]*(self.length**2)/8.,   # mz1
									   F[0]*self.length/2.,		   # fx2
									   F[1]*self.length*3./8.,	   # fy2
								 	   0. ] 					   # mz2
		elif freeDOFs in [[1,1,0,1,1,1],[1,0,0,1,1,1],[0,1,0,1,1,1]]:
			self.eqNodeForcesLocal = [ F[0]*self.length/2.,		   # fx1
									   F[1]*self.length*3./8.,	   # fy1
									   0.,  					   # mz1
									   F[0]*self.length/2.,		   # fx2
									   F[1]*self.length*5./8.,	   # fy2
								 	  -F[1]*(self.length**2)/8. ]  # mz2
		elif freeDOFs in [[1,1,0,1,1,0],[1,0,0,1,1,0],[0,1,0,1,1,0],[1,1,0,0,1,0],[1,1,0,1,0,0]]:
			self.eqNodeForcesLocal = [ F[0]*self.length/2.,		   # fx1
									   F[1]*self.length/2.,		   # fy1
									   0.,						   # mz1
									   F[0]*self.length/2.,		   # fx2
									   F[1]*self.length/2.,		   # fy2
								 	   0. ] 					   # mz2
		else:
			print('\n\tUnknown element configuration for equivalent nodal forces in element', self.number)
		self.eqNodeForces = np.linalg.inv(self.T_elm).dot(self.eqNodeForcesLocal)


	def calcForces(self,u,sol):
		'''
	Calculate the internal element forces using
	the element stiffness matrix and the
	displacement vector.
	'''
		u_local = np.dot(self.T_elm,u)
		K = self.T_elm.dot(self.K).dot(self.T_elm.T)
		nodeforce = K.dot(u_local)
		self.solutions[sol]['elementforce'] = [0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0.]
		self.solutions[sol]['elementforce'][0] = ((self.section.area*self.section.material.elastMod)/self.length)*(u_local[3]-u_local[0])
		self.solutions[sol]['elementforce'][1] = nodeforce[1]
		self.solutions[sol]['elementforce'][5] = nodeforce[2]
		self.solutions[sol]['elementforce'][6] = nodeforce[4]
		self.solutions[sol]['elementforce'][10] = nodeforce[5]

		if hasattr(self,'eqNodeForcesLocal'):
			self.solutions[sol]['elementforce'][0] += self.eqNodeForcesLocal[0]
			self.solutions[sol]['elementforce'][1] -= self.eqNodeForcesLocal[1]
			self.solutions[sol]['elementforce'][5] -= self.eqNodeForcesLocal[2]
			self.solutions[sol]['elementforce'][6] -= self.eqNodeForcesLocal[4]
			self.solutions[sol]['elementforce'][10] -= self.eqNodeForcesLocal[5]


	def calcStrain(self,u,calcStrain,calcStress,sol):	# NOT READY
		'''
	Calculate the element stress and/or strain.
	Currently beyond the scope of this program.
	'''
		strain = np.nan
		stress = np.nan
		if calcStrain == True:
			self.solutions[sol]['strain'] = {'nodal': {}}
			self.solutions[sol]['strain']['nodal'][1] = {'VonMises': strain, 'MaxPrinc': strain, 'MinPrinc': strain/2., 'MaxShear': strain/2.}
			self.solutions[sol]['strain']['nodal'][2] = {'VonMises': strain, 'MaxPrinc': strain, 'MinPrinc': strain/2., 'MaxShear': strain/2.}
		if calcStress == True:
			self.solutions[sol]['stress'] = {'nodal': {}}
			self.solutions[sol]['stress']['nodal'][1] = {'VonMises': stress, 'MaxPrinc': stress, 'MinPrinc': stress/2., 'MaxShear': stress/2.}
			self.solutions[sol]['stress']['nodal'][2] = {'VonMises': stress, 'MaxPrinc': stress, 'MinPrinc': stress/2., 'MaxShear': stress/2.}





class TRI3N(Element):
	'''
Class for triangular 3-node 2D element.
Has two active degrees of freedom per node.
3 nodes gives 6 degrees of freedom total.
This is the CST element (constant strain
triangle element). It has the same strain
value everywhere on the element.
'''
	def __init__(self,number,sect,nodes):
		super(TRI3N,self).__init__(number,sect,nodes)
		self.EFS = [[1,1,0,0,0,0],]*3
		self.nodeFreedomSignature()
		self.type = 'TRI3N'


	def nodeFreedomSignature(self):
		'''
	Update node freedom signature for nodes in element.
	'''
		for i in range(len(self.nodes)):
			if self.nodes[i].NFS[0] == 0:
				self.nodes[i].NFS[0] = 1
			if self.nodes[i].NFS[1] == 0:
				self.nodes[i].NFS[1] = 1


	def calcStrainDisplacementMatrix(self):
		'''
	Calculate the B-matrix given specific node coordinates.
	'''
		A = (self.nodes[1].coord[0][0]*self.nodes[2].coord[1][0] - \
			 self.nodes[2].coord[0][0]*self.nodes[1].coord[1][0] + \
			 self.nodes[2].coord[0][0]*self.nodes[0].coord[1][0] - \
			 self.nodes[0].coord[0][0]*self.nodes[2].coord[1][0] + \
			 self.nodes[0].coord[0][0]*self.nodes[1].coord[1][0] - \
			 self.nodes[1].coord[0][0]*self.nodes[0].coord[1][0])*0.5

		tempVal = 0.5/A
		B = np.array([[self.nodes[1].coord[1][0]-self.nodes[2].coord[1][0],0.0,
					   self.nodes[2].coord[1][0]-self.nodes[0].coord[1][0],0.0,
					   self.nodes[0].coord[1][0]-self.nodes[1].coord[1][0],0.0],
					  [0.0,self.nodes[2].coord[0][0]-self.nodes[1].coord[0][0],
					   0.0,self.nodes[0].coord[0][0]-self.nodes[2].coord[0][0],
					   0.0,self.nodes[1].coord[0][0]-self.nodes[0].coord[0][0]],
					  [self.nodes[2].coord[0][0]-self.nodes[1].coord[0][0],
					   self.nodes[1].coord[1][0]-self.nodes[2].coord[1][0],
					   self.nodes[0].coord[0][0]-self.nodes[2].coord[0][0],
					   self.nodes[2].coord[1][0]-self.nodes[0].coord[1][0],
					   self.nodes[1].coord[0][0]-self.nodes[0].coord[0][0],
					   self.nodes[0].coord[1][0]-self.nodes[1].coord[1][0]]])*tempVal

		return [A,B]


	def calcStiffnessMatrix(self):
		'''
	Calculate the element stiffness matrix.
	'''
		[A,B] = self.calcStrainDisplacementMatrix()
		self.K = ((B.transpose().dot(self.section.E)).dot(B))*(A*self.section.thickness)


	def calcMassMatrix(self):
		'''
	Calculate the element mass matrix using the
	lumped mass matrix method.
	'''
		area = abs(self.nodes[0].coord[0][0]*(self.nodes[1].coord[1][0]-self.nodes[2].coord[1][0]) + \
				   self.nodes[1].coord[0][0]*(self.nodes[2].coord[1][0]-self.nodes[0].coord[1][0]) + \
				   self.nodes[2].coord[0][0]*(self.nodes[0].coord[1][0]-self.nodes[1].coord[1][0]))*0.5
		self.M = np.identity(6)*(self.section.material.density*area*self.section.thickness*(1.0/3.0))


	def calcStrain(self,u,calcStrain,calcStress,sol):
		'''
	Use the element strain-displacement matrix and 
	node displacements to find stresses and strains
	in element at integration points and at nodes.
	This is the CST (constant strain triangle), so
	it only has one constant stress/strain for the
	whole element.
	'''
		if calcStrain == True:
			self.solutions[sol]['strain'] = {'nodal': {}}
		if calcStress == True:
			self.solutions[sol]['stress'] = {'nodal': {}}

		[A,B] = self.calcStrainDisplacementMatrix()

		if calcStrain:
			self.solutions[sol]['strain']['nodal'][1] = {'strain_tensor': B.dot(u), 
									'VonMises': 0., 'MaxPrinc': 0., 'MinPrinc': 0., 'MaxShear': 0.}
			self.solutions[sol]['strain']['nodal'][2] = self.solutions[sol]['strain']['nodal'][1]
			self.solutions[sol]['strain']['nodal'][3] = self.solutions[sol]['strain']['nodal'][1]
		if calcStress:
			self.solutions[sol]['stress']['nodal'][1] = {'stress_tensor': self.section.E.dot(B.dot(u)), 
									'VonMises': 0., 'MaxPrinc': 0., 'MinPrinc': 0., 'MaxShear': 0.}
			self.solutions[sol]['stress']['nodal'][2] = self.solutions[sol]['stress']['nodal'][1]
			self.solutions[sol]['stress']['nodal'][3] = self.solutions[sol]['stress']['nodal'][1]

		if calcStrain == True:
			e = self.solutions[sol]['strain']['nodal']
			e[1]['VonMises'] = sqrt(e[1]['strain_tensor'][0]**2 - e[1]['strain_tensor'][0]*e[1]['strain_tensor'][1] + \
					   e[1]['strain_tensor'][1]**2 + 3*e[1]['strain_tensor'][2]**2)
			e[1]['MaxPrinc'] = (e[1]['strain_tensor'][0] + e[1]['strain_tensor'][1])/2.0 + \
						sqrt(((e[1]['strain_tensor'][0] - e[1]['strain_tensor'][1])/2.0)**2 + \
						e[1]['strain_tensor'][2]**2)
			e[1]['MinPrinc'] = (e[1]['strain_tensor'][0] + e[1]['strain_tensor'][1])/2.0 - \
						sqrt(((e[1]['strain_tensor'][0] - e[1]['strain_tensor'][1])/2.0)**2 + \
						e[1]['strain_tensor'][2]**2)
			e[1]['MaxShear'] = (e[1]['MaxPrinc']-e[1]['MinPrinc'])/2.0

		if calcStress == True:
			s = self.solutions[sol]['stress']['nodal']
			s[1]['VonMises'] = sqrt(s[1]['stress_tensor'][0]**2 - s[1]['stress_tensor'][0]*s[1]['stress_tensor'][1] + \
					   s[1]['stress_tensor'][1]**2 + 3*s[1]['stress_tensor'][2]**2)
			s[1]['MaxPrinc'] = (s[1]['stress_tensor'][0] + s[1]['stress_tensor'][1])/2.0 + \
						sqrt(((s[1]['stress_tensor'][0] - s[1]['stress_tensor'][1])/2.0)**2 + \
						s[1]['stress_tensor'][2]**2)
			s[1]['MinPrinc'] = (s[1]['stress_tensor'][0] + s[1]['stress_tensor'][1])/2.0 - \
						sqrt(((s[1]['stress_tensor'][0] - s[1]['stress_tensor'][1])/2.0)**2 + \
						s[1]['stress_tensor'][2]**2)
			s[1]['MaxShear'] = (s[1]['MaxPrinc']-s[1]['MinPrinc'])/2.0





class TRI6N(Element):
	'''
Class for triangular 6-node 2D element.
Has two active degrees of freedom per node.
6 nodes gives 12 degrees of freedom total.
'''
	def __init__(self,number,sect,nodes,gaussQuad):
		self.gaussPnts = gaussQuad.tri_p3
		super(TRI6N,self).__init__(number,sect,nodes)
		self.EFS = [[1,1,0,0,0,0],]*6
		self.nodeFreedomSignature()
		self.type = 'TRI6N'


	def nodeFreedomSignature(self):
		'''
	Update node freedom signature for nodes in element.
	'''
		for i in range(len(self.nodes)):
			if self.nodes[i].NFS[0] == 0:
				self.nodes[i].NFS[0] = 1
			if self.nodes[i].NFS[1] == 0:
				self.nodes[i].NFS[1] = 1


	def calcStrainDisplacementMatrix(self,zeta1,zeta2,zeta3):
		'''
	Calculate the B-matrix given specific 
	shape function coordinates.
	'''
		dx4 = self.nodes[3].coord[0][0] - 0.5*(self.nodes[0].coord[0][0] + self.nodes[1].coord[0][0])
		dx5 = self.nodes[4].coord[0][0] - 0.5*(self.nodes[1].coord[0][0] + self.nodes[2].coord[0][0])
		dx6 = self.nodes[5].coord[0][0] - 0.5*(self.nodes[2].coord[0][0] + self.nodes[0].coord[0][0])

		dy4 = self.nodes[3].coord[1][0] - 0.5*(self.nodes[0].coord[1][0] + self.nodes[1].coord[1][0])
		dy5 = self.nodes[4].coord[1][0] - 0.5*(self.nodes[1].coord[1][0] + self.nodes[2].coord[1][0])
		dy6 = self.nodes[5].coord[1][0] - 0.5*(self.nodes[2].coord[1][0] + self.nodes[0].coord[1][0])

		Jx21 = self.nodes[1].coord[0][0] - self.nodes[0].coord[0][0] + 4.0*(dx4*(zeta1-zeta2) + (dx5-dx6)*zeta3)
		Jx32 = self.nodes[2].coord[0][0] - self.nodes[1].coord[0][0] + 4.0*(dx5*(zeta2-zeta3) + (dx6-dx4)*zeta1)
		Jx13 = self.nodes[0].coord[0][0] - self.nodes[2].coord[0][0] + 4.0*(dx6*(zeta3-zeta1) + (dx4-dx5)*zeta2)
		Jy12 = self.nodes[0].coord[1][0] - self.nodes[1].coord[1][0] + 4.0*(dy4*(zeta2-zeta1) + (dy6-dy5)*zeta3)
		Jy23 = self.nodes[1].coord[1][0] - self.nodes[2].coord[1][0] + 4.0*(dy5*(zeta3-zeta2) + (dy4-dy6)*zeta1)
		Jy31 = self.nodes[2].coord[1][0] - self.nodes[0].coord[1][0] + 4.0*(dy6*(zeta1-zeta3) + (dy5-dy4)*zeta2)

		detJ = Jx21*Jy31 - Jy12*Jx13
		invdetJ = 1.0/detJ

		dNf_drc = [[invdetJ*(4.0*zeta1-1.0)*Jy23,        invdetJ*(4.0*zeta2-1.0)*Jy31, 
					invdetJ*(4.0*zeta3-1.0)*Jy12,        invdetJ*4.0*(zeta2*Jy23+zeta1*Jy31),
					invdetJ*4.0*(zeta3*Jy31+zeta2*Jy12), invdetJ*4.0*(zeta1*Jy12+zeta3*Jy23)],
				   [invdetJ*(4.0*zeta1-1.0)*Jx32,        invdetJ*(4.0*zeta2-1.0)*Jx13, 
					invdetJ*(4.0*zeta3-1.0)*Jx21,        invdetJ*4.0*(zeta2*Jx32+zeta1*Jx13),
					invdetJ*4.0*(zeta3*Jx13+zeta2*Jx21), invdetJ*4.0*(zeta1*Jx21+zeta3*Jx32)]]

		B = [[],[],[]]
		for l in range(6):
			B[0].append(dNf_drc[0][l])
			B[0].append(0.0)
		for m in range(6):
			B[1].append(0.0)
			B[1].append(dNf_drc[1][m])
		for n in range(6):
			B[2].append(dNf_drc[1][n])
			B[2].append(dNf_drc[0][n])
		B = np.array(B)

		return [detJ,B]


	def calcStiffnessMatrix(self):
		'''
	Calculate the element stiffness matrix using
	isoparametric shape functions and Gauss Quadrature.
	'''
		self.K = np.array([[0.0,]*12,]*12)
		gauss = len(self.gaussPnts)-1
		zeta1 = 0.0
		zeta2 = 0.0
		zeta3 = 0.0
		w = self.gaussPnts[3]
		for i in range(gauss):
			zeta1 = self.gaussPnts[i][0]
			zeta2 = self.gaussPnts[i][1]
			zeta3 = self.gaussPnts[i][2]

			[detJ,B] = self.calcStrainDisplacementMatrix(zeta1,zeta2,zeta3)

			self.K = ((B.transpose().dot(self.section.E)).dot(B))*(w*detJ*self.section.thickness*0.5) + self.K


	def calcMassMatrix(self):
		'''
	Calculate the element mass matrix using the
	lumped mass matrix method.
	'''
		area = abs(self.nodes[0].coord[0][0]*(self.nodes[1].coord[1][0]-self.nodes[2].coord[1][0]) + \
				   self.nodes[1].coord[0][0]*(self.nodes[2].coord[1][0]-self.nodes[0].coord[1][0]) + \
				   self.nodes[2].coord[0][0]*(self.nodes[0].coord[1][0]-self.nodes[1].coord[1][0]))*0.5
		self.M = np.identity(12)*(self.section.material.density*area*self.section.thickness*(1.0/6.0))


	def calcStrain(self,u,calcStrain,calcStress,sol):
		'''
	Use the element strain-displacement matrix and 
	node displacements to find stresses and strains
	in element at integration points and at nodes.
	'''
		if calcStrain == True:
			self.solutions[sol]['strain'] = {'int_points': {}, 'nodal': {}}
		if calcStress == True:
			self.solutions[sol]['stress'] = {'int_points': {}, 'nodal': {}}

		gauss = len(self.gaussPnts)-1
		ngauss = gauss
		nodal = 6

		zeta1 = 0.0
		zeta2 = 0.0
		zeta3 = 0.0

		for i in range(gauss):
			zeta1 = self.gaussPnts[i][0]
			zeta2 = self.gaussPnts[i][1]
			zeta3 = self.gaussPnts[i][2]

			[detJ,B] = self.calcStrainDisplacementMatrix(zeta1,zeta2,zeta3)

			if calcStrain:
				self.solutions[sol]['strain']['int_points'][i+1] = {'strain_tensor': B.dot(u), 
											'VonMises': 0., 'MaxPrinc': 0., 'MinPrinc': 0., 'MaxShear': 0.}
			if calcStress:
				self.solutions[sol]['stress']['int_points'][i+1] = {'stress_tensor': self.section.E.dot(B.dot(u)), 
											'VonMises': 0., 'MaxPrinc': 0., 'MinPrinc': 0., 'MaxShear': 0.}
		
		zeta1zeta2zeta3 = [[ 1.0, 0.0, 0.0], [ 0.0, 1.0, 0.0], [ 0.0, 0.0, 1.0],
						   [ 0.5, 0.5, 0.0], [ 0.0, 0.5, 0.5], [ 0.5, 0.0, 0.5]]
		for j in range(nodal):
			zeta1 = zeta1zeta2zeta3[j][0]
			zeta2 = zeta1zeta2zeta3[j][1]
			zeta3 = zeta1zeta2zeta3[j][2]

			[detJ,B] = self.calcStrainDisplacementMatrix(zeta1,zeta2,zeta3)

			if calcStrain:
				self.solutions[sol]['strain']['nodal'][j+1] = {'strain_tensor': B.dot(u), 
									'VonMises': 0., 'MaxPrinc': 0., 'MinPrinc': 0., 'MaxShear': 0.}
			if calcStress:
				self.solutions[sol]['stress']['nodal'][j+1] = {'stress_tensor': self.section.E.dot(B.dot(u)), 
									'VonMises': 0., 'MaxPrinc': 0., 'MinPrinc': 0., 'MaxShear': 0.}

		if calcStrain == True:
			e = self.solutions[sol]['strain']['int_points']
			for i in range(ngauss):
				e[i+1]['VonMises'] = sqrt(e[i+1]['strain_tensor'][0]**2 - e[i+1]['strain_tensor'][0]*e[i+1]['strain_tensor'][1] + \
						   e[i+1]['strain_tensor'][1]**2 + 3*e[i+1]['strain_tensor'][2]**2)
				e[i+1]['MaxPrinc'] = (e[i+1]['strain_tensor'][0] + e[i+1]['strain_tensor'][1])/2.0 + \
							sqrt(((e[i+1]['strain_tensor'][0] - e[i+1]['strain_tensor'][1])/2.0)**2 + \
							e[i+1]['strain_tensor'][2]**2)
				e[i+1]['MinPrinc'] = (e[i+1]['strain_tensor'][0] + e[i+1]['strain_tensor'][1])/2.0 - \
							sqrt(((e[i+1]['strain_tensor'][0] - e[i+1]['strain_tensor'][1])/2.0)**2 + \
							e[i+1]['strain_tensor'][2]**2)
				e[i+1]['MaxShear'] = (e[i+1]['MaxPrinc']-e[i+1]['MinPrinc'])/2.0
			e = self.solutions[sol]['strain']['nodal']
			for i in range(nodal):
				e[i+1]['VonMises'] = sqrt(e[i+1]['strain_tensor'][0]**2 - e[i+1]['strain_tensor'][0]*e[i+1]['strain_tensor'][1] + \
						   e[i+1]['strain_tensor'][1]**2 + 3*e[i+1]['strain_tensor'][2]**2)
				e[i+1]['MaxPrinc'] = (e[i+1]['strain_tensor'][0] + e[i+1]['strain_tensor'][1])/2.0 + \
							sqrt(((e[i+1]['strain_tensor'][0] - e[i+1]['strain_tensor'][1])/2.0)**2 + \
							e[i+1]['strain_tensor'][2]**2)
				e[i+1]['MinPrinc'] = (e[i+1]['strain_tensor'][0] + e[i+1]['strain_tensor'][1])/2.0 - \
							sqrt(((e[i+1]['strain_tensor'][0] - e[i+1]['strain_tensor'][1])/2.0)**2 + \
							e[i+1]['strain_tensor'][2]**2)
				e[i+1]['MaxShear'] = (e[i+1]['MaxPrinc']-e[i+1]['MinPrinc'])/2.0

		if calcStress == True:
			s = self.solutions[sol]['stress']['int_points']
			for i in range(ngauss):
				s[i+1]['VonMises'] = sqrt(s[i+1]['stress_tensor'][0]**2 - s[i+1]['stress_tensor'][0]*s[i+1]['stress_tensor'][1] + \
						   s[i+1]['stress_tensor'][1]**2 + 3*s[i+1]['stress_tensor'][2]**2)
				s[i+1]['MaxPrinc'] = (s[i+1]['stress_tensor'][0] + s[i+1]['stress_tensor'][1])/2.0 + \
							sqrt(((s[i+1]['stress_tensor'][0] - s[i+1]['stress_tensor'][1])/2.0)**2 + \
							s[i+1]['stress_tensor'][2]**2)
				s[i+1]['MinPrinc'] = (s[i+1]['stress_tensor'][0] + s[i+1]['stress_tensor'][1])/2.0 - \
							sqrt(((s[i+1]['stress_tensor'][0] - s[i+1]['stress_tensor'][1])/2.0)**2 + \
							s[i+1]['stress_tensor'][2]**2)
				s[i+1]['MaxShear'] = (s[i+1]['MaxPrinc']-s[i+1]['MinPrinc'])/2.0
			s = self.solutions[sol]['stress']['nodal']
			for i in range(nodal):
				s[i+1]['VonMises'] = sqrt(s[i+1]['stress_tensor'][0]**2 - s[i+1]['stress_tensor'][0]*s[i+1]['stress_tensor'][1] + \
						   s[i+1]['stress_tensor'][1]**2 + 3*s[i+1]['stress_tensor'][2]**2)
				s[i+1]['MaxPrinc'] = (s[i+1]['stress_tensor'][0] + s[i+1]['stress_tensor'][1])/2.0 + \
							sqrt(((s[i+1]['stress_tensor'][0] - s[i+1]['stress_tensor'][1])/2.0)**2 + \
							s[i+1]['stress_tensor'][2]**2)
				s[i+1]['MinPrinc'] = (s[i+1]['stress_tensor'][0] + s[i+1]['stress_tensor'][1])/2.0 - \
							sqrt(((s[i+1]['stress_tensor'][0] - s[i+1]['stress_tensor'][1])/2.0)**2 + \
							s[i+1]['stress_tensor'][2]**2)
				s[i+1]['MaxShear'] = (s[i+1]['MaxPrinc']-s[i+1]['MinPrinc'])/2.0





class QUAD4N(Element):
	'''
Class for quadrilateral 4-node 2D element.
Has two active degrees of freedom per node.
4 nodes gives 8 degrees of freedom total.
'''
	def __init__(self,number,sect,nodes,gaussQuad,reducedIntegration=False):
		if reducedIntegration:
			self.gaussPnts = gaussQuad.quad_p1
			self.reducedIntegration = True
		else:
			self.gaussPnts = gaussQuad.quad_p2
			self.reducedIntegration = False
		super(QUAD4N,self).__init__(number,sect,nodes)
		self.EFS = [[1,1,0,0,0,0],]*4
		self.nodeFreedomSignature()
		self.type = 'QUAD4N'


	def nodeFreedomSignature(self):
		'''
	Update node freedom signature for nodes in element.
	'''
		for i in range(len(self.nodes)):
			if self.nodes[i].NFS[0] == 0:
				self.nodes[i].NFS[0] = 1
			if self.nodes[i].NFS[1] == 0:
				self.nodes[i].NFS[1] = 1


	def calcStrainDisplacementMatrix(self,ksi,eta):
		'''
	Calculate the B-matrix given specific
	shape function coordinates.
	'''
		dNf_dqc = np.array([[-(1.0-eta)/4.0, (1.0-eta)/4.0, (1.0+eta)/4.0, -(1.0+eta)/4.0],
				   			[-(1.0-ksi)/4.0, -(1.0+ksi)/4.0, (1.0+ksi)/4.0, (1.0-ksi)/4.0]])

		J = dNf_dqc.dot(np.array([[self.nodes[0].coord[0][0],self.nodes[0].coord[1][0]],
								  [self.nodes[1].coord[0][0],self.nodes[1].coord[1][0]],
								  [self.nodes[2].coord[0][0],self.nodes[2].coord[1][0]],
								  [self.nodes[3].coord[0][0],self.nodes[3].coord[1][0]]]))

		detJ = J[0][0]*J[1][1] - J[0][1]*J[1][0]
		invJ = np.array([[(1.0/detJ)*J[1][1],-(1.0/detJ)*J[0][1]],
						 [-(1.0/detJ)*J[1][0],(1.0/detJ)*J[0][0]]])

		dNf_drc = invJ.dot(dNf_dqc)

		B = [[],[],[]]
		for l in range(4):
			B[0].append(dNf_drc[0][l])
			B[0].append(0.0)
		for m in range(4):
			B[1].append(0.0)
			B[1].append(dNf_drc[1][m])
		for n in range(4):
			B[2].append(dNf_drc[1][n])
			B[2].append(dNf_drc[0][n])
		B = np.array(B)
		
		return [detJ,B]


	def hourGlassControl(self):
		'''
	Apply hourglass control. NOT READY TO USE!!!

	Method taken from "A UNIFORM STRAIN HEXAHEDRON 
	AND QUADRILATERAL WITH ORTHOGONAL HOURGLASS CONTROL"
	by D. P. FLANAGAN AND T. BELYTSCHKO
	'''
		x1 = self.nodes[0].coord[0][0]
		x2 = self.nodes[1].coord[0][0]
		x3 = self.nodes[2].coord[0][0]
		x4 = self.nodes[3].coord[0][0]
		y1 = self.nodes[0].coord[1][0]
		y2 = self.nodes[1].coord[1][0]
		y3 = self.nodes[2].coord[1][0]
		y4 = self.nodes[3].coord[1][0]

		A = 0.5*((x3-x1)*(y4-y2) + (x2-x4)*(y3-y1))
		print('A:', A)
		B = 0.5*np.array([[y2-y4, y3-y1, y4-y2, y1-y3],
						  [x4-x2, x1-x3, x2-x4, x3-x1]])
		print('B:', B.shape)
		print(B)		
		HG_shape = (0.25/A)*np.array([[x2*(y3-y4) + x3*(y4-y2) + x4*(y2-y3)],
									  [x3*(y1-y4) + x4*(y3-y1) + x1*(y4-y3)],
									  [x4*(y1-y2) + x1*(y2-y4) + x2*(y4-y1)],
									  [x1*(y3-y2) + x2*(y1-y3) + x3*(y2-y1)]])
		
		k = 0.01 # 0.01, 0.125, 0.5
		h = self.section.thickness
		G = self.section.material.shearMod
		p = self.section.material.density
		K = self.section.material.elastMod/(3*(1-2*self.section.material.poisson))
		print('bulk modulus:', K)
		dt = A*np.sqrt(p/((K+G+G)*np.multiply(B,B)))
		print('dt:', dt)

		v = dt[0][0]*np.array([[1., 1.],
							   [1., 1.],
							   [1., 1.],
							   [1., 1.]])
		print('v:', v)

		q = 0.5*np.multiply(v,HG_shape)
		print('q:', q.shape)
		print(q)

		Q = q.dot(0.5*k*h*(K+G+G)*np.multiply(B,B))
		print('Q:', Q.shape)
		print(Q)
		print('HG_shape:', HG_shape.shape)
		print(HG_shape)
		
		fHG_res = 0.5*np.multiply(Q,HG_shape)
		print('fHG_res:', fHG_res.shape)
		print(fHG_res)
		
		return fHG_res


	def calcStiffnessMatrix(self):
		'''
	Calculate the element stiffness matrix using
	isoparametric shape functions and Gauss Quadrature.
	'''
		self.K = np.array([[0.0,]*8,]*8)
		gauss = len(self.gaussPnts)

		ksi = 0.0
		eta = 0.0
		w_i = 0.0
		w_j = 0.0

		for i in range(gauss):
			ksi = self.gaussPnts[i][0]
			w_i = self.gaussPnts[i][1]

			for j in range(gauss):
				eta = self.gaussPnts[j][0]
				w_j = self.gaussPnts[j][1]

				[detJ,B] = self.calcStrainDisplacementMatrix(ksi,eta)
				self.K = ((B.transpose().dot(self.section.E)).dot(B))*(w_i*w_j*detJ*self.section.thickness) + self.K


	def calcMassMatrix(self):
		'''
	Calculate the element mass matrix using the
	lumped mass matrix method.
	'''
		area = abs(self.nodes[0].coord[0][0]*(self.nodes[1].coord[1][0]-self.nodes[3].coord[1][0]) + \
				   self.nodes[1].coord[0][0]*(self.nodes[3].coord[1][0]-self.nodes[0].coord[1][0]) + \
				   self.nodes[3].coord[0][0]*(self.nodes[0].coord[1][0]-self.nodes[1].coord[1][0]))*0.5 + \
			   abs(self.nodes[1].coord[0][0]*(self.nodes[2].coord[1][0]-self.nodes[3].coord[1][0]) + \
				   self.nodes[2].coord[0][0]*(self.nodes[3].coord[1][0]-self.nodes[1].coord[1][0]) + \
				   self.nodes[3].coord[0][0]*(self.nodes[1].coord[1][0]-self.nodes[2].coord[1][0]))*0.5
		self.M = np.identity(8)*(self.section.material.density*area*self.section.thickness*0.25)


	def calcStrain(self,u,calcStrain,calcStress,sol):
		'''
	Use the element strain-displacement matrix and 
	node displacements to find stresses and strains
	in element at integration points and at nodes.
	'''
		if calcStrain == True:
			self.solutions[sol]['strain'] = {'int_points': {}, 'nodal': {}}
		if calcStress == True:
			self.solutions[sol]['stress'] = {'int_points': {}, 'nodal': {}}

		gauss = len(self.gaussPnts)
		ngauss = gauss*gauss
		nodal = 4

		ksi = 0.0
		eta = 0.0
		w_i = 0.0
		w_j = 0.0

		k = 1
		for i in range(gauss):
			ksi = self.gaussPnts[i][0]
			w_i = self.gaussPnts[i][1]
			for j in range(gauss):
				eta = self.gaussPnts[j][0]
				w_j = self.gaussPnts[j][1]

				[detJ,B] = self.calcStrainDisplacementMatrix(ksi,eta)

				if calcStrain:
					self.solutions[sol]['strain']['int_points'][k] = {'strain_tensor': B.dot(u), 
											'VonMises': 0., 'MaxPrinc': 0., 'MinPrinc': 0., 'MaxShear': 0.}
				if calcStress:
					self.solutions[sol]['stress']['int_points'][k] = {'stress_tensor': self.section.E.dot(B.dot(u)), 
											'VonMises': 0., 'MaxPrinc': 0., 'MinPrinc': 0., 'MaxShear': 0.}
				k += 1
		
		ksieta = [[-1.,-1.], [ 1.,-1.], [ 1., 1.], [-1., 1.]]
		for j in range(nodal):
			ksi = ksieta[j][0]
			eta = ksieta[j][1]

			[detJ,B] = self.calcStrainDisplacementMatrix(ksi,eta)

			if calcStrain:
				self.solutions[sol]['strain']['nodal'][j+1] = {'strain_tensor': B.dot(u), 
									'VonMises': 0., 'MaxPrinc': 0., 'MinPrinc': 0., 'MaxShear': 0.}
			if calcStress:
				self.solutions[sol]['stress']['nodal'][j+1] = {'stress_tensor': self.section.E.dot(B.dot(u)), 
									'VonMises': 0., 'MaxPrinc': 0., 'MinPrinc': 0., 'MaxShear': 0.}

		if calcStrain == True:
			e = self.solutions[sol]['strain']['int_points']
			for i in range(ngauss):
				e[i+1]['VonMises'] = sqrt(e[i+1]['strain_tensor'][0]**2 - e[i+1]['strain_tensor'][0]*e[i+1]['strain_tensor'][1] + \
						   e[i+1]['strain_tensor'][1]**2 + 3*e[i+1]['strain_tensor'][2]**2)
				e[i+1]['MaxPrinc'] = (e[i+1]['strain_tensor'][0] + e[i+1]['strain_tensor'][1])/2.0 + \
							sqrt(((e[i+1]['strain_tensor'][0] - e[i+1]['strain_tensor'][1])/2.0)**2 + \
							e[i+1]['strain_tensor'][2]**2)
				e[i+1]['MinPrinc'] = (e[i+1]['strain_tensor'][0] + e[i+1]['strain_tensor'][1])/2.0 - \
							sqrt(((e[i+1]['strain_tensor'][0] - e[i+1]['strain_tensor'][1])/2.0)**2 + \
							e[i+1]['strain_tensor'][2]**2)
				e[i+1]['MaxShear'] = (e[i+1]['MaxPrinc']-e[i+1]['MinPrinc'])/2.0
			e = self.solutions[sol]['strain']['nodal']
			for i in range(nodal):
				e[i+1]['VonMises'] = sqrt(e[i+1]['strain_tensor'][0]**2 - e[i+1]['strain_tensor'][0]*e[i+1]['strain_tensor'][1] + \
						   e[i+1]['strain_tensor'][1]**2 + 3*e[i+1]['strain_tensor'][2]**2)
				e[i+1]['MaxPrinc'] = (e[i+1]['strain_tensor'][0] + e[i+1]['strain_tensor'][1])/2.0 + \
							sqrt(((e[i+1]['strain_tensor'][0] - e[i+1]['strain_tensor'][1])/2.0)**2 + \
							e[i+1]['strain_tensor'][2]**2)
				e[i+1]['MinPrinc'] = (e[i+1]['strain_tensor'][0] + e[i+1]['strain_tensor'][1])/2.0 - \
							sqrt(((e[i+1]['strain_tensor'][0] - e[i+1]['strain_tensor'][1])/2.0)**2 + \
							e[i+1]['strain_tensor'][2]**2)
				e[i+1]['MaxShear'] = (e[i+1]['MaxPrinc']-e[i+1]['MinPrinc'])/2.0

		if calcStress == True:
			s = self.solutions[sol]['stress']['int_points']
			for i in range(ngauss):
				s[i+1]['VonMises'] = sqrt(s[i+1]['stress_tensor'][0]**2 - s[i+1]['stress_tensor'][0]*s[i+1]['stress_tensor'][1] + \
						   s[i+1]['stress_tensor'][1]**2 + 3*s[i+1]['stress_tensor'][2]**2)
				s[i+1]['MaxPrinc'] = (s[i+1]['stress_tensor'][0] + s[i+1]['stress_tensor'][1])/2.0 + \
							sqrt(((s[i+1]['stress_tensor'][0] - s[i+1]['stress_tensor'][1])/2.0)**2 + \
							s[i+1]['stress_tensor'][2]**2)
				s[i+1]['MinPrinc'] = (s[i+1]['stress_tensor'][0] + s[i+1]['stress_tensor'][1])/2.0 - \
							sqrt(((s[i+1]['stress_tensor'][0] - s[i+1]['stress_tensor'][1])/2.0)**2 + \
							s[i+1]['stress_tensor'][2]**2)
				s[i+1]['MaxShear'] = (s[i+1]['MaxPrinc']-s[i+1]['MinPrinc'])/2.0
			s = self.solutions[sol]['stress']['nodal']
			for i in range(nodal):
				s[i+1]['VonMises'] = sqrt(s[i+1]['stress_tensor'][0]**2 - s[i+1]['stress_tensor'][0]*s[i+1]['stress_tensor'][1] + \
						   s[i+1]['stress_tensor'][1]**2 + 3*s[i+1]['stress_tensor'][2]**2)
				s[i+1]['MaxPrinc'] = (s[i+1]['stress_tensor'][0] + s[i+1]['stress_tensor'][1])/2.0 + \
							sqrt(((s[i+1]['stress_tensor'][0] - s[i+1]['stress_tensor'][1])/2.0)**2 + \
							s[i+1]['stress_tensor'][2]**2)
				s[i+1]['MinPrinc'] = (s[i+1]['stress_tensor'][0] + s[i+1]['stress_tensor'][1])/2.0 - \
							sqrt(((s[i+1]['stress_tensor'][0] - s[i+1]['stress_tensor'][1])/2.0)**2 + \
							s[i+1]['stress_tensor'][2]**2)
				s[i+1]['MaxShear'] = (s[i+1]['MaxPrinc']-s[i+1]['MinPrinc'])/2.0





class QUAD8N(Element):
	'''
Class for quadrilateral 8-node 2D element.
Has two active degrees of freedom per node.
8 nodes gives 16 degrees of freedom total.
'''
	def __init__(self,number,sect,nodes,gaussQuad):
		self.gaussPnts = gaussQuad.quad_p3
		super(QUAD8N,self).__init__(number,sect,nodes)
		self.EFS = [[1,1,0,0,0,0],]*8
		self.nodeFreedomSignature()
		self.type = 'QUAD8N'


	def nodeFreedomSignature(self):
		'''
	Update node freedom signature for nodes in element.
	'''
		for i in range(len(self.nodes)):
			if self.nodes[i].NFS[0] == 0:
				self.nodes[i].NFS[0] = 1
			if self.nodes[i].NFS[1] == 0:
				self.nodes[i].NFS[1] = 1


	def calcStrainDisplacementMatrix(self,ksi,eta):
		'''
	Calculate the B-matrix given specific
	shape function coordinates.
	'''
		dNf_dqc = np.array([[(2.0*ksi+eta-2.0*ksi*eta-eta**2)/4.0,
							 (-2.0*ksi+2.0*ksi*eta)/2.0,
							 (2.0*ksi-eta-2.0*ksi*eta+eta**2)/4.0,
							 (1.0-eta**2)/2.0,
							 (2.0*ksi+eta+2.0*ksi*eta+eta**2)/4.0,
							 (-2.0*ksi-2.0*ksi*eta)/2.0,
							 (2.0*ksi-eta+2.0*ksi*eta-eta**2)/4.0,
							 (-1.0+eta**2)/2.0],
				 			[(ksi+2.0*eta-ksi**2-2.0*ksi*eta)/4.0,
							 (-1.0+ksi**2)/2.0,
							 (-ksi+2.0*eta-ksi**2+2.0*ksi*eta)/4.0,
							 (-2.0*eta-2.0*ksi*eta)/2.0,
							 (ksi+2.0*eta+ksi**2+2.0*ksi*eta)/4.0,
							 (1.0-ksi**2)/2.0,
							 (-ksi+2.0*eta+ksi**2-2.0*ksi*eta)/4.0,
							 (-2.0*eta+2.0*ksi*eta)/2.0]])

		J = dNf_dqc.dot(np.array([[self.nodes[0].coord[0][0],self.nodes[0].coord[1][0]],
								  [self.nodes[1].coord[0][0],self.nodes[1].coord[1][0]],
								  [self.nodes[2].coord[0][0],self.nodes[2].coord[1][0]],
								  [self.nodes[3].coord[0][0],self.nodes[3].coord[1][0]],
								  [self.nodes[4].coord[0][0],self.nodes[4].coord[1][0]],
								  [self.nodes[5].coord[0][0],self.nodes[5].coord[1][0]],
								  [self.nodes[6].coord[0][0],self.nodes[6].coord[1][0]],
								  [self.nodes[7].coord[0][0],self.nodes[7].coord[1][0]]]))
		detJ = J[0][0]*J[1][1] - J[0][1]*J[1][0]
		invJ = np.array([[(1.0/detJ)*J[1][1],-(1.0/detJ)*J[0][1]],
						 [-(1.0/detJ)*J[1][0],(1.0/detJ)*J[0][0]]])

		dNf_drc = invJ.dot(dNf_dqc)

		B = [[],[],[]]
		for l in range(8):
			B[0].append(dNf_drc[0][l])
			B[0].append(0.0)
		for m in range(8):
			B[1].append(0.0)
			B[1].append(dNf_drc[1][m])
		for n in range(8):
			B[2].append(dNf_drc[1][n])
			B[2].append(dNf_drc[0][n])
		B = np.array(B)

		return [detJ,B]


	def calcStiffnessMatrix(self):
		'''
	Calculate the element stiffness matrix using
	isoparametric shape functions and Gauss Quadrature.
	'''
		self.K = np.array([[0.0,]*16,]*16)
		gauss = len(self.gaussPnts)

		ksi = 0.0
		eta = 0.0
		w_i = 0.0
		w_j = 0.0

		for i in range(gauss):
			ksi = self.gaussPnts[i][0]
			w_i = self.gaussPnts[i][1]

			for j in range(gauss):
				eta = self.gaussPnts[j][0]
				w_j = self.gaussPnts[j][1]

				[detJ,B] = self.calcStrainDisplacementMatrix(ksi,eta)
				self.K = ((B.transpose().dot(self.section.E)).dot(B))*(w_i*w_j*detJ*self.section.thickness) + self.K


	def calcMassMatrix(self):
		'''
	Calculate the element mass matrix using the
	lumped mass matrix method.
	'''
		area = abs(self.nodes[0].coord[0][0]*(self.nodes[2].coord[1][0]-self.nodes[6].coord[1][0]) + \
				   self.nodes[2].coord[0][0]*(self.nodes[6].coord[1][0]-self.nodes[0].coord[1][0]) + \
				   self.nodes[6].coord[0][0]*(self.nodes[0].coord[1][0]-self.nodes[2].coord[1][0]))*0.5 + \
			   abs(self.nodes[2].coord[0][0]*(self.nodes[4].coord[1][0]-self.nodes[6].coord[1][0]) + \
				   self.nodes[4].coord[0][0]*(self.nodes[6].coord[1][0]-self.nodes[2].coord[1][0]) + \
				   self.nodes[6].coord[0][0]*(self.nodes[2].coord[1][0]-self.nodes[4].coord[1][0]))*0.5
		self.M = np.identity(16)*(self.section.material.density*area*self.section.thickness*0.125)


	def calcStrain(self,u,calcStrain,calcStress,sol):
		'''
	Use the element strain-displacement matrix and 
	node displacements to find stresses and strains
	in element at integration points and at nodes as
	well as midpoint for better contour plots.
	'''
		if calcStrain == True:
			self.solutions[sol]['strain'] = {'int_points': {}, 'nodal': {}}
		if calcStress == True:
			self.solutions[sol]['stress'] = {'int_points': {}, 'nodal': {}}

		gauss = len(self.gaussPnts)
		ngauss = gauss*gauss
		nodal = 9

		ksi = 0.0
		eta = 0.0
		w_i = 0.0
		w_j = 0.0

		k = 1
		for i in range(gauss):
			ksi = self.gaussPnts[i][0]
			w_i = self.gaussPnts[i][1]
			for j in range(gauss):
				eta = self.gaussPnts[j][0]
				w_j = self.gaussPnts[j][1]

				[detJ,B] = self.calcStrainDisplacementMatrix(ksi,eta)

				if calcStrain:
					self.solutions[sol]['strain']['int_points'][k] = {'strain_tensor': B.dot(u), 
											'VonMises': 0., 'MaxPrinc': 0., 'MinPrinc': 0., 'MaxShear': 0.}
				if calcStress:
					self.solutions[sol]['stress']['int_points'][k] = {'stress_tensor': self.section.E.dot(B.dot(u)), 
											'VonMises': 0., 'MaxPrinc': 0., 'MinPrinc': 0., 'MaxShear': 0.}
				k += 1
		
		ksieta = [[-1.,-1.], [ 0.,-1.], [ 1.,-1.], [ 1., 0.],
				  [ 1., 1.], [ 0., 1.], [-1., 1.], [-1., 0.],[ 0., 0.]]
		for j in range(nodal):
			ksi = ksieta[j][0]
			eta = ksieta[j][1]

			[detJ,B] = self.calcStrainDisplacementMatrix(ksi,eta)

			if calcStrain:
				self.solutions[sol]['strain']['nodal'][j+1] = {'strain_tensor': B.dot(u), 
									'VonMises': 0., 'MaxPrinc': 0., 'MinPrinc': 0., 'MaxShear': 0.}
			if calcStress:
				self.solutions[sol]['stress']['nodal'][j+1] = {'stress_tensor': self.section.E.dot(B.dot(u)), 
									'VonMises': 0., 'MaxPrinc': 0., 'MinPrinc': 0., 'MaxShear': 0.}

		if calcStrain == True:
			e = self.solutions[sol]['strain']['int_points']
			for i in range(ngauss):
				e[i+1]['VonMises'] = sqrt(e[i+1]['strain_tensor'][0]**2 - e[i+1]['strain_tensor'][0]*e[i+1]['strain_tensor'][1] + \
						   e[i+1]['strain_tensor'][1]**2 + 3*e[i+1]['strain_tensor'][2]**2)
				e[i+1]['MaxPrinc'] = (e[i+1]['strain_tensor'][0] + e[i+1]['strain_tensor'][1])/2.0 + \
							sqrt(((e[i+1]['strain_tensor'][0] - e[i+1]['strain_tensor'][1])/2.0)**2 + \
							e[i+1]['strain_tensor'][2]**2)
				e[i+1]['MinPrinc'] = (e[i+1]['strain_tensor'][0] + e[i+1]['strain_tensor'][1])/2.0 - \
							sqrt(((e[i+1]['strain_tensor'][0] - e[i+1]['strain_tensor'][1])/2.0)**2 + \
							e[i+1]['strain_tensor'][2]**2)
				e[i+1]['MaxShear'] = (e[i+1]['MaxPrinc']-e[i+1]['MinPrinc'])/2.0
			e = self.solutions[sol]['strain']['nodal']
			for i in range(nodal):
				e[i+1]['VonMises'] = sqrt(e[i+1]['strain_tensor'][0]**2 - e[i+1]['strain_tensor'][0]*e[i+1]['strain_tensor'][1] + \
						   e[i+1]['strain_tensor'][1]**2 + 3*e[i+1]['strain_tensor'][2]**2)
				e[i+1]['MaxPrinc'] = (e[i+1]['strain_tensor'][0] + e[i+1]['strain_tensor'][1])/2.0 + \
							sqrt(((e[i+1]['strain_tensor'][0] - e[i+1]['strain_tensor'][1])/2.0)**2 + \
							e[i+1]['strain_tensor'][2]**2)
				e[i+1]['MinPrinc'] = (e[i+1]['strain_tensor'][0] + e[i+1]['strain_tensor'][1])/2.0 - \
							sqrt(((e[i+1]['strain_tensor'][0] - e[i+1]['strain_tensor'][1])/2.0)**2 + \
							e[i+1]['strain_tensor'][2]**2)
				e[i+1]['MaxShear'] = (e[i+1]['MaxPrinc']-e[i+1]['MinPrinc'])/2.0

		if calcStress == True:
			s = self.solutions[sol]['stress']['int_points']
			for i in range(ngauss):
				s[i+1]['VonMises'] = sqrt(s[i+1]['stress_tensor'][0]**2 - s[i+1]['stress_tensor'][0]*s[i+1]['stress_tensor'][1] + \
						   s[i+1]['stress_tensor'][1]**2 + 3*s[i+1]['stress_tensor'][2]**2)
				s[i+1]['MaxPrinc'] = (s[i+1]['stress_tensor'][0] + s[i+1]['stress_tensor'][1])/2.0 + \
							sqrt(((s[i+1]['stress_tensor'][0] - s[i+1]['stress_tensor'][1])/2.0)**2 + \
							s[i+1]['stress_tensor'][2]**2)
				s[i+1]['MinPrinc'] = (s[i+1]['stress_tensor'][0] + s[i+1]['stress_tensor'][1])/2.0 - \
							sqrt(((s[i+1]['stress_tensor'][0] - s[i+1]['stress_tensor'][1])/2.0)**2 + \
							s[i+1]['stress_tensor'][2]**2)
				s[i+1]['MaxShear'] = (s[i+1]['MaxPrinc']-s[i+1]['MinPrinc'])/2.0
			s = self.solutions[sol]['stress']['nodal']
			for i in range(nodal):
				s[i+1]['VonMises'] = sqrt(s[i+1]['stress_tensor'][0]**2 - s[i+1]['stress_tensor'][0]*s[i+1]['stress_tensor'][1] + \
						   s[i+1]['stress_tensor'][1]**2 + 3*s[i+1]['stress_tensor'][2]**2)
				s[i+1]['MaxPrinc'] = (s[i+1]['stress_tensor'][0] + s[i+1]['stress_tensor'][1])/2.0 + \
							sqrt(((s[i+1]['stress_tensor'][0] - s[i+1]['stress_tensor'][1])/2.0)**2 + \
							s[i+1]['stress_tensor'][2]**2)
				s[i+1]['MinPrinc'] = (s[i+1]['stress_tensor'][0] + s[i+1]['stress_tensor'][1])/2.0 - \
							sqrt(((s[i+1]['stress_tensor'][0] - s[i+1]['stress_tensor'][1])/2.0)**2 + \
							s[i+1]['stress_tensor'][2]**2)
				s[i+1]['MaxShear'] = (s[i+1]['MaxPrinc']-s[i+1]['MinPrinc'])/2.0





class ROD2N(Element):
	'''
Class for 3D rod element.
Has 3 active degrees of freedom per node.
2 nodes gives 6 degrees of freedom total.
'''
	def __init__(self,number,sect,nodes):
		super(ROD2N,self).__init__(number,sect,nodes)
		self.EFS = [[1,1,1,0,0,0],]*2
		self.nodeFreedomSignature()
		self.type = 'ROD2N'
		self.setOrientation()


	def nodeFreedomSignature(self):
		'''
	Update node freedom signature for nodes in element.
	'''
		for i in range(len(self.nodes)):
			if self.nodes[i].NFS[0] == 0:
				self.nodes[i].NFS[0] = 1
			if self.nodes[i].NFS[1] == 0:
				self.nodes[i].NFS[1] = 1
			if self.nodes[i].NFS[2] == 0:
				self.nodes[i].NFS[2] = 1


	def setOrientation(self,orient='None'):
		'''
	Sets the element orientation which is used
	by viewer to render element if cross section
	has been applied to section.
	
	If x1 --> x2 is vertical, then y1 --> y2
	is set to be the same as the global negative
	x-axis.
	
	orient = {'x-vec': [x, y, z],	x-vector specified by user
			  'y-vec': [x, y, z]}	y-vector specified by user
	'''
		x21 = self.nodes[1].coord[0][0]-self.nodes[0].coord[0][0]
		y21 = self.nodes[1].coord[1][0]-self.nodes[0].coord[1][0]
		z21 = self.nodes[1].coord[2][0]-self.nodes[0].coord[2][0]

		self.length = sqrt(x21**2 + y21**2 + z21**2)

		x1 = self.nodes[0].coord[0][0]
		x2 = self.nodes[1].coord[0][0]
		y1 = self.nodes[0].coord[1][0]
		y2 = self.nodes[1].coord[1][0]
		z1 = self.nodes[0].coord[2][0]
		z2 = self.nodes[1].coord[2][0]

		if orient != 'None':
			if x21 < 0. and orient['x-vec'][0] < 0.:
				xv = np.array([x21, y21, z21])
			elif x21 >= 0. and orient['x-vec'][0] >= 0.:
				xv = np.array([x21, y21, z21])
			else:
				# if node order not alligned with beam orientation,
				# switch nodes 1 and 2 to allign them
				self.nodes[0], self.nodes[1] = self.nodes[1], self.nodes[0]
				x21 = self.nodes[1].coord[0][0]-self.nodes[0].coord[0][0]
				y21 = self.nodes[1].coord[1][0]-self.nodes[0].coord[1][0]
				z21 = self.nodes[1].coord[2][0]-self.nodes[0].coord[2][0]
				xv = np.array([x21, y21, z21])
				x1 = self.nodes[0].coord[0][0]
				x2 = self.nodes[1].coord[0][0]
				y1 = self.nodes[0].coord[1][0]
				y2 = self.nodes[1].coord[1][0]
				z1 = self.nodes[0].coord[2][0]
				z2 = self.nodes[1].coord[2][0]
			xu = xv/self.length
			n1_offset = np.array([x1,y1,z1]) + np.array(orient['y-vec'])
			n2_offset = np.array([x2,y2,z2]) + np.array(orient['y-vec'])

		else:
			if abs(x21) < 0.001 and abs(y21) > 0.001:
				n1_offset = np.array([x1-1, y1, z1])
				n2_offset = np.array([x2-1, y2, z2])
			else:
				n1_offset = np.array([x1, y1+1, z1])
				n2_offset = np.array([x2, y2+1, z2])
			xv = np.array([x21, y21, z21])
			xu = xv/self.length

		n_offset = n1_offset + 0.5*(n2_offset-n1_offset)

		ov = n_offset - np.array([x1,y1,z1])
		yv = ov - np.dot(ov,xu)*xu
		mag = sqrt(yv[0]**2 + yv[1]**2 + yv[2]**2)
		if mag == 0.:
			yu = yv
		else:
			yu = yv/mag
		zu = np.cross(xu, yu)

		self.orientation = {'x-vec': xu,
							'y-vec': yu,
							'z-vec': zu}


	def calcStiffnessMatrix(self):
		'''
	Calculate the element stiffness matrix.
	'''
		dx = self.nodes[1].coord[0][0]-self.nodes[0].coord[0][0]
		dy = self.nodes[1].coord[1][0]-self.nodes[0].coord[1][0]
		dz = self.nodes[1].coord[2][0]-self.nodes[0].coord[2][0]

		self.length = sqrt(dx**2 + dy**2 + dz**2)
		EA_L3 = self.section.material.elastMod*self.section.area/(self.length**3)

		self.K = EA_L3*np.array([[  dx**2,  dx*dy,  dx*dz, -dx**2, -dx*dy, -dx*dz],
								 [  dx*dy,  dy**2,  dy*dz, -dx*dy, -dy**2, -dy*dz],
								 [  dx*dz,  dy*dz,  dz**2, -dx*dz, -dy*dz, -dz**2],
								 [ -dx**2, -dx*dy, -dx*dz,  dx**2,  dx*dy,  dx*dz], 
								 [ -dx*dy, -dy**2, -dy*dz,  dx*dy,  dy**2,  dy*dz], 
								 [ -dx*dz, -dy*dz, -dz**2,  dx*dz,  dy*dz,  dz**2]])


	def calcMassMatrix(self):
		'''
	Calculate the element mass matrix using the
	lumped mass matrix method.
	'''
		self.M = np.identity(6)*(self.section.material.density*self.section.area*self.length*0.5)


	def calcForces(self,u,sol):
		'''
	Calculate the internal element forces using
	the element stiffness matrix and the
	displacement vector.
	'''
		dx = self.nodes[1].coord[0][0]-self.nodes[0].coord[0][0]
		dy = self.nodes[1].coord[1][0]-self.nodes[0].coord[1][0]
		dz = self.nodes[1].coord[2][0]-self.nodes[0].coord[2][0]
		dxu = u[3] - u[0]
		dyu = u[4] - u[1]
		dzu = u[5] - u[2]
		strain = dx*dxu + dy*dyu + dz*dzu
		nodeforce = self.K.dot(u)
		self.solutions[sol]['elementforce'] = [0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0.]
		if strain < 0:
			self.solutions[sol]['elementforce'][0] = -sqrt(abs(nodeforce[0]**2 + nodeforce[1]**2 + nodeforce[2]**2))
		else:
			self.solutions[sol]['elementforce'][0] = sqrt(abs(nodeforce[0]**2 + nodeforce[1]**2 + nodeforce[2]**2))


	def calcStrain(self,u,calcStrain,calcStress,sol):
		'''
	Use the element strain-displacement matrix and 
	node displacements to find stresses and strains
	in element.
	'''
		dx = self.nodes[1].coord[0][0]-self.nodes[0].coord[0][0]
		dy = self.nodes[1].coord[1][0]-self.nodes[0].coord[1][0]
		dz = self.nodes[1].coord[2][0]-self.nodes[0].coord[2][0]
		dxu = u[3] - u[0]
		dyu = u[4] - u[1]
		dzu = u[5] - u[2]
		strain = abs(dx*dxu + dy*dyu + dz*dzu)
		stress = strain*self.section.material.elastMod
		if calcStrain == True:
			self.solutions[sol]['strain'] = {'nodal': {}}
			self.solutions[sol]['strain']['nodal'][1] = {'VonMises': strain, 'MaxPrinc': strain, 'MinPrinc': strain/2., 'MaxShear': strain/2.}
			self.solutions[sol]['strain']['nodal'][2] = {'VonMises': strain, 'MaxPrinc': strain, 'MinPrinc': strain/2., 'MaxShear': strain/2.}
		if calcStress == True:
			self.solutions[sol]['stress'] = {'nodal': {}}
			self.solutions[sol]['stress']['nodal'][1] = {'VonMises': stress, 'MaxPrinc': stress, 'MinPrinc': stress/2., 'MaxShear': stress/2.}
			self.solutions[sol]['stress']['nodal'][2] = {'VonMises': stress, 'MaxPrinc': stress, 'MinPrinc': stress/2., 'MaxShear': stress/2.}




class BEAM2N(Element):
	'''
Class for 3D beam element.
Subclass of Element.
'''
	def __init__(self,number,sect,nodes):
		super(BEAM2N,self).__init__(number,sect,nodes)
		self.EFS = [[1,1,1,1,1,1],]*2
		self.nodeFreedomSignature()
		self.type = 'BEAM2N'


	def nodeFreedomSignature(self):
		'''
	Update node freedom signature for nodes in element.
	'''
		for i in range(len(self.nodes)):
			if self.nodes[i].NFS[0] == 0:
				self.nodes[i].NFS[0] = 1
			if self.nodes[i].NFS[1] == 0:
				self.nodes[i].NFS[1] = 1
			if self.nodes[i].NFS[2] == 0:
				self.nodes[i].NFS[2] = 1
			if self.nodes[i].NFS[3] == 0:
				self.nodes[i].NFS[3] = 1
			if self.nodes[i].NFS[4] == 0:
				self.nodes[i].NFS[4] = 1
			if self.nodes[i].NFS[5] == 0:
				self.nodes[i].NFS[5] = 1


	def setOrientation(self,orient='None'):
		'''
	Sets the element orientation which is used
	when calculating the stiffness matrix.
	
	If orient == 'None', the orientation is set
	to a default, where the "weak" bending axis
	(y-axis) is set to point as much upwards as
	possible given the direction x1 --> x2.
	
	If x1 --> x2 is vertical, then y1 --> y2
	is set to be the same as the global negative
	x-axis.
	
	orient = {'x-vec': [x, y, z],	x-vector specified by user
			  'y-vec': [x, y, z]}	y-vector specified by user
	'''
		x21 = self.nodes[1].coord[0][0]-self.nodes[0].coord[0][0]
		y21 = self.nodes[1].coord[1][0]-self.nodes[0].coord[1][0]
		z21 = self.nodes[1].coord[2][0]-self.nodes[0].coord[2][0]

		self.length = sqrt(x21**2 + y21**2 + z21**2)

		x1 = self.nodes[0].coord[0][0]
		x2 = self.nodes[1].coord[0][0]
		y1 = self.nodes[0].coord[1][0]
		y2 = self.nodes[1].coord[1][0]
		z1 = self.nodes[0].coord[2][0]
		z2 = self.nodes[1].coord[2][0]

		if orient != 'None':
			if x21 < 0. and orient['x-vec'][0] < 0.:
				xv = np.array([x21, y21, z21])
			elif x21 >= 0. and orient['x-vec'][0] >= 0.:
				xv = np.array([x21, y21, z21])
			else:
				# if node order not alligned with beam orientation,
				# switch nodes 1 and 2 to allign them
				self.nodes[0], self.nodes[1] = self.nodes[1], self.nodes[0]
				x21 = self.nodes[1].coord[0][0]-self.nodes[0].coord[0][0]
				y21 = self.nodes[1].coord[1][0]-self.nodes[0].coord[1][0]
				z21 = self.nodes[1].coord[2][0]-self.nodes[0].coord[2][0]
				xv = np.array([x21, y21, z21])
				x1 = self.nodes[0].coord[0][0]
				x2 = self.nodes[1].coord[0][0]
				y1 = self.nodes[0].coord[1][0]
				y2 = self.nodes[1].coord[1][0]
				z1 = self.nodes[0].coord[2][0]
				z2 = self.nodes[1].coord[2][0]
			xu = xv/self.length
			n1_offset = np.array([x1,y1,z1]) + np.array(orient['y-vec'])
			n2_offset = np.array([x2,y2,z2]) + np.array(orient['y-vec'])

		else:
			if abs(x21) < 0.001 and abs(y21) > 0.001:
				n1_offset = np.array([x1-1, y1, z1])
				n2_offset = np.array([x2-1, y2, z2])
			else:
				n1_offset = np.array([x1, y1+1, z1])
				n2_offset = np.array([x2, y2+1, z2])
			xv = np.array([x21, y21, z21])
			xu = xv/self.length

		n_offset = n1_offset + 0.5*(n2_offset-n1_offset)

		ov = n_offset - np.array([x1,y1,z1])
		yv = ov - np.dot(ov,xu)*xu
		mag = sqrt(yv[0]**2 + yv[1]**2 + yv[2]**2)
		if mag == 0.:
			yu = yv
		else:
			yu = yv/mag
		zu = np.cross(xu, yu)

		self.orientation = {'x-vec': xu,
							'y-vec': yu,
							'z-vec': zu}

		txx = xu[0]
		txy = xu[1]
		txz = xu[2]
		tyx = yu[0]
		tyy = yu[1]
		tyz = yu[2]
		tzx = zu[0]
		tzy = zu[1]
		tzz = zu[2]

		self.T_elm = np.array([[ txx, txy, txz,   0,   0,   0,   0,   0,   0,   0,   0,   0],
							   [ tyx, tyy, tyz,   0,   0,   0,   0,   0,   0,   0,   0,   0],
							   [ tzx, tzy, tzz,   0,   0,   0,   0,   0,   0,   0,   0,   0],
							   [   0,   0,   0, txx, txy, txz,   0,   0,   0,   0,   0,   0],
							   [   0,   0,   0, tyx, tyy, tyz,   0,   0,   0,   0,   0,   0],
							   [   0,   0,   0, tzx, tzy, tzz,   0,   0,   0,   0,   0,   0],
							   [   0,   0,   0,   0,   0,   0, txx, txy, txz,   0,   0,   0],
							   [   0,   0,   0,   0,   0,   0, tyx, tyy, tyz,   0,   0,   0],
							   [   0,   0,   0,   0,   0,   0, tzx, tzy, tzz,   0,   0,   0],
							   [   0,   0,   0,   0,   0,   0,   0,   0,   0, txx, txy, txz],
							   [   0,   0,   0,   0,   0,   0,   0,   0,   0, tyx, tyy, tyz],
							   [   0,   0,   0,   0,   0,   0,   0,   0,   0, tzx, tzy, tzz]])


	def calcStiffnessMatrix(self):
		'''
	Calculate the element stiffness matrix.
	'''
		EA   = self.section.material.elastMod*self.section.area
		EIzz = self.section.material.elastMod*self.section.Izz
		EIyy = self.section.material.elastMod*self.section.Iyy
		GJ   = self.section.material.shearMod*self.section.Jxx
		L    = self.length

		ra  = EA/L
		rx  = GJ/L
		ry  = (2*EIyy)/L
		ry2 = (6*EIyy)/(L**2)
		ry3 = (12*EIyy)/(L**3)
		rz  = (2*EIzz)/L
		rz2 = (6*EIzz)/(L**2)
		rz3 = (12*EIzz)/(L**3)

		K_beam = np.array([[  ra,   0,   0,   0,   0,   0, -ra,   0,   0,   0,   0,   0],
						   [   0, rz3,   0,   0,   0, rz2,   0,-rz3,   0,   0,   0, rz2],
						   [   0,   0, ry3,   0,-ry2,   0,   0,   0,-ry3,   0,-ry2,   0],
						   [   0,   0,   0,  rx,   0,   0,   0,   0,   0, -rx,   0,   0],
						   [   0,   0,-ry2,   0,2*ry,   0,   0,   0, ry2,   0,  ry,   0],
						   [   0, rz2,   0,   0,   0,2*rz,   0,-rz2,   0,   0,   0,  rz],
						   [ -ra,   0,   0,   0,   0,   0,  ra,   0,   0,   0,   0,   0],
						   [   0,-rz3,   0,   0,   0,-rz2,   0, rz3,   0,   0,   0,-rz2],
						   [   0,   0,-ry3,   0, ry2,   0,   0,   0, ry3,   0, ry2,   0],
						   [   0,   0,   0, -rx,   0,   0,   0,   0,   0,  rx,   0,   0],
						   [   0,   0,-ry2,   0,  ry,   0,   0,   0, ry2,   0,2*ry,   0],
						   [   0, rz2,   0,   0,   0,  rz,   0,-rz2,   0,   0,   0,2*rz]])

		self.K = ((self.T_elm.transpose().dot(K_beam)).dot(self.T_elm))


	def calcMassMatrix(self):
		'''
	Calculate the element mass matrix using the
	lumped mass matrix method.
	'''
		self.M = np.identity(12)*(self.section.material.density*self.section.area*self.length*0.5)
		self.M[3][3] = self.M[3][3]*((self.length**2)/12)
		self.M[4][4] = self.M[4][4]*((self.length**2)/12)
		self.M[5][5] = self.M[5][5]*((self.length**2)/12)
		self.M[9][9] = self.M[9][9]*((self.length**2)/12)
		self.M[10][10] = self.M[10][10]*((self.length**2)/12)
		self.M[11][11] = self.M[11][11]*((self.length**2)/12)


	def calcEquivalentNodalForces(self,distForce,freeDOFs):
		'''
	Calculate the equivalent nodal forces from
	a distributed load on element.
	distForce 			   - force vector per element length
	self.eqNodeForcesLocal - equivalent node forces in local
							 reference frame
	self.eqNodeForces	   - equivalent node forces in global
							 reference frame
	'''
		F = np.dot(self.T_elm[:3,:3],distForce)
		self.eqNodeForcesLocal = [0.]*12
		# fx1 and fx2
		self.eqNodeForcesLocal[0] = F[0]*self.length/2.			# fx1
		self.eqNodeForcesLocal[6] = F[0]*self.length/2.			# fx2
		# fy1 and fy2
		if freeDOFs[1] == freeDOFs[7] == 1:
			self.eqNodeForcesLocal[1] = F[1]*self.length/2.		# fy1
			self.eqNodeForcesLocal[7] = F[1]*self.length/2.		# fy2
		elif freeDOFs[1] == 1 and freeDOFs[7] == 0:
			self.eqNodeForcesLocal[1] = F[1]*self.length*5./8.	# fy1
			self.eqNodeForcesLocal[7] = F[1]*self.length*3./8.	# fy2
		elif freeDOFs[1] == 0 and freeDOFs[7] == 1:
			self.eqNodeForcesLocal[1] = F[1]*self.length*3./8.	# fy1
			self.eqNodeForcesLocal[7] = F[1]*self.length*5./8.	# fy2
		else:
			print('\n\tElement', self.number, 'not restrained in y-direction?')
		# fz1 and fz2
		if freeDOFs[2] == freeDOFs[8] == 1:
			self.eqNodeForcesLocal[2] = F[2]*self.length/2.		# fz1
			self.eqNodeForcesLocal[8] = F[2]*self.length/2.		# fz2
		elif freeDOFs[2] == 1 and freeDOFs[8] == 0:
			self.eqNodeForcesLocal[2] = F[2]*self.length*5./8.	# fz1
			self.eqNodeForcesLocal[8] = F[2]*self.length*3./8.	# fz2
		elif freeDOFs[2] == 0 and freeDOFs[8] == 1:
			self.eqNodeForcesLocal[2] = F[2]*self.length*3./8.	# fz1
			self.eqNodeForcesLocal[8] = F[2]*self.length*5./8.	# fz2
		else:
			print('\n\tElement', self.number, 'not restrained in z-direction?')
		# my1 and my2
		if freeDOFs[4] == freeDOFs[10] == 1:
			self.eqNodeForcesLocal[4]  =  F[2]*(self.length**2)/12.	# my1
			self.eqNodeForcesLocal[10] = -F[2]*(self.length**2)/12.	# my2
		elif freeDOFs[4] == 1 and freeDOFs[10] == 0:
			self.eqNodeForcesLocal[4]  =  F[2]*(self.length**2)/8.	# my1
		elif freeDOFs[4] == 0 and freeDOFs[10] == 1:
			self.eqNodeForcesLocal[10] = -F[2]*(self.length**2)/8.	# my2
		else:
			pass
		if freeDOFs[5] == freeDOFs[11] == 1:
			self.eqNodeForcesLocal[5]  =  F[1]*(self.length**2)/12.	# mz1
			self.eqNodeForcesLocal[11] = -F[1]*(self.length**2)/12.	# mz2
		elif freeDOFs[5] == 1 and freeDOFs[10] == 0:
			self.eqNodeForcesLocal[5]  =  F[1]*(self.length**2)/8.	# mz1
		elif freeDOFs[5] == 0 and freeDOFs[10] == 1:
			self.eqNodeForcesLocal[11] = -F[1]*(self.length**2)/8.	# mz2
		else:
			pass
		self.eqNodeForces = np.linalg.inv(self.T_elm).dot(self.eqNodeForcesLocal)


	def calcForces(self,u,sol):
		'''
	Calculate the internal element forces using
	the element stiffness matrix and the
	displacement vector.
	'''
		u_local = self.T_elm.dot(u)
		K = self.T_elm.dot(self.K).dot(self.T_elm.T)
		nodeforce = K.dot(u_local)
		self.solutions[sol]['elementforce'] = [0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0.]
		self.solutions[sol]['elementforce'][0] = ((self.section.area*self.section.material.elastMod)/self.length)*(u_local[6]-u_local[0])
		self.solutions[sol]['elementforce'][1:6] = nodeforce[1:6]
		self.solutions[sol]['elementforce'][6:] = nodeforce[7:]

		if hasattr(self,'eqNodeForcesLocal'):
			self.solutions[sol]['elementforce'][0] += self.eqNodeForcesLocal[0]
			self.solutions[sol]['elementforce'][1] -= self.eqNodeForcesLocal[1]
			self.solutions[sol]['elementforce'][2] -= self.eqNodeForcesLocal[2]
			self.solutions[sol]['elementforce'][3] -= self.eqNodeForcesLocal[3]
			self.solutions[sol]['elementforce'][4] -= self.eqNodeForcesLocal[4]
			self.solutions[sol]['elementforce'][5] -= self.eqNodeForcesLocal[5]
			self.solutions[sol]['elementforce'][6] -= self.eqNodeForcesLocal[7]
			self.solutions[sol]['elementforce'][7] -= self.eqNodeForcesLocal[8]
			self.solutions[sol]['elementforce'][8] -= self.eqNodeForcesLocal[9]
			self.solutions[sol]['elementforce'][9] -= self.eqNodeForcesLocal[10]
			self.solutions[sol]['elementforce'][10] -= self.eqNodeForcesLocal[11]


	def calcStrain(self,u,calcStrain,calcStress,sol): ### NOT READY
		'''
	Use the elementforces to find maximum/minimum
	stresses and strains at nodes in element. 
	'''
		strain = np.nan
		stress = np.nan
		if calcStrain == True:
			self.solutions[sol]['strain'] = {'nodal': {}}
			self.solutions[sol]['strain']['nodal'][1] = {'VonMises': 0., 'MaxPrinc': 0., 'MinPrinc': 0., 'MaxShear': 0.}
			self.solutions[sol]['strain']['nodal'][2] = {'VonMises': 0., 'MaxPrinc': 0., 'MinPrinc': 0., 'MaxShear': 0.}
		if calcStress == True:
			self.solutions[sol]['stress'] = {'nodal': {}}
			self.solutions[sol]['stress']['nodal'][1] = {'VonMises': 0., 'MaxPrinc': 0., 'MinPrinc': 0., 'MaxShear': 0.}
			self.solutions[sol]['stress']['nodal'][2] = {'VonMises': 0., 'MaxPrinc': 0., 'MinPrinc': 0., 'MaxShear': 0.}





class PLATE3N(Element):
	'''
Class for triangular 3-node plate element.
Subclass of Element.
'''
	pass


class PLATE6N(Element):
	'''
Class for triangular 6-node plate element.
Subclass of Element.
'''
	pass


class PLATE4N(Element):
	'''
Class for quadrilateral 4-node plate element.
Subclass of Element.
'''
	pass


class PLATE8N(Element):
	'''
Class for quadrilateral 8-node plate element.
Subclass of Element.
'''
	pass





class TET4N(Element):
	'''
Class for tetrahedral 4-node element.
Has 3 active degrees of freedom per node.
4 nodes gives 12 degrees of freedom total.
'''
	def __init__(self,number,sect,nodes):
		super(TET4N,self).__init__(number,sect,nodes)
		self.EFS = [[1,1,1,0,0,0],]*4
		self.nodeFreedomSignature()
		self.type = 'TET4N'


	def nodeFreedomSignature(self):
		'''
	Update node freedom signature for nodes in element.
	'''
		for i in range(len(self.nodes)):
			if self.nodes[i].NFS[0] == 0:
				self.nodes[i].NFS[0] = 1
			if self.nodes[i].NFS[1] == 0:
				self.nodes[i].NFS[1] = 1
			if self.nodes[i].NFS[2] == 0:
				self.nodes[i].NFS[2] = 1


	def calcStrainDisplacementMatrix(self):
		'''
	Calculate the B-matrix given specific
	node coordinates.
	'''
		x12 = self.nodes[0].coord[0][0] - self.nodes[1].coord[0][0]
		x13 = self.nodes[0].coord[0][0] - self.nodes[2].coord[0][0]
		x14 = self.nodes[0].coord[0][0] - self.nodes[3].coord[0][0]
		x23 = self.nodes[1].coord[0][0] - self.nodes[2].coord[0][0]
		x24 = self.nodes[1].coord[0][0] - self.nodes[3].coord[0][0]
		x34 = self.nodes[2].coord[0][0] - self.nodes[3].coord[0][0]
		x21 = -x12
		x31 = -x13
		x41 = -x14
		x32 = -x23
		x42 = -x24
		x43 = -x34
		y12 = self.nodes[0].coord[1][0] - self.nodes[1].coord[1][0]
		y13 = self.nodes[0].coord[1][0] - self.nodes[2].coord[1][0]
		y14 = self.nodes[0].coord[1][0] - self.nodes[3].coord[1][0]
		y23 = self.nodes[1].coord[1][0] - self.nodes[2].coord[1][0]
		y24 = self.nodes[1].coord[1][0] - self.nodes[3].coord[1][0]
		y34 = self.nodes[2].coord[1][0] - self.nodes[3].coord[1][0]
		y21 = -y12
		y31 = -y13
		y41 = -y14
		y32 = -y23
		y42 = -y24
		y43 = -y34
		z12 = self.nodes[0].coord[2][0] - self.nodes[1].coord[2][0]
		z13 = self.nodes[0].coord[2][0] - self.nodes[2].coord[2][0]
		z14 = self.nodes[0].coord[2][0] - self.nodes[3].coord[2][0]
		z23 = self.nodes[1].coord[2][0] - self.nodes[2].coord[2][0]
		z24 = self.nodes[1].coord[2][0] - self.nodes[3].coord[2][0]
		z34 = self.nodes[2].coord[2][0] - self.nodes[3].coord[2][0]
		z21 = -z12
		z31 = -z13
		z41 = -z14
		z32 = -z23
		z42 = -z24
		z43 = -z34
		
		detJ = x21*(y23*z34-y34*z23) + x32*(y34*z12-y12*z34) + x43*(y12*z23-y23*z12)
		
		invdetJ = 1.0/(6.0*detJ)
		
		dNf_drc = [[y42*z32-y32*z42, y31*z43-y34*z13, y24*z14-y14*z24, y13*z21-y12*z31],
				   [x32*z42-x42*z32, x43*z31-x13*z34, x14*z24-x24*z14, x21*z13-x31*z12],
				   [x42*y32-x32*y42, x31*y43-x34*y13, x24*y14-x14*y24, x13*y21-x12*y31]]

		B = [[],[],[],[],[],[]]
		for l in range(4):
			B[0].append(dNf_drc[0][l])
			B[0].append(0.0)
			B[0].append(0.0)
		for m in range(4):
			B[1].append(0.0)
			B[1].append(dNf_drc[1][m])
			B[1].append(0.0)
		for n in range(4):
			B[2].append(0.0)
			B[2].append(0.0)
			B[2].append(dNf_drc[2][n])
		for p in range(4):
			B[3].append(dNf_drc[1][p])
			B[3].append(dNf_drc[0][p])
			B[3].append(0.0)
		for q in range(4):
			B[4].append(0.0)
			B[4].append(dNf_drc[2][q])
			B[4].append(dNf_drc[1][q])
		for r in range(4):
			B[5].append(dNf_drc[2][r])
			B[5].append(0.0)
			B[5].append(dNf_drc[0][r])
		B = np.array(B)

		return [invdetJ,B]


	def calcStiffnessMatrix(self):
		'''
	Calculate the element stiffness matrix using
	the strain displacement matrix.
	'''
		self.K = np.array([[0.0,]*12,]*12)

		[invdetJ,B] = self.calcStrainDisplacementMatrix()
		self.K = ((B.transpose().dot(self.section.E)).dot(B))*invdetJ + self.K


	def calcMassMatrix(self):
		'''
	Calculate the element mass matrix using the
	lumped mass matrix method.
	'''
		ab = [self.nodes[1].coord[0][0]-self.nodes[0].coord[0][0],
			  self.nodes[1].coord[1][0]-self.nodes[0].coord[1][0],
			  self.nodes[1].coord[2][0]-self.nodes[0].coord[2][0]]
		ac = [self.nodes[2].coord[0][0]-self.nodes[0].coord[0][0],
			  self.nodes[2].coord[1][0]-self.nodes[0].coord[1][0],
			  self.nodes[2].coord[2][0]-self.nodes[0].coord[2][0]]
		ad = [self.nodes[3].coord[0][0]-self.nodes[0].coord[0][0],
			  self.nodes[3].coord[1][0]-self.nodes[0].coord[1][0],
			  self.nodes[3].coord[2][0]-self.nodes[0].coord[2][0]]
		volume = np.linalg.det(np.array([ab,ac,ad]))/6.0
		self.M = np.identity(12)*(self.section.material.density*volume*0.25)


	def calcStrain(self,u,calcStrain,calcStress,sol):		### POSSIBLY WRONG, DOUBLE CHECK THIS!!!
		'''
	Use the element strain-displacement matrix and 
	node displacements to find stresses and strains
	in element at integration points and at nodes.
	This TET4 element only has one constant 
	stress/strain for the whole element.
	'''
		if calcStrain == True:
			self.solutions[sol]['strain'] = {'nodal': {}}
		if calcStress == True:
			self.solutions[sol]['stress'] = {'nodal': {}}

		[invdetJ,B] = self.calcStrainDisplacementMatrix()

		if calcStrain:
			self.solutions[sol]['strain']['nodal'][1] = {'strain_tensor': (B*invdetJ).dot(u), 
									'VonMises': 0., 'MaxPrinc': 0., 'MinPrinc': 0., 'MaxShear': 0.}
			self.solutions[sol]['strain']['nodal'][2] = self.solutions[sol]['strain']['nodal'][1]
			self.solutions[sol]['strain']['nodal'][3] = self.solutions[sol]['strain']['nodal'][1]
			self.solutions[sol]['strain']['nodal'][4] = self.solutions[sol]['strain']['nodal'][1]
		if calcStress:
			self.solutions[sol]['stress']['nodal'][1] = {'stress_tensor': self.section.E.dot((B*invdetJ).dot(u)), 
									'VonMises': 0., 'MaxPrinc': 0., 'MinPrinc': 0., 'MaxShear': 0.}
			self.solutions[sol]['stress']['nodal'][2] = self.solutions[sol]['stress']['nodal'][1]
			self.solutions[sol]['stress']['nodal'][3] = self.solutions[sol]['stress']['nodal'][1]
			self.solutions[sol]['stress']['nodal'][4] = self.solutions[sol]['stress']['nodal'][1]

		if calcStrain == True:
			e = self.solutions[sol]['strain']['nodal']
			e[1]['VonMises'] = sqrt(((e[1]['strain_tensor'][0] - e[1]['strain_tensor'][1])**2 + \
						         (e[1]['strain_tensor'][1] - e[1]['strain_tensor'][2])**2 + \
								 (e[1]['strain_tensor'][0] - e[1]['strain_tensor'][2])**2 + \
								 6*(e[1]['strain_tensor'][3]**2 + e[1]['strain_tensor'][4]**2 + \
								 e[1]['strain_tensor'][5]**2))/2.0)
			e[1]['Principal'] = np.linalg.eigvalsh( \
							[[e[1]['strain_tensor'][0], e[1]['strain_tensor'][3], e[1]['strain_tensor'][4]],
							 [e[1]['strain_tensor'][3], e[1]['strain_tensor'][1], e[1]['strain_tensor'][5]],
							 [e[1]['strain_tensor'][4], e[1]['strain_tensor'][5], e[1]['strain_tensor'][2]]])
			e[1]['MaxPrinc'] = max(e[1]['Principal'])
			e[1]['MinPrinc'] = min(e[1]['Principal'])
			e[1]['MaxShear'] = (e[1]['MaxPrinc']-e[1]['MinPrinc'])/2.0

		if calcStress == True:
			s = self.solutions[sol]['stress']['nodal']
			s[1]['VonMises'] = sqrt(((s[1]['stress_tensor'][0] - s[1]['stress_tensor'][1])**2 + \
						         (s[1]['stress_tensor'][1] - s[1]['stress_tensor'][2])**2 + \
								 (s[1]['stress_tensor'][0] - s[1]['stress_tensor'][2])**2 + \
								 6*(s[1]['stress_tensor'][3]**2 + s[1]['stress_tensor'][4]**2 + \
								 s[1]['stress_tensor'][5]**2))/2.0)
			s[1]['Principal'] = np.linalg.eigvalsh( \
							[[s[1]['stress_tensor'][0], s[1]['stress_tensor'][3], s[1]['stress_tensor'][4]],
							 [s[1]['stress_tensor'][3], s[1]['stress_tensor'][1], s[1]['stress_tensor'][5]],
							 [s[1]['stress_tensor'][4], s[1]['stress_tensor'][5], s[1]['stress_tensor'][2]]])
			s[1]['MaxPrinc'] = max(s[1]['Principal'])
			s[1]['MinPrinc'] = min(s[1]['Principal'])
			s[1]['MaxShear'] = (s[1]['MaxPrinc']-s[1]['MinPrinc'])/2.0





class TET10N(Element):
	'''
Class for tetrahedral 10-node 3D element.
Has 3 active degrees of freedom per node.
10 nodes gives 30 degrees of freedom total.
'''
	def __init__(self,number,sect,nodes,gaussQuad):
		self.gaussPnts = gaussQuad.tet_p4
		super(TET10N,self).__init__(number,sect,nodes)
		self.EFS = [[1,1,1,0,0,0],]*10
		self.nodeFreedomSignature()
		self.type = 'TET10N'


	def nodeFreedomSignature(self):
		'''
	Update node freedom signature for nodes in element.
	'''
		for i in range(len(self.nodes)):
			if self.nodes[i].NFS[0] == 0:
				self.nodes[i].NFS[0] = 1
			if self.nodes[i].NFS[1] == 0:
				self.nodes[i].NFS[1] = 1
			if self.nodes[i].NFS[2] == 0:
				self.nodes[i].NFS[2] = 1


	def calcStrainDisplacementMatrix(self,zeta1,zeta2,zeta3,zeta4):
		'''
	Calculate the B-matrix given specific
	shape function coordinates.
	'''
		Jx1 = 4.0*(self.nodes[0].coord[0][0]*(zeta1-0.25)+self.nodes[4].coord[0][0]*zeta2+ \
				self.nodes[6].coord[0][0]*zeta3+self.nodes[7].coord[0][0]*zeta4)
		Jx2 = 4.0*(self.nodes[4].coord[0][0]*zeta1+self.nodes[1].coord[0][0]*(zeta2-0.25)+ \
				self.nodes[5].coord[0][0]*zeta3+self.nodes[8].coord[0][0]*zeta4)
		Jx3 = 4.0*(self.nodes[6].coord[0][0]*zeta1+self.nodes[5].coord[0][0]*zeta2+ \
				self.nodes[2].coord[0][0]*(zeta3-0.25)+self.nodes[9].coord[0][0]*zeta4)
		Jx4 = 4.0*(self.nodes[7].coord[0][0]*zeta1+self.nodes[8].coord[0][0]*zeta2+ \
				self.nodes[9].coord[0][0]*zeta3+self.nodes[3].coord[0][0]*(zeta4-0.25))
		Jy1 = 4.0*(self.nodes[0].coord[1][0]*(zeta1-0.25)+self.nodes[4].coord[1][0]*zeta2+ \
				self.nodes[6].coord[1][0]*zeta3+self.nodes[7].coord[1][0]*zeta4)
		Jy2 = 4.0*(self.nodes[4].coord[1][0]*zeta1+self.nodes[1].coord[1][0]*(zeta2-0.25)+ \
				self.nodes[5].coord[1][0]*zeta3+self.nodes[8].coord[1][0]*zeta4)
		Jy3 = 4.0*(self.nodes[6].coord[1][0]*zeta1+self.nodes[5].coord[1][0]*zeta2+ \
				self.nodes[2].coord[1][0]*(zeta3-0.25)+self.nodes[9].coord[1][0]*zeta4)
		Jy4 = 4.0*(self.nodes[7].coord[1][0]*zeta1+self.nodes[8].coord[1][0]*zeta2+ \
				self.nodes[9].coord[1][0]*zeta3+self.nodes[3].coord[1][0]*(zeta4-0.25))
		Jz1 = 4.0*(self.nodes[0].coord[2][0]*(zeta1-0.25)+self.nodes[4].coord[2][0]*zeta2+ \
				self.nodes[6].coord[2][0]*zeta3+self.nodes[7].coord[2][0]*zeta4)
		Jz2 = 4.0*(self.nodes[4].coord[2][0]*zeta1+self.nodes[1].coord[2][0]*(zeta2-0.25)+ \
				self.nodes[5].coord[2][0]*zeta3+self.nodes[8].coord[2][0]*zeta4)
		Jz3 = 4.0*(self.nodes[6].coord[2][0]*zeta1+self.nodes[5].coord[2][0]*zeta2+ \
				self.nodes[2].coord[2][0]*(zeta3-0.25)+self.nodes[9].coord[2][0]*zeta4)
		Jz4 = 4.0*(self.nodes[7].coord[2][0]*zeta1+self.nodes[8].coord[2][0]*zeta2+ \
				self.nodes[9].coord[2][0]*zeta3+self.nodes[3].coord[2][0]*(zeta4-0.25))

		Jx12 = Jx1-Jx2
		Jx21 = -Jx12
		Jx13 = Jx1-Jx3
		Jx31 = -Jx13
		Jx14 = Jx1-Jx4
		Jx41 = -Jx14
		Jx23 = Jx2-Jx3
		Jx32 = -Jx23
		Jx24 = Jx2-Jx4
		Jx42 = -Jx24
		Jx34 = Jx3-Jx4
		Jx43 = -Jx34
		Jy12 = Jy1-Jy2
		Jy21 = -Jy12
		Jy13 = Jy1-Jy3
		Jy31 = -Jy13
		Jy14 = Jy1-Jy4
		Jy41 = -Jy14
		Jy23 = Jy2-Jy3
		Jy32 = -Jy23
		Jy24 = Jy2-Jy4
		Jy42 = -Jy24
		Jy34 = Jy3-Jy4
		Jy43 = -Jy34
		Jz12 = Jz1-Jz2
		Jz21 = -Jz12
		Jz13 = Jz1-Jz3
		Jz31 = -Jz13
		Jz14 = Jz1-Jz4
		Jz41 = -Jz14
		Jz23 = Jz2-Jz3
		Jz32 = -Jz23
		Jz24 = Jz2-Jz4
		Jz42 = -Jz24
		Jz34 = Jz3-Jz4
		Jz43 = -Jz34

		detJ = Jx21*(Jy23*Jz34-Jy34*Jz23) + Jx32*(Jy34*Jz12-Jy12*Jz34) + Jx43*(Jy12*Jz23-Jy23*Jz12)

		invdetJ = 1.0/(6.0*detJ)

		a1 = Jy42*Jz32-Jy32*Jz42
		a2 = Jy31*Jz43-Jy34*Jz13
		a3 = Jy24*Jz14-Jy14*Jz24
		a4 = Jy13*Jz21-Jy12*Jz31
		b1 = Jx32*Jz42-Jx42*Jz32
		b2 = Jx43*Jz31-Jx13*Jz34
		b3 = Jx14*Jz24-Jx24*Jz14
		b4 = Jx21*Jz13-Jx31*Jz12
		c1 = Jx42*Jy32-Jx32*Jy42
		c2 = Jx31*Jy43-Jx34*Jy13
		c3 = Jx24*Jy14-Jx14*Jy24
		c4 = Jx13*Jy21-Jx12*Jy31

		dNf_drc = [[(4*zeta1-1)*a1, (4*zeta2-1)*a2, (4*zeta3-1)*a3, (4*zeta4-1)*a4,
					4*(zeta1*a2+zeta2*a1), 4*(zeta2*a3+zeta3*a2), 4*(zeta3*a1+zeta1*a3),
					4*(zeta1*a4+zeta4*a1), 4*(zeta2*a4+zeta4*a2), 4*(zeta3*a4+zeta4*a3)],
				   [(4*zeta1-1)*b1, (4*zeta2-1)*b2, (4*zeta3-1)*b3, (4*zeta4-1)*b4,
					4*(zeta1*b2+zeta2*b1), 4*(zeta2*b3+zeta3*b2), 4*(zeta3*b1+zeta1*b3),
					4*(zeta1*b4+zeta4*b1), 4*(zeta2*b4+zeta4*b2), 4*(zeta3*b4+zeta4*b3)],
				   [(4*zeta1-1)*c1, (4*zeta2-1)*c2, (4*zeta3-1)*c3, (4*zeta4-1)*c4,
					4*(zeta1*c2+zeta2*c1), 4*(zeta2*c3+zeta3*c2), 4*(zeta3*c1+zeta1*c3),
					4*(zeta1*c4+zeta4*c1), 4*(zeta2*c4+zeta4*c2), 4*(zeta3*c4+zeta4*c3)]]

		B = [[],[],[],[],[],[]]
		for l in range(10):
			B[0].append(dNf_drc[0][l])
			B[0].append(0.0)
			B[0].append(0.0)
		for m in range(10):
			B[1].append(0.0)
			B[1].append(dNf_drc[1][m])
			B[1].append(0.0)
		for n in range(10):
			B[2].append(0.0)
			B[2].append(0.0)
			B[2].append(dNf_drc[2][n])
		for p in range(10):
			B[3].append(dNf_drc[1][p])
			B[3].append(dNf_drc[0][p])
			B[3].append(0.0)
		for q in range(10):
			B[4].append(0.0)
			B[4].append(dNf_drc[2][q])
			B[4].append(dNf_drc[1][q])
		for r in range(10):
			B[5].append(dNf_drc[2][r])
			B[5].append(0.0)
			B[5].append(dNf_drc[0][r])
		B = np.array(B)

		return [invdetJ,B]


	def calcStiffnessMatrix(self):
		'''
	Calculate the element stiffness matrix using
	isoparametric shape functions and Gauss Quadrature.
	'''
		self.K = np.array([[0.0,]*30,]*30)
		gauss = len(self.gaussPnts)-1
		zeta1 = 0.0
		zeta2 = 0.0
		zeta3 = 0.0
		zeta4 = 0.0
		w = self.gaussPnts[4]
		for i in range(gauss):
			zeta1 = self.gaussPnts[i][0]
			zeta2 = self.gaussPnts[i][1]
			zeta3 = self.gaussPnts[i][2]
			zeta4 = self.gaussPnts[i][3]

			[invdetJ,B] = self.calcStrainDisplacementMatrix(zeta1,zeta2,zeta3,zeta4)

			self.K = ((B.transpose().dot(self.section.E)).dot(B))*(w*invdetJ) + self.K


	def calcMassMatrix(self):
		'''
	Calculate the element mass matrix using the
	lumped mass matrix method.
	'''
		ab = [self.nodes[1].coord[0][0]-self.nodes[0].coord[0][0],
			  self.nodes[1].coord[1][0]-self.nodes[0].coord[1][0],
			  self.nodes[1].coord[2][0]-self.nodes[0].coord[2][0]]
		ac = [self.nodes[2].coord[0][0]-self.nodes[0].coord[0][0],
			  self.nodes[2].coord[1][0]-self.nodes[0].coord[1][0],
			  self.nodes[2].coord[2][0]-self.nodes[0].coord[2][0]]
		ad = [self.nodes[3].coord[0][0]-self.nodes[0].coord[0][0],
			  self.nodes[3].coord[1][0]-self.nodes[0].coord[1][0],
			  self.nodes[3].coord[2][0]-self.nodes[0].coord[2][0]]
		volume = np.linalg.det(np.array([ab,ac,ad]))/6.0
		self.M = np.identity(30)*(self.section.material.density*volume*0.1)


	def calcStrain(self,u,calcStrain,calcStress,sol):
		'''
	Use the element strain-displacement matrix and 
	node displacements to find stresses and strains
	in element at integration points and at nodes.
	'''
		if calcStrain == True:
			self.solutions[sol]['strain'] = {'int_points': {}, 'nodal': {}}
		if calcStress == True:
			self.solutions[sol]['stress'] = {'int_points': {}, 'nodal': {}}

		gauss = len(self.gaussPnts)-1
		ngauss = gauss
		nodal = 10

		zeta1 = 0.0
		zeta2 = 0.0
		zeta3 = 0.0
		zeta4 = 0.0
		for i in range(gauss):
			zeta1 = self.gaussPnts[i][0]
			zeta2 = self.gaussPnts[i][1]
			zeta3 = self.gaussPnts[i][2]
			zeta4 = self.gaussPnts[i][3]

			[invdetJ,B] = self.calcStrainDisplacementMatrix(zeta1,zeta2,zeta3,zeta4)
			if calcStrain:
				self.solutions[sol]['strain']['int_points'][i+1] = {'strain_tensor': (B*invdetJ).dot(u), 
											'VonMises': 0., 'MaxPrinc': 0., 'MinPrinc': 0., 'MaxShear': 0.}
			if calcStress:
				self.solutions[sol]['stress']['int_points'][i+1] = {'stress_tensor': self.section.E.dot((B*invdetJ).dot(u)), 
											'VonMises': 0., 'MaxPrinc': 0., 'MinPrinc': 0., 'MaxShear': 0.}
		
		zeta = [[1.,0.,0.,0.], [0.,1.,0.,0.], [0.,0.,1.,0.], [0.,0.,0.,1.], [.5,.5,0.,0.],
				[0.,.5,.5,0.], [.5,0.,.5,0.], [.5,0.,0.,.5], [0.,.5,0.,.5], [0.,0.,.5,.5]]
		for j in range(nodal):
			zeta1 = zeta[j][0]
			zeta2 = zeta[j][1]
			zeta3 = zeta[j][2]
			zeta4 = zeta[j][3]

			[invdetJ,B] = self.calcStrainDisplacementMatrix(zeta1,zeta2,zeta3,zeta4)
			if calcStrain:
				self.solutions[sol]['strain']['nodal'][j+1] = {'strain_tensor': (B*invdetJ).dot(u), 
									'VonMises': 0., 'MaxPrinc': 0., 'MinPrinc': 0., 'MaxShear': 0.}
			if calcStress:
				self.solutions[sol]['stress']['nodal'][j+1] = {'stress_tensor': self.section.E.dot((B*invdetJ).dot(u)), 
									'VonMises': 0., 'MaxPrinc': 0., 'MinPrinc': 0., 'MaxShear': 0.}

		if calcStrain == True:
			e = self.solutions[sol]['strain']['int_points']
			for i in range(ngauss):
				e[i+1]['VonMises'] = sqrt(((e[i+1]['strain_tensor'][0] - e[i+1]['strain_tensor'][1])**2 + \
								     (e[i+1]['strain_tensor'][1] - e[i+1]['strain_tensor'][2])**2 + \
									 (e[i+1]['strain_tensor'][0] - e[i+1]['strain_tensor'][2])**2 + \
									 6*(e[i+1]['strain_tensor'][3]**2 + e[i+1]['strain_tensor'][4]**2 + \
									 e[i+1]['strain_tensor'][5]**2))/2.0)
				e[i+1]['Principal'] = np.linalg.eigvalsh( \
								[[e[i+1]['strain_tensor'][0], e[i+1]['strain_tensor'][3], e[i+1]['strain_tensor'][4]],
								 [e[i+1]['strain_tensor'][3], e[i+1]['strain_tensor'][1], e[i+1]['strain_tensor'][5]],
								 [e[i+1]['strain_tensor'][4], e[i+1]['strain_tensor'][5], e[i+1]['strain_tensor'][2]]])
				e[i+1]['MaxPrinc'] = max(e[i+1]['Principal'])
				e[i+1]['MinPrinc'] = min(e[i+1]['Principal'])
				e[i+1]['MaxShear'] = (e[i+1]['MaxPrinc']-e[i+1]['MinPrinc'])/2.0

			e = self.solutions[sol]['strain']['nodal']
			for i in range(nodal):
				e[i+1]['VonMises'] = sqrt(((e[i+1]['strain_tensor'][0] - e[i+1]['strain_tensor'][1])**2 + \
								     (e[i+1]['strain_tensor'][1] - e[i+1]['strain_tensor'][2])**2 + \
									 (e[i+1]['strain_tensor'][0] - e[i+1]['strain_tensor'][2])**2 + \
									 6*(e[i+1]['strain_tensor'][3]**2 + e[i+1]['strain_tensor'][4]**2 + \
									 e[i+1]['strain_tensor'][5]**2))/2.0)
				e[i+1]['Principal'] = np.linalg.eigvalsh( \
								[[e[i+1]['strain_tensor'][0], e[i+1]['strain_tensor'][3], e[i+1]['strain_tensor'][4]],
								 [e[i+1]['strain_tensor'][3], e[i+1]['strain_tensor'][1], e[i+1]['strain_tensor'][5]],
								 [e[i+1]['strain_tensor'][4], e[i+1]['strain_tensor'][5], e[i+1]['strain_tensor'][2]]])
				e[i+1]['MaxPrinc'] = max(e[i+1]['Principal'])
				e[i+1]['MinPrinc'] = min(e[i+1]['Principal'])
				e[i+1]['MaxShear'] = (e[i+1]['MaxPrinc']-e[i+1]['MinPrinc'])/2.0

		if calcStress == True:
			s = self.solutions[sol]['stress']['int_points']
			for i in range(ngauss):
				s[i+1]['VonMises'] = sqrt(((s[i+1]['stress_tensor'][0] - s[i+1]['stress_tensor'][1])**2 + \
								     (s[i+1]['stress_tensor'][1] - s[i+1]['stress_tensor'][2])**2 + \
									 (s[i+1]['stress_tensor'][0] - s[i+1]['stress_tensor'][2])**2 + \
									 6*(s[i+1]['stress_tensor'][3]**2 + s[i+1]['stress_tensor'][4]**2 + \
									 s[i+1]['stress_tensor'][5]**2))/2.0)
				s[i+1]['Principal'] = np.linalg.eigvalsh( \
								[[s[i+1]['stress_tensor'][0], s[i+1]['stress_tensor'][3], s[i+1]['stress_tensor'][4]],
								 [s[i+1]['stress_tensor'][3], s[i+1]['stress_tensor'][1], s[i+1]['stress_tensor'][5]],
								 [s[i+1]['stress_tensor'][4], s[i+1]['stress_tensor'][5], s[i+1]['stress_tensor'][2]]])
				s[i+1]['MaxPrinc'] = max(s[i+1]['Principal'])
				s[i+1]['MinPrinc'] = min(s[i+1]['Principal'])
				s[i+1]['MaxShear'] = (s[i+1]['MaxPrinc']-s[i+1]['MinPrinc'])/2.0

			s = self.solutions[sol]['stress']['nodal']
			for i in range(nodal):
				s[i+1]['VonMises'] = sqrt(((s[i+1]['stress_tensor'][0] - s[i+1]['stress_tensor'][1])**2 + \
								     (s[i+1]['stress_tensor'][1] - s[i+1]['stress_tensor'][2])**2 + \
									 (s[i+1]['stress_tensor'][0] - s[i+1]['stress_tensor'][2])**2 + \
									 6*(s[i+1]['stress_tensor'][3]**2 + s[i+1]['stress_tensor'][4]**2 + \
									 s[i+1]['stress_tensor'][5]**2))/2.0)
				s[i+1]['Principal'] = np.linalg.eigvalsh( \
								[[s[i+1]['stress_tensor'][0], s[i+1]['stress_tensor'][3], s[i+1]['stress_tensor'][4]],
								 [s[i+1]['stress_tensor'][3], s[i+1]['stress_tensor'][1], s[i+1]['stress_tensor'][5]],
								 [s[i+1]['stress_tensor'][4], s[i+1]['stress_tensor'][5], s[i+1]['stress_tensor'][2]]])
				s[i+1]['MaxPrinc'] = max(s[i+1]['Principal'])
				s[i+1]['MinPrinc'] = min(s[i+1]['Principal'])
				s[i+1]['MaxShear'] = (s[i+1]['MaxPrinc']-s[i+1]['MinPrinc'])/2.0





class HEX8N(Element):
	'''
Class for hex 8-node 3D element.
Has 3 active degrees of freedom per node.
8 nodes gives 24 degrees of freedom total.
'''
	def __init__(self,number,sect,nodes,gaussQuad,reducedIntegration=False):
		if reducedIntegration == True:
			self.reducedIntegration = True
			self.gaussPnts = gaussQuad.quad_p1
		else:
			self.reducedIntegration = False
			self.gaussPnts = gaussQuad.quad_p2
		super(HEX8N,self).__init__(number,sect,nodes)
		self.EFS = [[1,1,1,0,0,0],]*8
		self.nodeFreedomSignature()
		self.type = 'HEX8N'


	def nodeFreedomSignature(self):
		'''
	Update node freedom signature for nodes in element.
	'''
		for i in range(len(self.nodes)):
			if self.nodes[i].NFS[0] == 0:
				self.nodes[i].NFS[0] = 1
			if self.nodes[i].NFS[1] == 0:
				self.nodes[i].NFS[1] = 1
			if self.nodes[i].NFS[2] == 0:
				self.nodes[i].NFS[2] = 1


	def calcStrainDisplacementMatrix(self,zeta,eta,ksi):
		'''
	Calculate the B-matrix given specific
	shape function coordinates.
	'''
		dNf_dqc = np.array([[-(1.-eta)*(1.-zeta)*0.125, -(1.-ksi)*(1.-zeta)*0.125, -(1.-ksi)*(1.-eta)*0.125],
							[ (1.-eta)*(1.-zeta)*0.125, -(1.+ksi)*(1.-zeta)*0.125, -(1.+ksi)*(1.-eta)*0.125],
							[ (1.+eta)*(1.-zeta)*0.125,  (1.+ksi)*(1.-zeta)*0.125, -(1.+ksi)*(1.+eta)*0.125],
							[-(1.+eta)*(1.-zeta)*0.125,  (1.-ksi)*(1.-zeta)*0.125, -(1.-ksi)*(1.+eta)*0.125],
							[-(1.-eta)*(1.+zeta)*0.125, -(1.-ksi)*(1.+zeta)*0.125,  (1.-ksi)*(1.-eta)*0.125],
							[ (1.-eta)*(1.+zeta)*0.125, -(1.+ksi)*(1.+zeta)*0.125,  (1.+ksi)*(1.-eta)*0.125],
							[ (1.+eta)*(1.+zeta)*0.125,  (1.+ksi)*(1.+zeta)*0.125,  (1.+ksi)*(1.+eta)*0.125],
							[-(1.+eta)*(1.+zeta)*0.125,  (1.-ksi)*(1.+zeta)*0.125,  (1.-ksi)*(1.+eta)*0.125]])

		J = np.zeros((3,3))
		for i in range(3):
			for j in range(3):
				for a in range(8):
					J[i][j] = J[i][j] + self.nodes[a].coord[i][0]*dNf_dqc[a][j]

		detJ = J[0][0]*(J[1][1]*J[2][2]-J[2][1]*J[1][2]) + \
			   J[0][1]*(J[2][1]*J[0][2]-J[0][1]*J[2][2]) + \
			   J[0][2]*(J[0][1]*J[1][2]-J[0][2]*J[1][1])
			
		invdetJ = 1.0/detJ
		invJ = np.array([[invdetJ*(J[1][1]*J[2][2]-J[2][1]*J[1][2]),
						  invdetJ*(J[2][1]*J[0][2]-J[0][1]*J[2][2]),
						  invdetJ*(J[0][1]*J[1][2]-J[0][2]*J[1][1])],
						 [invdetJ*(J[1][0]*J[2][2]-J[2][0]*J[1][2]),
						  invdetJ*(J[0][0]*J[2][2]-J[2][0]*J[0][2]),
						  invdetJ*(J[0][2]*J[1][0]-J[1][2]*J[0][0])],
						 [invdetJ*(J[1][0]*J[2][1]-J[2][0]*J[1][1]), 
						  invdetJ*(J[2][0]*J[0][1]-J[2][1]*J[0][0]), 
						  invdetJ*(J[0][0]*J[1][1]-J[1][0]*J[0][1])]])

		dNf_drc = np.zeros((8,3))
		for a in range(8):
			for i in range(3):
				for j in range(3):
					dNf_drc[a][i] = dNf_drc[a][i] + dNf_dqc[a][j]*invJ[j][i]
		dNf_drc = dNf_drc.T

		B = [[],[],[],[],[],[]]
		for l in range(8):
			B[0].append(dNf_drc[0][l])
			B[0].append(0.0)
			B[0].append(0.0)
		for m in range(8):
			B[1].append(0.0)
			B[1].append(dNf_drc[1][m])
			B[1].append(0.0)
		for n in range(8):
			B[2].append(0.0)
			B[2].append(0.0)
			B[2].append(dNf_drc[2][n])
		for p in range(8):
			B[3].append(dNf_drc[1][p])
			B[3].append(dNf_drc[0][p])
			B[3].append(0.0)
		for q in range(8):
			B[4].append(0.0)
			B[4].append(dNf_drc[2][q])
			B[4].append(dNf_drc[1][q])
		for r in range(8):
			B[5].append(dNf_drc[2][r])
			B[5].append(0.0)
			B[5].append(dNf_drc[0][r])
		B = np.array(B)

		return [detJ,B]


	def calcStiffnessMatrix(self):
		'''
	Calculate the element stiffness matrix using
	isoparametric shape functions and Gauss Quadrature.
	'''
		self.K = np.array([[0.0,]*24,]*24)
		gauss = len(self.gaussPnts)

		ksi = 0.0
		eta = 0.0
		zeta = 0.0
		w_i = 0.0
		w_j = 0.0
		w_k = 0.0

		for i in range(gauss):
			ksi = self.gaussPnts[i][0]
			w_i = self.gaussPnts[i][1]

			for j in range(gauss):
				eta = self.gaussPnts[j][0]
				w_j = self.gaussPnts[j][1]

				for k in range(gauss):
					zeta = self.gaussPnts[k][0]
					w_k = self.gaussPnts[k][1]

					[detJ,B] = self.calcStrainDisplacementMatrix(ksi,eta,zeta)
					self.K = ((B.T.dot(self.section.E)).dot(B))*(w_i*w_j*w_k*detJ) + self.K
			

	def calcMassMatrix(self):
		'''
	Calculate the element mass matrix using the
	lumped mass matrix method.
	'''
		a0 = [0, 0, 0, 0, 2]
		ab = [1, 5, 5, 2, 6]
		ac = [2, 2, 7, 3, 7]
		ad = [5, 7, 4, 7, 5]
		volume = 0.
		for i in range(5):
			ab_v = [self.nodes[ab[i]].coord[0][0]-self.nodes[a0[i]].coord[0][0],
					self.nodes[ab[i]].coord[1][0]-self.nodes[a0[i]].coord[1][0],
					self.nodes[ab[i]].coord[2][0]-self.nodes[a0[i]].coord[2][0]]
			ac_v = [self.nodes[ac[i]].coord[0][0]-self.nodes[a0[i]].coord[0][0],
					self.nodes[ac[i]].coord[1][0]-self.nodes[a0[i]].coord[1][0],
					self.nodes[ac[i]].coord[2][0]-self.nodes[a0[i]].coord[2][0]]
			ad_v = [self.nodes[ad[i]].coord[0][0]-self.nodes[a0[i]].coord[0][0],
					self.nodes[ad[i]].coord[1][0]-self.nodes[a0[i]].coord[1][0],
					self.nodes[ad[i]].coord[2][0]-self.nodes[a0[i]].coord[2][0]]
			volume += np.linalg.det(np.array([ab_v,ac_v,ad_v]))/6.0
		self.M = np.identity(24)*(self.section.material.density*volume*0.125)


	def calcStrain(self,u,calcStrain,calcStress,sol):
		'''
	Use the element strain-displacement matrix and 
	node displacements to find stresses and strains
	in element at integration points and at nodes.
	'''
		if calcStrain == True:
			self.solutions[sol]['strain'] = {'int_points': {}, 'nodal': {}}
		if calcStress == True:
			self.solutions[sol]['stress'] = {'int_points': {}, 'nodal': {}}

		gauss = len(self.gaussPnts)
		ngauss = gauss**3
		nodal = 8

		ksi = 0.0
		eta = 0.0
		zeta = 0.0

		h = 1
		for i in range(gauss):
			ksi = self.gaussPnts[i][0]
			for j in range(gauss):
				eta = self.gaussPnts[j][0]
				for k in range(gauss):
					zeta = self.gaussPnts[k][0]

					[detJ,B] = self.calcStrainDisplacementMatrix(zeta,eta,ksi)
					if calcStrain:
						self.solutions[sol]['strain']['int_points'][h] = {'strain_tensor': B.dot(u), 
												'VonMises': 0., 'MaxPrinc': 0., 'MinPrinc': 0., 'MaxShear': 0.}
					if calcStress:
						self.solutions[sol]['stress']['int_points'][h] = {'stress_tensor': self.section.E.dot(B.dot(u)), 
												'VonMises': 0., 'MaxPrinc': 0., 'MinPrinc': 0., 'MaxShear': 0.}
					h += 1

		ksietazeta = [[-1.,-1.,-1.], [ 1.,-1.,-1.], [ 1., 1.,-1.], [-1., 1.,-1.],
					  [-1.,-1., 1.], [ 1.,-1., 1.], [ 1., 1., 1.], [-1., 1., 1.]]
		for j in range(nodal):
			ksi  = ksietazeta[j][0]
			eta  = ksietazeta[j][1]
			zeta = ksietazeta[j][2]

			[detJ,B] = self.calcStrainDisplacementMatrix(zeta,eta,ksi)

			if calcStrain:
				self.solutions[sol]['strain']['nodal'][j+1] = {'strain_tensor': B.dot(u), 
									'VonMises': 0., 'MaxPrinc': 0., 'MinPrinc': 0., 'MaxShear': 0.}
			if calcStress:
				self.solutions[sol]['stress']['nodal'][j+1] = {'stress_tensor': self.section.E.dot(B.dot(u)), 
									'VonMises': 0., 'MaxPrinc': 0., 'MinPrinc': 0., 'MaxShear': 0.}

		if calcStrain == True:
			e = self.solutions[sol]['strain']['int_points']
			for i in range(ngauss):
				e[i+1]['VonMises'] = sqrt(((e[i+1]['strain_tensor'][0] - e[i+1]['strain_tensor'][1])**2 + \
								     (e[i+1]['strain_tensor'][1] - e[i+1]['strain_tensor'][2])**2 + \
									 (e[i+1]['strain_tensor'][0] - e[i+1]['strain_tensor'][2])**2 + \
									 6*(e[i+1]['strain_tensor'][3]**2 + e[i+1]['strain_tensor'][4]**2 + \
									 e[i+1]['strain_tensor'][5]**2))/2.0)
				e[i+1]['Principal'] = np.linalg.eigvalsh( \
								[[e[i+1]['strain_tensor'][0], e[i+1]['strain_tensor'][3], e[i+1]['strain_tensor'][4]],
								 [e[i+1]['strain_tensor'][3], e[i+1]['strain_tensor'][1], e[i+1]['strain_tensor'][5]],
								 [e[i+1]['strain_tensor'][4], e[i+1]['strain_tensor'][5], e[i+1]['strain_tensor'][2]]])
				e[i+1]['MaxPrinc'] = max(e[i+1]['Principal'])
				e[i+1]['MinPrinc'] = min(e[i+1]['Principal'])
				e[i+1]['MaxShear'] = (e[i+1]['MaxPrinc']-e[i+1]['MinPrinc'])/2.0

			e = self.solutions[sol]['strain']['nodal']
			for i in range(nodal):
				e[i+1]['VonMises'] = sqrt(((e[i+1]['strain_tensor'][0] - e[i+1]['strain_tensor'][1])**2 + \
								     (e[i+1]['strain_tensor'][1] - e[i+1]['strain_tensor'][2])**2 + \
									 (e[i+1]['strain_tensor'][0] - e[i+1]['strain_tensor'][2])**2 + \
									 6*(e[i+1]['strain_tensor'][3]**2 + e[i+1]['strain_tensor'][4]**2 + \
									 e[i+1]['strain_tensor'][5]**2))/2.0)
				e[i+1]['Principal'] = np.linalg.eigvalsh( \
								[[e[i+1]['strain_tensor'][0], e[i+1]['strain_tensor'][3], e[i+1]['strain_tensor'][4]],
								 [e[i+1]['strain_tensor'][3], e[i+1]['strain_tensor'][1], e[i+1]['strain_tensor'][5]],
								 [e[i+1]['strain_tensor'][4], e[i+1]['strain_tensor'][5], e[i+1]['strain_tensor'][2]]])
				e[i+1]['MaxPrinc'] = max(e[i+1]['Principal'])
				e[i+1]['MinPrinc'] = min(e[i+1]['Principal'])
				e[i+1]['MaxShear'] = (e[i+1]['MaxPrinc']-e[i+1]['MinPrinc'])/2.0

		if calcStress == True:
			s = self.solutions[sol]['stress']['int_points']
			for i in range(ngauss):
				s[i+1]['VonMises'] = sqrt(((s[i+1]['stress_tensor'][0] - s[i+1]['stress_tensor'][1])**2 + \
								     (s[i+1]['stress_tensor'][1] - s[i+1]['stress_tensor'][2])**2 + \
									 (s[i+1]['stress_tensor'][0] - s[i+1]['stress_tensor'][2])**2 + \
									 6*(s[i+1]['stress_tensor'][3]**2 + s[i+1]['stress_tensor'][4]**2 + \
									 s[i+1]['stress_tensor'][5]**2))/2.0)
				s[i+1]['Principal'] = np.linalg.eigvalsh( \
								[[s[i+1]['stress_tensor'][0], s[i+1]['stress_tensor'][3], s[i+1]['stress_tensor'][4]],
								 [s[i+1]['stress_tensor'][3], s[i+1]['stress_tensor'][1], s[i+1]['stress_tensor'][5]],
								 [s[i+1]['stress_tensor'][4], s[i+1]['stress_tensor'][5], s[i+1]['stress_tensor'][2]]])
				s[i+1]['MaxPrinc'] = max(s[i+1]['Principal'])
				s[i+1]['MinPrinc'] = min(s[i+1]['Principal'])
				s[i+1]['MaxShear'] = (s[i+1]['MaxPrinc']-s[i+1]['MinPrinc'])/2.0

			s = self.solutions[sol]['stress']['nodal']
			for i in range(nodal):
				s[i+1]['VonMises'] = sqrt(((s[i+1]['stress_tensor'][0] - s[i+1]['stress_tensor'][1])**2 + \
								     (s[i+1]['stress_tensor'][1] - s[i+1]['stress_tensor'][2])**2 + \
									 (s[i+1]['stress_tensor'][0] - s[i+1]['stress_tensor'][2])**2 + \
									 6*(s[i+1]['stress_tensor'][3]**2 + s[i+1]['stress_tensor'][4]**2 + \
									 s[i+1]['stress_tensor'][5]**2))/2.0)
				s[i+1]['Principal'] = np.linalg.eigvalsh( \
								[[s[i+1]['stress_tensor'][0], s[i+1]['stress_tensor'][3], s[i+1]['stress_tensor'][4]],
								 [s[i+1]['stress_tensor'][3], s[i+1]['stress_tensor'][1], s[i+1]['stress_tensor'][5]],
								 [s[i+1]['stress_tensor'][4], s[i+1]['stress_tensor'][5], s[i+1]['stress_tensor'][2]]])
				s[i+1]['MaxPrinc'] = max(s[i+1]['Principal'])
				s[i+1]['MinPrinc'] = min(s[i+1]['Principal'])
				s[i+1]['MaxShear'] = (s[i+1]['MaxPrinc']-s[i+1]['MinPrinc'])/2.0





class HEX20N(Element):
	'''
Class for hex 20-node 3D element.
Has 3 active degrees of freedom per node.
20 nodes gives 60 degrees of freedom total.
'''
	def __init__(self,number,sect,nodes,gaussQuad):
		self.gaussPnts = gaussQuad.quad_p3
		super(HEX20N,self).__init__(number,sect,nodes)
		self.EFS = [[1,1,1,0,0,0],]*20
		self.nodeFreedomSignature()
		self.type = 'HEX20N'


	def nodeFreedomSignature(self):
		'''
	Update node freedom signature for nodes in element.
	'''
		for i in range(len(self.nodes)):
			if self.nodes[i].NFS[0] == 0:
				self.nodes[i].NFS[0] = 1
			if self.nodes[i].NFS[1] == 0:
				self.nodes[i].NFS[1] = 1
			if self.nodes[i].NFS[2] == 0:
				self.nodes[i].NFS[2] = 1


	def calcStrainDisplacementMatrix(self,zeta,eta,ksi):
		'''
	Calculate the B-matrix given specific
	shape function coordinates.
	'''
		dNf_dqc = np.array([[( (eta-1)*(zeta-1)*( 2*ksi+eta+zeta+1))*0.125,
							 (-(eta-1)*(zeta-1)*(-2*ksi+eta+zeta+1))*0.125,
							 (-(eta+1)*(zeta-1)*( 2*ksi+eta-zeta-1))*0.125,
							 ( (eta+1)*(zeta-1)*(-2*ksi+eta-zeta-1))*0.125,
							 (-(eta-1)*(zeta+1)*( 2*ksi+eta-zeta+1))*0.125,
							 ( (eta-1)*(zeta+1)*(-2*ksi+eta-zeta+1))*0.125,
							 ( (eta+1)*(zeta+1)*( 2*ksi+eta+zeta-1))*0.125,
							 (-(eta+1)*(zeta+1)*(-2*ksi+eta+zeta-1))*0.125,
							 (-2*ksi*(eta-1)*(zeta-1))*0.25,
							 ( ((eta**2)-1)*(zeta-1))*0.25,
							 ( 2*ksi*(eta+1)*(zeta-1))*0.25,
							 (-((eta**2)-1)*(zeta-1))*0.25,
							 (-((zeta**2)-1)*(eta-1))*0.25,
							 ( ((zeta**2)-1)*(eta-1))*0.25,
							 (-((zeta**2)-1)*(eta+1))*0.25,
							 ( ((zeta**2)-1)*(eta+1))*0.25,
							 ( 2*ksi*(eta-1)*(zeta+1))*0.25,
							 (-((eta**2)-1)*(zeta+1))*0.25,
							 (-2*ksi*(eta+1)*(zeta+1))*0.25,
							 ( ((eta**2)-1)*(zeta+1))*0.25],
							[( (ksi-1)*(zeta-1)*( ksi+2*eta+zeta+1))*0.125,
							 ( (ksi+1)*(zeta-1)*( ksi-2*eta-zeta-1))*0.125,
							 (-(ksi+1)*(zeta-1)*( ksi+2*eta-zeta-1))*0.125,
							 (-(ksi-1)*(zeta-1)*( ksi-2*eta+zeta+1))*0.125,
							 (-(ksi-1)*(zeta+1)*( ksi+2*eta-zeta+1))*0.125,
							 (-(ksi+1)*(zeta+1)*( ksi-2*eta+zeta-1))*0.125,
							 ( (ksi+1)*(zeta+1)*( ksi+2*eta+zeta-1))*0.125,
							 ( (ksi-1)*(zeta+1)*( ksi-2*eta-zeta+1))*0.125,
							 (-((ksi**2)-1)*(zeta-1))*0.25,
							 ( 2*eta*(ksi+1)*(zeta-1))*0.25,
							 ( ((ksi**2)-1)*(zeta-1))*0.25,
							 (-2*eta*(ksi-1)*(zeta-1))*0.25,
							 (-((zeta**2)-1)*(ksi-1))*0.25,
							 ( ((zeta**2)-1)*(ksi+1))*0.25,
							 (-((zeta**2)-1)*(ksi+1))*0.25,
							 ( ((zeta**2)-1)*(ksi-1))*0.25,
							 ( ((ksi**2)-1)*(zeta+1))*0.25,
							 (-2*eta*(ksi+1)*(zeta+1))*0.25,
							 (-((ksi**2)-1)*(zeta+1))*0.25,
							 ( 2*eta*(ksi-1)*(zeta+1))*0.25],
							[( (ksi-1)*(eta-1)*( ksi+eta+2*zeta+1))*0.125,
							 ( (ksi+1)*(eta-1)*( ksi-eta-2*zeta-1))*0.125,
							 (-(ksi+1)*(eta+1)*( ksi+eta-2*zeta-1))*0.125,
							 (-(ksi-1)*(eta+1)*( ksi-eta+2*zeta+1))*0.125,
							 (-(ksi-1)*(eta-1)*( ksi+eta-2*zeta+1))*0.125,
							 (-(ksi+1)*(eta-1)*( ksi-eta+2*zeta-1))*0.125,
							 ( (ksi+1)*(eta+1)*( ksi+eta+2*zeta-1))*0.125,
							 ( (ksi-1)*(eta+1)*( ksi-eta-2*zeta+1))*0.125,
							 (-((ksi**2)-1)*(eta-1))*0.25,
							 ( ((eta**2)-1)*(ksi+1))*0.25,
							 ( ((ksi**2)-1)*(eta+1))*0.25,
							 (-((eta**2)-1)*(ksi-1))*0.25,
							 (-2*zeta*(ksi-1)*(eta-1))*0.25,
							 ( 2*zeta*(ksi+1)*(eta-1))*0.25,
							 (-2*zeta*(ksi+1)*(eta+1))*0.25,
							 ( 2*zeta*(ksi-1)*(eta+1))*0.25,
							 ( ((ksi**2)-1)*(eta-1))*0.25,
							 (-((eta**2)-1)*(ksi+1))*0.25,
							 (-((ksi**2)-1)*(eta+1))*0.25,
							 ( ((eta**2)-1)*(ksi-1))*0.25]])
		dNf_dqc = dNf_dqc.T
		
		J = np.zeros((3,3))
		for i in range(3):
			for j in range(3):
				for a in range(20):
					J[i][j] = J[i][j] + self.nodes[a].coord[i][0]*dNf_dqc[a][j]

		detJ = J[0][0]*(J[1][1]*J[2][2]-J[2][1]*J[1][2]) + \
			   J[0][1]*(J[2][1]*J[0][2]-J[0][1]*J[2][2]) + \
			   J[0][2]*(J[0][1]*J[1][2]-J[0][2]*J[1][1])

		invdetJ = 1.0/detJ
		invJ = np.array([[invdetJ*(J[1][1]*J[2][2]-J[2][1]*J[1][2]), 
						  invdetJ*(J[1][0]*J[2][2]-J[2][0]*J[1][2]), 
						  invdetJ*(J[1][0]*J[2][1]-J[2][0]*J[1][1])],
						 [invdetJ*(J[2][1]*J[0][2]-J[0][1]*J[2][2]), 
						  invdetJ*(J[0][0]*J[2][2]-J[2][0]*J[0][2]),
						  invdetJ*(J[2][0]*J[0][1]-J[2][1]*J[0][0])],
						 [invdetJ*(J[0][1]*J[1][2]-J[0][2]*J[1][1]), 
						  invdetJ*(J[0][2]*J[1][0]-J[1][2]*J[0][0]),
						  invdetJ*(J[0][0]*J[1][1]-J[1][0]*J[0][1])]])

		dNf_drc = invJ.dot(dNf_dqc.T)

		B = [[],[],[],[],[],[]]
		for l in range(20):
			B[0].append(dNf_drc[0][l])
			B[0].append(0.0)
			B[0].append(0.0)
		for m in range(20):
			B[1].append(0.0)
			B[1].append(dNf_drc[1][m])
			B[1].append(0.0)
		for n in range(20):
			B[2].append(0.0)
			B[2].append(0.0)
			B[2].append(dNf_drc[2][n])
		for p in range(20):
			B[3].append(dNf_drc[1][p])
			B[3].append(dNf_drc[0][p])
			B[3].append(0.0)
		for q in range(20):
			B[4].append(0.0)
			B[4].append(dNf_drc[2][q])
			B[4].append(dNf_drc[1][q])
		for r in range(20):
			B[5].append(dNf_drc[2][r])
			B[5].append(0.0)
			B[5].append(dNf_drc[0][r])
		B = np.array(B)

		return [detJ,B]


	def calcStiffnessMatrix(self):
		'''
	Calculate the element stiffness matrix using
	isoparametric shape functions and Gauss Quadrature.
	'''
		self.K = np.array([[0.0,]*60,]*60)
		gauss = len(self.gaussPnts)

		ksi = 0.0
		eta = 0.0
		zeta = 0.0
		w_i = 0.0
		w_j = 0.0
		w_k = 0.0

		for i in range(gauss):
			ksi = self.gaussPnts[i][0]
			w_i = self.gaussPnts[i][1]

			for j in range(gauss):
				eta = self.gaussPnts[j][0]
				w_j = self.gaussPnts[j][1]

				for k in range(gauss):
					zeta = self.gaussPnts[k][0]
					w_k = self.gaussPnts[k][1]

					[detJ,B] = self.calcStrainDisplacementMatrix(ksi,eta,zeta)
					self.K = ((B.transpose().dot(self.section.E)).dot(B))*(w_i*w_j*w_k*detJ) + self.K


	def calcMassMatrix(self):
		'''
	Calculate the element mass matrix using the
	lumped mass matrix method.
	'''
		a0 = [0, 0, 0, 0, 2]
		ab = [1, 5, 5, 2, 6]
		ac = [2, 2, 7, 3, 7]
		ad = [5, 7, 4, 7, 5]
		volume = 0.
		for i in range(5):
			ab_v = [self.nodes[ab[i]].coord[0][0]-self.nodes[a0[i]].coord[0][0],
					self.nodes[ab[i]].coord[1][0]-self.nodes[a0[i]].coord[1][0],
					self.nodes[ab[i]].coord[2][0]-self.nodes[a0[i]].coord[2][0]]
			ac_v = [self.nodes[ac[i]].coord[0][0]-self.nodes[a0[i]].coord[0][0],
					self.nodes[ac[i]].coord[1][0]-self.nodes[a0[i]].coord[1][0],
					self.nodes[ac[i]].coord[2][0]-self.nodes[a0[i]].coord[2][0]]
			ad_v = [self.nodes[ad[i]].coord[0][0]-self.nodes[a0[i]].coord[0][0],
					self.nodes[ad[i]].coord[1][0]-self.nodes[a0[i]].coord[1][0],
					self.nodes[ad[i]].coord[2][0]-self.nodes[a0[i]].coord[2][0]]
			volume += np.linalg.det(np.array([ab_v,ac_v,ad_v]))/6.0
		self.M = np.identity(60)*(self.section.material.density*volume*0.05)


	def calcStrain(self,u,calcStrain,calcStress,sol):
		'''
	Use the element strain-displacement matrix and 
	node displacements to find stresses and strains
	in element at integration points and at nodes as
	well as midpoints of element sides for better
	contour plots.
	'''
		if calcStrain == True:
			self.solutions[sol]['strain'] = {'int_points': {}, 'nodal': {}}
		if calcStress == True:
			self.solutions[sol]['stress'] = {'int_points': {}, 'nodal': {}}

		gauss = len(self.gaussPnts)
		ngauss = gauss**3
		nodal = 26

		ksi = 0.0
		eta = 0.0
		zeta = 0.0

		h = 1
		for i in range(gauss):
			ksi = self.gaussPnts[i][0]
			for j in range(gauss):
				eta = self.gaussPnts[j][0]
				for k in range(gauss):
					zeta = self.gaussPnts[k][0]

					[detJ,B] = self.calcStrainDisplacementMatrix(zeta,eta,ksi)
					if calcStrain:
						self.solutions[sol]['strain']['int_points'][h] = {'strain_tensor': B.dot(u), 
												'VonMises': 0., 'MaxPrinc': 0., 'MinPrinc': 0., 'MaxShear': 0.}
					if calcStress:
						self.solutions[sol]['stress']['int_points'][h] = {'stress_tensor': self.section.E.dot(B.dot(u)), 
												'VonMises': 0., 'MaxPrinc': 0., 'MinPrinc': 0., 'MaxShear': 0.}
					h += 1

		ksietazeta = [[-1.,-1.,-1.], [ 1.,-1.,-1.], [ 1., 1.,-1.], [-1., 1.,-1.], [-1.,-1., 1.],
					  [ 1.,-1., 1.], [ 1., 1., 1.], [-1., 1., 1.], [ 0.,-1.,-1.], [ 1., 0.,-1.],
					  [ 0., 1.,-1.], [-1., 0.,-1.], [-1.,-1., 0.], [ 1.,-1., 0.], [ 1., 1., 0.],
					  [-1., 1., 0.], [ 0.,-1., 1.], [ 1., 0., 1.], [ 0., 1., 1.], [-1., 0., 1.],
					  [ 0., 0.,-1.], [ 0., 0., 1.], [ 0.,-1., 0.], [ 1., 0., 0.], [ 0., 1., 0.], [-1., 0., 0.]]
		for j in range(nodal):
			ksi = ksietazeta[j][0]
			eta = ksietazeta[j][1]
			zeta = ksietazeta[j][2]

			[detJ,B] = self.calcStrainDisplacementMatrix(zeta,eta,ksi)

			if calcStrain:
				self.solutions[sol]['strain']['nodal'][j+1] = {'strain_tensor': B.dot(u), 
									'VonMises': 0., 'MaxPrinc': 0., 'MinPrinc': 0., 'MaxShear': 0.}
			if calcStress:
				self.solutions[sol]['stress']['nodal'][j+1] = {'stress_tensor': self.section.E.dot(B.dot(u)), 
									'VonMises': 0., 'MaxPrinc': 0., 'MinPrinc': 0., 'MaxShear': 0.}

		if calcStrain == True:
			e = self.solutions[sol]['strain']['int_points']
			for i in range(ngauss):
				e[i+1]['VonMises'] = sqrt(((e[i+1]['strain_tensor'][0] - e[i+1]['strain_tensor'][1])**2 + \
								     (e[i+1]['strain_tensor'][1] - e[i+1]['strain_tensor'][2])**2 + \
									 (e[i+1]['strain_tensor'][0] - e[i+1]['strain_tensor'][2])**2 + \
									 6*(e[i+1]['strain_tensor'][3]**2 + e[i+1]['strain_tensor'][4]**2 + \
									 e[i+1]['strain_tensor'][5]**2))/2.0)
				e[i+1]['Principal'] = np.linalg.eigvalsh( \
								[[e[i+1]['strain_tensor'][0], e[i+1]['strain_tensor'][3], e[i+1]['strain_tensor'][4]],
								 [e[i+1]['strain_tensor'][3], e[i+1]['strain_tensor'][1], e[i+1]['strain_tensor'][5]],
								 [e[i+1]['strain_tensor'][4], e[i+1]['strain_tensor'][5], e[i+1]['strain_tensor'][2]]])
				e[i+1]['MaxPrinc'] = max(e[i+1]['Principal'])
				e[i+1]['MinPrinc'] = min(e[i+1]['Principal'])
				e[i+1]['MaxShear'] = (e[i+1]['MaxPrinc']-e[i+1]['MinPrinc'])/2.0

			e = self.solutions[sol]['strain']['nodal']
			for i in range(nodal):
				e[i+1]['VonMises'] = sqrt(((e[i+1]['strain_tensor'][0] - e[i+1]['strain_tensor'][1])**2 + \
								     (e[i+1]['strain_tensor'][1] - e[i+1]['strain_tensor'][2])**2 + \
									 (e[i+1]['strain_tensor'][0] - e[i+1]['strain_tensor'][2])**2 + \
									 6*(e[i+1]['strain_tensor'][3]**2 + e[i+1]['strain_tensor'][4]**2 + \
									 e[i+1]['strain_tensor'][5]**2))/2.0)
				e[i+1]['Principal'] = np.linalg.eigvalsh( \
								[[e[i+1]['strain_tensor'][0], e[i+1]['strain_tensor'][3], e[i+1]['strain_tensor'][4]],
								 [e[i+1]['strain_tensor'][3], e[i+1]['strain_tensor'][1], e[i+1]['strain_tensor'][5]],
								 [e[i+1]['strain_tensor'][4], e[i+1]['strain_tensor'][5], e[i+1]['strain_tensor'][2]]])
				e[i+1]['MaxPrinc'] = max(e[i+1]['Principal'])
				e[i+1]['MinPrinc'] = min(e[i+1]['Principal'])
				e[i+1]['MaxShear'] = (e[i+1]['MaxPrinc']-e[i+1]['MinPrinc'])/2.0

		if calcStress == True:
			s = self.solutions[sol]['stress']['int_points']
			for i in range(ngauss):
				s[i+1]['VonMises'] = sqrt(((s[i+1]['stress_tensor'][0] - s[i+1]['stress_tensor'][1])**2 + \
								     (s[i+1]['stress_tensor'][1] - s[i+1]['stress_tensor'][2])**2 + \
									 (s[i+1]['stress_tensor'][0] - s[i+1]['stress_tensor'][2])**2 + \
									 6*(s[i+1]['stress_tensor'][3]**2 + s[i+1]['stress_tensor'][4]**2 + \
									 s[i+1]['stress_tensor'][5]**2))/2.0)
				s[i+1]['Principal'] = np.linalg.eigvalsh( \
								[[s[i+1]['stress_tensor'][0], s[i+1]['stress_tensor'][3], s[i+1]['stress_tensor'][4]],
								 [s[i+1]['stress_tensor'][3], s[i+1]['stress_tensor'][1], s[i+1]['stress_tensor'][5]],
								 [s[i+1]['stress_tensor'][4], s[i+1]['stress_tensor'][5], s[i+1]['stress_tensor'][2]]])
				s[i+1]['MaxPrinc'] = max(s[i+1]['Principal'])
				s[i+1]['MinPrinc'] = min(s[i+1]['Principal'])
				s[i+1]['MaxShear'] = (s[i+1]['MaxPrinc']-s[i+1]['MinPrinc'])/2.0

			s = self.solutions[sol]['stress']['nodal']
			for i in range(nodal):
				s[i+1]['VonMises'] = sqrt(((s[i+1]['stress_tensor'][0] - s[i+1]['stress_tensor'][1])**2 + \
								     (s[i+1]['stress_tensor'][1] - s[i+1]['stress_tensor'][2])**2 + \
									 (s[i+1]['stress_tensor'][0] - s[i+1]['stress_tensor'][2])**2 + \
									 6*(s[i+1]['stress_tensor'][3]**2 + s[i+1]['stress_tensor'][4]**2 + \
									 s[i+1]['stress_tensor'][5]**2))/2.0)
				s[i+1]['Principal'] = np.linalg.eigvalsh( \
								[[s[i+1]['stress_tensor'][0], s[i+1]['stress_tensor'][3], s[i+1]['stress_tensor'][4]],
								 [s[i+1]['stress_tensor'][3], s[i+1]['stress_tensor'][1], s[i+1]['stress_tensor'][5]],
								 [s[i+1]['stress_tensor'][4], s[i+1]['stress_tensor'][5], s[i+1]['stress_tensor'][2]]])
				s[i+1]['MaxPrinc'] = max(s[i+1]['Principal'])
				s[i+1]['MinPrinc'] = min(s[i+1]['Principal'])
				s[i+1]['MaxShear'] = (s[i+1]['MaxPrinc']-s[i+1]['MinPrinc'])/2.0







