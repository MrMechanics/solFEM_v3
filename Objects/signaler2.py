#
#
#	signaler.py
#	-----------
#
#	This file holds functions used for
#	digital signal processing which is
#	sometimes usefull when doing modal
#	dynamic analysis
#
#


import numpy as np
from random import random
from math import sqrt, cos, sin, atan, log





def fwdDFT(x):
	'''
the Discrete Fourier Transform
'''
	pi = 3.141592653589793

	N = len(x)
	ReX = [0]*(N/2+1)
	ImX = [0]*(N/2+1)
	MagX = []
	PhaseX = []

	# Calculate ReX[] and ImX[]
	for k in range(N/2+1):
		for j in range(N):
			ReX[k] = ReX[k] + x[j] * cos(2*pi*k*j/N)
			ImX[k] = ImX[k] - x[j] * sin(2*pi*k*j/N)

	# Calculate MagX[] and PhaseX[]
	for k in range(N/2+1):
		MagX.append(sqrt(ReX[k]**2 + ImX[k]**2))
		# Prevent divide by zero error
		if ReX[k] == 0:
			ReX[k] = 1.0e-20
		PhaseX.append( (atan(ImX[k]/ReX[k])/(2*pi))*360 )
		# Correct incorrect arctan values
		if ReX[k] < 0 and ImX[k] < 0:
			PhaseX[k] -= 180
		if ReX[k] < 0 and ImX[k] >= 0:
			PhaseX[k] += 180

	return [ReX, ImX, MagX, PhaseX]





def invDFT(ReX, ImX):
	'''
the Inverse Discrete Fourier Transform
'''
	pi = 3.141592653589793
	
	if len(ReX) != len(ImX):
		print('ReX and ImX must be of the same size')
	else:
		N = (len(ReX)-1)*2
		x = [0]*N

		for k in range((N/2)+1):
			ReX[k] = ReX[k]/(N/2)
			ImX[k] = ImX[k]/(N/2)

		ReX[0] = ReX[0]/2
		ReX[N/2] = ReX[N/2]/2

		for j in range(N):
			for i in range((N/2)+1):
				x[j] = x[j] + ReX[i] * cos(2*pi*i*j/N)
				x[j] = x[j] + ImX[i] * sin(2*pi*i*j/N)

		# Need to flip the values between x[1] and x[N]
		# for some reason. Don't know why!!!
		y = x[1:N]
		y_flipped = y[::-1]
		x_first = x[0]
		x = []
		x.append(x_first)
		for j in range(N-1):
			x.append(y_flipped[j])

		return x





def complexFFT(x):
	'''
the Fast Fourier Transform with complex numbers
'''
	pi = 3.141592653589793
	N = len(x)
	if N <= 1: return x
	even = complexFFT(x[0::2])
	odd  = complexFFT(x[1::2])
	return [even[k] + np.exp(-2j*pi*k/N)*odd[k] for k in range(int(N/2))] + \
		   [even[k] - np.exp(-2j*pi*k/N)*odd[k] for k in range(int(N/2))]





def fwdFFT(x):
	'''
the Fast Fourier Transform
'''
	pi = 3.141592653589793

	# Check length of signal x
	N = 0
	for i in range(20):
		if len(x) > 2**i:
			continue
		elif len(x) < 2**i:
			N = 2**i
			break
		else:
			N = len(x)
			break

	# Convert time signal to combination of ReX and ImX and augment
	# the signal with zeros to get number of samples in power of two
	cx = []
	for i in range(N):
		if len(x) > i:
			cx.append(complex(x[i]))
		else:
			cx.append(0.0)

	# Fast Fourier Transform
	X = complexFFT(cx)
	
	# Put values into ReX and ImX
	ReX = []
	ImX = []
	for i in range(N):
		ReX.append(X[i].real)
		ImX.append(X[i].imag)

	# Calculate MagX[] and PhaseX[]
	MagX = []
	PhaseX = []
	for k in range(int(N/2)):
		MagX.append(sqrt(ReX[k]**2 + ImX[k]**2))
		# Prevent divide by zero error
		if ReX[k] == 0:
			ReX[k] = 1.0e-20
		PhaseX.append( (atan(ImX[k]/ReX[k])/(2*pi))*360 )
		# Correct incorrect arctan values
		if ReX[k] < 0 and ImX[k] < 0:
			PhaseX[k] -= 180
		if ReX[k] < 0 and ImX[k] >= 0:
			PhaseX[k] += 180

	return [X, ReX, ImX, MagX, PhaseX]





def invFFT(ReX,ImX):
	'''
the Inverse Fast Fourier Transform
'''
	N = len(ReX)
	for i in range(N):
		ImX[i] = -ImX[i]

	X = []
	for k in range(N):
		X.append(complex(ReX[k] + 1j*ImX[k]))

	x = fwdFFT(X)

	for l in range(N):
		x[1][l] = x[1][l]/N
		x[2][l] = -x[2][l]/N
		x[0][l] = complex(x[1][l] + 1j*x[2][l])

	return [x[0], x[1], x[2]]





def fwdPSD(MagX,f):
	'''
generate PSD from DFT, over frequency spectrum f
'''
	N = 2*len(MagX)
	df = float(f)/len(MagX)

	# Modify MagX values
	MagX[0] = MagX[0]/sqrt(2)
	MagX[(N/2)-1] = MagX[(N/2)-1]/sqrt(2)
	
	PSD = []
	f = [df]
	for i in range(N/2):
		PSD.append((1/df)*(1.0/N)*(2.0/N)*(MagX[i]**2))
		if i == 0:
			pass
		else:
			f.append(f[i-1] + df)

	return [PSD,f]





def invPSD(PSD,f):
	'''
generate time signal from PSD with uniform random
distribution of phase angles
'''
	pi = 3.141592653589793
	N = 2*len(PSD)
	df = float(f)/len(PSD)
	dt = 1.0/(2*f)
	MagX = []
	PhaseX = []
	ReX = []
	ImX = []
	X = []

	# Generate MagX
	for i in range(N/2):
		MagX.append(2*sqrt((df/2)*(N**2)*PSD[i]))
	MagX[0] = MagX[0]*sqrt(2)
	MagX[(N/2)-1] = MagX[(N/2)-1]*sqrt(2)
	for j in range(N/2):
		MagX.append(MagX[-j-1])
	
	# Generate PhaseX
	for i in range(N/2):					# Uniform random distribution
		PhaseX.append((random()*180)-90)	# between 0 and 180 degrees
	for j in range(N/2):
		PhaseX.append(-PhaseX[-j-1])

	# Generate ReX and ImX
	for k in range(N):
		X.append(complex(MagX[k]*np.exp(1j*PhaseX[k])))
		ReX.append(X[k].real)
		ImX.append(X[k].imag)

	x = invFFT(ReX,ImX)

	t = [dt]
	for i in range(1,N):
		t.append(t[i-1]+dt)

	return [t,x[1]]





def multiplyDFT(MagX1,MagX2,PhaseX1=[0],PhaseX2=[0]):
	'''
Multiply one DFT with another
'''
	N = len(MagX1)
	if (len(MagX1) != len(MagX2)) or (len(PhaseX1) != len(PhaseX2)):
		print('DFT 1 is not same size as DFT 2, cannot multiply')
	else:
		MagX = []
		PhaseX = []
		for i in range(N):
			MagX.append(MagX1[i]*MagX2[i])
		if len(PhaseX1) == N:
			for i in range(N):
				PhaseX.append(PhaseX1[i]+PhaseX2[i])
		else:
			PhaseX = [0]

	return [MagX,PhaseX]





def divideDFT(MagX1,MagX2,PhaseX1=0,PhaseX2=0):
	'''
Divide one DFT with another
'''
	N = len(MagX1)
	if (len(MagX1) != len(MagX2)) or (len(PhaseX1) != len(PhaseX2)):
		print('DFT 1 is not same size as DFT 2, cannot divide')
	else:
		MagX = []
		PhaseX = []
		for i in range(N):
			# Prevent divide by zero error
			if MagX2[i] == 0:
				MagX2[i] = 1E-16
			MagX.append(MagX1[i]/MagX2[i])
		if len(PhaseX1) == N:
			for i in range(N):
				PhaseX.append(PhaseX1[i]-PhaseX2[i])
		else:
			PhaseX = 0

	return [MagX,PhaseX]





def rmsDFT(MagX):
	'''
Perseval's relation for calculating the rms of a DFT
'''
	N = 2*len(MagX)-2

	# Copy MagX into X
	X = [0]*len(MagX)
	for i in range((N/2)+1):
		X[i] += MagX[i]

	# Modify MagX values
	X[0] = X[0]/sqrt(2)
	X[N/2] = X[N/2]/sqrt(2)

	# Sum up	
	perseval_sum = 0
	for i in range(N/2):
		perseval_sum += (2.0/N)*X[i]**2
	
	# Calculate RMS
	rms = sqrt((1.0/N)*perseval_sum)

	return rms





def avgDFT(x):
	'''
Filter out noise from DFT by sampling signal M times and
calculating the average DFT from all samples
'''
	print('\noriginal signal consists of', len(x), 'sample points')
	N = int(raw_input("""
number of points for each sampling 
of the original signal: """))

	while True:
		if N > len(x)/2:
			N = int(raw_input("""
number of points for each sampling 
of the original signal must be smaller 
than half the number of points in the 
original signal. 
Please choose another number: """))

		else:
			break
		
	M = int((len(x)/N))-1
	D = float(len(x)-M*N)/float(M)
	x_n = []
	for i in range(M):
		x_n.append([])
		for j in range(N):
			x_n[i].append(x[int((i+1)*D)+i*N+j])
	print('\nsignal sampled', M, 'times with', N, 'points in each sample')

	print('calculating DFT for all M =', M, 'samples...')
	X_n = []	
	for i in range(M):
		X_n.append([])
		X_n[i] = fwdFFT(x_n[i])
		print((i+1), '<>',)
	
	print('\n\ncalculating rms of DFT for all M =', M, 'samples...')
	X_rms = [0]*M
	for k in range(M):
		X_rms[k] = rmsDFT(X_n[k][3])
		print(X_rms[k], '<>',)

	# calculate the avgDFT
	R = int(raw_input("""\n\nhaving seen the rms values of every DFT,
how many of them would you like to remove
from the avgDFT? It must be an even number,
e.g. 0,2,4,6... Choosing 2 will remove the
first and last DFT, 4 will remove the
2 first and 2 last DFTs.   """))
	while R > M/2:
		R = int(raw_input("""you cannot remove more than there are available,
please choose another number: """))

	X_n.append([0]*(N/2))
	L = len(X_n[0][3])
	for j in range((R/2),M-(R/2)):
		for k in range(L):
			X_n[M][k] += (X_n[j][3][k])
	for i in range(L):
		X_n[M][i] = X_n[M][i]/(M-R)

	# calculate the rms of the avgDFT
	X_rms.append(rmsDFT(X_n[M]))
	print('\nrms of avgDFT:', X_rms[M])

	return [x_n, X_n, X_rms]




