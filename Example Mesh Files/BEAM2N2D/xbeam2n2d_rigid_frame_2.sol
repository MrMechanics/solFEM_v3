#
#
#
#
#
#
#-----------------------------------------------#
#	REACTION FORCES FROM TEXTBOOK				#
#												#
#	node 1										#
#	------										#
#	 x:  39.43kN, y:  49.29kN, mz: -197.14kNm	#
#												#
#	node 41										#
#	-------										#
#	 x:  14.14kN, y:  47.14kN, mz: 	   0kNm 	#
#												#
#	node 59										#
#	-------										#
#	 x:  16.43kN, y: -16.43kN, mz:	   0kNm 	#
#												#
#-----------------------------------------------#
#
#
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
	BOUNDARIES, boundary-1
	BOUNDARIES, boundary-2
#------------------------------------
RESULTS, solution-1
#------------------------------------
	DISPLACEMENT, plot, 1
	NODEFORCE, plot, 999
	ELEMENTFORCE, plot, 1, text, 1
#
#
#
#
#
MATERIAL, Isotropic, steel, 200000000000.0, 0.25, 0.0
#
#
#
SECTION, BeamSect, 0, steel, 0.01, 0.0002, 0.0
#
#
#
BOUNDARY, Displacement, boundary-1, 1, 0., 1, 2, 3, 4, 5, 6
BOUNDARY, Displacement, boundary-2, 2, 0., 1, 2
#
#
#
LOAD, ForceConcentrated, force_load-1, 3, 80000, 0., -1, 0.
LOAD, ForceConcentrated, force_load-2, 4, 40000, -1, 0, 0.
LOAD, ForceConcentrated, force_load-3, 5, 30000, -1, 0, 0.
#
#
#
SET_NODES, 1, 1
SET_NODES, 2, 41, 59
SET_NODES, 3, 21
SET_NODES, 4, 31
SET_NODES, 5, 53
SET_NODES, 999, 1 - 59
#
#
#
SET_ELEMENTS, 1, 1 - 58
#
#
#
NODE, 1, 0.0, 0.0, 0.0
NODE, 2, 0.0, 1.0, 0.0
NODE, 3, 0.0, 2.0, 0.0
NODE, 4, 0.0, 3.0, 0.0
NODE, 5, 0.0, 4.0, 0.0
NODE, 6, 0.0, 5.0, 0.0
NODE, 7, 0.0, 6.0, 0.0
NODE, 8, 0.0, 7.0, 0.0
NODE, 9, 0.0, 8.0, 0.0
NODE, 10, 0.0, 9.0, 0.0
NODE, 11, 0.0, 10.0, 0.0
NODE, 12, 1.0, 10.0, 0.0
NODE, 13, 2.0, 10.0, 0.0
NODE, 14, 3.0, 10.0, 0.0
NODE, 15, 4.0, 10.0, 0.0
NODE, 16, 5.0, 10.0, 0.0
NODE, 17, 6.0, 10.0, 0.0
NODE, 18, 7.0, 10.0, 0.0
NODE, 19, 8.0, 10.0, 0.0
NODE, 20, 9.0, 10.0, 0.0
NODE, 21, 10.0, 10.0, 0.0
NODE, 22, 11.0, 10.0, 0.0
NODE, 23, 12.0, 10.0, 0.0
NODE, 24, 13.0, 10.0, 0.0
NODE, 25, 14.0, 10.0, 0.0
NODE, 26, 15.0, 10.0, 0.0
NODE, 27, 16.0, 10.0, 0.0
NODE, 28, 17.0, 10.0, 0.0
NODE, 29, 18.0, 10.0, 0.0
NODE, 30, 19.0, 10.0, 0.0
NODE, 31, 20.0, 10.0, 0.0
NODE, 32, 20.0, 9.0, 0.0
NODE, 33, 20.0, 8.0, 0.0
NODE, 34, 20.0, 7.0, 0.0
NODE, 35, 20.0, 6.0, 0.0
NODE, 36, 20.0, 5.0, 0.0
NODE, 37, 20.0, 4.0, 0.0
NODE, 38, 20.0, 3.0, 0.0
NODE, 39, 20.0, 2.0, 0.0
NODE, 40, 20.0, 1.0, 0.0
NODE, 41, 20.0, 0.0, 0.0
NODE, 42, 21.0, 6.0, 0.0
NODE, 43, 22.0, 6.0, 0.0
NODE, 44, 23.0, 6.0, 0.0
NODE, 45, 24.0, 6.0, 0.0
NODE, 46, 25.0, 6.0, 0.0
NODE, 47, 26.0, 6.0, 0.0
NODE, 48, 27.0, 6.0, 0.0
NODE, 49, 28.0, 6.0, 0.0
NODE, 50, 29.0, 6.0, 0.0
NODE, 51, 30.0, 6.0, 0.0
NODE, 52, 31.0, 6.0, 0.0
NODE, 53, 32.0, 6.0, 0.0
NODE, 54, 32.0, 5.0, 0.0
NODE, 55, 32.0, 4.0, 0.0
NODE, 56, 32.0, 3.0, 0.0
NODE, 57, 32.0, 2.0, 0.0
NODE, 58, 32.0, 1.0, 0.0
NODE, 59, 32.0, 0.0, 0.0
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
ELEMENT, BEAM2N2D, 33, 0, 33, 34
ELEMENT, BEAM2N2D, 34, 0, 34, 35
ELEMENT, BEAM2N2D, 35, 0, 35, 36
ELEMENT, BEAM2N2D, 36, 0, 36, 37
ELEMENT, BEAM2N2D, 37, 0, 37, 38
ELEMENT, BEAM2N2D, 38, 0, 38, 39
ELEMENT, BEAM2N2D, 39, 0, 39, 40
ELEMENT, BEAM2N2D, 40, 0, 40, 41
ELEMENT, BEAM2N2D, 41, 0, 35, 42
ELEMENT, BEAM2N2D, 42, 0, 42, 43
ELEMENT, BEAM2N2D, 43, 0, 43, 44
ELEMENT, BEAM2N2D, 44, 0, 44, 45
ELEMENT, BEAM2N2D, 45, 0, 45, 46
ELEMENT, BEAM2N2D, 46, 0, 46, 47
ELEMENT, BEAM2N2D, 47, 0, 47, 48
ELEMENT, BEAM2N2D, 48, 0, 48, 49
ELEMENT, BEAM2N2D, 49, 0, 49, 50
ELEMENT, BEAM2N2D, 50, 0, 50, 51
ELEMENT, BEAM2N2D, 51, 0, 51, 52
ELEMENT, BEAM2N2D, 52, 0, 52, 53
ELEMENT, BEAM2N2D, 53, 0, 53, 54
ELEMENT, BEAM2N2D, 54, 0, 54, 55
ELEMENT, BEAM2N2D, 55, 0, 55, 56
ELEMENT, BEAM2N2D, 56, 0, 56, 57
ELEMENT, BEAM2N2D, 57, 0, 57, 58
ELEMENT, BEAM2N2D, 58, 0, 58, 59
#
#
#
