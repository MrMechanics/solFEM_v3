#
#
#
#
#---------------------------------------#
#	EXPECTED REACTION FORCES			#
#										#
#	node 4								#
#	------								#
#	 x:     0kN, y: 125kN				#
#										#
#	node 5								#
#	------								#
#	 x:     0kN, y: 125kN				#
#										#
#	EXPECTED DISPLACEMENTS				#
#										#
#	node 3								#
#	------								#
#	 x: 7.351E-04 y: -4.669e-03			#
#---------------------------------------#
#
#
#
#
#
#
#
#------------------------------------
SOLUTION, rod2n2d_frame_1, Static
#------------------------------------
	MESHES, 1
	LOADS, force_load-1
	BOUNDARIES, boundary-1
	BOUNDARIES, boundary-2
#------------------------------------
RESULTS, rod2n2d_frame_1
#------------------------------------
	DISPLACEMENT, plot, 1, text, 999
	STRESS, plot, 1, text, 1
	STRAIN, plot, 1, text, 1
	NODEFORCE, plot, 1, text, 1
	ELEMENTFORCE, plot, 1, text, 1
#
#
#
#
#
MATERIAL, Isotropic, steel, 200000000000.0, 0.3, 1.0
#
#
#
SECTION, RodSect, 0, steel, 0.000490874
#
#
#
BOUNDARY, Displacement, boundary-1, 1, 0., 1, 2, 3, 4, 5, 6
BOUNDARY, Displacement, boundary-2, 2, 0., 2, 4, 5, 6
#
#
#
LOAD, ForceConcentrated, force_load-1, 3, 250000, 0., -1, 0.
#
#
#
SET_NODES, 1, 5
SET_NODES, 3, 3
SET_NODES, 2, 4
SET_NODES, 999, 1 - 5
#
#
#
SET_ELEMENTS, 1, 1 - 7
#
#
#
NODE, 1, -0.460000008, 0.533012688, 0.0
NODE, 2, 0.540000021, 0.533012688, 0.0
NODE, 3, 0.0399999991, -0.3330127, 0.0
NODE, 4, 1.03999996, -0.3330127, 0.0
NODE, 5, -0.959999979, -0.3330127, 0.0
#
#
#
ELEMENT, ROD2N2D, 1, 0, 1, 2
ELEMENT, ROD2N2D, 2, 0, 3, 2
ELEMENT, ROD2N2D, 3, 0, 4, 3
ELEMENT, ROD2N2D, 4, 0, 2, 4
ELEMENT, ROD2N2D, 5, 0, 5, 1
ELEMENT, ROD2N2D, 6, 0, 1, 3
ELEMENT, ROD2N2D, 7, 0, 3, 5
#
#
#
