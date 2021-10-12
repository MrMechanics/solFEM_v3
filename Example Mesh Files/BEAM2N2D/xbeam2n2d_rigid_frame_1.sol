#
#
#
#
#-----------------------------------------------#
#	REACTION FORCES FROM TEXTBOOK				#
#												#
#	node 1										#
#	------										#
#	 x:  13.41kN, y: 100.75kN, mz: -28.52kNm	#
#												#
#	node 21										#
#	-------										#
#	 x: -56.97kN, y:      0kN, mz: 	   0kNm 	#
#												#
#	node 33										#
#	-------										#
#	 x: -24.40kN, y:  85.25kN, mz:	   0kNm 	#
#												#
#	element 8									#
#	---------									#
#	 mz: -89.1kNm								#
#-----------------------------------------------#
#
#
#
#------------------------------------
SOLUTION, solution-1, Static
#------------------------------------
	MESHES, 1
	LOADS, force_load-1
	LOADS, force_load-2
	LOADS, force_load-3
	LOADS, force_load-4
	LOADS, force_load-5
	BOUNDARIES, boundary-1
	BOUNDARIES, boundary-2
#------------------------------------
RESULTS, solution-1
#------------------------------------
	DISPLACEMENT, plot, 1
	STRESS, plot, 1
	STRAIN, plot, 1
	NODEFORCE, plot, 999
	ELEMENTFORCE, plot, 1, text, 2
#
#
#
#
#
MATERIAL, Isotropic, steel, 200000000000.0, 0.25, 0.0
#
#
#
SECTION, BeamSect, 0, steel, 0.001, 2e-06, 0.0
#
#
#
#
#
#
BOUNDARY, Displacement, boundary-1, 1, 0., 1, 2, 3, 4, 5, 6
BOUNDARY, Displacement, boundary-2, 2, 0., 1, 2, 3
#
#
#
LOAD, ForceConcentrated, force_load-1, 3, 16000, 0., -1, 0.
LOAD, ForceConcentrated, force_load-2, 4, 20000, 0., -1, 0.
LOAD, Force, force_load-3, 5, 150000, 0., -1, 0.
LOAD, Force, force_load-4, 6, 32000, 1, 0, 0.
LOAD, Force, force_load-5, 7, 36000, 1, 0, 0.
#
#
#
#
#
#
#
#
#
SET_NODES, 1, 1
SET_NODES, 2, 21, 33
SET_NODES, 3, 13
SET_NODES, 4, 17
SET_NODES, 5, 9 - 20
SET_NODES, 6, 2 - 9
SET_NODES, 7, 22 - 32
SET_NODES, 999, 1 - 33
#
#
#
SET_ELEMENTS, 1, 1 - 32
SET_ELEMENTS, 2, 8
#
#
#
NODE, 1, 0.0, 0.0, 0.0
NODE, 2, 0.0, 0.5, 0.0
NODE, 3, 0.0, 1.0, 0.0
NODE, 4, 0.0, 1.5, 0.0
NODE, 5, 0.0, 2.0, 0.0
NODE, 6, 0.0, 2.5, 0.0
NODE, 7, 0.0, 3.0, 0.0
NODE, 8, 0.0, 3.5, 0.0
NODE, 9, 0.0, 4.0, 0.0
NODE, 10, 0.5, 4.0, 0.0
NODE, 11, 1.0, 4.0, 0.0
NODE, 12, 1.5, 4.0, 0.0
NODE, 13, 2.0, 4.0, 0.0
NODE, 14, 2.5, 4.0, 0.0
NODE, 15, 3.0, 4.0, 0.0
NODE, 16, 3.5, 4.0, 0.0
NODE, 17, 4.0, 4.0, 0.0
NODE, 18, 4.5, 4.0, 0.0
NODE, 19, 5.0, 4.0, 0.0
NODE, 20, 5.5, 4.0, 0.0
NODE, 21, 6.0, 4.0, 0.0
NODE, 22, 6.0, 3.5, 0.0
NODE, 23, 6.0, 3.0, 0.0
NODE, 24, 6.0, 2.5, 0.0
NODE, 25, 6.0, 2.0, 0.0
NODE, 26, 6.0, 1.5, 0.0
NODE, 27, 6.0, 1.0, 0.0
NODE, 28, 6.0, 0.5, 0.0
NODE, 29, 6.0, 0.0, 0.0
NODE, 30, 6.0, -0.5, 0.0
NODE, 31, 6.0, -1.0, 0.0
NODE, 32, 6.0, -1.5, 0.0
NODE, 33, 6.0, -2.0, 0.0
#
#
#
ELEMENT, BEAM2N2D, 1, 0, 1, 2
ELEMENT, BEAM2N2D, 2, 0, 2, 3
ELEMENT, BEAM2N2D, 3, 0, 3, 4
ELEMENT, BEAM2N2D, 4, 0, 4, 5
ELEMENT, BEAM2N2D, 5, 0, 5, 6
ELEMENT, BEAM2N2D, 6, 0, 6, 7
ELEMENT, BEAM2N2D, 7, 0, 7, 8
ELEMENT, BEAM2N2D, 8, 0, 8, 9
ELEMENT, BEAM2N2D, 9, 0, 9, 10
ELEMENT, BEAM2N2D, 10, 0, 10, 11
ELEMENT, BEAM2N2D, 11, 0, 11, 12
ELEMENT, BEAM2N2D, 12, 0, 12, 13
ELEMENT, BEAM2N2D, 13, 0, 13, 14
ELEMENT, BEAM2N2D, 14, 0, 14, 15
ELEMENT, BEAM2N2D, 15, 0, 15, 16
ELEMENT, BEAM2N2D, 16, 0, 16, 17
ELEMENT, BEAM2N2D, 17, 0, 17, 18
ELEMENT, BEAM2N2D, 18, 0, 18, 19
ELEMENT, BEAM2N2D, 19, 0, 19, 20
ELEMENT, BEAM2N2D, 20, 0, 20, 21
ELEMENT, BEAM2N2D, 21, 0, 21, 22
ELEMENT, BEAM2N2D, 22, 0, 22, 23
ELEMENT, BEAM2N2D, 23, 0, 23, 24
ELEMENT, BEAM2N2D, 24, 0, 24, 25
ELEMENT, BEAM2N2D, 25, 0, 25, 26
ELEMENT, BEAM2N2D, 26, 0, 26, 27
ELEMENT, BEAM2N2D, 27, 0, 27, 28
ELEMENT, BEAM2N2D, 28, 0, 28, 29
ELEMENT, BEAM2N2D, 29, 0, 29, 30
ELEMENT, BEAM2N2D, 30, 0, 30, 31
ELEMENT, BEAM2N2D, 31, 0, 31, 32
ELEMENT, BEAM2N2D, 32, 0, 32, 33
#
#
#
