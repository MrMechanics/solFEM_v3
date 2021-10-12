#
#
#	script for converting mesh-file
#	from other formats into *.sol 
#	file for viewFEM to use
#


import time
import os
import nodes
import elements



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
		if filetype == '.dat':
			self.input_error = self.readDat(inputfile)
		if filetype == '.bdf':
			self.input_error = self.readBdf(inputfile)
		read_file_stop = time.time()
		self.read_time = read_file_stop - read_file_start
		print('%.3f seconds\n' % (self.read_time))
		print('\tNumber of nodes in mesh: '+str(len(self.nodes)))
		print('\tNumber of elements in mesh: '+str(len(self.elements)))



	def readBdf(self,inputfile):
		'''
	Reads bdf-file from Gmsh into nodes
	and elements.
	'''
		try:
			fobj = open(inputfile, 'r')

		except OSError as e:
			print('\n\n  *** ERROR!!!', e)

		else:
			input_error = False
			line_number = 1

			tmpNode = []
			tmpElm = []
			elmType = ''
			tmpStr = ''
			two_line = False
			three_line = False

			for eachLine in fobj:
				if two_line:
					two_line = False
					tmpStr = ''
					k = 0
					for i in eachLine:
						if i == ',':
							if k == 0:
								tmpStr = ''
							elif k < 8:
								tmpElm.append(int(tmpStr))
								tmpStr = ''
							elif k == 8:
								tmpElm.append(int(tmpStr))
								three_line = True
							else:
								tmpStr = ''
							k += 1
						elif i == '\n':
							if k < 8:
								tmpElm.append(int(tmpStr))
							break
						else:
							tmpStr += i
					if three_line == False:
						if elmType == 'QUAD':
							elmType = 'QUAD8N'
							self.elements[tmpElm[0]] = {'type':elmType,
														'section':tmpElm[1],
														'nodes':[tmpElm[4], tmpElm[7], tmpElm[3], tmpElm[6],
																 tmpElm[2], tmpElm[9], tmpElm[5], tmpElm[8]]}
						elif elmType == 'TET':
							elmType = 'TET10N'
							self.elements[tmpElm[0]] = {'type':elmType,
														'section':tmpElm[1],
														'nodes':tmpElm[2:]}
						elif elmType == 'HEX':
							elmType = 'HEX8N'
							self.elements[tmpElm[0]] = {'type':elmType,
														'section':tmpElm[1],
														'nodes':[tmpElm[3], tmpElm[7], tmpElm[8], tmpElm[4],
																 tmpElm[2], tmpElm[6], tmpElm[9], tmpElm[5]]}
						else:
							print('Element type:', elmType, 'over 2 lines but not CQUAD8, CTETRA or CHEXA???')
						if elmType not in self.elmTypes:
							self.elmTypes.append(elmType)

				elif three_line:
					three_line = False
					tmpStr = ''
					k = 0
					for i in eachLine:
						if i == ',':
							if k == 0:
								tmpStr = ''
							else:
								tmpElm.append(int(tmpStr))
								tmpStr = ''
							k += 1
						elif i == '\n':
							if k < 8:
								tmpElm.append(int(tmpStr))
							break
						else:
							tmpStr += i
					self.elements[tmpElm[0]] = {'type':'HEX20N',
												'section':tmpElm[1],
												'nodes':[tmpElm[ 3], tmpElm[ 7], tmpElm[ 8], tmpElm[ 4], tmpElm[ 2],
														 tmpElm[ 6], tmpElm[ 9], tmpElm[ 5], tmpElm[15], tmpElm[19], 
														 tmpElm[16], tmpElm[11], tmpElm[10], tmpElm[18], tmpElm[20], 
														 tmpElm[12], tmpElm[14], tmpElm[21], tmpElm[17], tmpElm[13]]}
					if elmType not in self.elmTypes:
						self.elmTypes.append(elmType)

					
				elif eachLine[:4] == 'GRID':
					tmpNode = []
					tmpStr = ''
					k = 0
					for i in eachLine:
						if i == ',':
							if k == 1:
								tmpNode.append(int(tmpStr))
								tmpStr = ''
							elif k > 2:
								tmpNode.append(float(tmpStr))
								tmpStr = ''
							else:
								tmpStr = ''
							k += 1
						elif i == '\n':
							tmpNode.append(float(tmpStr))
							break
						else:
							tmpStr += i
					self.nodes[tmpNode[0]] = {'coord':tmpNode[1:]}

				elif eachLine[:5] == 'CTRIA':
					tmpElm = []
					tmpStr = ''
					k = 0
					for i in eachLine:
						if i == ',':
							if k == 0:
								tmpStr = ''
							elif k < 9:
								tmpElm.append(int(tmpStr))
								tmpStr = ''
							else:
								tmpStr = ''
							k += 1
						elif i == '\n':
							if k < 9:
								tmpElm.append(int(tmpStr))
							break
						else:
							tmpStr += i
					if len(tmpElm) == 5:
						elmType = 'TRI3N'
						self.elements[tmpElm[0]] = {'type':elmType,
													'section':tmpElm[1],
													'nodes':[tmpElm[2], tmpElm[4], tmpElm[3]]}
					else:
						elmType = 'TRI6N'
						self.elements[tmpElm[0]] = {'type':elmType,
													'section':tmpElm[1],
													'nodes':[tmpElm[2], tmpElm[4], tmpElm[3],
															 tmpElm[7], tmpElm[6], tmpElm[5]]}
					if elmType not in self.elmTypes:
						self.elmTypes.append(elmType)

				elif eachLine[:5] == 'CQUAD':
					elmType = 'QUAD'
					tmpElm = []
					tmpStr = ''
					k = 0
					for i in eachLine:
						if i == ',':
							if k == 0:
								tmpStr = ''
							elif k < 8:
								tmpElm.append(int(tmpStr))
								tmpStr = ''
							elif k == 8:
								tmpElm.append(int(tmpStr))
								two_line = True
							else:
								tmpStr = ''
							k += 1
						elif i == '\n':
							if k < 8:
								tmpElm.append(int(tmpStr))
							break
						else:
							tmpStr += i
					if not two_line:
						self.elements[tmpElm[0]] = {'type':'QUAD4N',
													'section':tmpElm[1],
													'nodes':[tmpElm[4], tmpElm[3], tmpElm[2], tmpElm[5]]}
						if elmType not in self.elmTypes:
							self.elmTypes.append(elmType)

				elif eachLine[:6] == 'CTETRA':
					elmType = 'TET'
					tmpElm = []
					tmpStr = ''
					k = 0
					for i in eachLine:
						if i == ',':
							if k == 0:
								tmpStr = ''
							elif k < 8:
								tmpElm.append(int(tmpStr))
								tmpStr = ''
							elif k == 8:
								tmpElm.append(int(tmpStr))
								two_line = True
							else:
								tmpStr = ''
							k += 1
						elif i == '\n':
							if k < 8:
								tmpElm.append(int(tmpStr))
							break
						else:
							tmpStr += i
					if not two_line:
						self.elements[tmpElm[0]] = {'type':'TET4N',
													'section':tmpElm[1],
													'nodes':tmpElm[2:]}
						if elmType not in self.elmTypes:
							self.elmTypes.append(elmType)

				elif eachLine[:5] == 'CHEXA':
					elmType = 'HEX'
					tmpElm = []
					tmpStr = ''
					k = 0
					for i in eachLine:
						if i == ',':
							if k == 0:
								tmpStr = ''
							elif k < 8:
								tmpElm.append(int(tmpStr))
								tmpStr = ''
							elif k == 8:
								tmpElm.append(int(tmpStr))
								two_line = True
							else:
								tmpStr = ''
							k += 1
						elif i == '\n':
							if k < 8:
								tmpElm.append(int(tmpStr))
							break
						else:
							tmpStr += i
				else:
					pass

				line_number +=1

			fobj.close()
			return input_error



	def readDat(self,inputfile):
		'''
	Reads dat-file from freeCAD into nodes
	and elements.
	'''
		try:
			fobj = open(inputfile, 'r')

		except OSError as e:
			print('\n\n  *** ERROR!!!', e)

		else:
			input_error = False
			self.elmTypes.append('TET10N')
			line_number = 1

			for eachLine in fobj:

				if(eachLine.count(' ') == 3):
					tmpNode = []
					tmpStr = ''
					k = 0
					for i in eachLine:
						if i == ' ':
							if k == 0:
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

				elif(eachLine.count(' ') == 12):
					tmpElm = []
					tmpStr = ''
					k = 0
					for i in eachLine:
						if i == ' ':
							tmpElm.append(int(tmpStr))
							tmpStr = ''
						elif i == '\n':
							break
						else:
							tmpStr += i
					self.elements[tmpElm[0]] = {'type':'TET10N',
												'section':tmpElm[1],
												'nodes':tmpElm[2:]}

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
#		firstnode = raw_input('\n\tNode numbers start at: ')
#		gotInput = False
#		while gotInput == False:
#			if int(firstnode):
#				firstnode = int(firstnode)
#				gotInput = True
#			else:
#				print '\n\tThat is not a valid node number, try again.'
#				firstnode = raw_input('\tNode numbers should start at: ')
		firstnode = 1

		newNumber = firstnode
		for node in sorted(self.nodes):
			self.nodes[newNumber] = self.nodes.pop(node)
			for element in self.elements:
				for node_num in range(len(self.elements[element]['nodes'])):
					if self.elements[element]['nodes'][node_num] == node:
						self.elements[element]['nodes'][node_num] = newNumber
			newNumber += 1

		if len(self.elmTypes) == 1:
			pass
		else:
			for element in sorted(self.elements):
				if self.elements[element]['type'] in ['TRI3N', 'TRI6N', 'QUAD4N', 'QUAD8N']:
					del self.elements[element]

#		firstelement = raw_input('\tElement numbers start at: ')
#		gotInput = False
#		while gotInput == False:
#			if int(firstelement):
#				firstelement = int(firstelement)
#				gotInput = True
#			else:
#				print '\n\tThat is not a valid element number, try again.'
#				firstelement = raw_input('\tElement numbers should start at: ')
		firstelement = 1

		newNumber = firstelement
		for element in sorted(self.elements):
			self.elements[newNumber] = self.elements.pop(element)
			newNumber += 1

		if os.path.exists(filename+'.sol'):
			for i in range(len(filename)):
				if filename[-i-1] == '/' or filename[-i-1] == '\\':
					shortname = filename[-i:]
					break
			print('\n\t'+self.shortname[:-4]+'.sol already exists.\n\tOverwriting now...')

		fobj = open(filename+'.sol','w+')
		fobj.write('#\n#\n#\n')
#		fobj.write('#       num         x               y              z\n')
		for node in self.nodes:
			fobj.write('NODE, '+str(node)+',\t%.9E, %.9E, %.9E' % \
							   (self.nodes[node]['coord'][0], \
								self.nodes[node]['coord'][1], \
								self.nodes[node]['coord'][2]))
			fobj.write('\n') 

		fobj.write('#\n#\n#\n')
#		fobj.write('#         type    num    sect    nodes...\n')
		for element in self.elements:
			fobj.write('ELEMENT, '+ str(self.elements[element]['type'])+', '+ \
									str(element)+', '+ \
									str(self.elements[element]['section'])+', ')
			for i in range(len(self.elements[element]['nodes'])-1):
				fobj.write(str(self.elements[element]['nodes'][i])+', ')
			fobj.write(str(self.elements[element]['nodes'][-1])+'\n')
		fobj.write('#\n#\n#')
		fobj.close()





if __name__ == '__main__':

	print('\n\n\tFinite Element Inputfile Converter')
	print('\t----------------------------------\n')
	print('\tThis script takes an input mesh file (*.bdf) exported from')
	print('\tthe program gmsh, and converts it to a *.sol file to be')
	print('\timported in viewFEM.')

	fname = input('\n\n\tbdf-file: ')
	if fname[-4:] == '.bdf':
		mesh = ConvertMesh(fname)
		mesh.writeSol(fname[:-4])
	else:
		print('\n\tThat is not a *.bdf file.')




