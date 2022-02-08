#
#
#	reader.py
#  -----------
#
#	This is the reader module. It generates an InputData object, by reading
# 	data from the input file (*.sol). This InputData object is used by the
#	FEModel object in solFEM.py to run the various solvers.
#


import os
from timeit import time





class InputData(object):
	'''
Class for input read from *.sol-files. This object
reads the data from the *.sol-file into a format that
is accessible to the FEModel object.
'''
	def __init__(self,inputfile):

		self.name = inputfile[:-4]
		for i in range(len(inputfile)):
			if inputfile[-i-1] == '/' or inputfile[-i-1] == '\\':
				self.name = str(inputfile[-i:-4])
				break
		self.nodes = {}
		self.nodesets = {}
		self.elements = {}
		self.elementsets = {}
		self.materials = {}
		self.meshes = {}
		self.sections = {}
		self.beamOrients = {}
		self.loads = {}
		self.boundaries = {}
		self.constraints = {}
		self.dampings = {}
		self.tables = {}
		self.solutions = {}

		read_file_start = time.time()
		print('\n\tReading input file:', self.name, '...', end=' ')
		self.input_error = self.readInput(inputfile)
		if self.input_error == False:
			read_file_stop = time.time()
			self.read_time = read_file_stop - read_file_start
			print('%.3f seconds\n' % (self.read_time))


	def readInput(self,inputfile):
		'''
	Read nodes, materials, element sections,
	elements, boundary conditions, loads and
	solutions into the FEModel object
	'''
		try:
			fobj = open(inputfile, 'r')

		except OSError as e:
			print('\n\n  *** ERROR!!!', e)

		else:
			current_solution = ''
			current_results = ''
			input_error = False
			line_number = 1

			for eachLine in fobj:

				line = [x.strip() for x in eachLine.split(',')]
				if line[0] == '':
					pass
				elif(line[0][0] == '#'):
					pass
				elif(line[0] == 'NODE'):
					self.nodes[int(line[1])] = {'coord':[float(x) for x in line[2:]]}

				elif(line[0] == 'SET_NODES'):
					tmpNodeSet = []
					for n in line[2:]:
						if '-' not in n:
							tmpNodeSet.append(int(n))
						else:
							r_n = n.split('-')
							for n_i in range(int(r_n[0]),int(r_n[1])):
								tmpNodeSet.append(n_i)
							tmpNodeSet.append(int(r_n[1]))
					self.nodesets[int(line[1])] = tmpNodeSet

				elif(line[0] == 'MATERIAL'):
					self.materials[line[2]] = {'type':line[1],'properties': {}}
					if self.materials[line[2]]['type'] == 'Isotropic':
						if len(line[3:]) >= 2:
							self.materials[line[2]]['properties']['E-modulus'] = float(line[3])
							self.materials[line[2]]['properties']['poisson ratio'] = float(line[4])
						else:
							print('\n\tERROR: (line number '+str(line_number)+')')
							print('\tNot enough material properties specified for ', line[2])
							input_error = True
							break
						if len(line[3:]) > 2:
							self.materials[line[2]]['properties']['density'] = float(line[5])
						if len(line[3:]) > 3:
							self.materials[line[2]]['properties']['thermal expansion coefficient'] = float(line[6])
						if len(line[3:]) > 4:
							self.materials[line[2]]['properties']['conductivity'] = float(line[7])
						if len(line[3:]) > 5:
							self.materials[line[2]]['properties']['specific heat'] = float(line[8])
					else:
						print('\n\tERROR: (line number '+str(line_number)+')')
						print('\tUnknown material type: ', line[1])
						input_error = True
						break

				elif(line[0] == 'SECTION'):
					self.sections[line[2]] = {'type': line[1],
											  'material': line[3],
											  'properties': {}}
					if self.sections[line[2]]['type'] == 'PlaneSect':
						self.sections[line[2]]['properties']['thickness'] = float(line[4])
						if len(line) > 5:
							if line[5] == 'planestrain':
								self.sections[line[2]]['properties']['planestrain'] = True
							else:
								print('\n\tERROR: (line number '+str(line_number)+')')
								print('\tUnknown input for SECTION ', line[2], ': ', line[5])
								input_error = True
								break
						else:
							self.sections[line[2]]['properties']['planestrain'] = False
					elif self.sections[line[2]]['type'] == 'PlateSect':
						self.sections[line[2]]['properties']['thickness'] = float(line[4])
					elif self.sections[line[2]]['type'] == 'RodSect':
						self.sections[line[2]]['properties']['area'] = float(line[4])
					elif self.sections[line[2]]['type'] == 'BeamSect':
						self.sections[line[2]]['properties']['area'] = float(line[4])
						self.sections[line[2]]['properties']['Izz'] = float(line[5])
						if len(line) > 6 and line[6] != 'CrossSection':
							self.sections[line[2]]['properties']['Iyy']  = float(line[6])
					elif self.sections[line[2]]['type'] == 'SolidSect':
						pass
					else:
						print('\n\tERROR: (line number '+str(line_number)+')')
						print('\tUnknown SECTION type: ', line[1])
						input_error = True
						break
					if 'CrossSection' in line:
						c_n = line.index('CrossSection')
						if line[c_n+1] == 'Rectangle':
							self.sections[line[2]]['CrossSection'] = {'Type': line[c_n+1],
																	  'width, w': float(line[c_n+2]),
																	  'height, h': float(line[c_n+3]),
																	  'inner width, iw': float(line[c_n+4]),
																	  'inner height, ih': float(line[c_n+5])}
						elif line[c_n+1] == 'Circle':
							self.sections[line[2]]['CrossSection'] = {'Type': line[c_n+1],
																	  'radius, r': float(line[c_n+2]),
																	  'inner radius, ir': float(line[c_n+3])}
						elif line[c_n+1] == 'L-Beam':
							self.sections[line[2]]['CrossSection'] = {'Type': line[c_n+1],
																	  'side thickness, st': float(line[c_n+2]),
																	  'bottom width, bw': float(line[c_n+3]),
																	  'bottom thickness, bt': float(line[c_n+4]),
																	  'height, h': float(line[c_n+5])}
						elif line[c_n+1] == 'I-Beam':
							self.sections[line[2]]['CrossSection'] = {'Type': line[c_n+1],
																	  'top width, tw': float(line[c_n+2]),
																	  'top thickness, tt': float(line[c_n+3]),
																	  'middle thickness, mt': float(line[c_n+4]),
																	  'bottom width, bw': float(line[c_n+5]),
																	  'bottom thickness, bt': float(line[c_n+6]),
																	  'height, h': float(line[c_n+7])}
						elif line[c_n+1] == 'C-Beam':
							self.sections[line[2]]['CrossSection'] = {'Type': line[c_n+1],
																	  'top width, tw': float(line[c_n+2]),
																	  'top thickness, tt': float(line[c_n+3]),
																	  'middle thickness, mt': float(line[c_n+4]),
																	  'bottom width, bw': float(line[c_n+5]),
																	  'bottom thickness, bt': float(line[c_n+6]),
																	  'height, h': float(line[c_n+7])}
						elif line[c_n+1] == 'T-Beam':
							self.sections[line[2]]['CrossSection'] = {'Type': line[c_n+1],
																	  'top width, tw': float(line[c_n+2]),
																	  'top thickness, tt': float(line[c_n+3]),
																	  'middle thickness, mt': float(line[c_n+4]),
																	  'height, h': float(line[c_n+5])}
						else:
							print('\n\tERROR: (line number '+str(line_number)+')')
							print('\tUnknown SECTION CrossSection type: ', line[c_n+1])
							input_error = True
							break

				elif(line[0] == 'BEAMORIENT'):
					self.beamOrients[line[2]] = {'type': line[1],
												 'elementset': int(line[3])}
					if self.beamOrients[line[2]]['type'] == 'BEAM2N2D':
						self.beamOrients[line[2]]['x-vec'] = [float(line[4]), float(line[5])]
					elif self.beamOrients[line[2]]['type'] == 'BEAM2N':
						self.beamOrients[line[2]]['x-vec'] = [float(line[4]), float(line[5]), float(line[6])]
						self.beamOrients[line[2]]['y-vec'] = [float(line[7]), float(line[8]), float(line[9])]
					else:
						print('\n\tERROR: (line number '+str(line_number)+')')
						print('\tUnknown BEAMSECTION type: ', line[1])
						input_error = True
						break

				elif(line[0] == 'ELEMENT'):
					self.elements[int(line[2])] = {'type': line[1],
												   'section': line[3],
												   'nodes': [int(x) for x in line[4:]]}
					if line[1] in ['ROD2N', 'ROD2N2D', 'BEAM2N', 'BEAM2N2D', 'TRI3N',
									'TRI6N', 'QUAD4N', 'QUAD8N', 'TET4N', 'TET10N', 'HEX8N', 'HEX20N']:
						pass
					else:
						print('\n\tERROR: (line number '+str(line_number)+')')
						print('\tUnknown ELEMENT type: ', line[1])
						input_error = True
						break

				elif(line[0] == 'SET_ELEMENTS'):
					tmpElmSet = []
					for n in line[2:]:
						if '-' not in n:
							tmpElmSet.append(int(n))
						else:
							r_n = n.split('-')
							for n_i in range(int(r_n[0]),int(r_n[1])):
								tmpElmSet.append(n_i)
							tmpElmSet.append(int(r_n[1]))
					self.elementsets[int(line[1])] = tmpElmSet

				elif(line[0] == 'LOAD'):
					self.loads[line[2]] = {'type': line[1],
										   'vector': [float(x) for x in line[5:]]}
					if self.loads[line[2]]['type'] == 'Gravity':
						self.loads[line[2]]['acceleration'] = float(line[4])
						self.loads[line[2]]['elementset'] = int(line[3])
					elif self.loads[line[2]]['type'] in ['ForceConcentrated', 'Force', 'ForceDynamic', 'Acceleration']:
						self.loads[line[2]]['force'] = float(line[4])
						self.loads[line[2]]['nodeset'] = int(line[3])
					elif self.loads[line[2]]['type'] == 'Torque':
						self.loads[line[2]]['torque'] = float(line[4])
						self.loads[line[2]]['nodeset'] = int(line[3])
					elif self.loads[line[2]]['type'] == 'Pressure':
						self.loads[line[2]]['pressure'] = float(line[4])
						self.loads[line[2]]['nodeset'] = int(line[3])
					elif self.loads[line[2]]['type'] == 'ForceDistributed':
						self.loads[line[2]]['force'] = float(line[4])
						self.loads[line[2]]['elementset'] = int(line[3])
					else:
						print('\n\tERROR: (line number '+str(line_number)+')')
						print('\tUnknown LOAD type: ', line[1])
						input_error = True
						break

				elif(line[0] == 'BOUNDARY'):
					self.boundaries[line[2]] = {'type': line[1],
												'nodeset': int(line[3]),
												'value': float(line[4]),
												'DOFs': [int(x) for x in line[5:]]}
					if line[1] in ['Displacement']:
						pass
					else:
						print('\n\tERROR: (line number '+str(line_number)+')')
						print('\tUnknown BOUNDARY type: ', line[1])
						input_error = True
						break

				elif(line[0] == 'CONSTRAINT'):
					self.constraints[line[2]] = {'type': line[1],
												 'nodeset1': int(line[3]),
												 'nodeset2': int(line[4])}
					if line[1] == 'TouchLock':
						self.constraints[line[2]]['tolerance'] = float(line[5])
						self.constraints[line[2]]['DOFs'] = [int(x) for x in line[6:]]
					else:
						self.constraints[line[2]]['DOFs'] = [int(x) for x in line[6:]]
					if line[1] in ['NodeLock', 'TouchLock']:
						pass
					else:
						print('\n\tERROR: (line number '+str(line_number)+')')
						print('\tUnknown CONSTRAINT type: ', line[0])
						input_error = True
						break

				elif(line[0] == 'DAMPING'):
					self.dampings[line[2]] = {'type': line[1]}
					if line[1] == 'Viscous':
						self.dampings[line[2]]['damping_ratio'] = float(line[3])
					elif line[1] == 'Frequency':
						self.dampings[line[2]]['damping_ratio'] = 1.
					else:
						print('\n\tERROR: (line number '+str(line_number)+')')
						print('\tUnknown DAMPING type: ', line[1])
						input_error = True
						break

				elif(line[0] == 'TABLE'):
					self.tables[line[2]] = {'type': line[1],
											'filename': line[4]}
					if line[1] == 'Acceleration':
						self.tables[line[2]]['type'] = 'AccelTable'
						self.tables[line[2]]['boundary'] = line[3]
					elif line[1] == 'StressStrain':
						self.tables[line[2]]['type'] = 'StressStrainTable'
						self.tables[line[2]]['material'] = line[3]
					elif line[1] == 'ForceDynamic':
						self.tables[line[2]]['type'] = 'ForceTable'
						self.tables[line[2]]['load'] = line[3]
					elif line[1] == 'DampingRatio':
						self.tables[line[2]]['type'] = 'DampingTable'
						self.tables[line[2]]['damping'] = line[3]
					else:
						print('\n\tERROR: (line number '+str(line_number)+')')
						print('\tUnknown TABLE type: ', line[1])
						input_error = True
						break

				elif(line[0] == 'SOLUTION'):
					self.solutions[line[1]] = {'type':line[2],
											   'meshes': {},
											   'constraints': [],
											   'loads': [],
											   'boundaries': [],
											   'dampings': [],
											   'results': {} }
					current_solution = line[1]
					self.meshes[current_solution] = 'all'
					if line[2] in ['Static', 'StaticPlastic', 'Eigenmodes', 'ModalDynamic']:
						pass
					else:
						print('\n\tERROR: (line number '+str(line_number)+')')
						print('\tUnknown SOLUTION type: ', line[2])
						input_error = True
						break

				elif(line[0] == 'MESHES'):
					if current_solution == '':
						print('\n\tERROR: (line number '+str(line_number)+')')
						print('\tMESHES need to be specified AFTER the SOLUTION they are used in!')
						input_error = True
						break
					else:
						self.solutions[current_solution]['meshes'] = [int(x) for x in line[1:]]
						self.meshes[current_solution] = [int(x) for x in line[1:]]

				elif(line[0] == 'CONSTRAINTS'):
					if current_solution == '':
						print('\n\tERROR: (line number '+str(line_number)+')')
						print('\tCONSTRAINTS need to be specified AFTER the SOLUTION they are used in!')
						input_error = True
						break
					else:
						self.solutions[current_solution]['constraints'].append(line[1])

				elif(line[0] == 'LOADS'):
					if current_solution == '':
						print('\n\tERROR: (line number '+str(line_number)+')')
						print('\tLOADS need to be specified AFTER the SOLUTION they are used in!')
						input_error = True
						break
					else:
						self.solutions[current_solution]['loads'].append(line[1])

				elif(line[0] == 'BOUNDARIES'):
					if current_solution == '':
						print('\n\tERROR: (line number '+str(line_number)+')')
						print('\tBOUNDARIES need to be specified AFTER the SOLUTION they are used in!')
						input_error = True
						break
					else:
						self.solutions[current_solution]['boundaries'].append(line[1])

				elif(line[0] == 'DAMPINGS'):
					if current_solution == '':
						print('\n\tERROR: (line number '+str(line_number)+')')
						print('\tDAMPINGS need to be specified AFTER the SOLUTION they are used in!')
						input_error = True
						break
					else:
						self.solutions[current_solution]['dampings'].append(line[1])

				elif(line[0] == 'RESULTS'):
					if current_solution == '':
						print('\n\tERROR: (line number '+str(line_number)+')')
						print('\tRESULTS need to be specified AFTER the SOLUTION they are used in!')
						input_error = True
						break
					else:
						self.solutions[current_solution]['results'] = {}
						current_results = line[1]

				elif(line[0] == 'DISPLACEMENT'):
					if current_results == '':
						print('\n\tERROR: (line number '+str(line_number)+')')
						print('\tDISPLACEMENT needs to be specified AFTER the RESULTS they are from!')
						input_error = True
						break
					else:
						line += ['pass', 'pass']
						if 'plot' in line:
							self.solutions[current_solution]['results']['displacement'] = \
										{'plot': int(line[line.index('plot')+1])}
							if line[line.index('plot')+2].isdigit():
								self.solutions[current_solution]['results']['displacement']['result DOF'] = int(line[line.index('plot')+2])
						if 'text' in line:
							if 'plot' not in line:
								self.solutions[current_solution]['results']['displacement'] = {}
							self.solutions[current_solution]['results']['displacement']['text'] = int(line[line.index('text')+1])
							if line[line.index('text')+2].isdigit():
								self.solutions[current_solution]['results']['displacement']['result DOF'] = int(line[line.index('text')+2])

				elif(line[0] == 'ACCELERATION'):
					if current_results == '':
						print('\n\tERROR: (line number '+str(line_number)+')')
						print('\tACCELERATION needs to be specified AFTER the RESULTS they are from!')
						input_error = True
						break
					else:
						line += ['pass', 'pass']
						if 'plot' in line:
							self.solutions[current_solution]['results']['acceleration'] = \
										{'plot': int(line[line.index('plot')+1])}
							if line[line.index('plot')+2].isdigit():
								self.solutions[current_solution]['results']['acceleration']['result DOF'] = int(line[line.index('plot')+2])
						if 'text' in line:
							if 'plot' not in line:
								self.solutions[current_solution]['results']['acceleration'] = {}
							self.solutions[current_solution]['results']['acceleration']['text'] = int(line[line.index('text')+1])
							if line[line.index('text')+2].isdigit():
								self.solutions[current_solution]['results']['acceleration']['result DOF'] = int(line[line.index('text')+2])

				elif(line[0] == 'FRF_ACCEL'):
					if current_results == '':
						print('\n\tERROR: (line number '+str(line_number)+')')
						print('\tFRF_ACCEL needs to be specified AFTER the RESULTS they are from!')
						input_error = True
						break
					else:
						line += ['pass', 'pass']
						if 'plot' in line:
							self.solutions[current_solution]['results']['frf_accel'] = \
										{'plot': int(line[line.index('plot')+1])}
							if line[line.index('plot')+2].isdigit():
								self.solutions[current_solution]['results']['frf_accel']['result DOF'] = int(line[line.index('plot')+2])
						if 'text' in line:
							if 'plot' not in line:
								self.solutions[current_solution]['results']['frf_accel'] = {}
							self.solutions[current_solution]['results']['frf_accel']['text'] = int(line[line.index('text')+1])
							if line[line.index('text')+2].isdigit():
								self.solutions[current_solution]['results']['frf_accel']['result DOF'] = int(line[line.index('text')+2])

				elif(line[0] == 'SRS_ACCEL'):
					if current_results == '':
						print('\n\tERROR: (line number '+str(line_number)+')')
						print('\tFRF_ACCEL needs to be specified AFTER the RESULTS they are from!')
						input_error = True
						break
					else:
						line += ['pass', 'pass']
						if 'plot' in line:
							self.solutions[current_solution]['results']['srs_accel'] = \
										{'plot': int(line[line.index('plot')+1])}
							if line[line.index('plot')+2].isdigit():
								self.solutions[current_solution]['results']['srs_accel']['result DOF'] = int(line[line.index('plot')+2])
						if 'text' in line:
							if 'plot' not in line:
								self.solutions[current_solution]['results']['srs_accel'] = {}
							self.solutions[current_solution]['results']['srs_accel']['text'] = int(line[line.index('text')+1])
							if line[line.index('text')+2].isdigit():
								self.solutions[current_solution]['results']['srs_accel']['result DOF'] = int(line[line.index('text')+2])

				elif(line[0] == 'VELOCITY'):
					if current_results == '':
						print('\n\tERROR: (line number '+str(line_number)+')')
						print('\tVELOCITY needs to be specified AFTER the RESULTS they are from!')
						input_error = True
						break
					else:
						line += ['pass', 'pass']
						if 'plot' in line:
							self.solutions[current_solution]['results']['velocity'] = \
										{'plot': int(line[line.index('plot')+1])}
							if line[line.index('plot')+2].isdigit():
								self.solutions[current_solution]['results']['velocity']['result DOF'] = int(line[line.index('plot')+2])
						if 'text' in line:
							if 'plot' not in line:
								self.solutions[current_solution]['results']['velocity'] = {}
							self.solutions[current_solution]['results']['velocity']['text'] = int(line[line.index('text')+1])
							if line[line.index('text')+2].isdigit():
								self.solutions[current_solution]['results']['velocity']['result DOF'] = int(line[line.index('text')+2])

				elif(line[0] == 'NODEFORCE'):
					if current_results == '':
						print('\n\tERROR: (line number '+str(line_number)+')')
						print('\tNODEFORCE needs to be specified AFTER the RESULTS they are from!')
						input_error = True
						break
					else:
						line += ['pass', 'pass']
						if 'plot' in line:
							self.solutions[current_solution]['results']['nodeforce'] = \
										{'plot': int(line[line.index('plot')+1])}
							if line[line.index('plot')+2].isdigit():
								self.solutions[current_solution]['results']['nodeforce']['result DOF'] = int(line[line.index('plot')+2])
						if 'text' in line:
							if 'plot' not in line:
								self.solutions[current_solution]['results']['nodeforce'] = {}
							self.solutions[current_solution]['results']['nodeforce']['text'] = int(line[line.index('text')+1])
							if line[line.index('text')+2].isdigit():
								self.solutions[current_solution]['results']['nodeforce']['result DOF'] = int(line[line.index('text')+2])

				elif(line[0] == 'ELEMENTFORCE'):
					if current_results == '':
						print('\n\tERROR: (line number '+str(line_number)+')')
						print('\tELEMENTFORCE needs to be specified AFTER the RESULTS they are from!')
						input_error = True
						break
					else:
						line += ['pass', 'pass']
						if 'plot' in line:
							self.solutions[current_solution]['results']['elementforce'] = \
										{'plot': int(line[line.index('plot')+1])}
							if line[line.index('plot')+2].isdigit():
								self.solutions[current_solution]['results']['elementforce']['result DOF'] = int(line[line.index('plot')+2])
						if 'text' in line:
							if 'plot' not in line:
								self.solutions[current_solution]['results']['elementforce'] = {}
							self.solutions[current_solution]['results']['elementforce']['text'] = int(line[line.index('text')+1])
							if line[line.index('text')+2].isdigit():
								self.solutions[current_solution]['results']['elementforce']['result DOF'] = int(line[line.index('text')+2])


				elif(line[0] == 'STRESS'):
					if current_results == '':
						print('\n\tERROR: (line number '+str(line_number)+')')
						print('\tSTRESS needs to be specified AFTER the RESULTS they are from!')
						input_error = True
						break
					else:
						line += ['pass', 'pass']
						if 'plot' in line:
							self.solutions[current_solution]['results']['stress'] = \
										{'plot': int(line[line.index('plot')+1])}
							if line[line.index('plot')+2].isdigit():
								self.solutions[current_solution]['results']['stress']['result DOF'] = int(line[line.index('plot')+2])
						if 'text' in line:
							if 'plot' not in line:
								self.solutions[current_solution]['results']['stress'] = {}
							self.solutions[current_solution]['results']['stress']['text'] = int(line[line.index('text')+1])
							if line[line.index('text')+2].isdigit():
								self.solutions[current_solution]['results']['stress']['result DOF'] = int(line[line.index('text')+2])

				elif(line[0] == 'STRAIN'):
					if current_results == '':
						print('\n\tERROR: (line number '+str(line_number)+')')
						print('\tSTRAIN needs to be specified AFTER the RESULTS they are from!')
						input_error = True
						break
					else:
						line += ['pass', 'pass']
						if 'plot' in line:
							self.solutions[current_solution]['results']['strain'] = \
										{'plot': int(line[line.index('plot')+1])}
							if line[line.index('plot')+2].isdigit():
								self.solutions[current_solution]['results']['strain']['result DOF'] = int(line[line.index('plot')+2])
						if 'text' in line:
							if 'plot' not in line:
								self.solutions[current_solution]['results']['strain'] = {}
							self.solutions[current_solution]['results']['strain']['text'] = int(line[line.index('text')+1])
							if line[line.index('text')+2].isdigit():
								self.solutions[current_solution]['results']['strain']['result DOF'] = int(line[line.index('text')+2])

				elif(line[0] == 'MODESHAPES'):
					if current_results == '':
						print('\n\tERROR: (line number '+str(line_number)+')')
						print('\tMODESHAPES need to be specified AFTER the RESULTS they are from!')
						input_error = True
						break
					else:
						self.solutions[current_solution]['results']['modeshapes'] = int(line[1])

				elif(eachLine[0:14] == '\tENERGYDENSITY'):
					if current_results == '':
						print('\n\tERROR: (line number '+str(line_number)+')')
						print('\tENERGYDENSITY needs to be specified AFTER the RESULTS they are from!')
						input_error = True
						break
					else:
						self.solutions[current_solution]['results']['energydensity'] = True

				else:
					print('\n\tINPUT WARNING: (line number '+str(line_number)+')')
					print('\tUnknown input '+line[0]+'...   Ignored!')

				line_number +=1





			# reality check for sol-file
		# ---------------------------------


			# check that there are nodes
			if len(self.nodes) == 0:
				print('\n\tERROR:\n\tNo nodes have been defined.')
				input_error = True
		
			# check that there are elements
			if len(self.elements) == 0:
				print('\n\tERROR:\n\tNo elements have been defined.')
				input_error = True

			# check if all elements and nodes specified in
			# element- and nodesets are actually defined
			for nodeset in self.nodesets:
				if not all(node in self.nodes for node in self.nodesets[nodeset]):
					print('\n\tERROR:\n\tNodeset '+str(nodeset)+' contains nodes that have not been defined.')
					input_error = True

			for elementset in self.elementsets:
				if not all(element in self.elements for element in self.elementsets[elementset]):
					print('\n\tERROR:\n\tElementset '+str(elementset)+' contains elements that have not been defined.')
					input_error = True

			for element in self.elements:
				if self.elements[element]['section'] not in self.sections:
					print('\n\tERROR:\n\tElement '+str(element)+' has section which has not been defined.')
					input_error = True

				# check that elements have the right
				# number of nodes
				if self.elements[element]['type'] in ['ROD2N2D', 'ROD2N', 'BEAM2N2D', 'BEAM2N']:
					if len(self.elements[element]['nodes']) != 2:
						print('\n\tERROR:\n\tElement '+str(element)+' does not have the right number of nodes.')
						input_error = True
				elif self.elements[element]['type'] == 'TRI3N':
					if len(self.elements[element]['nodes']) != 3:
						print('\n\tERROR:\n\tElement '+str(element)+' does not have the right number of nodes.')
						input_error = True
				elif self.elements[element]['type'] == 'TRI6N':
					if len(self.elements[element]['nodes']) != 6:
						print('\n\tERROR:\n\tElement '+str(element)+' does not have the right number of nodes.')
						input_error = True
				elif self.elements[element]['type'] == 'QUAD4N':
					if len(self.elements[element]['nodes']) != 4:
						print('\n\tERROR:\n\tElement '+str(element)+' does not have the right number of nodes.')
						input_error = True
				elif self.elements[element]['type'] == 'QUAD8N':
					if len(self.elements[element]['nodes']) != 8:
						print('\n\tERROR:\n\tElement '+str(element)+' does not have the right number of nodes.')
						input_error = True
				elif self.elements[element]['type'] == 'TET4N':
					if len(self.elements[element]['nodes']) != 4:
						print('\n\tERROR:\n\tElement '+str(element)+' does not have the right number of nodes.')
						input_error = True
				elif self.elements[element]['type'] == 'TET10N':
					if len(self.elements[element]['nodes']) != 10:
						print('\n\tERROR:\n\tElement '+str(element)+' does not have the right number of nodes.')
						input_error = True
				elif self.elements[element]['type'] == 'HEX8N':
					if len(self.elements[element]['nodes']) != 8:
						print('\n\tERROR:\n\tElement '+str(element)+' does not have the right number of nodes.')
						input_error = True
				elif self.elements[element]['type'] == 'HEX20N':
					if len(self.elements[element]['nodes']) != 20:
						print('\n\tERROR:\n\tElement '+str(element)+' does not have the right number of nodes.')
						input_error = True
				else:
					pass

			# check if specified section
			# material is actually defined
			for sect in self.sections:
				if self.sections[sect]['material'] not in self.materials:
					print('\n\tERROR:\n\tSection '+sect+' uses material that has not been defined.')
					input_error = True

			# check if specifed tables
			# can be accessed
			for table in self.tables:
				if not os.path.isfile(self.tables[table]['filename']):
					print('\n\tERROR:\n\tTable '+table+' uses file '+self.tables[table]['filename']+' which does not exist.')
					input_error = True
			
			# check that nodelock constraints have
			# nodeset with only one node in it
			for constraint in self.constraints:
				if self.constraints[constraint]['nodeset1'] not in self.nodesets or \
						self.constraints[constraint]['nodeset2'] not in self.nodesets:
					print('\n\tERROR:\n\tConstraint '+constraint+' has nodeset that is not defined.')
					input_error = True
					break
				if self.constraints[constraint]['type'] == 'NodeLock':
					not_ok = True
					if len(self.nodesets[self.constraints[constraint]['nodeset1']]) == 1:
						not_ok = False
					if len(self.nodesets[self.constraints[constraint]['nodeset2']]) == 1:
						not_ok = False
					if not_ok:
						print('\n\tERROR:\n\tConstraint '+constraint+' must have at least one nodeset with only one node in it.')
						input_error = True

			for sol in self.solutions:
				# check that results are specified for
				# every solution
				if len(self.solutions[sol]['results']) == 0:
					print('\n\tERROR:\n\tSolution '+sol+' has no results requested.')
					input_error = True
					break

				# check if constraints in solution
				# have been defined
				for constraint in self.solutions[sol]['constraints']:
					if constraint not in self.constraints:
						print('\n\tERROR:\n\tSolution '+sol+' has constraints that are not defined.')
						input_error = True
					else:
						pass

				# check if specified loads are defined
				for load in self.solutions[sol]['loads']:
					if load not in self.loads:
						print('\n\tERROR:\n\tSolution '+sol+' has loads that are not defined.')
						input_error = True
						break
					else:
						if 'nodeset' in self.loads[load]:
							if self.loads[load]['nodeset'] not in self.nodesets:
								print('\n\tERROR:\n\tLoad '+load+' has nodeset that is not defined.')
								input_error = True
						if 'elementset' in self.loads[load]:
							if self.loads[load]['elementset'] not in self.elementsets:
								print('\n\tERROR:\n\tLoad '+load+' has elementset that is not defined.')
								input_error = True

				if self.solutions[sol]['type'] in ['Static', 'StaticPlastic']:
					# check that results requested are
					# supported for solution type
					for result in self.solutions[sol]['results']:
						if result not in ['displacement', 'nodeforce', 'elementforce', 'stress', 'strain']:
							print('\n\tERROR:\n\t'+result+' not supported for solution type '+self.solutions[sol]['type'])
							input_error = True

					# check if static solutions are
					# constrained with boundary conditions
					if len(self.solutions[sol]['boundaries']) == 0:
						print('\n\tERROR:\n\tSolution '+sol+' has no boundary conditions applied.')
						input_error = True

					# check if boundary conditions in solution
					# have been defined
					else:
						for boundary in self.solutions[sol]['boundaries']:
							if boundary not in self.boundaries:
								print('\n\tERROR:\n\tSolution '+sol+' has boundary conditions that are not defined.')
								input_error = True
							elif self.boundaries[boundary]['nodeset'] not in self.nodesets:
								print('\n\tERROR:\n\tBoundary '+boundary+' has nodeset that is not defined.')
								input_error = True
							else:
								pass

					# check if specified loads are
					# applicable to solution type
					for load in self.solutions[sol]['loads']:
						if load in self.loads:
							if self.loads[load]['type'] not in ['Force', 'ForceConcentrated', 'Torque', 'ForceDistributed', 'Gravity', 'Pressure']:
								print('\n\tERROR:\n\tSolution '+sol+' has loads that can not be used in Static solution.')
								input_error = True

				elif self.solutions[sol]['type'] in ['Eigenmodes']:
					if len(self.solutions[sol]['results']) == 0:
						print('\n\tERROR:\n\tSolution '+sol+' has no results requested.')
						input_error = True

				elif self.solutions[sol]['type'] in ['ModalDynamic']:
					# check that results requested are
					# supported for solution type
					for result in self.solutions[sol]['results']:
						if result not in ['displacement', 'velocity', 'acceleration', 'frf_accel', 'srs_accel', 'modeshapes']:
							print('\n\tERROR:\n\t'+result+' not supported for solution type '+self.solutions[sol]['type'])
							input_error = True

					# check if boundary conditions in solution
					# have been defined
					else:
						for boundary in self.solutions[sol]['boundaries']:
							if boundary not in self.boundaries:
								print('\n\tERROR:\n\tSolution '+sol+' has boundary conditions that are not defined.')
								input_error = True
							elif self.boundaries[boundary]['nodeset'] not in self.nodesets:
								print('\n\tERROR:\n\tBoundary '+boundary+' has nodeset that is not defined.')
								input_error = True
							else:
								pass

					# check if specified loads are
					# applicable to solution type
					for load in self.solutions[sol]['loads']:
						if self.loads[load]['type'] not in ['ForceDynamic', 'Acceleration']:
							print('\n\tERROR:\n\tSolution '+sol+' has loads that can not be used in ModalDynamic solution.')
							input_error = True

				else:
					pass


				# check that damping is applied to
				# modal dynamics solution
				

				
			fobj.close()
			return input_error







