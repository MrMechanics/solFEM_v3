#
#
#
#---------------------------------------#
#	REACTION FORCES FROM TEXTBOOK		#
#										#
#	node 1								#
#	------								#
#	 x:     0kN, y: -8.0kN, z:  15.9kN	#
#										#
#	node 2								#
#	------								#
#	 x:     0kN, y:    0kN, z:  22.1kN	#
#										#
#	node 3								#
#	------								#
#	 x:     0kN, y:    0kN, z:  22.0kN	#
#---------------------------------------#
#
#
#
#
#
#------------------------------------
SOLUTION, rod2n_frame_2, Static
#------------------------------------
	MESHES, 1
	LOADS, force_load-1
	LOADS, force_load-2
	BOUNDARIES, boundary-1
#------------------------------------
RESULTS, rod2n_frame_2
#------------------------------------
	DISPLACEMENT, plot, 1
	STRESS, plot, 1, text, 1
	STRAIN, text, 1
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
LOAD, ForceConcentrated, force_load-1, 2, 20000, 0., 0., -1.
LOAD, ForceConcentrated, force_load-2, 3,  8000, 0., 1., 0.
#
#
#
SET_NODES, 1, 1 - 3
SET_NODES, 2, 4 - 6
SET_NODES, 3, 4
SET_NODES, 999, 1 - 6
#
#
#
SET_ELEMENTS, 1, 1 - 9
#
#
#
NODE, 1,  0.0,  0.0,  0.0
NODE, 2,  1.0, 3.87,  0.0
NODE, 3, -1.0, 3.87,  0.0
NODE, 4,  0.0,  0.0,  2.0
NODE, 5,  1.0, 3.87,  2.0
NODE, 6, -1.0, 3.87,  2.0
#
#
#
ELEMENT, ROD2N, 1, 0, 1, 4
ELEMENT, ROD2N, 2, 0, 1, 5
ELEMENT, ROD2N, 3, 0, 1, 6
ELEMENT, ROD2N, 4, 0, 4, 5
ELEMENT, ROD2N, 5, 0, 4, 6
ELEMENT, ROD2N, 6, 0, 5, 6
ELEMENT, ROD2N, 7, 0, 3, 6
ELEMENT, ROD2N, 8, 0, 3, 5
ELEMENT, ROD2N, 9, 0, 2, 5
#
#
#
