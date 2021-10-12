#! /usr/bin/env python3
#
#
#	solFEM.py
#  -----------
#
#	This is the solFEM module. It generates a FEModel object, by reading
# 	data from the InputFile object. It also has the functions necessary
# 	to build stiffness matrices, mass matrices and load vectors. After
# 	building the FEModel object, the requested solution is calculated
# 	using the solution objects.
#

import os
import pickle
import numpy as np
import scipy.sparse as sp
import sys

sys.path.insert(1, '../Objects')

from timeit import time
from reader import *

from nodes import *
from materials import *
from sections import *
from elements import *
from meshes import *
from loads import *
from boundaries import *
from constraints import *
from dampings import *
from tables import *
from solutions import *






class FEModel(object):
	'''
Base class for finite element model. It first instantiates
all nodes, materials, sections, elements, meshes, loads,
boundaries and solutions listed in the InputData object.
It also checks what elements will be used in what solution.
If two solutions use all the same elements, they can use
the same global stiffness matrix as a base to modify with
their individual boundary conditions, loads and constraints.
'''
	def __init__(self,inputobj):

		self.name = inputobj.name
		self.gaussQuad = GaussQuad()

		self.nodesets = {}
		self.elementsets = {}
		self.nodes = {}
		self.materials = {}
		self.sections = {}
		self.elements = {}
		self.meshes = {}
		self.loads = {}
		self.boundaries = {}
		self.constraints = {}
		self.dampings = {}
		self.tables = {}
		self.solutions = {}

		# set up all node sets listed in *.sol-file ready to be used
		for key in inputobj.nodesets:
			self.nodesets[key] = []
			for i in range(len(inputobj.nodesets[key])):
				if isinstance(inputobj.nodesets[key][i],int):
					self.nodesets[key].append(inputobj.nodesets[key][i])
				else:
					for j in range(inputobj.nodesets[key][i][1]-inputobj.nodesets[key][i][0]+1):
						self.nodesets[key].append(inputobj.nodesets[key][i][0]+j)

		# set up all element sets listed in *.sol-file ready to be used
		for key in inputobj.elementsets:
			self.elementsets[key] = []
			for i in range(len(inputobj.elementsets[key])):
				if isinstance(inputobj.elementsets[key][i],int):
					self.elementsets[key].append(inputobj.elementsets[key][i])
				else:
					for j in range(inputobj.elementsets[key][i][1]-inputobj.elementsets[key][i][0]+1):
						self.elementsets[key].append(inputobj.elementsets[key][i][0]+j)
		
		# instantiate all Node objects listed in *.sol-file
		for key in inputobj.nodes:
			self.nodes[key] = Node(key,*inputobj.nodes[key]['coord'])

		# instantiate all Material objects listed in *.sol-file
		for key in inputobj.materials:
			properties = []
			if inputobj.materials[key]['type'] == 'Isotropic':
				if 'E-modulus' in inputobj.materials[key]['properties']:
					properties.append(inputobj.materials[key]['properties']['E-modulus'])
				if 'poisson ratio' in inputobj.materials[key]['properties']:
					properties.append(inputobj.materials[key]['properties']['poisson ratio'])
				if 'density' in inputobj.materials[key]['properties']:
					properties.append(inputobj.materials[key]['properties']['density'])
				if 'thermal expansion coefficient' in inputobj.materials[key]['properties']:
					properties.append(inputobj.materials[key]['properties']['thermal expansion coefficient'])
				if 'conductivity' in inputobj.materials[key]['properties']:
					properties.append(inputobj.materials[key]['properties']['conductivity'])
				if 'specific heat' in inputobj.materials[key]['properties']:
					properties.append(inputobj.materials[key]['properties']['specific heat'])
			self.materials[key] = globals()[inputobj.materials[key]['type']](key, *properties)

		# instantiate all Section objects listed in *.sol-file
		for key in inputobj.sections:
			properties = []
			if inputobj.sections[key]['type'] == 'RodSect':
				if 'area' in inputobj.sections[key]['properties']:
					properties.append(inputobj.sections[key]['properties']['area'])
				else:
					pass
			elif inputobj.sections[key]['type'] == 'BeamSect':
				if 'area' in inputobj.sections[key]['properties']:
					properties.append(inputobj.sections[key]['properties']['area'])
				if 'Izz' in inputobj.sections[key]['properties']:
					properties.append(inputobj.sections[key]['properties']['Izz'])
				if 'Iyy' in inputobj.sections[key]['properties']:
					properties.append(inputobj.sections[key]['properties']['Iyy'])
			elif inputobj.sections[key]['type'] in ['PlaneSect', 'PlateSect']:
				if 'thickness' in inputobj.sections[key]['properties']:
					properties.append(inputobj.sections[key]['properties']['thickness'])
			else:
				pass
			self.sections[key] = globals()[inputobj.sections[key]['type']](key, \
						self.materials[inputobj.sections[key]['material']], *properties)

		# instantiate all Element objects listed in *.sol-file
		for key in inputobj.elements:
			for node in range(len(inputobj.elements[key]['nodes'])):
				inputobj.elements[key]['nodes'][node] = \
					self.nodes[inputobj.elements[key]['nodes'][node]]
		for key in inputobj.elements:
			if inputobj.elements[key]['type'] in ['TRI6N', 'QUAD4N', 'QUAD8N', \
												  'TET10N', 'HEX8N', 'HEX20N']:
				self.elements[key] = globals()[inputobj.elements[key]['type']](key, \
										self.sections[inputobj.elements[key]['section']], \
										inputobj.elements[key]['nodes'], self.gaussQuad)
			else:
				self.elements[key] = globals()[inputobj.elements[key]['type']](key, \
										self.sections[inputobj.elements[key]['section']], \
										inputobj.elements[key]['nodes'])

		# apply beam orientation to any Element given a specified beam orientation
		for key in inputobj.beamOrients:
			for element in self.elements:
				if self.elements[element].number in self.elementsets[inputobj.beamOrients[key]['elementset']]:
					if self.elements[element].type == inputobj.beamOrients[key]['type'] == 'BEAM2N2D':
						self.elements[element].setOrientation({'x-vec': inputobj.beamOrients[key]['x-vec']})
					if self.elements[element].type == inputobj.beamOrients[key]['type'] == 'BEAM2N':
						self.elements[element].setOrientation({'x-vec': inputobj.beamOrients[key]['x-vec'],
															   'y-vec': inputobj.beamOrients[key]['y-vec']})
		for element in self.elements:
			if not hasattr(self.elements[element],'T_elm') and self.elements[element].type in ['BEAM2N2D', 'BEAM2N']:
				self.elements[element].setOrientation()

		# create an element set 0 which includes all Element objects listed in *.sol-file
		# to be used as default mesh if mesh is not specified for a given solution
		self.elementsets[0] = []
		for key in self.elements:
			self.elementsets[0].append(key)

		# instantiate all Mesh objects listed in *.sol-file
		self.meshes[0] = 1
		for key in inputobj.meshes:
			if inputobj.meshes[key] == 'all':
				if self.meshes[0] == 1:
					self.meshes[0] = Mesh(self.nodes,self.elements)
					self.meshes[0].solutions.append(key)
				else:
					self.meshes[0].solutions.append(key)
			else:
				elmsets = []
				for i in range(len(inputobj.meshes[key])):
					for j in range(len(self.elementsets[inputobj.meshes[key][i]])):
						if self.elementsets[inputobj.meshes[key][i]][j] in elmsets:
							pass
						else:
							elmsets.append(self.elementsets[inputobj.meshes[key][i]][j])
				elmsets.sort()
				if elmsets == self.elementsets[0]:
					if self.meshes[0] == 1:
						self.meshes[0] = Mesh(self.nodes,self.elements)
						self.meshes[0].solutions.append(key)
					else:
						self.meshes[0].solutions.append(key)
				else:
					exists = False
					for mesh in self.meshes:
						if self.meshes[mesh] == 1:
							pass
						else:
							tmplist = list(self.meshes[mesh].elements.keys())
							tmplist.sort()
							if tmplist == elmsets:
								exists = True
								self.meshes[mesh].solutions.append(key)
					if exists == False:
						tmpelms = {}
						for j in range(len(elmsets)):
							tmpelms[elmsets[j]] = self.elements[elmsets[j]]
						tmpnodes = {}
						for j in tmpelms:
							for k in range(len(tmpelms[j].nodes)):
								if tmpelms[j].nodes[k] in tmpnodes:
									pass
								else:
									tmpnodes[tmpelms[j].nodes[k].number] = tmpelms[j].nodes[k]
						self.meshes[len(self.meshes)] = Mesh(tmpnodes,tmpelms)
						self.meshes[len(self.meshes)-1].solutions.append(key)

		# check if mesh is 2D or 3D
		for mesh in self.meshes:
			self.meshes[mesh].is3D = True
			for element in self.meshes[mesh].elements:
				if self.meshes[mesh].elements[element].type in ['ROD2N2D', 'BEAM2N2D', 'TRI3N',
																'TRI6N', 'QUAD4N', 'QUAD8N']:
					self.meshes[mesh].is3D = False
					break
				else:
					break

		# check for loose nodes that have not been set with a NFS, and then give them
		# NFS = [1,1,0,0,0,1] if 2D, and NFS = [1,1,1,1,1,1] if 3D.
		element_nodes = []
		for mesh in self.meshes:
			for element in self.meshes[mesh].elements:
				for node in self.meshes[mesh].elements[element].nodes:
					if node.number not in element_nodes:
						element_nodes.append(node.number)
		for mesh in self.meshes:
			for node in self.meshes[mesh].nodes:
				if node not in element_nodes:
					if self.meshes[mesh].is3D:
						self.meshes[mesh].nodes[node].NFS = [1,1,1,1,1,1]
					else:
						self.meshes[mesh].nodes[node].NFS = [1,1,0,0,0,1]

		# instantiate all Load objects listed in *.sol-file
		for key in inputobj.loads:
			if inputobj.loads[key]['type'] in ['Force', 'ForceConcentrated', 'ForceDynamic', 'Acceleration']:
				self.loads[key] = globals()[inputobj.loads[key]['type']](key, \
							self.nodesets[inputobj.loads[key]['nodeset']], inputobj.loads[key]['force'], \
							*inputobj.loads[key]['vector'])
			elif inputobj.loads[key]['type'] == 'Gravity':
				self.loads[key] = globals()[inputobj.loads[key]['type']](key, \
							self.elementsets[inputobj.loads[key]['elementset']], inputobj.loads[key]['acceleration'], \
							*inputobj.loads[key]['vector'])
			elif inputobj.loads[key]['type'] == 'Torque':
				self.loads[key] = globals()[inputobj.loads[key]['type']](key, \
							self.nodesets[inputobj.loads[key]['nodeset']], inputobj.loads[key]['torque'], \
							*inputobj.loads[key]['vector'])
			elif inputobj.loads[key]['type'] == 'Pressure':
				self.loads[key] = globals()[inputobj.loads[key]['type']](key, \
							self.nodesets[inputobj.loads[key]['nodeset']], inputobj.loads[key]['pressure'], \
							*inputobj.loads[key]['vector'])
			else:
				pass

		# instantiate all Boundary objects listed in *.sol-file
		for key in inputobj.boundaries:
			inputobj.boundaries[key]['nodeset']
			self.boundaries[key] = globals()[inputobj.boundaries[key]['type']](key, \
						self.nodesets[inputobj.boundaries[key]['nodeset']], inputobj.boundaries[key]['value'], \
						inputobj.boundaries[key]['DOFs'])

		# instantiate all Constraint objects listed in *.sol-file
		for key in inputobj.constraints:
			if inputobj.constraints[key]['type'] == 'TouchLock':
				self.constraints[key] = globals()[inputobj.constraints[key]['type']](key, \
							self.nodesets[inputobj.constraints[key]['nodeset1']], \
							self.nodesets[inputobj.constraints[key]['nodeset2']], \
							inputobj.constraints[key]['DOFs'], \
							inputobj.constraints[key]['tolerance'])
			else:
				self.constraints[key] = globals()[inputobj.constraints[key]['type']](key, \
							self.nodesets[inputobj.constraints[key]['nodeset1']], \
							self.nodesets[inputobj.constraints[key]['nodeset2']], \
							inputobj.constraints[key]['DOFs'])

		# instantiate all Damping objects listed in *.sol-file
		for key in inputobj.dampings:
			self.dampings[key] = globals()[inputobj.dampings[key]['type']](key, \
						inputobj.dampings[key]['damping_ratio'])


		# instantiate all Table objects listed in *.sol-file
		# and assign each table to boundary, load, material or damping
		for key in inputobj.tables:
			if inputobj.tables[key]['type'] == 'AccelTable':
				target = inputobj.tables[key]['boundary']
			elif inputobj.tables[key]['type'] == 'ForceTable':
				target = inputobj.tables[key]['load']
			elif inputobj.tables[key]['type'] == 'StressStrainTable':
				target = inputobj.tables[key]['material']
			elif inputobj.tables[key]['type'] == 'DampingTable':
				target = inputobj.tables[key]['damping']
			else:
				pass
			self.tables[key] = globals()[inputobj.tables[key]['type']](key, \
						inputobj.tables[key]['filename'], target)
			if inputobj.tables[key]['type'] == 'AccelTable':
				self.loads[target].table = self.tables[key]
			elif inputobj.tables[key]['type'] == 'ForceTable':
				self.loads[target].table = self.tables[key]
			elif inputobj.tables[key]['type'] == 'StressStrainTable':
				self.materials[target].table = self.tables[key]
			elif inputobj.tables[key]['type'] == 'DampingTable':
				self.dampings[target].table = self.tables[key]
			else:
				pass
			

		# assemble stiffness and mass matrices so they are ready
		# for the solutions that need them
		print('\n\n\n    |------^------^------^------^------^------^------|')
		print('\t\tFEModel:', self.name)
		print('    |------^------^------^------^------^------^------|\n')
		print('\t', len(inputobj.solutions), 'solution(s)\n')

		if os.path.exists(self.name+'.res'):
			print('\tOverwriting solution file '+self.name+'.res\n')
		fobj = open(self.name+'.res', 'w')
		fobj.write('\n\n    |------^------^------^------^------^------^------|\n')
		fobj.write('\t\t\tFEMODEL: '+self.name+'\n')
		fobj.write('    |------^------^------^------^------^------^------|\n\n')
		fobj.close()

		for mesh in self.meshes:
			print('\tAssembling stiffness matrix for solution(s):\n\n')
			for solution in range(len(self.meshes[mesh].solutions)):
				print('\t> '+self.meshes[mesh].solutions[solution])
			fobj = open(self.name+'.res', 'a')
			fobj.write('\t\tStiffness matrix for solution(s):\n\n\t\t')
			for solution in range(len(self.meshes[mesh].solutions)):
				fobj.write('\t> '+str(self.meshes[mesh].solutions[solution])+'\n\t\t')
			fobj.write('\n')
			assm_time_start = time.time()
			[self.meshes[mesh].NFAT, self.meshes[mesh].NFMT, self.meshes[mesh].nDOFs] = \
											self.nodeFreedomMapTable(self.meshes[mesh].nodes)
			self.meshes[mesh].K = []
			self.assembleStiffnessMatrix(self.meshes[mesh])
			self.meshes[mesh].needMassMatrix = False
			for solution in self.meshes[mesh].solutions:
				if inputobj.solutions[solution]['type'] in ['Eigenmodes', 'ModalDynamic']:
					self.meshes[mesh].needMassMatrix = True
				elif inputobj.solutions[solution]['type'] in ['Static', 'StaticPlastic']:
					for load in range(len(inputobj.solutions[solution]['loads'])):
						if inputobj.loads[inputobj.solutions[solution]['loads'][load]]['type'] == 'Gravity':
							self.meshes[mesh].needMassMatrix = True
				else:
					pass
			if self.meshes[mesh].needMassMatrix == True:
				self.assembleMassMatrix(self.meshes[mesh])
			assm_time_stop = time.time()
			self.assm_time = assm_time_stop - assm_time_start
			print('\n\tAssembly time: %.3f seconds\n' % (self.assm_time))
			print('\tModel has', len(self.meshes[mesh].nodes), 'nodes,', \
						len(self.meshes[mesh].elements), 'elements, and\n\t', \
						self.meshes[mesh].nDOFs, 'degrees of freedom\n')
			print('    |------^------^------^------^------^------^------|\n\n')
			fobj.write('\n\t\tAssembly time: %.3f seconds\n\n\n' % (self.assm_time))
			fobj.write('\t\tModel has '+str(len(self.meshes[mesh].nodes))+str(' nodes, ')+ \
						str(len(self.meshes[mesh].elements))+' elements, and\n\t\t'+ \
						str(self.meshes[mesh].nDOFs)+' degrees of freedom\n')
			fobj.close()

			# instantiate and run all solution objects listed in the *.sol-file
			# in such an order that they will use the same mesh stiffness and
			# mass matrices to save time and memory
			for solution in self.meshes[mesh].solutions:
				self.solutions[solution] = globals()[inputobj.solutions[solution]['type']](solution,self.meshes[mesh])
				self.solutions[solution].loads = {}
				for load in inputobj.solutions[solution]['loads']:
					self.solutions[solution].loads[load] = self.loads[load]
					if self.solutions[solution].loads[load].type == 'Acceleration':
						self.solutions[solution].hasBaseMotion = True
				self.solutions[solution].boundaries = {}
				for BC in inputobj.solutions[solution]['boundaries']:
					self.solutions[solution].boundaries[BC] = self.boundaries[BC]
				self.solutions[solution].constraints = {}
				for constr in inputobj.solutions[solution]['constraints']:
					self.solutions[solution].constraints[constr] = self.constraints[constr]
				self.solutions[solution].dampings = {}
				for damp in inputobj.solutions[solution]['dampings']:
					self.solutions[solution].dampings[damp] = self.dampings[damp]
				self.solutions[solution].results = {}
				self.solutions[solution].nodesets = {}
				self.solutions[solution].elementsets = {}
				for result in inputobj.solutions[solution]['results']:
					self.solutions[solution].results[result] = inputobj.solutions[solution]['results'][result]
					if result in ['displacement', 'nodeforce', 'acceleration', 'velocity', 'frf_accel', 'elementforce', 'stress', 'strain']:
						for pltxt in self.solutions[solution].results[result]:
							if result in ['displacement', 'nodeforce', 'acceleration', 'velocity', 'frf_accel']:
#								print('adding results nodesets for:', result)
								if self.solutions[solution].results[result][pltxt] not in self.solutions[solution].nodesets:
									self.solutions[solution].nodesets[self.solutions[solution].results[result][pltxt]] = \
																			self.nodesets[self.solutions[solution].results[result][pltxt]]
							elif result in ['stress', 'strain', 'elementforce']:
								if self.solutions[solution].results[result][pltxt] not in self.solutions[solution].elementsets:
									self.solutions[solution].elementsets[self.solutions[solution].results[result][pltxt]] = \
																			self.elementsets[self.solutions[solution].results[result][pltxt]]
							else:
								pass

				# run static solution
				if self.solutions[solution].type == 'Static':
					sol_time_start = time.time()
					print('\n\n    |------^------^------^------^------^------^------|')
					print('\tStarting solution:', solution, '(Static)')
					print('    |------^------^------^------^------^------^------|\n')
					print('\tApplying multipoint constraints...')
					self.solutions[solution].applyConstraints()
					print('\tApplying boundary conditions...')
					self.solutions[solution].applyBoundaryConditions()
					print('\tAssembling load vector...')
					self.solutions[solution].assembleLoadVector()
					print('\tCalculating displacements...')
					self.solutions[solution].calcDisplacements()
					print('\tCalculating node forces...')
					self.solutions[solution].calcNodeForces()
					self.solutions[solution].calcElementForces()
					self.solutions[solution].calcElementStrains()
					print('\tWriting results to file...')
					self.solutions[solution].writeResults(self.name)
					sol_time_stop = time.time()
					sol_time = sol_time_stop - sol_time_start
					print('\n\tSolution time: %.3f seconds\n' % (sol_time))

				# run Eigenmodes solution
				elif self.solutions[solution].type == 'Eigenmodes':
					sol_time_start = time.time()
					print('\n\n    |------^------^------^------^------^------^------|')
					print('       Starting solution:', solution, '(Eigenmodes)')
					print('    |------^------^------^------^------^------^------|\n')
					print('\tApplying multipoint constraints...')
					self.solutions[solution].applyConstraints()
					print('\tApplying boundary conditions...')
					self.solutions[solution].applyBoundaryConditions()
					print('\tCalculating eigenmodes...')
					self.solutions[solution].calcEigenvalues()
					print('\tWriting results to file...')
					self.solutions[solution].writeResults(self.name)
					sol_time_stop = time.time()
					sol_time = sol_time_stop - sol_time_start
					print('\n\tSolution time: %.3f seconds\n' % (sol_time))

				# run ModalDynamic solution
				elif self.solutions[solution].type == 'ModalDynamic':
					sol_time_start = time.time()
					print('\n\n    |------^------^------^------^------^------^------|')
					print('      Starting solution:', solution, '(ModalDynamic)')
					print('    |------^------^------^------^------^------^------|\n')
					print('\tApplying multipoint constraints...')
					self.solutions[solution].applyConstraints()
					print('\tApplying boundary conditions...')
					self.solutions[solution].applyBoundaryConditions()
					print('\tAssembling load vector...')
					self.solutions[solution].assembleLoadVector()
					print('\tCalculating eigenmodes...')
					self.solutions[solution].calcEigenvalues()
					print('\tCalculating displacements...')
					self.solutions[solution].calcDisplacements()
					print('\tWriting results to file...')
					self.solutions[solution].writeResults(self.name)
					self.solutions[solution].exportToCSV(self.name)
					sol_time_stop = time.time()
					sol_time = sol_time_stop - sol_time_start
					print('\n\tSolution time: %.3f seconds\n' % (sol_time))

				# run non-linear StaticPlastic solution
				elif self.solutions[solution].type == 'StaticPlastic':
					pass
				else:
					print('\n\tUnknown solution type:', self.solutions[solution].type, '\n')

	
			print('\tDeleting stiffness matrices...')
			# print out stiffness-matrix by
			# uncommenting the next 5 lines
			# (not including MPCs!).
#			print('\n\tStiffness matrix:')
#			for row in range(self.meshes[mesh].nDOFs):
#				for col in range(self.meshes[mesh].nDOFs):
#					print(self.meshes[mesh].K_mpc[row,col], end=' ')
#				print(' ')
			del self.meshes[mesh].K
			for solution in self.meshes[mesh].solutions:
				if hasattr(self.solutions[solution], 'K_11'):
					del self.solutions[solution].K_11
				if hasattr(self.solutions[solution], 'K_12'):
					del self.solutions[solution].K_12
				if hasattr(self.solutions[solution], 'K_22'):
					del self.solutions[solution].K_22
				if hasattr(self.solutions[solution], 'K_mpc'):
					del self.solutions[solution].K_mpc
			for element in self.meshes[mesh].elements:
				del self.meshes[mesh].elements[element].K
				if hasattr(self.meshes[mesh].elements[element],'T_elm'):
					del self.meshes[mesh].elements[element].T_elm
			if self.meshes[mesh].needMassMatrix == True:
				for solution in self.meshes[mesh].solutions:
					if hasattr(self.solutions[solution], 'M_11'):
						del self.solutions[solution].M_11
					if hasattr(self.solutions[solution], 'M_12'):
						del self.solutions[solution].M_12
					if hasattr(self.solutions[solution], 'M_22'):
						del self.solutions[solution].M_22
					if hasattr(self.solutions[solution], 'M'):
						del self.solutions[solution].M
				print('\tDeleting mass matrices...')
				# print out mass-matrix by
				# uncommenting the next 8 lines
				# (not including MPCs!).
#				print('\n\tMass matrix:')
#				for row in range(self.meshes[mesh].nDOFs):
#					for col in range(self.meshes[mesh].nDOFs):
#						if row == col:
#							print(self.meshes[mesh].M[row], end=' ')
#						else:
#							print(0.0, end=' ')
#					print(' ')
				del self.meshes[mesh].M
				for element in self.meshes[mesh].elements:
					del self.meshes[mesh].elements[element].M
			print('\n\n    |------^------^------^------^------^------^------|\n')
			fobj = open(self.name+'.res', 'a')
			fobj.write('\n\n    |------^------^------^------^------^------^------|\n\n')
			fobj.write('    |------^------^------^------^------^------^------|\n\n')
			fobj.close()
		if os.path.exists(self.name+'.out'):
			print('\tOverwriting solution file '+self.name+'.out\n')
		pickle.dump((self,), open(self.name+'.out', 'wb'))



	def nodeFreedomMapTable(self,nodes):
		'''
	Set up node freedom map table. Every element needs
	this to set up an element freedom table, which is
	used for assembling element stiffness matrices into
	the global stiffness matrix.
	
	self.NFAT 			- node freedom allocation table
	self.nodes[i].NFS	- node freedom signature
	self.NFMT			- node freedom map table
	self.nDOFs			- total degrees of freedom for model
	'''
		NFAT = {}
		for i in nodes:
			NFAT[i] = nodes[i].NFS

		NFMT = {}
		m = 0
		for i in nodes:
			NFMT[nodes[i].number] = m
			k = 0
			for j in range(6):
				if NFAT[i][j] == 1:
					k += 1
			m += k
		nDOFs = m

		return [NFAT, NFMT, nDOFs]


	def assembleStiffnessMatrix(self,mesh):
		'''
	Assemble the global stiffness matrix. First set up
	element freedom tables for each element using self.NFAT
	and self.NFMT as input. Then merge all element stiffness
	matrices into mesh.K matrix using their element 
	freedom tables.
	'''
		row = []
		col = []
		data = []
		for i in mesh.elements:
			mesh.elements[i].elementFreedomTable(mesh.NFAT,mesh.NFMT)
			mesh.elements[i].calcStiffnessMatrix()
			elmDOFs = len(mesh.elements[i].K)
			for j in range(elmDOFs):
				for k in range(elmDOFs):
					row.append(mesh.elements[i].EFT[k])
					col.append(mesh.elements[i].EFT[j])
					data.append(mesh.elements[i].K[j][k])

		mesh.K = sp.coo_matrix((np.array(data),(np.array(row),np.array(col))),shape=(mesh.nDOFs,mesh.nDOFs))
		mesh.K = mesh.K.tocsc()


	def assembleMassMatrix(self,mesh):
		'''
	Assemble the global mass matrix by merging
	all element mass matrices into mesh.M matrix
	using their element freedom tables. mesh.M
	only has values on the diagonal and is
	therefore stored as a vector to save memory.
	'''
		print('\n\tAssembling mass matrix...')
		mesh.M = np.zeros(mesh.nDOFs)
		mesh.totalMass = [0., 0., 0., 0., 0., 0.]

		for i in mesh.elements:
			mesh.elements[i].calcMassMatrix()
			elmDOFs = len(mesh.elements[i].M)
			m = 0
			for k in range(6):
				if mesh.elements[i].EFS[0][k] == 1:
					m += 1
			k = 0
			for j in range(elmDOFs):
				mesh.M[mesh.elements[i].EFT[j]] += mesh.elements[i].M[j][j]
				mesh.totalMass[k] += mesh.elements[i].M[j][j]
				k += 1
				if k == m:
					k = 0
		if mesh.totalMass[0] == mesh.totalMass[1]:
			print('\tTotal Mass: %.4E' % (mesh.totalMass[0]))
		else:
			print('\tSomething wrong with mass matrix...')
			print('\tMass:', mesh.totalMass[0])







	

if __name__ == '__main__':

	print('\n\n\tFinite Element Solver v3.0')
	print('\t--------------------------\n')
	print('\tThis finite element solver takes input solver files (.sol)')
	print('\tand generates displacement, stress, strain and more results')
	print('\tas requested in the solver files.')

	fname = input('\n\n\tsolver-file: ')
	inputobj = InputData(fname)
	if inputobj.input_error == False:
		model = FEModel(inputobj)
	else:
		print('\n\tSolver aborted because of input error(s).')





