#
#
#	tables.py
#  --------------
#
#	This file holds the table objects. These are applied to
#	solution objects which use the xy-data information as
#	input in the analysis. Table objects are created by
#	reading x-y data from *.tab-files.
#


import matplotlib.pyplot as plt
import numpy as np
import os





class Table(object):
	'''
Base class for tables.
'''
	def __init__(self,number,fname):
		self.number = number
		self.filename = fname


	def readFile(self):
		'''
	Reads the x-y data from file to
	Table object. Also checks if file
	exists, and if it is the right
	format.
	'''
		datay = []
		datax = []
		try:
			fobj = open(self.filename, 'r')

		except(OSError, e):
			print('*** file open error:', e)

		else:
			line_number = 1
			for eachLine in fobj:
				tmpStr = ''
				k = 0
				if eachLine[0] == '#' or eachLine == '\n':
					line_number += 1
					pass
				else:
					for i in eachLine:
						if i == ' ':
							pass
						elif i == ',':
							if k == 0:
								datay.append(float(tmpStr))
								tmpStr = ''
							else:
								print('\nINPUT ERROR on line', line_number, 'in file:', self.filename)
							k += 1
						elif i == '\n':
							datax.append(float(tmpStr))
							break
						else:
							tmpStr += i
					line_number += 1
			fobj.close()
		return [datay, datax]


	def writeToFile(self,fname):
		'''
	Writes data to file in a format that
	is easy to read and plot elsewhere if
	needed.
	'''
		if os.path.exists(fname):
			print('file with that name already exists')
		else:
			fobj = open(fname, 'w')
			for i in range(len(data)):
				fobj.write(str(data[i][0]) + ', ' + str(data[i][1]) + '\n')
			fobj.close()




class AccelTable(Table):
	'''
Acceleration table used for dynamic
basemotion applied to boundary
constraints.
'''
	def __init__(self,number,fname,bound):
		self.boundary = bound
		super(AccelTable,self).__init__(number,fname)
		[self.accel, self.time] = self.readFile()




class ForceTable(Table):
	'''
ForceDynamic table used for dynamic
force loads applied to specified
nodes.
'''
	def __init__(self,number,fname,load):
		self.load = load
		super(ForceTable,self).__init__(number,fname)
		[self.force, self.time] = self.readFile()




class StressStrainTable(Table):
	'''
Stress/Strain table for use with
non-linear analysis with plasticity
in materials.
'''
	def __init__(self,number,fname,material):
		self.material = material
		super(StressStrainTable,self).__init__(number,fname)
		[self.stress, self.strain] = self.readFile()




class DampingTable(Table):
	'''
DampingRatio table for use with
ModalDynamic analysis with damping,
where the damping changes depending
on frequency.
'''
	def __init__(self,number,fname,damping):
		self.damping = damping
		super(DampingTable,self).__init__(number,fname)
		[self.dampRatio, self.frequency] = self.readFile()









