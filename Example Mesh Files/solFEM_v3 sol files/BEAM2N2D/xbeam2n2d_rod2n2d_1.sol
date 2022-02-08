#
#
#
#
# example showing you can use beam elements
# and rod elements in the same analysis using
# constraints (lagrange multipliers)
#
#
#
#
#-----------------------------------------------#
#	EXPECTED DISPLACEMENTS						#
#												#
#	node 26										#
#	------										#
#	 y: -5.44e-03								#
#												#
#-----------------------------------------------#
#	REACTION FORCES FROM TEXTBOOK				#
#												#
#	node 4										#
#	-------										#
#	 x:  34.0 kN, y:  28.0 kN, mz: 0.0 kNm	 	#
#												#
#	node 6										#
#	------										#
#	 x: -34.0 kN, y: -11.0 kN, mz: 0.0 kNm		#
#												#
#-----------------------------------------------#
#
#
#
#
#------------------------------------
SOLUTION, xbeam2n2d_rod2n2d_1, Static
#------------------------------------
	MESHES, 999
	LOADS, distributed_load-1
	LOADS, concentrated_load-1
	BOUNDARIES, boundary-1
	CONSTRAINTS, touchlock-1
#------------------------------------
RESULTS, xbeam2n2d_rod2n2d_1
#------------------------------------
	DISPLACEMENT, plot, 999, text, 5
	NODEFORCE, plot, 999
	STRESS, plot, 999, text, 2
	STRAIN, plot, 999, text, 999
	ELEMENTFORCE, plot, 999, text, 999
#
#
#
#
#
MATERIAL, Isotropic, steel, 205000000000.0, 0.25, 0.0
MATERIAL, Isotropic, steel, 205000000000.0, 0.25, 0.0
#
#
#
SECTION, BeamSect, 0, steel, 0.0015, 9e-05, 0.0
SECTION, RodSect, 1, steel, 0.0015
#
#
#
CONSTRAINT, TouchLock, touchlock-1, 2, 3, 0.15, 1, 2
#
#
#
BOUNDARY, Displacement, boundary-1, 1, 0., 1, 2
#
#
#
LOAD, ForceDistributed, distributed_load-1, 3, 1000, 0., -1, 0.
LOAD, ForceConcentrated, concentrated_load-1, 5, 15000, 0., -1, 0.
#
#
#
SET_NODES, 1, 4, 6
SET_NODES, 2, 16
SET_NODES, 3, 5
SET_NODES, 4, 7 - 16
SET_NODES, 5, 26
SET_NODES, 999, 4 - 26
#
#
#
SET_ELEMENTS, 1, 4 - 23
SET_ELEMENTS, 2, 3
SET_ELEMENTS, 3, 4 - 13
SET_ELEMENTS, 999, 3 - 23
#
#
#
NODE, 4, 0.0, -2.0, 0.0
NODE, 5, 2.0, -0.1, 0.0
NODE, 6, 0.0, 0.0, 0.0
NODE, 7, 0.2, 0.0, 0.0
NODE, 8, 0.4, 0.0, 0.0
NODE, 9, 0.6000000000000001, 0.0, 0.0
NODE, 10, 0.8, 0.0, 0.0
NODE, 11, 1.0, 0.0, 0.0
NODE, 12, 1.2, 0.0, 0.0
NODE, 13, 1.4, 0.0, 0.0
NODE, 14, 1.5999999999999999, 0.0, 0.0
NODE, 15, 1.7999999999999998, 0.0, 0.0
NODE, 16, 1.9999999999999998, 0.0, 0.0
NODE, 17, 2.1999999999999997, 0.0, 0.0
NODE, 18, 2.4, 0.0, 0.0
NODE, 19, 2.6, 0.0, 0.0
NODE, 20, 2.8000000000000003, 0.0, 0.0
NODE, 21, 3.0000000000000004, 0.0, 0.0
NODE, 22, 3.2000000000000006, 0.0, 0.0
NODE, 23, 3.400000000000001, 0.0, 0.0
NODE, 24, 3.600000000000001, 0.0, 0.0
NODE, 25, 3.800000000000001, 0.0, 0.0
NODE, 26, 4.000000000000001, 0.0, 0.0
#
#
#
ELEMENT, ROD2N2D, 3, 1, 4, 5
ELEMENT, BEAM2N2D, 4, 0, 6, 7
ELEMENT, BEAM2N2D, 5, 0, 7, 8
ELEMENT, BEAM2N2D, 6, 0, 8, 9
ELEMENT, BEAM2N2D, 7, 0, 9, 10
ELEMENT, BEAM2N2D, 8, 0, 10, 11
ELEMENT, BEAM2N2D, 9, 0, 11, 12
ELEMENT, BEAM2N2D, 10, 0, 12, 13
ELEMENT, BEAM2N2D, 11, 0, 13, 14
ELEMENT, BEAM2N2D, 12, 0, 14, 15
ELEMENT, BEAM2N2D, 13, 0, 15, 16
ELEMENT, BEAM2N2D, 14, 0, 16, 17
ELEMENT, BEAM2N2D, 15, 0, 17, 18
ELEMENT, BEAM2N2D, 16, 0, 18, 19
ELEMENT, BEAM2N2D, 17, 0, 19, 20
ELEMENT, BEAM2N2D, 18, 0, 20, 21
ELEMENT, BEAM2N2D, 19, 0, 21, 22
ELEMENT, BEAM2N2D, 20, 0, 22, 23
ELEMENT, BEAM2N2D, 21, 0, 23, 24
ELEMENT, BEAM2N2D, 22, 0, 24, 25
ELEMENT, BEAM2N2D, 23, 0, 25, 26
#
#
#
