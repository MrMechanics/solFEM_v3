#
#
#	solutions.py
#  --------------
#
#	This file holds all solutions objects. It takes matrices
#	from the FEModel objects and calculates results which are
#	stored in text-file and binary (for ploting in viewFEM).
#


import os
import numpy as np
import scipy.sparse as sp
import matplotlib.pyplot as plt

from signaler import *
from math import sqrt
from timeit import time
from scipy.sparse.linalg import ArpackNoConvergence
from scipy.linalg import eigh
from scipy.integrate import cumtrapz





class Solution(object):
	'''
Base class for Finite Element solver. Takes
input in the form of vectors and matrices,
and generates results as requested.
'''
	def __init__(self,name,mesh):
		self.name = name
		self.mesh = mesh


	def applyBoundaryConditions(self):
		'''
	Applies boundary conditions specified in the input
	file to the global stiffness and mass matrices.

	self.K_11		- Part of stiffness matrix arranged
					  so as to exclude DOFs
					  found in self.fixedDOFs.
	self.K_12		- Part of stiffness matrix arranged
					  with regards to boundary 
					  displacements found in
					  self.fixedDOFs.
	self.K_22		- Part of stiffness matrix arranged
					  so as to include only DOFs found
					  in self.fixedDOFs.
	self.M_11		- Part of Mass matrix arranged so
					  as to not include DOFs from
					  self.fixedDOFs. Used with K11 to
					  solve eigenfrequencies and 
					  eigenvectors.
	self.fixedDOFs 	- DOFs with a fixed displacement.
	self.mesh.NFMT	- Node Freedom Map Table.
	self.index11	- List of DOFs for sorting K_11,
					  K_12 and M_11, given K, K_mpc
					  and M.
	'''
		self.fixedDOFs = {}
		for bound in self.boundaries:
			self.boundaries[bound].setDegreeOfFreedomBoundary(self.mesh)
			for DOF in self.boundaries[bound].fixed:
				self.fixedDOFs[DOF] = self.boundaries[bound].fixed[DOF]

		if hasattr(self,'K_mpc'):
			self.index11 = []
			for DOF in range(self.mesh.nDOFs+len(self.MPCs)):
				if DOF not in self.fixedDOFs:
					self.index11.append(DOF)
			for DOF in sorted(self.fixedDOFs.keys()):
				self.index11.append(DOF)

			self.K_11 = self.K_mpc[self.index11[:(self.mesh.nDOFs+len(self.MPCs)-len(self.fixedDOFs))],:] \
									[:,self.index11[:(self.mesh.nDOFs+len(self.MPCs)-len(self.fixedDOFs))]]
			self.K_12 = self.K_mpc[self.index11,:][:,self.index11][range(0,self.mesh.nDOFs+len(self.MPCs)-len(self.fixedDOFs)),:] \
									[:,range(self.mesh.nDOFs+len(self.MPCs)-len(self.fixedDOFs),self.mesh.nDOFs+len(self.MPCs))]
			if self.type in ['Eigenmodes', 'ModalDynamic']:
				if len(self.fixedDOFs) > 0:
					self.K_22 = self.K_mpc[self.index11,:][:,self.index11][range(self.mesh.nDOFs+len(self.MPCs)-len(self.fixedDOFs),self.mesh.nDOFs+len(self.MPCs)),:] \
											[:,range(self.mesh.nDOFs+len(self.MPCs)-len(self.fixedDOFs),self.mesh.nDOFs+len(self.MPCs))]
		else:
			self.index11 = []
			for DOF in range(self.mesh.nDOFs):
				if DOF not in self.fixedDOFs:
					self.index11.append(DOF)
			for DOF in sorted(self.fixedDOFs.keys()):
				self.index11.append(DOF)

			self.K_11 = self.mesh.K[self.index11[:(self.mesh.nDOFs-len(self.fixedDOFs))],:] \
									[:,self.index11[:(self.mesh.nDOFs-len(self.fixedDOFs))]]
			self.K_12 = self.mesh.K[self.index11,:][:,self.index11][range(0,self.mesh.nDOFs-len(self.fixedDOFs)),:] \
									[:,range(self.mesh.nDOFs-len(self.fixedDOFs),self.mesh.nDOFs)]
			if self.type in ['Eigenmodes', 'ModalDynamic']:
				if len(self.fixedDOFs) > 0:
					self.K_22 = self.mesh.K[self.index11,:][:,self.index11][range(self.mesh.nDOFs-len(self.fixedDOFs),self.mesh.nDOFs),:] \
											[:,range(self.mesh.nDOFs-len(self.fixedDOFs),self.mesh.nDOFs)]

		if self.mesh.needMassMatrix == True:
			if hasattr(self,'K_mpc'):
				M = self.mesh.M
				M = np.append(M,np.zeros(len(self.MPCs)))
				M = sp.diags(M,0)
				M = M.tocsc()
				self.M_11 = M[self.index11[:(self.mesh.nDOFs+len(self.MPCs)-len(self.fixedDOFs))],:] \
								[:,self.index11[:(self.mesh.nDOFs+len(self.MPCs)-len(self.fixedDOFs))]]
				if self.type in ['Eigenmodes', 'ModalDynamic']:
					if len(self.fixedDOFs) > 0:
						self.M_12 = M[self.index11,:][:,self.index11][range(0,self.mesh.nDOFs+len(self.MPCs)-len(self.fixedDOFs)),:] \
											[:,range(self.mesh.nDOFs+len(self.MPCs)-len(self.fixedDOFs),self.mesh.nDOFs+len(self.MPCs))]
						self.M_22 = M[self.index11,:][:,self.index11][range(self.mesh.nDOFs+len(self.MPCs)-len(self.fixedDOFs),self.mesh.nDOFs+len(self.MPCs)),:] \
											[:,range(self.mesh.nDOFs+len(self.MPCs)-len(self.fixedDOFs),self.mesh.nDOFs+len(self.MPCs))]
			else:
				M = sp.diags(self.mesh.M,0)
				M = M.tocsc()
				self.M_11 = M[self.index11[:(self.mesh.nDOFs-len(self.fixedDOFs))],:][:,self.index11[:(self.mesh.nDOFs-len(self.fixedDOFs))]]
				if self.type in ['Eigenmodes', 'ModalDynamic']:
					if len(self.fixedDOFs) > 0:
						self.M_12 = M[self.index11,:][:,self.index11][range(0,self.mesh.nDOFs-len(self.fixedDOFs)),:] \
											[:,range(self.mesh.nDOFs-len(self.fixedDOFs),self.mesh.nDOFs)]
						self.M_22 = M[self.index11,:][:,self.index11][range(self.mesh.nDOFs-len(self.fixedDOFs),self.mesh.nDOFs),:] \
											[:,range(self.mesh.nDOFs-len(self.fixedDOFs),self.mesh.nDOFs)]


	def applyConstraints(self):
		'''
	Use constraints input from FEModel to create
	lagrange multipliers that are applied to the
	global stiffness matrix.

	self.mesh.K			- Global stiffness matrix.
	self.K_mpc			- Global stiffness matrix
						  with multipoint
						  constraints applied.
	self.MPCs			- DOFs that have lagrange
						  multipliers.	
	'''
		self.MPCs = {}
		MPC_count = 0
		for constr in self.constraints:
			self.constraints[constr].setupNodePairs(self.mesh)
			self.constraints[constr].lagrangeMultipliers(self.mesh)
			for MPC in self.constraints[constr].lagrange:
				self.MPCs[MPC_count] = self.constraints[constr].lagrange[MPC]
				MPC_count += 1

		if len(self.MPCs) != 0:
			row = []
			col = []
			data = []
			for elm in self.mesh.elements:
				elmDOFs = len(self.mesh.elements[elm].K)
				for j in range(elmDOFs):
					for k in range(elmDOFs):
						row.append(self.mesh.elements[elm].EFT[k])
						col.append(self.mesh.elements[elm].EFT[j])
						data.append(self.mesh.elements[elm].K[j][k])
			for MPC in range(len(self.MPCs)):
				row.append(self.mesh.nDOFs+MPC)
				col.append(self.MPCs[MPC][0])
				data.append(1.)
				row.append(self.mesh.nDOFs+MPC)
				col.append(self.MPCs[MPC][1])
				data.append(-1.)
				row.append(self.MPCs[MPC][0])
				col.append(self.mesh.nDOFs+MPC)
				data.append(1.)
				row.append(self.MPCs[MPC][1])
				col.append(self.mesh.nDOFs+MPC)
				data.append(-1.)
			self.K_mpc = sp.coo_matrix((np.array(data),(np.array(row),np.array(col))), \
										shape=(self.mesh.nDOFs+len(self.MPCs),self.mesh.nDOFs+len(self.MPCs)))
			self.K_mpc = self.K_mpc.tocsc()





class Static(Solution):
	'''
Static solver. Solves for displacements
given the stiffness matrix, K, and the
stiffness matrix modified for loads and
constraints, K_11 and K_12, as well as 
the force vector F.
'''
	def __init__(self,name,mesh):
		self.type = 'Static'
		super(Static,self).__init__(name,mesh)


	def assembleLoadVector(self):
		'''
	Assemble the load vector from loads defined in
	the input file.
	'''
		self.F = np.zeros((self.mesh.nDOFs+len(self.MPCs),1))
		for j in self.loads:
			if self.loads[j].type == 'Gravity':
				self.loads[j].calcDegreeOfFreedomForces(self.mesh.nDOFs,self.mesh.NFMT,self.mesh.elements)
			elif self.loads[j].type == 'ForceDistributed':
				self.loads[j].calcDegreeOfFreedomForces(self.mesh.nDOFs,self.mesh.NFMT,self.mesh.elements,self.fixedDOFs,self.MPCs)
			elif self.loads[j].type == 'Torque':
				self.loads[j].calcDegreeOfFreedomForces(self.mesh.nDOFs,self.mesh.NFMT,self.mesh.nodes)
			else:
				self.loads[j].calcDegreeOfFreedomForces(self.mesh.nDOFs,self.mesh.NFMT)
			for k in range(self.mesh.nDOFs):
				self.F[k] += self.loads[j].F[k]


	def calcDisplacements(self):
		'''
	Calculate displacements for FE-model
	using the scipy sparsity matrix solver.
	
		K u  =  F

	[ K_11  K_12 ] [ u_1 ] = [ F_1 ]
	[ K_21  K_22 ] [ u_2 ]   [ F_2 ]

	[ K_11   0   ] [ u_1 ] = [ F_1 - K_12 u_2 ]
	[  0     I   ] [ u_2 ]   [ 		 u_2	  ]

	self.u			- Global displacement vector.
	u_2				- Displacement vector of known
					  displacements as found in
					  self.fixedDOFs.
	u_1				- Displacement vector of unknown
					  displacements.
	self.F			- Global load vector.
	F_1				- Load vector of known external
					  forces applied.
	F_2				- Load vector of reaction forces
					  on fixed boundary points found
					  in self.fixedDOFs. Not used in
					  calculation.
	self.mesh.K		- Global stiffness matrix.
	self.K_11		- Part of global stiffness matrix
					  rearranged to exclude fixed
					  boundary DOFs.
	self.K_12		- Part of rearranged global
					  stiffness matrix.
	'''
		u_2 = []
		for DOF in sorted(self.fixedDOFs.keys()):
			u_2.append(self.fixedDOFs[DOF])
		u_2 = np.array(u_2)

		F_1 = []
		for DOF in range(self.mesh.nDOFs+len(self.MPCs)):
			if DOF not in self.fixedDOFs:
				F_1.append(self.F[DOF][0])
		F_1 = np.array(F_1)

		if hasattr(self,'K_mpc'):
			u_1 = sp.linalg.spsolve(self.K_11,F_1-self.K_12.dot(u_2))
		else:
			u_1 = sp.linalg.spsolve(self.K_11,F_1-self.K_12.dot(u_2))

		self.u = []
		count_1 = 0
		count_2 = 0
		for DOF in range(self.mesh.nDOFs):
			if DOF in self.fixedDOFs:
				self.u.append(u_2[count_2])
				count_2 += 1
			else:
				self.u.append(u_1[count_1])
				count_1 += 1
		self.u = np.array(self.u)

		for node in self.mesh.nodes:
			if self.name not in self.mesh.nodes[node].solutions:
				self.mesh.nodes[node].solutions[self.name] = {}
			self.mesh.nodes[node].solutions[self.name]['displacement'] = [0., 0., 0., 0., 0., 0., 0.]
			m = 0
			for nfs in range(len(self.mesh.nodes[node].NFS)):
				if self.mesh.nodes[node].NFS[nfs] == 1:
					self.mesh.nodes[node].solutions[self.name]['displacement'][nfs] = self.u[self.mesh.NFMT[node]+m]
					m += 1
				else:
					self.mesh.nodes[node].solutions[self.name]['displacement'][nfs] = 0.0

			self.mesh.nodes[node].solutions[self.name]['displacement'][6] = \
				sqrt(self.mesh.nodes[node].solutions[self.name]['displacement'][0]**2 + \
					 self.mesh.nodes[node].solutions[self.name]['displacement'][1]**2 + \
					 self.mesh.nodes[node].solutions[self.name]['displacement'][2]**2)


	def calcNodeForces(self):
		'''
	Calculate node forces for FE-model.
	'''
		self.F = self.mesh.K.dot(self.u)
		self.F = np.reshape(self.F,(len(self.F),1))
		for j in self.loads:
			if self.loads[j].type == 'ForceDistributed':
				self.F -= self.loads[j].F

		self.reactionForces = {}
		for BC in self.boundaries:
			for node in self.boundaries[BC].nodeset:
				if node not in self.reactionForces:
					self.reactionForces[node] = []

		for node in self.mesh.nodes:
			if 'nodeforce' in self.mesh.nodes[node].solutions[self.name]:
				pass
			elif node in self.reactionForces:
				self.mesh.nodes[node].solutions[self.name]['nodeforce'] = [0., 0., 0., 0., 0., 0., 0.]
				m = 0
				for nfs in range(6):
					if self.mesh.nodes[node].NFS[nfs] == 1:
						self.mesh.nodes[node].solutions[self.name]['nodeforce'][nfs] = float(self.F[self.mesh.NFMT[node]+m])
						m += 1
				self.mesh.nodes[node].solutions[self.name]['nodeforce'][6] = \
							sqrt(self.mesh.nodes[node].solutions[self.name]['nodeforce'][0]**2 + \
								 self.mesh.nodes[node].solutions[self.name]['nodeforce'][1]**2 + \
								 self.mesh.nodes[node].solutions[self.name]['nodeforce'][2]**2)
				self.reactionForces[node] = self.mesh.nodes[node].solutions[self.name]['nodeforce']
			elif 'nodeforce' in self.results:
				for pltxt in self.results['nodeforce']:
					if node in self.nodesets[self.results['nodeforce'][pltxt]]:
						self.mesh.nodes[node].solutions[self.name]['nodeforce'] = [0., 0., 0., 0., 0., 0., 0.]
						m = 0
						for nfs in range(6):
							if self.mesh.nodes[node].NFS[nfs] == 1:
								self.mesh.nodes[node].solutions[self.name]['nodeforce'][nfs] = float(self.F[self.mesh.NFMT[node]+m])
								m += 1
						self.mesh.nodes[node].solutions[self.name]['nodeforce'][6] = \
									sqrt(self.mesh.nodes[node].solutions[self.name]['nodeforce'][0]**2 + \
										 self.mesh.nodes[node].solutions[self.name]['nodeforce'][1]**2 + \
										 self.mesh.nodes[node].solutions[self.name]['nodeforce'][2]**2)
			else:
				pass


	def calcElementForces(self):
		'''
	Calculate element forces for FE-model.
	'''
		if 'elementforce' in self.results:
			print('\tCalculating element forces...')
			for pltxt in self.results['elementforce']:
				for element in self.elementsets[self.results['elementforce'][pltxt]]:
					if self.mesh.elements[element].type in ['ROD2N2D', 'ROD2N', 'BEAM2N2D', 'BEAM2N']:
						if self.name not in self.mesh.elements[element].solutions:
							self.mesh.elements[element].solutions[self.name] = {}
						u = []
						for node in range(len(self.mesh.elements[element].nodes)):
							dof = 0
							for nfs in self.mesh.elements[element].nodes[node].NFS:
								if nfs == 1:
									u.append(self.u[self.mesh.NFMT[self.mesh.elements[element].nodes[node].number]+dof])
									dof += 1
						self.mesh.elements[element].calcForces(u,self.name)
					else:
						pass


	def calcElementStrains(self):
		'''
	Calculate element stresses/strains for 
	elements as requested in input file.
	'''
		strain = False
		stress = False
		if 'strain' in self.results:
			strain = True
		if 'stress' in self.results:
			stress = True
		if stress or strain:
			print('\tCalculating element stresses/strains...')

		if strain:
			for pltxt in self.results['strain']:
				for element in self.elementsets[self.results['strain'][pltxt]]:
					if self.name not in self.mesh.elements[element].solutions:
						self.mesh.elements[element].solutions[self.name] = {}
					u = []
					for node in range(len(self.mesh.elements[element].nodes)):
						dof = 0
						for nfs in self.mesh.elements[element].nodes[node].NFS:
							if nfs == 1:
								u.append(self.u[self.mesh.NFMT[self.mesh.elements[element].nodes[node].number]+dof])
								dof += 1
					self.mesh.elements[element].calcStrain(u,strain,stress,self.name)
		if stress:
			for pltxt in self.results['stress']:
				for element in self.elementsets[self.results['stress'][pltxt]]:
					if self.name not in self.mesh.elements[element].solutions:
						self.mesh.elements[element].solutions[self.name] = {}
					if 'stress' in self.mesh.elements[element].solutions[self.name]:
						pass
					else:
						u = []
						for node in range(len(self.mesh.elements[element].nodes)):
							dof = 0
							for nfs in self.mesh.elements[element].nodes[node].NFS:
								if nfs == 1:
									u.append(self.u[self.mesh.NFMT[self.mesh.elements[element].nodes[node].number]+dof])
									dof += 1
						self.mesh.elements[element].calcStrain(u,strain,stress,self.name)

		if strain:
			print('\t...average element strains...')
			for element in self.mesh.elements:
				if self.name in self.mesh.elements[element].solutions:
					if ('strain' in self.mesh.elements[element].solutions[self.name]):
						for elm_node in range(len(self.mesh.elements[element].nodes)):
							node_number = self.mesh.elements[element].nodes[elm_node].number
							if 'avg_strain' not in self.mesh.nodes[node_number].solutions[self.name]:
								self.mesh.nodes[node_number].solutions[self.name]['avg_strain'] = {'VonMises': 0.,
																								   'MaxPrinc': 0.,
																								   'MinPrinc': 0.,
																								   'MaxShear': 0.,
																								   'elm_count': 0}
							self.mesh.nodes[node_number].solutions[self.name]['avg_strain']['VonMises'] += \
									self.mesh.elements[element].solutions[self.name]['strain']['nodal'][elm_node+1]['VonMises']
							self.mesh.nodes[node_number].solutions[self.name]['avg_strain']['MaxPrinc'] += \
									self.mesh.elements[element].solutions[self.name]['strain']['nodal'][elm_node+1]['MaxPrinc']
							self.mesh.nodes[node_number].solutions[self.name]['avg_strain']['MinPrinc'] += \
									self.mesh.elements[element].solutions[self.name]['strain']['nodal'][elm_node+1]['MinPrinc']
							self.mesh.nodes[node_number].solutions[self.name]['avg_strain']['MaxShear'] += \
									self.mesh.elements[element].solutions[self.name]['strain']['nodal'][elm_node+1]['MaxShear']
							self.mesh.nodes[node_number].solutions[self.name]['avg_strain']['elm_count'] += 1
			for node in self.mesh.nodes:
				if 'avg_strain' in self.mesh.nodes[node].solutions[self.name]:
					if self.mesh.nodes[node].solutions[self.name]['avg_strain']['elm_count'] != 1:
						count = self.mesh.nodes[node].solutions[self.name]['avg_strain']['elm_count']
						self.mesh.nodes[node].solutions[self.name]['avg_strain']['VonMises'] /= count
						self.mesh.nodes[node].solutions[self.name]['avg_strain']['MaxPrinc'] /= count
						self.mesh.nodes[node].solutions[self.name]['avg_strain']['MinPrinc'] /= count
						self.mesh.nodes[node].solutions[self.name]['avg_strain']['MaxShear'] /= count
					del self.mesh.nodes[node].solutions[self.name]['avg_strain']['elm_count']

		if stress:
			print('\t...average element stresses...')
			for element in self.mesh.elements:
				if self.name in self.mesh.elements[element].solutions:
					if ('stress' in self.mesh.elements[element].solutions[self.name]):
						for elm_node in range(len(self.mesh.elements[element].nodes)):
							node_number = self.mesh.elements[element].nodes[elm_node].number
							if 'avg_stress' not in self.mesh.nodes[node_number].solutions[self.name]:
								self.mesh.nodes[node_number].solutions[self.name]['avg_stress'] = {'VonMises': 0.,
																								   'MaxPrinc': 0.,
																								   'MinPrinc': 0.,
																								   'MaxShear': 0.,
																								   'elm_count': 0}
							self.mesh.nodes[node_number].solutions[self.name]['avg_stress']['VonMises'] += \
									self.mesh.elements[element].solutions[self.name]['stress']['nodal'][elm_node+1]['VonMises']
							self.mesh.nodes[node_number].solutions[self.name]['avg_stress']['MaxPrinc'] += \
									self.mesh.elements[element].solutions[self.name]['stress']['nodal'][elm_node+1]['MaxPrinc']
							self.mesh.nodes[node_number].solutions[self.name]['avg_stress']['MinPrinc'] += \
									self.mesh.elements[element].solutions[self.name]['stress']['nodal'][elm_node+1]['MinPrinc']
							self.mesh.nodes[node_number].solutions[self.name]['avg_stress']['MaxShear'] += \
									self.mesh.elements[element].solutions[self.name]['stress']['nodal'][elm_node+1]['MaxShear']
							self.mesh.nodes[node_number].solutions[self.name]['avg_stress']['elm_count'] += 1
			for node in self.mesh.nodes:
				if 'avg_stress' in self.mesh.nodes[node].solutions[self.name]:
					if self.mesh.nodes[node].solutions[self.name]['avg_stress']['elm_count'] != 1:
						count = self.mesh.nodes[node].solutions[self.name]['avg_stress']['elm_count']
						self.mesh.nodes[node].solutions[self.name]['avg_stress']['VonMises'] /= count
						self.mesh.nodes[node].solutions[self.name]['avg_stress']['MaxPrinc'] /= count
						self.mesh.nodes[node].solutions[self.name]['avg_stress']['MinPrinc'] /= count
						self.mesh.nodes[node].solutions[self.name]['avg_stress']['MaxShear'] /= count
					del self.mesh.nodes[node].solutions[self.name]['avg_stress']['elm_count']


	def writeResults(self,filename):
		'''
	Writes results summary to file in ascii format
	and deletes all results not to be saved in binary 
	format using pickle for plotting in viewer.
	'''
		if os.path.exists(filename+'.res'):
			fobj = open(filename+'.res', 'a')
			fobj.write('\n\n\n    |------^------^------^------^------^------^------|\n')
			fobj.write('\t\t\tSOLUTION: '+self.name+' (Static)\n')
			fobj.write('    |------^------^------^------^------^------^------|\n\n')
			max_disp = 0.0
			max_disp_node = 0
			for node in self.mesh.nodes:
				if self.name in self.mesh.nodes[node].solutions:
					if 'displacement' in self.mesh.nodes[node].solutions[self.name]:
						if self.mesh.nodes[node].solutions[self.name]['displacement'][6] > max_disp:
							max_disp = self.mesh.nodes[node].solutions[self.name]['displacement'][6]
							max_disp_node = self.mesh.nodes[node].number
			fobj.write('\n\n\t\t\t MAXIMUM DISPLACEMENT (node '+str(max_disp_node)+'):\n\t\t\t\t%6.3E\n\n' % (max_disp))
			max_stress = 0.0
			max_stress_elm = 0
			if 'stress' in self.results:
				for element in self.mesh.elements:
					if self.name in self.mesh.elements[element].solutions:
						if ('stress' in self.mesh.elements[element].solutions[self.name]):
							for node in range(len(self.mesh.elements[element].solutions[self.name]['stress']['nodal'])):
								if self.mesh.elements[element].solutions[self.name]['stress']['nodal'][node+1]['VonMises'] > max_stress:
									max_stress = self.mesh.elements[element].solutions[self.name]['stress']['nodal'][node+1]['VonMises']
									max_stress_elm = self.mesh.elements[element].number
				fobj.write('\t\t MAXIMUM VONMISES STRESS (element '+str(max_stress_elm)+'):\n\t\t\t\t%6.3E\n\n' % (max_stress))

			line11 = '  |-------------------------------------------------------------|'
			line12 = '  |---------^------------^------------^------------^------------|'
			line21 = '  |---------------------------------------------------------------------------------------------------|'
			line22 = '  |--------^------------^------------^------------^------------^------------^------------^------------|'
			line31 = '  |--------------------------------------------------------------------------------------|'
			line32 = '  |--------^------------^------------^------------^------------^------------^------------|'
			line41 = '  |-------------------------------------------------------------------------------------------------------------------------------------------------------|'
			line42 = '  |--------^------------^------------^------------^------------^------------^------------^------------^------------^------------^------------^------------|'
			template1 = '  |{0:9}|{1:12}|{2:12}|{3:12}|{4:12}|'
			template2 = '  |{0:8}|{1:12}|{2:12}|{3:12}|{4:12}|{5:12}|{6:12}|{7:12}|'
			template3 = '  |{0:8}|{1:12}|{2:12}|{3:12}|{4:12}|{5:12}|{6:12}|'
			template4 = '  |{0:8}|{1:12}|{2:12}|{3:12}|{4:12}|{5:12}|{6:12}|{7:12}|{8:12}|{9:12}|{10:12}|{11:12}|'

			header = ('  NODE', '     X', '     Y', '     Z', '     RX', '     RY', '     RZ')
			fobj.write('\n\n\t\tREACTION FORCES:\n')
			fobj.write(line31+'\n')
			fobj.write(template3.format(*header)+'\n')
			fobj.write(line32+'\n')
			xyz_sum = [0., 0., 0., 0., 0., 0.]
			sumForce = ['  SUM ']
			count = 1
			for node in sorted(self.reactionForces):
				nodeRes  = ['  %04d' % node]
				for xyz in range(6):
					nodeRes.append(' %6.3E' % (self.reactionForces[node][xyz]))
					xyz_sum[xyz] += self.reactionForces[node][xyz]
				if count < 8:
					fobj.write(template3.format(*nodeRes)+'\n')
					count += 1
				elif count == 8:
					fobj.write('  |   ...  |    ....    |    ....    |    ....    |    ....    |    ....    |    ....    |\n')
					count += 1
				else:
					pass
			fobj.write(line32+'\n')
			for xyz in range(6):
				sumForce.append(' %6.3E' % (xyz_sum[xyz]))
			fobj.write(template3.format(*sumForce)+'\n')
			fobj.write(line32+'\n')
			

			for res in self.results:
				if res == 'displacement' and ('text' in self.results['displacement']):
					header = ('  NODE', '  MAGN', '     X', '     Y', '     Z', '     RX', '     RY', '     RZ')
					fobj.write('\n\n\t\tNODE DISPLACEMENTS:\n')
					fobj.write(line21+'\n')
					fobj.write(template2.format(*header)+'\n')
					fobj.write(line22+'\n')
					for node in self.nodesets[self.results[res]['text']]:
						nodeRes = ['  %04d' % (node)]
						nodeRes.append(' %6.3E' % (self.mesh.nodes[node].solutions[self.name]['displacement'][6]))
						for xyz in range(6):
							nodeRes.append(' %6.3E' % (self.mesh.nodes[node].solutions[self.name]['displacement'][xyz]))
						fobj.write(template2.format(*nodeRes)+'\n')
					fobj.write(line22+'\n')

				elif res == 'nodeforce' and ('text' in self.results['nodeforce']):
					header = ('  NODE', '  MAGN', '     X', '     Y', '     Z', '     RX', '     RY', '     RZ')
					fobj.write('\n\n\t\tNODE FORCES:\n')
					fobj.write(line21+'\n')
					fobj.write(template2.format(*header)+'\n')
					fobj.write(line22+'\n')
					for node in self.nodesets[self.results[res]['text']]:
						nodeRes = ['  %04d' % (node)]
						nodeRes.append(' %6.3E' % (self.mesh.nodes[node].solutions[self.name]['nodeforce'][6]))
						for xyz in range(6):
							nodeRes.append(' %6.3E' % (self.mesh.nodes[node].solutions[self.name]['nodeforce'][xyz]))
						fobj.write(template2.format(*nodeRes)+'\n')
						if ('plot' in self.results['nodeforce']) and \
							(node in self.nodesets[self.results[res]['plot']]):
							pass
						else:
							del self.mesh.nodes[node].solutions[self.name]['nodeforce']
					fobj.write(line22+'\n')

				elif res == 'elementforce' and ('text' in self.results['elementforce']):
					header = (' ELEMENT', '   FX   ', '   FY1', '   FZ1', '   MX1', '    MY1', '    MZ1', '    FY2', '   FZ2', '   MX2', '    MY2', '    MZ2')
					fobj.write('\n\n\t\tELEMENT FORCES:\n')
					fobj.write(line41+'\n')
					fobj.write(template4.format(*header)+'\n')
					fobj.write(line42+'\n')
					for element in self.elementsets[self.results[res]['text']]:
						if self.mesh.elements[element].type in ['ROD2N2D', 'ROD2N', 'BEAM2N2D', 'BEAM2N']:
							elmRes = ['  %04d' % (element)]
							for i in range(11):
								elmRes.append(' %6.3E' % (self.mesh.elements[element].solutions[self.name]['elementforce'][i]))
							fobj.write(template4.format(*elmRes)+'\n')
						else:
							elmRes = ['  %04d' % (element)]
							for i in range(11):
								elmRes.append('    N/A     ')
							fobj.write(template4.format(*elmRes)+'\n')
						if ('plot' in self.results['elementforce']) and \
							(element in self.elementsets[self.results[res]['plot']]):
							pass
						else:
							if 'elementforce' in self.mesh.elements[element].solutions[self.name]:
								del self.mesh.elements[element].solutions[self.name]['elementforce']
					fobj.write(line41+'\n')

				elif res == 'strain' and ('text' in self.results['strain']):
					header = (' ELEMENT', '  VONMISES', '  MAXPRIN.', '  MAXSHEAR', '  MINPRIN.')
					fobj.write('\n\n\t\tELEMENT STRAINS:\n')
					fobj.write(line11+'\n')
					fobj.write(template1.format(*header)+'\n')
					fobj.write(line12+'\n')
					for element in self.elementsets[self.results[res]['text']]:
						if self.mesh.elements[element].type in ['BEAM2N2D', 'BEAM2N']:
							elmRes = ['  %04d' % (element)]
							elmRes.append('    N/A     ')
							elmRes.append('    N/A     ')
							elmRes.append('    N/A     ')
							elmRes.append('    N/A     ')
							fobj.write(template1.format(*elmRes)+'\n')
						else:
							elmRes = ['  %04d' % (element)]
							VonMises = 0.0
							for node in range(len(self.mesh.elements[element].solutions[self.name]['strain']['nodal'])):
								if self.mesh.elements[element].solutions[self.name]['strain']['nodal'][node+1]['VonMises'] > VonMises:
									VonMises = self.mesh.elements[element].solutions[self.name]['strain']['nodal'][node+1]['VonMises']
							MaxPrincipal = self.mesh.elements[element].solutions[self.name]['strain']['nodal'][1]['MaxPrinc']
							for node in range(len(self.mesh.elements[element].solutions[self.name]['strain']['nodal'])):
								if self.mesh.elements[element].solutions[self.name]['strain']['nodal'][node+1]['MaxPrinc'] > MaxPrincipal:
									MaxPrincipal = self.mesh.elements[element].solutions[self.name]['strain']['nodal'][node+1]['MaxPrinc']
							MinPrincipal = self.mesh.elements[element].solutions[self.name]['strain']['nodal'][1]['MinPrinc']
							for node in range(len(self.mesh.elements[element].solutions[self.name]['strain']['nodal'])):
								if self.mesh.elements[element].solutions[self.name]['strain']['nodal'][node+1]['MinPrinc'] < MinPrincipal:
									MinPrincipal = self.mesh.elements[element].solutions[self.name]['strain']['nodal'][node+1]['MinPrinc']
							MaxShear = self.mesh.elements[element].solutions[self.name]['strain']['nodal'][1]['MaxShear']
							for node in range(len(self.mesh.elements[element].solutions[self.name]['strain']['nodal'])):
								if self.mesh.elements[element].solutions[self.name]['strain']['nodal'][node+1]['MaxShear'] > MaxShear:
									MaxShear = self.mesh.elements[element].solutions[self.name]['strain']['nodal'][node+1]['MaxShear']
							elmRes.append(' %6.3E' % (VonMises))
							elmRes.append(' %6.3E' % (MaxPrincipal))
							elmRes.append(' %6.3E' % (MaxShear))
							elmRes.append(' %6.3E' % (MinPrincipal))
							fobj.write(template1.format(*elmRes)+'\n')
						if ('plot' in self.results['strain']) and \
							(element in self.elementsets[self.results[res]['plot']]):
							pass
						else:
							if 'strain' in self.mesh.elements[element].solutions[self.name]:
								del self.mesh.elements[element].solutions[self.name]['strain']
					fobj.write(line12+'\n')

				elif res == 'stress' and ('text' in self.results['stress']):
					header = (' ELEMENT', '  VONMISES', '  MAXPRIN.', '  MAXSHEAR', '  MINPRIN.')
					fobj.write('\n\n\t\tELEMENT STRESSES:\n')
					fobj.write(line11+'\n')
					fobj.write(template1.format(*header)+'\n')
					fobj.write(line12+'\n')
					for element in self.elementsets[self.results[res]['text']]:
						if self.mesh.elements[element].type in ['BEAM2N2D', 'BEAM2N']:
							elmRes = ['  %04d' % (element)]
							elmRes.append('    N/A     ')
							elmRes.append('    N/A     ')
							elmRes.append('    N/A     ')
							elmRes.append('    N/A     ')
							fobj.write(template1.format(*elmRes)+'\n')
						else:
							elmRes = ['  %04d' % (element)]
							VonMises = 0.0
							for node in range(len(self.mesh.elements[element].solutions[self.name]['stress']['nodal'])):
								if self.mesh.elements[element].solutions[self.name]['stress']['nodal'][node+1]['VonMises'] > VonMises:
									VonMises = self.mesh.elements[element].solutions[self.name]['stress']['nodal'][node+1]['VonMises']
							MaxPrincipal = self.mesh.elements[element].solutions[self.name]['stress']['nodal'][1]['MaxPrinc']
							for node in range(len(self.mesh.elements[element].solutions[self.name]['stress']['nodal'])):
								if self.mesh.elements[element].solutions[self.name]['stress']['nodal'][node+1]['MaxPrinc'] > MaxPrincipal:
									MaxPrincipal = self.mesh.elements[element].solutions[self.name]['stress']['nodal'][node+1]['MaxPrinc']
							MinPrincipal = self.mesh.elements[element].solutions[self.name]['stress']['nodal'][1]['MinPrinc']
							for node in range(len(self.mesh.elements[element].solutions[self.name]['stress']['nodal'])):
								if self.mesh.elements[element].solutions[self.name]['stress']['nodal'][node+1]['MinPrinc'] < MinPrincipal:
									MinPrincipal = self.mesh.elements[element].solutions[self.name]['stress']['nodal'][node+1]['MinPrinc']
							MaxShear = self.mesh.elements[element].solutions[self.name]['stress']['nodal'][1]['MaxShear']
							for node in range(len(self.mesh.elements[element].solutions[self.name]['stress']['nodal'])):
								if self.mesh.elements[element].solutions[self.name]['stress']['nodal'][node+1]['MaxShear'] > MaxShear:
									MaxShear = self.mesh.elements[element].solutions[self.name]['stress']['nodal'][node+1]['MaxShear']
							elmRes.append(' %6.3E' % (VonMises))
							elmRes.append(' %6.3E' % (MaxPrincipal))
							elmRes.append(' %6.3E' % (MaxShear))
							elmRes.append(' %6.3E' % (MinPrincipal))
							fobj.write(template1.format(*elmRes)+'\n')
						if ('plot' in self.results['stress']) and \
							(element in self.elementsets[self.results[res]['plot']]):
							pass
						else:
							if 'stress' in self.mesh.elements[element].solutions[self.name]:
								del self.mesh.elements[element].solutions[self.name]['stress']
					fobj.write(line12+'\n')

				else:
					pass

			fobj.write('\n\n\n')
			fobj.close()

		else:
			print('ERROR: problem writing to solution file '+filename+'.res')





class StaticPlastic(Solution):
	'''
Non-linear Static solver with material
plasticity.
'''
	def __init__(self,name,mesh):
		self.type = 'StaticPlastic'
		super(StaticPlastic,self).__init__(name,mesh)





class Eigenmodes(Solution):
	'''
Eigenmodes solver. Solves for eigenfrequencies
given the modified stiffness matrix, K_11, and the
modified mass matrix, M_11.
'''
	def __init__(self,name,mesh):
		self.type = 'Eigenmodes'
		super(Eigenmodes,self).__init__(name,mesh)
		self.is3D = True
		for element in mesh.elements:
			if mesh.elements[element].type in ['ROD2N2D', 'BEAM2N2D', 'TRI3N',
								'TRI6N', 'QUAD4N', 'QUAD8N']:
				self.is3D = False
				break


	def calcCenterOfMass(self):
		'''
	Calculate the center of mass for the
	mesh used in this solution.
	'''
		self.mesh.centerOfMass = np.array([[0.],[0.],[0.]])
		for element in self.mesh.elements:
			for node in range(len(self.mesh.elements[element].nodes)):
				self.mesh.centerOfMass += self.mesh.elements[element].M[0][0]*np.array(self.mesh.elements[element].nodes[node].coord)
		self.mesh.centerOfMass = self.mesh.centerOfMass*(1.0/self.mesh.totalMass[0])


	def calcInertiaTensor(self):	# WRONG RESULTS?? NOT THE SAME AS CALCULATED IN FREECAD
		'''
	Calculate the inertia tensor for the
	mesh used in this solution. Both about
	the origin and about the center of mass.
	'''
		Ixx = 0.
		Iyy = 0.
		Izz = 0.
		Ixy = 0.
		Ixz = 0.
		Iyz = 0.
		for element in self.mesh.elements:
			for node in range(len(self.mesh.elements[element].nodes)):
				Ixx += self.mesh.elements[element].M[0][0]*(self.mesh.elements[element].nodes[node].coord[1][0]**2 + \
															self.mesh.elements[element].nodes[node].coord[2][0]**2)
				Iyy += self.mesh.elements[element].M[0][0]*(self.mesh.elements[element].nodes[node].coord[0][0]**2 + \
															self.mesh.elements[element].nodes[node].coord[2][0]**2)
				Izz += self.mesh.elements[element].M[0][0]*(self.mesh.elements[element].nodes[node].coord[0][0]**2 + \
															self.mesh.elements[element].nodes[node].coord[1][0]**2)
				Ixy += self.mesh.elements[element].M[0][0]*(self.mesh.elements[element].nodes[node].coord[0][0]*self.mesh.elements[element].nodes[node].coord[1][0])
				Ixz += self.mesh.elements[element].M[0][0]*(self.mesh.elements[element].nodes[node].coord[0][0]*self.mesh.elements[element].nodes[node].coord[2][0])
				Iyz += self.mesh.elements[element].M[0][0]*(self.mesh.elements[element].nodes[node].coord[1][0]*self.mesh.elements[element].nodes[node].coord[2][0])
		self.mesh.inertiaOrigin = np.array([[ Ixx,-Ixy,-Ixz],
											[-Ixy, Iyy,-Iyz],
											[-Ixz,-Iyz, Izz]])
		Ixx = 0.
		Iyy = 0.
		Izz = 0.
		Ixy = 0.
		Ixz = 0.
		Iyz = 0.
		for element in self.mesh.elements:
			for node in range(len(self.mesh.elements[element].nodes)):
				Ixx += self.mesh.elements[element].M[0][0]*((self.mesh.elements[element].nodes[node].coord[1][0]-self.mesh.centerOfMass[1][0])**2 + \
															(self.mesh.elements[element].nodes[node].coord[2][0]-self.mesh.centerOfMass[2][0])**2)
				Iyy += self.mesh.elements[element].M[0][0]*((self.mesh.elements[element].nodes[node].coord[0][0]-self.mesh.centerOfMass[0][0])**2 + \
															(self.mesh.elements[element].nodes[node].coord[2][0]-self.mesh.centerOfMass[2][0])**2)
				Izz += self.mesh.elements[element].M[0][0]*((self.mesh.elements[element].nodes[node].coord[0][0]-self.mesh.centerOfMass[0][0])**2 + \
															(self.mesh.elements[element].nodes[node].coord[1][0]-self.mesh.centerOfMass[1][0])**2)
				Ixy += self.mesh.elements[element].M[0][0]*((self.mesh.elements[element].nodes[node].coord[0][0]-self.mesh.centerOfMass[0][0])\
														   *(self.mesh.elements[element].nodes[node].coord[1][0]-self.mesh.centerOfMass[1][0]))
				Ixz += self.mesh.elements[element].M[0][0]*((self.mesh.elements[element].nodes[node].coord[0][0]-self.mesh.centerOfMass[0][0])\
														   *(self.mesh.elements[element].nodes[node].coord[2][0]-self.mesh.centerOfMass[2][0]))
				Iyz += self.mesh.elements[element].M[0][0]*((self.mesh.elements[element].nodes[node].coord[1][0]-self.mesh.centerOfMass[1][0])\
														   *(self.mesh.elements[element].nodes[node].coord[2][0]-self.mesh.centerOfMass[2][0]))
		self.mesh.inertiaCenterOfMass = np.array([[ Ixx,-Ixy,-Ixz],
												  [-Ixy, Iyy,-Iyz],
												  [-Ixz,-Iyz, Izz]])


	def calcEigenvalues(self):
		'''
	Calculate selected number of eigenvalues
	using the scipy sparsity matrix solver.
	
		([K] - w2[M])[D] = [0]

	self.K_11				- Stiffness matrix of model
							  modified to exclude DOFs
							  listed in self.fixedDOFs.
	self.M_11				- Mass matrix of model
							  modified to exclude DOFs
							  listed in self.fixedDOFs.
	self.X					- Mass normalized eigenvectors
							  modified to exclude DOFs
							  listed in self.fixedDOFs.
	self.fixedDOFs			- List of fixed DOFs.
	self.mesh.nDOFs			- Total number of DOFs.
	self.eigenvalues		- List of caluclated
							  eigenvalues.
	self.eigenfrequencies	- self.eigenvalues converted
							  to frequencies.
								eigf = sqrt(eigv)/2pi
	self.eigenvectors		- Eigenvectors used to
							  build displaylists in
							  viewer showing the
							  eigenmodes in the model
							  corresponding to their
							  eigenfrequencies.
	'''
		try:
			self.eigenvalues, self.eigenvectors = sp.linalg.eigsh(self.K_11,self.results['modeshapes'],self.M_11,
								sigma=0,which='LM',tol=1.0e-5,maxiter=10000)
		except sp.linalg.ArpackNoConvergence as ee:
			eigs = ee.eigenvalues
			svecs = ee.eigenvectors
			output('only %d eigenvalues converged!' % len(eigs))

		self.eigenfrequencies = []
		for i in range(len(self.eigenvalues)):
			if self.eigenvalues[i] <= 0.:
				print('\tfound negative eigenvalues!!!')
				self.eigenfrequencies.append(sqrt(abs(self.eigenvalues[i])/(2.0*3.14159)))
			else:
				self.eigenfrequencies.append(sqrt(self.eigenvalues[i])/(2.0*3.14159))

		self.X = self.eigenvectors.copy()
		for DOF in range(self.mesh.nDOFs):
			if DOF not in self.fixedDOFs:
				pass
			else:
				self.eigenvectors = np.insert(self.eigenvectors,DOF,0.,axis=0)


	def calcModalEffectiveMass(self):	### WRONG!!!
		'''
	Calculate the modal effective mass for
	every eigenmode using the normalized
	eigenvectors.
	'''
		nModes = self.results['modeshapes']
		nDOFs = self.mesh.nDOFs
		NFMT = self.mesh.NFMT
		NFAT = self.mesh.NFAT

		self.massOfFixedDOFs = np.zeros(3)
#		self.centerOfFixedDOFs = np.zeros(3)
		x_count = 0
		y_count = 0
		z_count = 0
		for DOF in self.fixedDOFs:
			Nodes = sorted(NFMT.keys())
			previous_node = Nodes[0]
			for node in Nodes:
				if previous_node == node:
					pass
				elif NFMT[previous_node] <= DOF < NFMT[node]:
					dof_count = 0
					for dof in range(6):
						if NFAT[previous_node][dof] == 1:
							if NFMT[previous_node]+dof_count == DOF:
								if dof_count == 0:
#									self.centerOfFixedDOFs[0] += self.mesh.nodes[previous_node].coord[0][0]
									self.massOfFixedDOFs[0] += self.mesh.M[DOF]
									x_count += 1
								elif dof_count == 1:
#									self.centerOfFixedDOFs[1] += self.mesh.nodes[previous_node].coord[1][0]
									self.massOfFixedDOFs[1] += self.mesh.M[DOF]
									y_count += 1
								elif dof_count == 2:
#									self.centerOfFixedDOFs[2] += self.mesh.nodes[previous_node].coord[2][0]
									self.massOfFixedDOFs[2] += self.mesh.M[DOF]
									z_count += 1
								else:
									pass
							dof_count += 1
				elif node == Nodes[-1] and DOF > NFMT[node]:
					dof_count = 0
					for dof in range(6):
						if NFAT[node][dof] == 1:
							if NFMT[node]+dof_count == DOF:
								if dof_count == 0:
#									self.centerOfFixedDOFs[0] += self.mesh.nodes[node].coord[0][0]
									self.massOfFixedDOFs[0] += self.mesh.M[DOF]
									x_count += 1
								elif dof_count == 1:
#									self.centerOfFixedDOFs[1] += self.mesh.nodes[node].coord[1][0]
									self.massOfFixedDOFs[1] += self.mesh.M[DOF]
									y_count += 1
								elif dof_count == 2:
#									self.centerOfFixedDOFs[2] += self.mesh.nodes[node].coord[2][0]
									self.massOfFixedDOFs[2] += self.mesh.M[DOF]
									z_count += 1
								else:
									pass
							dof_count += 1
				else:
					pass
				previous_node = node

		r = np.ones(nDOFs+len(self.MPCs)-len(self.fixedDOFs))
		r = sp.diags(r,0)
		r = r.tocsc()

		self.evecs = sp.csc_matrix(self.X)
		del self.X
		L = self.evecs.T.dot(self.M_11.dot(r))
		L = L.toarray()
		L = L.T
		for DOF in range(self.mesh.nDOFs):
			if DOF not in self.fixedDOFs:
				pass
			else:
				L = np.insert(L,DOF,0.,axis=0)
		L = L.T

		self.modalMass = {}
		for mode in range(nModes):
			self.modalMass[mode+1] = [0., 0., 0., 0., 0., 0.]
			for node in NFMT:
				dof_count = 0
				for dof in range(6):
					if NFAT[node][dof] == 1:
						dof_count += 1
						self.modalMass[mode+1][dof] += L[mode][NFMT[node]+dof_count-1]**2
		del self.evecs


	def calcStrainEnergyDensity(self):
		'''
	Calculate element strain energy density
	as requested in input file.
	'''
		pass


	def writeResults(self,filename):
		'''
	Writes results summary to *.res-file with
	eigenfrequencies, mass, center of mass,
	inertia tensor and modal effective mass.
	'''
		if os.path.exists(filename+'.res'):
			fobj = open(filename+'.res', 'a')
			fobj.write('\n\n\n    |------^------^------^------^------^------^------|\n')
			fobj.write('\t\t\tSOLUTION: '+self.name+' ('+self.type+')\n')
			fobj.write('    |------^------^------^------^------^------^------|\n\n')
			fobj.write('\n\t\t\t TOTAL MASS:\n\t\t\t %6.3E\n' % (self.mesh.totalMass[0]))
			self.calcCenterOfMass()
			fobj.write('\n\t\t   CENTER OF MASS:\n\t\t [ %.2f, %.2f, %.2f ]\n' % (self.mesh.centerOfMass[0][0], \
																				  self.mesh.centerOfMass[1][0], \
																				  self.mesh.centerOfMass[2][0]))
			self.calcInertiaTensor()
			fobj.write('\n\t\t   INERTIA TENSOR (ABOUT ORIGIN):' % (self.mesh.totalMass[0]))
			fobj.write('\n\t\t [ %.4E, %.4E, %.4E ]' % (self.mesh.inertiaOrigin[0][0], \
														  self.mesh.inertiaOrigin[0][1], \
														  self.mesh.inertiaOrigin[0][2]))
			fobj.write('\n\t\t [ %.4E, %.4E, %.4E ]' % (self.mesh.inertiaOrigin[1][0], \
														  self.mesh.inertiaOrigin[1][1], \
														  self.mesh.inertiaOrigin[1][2]))
			fobj.write('\n\t\t [ %.4E, %.4E, %.4E ]' % (self.mesh.inertiaOrigin[2][0], \
														  self.mesh.inertiaOrigin[2][1], \
														  self.mesh.inertiaOrigin[2][2]))
			fobj.write('\n\n\t\t   INERTIA TENSOR (ABOUT CENTER OF MASS):' % (self.mesh.totalMass[0]))
			fobj.write('\n\t\t [ %.4E, %.4E, %.4E ]' % (self.mesh.inertiaCenterOfMass[0][0], \
														  self.mesh.inertiaCenterOfMass[0][1], \
														  self.mesh.inertiaCenterOfMass[0][2]))
			fobj.write('\n\t\t [ %.4E, %.4E, %.4E ]' % (self.mesh.inertiaCenterOfMass[1][0], \
														  self.mesh.inertiaCenterOfMass[1][1], \
														  self.mesh.inertiaCenterOfMass[1][2]))
			fobj.write('\n\t\t [ %.4E, %.4E, %.4E ]' % (self.mesh.inertiaCenterOfMass[2][0], \
														  self.mesh.inertiaCenterOfMass[2][1], \
														  self.mesh.inertiaCenterOfMass[2][2]))
			self.calcModalEffectiveMass()
			line11 = '  |-----------------------------------------------------------------------------------------------------|'
			line12 = '  |------^----------------^------------^------------^------------^------------^------------^------------|'
			line13 = '  |-----------------------^------------^------------^------------^------------^------------^------------|'
			template1 = '  |{0:6}|{1:16}|{2:12}|{3:12}|{4:12}|{5:12}|{6:12}|{7:12}|'
			template2 = '  |{0:23}|{1:12}|{2:12}|{3:12}|{4:12}|{5:12}|{6:12}|'
			for i in self.results:
				if i == 'modeshapes':
					header = (' MODE ', ' EIGENFREQUENCY ', '  M_EFF_X', '  M_EFF_Y', '  M_EFF_Z', '  M_EFF_RX', '  M_EFF_RY', '  M_EFF_RZ')
					fobj.write('\n\n\n\t\tEIGENMODES:  ### WRONG MODAL EFFECTIVE MASS ###\n')
					fobj.write(line11+'\n')
					fobj.write(template1.format(*header)+'\n')
					fobj.write(line12+'\n')
					m_effX_total = 0.
					m_effY_total = 0.
					m_effZ_total = 0.
					m_effRX_total = 0.
					m_effRY_total = 0.
					m_effRZ_total = 0.
					for j in range(self.results[i]):
						nodeRes = ['  %03d' % (j+1)]
						nodeRes.append('    %.4E' % (self.eigenfrequencies[j]))
						nodeRes.append(' %.4E' % (self.modalMass[j+1][0]))
						m_effX_total += self.modalMass[j+1][0]
						nodeRes.append(' %.4E' % (self.modalMass[j+1][1]))
						m_effY_total += self.modalMass[j+1][1]
						nodeRes.append(' %.4E' % (self.modalMass[j+1][2]))
						m_effZ_total += self.modalMass[j+1][2]
						nodeRes.append(' %.4E' % (self.modalMass[j+1][3]))
						m_effRX_total += self.modalMass[j+1][3]
						nodeRes.append(' %.4E' % (self.modalMass[j+1][4]))
						m_effRY_total += self.modalMass[j+1][4]
						nodeRes.append(' %.4E' % (self.modalMass[j+1][5]))
						m_effRZ_total += self.modalMass[j+1][5]
						fobj.write(template1.format(*nodeRes)+'\n')
					fobj.write(line12+'\n')
					nodeRes = ['  SUM MODAL EFF. MASS']
					nodeRes.append(' %.4E' % (m_effX_total))
					nodeRes.append(' %.4E' % (m_effY_total))
					nodeRes.append(' %.4E' % (m_effZ_total))
					nodeRes.append(' %.4E' % (m_effRX_total))
					nodeRes.append(' %.4E' % (m_effRY_total))
					nodeRes.append(' %.4E' % (m_effRZ_total))
					fobj.write(template2.format(*nodeRes)+'\n')
					nodeRes = ['     (IN PERCENT)']
					nodeRes.append(' %.2f' % (100*m_effX_total/(self.mesh.totalMass[0] - self.massOfFixedDOFs[0])))
					nodeRes.append(' %.2f' % (100*m_effY_total/(self.mesh.totalMass[0] - self.massOfFixedDOFs[1])))
					nodeRes.append(' %.2f' % (100*m_effZ_total/(self.mesh.totalMass[0] - self.massOfFixedDOFs[2])))
					nodeRes.append('  ...')
					nodeRes.append('  ...')
					nodeRes.append('  ...')
					fobj.write(template2.format(*nodeRes)+'\n')
					fobj.write(line13+'\n')
				else:
					pass

			fobj.write('\n\n\n')
			fobj.close()

		else:
			print('WARNING: problem writing to solution file...')





class ModalDynamic(Eigenmodes):
	'''
Modal dynamics solver. Calculates eigenvalues
and eigenvectors for use in a transient dynamic
analysis. Takes dynamic forces with fixed nodes
boundary condition, or applies acceleration to
fixed nodes boundary condition.

Results can be requested for displacement (comes
as relative displacement if accelerated base),
velocity, acceleration and a fourier transform
of the acceleration.
'''
	def __init__(self,name,mesh):
		super(ModalDynamic,self).__init__(name,mesh)
		self.type = 'ModalDynamic'
		self.hasBaseMotion = False


	def calcEigenvalues(self):
		'''
	Calculate selected number of eigenvalues
	using the scipy sparsity matrix solver.
	
		([K] - w2[M])[D] = [0]

	self.K_11				- Stiffness matrix of model
							  modified to exclude DOFs
							  listed in self.fixedDOFs.
	self.M_11				- Mass matrix of model
							  modified to exclude DOFs
							  listed in self.fixedDOFs.
	self.X					- Mass normalized eigenvectors
							  modified to exclude DOFs
							  listed in self.fixedDOFs.
	self.fixedDOFs			- List of fixed DOFs.
	self.mesh.nDOFs			- Total number of DOFs.
	self.eigenvalues		- List of caluclated
							  eigenvalues.
	self.eigenfrequencies	- self.eigenvalues converted
							  to frequencies.
								eigf = sqrt(eigv)/2pi
	self.eigenvectors		- Eigenvectors used to
							  build displaylists in
							  viewer showing the
							  eigenmodes in the model
							  corresponding to their
							  eigenfrequencies.
	'''
		if self.hasBaseMotion:
			# rearrange the stiffness and mass matrices
			# with regards to the accelerated boundary DOFs
			L = self.mesh.nDOFs+len(self.MPCs)						# total number of DOFs
			M = self.mesh.nDOFs+len(self.MPCs)-len(self.fixedDOFs)	# number of internal DOFs
			N = len(self.fixedDOFs)									# number of fixed DOFs

			self.T1 = -sp.linalg.inv(self.K_11).dot(self.K_12)
			T2 = np.ones(M)
			T2 = sp.diags(T2,0)
			self.T2 = T2.tocsc()
			TT_1 = 0
			if N > 1:
				TT_1 = np.ones(N)
			else:
				TT_1 = np.array([[1.]])
			TT_1 = sp.diags(TT_1,0)
			TT_1 = TT_1.tocsc()
			TT_0 = sp.csc_matrix((N,M))
			TT = sp.vstack([sp.hstack([TT_1,TT_0]),sp.hstack([self.T1,self.T2])])

			M_q = sp.vstack([sp.hstack([self.M_22,self.M_12.T]),sp.hstack([self.M_12,self.M_11])])
			m_q = TT.T.dot(M_q.dot(TT))
#			m_22 = m_q[range(N)][:,range(N)]
			m_w2 = m_q[range(N)][:,range(N,m_q.shape[0])]
			self.m_w2 = m_w2.T
			self.m_ww = m_q[range(N,m_q.shape[0])][:,range(N,m_q.shape[0])]

			K_q = sp.vstack([sp.hstack([self.K_22,self.K_12.T]),sp.hstack([self.K_12,self.K_11])])
			k_q = TT.T.dot(K_q.dot(TT))
#			k_22 = k_q[range(N)][:,range(N)]
#			k_w2 = k_q[range(N)][:,range(N,m_q.shape[0])]
#			k_w2 = k_w2.T
			self.k_ww = k_q[range(N,m_q.shape[0])][:,range(N,m_q.shape[0])]
			
			try:
				self.eigenvalues, self.eigenvectors = sp.linalg.eigsh(k_q[range(N,L)][:,range(N,L)],self.results['modeshapes'],m_q[range(N,L)][:,range(N,L)],
										sigma=0,which='LM',tol=1.0e-5,maxiter=10000)
			except sp.linalg.ArpackNoConvergence as ee:
				eigs = ee.eigenvalues
				svecs = ee.eigenvectors
				output('only %d eigenvalues converged!' % len(eigs))


		else:
			# use the same constrained stiffness and 
			# mass matrices that are used in a static solution
			try:
				self.eigenvalues, self.eigenvectors = sp.linalg.eigsh(self.K_11,self.results['modeshapes'],self.M_11,
									sigma=0,which='LM',tol=1.0e-5,maxiter=10000)
			except sp.linalg.ArpackNoConvergence as ee:
				eigs = ee.eigenvalues
				svecs = ee.eigenvectors
				output('only %d eigenvalues converged!' % len(eigs))

		self.eigenfrequencies = []
		for i in range(len(self.eigenvalues)):
			if self.eigenvalues[i] <= 0.:
				print('\tfound negative eigenvalues!!!')
				self.eigenfrequencies.append(sqrt(abs(self.eigenvalues[i])/(2.0*3.14159)))
			else:
				self.eigenfrequencies.append(sqrt(self.eigenvalues[i])/(2.0*3.14159))

		self.X = self.eigenvectors.copy()
		for DOF in range(self.mesh.nDOFs):
			if DOF not in self.fixedDOFs:
				pass
			else:
				self.eigenvectors = np.insert(self.eigenvectors,DOF,0.,axis=0)


	def assembleLoadVector(self):
		'''
	Assemble the load vector from loads defined in
	the input file.
	
	self.F		- Load vector assembled from input
				  directly from *.sol-file.
	self.t		- The time steps for the load as
				  listed in *.tab-file.
	self.n		- Number of time steps.
	self.dt 	- Size of one time step.
	self.time	- Total time of self.t.
	self.forces - Loads as a function of time (self.t).
	self.accel  - Base acceleration as a function
				  of time (self.t).
	'''
		self.F = np.zeros((self.mesh.nDOFs+len(self.MPCs),1))
		for j in self.loads:
			if self.loads[j].type in ['Acceleration', 'ForceDynamic']:
				self.loads[j].calcDegreeOfFreedomForces(self.mesh.nDOFs,self.mesh.NFMT)
			else:
				print('\n\tUNKNOWN LOAD TYPE FOR MODAL DYNAMCS:', self.loads[j].type)
			for k in range(self.mesh.nDOFs):
				self.F[k] += self.loads[j].F[k]

			if self.loads[j].table.time[0] == 0.:
				time = self.loads[j].table.time[-1]
				n = len(self.loads[j].table.time)
				dt = time/n
				if self.hasBaseMotion:
					self.accel = self.loads[j].table.accel
				else:
					self.force = self.loads[j].table.force
				if hasattr(self,'time'):
					print('\n\tERROR!!!')
					print('\tCan only use one force/acceleration table in one analysis.')
					self.loadError = True
				else:
					self.t = self.loads[j].table.time
					self.time = time
					self.n = n
					self.dt = dt
			else:
				print('\n\tERROR!!!')
				print('\n\tAcceleration/Force input table must start at time t = 0.')


	def newmarkCoefficients(self,dt):
		'''
	Calculates the Newmark coefficients used
	for iteration when calculating the displacements.
	'''
		alpha=0.25
		beta=0.5

		a0=1/(alpha*(dt**2))
		a1=beta/(alpha*dt)
		a2=1/(alpha*dt)
		a3=(1/(2*alpha))-1
		a4=(beta/alpha)-1
		a5=(dt/2)*((beta/alpha)-2)
		a6=dt*(1-beta)
		a7=beta*dt

		return [a0,a1,a2,a3,a4,a5,a6,a7]


	def calcDisplacements(self):
		'''
	Calculates displacements of only selected
	nodes specified in *.sol-file, using modal
	dynamics.

	self.K_11		- Stiffness matrix of model
					  modified to exclude DOFs
					  listed in self.fixedDOFs.
	self.M_11		- Mass matrix of model
					  modified to exclude DOFs
					  listed in self.fixedDOFs.
	self.fixedDOFs	- List of fixed DOFs.
	self.mesh.nDOFs	- Total number of DOFs.
	self.F			- Load vector
	F_1				- Load vector of known external
					  forces applied.
	self.nModes 	- Number of eigenmodes
	self.X		 	- Eigenvectors excluding DOFs
					  listed in self.fixedDOFs.

	init_disp		- Initial displacements (set to zero)
	init_velc		- Initial velocities (also set to zero)
	q0				- Initial displacements in modal coordinates
	dq_dt0			- Initial velocities in modal coordinates
	Q				- Load vector in modal coordinates

	'''
		L = self.mesh.nDOFs+len(self.MPCs)
		M = self.mesh.nDOFs+len(self.MPCs)-len(self.fixedDOFs)
		N = len(self.fixedDOFs)
		self.nModes = len(self.X[0])
		evecs_s = sp.csc_matrix(self.X)
		self.omega = np.sqrt(self.eigenvalues)

		# declare variables
		F_1 = 0
		q0 = 0
		dq_dt0 = 0
		Q = 0

		# set Newmark coefficients
		[a0,a1,a2,a3,a4,a5,a6,a7] = self.newmarkCoefficients(self.dt)

		# set damping ratio
		for damp in self.dampings:
			if len(self.dampings) > 1:
				print('\n\tWARNING!!!\n\tMore than one damping specified for solution.')
				print('\tWill use damping:', self.dampings[damp].name)
			self.dampRatio = []
			if self.dampings[damp].type == 'Viscous':
				self.dampRatio = [self.dampings[damp].dampRatio for i in range(self.nModes)]
			else:
				for mode in range(self.nModes):
					for freq in range(len(self.dampings[damp].table.frequency)):
						if self.eigenfrequencies[mode] < self.dampings[damp].table.frequency[freq]:
							self.dampRatio.append(self.dampings[damp].table.dampRatio[freq-1])
							break
						if freq == len(self.dampings[damp].table.frequency)-1:
							self.dampRatio.append(self.dampings[damp].table.dampRatio[freq])
			break


		if self.hasBaseMotion:
			# modal dynamics with base acceleration
			A_2 = self.F[self.index11]
			enf_dofs = self.index11[M:]
			free_dofs = self.index11[:M]

			# given base acceleration, use integration
			# to find velocity and displacement at base
			enf_accl = {}
			enf_velc = {}
			enf_disp = {}
			for r in range(L):
				if A_2[r][0] != 0.:
					enf_accl[r] = A_2[r]*self.accel
					enf_dv = cumtrapz(enf_accl[r])
					enf_velc[r] = np.zeros(self.n)
					enf_velc[r][1:self.n] = enf_dv*self.dt
					enf_du = cumtrapz(enf_velc[r])
					enf_disp[r] = np.zeros(self.n)
					enf_disp[r][1:self.n] = enf_du*self.dt
					
			# set up base acceleration, velocity and
			# displacement vectors as sparse matrices
			# because of all the zeros
			a_row = []
			a_col = []
			a_data = []
			v_row = []
			v_col = []
			v_data = []
			d_row = []
			d_col = []
			d_data = []
			for r in range(L):
				if A_2[r][0] != 0.:
					for c in range(self.n):
						a_row.append(enf_dofs.index(self.index11[r]))
						a_col.append(c)
						a_data.append(enf_accl[r][c])
						v_row.append(enf_dofs.index(self.index11[r]))
						v_col.append(c)
						v_data.append(enf_velc[r][c])
						d_row.append(enf_dofs.index(self.index11[r]))
						d_col.append(c)
						d_data.append(enf_disp[r][c])
			enf_accl = sp.coo_matrix((np.array(a_data),(np.array(a_col),np.array(a_row))),shape=(self.n,N))
			enf_accl = enf_accl.tocsc()
			enf_velc = sp.coo_matrix((np.array(v_data),(np.array(v_col),np.array(v_row))),shape=(self.n,N))
			enf_velc = enf_velc.tocsc()
			enf_disp = sp.coo_matrix((np.array(d_data),(np.array(d_col),np.array(d_row))),shape=(self.n,N))
			enf_disp = enf_disp.tocsc()
	
			K_Q = evecs_s.T.dot(self.k_ww.dot(evecs_s))
			K_Q = K_Q.tocsc()
			M_Q = evecs_s.T.dot(self.m_ww.dot(evecs_s))
			M_Q = M_Q.tocsc()
			C_Q = np.zeros(self.nModes)
			for i in range(self.nModes):
				C_Q[i] = 2*self.dampRatio[i]*self.omega[i]
			C_Q = sp.diags(C_Q,0)
			C_Q = C_Q.tocsc()

			# variables in which to save
			# the requested results
			self.displacement = {}
			self.velocity = {}
			self.acceleration = {}
			self.frf_accel = {}

			# specify res_dofs
			res_dofs = {'displacement': [], 'velocity': [], 'acceleration': []}
			for result in self.results:
				if result in ['displacement', 'velocity', 'acceleration', 'frf_accel']:
					node_DOFs = ['X', 'Y', 'Z', 'RX', 'RY', 'RZ']
					if 'plot' in self.results[result]:
						for node in self.nodesets[self.results[result]['plot']]:
							if result == 'displacement':
								self.displacement[node] = {}
							if result == 'velocity':
								self.velocity[node] = {}
							if result == 'acceleration':
								self.acceleration[node] = {}
							if result == 'frf_accel':
								self.frf_accel[node] = {}
							only_one_dof = False
							if 'result DOF' in self.results[result]:
								if self.mesh.NFAT[node][self.results[result]['result DOF']-1] == 1:
									only_one_dof = True
								else:
									print('\n\tWARNING:\n\tSelected DOF for results at node', node, 'is not available')
									print('\tfor this type of element. Calculating results for all DOFs in node.')
							m = 0
							for nfs in range(6):
								if self.mesh.nodes[node].NFS[nfs] == 1:
									if only_one_dof:
										if self.results[result]['result DOF']-1 == nfs:
											res = result
											if result == 'displacement':
												self.displacement[node][node_DOFs[nfs]] = self.mesh.NFMT[node]+m
											elif result == 'velocity':
												self.velocity[node][node_DOFs[nfs]] = self.mesh.NFMT[node]+m
											elif result == 'acceleration':
												self.acceleration[node][node_DOFs[nfs]] = self.mesh.NFMT[node]+m
											elif result == 'frf_accel':
												self.frf_accel[node][node_DOFs[nfs]] = self.mesh.NFMT[node]+m
												res = 'acceleration'
											else:
												pass
											if self.mesh.NFMT[node]+m not in res_dofs[res]:
												res_dofs[res].append(self.mesh.NFMT[node]+m)
											break
									else:
										res = result
										if result == 'displacement':
											self.displacement[node][node_DOFs[nfs]] = self.mesh.NFMT[node]+m
										elif result == 'velocity':
											self.velocity[node][node_DOFs[nfs]] = self.mesh.NFMT[node]+m
										elif result == 'acceleration':
											self.acceleration[node][node_DOFs[nfs]] = self.mesh.NFMT[node]+m
										elif result == 'frf_accel':
											self.frf_accel[node][node_DOFs[nfs]] = self.mesh.NFMT[node]+m
											res = 'acceleration'
										else:
											pass
										if self.mesh.NFMT[node]+m not in res_dofs[res]:
											res_dofs[res].append(self.mesh.NFMT[node]+m)
									m += 1
					if 'text' in self.results[result]:
						for node in self.nodesets[self.results[result]['text']]:
							if result == 'displacement':
								self.displacement[node] = {}
							if result == 'velocity':
								self.velocity[node] = {}
							if result == 'acceleration':
								self.acceleration[node] = {}
							if result == 'frf_accel':
								self.frf_accel[node] = {}
							only_one_dof = False
							if 'result DOF' in self.results[result]:
								if self.mesh.NFAT[node][self.results[result]['result DOF']-1] == 1:
									only_one_dof = True
								else:
									print('\n\tWARNING:\n\tSelected DOF for results at node', node, 'is not available')
									print('\tfor this type of element. Calculating results for all DOFs in node.')
							m = 0
							for nfs in range(6):
								if self.mesh.nodes[node].NFS[nfs] == 1:
									if only_one_dof:
										if self.results[result]['result DOF']-1 == nfs:
											res = result
											if result == 'displacement':
												self.displacement[node][node_DOFs[nfs]] = self.mesh.NFMT[node]+m
											elif result == 'velocity':
												self.velocity[node][node_DOFs[nfs]] = self.mesh.NFMT[node]+m
											elif result == 'acceleration':
												self.acceleration[node][node_DOFs[nfs]] = self.mesh.NFMT[node]+m
											elif result == 'frf_accel':
												self.frf_accel[node][node_DOFs[nfs]] = self.mesh.NFMT[node]+m
												res = 'acceleration'
											else:
												pass
											if self.mesh.NFMT[node]+m not in res_dofs[res]:
												res_dofs[res].append(self.mesh.NFMT[node]+m)
											break
									else:
										res = result
										if result == 'displacement':
											self.displacement[node][node_DOFs[nfs]] = self.mesh.NFMT[node]+m
										elif result == 'velocity':
											self.velocity[node][node_DOFs[nfs]] = self.mesh.NFMT[node]+m
										elif result == 'acceleration':
											self.acceleration[node][node_DOFs[nfs]] = self.mesh.NFMT[node]+m
										elif result == 'frf_accel':
											self.frf_accel[node][node_DOFs[nfs]] = self.mesh.NFMT[node]+m
											res = 'acceleration'
										else:
											pass
										if self.mesh.NFMT[node]+m not in res_dofs[res]:
											res_dofs[res].append(self.mesh.NFMT[node]+m)
									m += 1

			disp = {}
			for dof in res_dofs['displacement']:
				disp[dof] = np.zeros((self.n,1))
			velc = {}
			for dof in res_dofs['velocity']:
				velc[dof] = np.zeros((self.n,1))
			accl = {}
			for dof in res_dofs['acceleration']:
				accl[dof] = np.zeros((self.n,1))

			q   = np.zeros((self.nModes,1))
			qd  = np.zeros((self.nModes,1))
			qdd = np.zeros((self.nModes,1))
			qn  = np.zeros((self.nModes,1))

			KH = K_Q+a0*M_Q+a1*C_Q

			inv_KH = sp.linalg.inv(KH)
			inv_KH_diag = np.zeros(self.nModes)
			for i in range(self.nModes):
				inv_KH_diag[i]=inv_KH[i,i]

			n_min1 = self.n-1
			for i in range(n_min1):

				FP = -evecs_s.T.dot(self.m_w2.dot(enf_accl[i,:].T))
				FH = M_Q.dot(a0*q+a2*qd+a3*qdd)+C_Q.dot(a1*q+a4*qd+a5*qdd)
				for dof in range(self.nModes):
					FH[dof] += FP[dof]

				for dof in range(self.nModes):
					qn[dof] = inv_KH_diag[dof]*FH[dof]

				qddn = a0*(qn-q)-a2*qd-a3*qdd
				qdn = qd+a6*qdd+a7*qddn

				for dof in range(self.nModes):
					q[dof]   = qn[dof]
					qd[dof]  = qdn[dof]
					qdd[dof] = qddn[dof]

				for dof in res_dofs['displacement']:
					disp[dof][i+1] = evecs_s[free_dofs.index(dof)].dot(q)
				for dof in res_dofs['velocity']:
					velc[dof][i+1] = evecs_s[free_dofs.index(dof)].dot(qd)
				for dof in res_dofs['acceleration']:
					accl[dof][i+1] = evecs_s[free_dofs.index(dof)].dot(qdd)

			# set up acceleration, velocity and
			# displacement vectors for all dofs as
			# sparse matrices because of all the zeros
			# needed to transform back using self.TT
			# here in the form of self.T1 and self.T2
			a_row = []
			a_col = []
			a_data = []
			v_row = []
			v_col = []
			v_data = []
			d_row = []
			d_col = []
			d_data = []
			for r in range(M):
				if free_dofs[r] in disp:
					for c in range(self.n):
						d_row.append(r)
						d_col.append(c)
						d_data.append(disp[free_dofs[r]][c][0])
				if free_dofs[r] in velc:
					for c in range(self.n):
						v_row.append(r)
						v_col.append(c)
						v_data.append(velc[free_dofs[r]][c][0])
				if free_dofs[r] in accl:
					for c in range(self.n):
						a_row.append(r)
						a_col.append(c)
						a_data.append(accl[free_dofs[r]][c][0])
			disp = sp.coo_matrix((np.array(d_data),(np.array(d_col),np.array(d_row))),shape=(self.n,M))
			disp = disp.tocsc()
			velc = sp.coo_matrix((np.array(v_data),(np.array(v_col),np.array(v_row))),shape=(self.n,M))
			velc = velc.tocsc()
			accl = sp.coo_matrix((np.array(a_data),(np.array(a_col),np.array(a_row))),shape=(self.n,M))
			accl = accl.tocsc()

			dT = self.T1.dot(enf_disp.T) + self.T2.dot(disp.T)
			vT = self.T1.dot(enf_velc.T) + self.T2.dot(velc.T)
			aT = self.T1.dot(enf_accl.T) + self.T2.dot(accl.T)

			ZdT = sp.hstack([dT.T,enf_disp])
			ZdT = ZdT.tocsc()
			ZvT = sp.hstack([vT.T,enf_velc])
			ZvT = ZvT.tocsc()
			ZaT = sp.hstack([aT.T,enf_accl])
			ZaT = ZaT.tocsc()

			# save requested results to
			# solution to be written in
			# *.out-file
			self.base_disp = {}
			self.base_accel = {}
			node_DOFs = ['X', 'Y', 'Z', 'RX', 'RY', 'RZ']
			for bound in self.boundaries:
				for node in self.boundaries[bound].nodeset:
					m = 0
					for nfs in range(6):
						if self.mesh.nodes[node].NFS[nfs] == 1:
							self.base_disp[node_DOFs[nfs]] = ZdT[:,self.index11[M+m]].toarray()
							self.base_accel[node_DOFs[nfs]] = ZaT[:,self.index11[M+m]].toarray()
							m += 1
					break
				break
			for node in self.displacement:
				for dof in self.displacement[node]:
					if dof in self.base_disp:
						self.displacement[node][dof] = ZdT[:,self.index11.index(self.displacement[node][dof])].toarray()-self.base_disp[dof]
					else:
						self.displacement[node][dof] = ZdT[:,self.index11.index(self.displacement[node][dof])].toarray()
			for node in self.velocity:
				for dof in self.velocity[node]:
					self.velocity[node][dof] = ZvT[:,self.index11.index(self.velocity[node][dof])].toarray()
			for node in self.acceleration:
				for dof in self.acceleration[node]:
					self.acceleration[node][dof] = ZaT[:,self.index11.index(self.acceleration[node][dof])].toarray()
			# include base motion acceleration in results
			self.acceleration[0] = {}
			for dof in self.base_accel:
				self.acceleration[0][dof] = self.base_accel[dof]
			for node in self.frf_accel:
				for dof in self.frf_accel[node]:
					self.frf_accel[node][dof] = {'MAGN': fwdFFT(ZaT[:,self.index11.index(self.frf_accel[node][dof])].toarray())[3]}
					if not hasattr(self,'freq'):
						self.freq = (1./self.dt)/2.
						self.df = self.freq/len(self.frf_accel[node][dof]['MAGN'])
						self.f = np.arange(0., self.freq, self.df)


		else:
			# modal dynamics with dynamic load
			# applied somewhere other than base
			F_1 = self.F[self.index11[:M]]
			row = []
			col = []
			data = []
			for r in range(M):
				for c in range(self.n):
					if F_1[r][0] != 0.:
						row.append(r)
						col.append(c)
						data.append(F_1[r][0]*self.force[c])
			F_1 = sp.coo_matrix((np.array(data),(np.array(row),np.array(col))),shape=(M,self.n))
			F_1 = F_1.tocsc()

			init_disp = np.zeros((self.mesh.nDOFs-len(self.fixedDOFs)+len(self.MPCs),1))
			init_velc = np.zeros((self.mesh.nDOFs-len(self.fixedDOFs)+len(self.MPCs),1))

			q0 = evecs_s.T.dot(self.M_11).dot(init_disp)
			dq_dt0 = evecs_s.T.dot(self.M_11).dot(init_velc)
			Q = evecs_s.T.dot(F_1)

			ksi = []
			d = []
			KH = []
			FH = []
			for i in range(self.nModes):
				ksi.append(self.dampRatio[i])
				d.append(2.*ksi[i]*self.omega[i])
				KH.append(self.omega[i]**2 + a0 + a1*2.*ksi[i]*self.omega[i])
				FH.append(0.)

			q = []
			dq_dt = []
			d2q_dt2 = []
			if self.hasBaseMotion:
				for i in range(self.nModes):
					q.append([])
					q[i].append(0.)
					dq_dt.append([])
					dq_dt[i].append(0.)
					d2q_dt2.append([])
					d2q_dt2[i].append(0.)
			else:
				for i in range(self.nModes):
					q.append([])
					q[i].append(q0[i][0])
					dq_dt.append([])
					dq_dt[i].append(dq_dt0[i][0])
					d2q_dt2.append([])
					d2q_dt2[i].append(0.)

			for j in range(1,self.n):
				for i in range(self.nModes):
					V1 = a1*q[i][j-1] + a4*dq_dt[i][j-1] + a5*d2q_dt2[i][j-1]
					V2 = a0*q[i][j-1] + a2*dq_dt[i][j-1] + a3*d2q_dt2[i][j-1]

					CV = d[i]*V1
					FH[i] = Q[i,j] + V2 + CV

					q[i].append(FH[i]/KH[i])
					d2q_dt2[i].append(a0*(q[i][j]-q[i][j-1])-a2*dq_dt[i][j-1]-a3*d2q_dt2[i][j-1])
					dq_dt[i].append(dq_dt[i][j-1]+a6*d2q_dt2[i][j-1]+a7*d2q_dt2[i][j])


			# save the requested results
			self.displacement = {}
			self.velocity = {}
			self.acceleration = {}
			self.frf_accel = {}
			for result in self.results:
				if result in ['displacement', 'velocity', 'acceleration', 'frf_accel']:
					node_DOFs = ['X', 'Y', 'Z', 'RX', 'RY', 'RZ']
					if 'plot' in self.results[result]:
						for node in self.nodesets[self.results[result]['plot']]:
							if result == 'displacement':
								self.displacement[node] = {}
							elif result == 'velocity':
								self.velocity[node] = {}
							elif result == 'acceleration':
								self.acceleration[node] = {}
							elif result == 'frf_accel':
								self.frf_accel[node] = {}
							else:
								print('\n\tERROR:\n\tType of result not supported:', result)
							only_one_dof = False
							if 'result DOF' in self.results[result]:
								if self.mesh.NFAT[node][self.results[result]['result DOF']-1] == 1:
									only_one_dof = True
								else:
									print('\n\tWARNING:\n\tSelected DOF for results at node', node, 'is not available')
									print('\tfor this type of element. Calculating results for all DOFs in node.')
							m = 0
							for nfs in range(6):
								if self.mesh.nodes[node].NFS[nfs] == 1:
									if self.mesh.NFMT[node]+m in self.fixedDOFs:
										print('\n\tWARNING:\n\tCannot calculate displacements on dof', node_DOFs[m], 'for node', node, 'beacause it')
										print('\thas been set to a fixed displacement boundary condition.')
									if only_one_dof:
										if self.results[result]['result DOF']-1 == nfs:
											if result == 'displacement':
												self.displacement[node][node_DOFs[nfs]] = self.eigenvectors[self.mesh.NFMT[node]+m].dot(q)
											elif result == 'velocity':
												self.velocity[node][node_DOFs[nfs]] = self.eigenvectors[self.mesh.NFMT[node]+m].dot(dq_dt)
											elif result == 'acceleration':
												self.acceleration[node][node_DOFs[nfs]] = self.eigenvectors[self.mesh.NFMT[node]+m].dot(d2q_dt2)
											elif result == 'frf_accel':
												if node_DOFs[nfs] not in self.acceleration[node]:
													self.acceleration[node][node_DOFs[nfs]] = self.eigenvectors[self.mesh.NFMT[node]+m].dot(d2q_dt2)
												[X, REAL, IMAG, MAGN, PHASE] = fwdFFT(self.acceleration[node][node_DOFs[nfs]])
												self.frf_accel[node][node_DOFs[nfs]] = {'MAGN': MAGN}
												if not hasattr(self,'freq'):
													self.freq = (1./self.dt)/2.
													self.df = self.freq/len(self.frf_accel[node][node_DOFs[nfs]]['MAGN'])
													self.f = np.arange(0., self.freq, self.df)
											else:
												print('\n\tERROR:\n\tType of result not supported:', result)
											break
									else:
										if result == 'displacement':
											self.displacement[node][node_DOFs[nfs]] = self.eigenvectors[self.mesh.NFMT[node]+m].dot(q)
										elif result == 'velocity':
											self.velocity[node][node_DOFs[nfs]] = self.eigenvectors[self.mesh.NFMT[node]+m].dot(dq_dt)
										elif result == 'acceleration':
											self.acceleration[node][node_DOFs[nfs]] = self.eigenvectors[self.mesh.NFMT[node]+m].dot(d2q_dt2)
										elif result == 'frf_accel':
											if node_DOFs[nfs] not in self.acceleration[node]:
												self.acceleration[node][node_DOFs[nfs]] = self.eigenvectors[self.mesh.NFMT[node]+m].dot(d2q_dt2)
											[X, REAL, IMAG, MAGN, PHASE] = fwdFFT(self.acceleration[node][node_DOFs[nfs]])
											self.frf_accel[node][node_DOFs[nfs]] = {'MAGN': MAGN, 'PHASE': PHASE}
											if not hasattr(self,'freq'):
												self.freq = (1./self.dt)/2.
												self.df = self.freq/len(self.frf_accel[node][node_DOFs[nfs]]['MAGN'])
												self.f = np.arange(0., self.freq, self.df)
										else:
											print('\n\tERROR:\n\tType of result not supported:', result)
									m += 1

					if 'text' in self.results[result]:
						pass
				else:
					pass

		# delete some matrices so the *.out-file
		# doesn't become unneccesarily big
		if hasattr(self,'T1'):
			del self.T1
		if hasattr(self,'T2'):
			del self.T2
		if hasattr(self,'m_ww'):
			del self.m_ww
		if hasattr(self,'m_w2'):
			del self.m_w2
		if hasattr(self,'k_ww'):
			del self.k_ww


	def exportToCSV(self,filename):
		'''
	Writes requested results to *.csv-file.
	'''
		# write results to *.csv file if
		# user requested results in text
		text_nodes = []
		text_result = []
		has_time = False
		has_frf = False
		for result in self.results:
			if result in ['displacement', 'velocity', 'acceleration', 'frf_accel']:
				if 'text' in self.results[result]:
					text_result.append(result)
					for node in self.nodesets[self.results[result]['text']]:
						text_nodes.append(node)

		if len(text_nodes) != 0:
			write_to_csv = {}
			for node in self.displacement:
				if node in text_nodes and 'displacement' in text_result:
					if has_time == False:
						has_time = True
					if 'displacement' not in write_to_csv:
						write_to_csv['displacement'] = {}
					if node not in write_to_csv['displacement']:
						write_to_csv['displacement'][node] = {}
					for dof in self.displacement[node]:
						write_to_csv['displacement'][node][dof] = self.displacement[node][dof]
			for node in self.velocity:
				if node in text_nodes and 'velocity' in text_result:
					if has_time == False:
						has_time = True
					if 'velocity' not in write_to_csv:
						write_to_csv['velocity'] = {}
					if node not in write_to_csv['velocity']:
						write_to_csv['velocity'][node] = {}
					for dof in self.velocity[node]:
						write_to_csv['velocity'][node][dof] = self.velocity[node][dof]
			for node in self.acceleration:
				if node in text_nodes and 'acceleration' in text_result:
					if has_time == False:
						has_time = True
					if 'acceleration' not in write_to_csv:
						write_to_csv['acceleration'] = {}
					if node not in write_to_csv['acceleration']:
						write_to_csv['acceleration'][node] = {}
					for dof in self.acceleration[node]:
						write_to_csv['acceleration'][node][dof] = self.acceleration[node][dof]
				if 0 in self.acceleration:
					write_to_csv['acceleration'][0] = {}
					for dof in self.acceleration[0]:
						write_to_csv['acceleration'][0][dof] = self.acceleration[0][dof]
			for node in self.frf_accel:
				if node in text_nodes and 'frf_accel' in text_result:
					if has_frf == False:
						has_frf = True
					if 'frf_accel' not in write_to_csv:
						write_to_csv['frf_accel'] = {}
					if node not in write_to_csv['frf_accel']:
						write_to_csv['frf_accel'][node] = {}
					for dof in self.frf_accel[node]:
						write_to_csv['frf_accel'][node][dof] = self.frf_accel[node][dof]

			if os.path.exists(filename+'.csv'):
				print('\n\tOverwriting '+filename+'.csv')
			fobj = open(filename+'.csv', 'w')
			if has_time:
				fobj.write('time')
			if has_frf:
				if has_time:
					fobj.write(',freq')
				else:
					fobj.write('freq')
			for res in write_to_csv:
				if res in text_result:
					for node in write_to_csv[res]:
						if node in text_nodes or node == 0:
							for dof in write_to_csv[res][node]:
								fobj.write(','+res+'_node_'+str(node)+'_'+dof)
			fobj.write('\n')
			n_f = 0
			if hasattr(self,'f'):
				n_f = len(self.f)
			for n in range(self.n):
				if has_time:
						fobj.write(str(self.t[n]))
				if has_frf:
					if has_time:
						if n < n_f:
							fobj.write(','+str(self.f[n]))
						else:
							fobj.write(',---')
					else:
						if n < n_f:
							fobj.write(str(self.f[n]))
						else:
							fobj.write('---')
				for res in write_to_csv:
					for node in write_to_csv[res]:
						for dof in write_to_csv[res][node]:
							if res in ['displacement', 'velocity', 'acceleration']:
								if self.hasBaseMotion:
									fobj.write(','+str(write_to_csv[res][node][dof][n][0]))
								else:
									fobj.write(','+str(write_to_csv[res][node][dof][n]))
							else:
								if n < n_f:
									fobj.write(','+str(write_to_csv[res][node][dof]['MAGN'][n]))
								else:
									fobj.write(',---')
				fobj.write('\n')
			fobj.close()






