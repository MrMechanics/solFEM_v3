#
# Quaternion class for mathmatics
# using quaternions
#



import numpy as np



def normalize(v, tolerance=0.00001):
	'''
Normalizes vector v to a unit vector.
'''
	mag2 = sum(n * n for n in v)
	if abs(mag2 - 1.0) > tolerance:
		mag = np.sqrt(mag2)
		v = tuple(n / mag for n in v)
	return v


def rotatePointAboutAxis(point,axis0,axis1,angle):
	'''
First moves point, axis0 and axis1
together so that axis0 is at the
origin. Then creates the two
quaternions and rotates the point
about the arbitrary axis defined
by axis0 and axis1. Finally
moves the point back so that axis0
is at its original position again. 
'''
	axis1_0 = [axis1[0]-axis0[0], axis1[1]-axis0[1], axis1[2]-axis0[2]]
	point_0 = [point[0]-axis0[0], point[1]-axis0[1], point[2]-axis0[2]]
#	angle = np.pi*angle/180.

	qPnt0 = Quaternion()
	qPnt0.vectorToQuat(point_0)
#	print("Point_0 quaternion:")
#	qPnt0.printQuat()

	qRot = Quaternion()
	qRot.axisAngleToQuat(normalize(axis1_0),angle)
	qPnt1 = qRot.multi(qPnt0.multi(qRot.conj()))
#	print("Point_1 quaternion:")
#	qPnt1.printQuat()

	return [qPnt1.i+axis0[0], qPnt1.j+axis0[1], qPnt1.k+axis0[2]]


def getAngleBetweenThreePoints(origin,point1,point2):
	'''
Creates two vectors and finds the
angles between them using quaternions
'''

	return angle


class Quaternion(object):
	'''
A quaternion object, with
the option to add, subtract
and multiply with other
quaternions.
'''
	def __init__(self, array = [0.0,0.0,0.0,0.0]):
		'''
	Initialize the quaternion
	object with the r, i, j and
	k values specified.
	'''
		self.r = array[0]
		self.i = array[1]
		self.j = array[2]
		self.k = array[3]


	def printQuat(self):
		'''
	Prints out the quaternion in
	standard format (and with
	angles?).
	'''
		print(str("%.3f" % self.r) + " " + \
			  str("%.3f" % self.i) + "i " + \
			  str("%.3f" % self.j) + "j " + \
			  str("%.3f" % self.k) + "k")


	def add(self, quat):
		'''
	Add to another quaternion and
	return the result.
	'''
		return Quaternion([self.r + quat.r,
						   self.i + quat.i,
						   self.j + quat.j,
						   self.k + quat.k])


	def sub(self, quat):
		'''
	Subtract from another quaternion
	and return the result.
	'''
		return Quaternion([self.r - quat.r,
						   self.i - quat.i,
						   self.j - quat.j,
						   self.k - quat.k])


	def scale(self, scalar):
		'''
	Multiply quaternion with scalar
	and return the result.
	'''
		return Quaternion([self.r * scalar,
						   self.i * scalar,
						   self.j * scalar,
						   self.k * scalar])


	def multi(self, quat):
		'''
	Multiply with another quaternion
	and return the result.
	'''
		return Quaternion([self.r*quat.r - self.i*quat.i - self.j*quat.j - self.k*quat.k,
						   self.r*quat.i + self.i*quat.r + self.j*quat.k - self.k*quat.j,
						   self.r*quat.j - self.i*quat.k + self.j*quat.r + self.k*quat.i,
						   self.r*quat.k + self.i*quat.j - self.j*quat.i + self.k*quat.r])


	def conj(self):
		'''
	Gives the conjugate of the
	quaternion.
	'''
		conjQuat = Quaternion([ self.r, -self.i, -self.j, -self.k])
		return conjQuat


	def inv(self):
		'''
	Invert quaternion.
	'''
		if (self.r == self.i == self.j == self.k == 0):
			print("Zero Quaternion has no inverse")
		else:
			scl = 1.0 / (self.r**2 + self.i**2 + self.j**2 + self.k**2)

			invQuat = Quaternion([ self.r * scl,
								  -self.i * scl,
								  -self.j * scl,
								  -self.k * scl])
			return invQuat


	def norm(self):
		'''
	Gives the norm of the quaternion.
	'''
		return np.sqrt(self.r**2 + self.i**2 + self.j**2 + self.k**2)


	def unit(self):
		'''
	Gives the unit quaternion (versor).
	'''
		if (self.r == self.i == self.j == self.k == 0):
			print("Zero Quaternion has no versor")
		else:
			norm = self.norm()
			return Quaternion([self.r / norm,
							   self.i / norm,
							   self.j / norm,
							   self.k / norm])


	def recip(self):
		'''
	Gives the reciprocal of
	quaternion.
	'''
		if (self.r == self.i == self.j == self.k == 0):
			print("Zero Quaternion has no reciprocal")
		else:
			return self.conj().scale(1.0/(self.norm()**2))


	def vectorToQuat(self, v):
		'''
	Converts quaternion to a vector
	quaternion with the same values
	as vector v.	
	'''
		self.r = 0.
		self.i = v[0]
		self.j = v[1]
		self.k = v[2]


	def axisAngleToQuat(self, rAx, rAng):
		'''
	Converts quaternion to a rotation
	quaternion with axis vAx and angle
	rAng (in radians).
	'''
		norm = np.sqrt(rAx[0]**2 + rAx[1]**2 + rAx[2]**2)
		v_norm = [rAx[0]/norm, rAx[1]/norm, rAx[2]/norm]
		theta = rAng/2

		self.r = np.cos(theta)
		self.i = rAx[0]*np.sin(theta)
		self.j = rAx[1]*np.sin(theta)
		self.k = rAx[2]*np.sin(theta)
		

	def quatToAxisAngle(self):
		'''
	Gives the Axis and Angle of
	rotation quaternion.
	'''
		rAx = [self.i, self.j, self.k]
		rAng = np.arccos(self.r)*2
		return rAx, rAng



if __name__ == '__main__':


	v0 = [1./np.sqrt(3), 1./np.sqrt(3), 1./np.sqrt(3)]

	rAx1 = [1., 0., 0.]			# rotate around x-axis
	rAng1 = np.pi/4				# 45 degrees in radians

	rAx2 = [0., 1., 0.]			# rotate around y-axis
	rAng2 = np.pi				# 180 degrees in radians

	rAx3 = [0., 0., 1.]			# rotate around z-axis
	rAng3 = np.pi/2				# 90 degrees in radians

	q0 = Quaternion()
	q0.vectorToQuat(v0)

	qr1 = Quaternion()
	qr1.axisAngleToQuat(rAx1, rAng1)
	q1 = qr1.multi(q0.multi(qr1.conj()))

	print("Start vector:\n"), q0.printQuat()
	print("Rotation Axis:\n" + str(rAx1))
	print("Rotation Angle:\n" + str(rAng1))
	print("New vector:\n"), q1.printQuat()
	print("----------------")
	
	qr2 = Quaternion()
	qr2.axisAngleToQuat(rAx2, rAng2)
	q2 = qr2.multi(q1.multi(qr2.conj()))
	
	print("Rotation Axis:\n" + str(rAx2))
	print("Rotation Angle:\n" + str(rAng2))
	print("New vector:\n"), q2.printQuat()
	print("----------------")

	qr3 = Quaternion()
	qr3.axisAngleToQuat(rAx3, rAng3)
	q3 = qr3.multi(q2.multi(qr3.conj()))
	
	print("Rotation Axis:\n" + str(rAx3))
	print("Rotation Angle:\n" + str(rAng3))
	print("New vector:\n"), q3.printQuat()
	print("----------------")


	point = [2.0, 4.0, 1.0]
	axis0 = [1.0, 1.0, 1.0]
	axis1 = [2.0, 2.0, 0.0]
	angle = np.pi/4

	print("Start point: "+str(point))
	print("Rotation Axis: "+str(axis0)+" "+str(axis1))
	print("Rotation Angle: "+str(angle))
	print("End point: "+str(rotatePointAboutAxis(point,axis0,axis1,angle)))
	print("----------------")



	# some useful numpy functions for
	# calculating angles and vectors
	v1 = np.array([1., 1., 1.])
	v2 = np.array([1., 0., 1.])
	v1xv2 = np.cross(v1,v2)
	v2xv1 = -v1xv2
	v1dotv2 = np.arccos(np.clip(np.dot(v1,v2), -1., 1.))

	
