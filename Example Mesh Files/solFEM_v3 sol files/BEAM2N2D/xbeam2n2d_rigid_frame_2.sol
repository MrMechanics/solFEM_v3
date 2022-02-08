#
#
#
#-----------------------------------------------#
#	REACTION FORCES AND ELEMENT FORCES			#
#		FROM TEXTBOOK							#
#												#
#	node 1										#
#	------										#
#	 x: -2.35 kN, y: 28.76 kN, mz: 22.35 kNm	#
#												#
#	node 3										#
#	------										#
#	 x:  0.0 kN,  y: 40.42 kN, mz: 	0.0 kNm 	#
#												#
#	node 4										#
#	------										#
#	 x:  2.35 kN, y: 14.82 kN, mz:	0.0 kNm 	#
#												#
#-----------------------------------------------#
#
#
#
#
#
#------------------------------------
SOLUTION, xbeam2n2d_rigid_frame_2, Static
#------------------------------------
	MESHES, 1
	LOADS, force_load-1
	LOADS, force_load-2
	BOUNDARIES, boundary-1
	BOUNDARIES, boundary-2
	BOUNDARIES, boundary-3
#------------------------------------
RESULTS, xbeam2n2d_rigid_frame_2
#------------------------------------
	DISPLACEMENT, plot, 1
	NODEFORCE, plot, 999
	ELEMENTFORCE, plot, 1
#
#
#
#
#
MATERIAL, Isotropic, 1010_carbon_steel (N m kg), 205000000000.0, 0.29, 7870.0
#
#
#
SECTION, BeamSect, 0, 1010_carbon_steel (N m kg), 0.005, 4.166666666668e-06, 1.0416666666667e-06, CrossSection, Rectangle, 0.05, 0.1, 0.0, 0.0
#
#
#
#
#
#
#
#
#
BOUNDARY, Displacement, boundary-1, 1, 0., 1, 2, 6
BOUNDARY, Displacement, boundary-2, 2, 0., 2
BOUNDARY, Displacement, boundary-3, 3, 0., 1, 2
#
#
#
LOAD, ForceConcentrated, force_load-1, 4, 36000, 0., -1, 0.
LOAD, ForceDistributed, force_load-2, 2, 12000, 0., -1, 0.
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
SET_NODES, 2, 3
SET_NODES, 3, 4
SET_NODES, 4, 17
SET_NODES, 999, 1 - 19
#
#
#
SET_ELEMENTS, 1, 4 - 21
SET_ELEMENTS, 2, 4 - 9
#
#
#
NODE, 1, 0.0, 4.0, 0.0
NODE, 2, 4.0, 4.0, 0.0
NODE, 3, 4.0, 0.0, 0.0
NODE, 4, 8.0, 0.0, 0.0
NODE, 5, 0.6666666666666666, 4.0, 0.0
NODE, 6, 1.3333333333333333, 4.0, 0.0
NODE, 7, 2.0, 4.0, 0.0
NODE, 8, 2.6666666666666665, 4.0, 0.0
NODE, 9, 3.3333333333333335, 4.0, 0.0
NODE, 10, 4.0, 3.3333333333333335, 0.0
NODE, 11, 4.0, 2.666666666666667, 0.0
NODE, 12, 4.0, 2.0, 0.0
NODE, 13, 4.0, 1.3333333333333335, 0.0
NODE, 14, 4.0, 0.6666666666666665, 0.0
NODE, 15, 4.666666666666667, 0.0, 0.0
NODE, 16, 5.333333333333333, 0.0, 0.0
NODE, 17, 6.0, 0.0, 0.0
NODE, 18, 6.666666666666666, 0.0, 0.0
NODE, 19, 7.333333333333334, 0.0, 0.0
#
#
#
ELEMENT, BEAM2N2D, 4, 0, 1, 5
ELEMENT, BEAM2N2D, 5, 0, 5, 6
ELEMENT, BEAM2N2D, 6, 0, 6, 7
ELEMENT, BEAM2N2D, 7, 0, 7, 8
ELEMENT, BEAM2N2D, 8, 0, 8, 9
ELEMENT, BEAM2N2D, 9, 0, 9, 2
ELEMENT, BEAM2N2D, 10, 0, 2, 10
ELEMENT, BEAM2N2D, 11, 0, 10, 11
ELEMENT, BEAM2N2D, 12, 0, 11, 12
ELEMENT, BEAM2N2D, 13, 0, 12, 13
ELEMENT, BEAM2N2D, 14, 0, 13, 14
ELEMENT, BEAM2N2D, 15, 0, 14, 3
ELEMENT, BEAM2N2D, 16, 0, 3, 15
ELEMENT, BEAM2N2D, 17, 0, 15, 16
ELEMENT, BEAM2N2D, 18, 0, 16, 17
ELEMENT, BEAM2N2D, 19, 0, 17, 18
ELEMENT, BEAM2N2D, 20, 0, 18, 19
ELEMENT, BEAM2N2D, 21, 0, 19, 4
#
#
#
