#
#
#
#---------------------------------------#
#	REACTION FORCES FROM TEXTBOOK		#
#										#
#	node 1								#
#	------								#
#	 x: -35.5kN, y:  8.2kN, z:  11.8kN	#
#										#
#	node 2								#
#	------								#
#	 x:  51.8kN, y: 31.8kN, z:  34.6kN	#
#										#
#	node 3								#
#	------								#
#	 x: -16.4kN, y:    0kN, z: -16.4kN	#
#---------------------------------------#
#
#
#
#
#
#------------------------------------
SOLUTION, rod2n_frame_1, Static
#------------------------------------
	MESHES, 1
	LOADS, force_load-1
	LOADS, force_load-2
	BOUNDARIES, boundary-1
#------------------------------------
RESULTS, rod2n_frame_1
#------------------------------------
	DISPLACEMENT, plot, 1
	STRESS, plot, 1, text, 1
	STRAIN, text, 1
	NODEFORCE, plot, 1, text, 1
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
LOAD, ForceConcentrated, force_load-1, 2, 40000, 0., -1, 0.
LOAD, ForceConcentrated, force_load-2, 2, 30000, 0., 0, -1
#
#
#
SET_NODES, 1, 1 - 3
SET_NODES, 2, 4
SET_NODES, 999, 1 - 5
#
#
#
SET_ELEMENTS, 1, 1 - 6
#
#
#
NODE, 1, 0.0, 0.0, 0.0
NODE, 2, 0.0, -2.0, -3.0
NODE, 3, 0.0, 1.0, -4.0
NODE, 4, 3.0, -1.0, -1.0
NODE, 5, 3.0, 1.0, -1.0
#
#
#
ELEMENT, ROD2N, 1, 0, 1, 4
ELEMENT, ROD2N, 2, 0, 1, 5
ELEMENT, ROD2N, 3, 0, 2, 4
ELEMENT, ROD2N, 4, 0, 2, 5
ELEMENT, ROD2N, 5, 0, 4, 5
ELEMENT, ROD2N, 6, 0, 3, 5
#
#
#
