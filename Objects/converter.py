#
#
#	script for converting mesh-file
#	from other formats into *.sol 
#	file for viewFEM to use
#


import time
import os
from nodes import Node
from elements import Element



class ConvertMesh:
	'''
Class for converting mesh-files from
other formats into *.sol-files to be
used with viewFEM.
'''
	def __init__(self,inputfile,filetype):

		self.name = inputfile[:-4]
		self.nodes = {}
		self.elements = {}
		self.elmTypes = []

		not_with_path = True
		for i in range(len(inputfile)):
			if inputfile[-i-1] == '/' or inputfile[-i-1] == '\\':
				self.shortname = inputfile[-i:]
				not_with_path = False
				break
		if not_with_path:
			self.shortname = inputfile

		read_file_start = time.time()
		print('\tReading input file:', self.shortname, '...',end=' ')
		if filetype == '.inp':
			self.input_error = self.readInp(inputfile)
		if filetype == '.bdf':
			self.input_error = self.readBdf(inputfile)
		read_file_stop = time.time()
		self.read_time = read_file_stop - read_file_start
		print('%.3f seconds\n' % (self.read_time))
		print('\tNumber of nodes in mesh: '+str(len(self.nodes)))
		print('\tNumber of elements in mesh: '+str(len(self.elements)))



	def readBdf(self,inputfile):
		'''
	Reads Nastran bdf-file (from Gmsh)
	into nodes and elements.
	'''
		try:
			fobj = open(inputfile, 'r')

		except OSError as e:
			print('\n\n  *** ERROR!!!', e)

		else:
			input_error = False
			line_number = 1

			current_element_number = 0
			two_line = False
			three_line = False

			for eachLine in fobj:
				line = [x.strip() for x in eachLine.split(',')]
				
				# building on element from last line
				if two_line:
					two_line = False
					if self.elements[current_element_number]['type'] == 'QUAD8N':
						self.elements[current_element_number]['nodes'] += [int(line[1]), int(line[2])]
						# shuffle nodes around
						reshuffle = [2, 5, 1, 4, 0, 7, 3, 6]
						self.elements[current_element_number]['nodes'] = [self.elements[current_element_number]['nodes'][x] for x in reshuffle]
						
					elif self.elements[current_element_number]['type'] == 'TET10N':
						self.elements[current_element_number]['nodes'] += [int(line[1]), int(line[2]), int(line[3]), int(line[4])]

					elif self.elements[current_element_number]['type'] == 'HEX8N':
						if len(line) == 3:
							self.elements[current_element_number]['type'] = 'HEX8N'
							self.elements[current_element_number]['nodes'] += [int(line[1]), int(line[2])]
						else:
							three_line = True
							self.elements[current_element_number]['nodes'] += [int(line[1]), int(line[2]), int(line[3]), int(line[4]),
																			   int(line[5]), int(line[6]), int(line[7]), int(line[8])]
					else:
						print('Element type:', self.elements[current_element_number]['type'], 'over 2 lines but not CQUAD8, CTETRA or CHEXA???')

				# building on element from last two lines
				elif three_line:
					three_line = False
					self.elements[current_element_number]['type'] = 'HEX20N'
					self.elements[current_element_number]['nodes'] += [int(line[1]), int(line[2]), int(line[3]),
																	   int(line[4]), int(line[5]), int(line[6])]
					
				elif line[0] == 'GRID':
					self.nodes[int(line[1])] = {'coord':[float(x) for x in line[3:]]}

				elif line[0] == 'CBAR':
					self.elements[int(line[1])] = {'type':	  'BEAM2N',
												   'section': None,
												   'nodes':	  [int(line[3]), int(line[4])]}
					if 'CBAR' not in self.elmTypes:
						self.elmTypes.append('CBAR')

				elif line[0] == 'CTRIA3':
					self.elements[int(line[1])] = {'type':	  'TRI3N',
												   'section': None,
												   'nodes':   [int(line[5]), int(line[4]), int(line[3])]}
					if 'CTRIA3' not in self.elmTypes:
						self.elmTypes.append('CTRIA3')

				elif line[0] == 'CTRIA6':
					self.elements[int(line[1])] = {'type':	  'TRI6N',
												   'section': None,
												   'nodes':   [int(line[8]), int(line[7]), int(line[6]),
											  				   int(line[5]), int(line[4]), int(line[3])]}
					if 'CTRIA6' not in self.elmTypes:
						self.elmTypes.append('CTRIA6')

				elif line[0] == 'CQUAD4':
					self.elements[int(line[1])] = {'type':    'QUAD4N',
												   'section': None,
												   'nodes':   [int(line[6]), int(line[5]), int(line[4]), int(line[3])]}
					if 'CQUAD4' not in self.elmTypes:
						self.elmTypes.append('CQUAD4')

				elif line[0] == 'CQUAD8':
					self.elements[int(line[1])] = {'type':    'QUAD8N',
												   'section': None,
												   'nodes':   [int(line[3]), int(line[4]), int(line[5]),
												   			   int(line[6]), int(line[7]), int(line[8])]}
					two_line = True
					current_element_number = int(line[1])
					if 'CQUAD8' not in self.elmTypes:
						self.elmTypes.append('CQUAD8')

				elif line[0] == 'CTETRA':
					if len(line) == 7:
						self.elements[int(line[1])] = {'type':    'TET4N',
													   'section': None,
													   'nodes':   [int(line[3]), int(line[4]), int(line[5]), int(line[6])]}
					else:
						self.elements[int(line[1])] = {'type':    'TET10N',
													   'section': None,
													   'nodes':   [int(line[3]), int(line[4]), int(line[5]), 
																   int(line[6]), int(line[7]), int(line[8])]}
						two_line = True
						current_element_number = int(line[1])
					if 'CTETRA' not in self.elmTypes:
						self.elmTypes.append('CTETRA')

				elif line[0] == 'CHEXA':
					self.elements[int(line[1])] = {'type':	  'HEX8N',
												   'section': None,
												   'nodes':   [int(line[3]), int(line[4]), int(line[5]), 
															   int(line[6]), int(line[7]), int(line[8])]}
					two_line = True
					current_element_number = int(line[1])
					if 'CHEXA' not in self.elmTypes:
						self.elmTypes.append('CHEXA')

				else:
					pass

				line_number +=1

			fobj.close()
			return input_error



	def readInp(self,inputfile):
		'''
	Reads Abaqus inp-file into nodes and elements.
	'''
		try:
			fobj = open(inputfile, 'r')

		except OSError as e:
			print('\n\n  *** ERROR!!!', e)

		else:
			input_error = False
			line_number = 1
			reading_nodes = False
			reading_elements = False
			element_type = 'None'
			two_line = False
			current_element_number = 0

			for eachLine in fobj:
				line = [x.strip() for x in eachLine.split(',')]

				if reading_nodes:
					if line[0][0] == '*':
						reading_nodes = False
					else:
						self.nodes[int(line[0])] = {'coord':[float(x) for x in line[1:]]}
						if len(self.nodes[int(line[0])]['coord']) == 2:
							self.nodes[int(line[0])]['coord'].append(0.0)

				if reading_elements:
					if line[0][0] == '*':
						reading_elements = False
					elif two_line:
						self.elements[current_element_number]['nodes'] += [int(line[0]),int(line[1]),int(line[2]),
																		   int(line[3]),int(line[4])]
						# shuffle nodes around
						reshuffle = [4,0,3,7,5,1,2,6,16,11,19,15,12,8,10,14,17,9,18,13]
						self.elements[current_element_number]['nodes'] = [self.elements[current_element_number]['nodes'][x] for x in reshuffle]
						two_line = False
					else:
						if element_type == 'ROD2N':
							self.elements[int(line[0])] = {'type':	  'ROD2N',
														   'section': None,
														   'nodes':   [int(line[1]), int(line[2])]}
						elif element_type == 'BEAM2N':
							self.elements[int(line[0])] = {'type':	  'BEAM2N',
														   'section': None,
														   'nodes':   [int(line[1]), int(line[2])]}
						elif element_type == 'TET4N':
							self.elements[int(line[0])] = {'type':	  'TET4N',
														   'section': None,
														   'nodes':   [int(line[1]), int(line[2]), int(line[3]), int(line[4])]}
						elif element_type == 'TET10N':
							self.elements[int(line[0])] = {'type':	  'TET10N',
														   'section': None,
														   'nodes':   [int(line[1]), int(line[2]), int(line[3]), int(line[4]), 
																	   int(line[5]), int(line[6]), int(line[7]), int(line[8]),
																	   int(line[9]), int(line[10])]}
						elif element_type == 'HEX8N':
							self.elements[int(line[0])] = {'type':	  'HEX8N',
														   'section': None,
														   'nodes':   [int(line[1]), int(line[2]), int(line[3]), int(line[4]), 
																	   int(line[5]), int(line[6]), int(line[7]), int(line[8])]}
						elif element_type == 'HEX20N':
							self.elements[int(line[0])] = {'type':	  'HEX20N',
														   'section': None,
														   'nodes':   [int(line[1]), int(line[2]), int(line[3]), int(line[4]), 
																	   int(line[5]), int(line[6]), int(line[7]), int(line[8]),
																	   int(line[9]), int(line[10]), int(line[11]), int(line[12]),
																	   int(line[13]), int(line[14]), int(line[15])]}
							two_line = True
							current_element_number = int(line[0])
						elif element_type == 'QUAD4N':
							self.elements[int(line[0])] = {'type':	  'QUAD4N',
														   'section': None,
														   'nodes':   [int(line[1]), int(line[2]), int(line[3]), int(line[4])]}
						elif element_type == 'QUAD8N':
							self.elements[int(line[0])] = {'type':	  'QUAD8N',
														   'section': None,
														   'nodes':   [int(line[1]), int(line[2]), int(line[3]), int(line[4]),
														   			   int(line[5]), int(line[6]), int(line[7]), int(line[8])]}
							# shuffle nodes around
							reshuffle = [6, 3, 7, 0, 4, 1, 5, 2]
							self.elements[int(line[0])]['nodes'] = [self.elements[int(line[0])]['nodes'][x] for x in reshuffle]
						elif element_type == 'TRI3N':
							self.elements[int(line[0])] = {'type':	  'TRI3N',
														   'section': None,
														   'nodes':   [int(line[1]), int(line[2]), int(line[3])]}
						elif element_type == 'TRI6N':
							self.elements[int(line[0])] = {'type':	  'TRI6N',
														   'section': None,
														   'nodes':   [int(line[1]), int(line[2]), int(line[3]),
														   			   int(line[4]), int(line[5]), int(line[6])]}
						else:
							pass

				if line[0] in ['*Node', '*NODE']:
					reading_nodes = True

				elif line[0] in ['*Element', '*ELEMENT']:
					reading_elements = True
					if 'type=T' in line[1]:
						element_type = 'ROD2N'
						if 'ROD2N' not in self.elmTypes:
							self.elmTypes.append('ROD2N')
					elif 'type=B' in line[1]:
						element_type = 'BEAM2N'
						if 'BEAM2N' not in self.elmTypes:
							self.elmTypes.append('BEAM2N')
					elif 'C3D4' in line[1]:
						element_type = 'TET4N'
						if 'TET4N' not in self.elmTypes:
							self.elmTypes.append('TET4N')
					elif 'C3D8' in line[1]:
						element_type = 'HEX8N'
						if 'HEX8N' not in self.elmTypes:
							self.elmTypes.append('HEX8N')
					elif 'C3D10' in line[1]:
						element_type = 'TET10N'
						if 'TET10N' not in self.elmTypes:
							self.elmTypes.append('TET10N')
					elif 'C3D20' in line[1]:
						element_type = 'HEX20N'
						if 'HEX20N' not in self.elmTypes:
							self.elmTypes.append('HEX20N')
					elif 'CPS4' in line[1]:
						element_type = 'QUAD4N'
						if 'QUAD4N' not in self.elmTypes:
							self.elmTypes.append('QUAD4N')
					elif 'CPS8' in line[1]:
						element_type = 'QUAD8N'
						if 'QUAD8N' not in self.elmTypes:
							self.elmTypes.append('QUAD8N')
					elif 'CPS3' in line[1]:
						element_type = 'TRI3N'
						if 'TRI3N' not in self.elmTypes:
							self.elmTypes.append('TRI3N')
					elif 'CPS6' in line[1]:
						element_type = 'TRI6N'
						if 'TRI6N' not in self.elmTypes:
							self.elmTypes.append('TRI6N')
					else:
						print('\n\tUnknown element type:', line[1])
						reading_elements = False

				else:
					pass

				line_number +=1

			fobj.close()
			return input_error



	def writeSol(self,filename):
		'''
	Writes *.sol file for nodes
	and elements.
	'''
		if len(self.elmTypes) == 1:
			pass
		elif len(self.elmTypes) == 2:
			for element in sorted(self.elements):
				if self.elements[element]['type'] == 'BEAM2N':
					del self.elements[element]
		else:
			for element in sorted(self.elements):
				if self.elements[element]['type'] in ['BEAM2N', 'TRI3N', 'TRI6N', 'QUAD4N', 'QUAD8N']:
					del self.elements[element]

		for node in sorted(self.nodes):
			self.nodes[node] = Node(node,self.nodes[node]['coord'][0],
										 self.nodes[node]['coord'][1],
										 self.nodes[node]['coord'][2])

		firstelement = 1
		newNumber = firstelement
		for element in sorted(self.elements):
			elmtype = self.elements[element]['type']
			self.elements[element] = Element(element,None,[self.nodes[x] for x in self.elements[element]['nodes']])
			self.elements[newNumber] = self.elements.pop(element)
			self.elements[newNumber].type = elmtype
			self.elements[newNumber].number = newNumber
			newNumber += 1

		firstnode = 1
		newNumber = firstnode
		for node in sorted(self.nodes):
			self.nodes[newNumber] = self.nodes.pop(node)
			self.nodes[newNumber].number = newNumber
			newNumber += 1



		if os.path.exists(filename+'.sol'):
			for i in range(len(filename)):
				if filename[-i-1] == '/' or filename[-i-1] == '\\':
					shortname = filename[-i:]
					break
			print('\n\t'+self.shortname[:-4]+'.sol already exists.\n\tOverwriting now...')

		fobj = open(filename+'.sol','w+')
		fobj.write('#\n#\n#\n')
		fobj.write('#    num            x               y              z\n')
		for node in self.nodes:
			fobj.write('NODE, '+str(self.nodes[node].number)+',\t%.9E, %.9E, %.9E' % \
							   (self.nodes[node].coord[0][0], \
								self.nodes[node].coord[1][0], \
								self.nodes[node].coord[2][0]))
			fobj.write('\n') 

		fobj.write('#\n#\n#\n')
		fobj.write('#        type  num  sect  nodes...\n')
		for element in self.elements:
			fobj.write('ELEMENT, '+ str(self.elements[element].type)+', '+ \
									str(self.elements[element].number)+', '+ \
									str(self.elements[element].section)+', ')
			for i in range(len(self.elements[element].nodes)-1):
				fobj.write(str(self.elements[element].nodes[i].number)+', ')
			fobj.write(str(self.elements[element].nodes[-1].number)+'\n')
		fobj.write('#\n#\n#')
		fobj.close()





if __name__ == '__main__':

	print('\n\n\tFinite Element Inputfile Converter')
	print('\t----------------------------------\n')
	print('\tThis script takes an Nastran mesh file (*.bdf) exported')
	print('\tfrom the program gmsh, and converts it to a *.sol file')
	print('\tto be imported in viewFEM.')

	fname = input('\n\n\tbdf-file: ')
	if fname[-4:] == '.bdf':
		mesh = ConvertMesh(fname)
		mesh.writeSol(fname[:-4])
	else:
		print('\n\tThat is not a *.bdf file.')




