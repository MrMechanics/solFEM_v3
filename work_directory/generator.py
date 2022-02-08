#
#	script used to generate
#	sinusoidal signals for use
#	as input in analysis
#
#	modify t and x as you want
#	and run script to generate
#	tab file which can be used
#	in analysis.
#


import matplotlib.pyplot as plt
import os
import numpy as np



def toFile(x,t,fname,description):
#	fname = raw_input('filename: ')
	if os.path.exists(fname):
		print('Overwriting existing file:', fname)
	else:
		print('Writing to file:', fname)
	fobj = open(fname, 'w')
	fobj.write('#\n#\n#\t'+description+'\n#\n#\n')
	n = len(x)
	for i in range(n):
		fobj.write(str(x[i]) + ', ' + str(t[i]) + '\n')
	fobj.close()


def fromFile(fname):

	data = []
	try:
		fobj = open(fname, 'r')

	except OSError as e:
		print('*** file open error:', e)

	else:
		line_number = 1
		for eachLine in fobj:
			tmpNum = []
			tmpStr = ''
			k = 0
			for i in eachLine:
				if i == ' ':
					pass
				elif i == ',':
					if k == 0:
						tmpNum.append(float(tmpStr))
						tmpStr = ''
					else:
						print('\nINPUT ERROR on line: ', line_number)
					k += 1
				elif i == '\n':
					tmpNum.append(float(tmpStr))
					break
				else:
					tmpStr += i
			data.append(tmpNum)
			line_number += 1
		fobj.close()
	return data




if __name__ == '__main__':

	time = 12.
	t = np.arange(0., time, 0.001)

	x = np.sin(1.7*2*np.pi*t)
	x[2900:] = 0.
	
	plt.plot(t,x,'r')
	plt.show()

	toFile(x,t,'tutorial_11-base_motion.tab','base acceleration for tutorial 11')





