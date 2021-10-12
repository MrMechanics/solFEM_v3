#
#
#	reader.py
#  -----------
#
#	This is the reader module. It generates an InputData object, by reading
# 	data from the input file (*.sol). This InputData object is used by the
#	FEModel object in solFEM.py to run the various solvers.
#



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

				if(eachLine[0] == '#'):
					pass
				elif(eachLine[0:4] == 'NODE'):
					tmpNode = []
					tmpStr = ''
					k = 0
					for i in eachLine:
						if i == ' ':
							pass
						elif i == ',':
							if k == 0:
								tmpStr = ''
							elif k == 1:
								tmpNode.append(int(tmpStr))
								tmpStr = ''
							else:
								tmpNode.append(float(tmpStr))
								tmpStr = ''
							k += 1
						elif i == '\n':
							tmpNode.append(float(tmpStr))
							break
						else:
							tmpStr += i
					self.nodes[tmpNode[0]] = {'coord':tmpNode[1:]}

				elif(eachLine[0:9] == 'SET_NODES'):
					tmpNodeSet = []
					tmpStr = ''
					tofrom = False
					k = 0
					for i in eachLine:
						if i == ' ':
							pass
						elif i == ',':
							if k == 0:
								tmpStr = ''
							elif tofrom == True:
								tmpNodeSet[-1].append(int(tmpStr))
								tmpStr = ''
								tofrom = False
							elif k == 1:
								tmpNodeSet.append(int(tmpStr))
								tmpStr = ''
							else:
								tmpNodeSet.append(int(tmpStr))
								tmpStr = ''
							k += 1
						elif i == '-':
							tmpNodeSet.append([int(tmpStr),])
							tmpStr = ''
							tofrom = True
						elif i == '\n':
							if tofrom == True:
								tmpNodeSet[-1].append(int(tmpStr))
							else:
								tmpNodeSet.append(int(tmpStr))
							break
						else:
							tmpStr += i
					self.nodesets[tmpNodeSet[0]] = tmpNodeSet[1:]

				elif(eachLine[0:8] == 'MATERIAL'):
					tmpMat = []
					tmpProp = []
					tmpStr = ''
					k = 0
					for i in eachLine:
						if i == ' ':
							pass
						elif i == ',':
							if k == 0:
								tmpStr = ''
							elif k == 1:
								tmpMat.append(tmpStr)
								tmpStr = ''
							elif k == 2:
								tmpMat.append(tmpStr)
								tmpStr = ''
							else:
								tmpProp.append(float(tmpStr))
								tmpStr = ''
							k += 1
						elif i == '\n':
							tmpProp.append(float(tmpStr))
							break
						else:
							tmpStr += i
					self.materials[tmpMat[1]] = {'type':tmpMat[0],'properties':tmpProp}
					if self.materials[tmpMat[1]]['type'] == 'Isotropic':
						self.materials[tmpMat[1]]['properties'] = {}
						if len(tmpProp) >= 2:
							self.materials[tmpMat[1]]['properties']['E-modulus'] = tmpProp[0]
							self.materials[tmpMat[1]]['properties']['poisson ratio'] = tmpProp[1]
						else:
							print('\n\tERROR: (line number '+str(line_number)+')')
							print('\tNot enough material properties specified for ', tmpMat[1])
							input_error = True
							break
						if len(tmpProp) > 2:
							self.materials[tmpMat[1]]['properties']['density'] = tmpProp[2]
						if len(tmpProp) > 3:
							self.materials[tmpMat[1]]['properties']['thermal expansion coefficient'] = tmpProp[3]
						if len(tmpProp) > 4:
							self.materials[tmpMat[1]]['properties']['conductivity'] = tmpProp[4]
						if len(tmpProp) > 5:
							self.materials[tmpMat[1]]['properties']['specific heat'] = tmpProp[5]
					else:
						print('\n\tERROR: (line number '+str(line_number)+')')
						print('\tUnknown material type: ', tmpMat[0])
						input_error = True
						break

				elif(eachLine[0:7] == 'SECTION'):
					tmpSect = []
					tmpProp = []
					tmpStr = ''
					k = 0
					for i in eachLine:
						if i == ' ':
							pass
						elif i == ',':
							if k == 0:
								tmpStr = ''
							elif k == 1:
								tmpSect.append(tmpStr)
								tmpStr = ''
							elif k == 2:
								tmpSect.append(int(tmpStr))
								tmpStr = ''
							elif k == 3:
								tmpSect.append(tmpStr)
								tmpStr = ''
							elif k == 4:
								tmpProp.append(float(tmpStr))
								tmpStr = ''
							else:
								tmpProp.append(tmpStr)
								tmpStr = ''
							k += 1
						elif i == '\n':
							if k == 3:
								tmpSect.append(tmpStr)
							elif k == 4:
								tmpProp.append(float(tmpStr))
								tmpStr = ''
							else:
								tmpProp.append(tmpStr)
								tmpStr = ''
							break
						else:
							tmpStr += i
					self.sections[tmpSect[1]] = {'type':tmpSect[0],
												 'material':tmpSect[2]}
					if self.sections[tmpSect[1]]['type'] == 'PlaneSect':
						self.sections[tmpSect[1]]['properties'] = {'thickness': tmpProp[0]}
						if len(tmpProp) == 2:
							if tmpProp[1] == 'planestrain':
								self.sections[tmpSect[1]]['properties']['planestrain'] = True
							else:
								print('\n\tERROR: (line number '+str(line_number)+')')
								print('\tUnknown input for SECTION ', tmpSect[1], ': ', tmpProp[1])
								input_error = True
								break
						else:
							self.sections[tmpSect[1]]['properties']['planestrain'] = False
					elif self.sections[tmpSect[1]]['type'] == 'PlateSect':
						self.sections[tmpSect[1]]['properties'] = {'thickness': tmpProp[0]}
					elif self.sections[tmpSect[1]]['type'] == 'RodSect':
						self.sections[tmpSect[1]]['properties'] = {'area': tmpProp[0]}
					elif self.sections[tmpSect[1]]['type'] == 'BeamSect':
						self.sections[tmpSect[1]]['properties'] = {'area': tmpProp[0], 'Izz': float(tmpProp[1])}
						if len(tmpProp) == 3:
							self.sections[tmpSect[1]]['properties']['Iyy'] = float(tmpProp[2])
					elif self.sections[tmpSect[1]]['type'] == 'SolidSect':
						self.sections[tmpSect[1]]['properties'] = {}
					else:
						print('\n\tERROR: (line number '+str(line_number)+')')
						print('\tUnknown SECTION type: ', tmpSect[0])
						input_error = True
						break

				elif(eachLine[0:10] == 'BEAMORIENT'):
					tmpBeam = []
					tmpStr = ''
					k = 0
					for i in eachLine:
						if i == ' ':
							pass
						elif i == ',':
							if k == 0:
								tmpStr = ''
							elif k == 1:
								tmpBeam.append(tmpStr)
								tmpStr = ''
							elif k == 2:
								tmpBeam.append(tmpStr)
								tmpStr = ''
							elif k == 3:
								tmpBeam.append(int(tmpStr))
								tmpStr = ''
							else:
								tmpBeam.append(float(tmpStr))
								tmpStr = ''
							k += 1
						elif i == '\n':
							tmpBeam.append(float(tmpStr))
							tmpStr = ''
							break
						else:
							tmpStr += i
					self.beamOrients[tmpBeam[1]] = {'type':tmpBeam[0],
												 	'elementset':tmpBeam[2]}
					if self.beamOrients[tmpBeam[1]]['type'] == 'BEAM2N2D':
						self.beamOrients[tmpBeam[1]]['x-vec'] = [tmpBeam[3], tmpBeam[4]]
					elif self.beamOrients[tmpBeam[1]]['type'] == 'BEAM2N':
						self.beamOrients[tmpBeam[1]]['x-vec'] = [tmpBeam[3], tmpBeam[4], tmpBeam[5]]
						self.beamOrients[tmpBeam[1]]['y-vec'] = [tmpBeam[6], tmpBeam[7], tmpBeam[8]]
					else:
						print('\n\tERROR: (line number '+str(line_number)+')')
						print('\tUnknown BEAMSECTION type: ', tmpBeam[0])
						input_error = True
						break

				elif(eachLine[0:7] == 'ELEMENT'):
					tmpElm = []
					tmpStr = ''
					k = 0
					for i in eachLine:
						if i == ' ':
							pass
						elif i == ',':
							if k == 0:
								tmpStr = ''
							elif k == 1:
								tmpElm.append(tmpStr)
								tmpStr = ''
							elif k == 2:
								tmpElm.append(int(tmpStr))
								tmpStr = ''
							elif k == 3:
								tmpElm.append(int(tmpStr))
								tmpStr = ''
							else:
								tmpElm.append(int(tmpStr))
								tmpStr = ''
							k += 1
						elif i == '\n':
							tmpElm.append(int(tmpStr))
							break
						else:
							tmpStr += i
					self.elements[tmpElm[1]] = {'type':tmpElm[0],
												'section':tmpElm[2],
												'nodes':tmpElm[3:]}
					if tmpElm[0] in ['ROD2N', 'ROD2N2D', 'BEAM2N', 'BEAM2N2D', 'TRI3N',
									 'TRI6N', 'QUAD4N', 'QUAD8N', 'TET4N', 'TET10N', 'HEX8N', 'HEX20N']:
						pass
					else:
						print('\n\tERROR: (line number '+str(line_number)+')')
						print('\tUnknown ELEMENT type: ', tmpElm[0])
						input_error = True
						break

				elif(eachLine[0:12] == 'SET_ELEMENTS'):
					tmpElmSet = []
					tmpStr = ''
					tofrom = False
					k = 0
					for i in eachLine:
						if i == ' ':
							pass
						elif i == ',':
							if k == 0:
								tmpStr = ''
							elif tofrom == True:
								tmpElmSet[-1].append(int(tmpStr))
								tmpStr = ''
								tofrom = False
							elif k == 1:
								tmpElmSet.append(int(tmpStr))
								tmpStr = ''
							else:
								tmpElmSet.append(int(tmpStr))
								tmpStr = ''
							k += 1
						elif i == '-':
							tmpElmSet.append([int(tmpStr),])
							tmpStr = ''
							tofrom = True
						elif i == '\n':
							if tofrom == True:
								tmpElmSet[-1].append(int(tmpStr))
							else:
								tmpElmSet.append(int(tmpStr))
							break
						else:
							tmpStr += i
					self.elementsets[tmpElmSet[0]] = tmpElmSet[1:]

				elif(eachLine[0:4] == 'LOAD'):
					tmpLoad = []
					tmpForceVect = []
					tmpStr = ''
					k = 0
					for i in eachLine:
						if i == ' ':
							pass
						elif i == ',':
							if k == 0:
								tmpStr = ''
							elif k == 1:
								tmpLoad.append(tmpStr)
								tmpStr = ''
							elif k == 2:
								tmpLoad.append(tmpStr)
								tmpStr = ''
							elif k == 3:
								tmpLoad.append(int(tmpStr))
								tmpStr = ''
							elif k == 4:
								tmpLoad.append(float(tmpStr))
								tmpStr = ''
							else:
								tmpForceVect.append(float(tmpStr))
								tmpStr = ''
							k += 1
						elif i == '\n':
							tmpForceVect.append(float(tmpStr))
							break
						else:
							tmpStr += i
					self.loads[tmpLoad[1]] = {'type':tmpLoad[0],
											  'vector':tmpForceVect}
					if self.loads[tmpLoad[1]]['type'] == 'Gravity':
						self.loads[tmpLoad[1]]['acceleration'] = float(tmpLoad[3])
						self.loads[tmpLoad[1]]['elementset'] = tmpLoad[2]
					elif self.loads[tmpLoad[1]]['type'] in ['ForceConcentrated', 'Force', 'ForceDynamic', 'Acceleration']:
						self.loads[tmpLoad[1]]['force'] = float(tmpLoad[3])
						self.loads[tmpLoad[1]]['nodeset'] = tmpLoad[2]
					elif self.loads[tmpLoad[1]]['type'] == 'Torque':
						self.loads[tmpLoad[1]]['torque'] = float(tmpLoad[3])
						self.loads[tmpLoad[1]]['nodeset'] = tmpLoad[2]
					elif self.loads[tmpLoad[1]]['type'] == 'Pressure':
						self.loads[tmpLoad[1]]['pressure'] = float(tmpLoad[3])
						self.loads[tmpLoad[1]]['nodeset'] = tmpLoad[2]
					else:
						print('\n\tERROR: (line number '+str(line_number)+')')
						print('\tUnknown LOAD type: ', tmpLoad[0])
						input_error = True
						break

				elif(eachLine[0:8] == 'BOUNDARY'):
					tmpBC = []
					tmpDOFs = []
					tmpStr = ''
					k = 0
					for i in eachLine:
						if i == ' ':
							pass
						elif i == ',':
							if k == 0:
								tmpStr = ''
							elif k == 1:
								tmpBC.append(tmpStr)
								tmpStr = ''
							elif k == 2:
								tmpBC.append(tmpStr)
								tmpStr = ''
							elif k == 3:
								tmpBC.append(int(tmpStr))
								tmpStr = ''
							elif k == 4:
								tmpBC.append(float(tmpStr))
								tmpStr = ''
							else:
								tmpDOFs.append(int(tmpStr))
								tmpStr = ''
							k += 1
						elif i == '\n':
							tmpDOFs.append(int(tmpStr))
							break
						else:
							tmpStr += i
					self.boundaries[tmpBC[1]] = {'type':tmpBC[0],
												 'nodeset':tmpBC[2],
												 'value':tmpBC[3],
												 'DOFs':tmpDOFs}
					if tmpBC[0] in ['Displacement']:
						pass
					else:
						print('\n\tERROR: (line number '+str(line_number)+')')
						print('\tUnknown BOUNDARY type: ', tmpBC[0])
						input_error = True
						break

				elif(eachLine[0:10] == 'CONSTRAINT'):
					tmpCon = []
					tmpStr = ''
					k = 0
					for i in eachLine:
						if i == ' ':
							pass
						elif i == ',':
							if k == 0:
								tmpStr = ''
							elif k == 1:
								tmpCon.append(tmpStr)
								tmpStr = ''
							elif k == 2:
								tmpCon.append(tmpStr)
								tmpStr = ''
							elif k == 3:
								tmpCon.append(int(tmpStr))
								tmpStr = ''
							elif k == 4:
								tmpCon.append(int(tmpStr))
								tmpStr = ''
							elif k == 5:
								tmpCon.append(tmpStr)
								tmpStr = ''
							else:
								tmpCon.append(int(tmpStr))
								tmpStr = ''
							k += 1
						elif i == '\n':
							tmpCon.append(int(tmpStr))
							break
						else:
							tmpStr += i
					self.constraints[tmpCon[1]] = {'type':tmpCon[0],
												   'nodeset1':tmpCon[2],
												   'nodeset2':tmpCon[3]}
					if tmpCon[0] == 'TouchLock':
						self.constraints[tmpCon[1]]['tolerance'] = float(tmpCon[4])
						self.constraints[tmpCon[1]]['DOFs'] = tmpCon[5:]
					else:
						self.constraints[tmpCon[1]]['DOFs'] = [int(tmpCon[4])]+tmpCon[5:]
					if tmpCon[0] in ['NodeLock', 'TouchLock']:
						pass
					else:
						print('\n\tERROR: (line number '+str(line_number)+')')
						print('\tUnknown CONSTRAINT type: ', tmpCon[0])
						input_error = True
						break

				elif(eachLine[0:7] == 'DAMPING'):
					tmpDamp = []
					tmpStr = ''
					k = 0
					for i in eachLine:
						if i == ' ':
							pass
						elif i == ',':
							if k == 0:
								tmpStr = ''
							elif k == 1:
								tmpDamp.append(tmpStr)
								tmpStr = ''
							elif k == 2:
								tmpDamp.append(tmpStr)
								tmpStr = ''
							else:
								tmpDamp.append(tmpStr)
								tmpStr = ''
							k += 1
						elif i == '\n':
							tmpDamp.append(tmpStr)
							break
						else:
							tmpStr += i
					self.dampings[tmpDamp[1]] = {'type':tmpDamp[0]}
					if tmpDamp[0] == 'Viscous':
						self.dampings[tmpDamp[1]]['damping_ratio'] = float(tmpDamp[2])
					elif tmpDamp[0] == 'Frequency':
						self.dampings[tmpDamp[1]]['damping_ratio'] = 1.
					else:
						print('\n\tERROR: (line number '+str(line_number)+')')
						print('\tUnknown DAMPING type: ', tmpDamp[0])
						input_error = True
						break

				elif(eachLine[0:5] == 'TABLE'):
					tmpTab = []
					tmpStr = ''
					k = 0
					for i in eachLine:
						if i == ' ':
							pass
						elif i == ',':
							if k == 0:
								tmpStr = ''
							elif k == 1:
								tmpTab.append(tmpStr)
								tmpStr = ''
							elif k == 2:
								tmpTab.append(int(tmpStr))
								tmpStr = ''
							else:
								tmpTab.append(tmpStr)
								tmpStr = ''
							k += 1
						elif i == '\n':
							tmpTab.append(tmpStr)
							break
						else:
							tmpStr += i
					self.tables[tmpTab[1]] = {'type':tmpTab[0],
											  'filename':tmpTab[3]}
					if tmpTab[0] == 'Acceleration':
						self.tables[tmpTab[1]]['type'] = 'AccelTable'
						self.tables[tmpTab[1]]['boundary'] = tmpTab[2]
					elif tmpTab[0] == 'StressStrain':
						self.tables[tmpTab[1]]['type'] = 'StressStrainTable'
						self.tables[tmpTab[1]]['material'] = tmpTab[2]
					elif tmpTab[0] == 'ForceDynamic':
						self.tables[tmpTab[1]]['type'] = 'ForceTable'
						self.tables[tmpTab[1]]['load'] = tmpTab[2]
					elif tmpTab[0] == 'DampingRatio':
						self.tables[tmpTab[1]]['type'] = 'DampingTable'
						self.tables[tmpTab[1]]['damping'] = tmpTab[2]
					else:
						print('\n\tERROR: (line number '+str(line_number)+')')
						print('\tUnknown TABLE type: ', tmpTab[0])
						input_error = True
						break

				elif(eachLine[0:8] == 'SOLUTION'):
					tmpSol = []
					tmpStr = ''
					k = 0
					for i in eachLine:
						if i == ' ':
							pass
						elif i == ',':
							if k == 0:
								tmpStr = ''
							elif k == 1:
								tmpSol.append(tmpStr)
								tmpStr = ''
							k += 1
						elif i == '\n':
							tmpSol.append(tmpStr)
							break
						else:
							tmpStr += i
					self.solutions[tmpSol[0]] = {'type':tmpSol[1],
												 'meshes': {},
												 'constraints': [],
												 'loads': [],
												 'boundaries': [],
												 'dampings': [],
												 'results': {} }
					current_solution = tmpSol[0]
					self.meshes[current_solution] = 'all'
					if tmpSol[1] in ['Static', 'StaticPlastic', 'Eigenmodes', 'ModalDynamic']:
						pass
					else:
						print('\n\tERROR: (line number '+str(line_number)+')')
						print('\tUnknown SOLUTION type: ', tmpSol[1])
						input_error = True
						break

				elif(eachLine[0:7] == '\tMESHES'):
					if current_solution == '':
						print('\n\tERROR: (line number '+str(line_number)+')')
						print('\tMESHES need to be specified AFTER the SOLUTION they are used in!')
						input_error = True
						break
					else:
						tmpMesh = []
						tmpStr = ''
						k = 0
						for i in eachLine:
							if i == ' ':
								pass
							elif i == ',':
								if k == 0:
									tmpStr = ''
								elif k == 1:
									tmpMesh.append(int(tmpStr))
									tmpStr = ''
								k += 1
							elif i == '\n':
								tmpMesh.append(int(tmpStr))
								break
							else:
								tmpStr += i
						self.solutions[current_solution]['meshes'] = tmpMesh
						self.meshes[current_solution] = tmpMesh

				elif(eachLine[0:12] == '\tCONSTRAINTS'):
					if current_solution == '':
						print('\n\tERROR: (line number '+str(line_number)+')')
						print('\tCONSTRAINTS need to be specified AFTER the SOLUTION they are used in!')
						input_error = True
						break
					else:
						tmpCon = []
						tmpStr = ''
						k = 0
						for i in eachLine:
							if i == ' ':
								pass
							elif i == ',':
								if k == 0:
									tmpStr = ''
								elif k == 1:
									tmpCon.append(tmpStr)
									tmpStr = ''
								k += 1
							elif i == '\n':
								tmpCon.append(tmpStr)
								break
							else:
								tmpStr += i
						self.solutions[current_solution]['constraints'].append(tmpCon[0])

				elif(eachLine[0:6] == '\tLOADS'):
					if current_solution == '':
						print('\n\tERROR: (line number '+str(line_number)+')')
						print('\tLOADS need to be specified AFTER the SOLUTION they are used in!')
						input_error = True
						break
					else:
						tmpLoad = []
						tmpStr = ''
						k = 0
						for i in eachLine:
							if i == ' ':
								pass
							elif i == ',':
								if k == 0:
									tmpStr = ''
								elif k == 1:
									tmpLoad.append(tmpStr)
									tmpStr = ''
								k += 1
							elif i == '\n':
								tmpLoad.append(tmpStr)
								break
							else:
								tmpStr += i
						self.solutions[current_solution]['loads'].append(tmpLoad[0])

				elif(eachLine[0:11] == '\tBOUNDARIES'):
					if current_solution == '':
						print('\n\tERROR: (line number '+str(line_number)+')')
						print('\tBOUNDARIES need to be specified AFTER the SOLUTION they are used in!')
						input_error = True
						break
					else:
						tmpBC = []
						tmpStr = ''
						k = 0
						for i in eachLine:
							if i == ' ':
								pass
							elif i == ',':
								if k == 0:
									tmpStr = ''
								elif k == 1:
									tmpBC.append(tmpStr)
									tmpStr = ''
								k += 1
							elif i == '\n':
								tmpBC.append(tmpStr)
								break
							else:
								tmpStr += i
						self.solutions[current_solution]['boundaries'].append(tmpBC[0])

				elif(eachLine[0:9] == '\tDAMPINGS'):
					if current_solution == '':
						print('\n\tERROR: (line number '+str(line_number)+')')
						print('\tDAMPINGS need to be specified AFTER the SOLUTION they are used in!')
						input_error = True
						break
					else:
						tmpDamp = []
						tmpStr = ''
						k = 0
						for i in eachLine:
							if i == ' ':
								pass
							elif i == ',':
								if k == 0:
									tmpStr = ''
								else:
									tmpDamp.append(tmpStr)
									tmpStr = ''
								k += 1
							elif i == '\n':
								tmpDamp.append(tmpStr)
								break
							else:
								tmpStr += i
						self.solutions[current_solution]['dampings'].append(tmpDamp[0])

				elif(eachLine[0:7] == 'RESULTS'):
					if current_solution == '':
						print('\n\tERROR: (line number '+str(line_number)+')')
						print('\tRESULTS need to be specified AFTER the SOLUTION they are used in!')
						input_error = True
						break
					else:
						tmpRes = []
						tmpStr = ''
						k = 0
						for i in eachLine:
							if i == ' ':
								pass
							elif i == ',':
								if k == 0:
									tmpStr = ''
								k += 1
							elif i == '\n':
								tmpRes.append(tmpStr)
								break
							else:
								tmpStr += i
						self.solutions[current_solution]['results'] = {}
						current_results = tmpRes

				elif(eachLine[0:13] == '\tDISPLACEMENT'):
					if current_results == '':
						print('\n\tERROR: (line number '+str(line_number)+')')
						print('\tDISPLACEMENT needs to be specified AFTER the RESULTS they are from!')
						input_error = True
						break
					else:
						tmpDisp = []
						tmpStr = ''
						k = 0
						for i in eachLine:
							if i == ' ':
								pass
							elif i == ',':
								if k == 0:
									tmpStr = ''
								elif k == 1:
									tmpDisp.append(tmpStr)
									tmpStr = ''
								elif k == 2:
									tmpDisp.append(int(tmpStr))
									tmpStr = ''
								elif k == 3:
									tmpDisp.append(tmpStr)
									tmpStr = ''
								elif k == 4:
									tmpDisp.append(int(tmpStr))
									tmpStr = ''
								k += 1
							elif i == '\n':
								tmpDisp.append(int(tmpStr))
								break
							else:
								tmpStr += i
						
						if len(tmpDisp) == 2:
							self.solutions[current_solution]['results']['displacement'] = \
										{tmpDisp[0]: tmpDisp[1]}
						elif len(tmpDisp) == 3:
							self.solutions[current_solution]['results']['displacement'] = \
										{tmpDisp[0]: tmpDisp[1], 'result DOF': tmpDisp[2]}
						elif len(tmpDisp) == 4:
							self.solutions[current_solution]['results']['displacement'] = \
										{tmpDisp[0]: tmpDisp[1], tmpDisp[2]: tmpDisp[3]}
						elif len(tmpDisp) == 5:
							self.solutions[current_solution]['results']['displacement'] = \
										{tmpDisp[0]: tmpDisp[1], tmpDisp[2]: tmpDisp[3], 'result DOF': tmpDisp[4]}
						else:
							print('\n\tWARNING: (line number '+str(line_number)+')')
							print('\tToo much input requested for this type of result.')

				elif(eachLine[0:13] == '\tACCELERATION'):
					if current_results == '':
						print('\n\tERROR: (line number '+str(line_number)+')')
						print('\tACCELERATION needs to be specified AFTER the RESULTS they are from!')
						input_error = True
						break
					else:
						tmpAcce = []
						tmpStr = ''
						k = 0
						for i in eachLine:
							if i == ' ':
								pass
							elif i == ',':
								if k == 0:
									tmpStr = ''
								elif k == 1:
									tmpAcce.append(tmpStr)
									tmpStr = ''
								elif k == 2:
									tmpAcce.append(int(tmpStr))
									tmpStr = ''
								elif k == 3:
									tmpAcce.append(tmpStr)
									tmpStr = ''
								elif k == 4:
									tmpAcce.append(int(tmpStr))
									tmpStr = ''
								k += 1
							elif i == '\n':
								tmpAcce.append(int(tmpStr))
								break
							else:
								tmpStr += i
						if len(tmpAcce) == 2:
							self.solutions[current_solution]['results']['acceleration'] = \
										{tmpAcce[0]: tmpAcce[1]}
						elif len(tmpAcce) == 3:
							self.solutions[current_solution]['results']['acceleration'] = \
										{tmpAcce[0]: tmpAcce[1], 'result DOF': tmpAcce[2]}
						elif len(tmpAcce) == 4:
							self.solutions[current_solution]['results']['acceleration'] = \
										{tmpAcce[0]: tmpAcce[1], tmpAcce[2]: tmpAcce[3]}
						elif len(tmpAcce) == 5:
							self.solutions[current_solution]['results']['acceleration'] = \
										{tmpAcce[0]: tmpAcce[1], tmpAcce[2]: tmpAcce[3], 'result DOF': tmpAcce[4]}
						else:
							print('\n\tWARNING: (line number '+str(line_number)+')')
							print('\tToo much input requested for this type of result.')

				elif(eachLine[0:10] == '\tFRF_ACCEL'):
					if current_results == '':
						print('\n\tERROR: (line number '+str(line_number)+')')
						print('\tFRF_ACCEL needs to be specified AFTER the RESULTS they are from!')
						input_error = True
						break
					else:
						tmpAcce = []
						tmpStr = ''
						k = 0
						for i in eachLine:
							if i == ' ':
								pass
							elif i == ',':
								if k == 0:
									tmpStr = ''
								elif k == 1:
									tmpAcce.append(tmpStr)
									tmpStr = ''
								elif k == 2:
									tmpAcce.append(int(tmpStr))
									tmpStr = ''
								elif k == 3:
									tmpAcce.append(tmpStr)
									tmpStr = ''
								elif k == 4:
									tmpAcce.append(int(tmpStr))
									tmpStr = ''
								k += 1
							elif i == '\n':
								tmpAcce.append(int(tmpStr))
								break
							else:
								tmpStr += i
						if len(tmpAcce) == 2:
							self.solutions[current_solution]['results']['frf_accel'] = \
										{tmpAcce[0]: tmpAcce[1]}
						elif len(tmpAcce) == 3:
							self.solutions[current_solution]['results']['frf_accel'] = \
										{tmpAcce[0]: tmpAcce[1], 'result DOF': tmpAcce[2]}
						elif len(tmpAcce) == 4:
							self.solutions[current_solution]['results']['frf_accel'] = \
										{tmpAcce[0]: tmpAcce[1], tmpAcce[2]: tmpAcce[3]}
						elif len(tmpAcce) == 5:
							self.solutions[current_solution]['results']['frf_accel'] = \
										{tmpAcce[0]: tmpAcce[1], tmpAcce[2]: tmpAcce[3], 'result DOF': tmpAcce[4]}
						else:
							print('\n\tWARNING: (line number '+str(line_number)+')')
							print('\tToo much input requested for this type of result.')

				elif(eachLine[0:10] == '\tSRS_ACCEL'):
					if current_results == '':
						print('\n\tERROR: (line number '+str(line_number)+')')
						print('\tFRF_ACCEL needs to be specified AFTER the RESULTS they are from!')
						input_error = True
						break
					else:
						tmpAcce = []
						tmpStr = ''
						k = 0
						for i in eachLine:
							if i == ' ':
								pass
							elif i == ',':
								if k == 0:
									tmpStr = ''
								elif k == 1:
									tmpAcce.append(tmpStr)
									tmpStr = ''
								elif k == 2:
									tmpAcce.append(int(tmpStr))
									tmpStr = ''
								elif k == 3:
									tmpAcce.append(tmpStr)
									tmpStr = ''
								elif k == 4:
									tmpAcce.append(int(tmpStr))
									tmpStr = ''
								k += 1
							elif i == '\n':
								tmpAcce.append(int(tmpStr))
								break
							else:
								tmpStr += i
						if len(tmpAcce) == 2:
							self.solutions[current_solution]['results']['srs_accel'] = \
										{tmpAcce[0]: tmpAcce[1]}
						elif len(tmpAcce) == 3:
							self.solutions[current_solution]['results']['srs_accel'] = \
										{tmpAcce[0]: tmpAcce[1], 'result DOF': tmpAcce[2]}
						elif len(tmpAcce) == 4:
							self.solutions[current_solution]['results']['srs_accel'] = \
										{tmpAcce[0]: tmpAcce[1], tmpAcce[2]: tmpAcce[3]}
						elif len(tmpAcce) == 5:
							self.solutions[current_solution]['results']['srs_accel'] = \
										{tmpAcce[0]: tmpAcce[1], tmpAcce[2]: tmpAcce[3], 'result DOF': tmpAcce[4]}
						else:
							print('\n\tWARNING: (line number '+str(line_number)+')')
							print('\tToo much input requested for this type of result.')

				elif(eachLine[0:9] == '\tVELOCITY'):
					if current_results == '':
						print('\n\tERROR: (line number '+str(line_number)+')')
						print('\tVELOCITY needs to be specified AFTER the RESULTS they are from!')
						input_error = True
						break
					else:
						tmpVel = []
						tmpStr = ''
						k = 0
						for i in eachLine:
							if i == ' ':
								pass
							elif i == ',':
								if k == 0:
									tmpStr = ''
								elif k == 1:
									tmpVel.append(tmpStr)
									tmpStr = ''
								elif k == 2:
									tmpVel.append(int(tmpStr))
									tmpStr = ''
								elif k == 3:
									tmpVel.append(tmpStr)
									tmpStr = ''
								elif k == 4:
									tmpVel.append(int(tmpStr))
									tmpStr = ''
								k += 1
							elif i == '\n':
								tmpVel.append(int(tmpStr))
								break
							else:
								tmpStr += i
						if len(tmpVel) == 2:
							self.solutions[current_solution]['results']['velocity'] = \
										{tmpVel[0]: tmpVel[1]}
						elif len(tmpVel) == 3:
							self.solutions[current_solution]['results']['velocity'] = \
										{tmpVel[0]: tmpVel[1], 'result DOF': tmpVel[2]}
						elif len(tmpVel) == 4:
							self.solutions[current_solution]['results']['velocity'] = \
										{tmpVel[0]: tmpVel[1], tmpVel[2]: tmpVel[3]}
						elif len(tmpVel) == 5:
							self.solutions[current_solution]['results']['velocity'] = \
										{tmpVel[0]: tmpVel[1], tmpVel[2]: tmpVel[3], 'result DOF': tmpVel[4]}
						else:
							print('\n\tWARNING: (line number '+str(line_number)+')')
							print('\tToo much input requested for this type of result.')

				elif(eachLine[0:10] == '\tNODEFORCE'):
					if current_results == '':
						print('\n\tERROR: (line number '+str(line_number)+')')
						print('\tNODEFORCE needs to be specified AFTER the RESULTS they are from!')
						input_error = True
						break
					else:
						tmpForc = []
						tmpStr = ''
						k = 0
						for i in eachLine:
							if i == ' ':
								pass
							elif i == ',':
								if k == 0:
									tmpStr = ''
								elif k == 1:
									tmpForc.append(tmpStr)
									tmpStr = ''
								elif k == 2:
									tmpForc.append(int(tmpStr))
									tmpStr = ''
								elif k == 3:
									tmpForc.append(tmpStr)
									tmpStr = ''
								elif k == 4:
									tmpForc.append(int(tmpStr))
									tmpStr = ''
								k += 1
							elif i == '\n':
								tmpForc.append(int(tmpStr))
								break
							else:
								tmpStr += i
						if len(tmpForc) == 2:
							self.solutions[current_solution]['results']['nodeforce'] = \
										{tmpForc[0]: tmpForc[1]}
						elif len(tmpForc) == 3:
							self.solutions[current_solution]['results']['nodeforce'] = \
										{tmpForc[0]: tmpForc[1], 'result DOF': tmpForc[2]}
						elif len(tmpForc) == 4:
							self.solutions[current_solution]['results']['nodeforce'] = \
										{tmpForc[0]: tmpForc[1], tmpForc[2]: tmpForc[3]}
						elif len(tmpForc) == 5:
							self.solutions[current_solution]['results']['nodeforce'] = \
										{tmpForc[0]: tmpForc[1], tmpForc[2]: tmpForc[3], 'result DOF': tmpForc[4]}
						else:
							print('\n\tWARNING: (line number '+str(line_number)+')')
							print('\tToo much input requested for this type of result.')

				elif(eachLine[0:13] == '\tELEMENTFORCE'):
					if current_results == '':
						print('\n\tERROR: (line number '+str(line_number)+')')
						print('\tELEMENTFORCE needs to be specified AFTER the RESULTS they are from!')
						input_error = True
						break
					else:
						tmpForc = []
						tmpStr = ''
						k = 0
						for i in eachLine:
							if i == ' ':
								pass
							elif i == ',':
								if k == 0:
									tmpStr = ''
								elif k == 1:
									tmpForc.append(tmpStr)
									tmpStr = ''
								elif k == 2:
									tmpForc.append(int(tmpStr))
									tmpStr = ''
								elif k == 3:
									tmpForc.append(tmpStr)
									tmpStr = ''
								elif k == 4:
									tmpForc.append(int(tmpStr))
									tmpStr = ''
								k += 1
							elif i == '\n':
								tmpForc.append(int(tmpStr))
								break
							else:
								tmpStr += i
						if len(tmpForc) == 2:
							self.solutions[current_solution]['results']['elementforce'] = \
										{tmpForc[0]: tmpForc[1]}
						if len(tmpForc) == 4:
							self.solutions[current_solution]['results']['elementforce'] = \
										{tmpForc[0]: tmpForc[1], tmpForc[2]: tmpForc[3]}

				elif(eachLine[0:7] == '\tSTRESS'):
					if current_results == '':
						print('\n\tERROR: (line number '+str(line_number)+')')
						print('\tSTRESS needs to be specified AFTER the RESULTS they are from!')
						input_error = True
						break
					else:
						tmpStrs = []
						tmpStr = ''
						k = 0
						for i in eachLine:
							if i == ' ':
								pass
							elif i == ',':
								if k == 0:
									tmpStr = ''
								elif k == 1:
									tmpStrs.append(tmpStr)
									tmpStr = ''
								elif k == 2:
									tmpStrs.append(int(tmpStr))
									tmpStr = ''
								elif k == 3:
									tmpStrs.append(tmpStr)
									tmpStr = ''
								elif k == 4:
									tmpStrs.append(int(tmpStr))
									tmpStr = ''
								k += 1
							elif i == '\n':
								tmpStrs.append(int(tmpStr))
								break
							else:
								tmpStr += i
						if len(tmpStrs) == 2:
							self.solutions[current_solution]['results']['stress'] = \
										{tmpStrs[0]: tmpStrs[1]}
						if len(tmpStrs) == 4:
							self.solutions[current_solution]['results']['stress'] = \
										{tmpStrs[0]: tmpStrs[1], tmpStrs[2]: tmpStrs[3]}

				elif(eachLine[0:7] == '\tSTRAIN'):
					if current_results == '':
						print('\n\tERROR: (line number '+str(line_number)+')')
						print('\tSTRAIN needs to be specified AFTER the RESULTS they are from!')
						input_error = True
						break
					else:
						tmpStrn = []
						tmpStr = ''
						k = 0
						for i in eachLine:
							if i == ' ':
								pass
							elif i == ',':
								if k == 0:
									tmpStr = ''
								elif k == 1:
									tmpStrn.append(tmpStr)
									tmpStr = ''
								elif k == 2:
									tmpStrn.append(int(tmpStr))
									tmpStr = ''
								elif k == 3:
									tmpStrn.append(tmpStr)
									tmpStr = ''
								elif k == 4:
									tmpStrn.append(int(tmpStr))
									tmpStr = ''
								k += 1
							elif i == '\n':
								tmpStrn.append(int(tmpStr))
								break
							else:
								tmpStr += i
						if len(tmpStrn) == 2:
							self.solutions[current_solution]['results']['strain'] = \
										{tmpStrn[0]: tmpStrn[1]}
						if len(tmpStrn) == 4:
							self.solutions[current_solution]['results']['strain'] = \
										{tmpStrn[0]: tmpStrn[1], tmpStrn[2]: tmpStrn[3]}

				elif(eachLine[0:11] == '\tMODESHAPES'):
					if current_results == '':
						print('\n\tERROR: (line number '+str(line_number)+')')
						print('\tMODESHAPES need to be specified AFTER the RESULTS they are from!')
						input_error = True
						break
					else:
						tmpMode = []
						tmpStr = ''
						k = 0
						for i in eachLine:
							if i == ' ':
								pass
							elif i == ',':
								if k == 0:
									tmpStr = ''
								elif k == 1:
									tmpMode.append(int(tmpStr))
									tmpStr = ''
								k += 1
							elif i == '\n':
								tmpMode.append(int(tmpStr))
								break
							else:
								tmpStr += i
						self.solutions[current_solution]['results']['modeshapes'] = tmpMode[0]

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
					print('\tUnknown input '+eachLine[0:15]+'...   Ignored!')

				line_number +=1

			fobj.close()
			return input_error







