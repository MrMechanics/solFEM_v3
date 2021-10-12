#
#	materials.py
#  --------------
#
#	This file holds the material objects. These are applied to
#	section objects which use the material information for
#	calculating the element E-matrix. Only isotropic materials
#	are supported in this program currently.
#





class Material(object):
	'''
Base class for material properties.
'''
	def __init__(self,name):
		self.name = name




class Isotropic(Material):
	'''
Isotropic material
'''
	def __init__(self,name,E,v,p=0,a=0,k=0,c=0):
		self.isotropic = True
		self.elastMod = E
		self.poisson = v
		self.shearMod = E/(2*(1-v))
		self.density = p
		self.thrmExp = a
		self.conduct = k
		self.spfHeat = c
		super(Isotropic,self).__init__(name)




class Anisotropic(Material):	# NOT READY TO BE USED
	'''
Anisotropic material
'''
	pass





