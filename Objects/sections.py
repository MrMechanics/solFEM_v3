#
#
#	sections.py
#  -------------
#
#	This file holds all the section objects. These are used to
#	apply material properties (e.g. the E-matrix) to each individual
#	element.
#


import numpy as np





class Section(object):
	'''
Base class for section properties.
'''
	def __init__(self,number,material):
		self.number = number
		self.material = material
		self.is3D = True


	def calcElasticModuli(self):
		'''
	Calculate the elastic moduli matrix for element section.
	This is used by solver when building element stiffness
	matrices.
	'''
		E = self.material.elastMod
		v = self.material.poisson
		if self.material.isotropic == True:
			if self.is3D == False:
				if self.planeStressStrain == 'planestress':
					self.E = np.array([[E/(1-v**2), (v*E)/(1-v**2), 0],
									   [(v*E)/(1-v**2), E/(1-v**2), 0],
									   [ 0, 0, (0.5*(1-v)*E)/(1-v**2)]])
				else:
					XE = E/((1+v)*(1-(2*v)))
					self.E = np.array([[ 1-v, 	v, 		 0],
		                      		   [   v, 1-v, 		 0],
		                      		   [   0, 	0, (1-2*v)]])
			else:
				XE = E/((1+v)*(1-2*v))
				self.E = np.array([[XE*(1-v), XE*v, XE*v, 0, 0, 0],
								   [XE*v, XE*(1-v), XE*v, 0, 0, 0],
								   [XE*v, XE*v, XE*(1-v), 0, 0, 0],
								   [0, 0, 0, XE*(0.5-v), 0, 0],
								   [0, 0, 0, 0, XE*(0.5-v), 0],
								   [0, 0, 0, 0, 0, XE*(0.5-v)]])
		else:
			print('non-isotropic material not supported')




class MassSect(Section):
	'''
Class for mass element cross section properties.
Subclass of Section.
'''
	def __init__(self,number,material,m_x,m_y,m_z,m_rx,m_ry,m_rz):
		self.mass = [float(m_x), float(m_y), float(m_z), 
						float(m_rx), float(m_ry), float(m_rz)]
		super(MassSect, self).__init__(number,material)




class RodSect(Section):
	'''
Class for rod element cross section properties.
Subclass of Section.
'''
	def __init__(self,number,material,A):
		self.area = float(A)
		super(RodSect, self).__init__(number,material)




class BeamSect(Section):
	'''
Class for beam element cross section properties.
Subclass of Section.
'''
	def __init__(self,number,material,A,Izz,Iyy=0.):
		self.area = float(A)
		self.Izz = float(Izz)
		self.Iyy = float(Iyy)
		self.Jxx = self.Izz + self.Iyy
		super(BeamSect, self).__init__(number,material)




class PlaneSect(Section):
	'''
Class for plane element section properties.
This is used for 2D elements that have more than
two nodes (not rods and beams).
Subclass of Section.
'''
	def __init__(self,number,material,h,stress='planestress'):
		self.thickness = float(h)
		super(PlaneSect, self).__init__(number,material)
		self.is3D = False
		self.planeStressStrain = stress
		self.calcElasticModuli()




class PlateSect(Section):
	'''
Class for plate element section properties.
Used for 3D shell elements, if such are ever
implemented in this program.
Subclass of Section.
'''
	def __init__(self,number,material,h,stress='planestress'):
		self.thickness = float(h)
		super(PlateSect, self).__init__(number,material)
		self.is3D = False
		self.planeStressStrain = stress
		self.calcElasticModuli()




class SolidSect(Section):
	'''
Class for solid element section properties.
Subclass of Section.
'''
	def __init__(self,number,material):
		super(SolidSect,self).__init__(number,material)
		self.calcElasticModuli()




