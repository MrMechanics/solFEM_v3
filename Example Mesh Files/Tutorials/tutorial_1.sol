#
#
#
#
#
#
#	TUTORIAL 1 (ROD2N2D elements)
#
#
#	Show how to:
#	------------
#	Edit the *.sol file
#	Run the solver from the command line
#	
#
#
#
#
#
#--------------------------
SOLUTION, tutorial_1-1, Static
#--------------------------
	LOADS, load_1
	BOUNDARIES, fixed_nodes
	BOUNDARIES, sliding_nodes
#--------------------------
RESULTS, tutorial_1-1
#--------------------------
	DISPLACEMENT, text, 4
	NODEFORCE, text, 1
	ELEMENTFORCE, text, 1
	STRESS, text, 1
#
#
#
#
SET_NODES, 1, 1
SET_NODES, 2, 2
SET_NODES, 3, 3
SET_NODES, 4, 1 - 3
#
#
#
SET_ELEMENTS, 1, 1 - 3
#
#
#
MATERIAL, Isotropic, steel, 200e9, 0.25
#
#
#
SECTION, RodSect, 0, steel,  0.02
#
#
#
LOAD, ForceConcentrated, load_1,   3,   75000., 0., -1.
#
#
#
BOUNDARY, Displacement, fixed_nodes,	 2,   0.0, 1, 2
BOUNDARY, Displacement, sliding_nodes,   1,   0.0, 1
#
#
#
NODE,  1,  0.0,  0.0
NODE,  2,  0.0,  3.0
NODE,  3,  3.0,  3.0
#
#
#
ELEMENT, ROD2N2D,  1,  0,  1,  2
ELEMENT, ROD2N2D,  2,  0,  2,  3
ELEMENT, ROD2N2D,  3,  0,  3,  1
#
#
#
