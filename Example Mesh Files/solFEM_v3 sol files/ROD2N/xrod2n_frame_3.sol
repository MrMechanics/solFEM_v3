#
#
#
#---------------------------------------#
#	REACTION FORCES FROM TEXTBOOK		#
#										#
#	node 1								#
#	------								#
#	 x:     0kN, y:    0kN, z:    0kN	#
#										#
#	node 2								#
#	------								#
#	 x:   -40kN, y:  -20kN, z:  -40kN	#
#										#
#	node 3								#
#	------								#
#	 x:   -40kN, y:  -20kN, z:   40kN	#
#---------------------------------------#
#
#
#
#
#
#------------------------------------
SOLUTION, rod2n_frame_3, Static
#------------------------------------
	MESHES, 1
	LOADS, force_load-1
	LOADS, force_load-2
	BOUNDARIES, boundary-1
#------------------------------------
RESULTS, rod2n_frame_3
#------------------------------------
	DISPLACEMENT, plot, 1, text, 999
	STRESS, plot, 1, text, 1
	STRAIN, plot, 1, text, 1
	NODEFORCE, plot, 999, text, 1
	ELEMENTFORCE, plot, 1, text, 1
#
#
#
#
#
MATERIAL, Isotropic, steel, 205e9, 0.29
#
#
#
SECTION, RodSect, 0, steel, 0.005
#
#
#
BOUNDARY, Displacement, boundary-1, 1, 0., 1, 2, 3, 4, 5, 6
#
#
#
LOAD, ForceConcentrated, force_load-1, 2, 80000, 1., 0., 0.
LOAD, ForceConcentrated, force_load-2, 3, 40000, 0., 1., 0.
#
#
#
SET_NODES, 1, 1 - 3
SET_NODES, 2, 5
SET_NODES, 3, 4
SET_NODES, 999, 1 - 5
#
#
#
SET_ELEMENTS, 1, 1 - 6
#
#
#
NODE, 1,  0.0,   0.0,  0.0
NODE, 2,  0.0, -20.0,  0.0
NODE, 3, 20.0, -10.0,  0.0
NODE, 4, 10.0,  -5.0, 10.0
NODE, 5, 10.0, -15.0, 10.0
#
#
#
ELEMENT, ROD2N, 1, 0, 1, 4
ELEMENT, ROD2N, 2, 0, 1, 5
ELEMENT, ROD2N, 3, 0, 2, 5
ELEMENT, ROD2N, 4, 0, 3, 4
ELEMENT, ROD2N, 5, 0, 3, 5
ELEMENT, ROD2N, 6, 0, 4, 5
#
#
#
