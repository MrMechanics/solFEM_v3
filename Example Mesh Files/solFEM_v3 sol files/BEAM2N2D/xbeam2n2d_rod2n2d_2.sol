#
#
#
#
# example of how you can use beam elements
# and rod elements in the same analysis using
# constraints (lagrange multipliers)
#
#
#
#
#-------------------------------------------#
#	EXPECTED DISPLACEMENTS FROM TEXTBOOK	#
#											#
#	node 26									#
#	------- 								#
#	 y: -6.64e-03							#
#											#
#											#
#	EXPECTED REACTION FORCES FROM TEXTBOOK	#
#											#
#	node 1									#
#	------	 								#
#	 x: -81kN, y:  0kN						#
#											#
#	node 2									#
#	------	 								#
#	 x:  81kN, y: 48kN						#
#-------------------------------------------#
#
#
#
#
#------------------------------------
SOLUTION, xbeam2n2d_rod2n2d_2, Static
#------------------------------------
	MESHES, 999
	LOADS, force_load-1
	LOADS, force_load-2
	BOUNDARIES, boundary-1
	CONSTRAINTS, touchlock-1
	CONSTRAINTS, touchlock-2
#------------------------------------
RESULTS, xbeam2n2d_rod2n2d_2
#------------------------------------
	DISPLACEMENT, plot, 6, text, 6
	STRESS, plot, 1
	STRAIN, plot, 1
	NODEFORCE, plot, 999
	ELEMENTFORCE, plot, 999, text, 2
#
#
#
#
#
MATERIAL, Isotropic, steel, 205000000000.0, 0.25, 0.0
#
#
#
SECTION, RodSect, 0, steel, 0.004
SECTION, BeamSect, 1, steel, 0.004, 0.0005
#
#
#
CONSTRAINT, TouchLock, touchlock-1, 1, 2, 0.1, 1, 2
CONSTRAINT, TouchLock, touchlock-2, 3, 4, 0.1, 2
#
#
#
BOUNDARY, Displacement, boundary-1, 5, 0., 1, 2
#
#
#
LOAD, ForceConcentrated, force_load-1, 6, 12000, 0., -1, 0.
LOAD, ForceDistributed, force_load-2, 2, 6000, 0., -1, 0.
#
#
#
#
#
#
#
#
#
SET_NODES, 1, 3
SET_NODES, 2, 6
SET_NODES, 3, 16
SET_NODES, 4, 4
SET_NODES, 5, 1, 2
SET_NODES, 6, 26
SET_NODES, 7, 6 - 26
SET_NODES, 999, 1 - 26
#
#
#
SET_ELEMENTS, 1, 1 - 6
SET_ELEMENTS, 2, 7 - 26
SET_ELEMENTS, 999, 1 - 26
#
#
#
NODE, 1, 0.0, 0.0, 0.0
NODE, 2, 0.0, -4.0, 0.0
NODE, 3, 3.0, 0.0, 0.0
NODE, 4, 6.0, 0.0, 0.0
NODE, 5, 3.0, -4.0, 0.0
NODE, 6, 3.0, 0.05, 0.0
NODE, 7, 3.3, 0.05, 0.0
NODE, 8, 3.5999999999999996, 0.05, 0.0
NODE, 9, 3.8999999999999995, 0.05, 0.0
NODE, 10, 4.199999999999999, 0.05, 0.0
NODE, 11, 4.499999999999999, 0.05, 0.0
NODE, 12, 4.799999999999999, 0.05, 0.0
NODE, 13, 5.099999999999999, 0.05, 0.0
NODE, 14, 5.399999999999999, 0.05, 0.0
NODE, 15, 5.699999999999998, 0.05, 0.0
NODE, 16, 5.999999999999998, 0.05, 0.0
NODE, 17, 6.299999999999998, 0.05, 0.0
NODE, 18, 6.599999999999998, 0.05, 0.0
NODE, 19, 6.899999999999998, 0.05, 0.0
NODE, 20, 7.1999999999999975, 0.05, 0.0
NODE, 21, 7.499999999999997, 0.05, 0.0
NODE, 22, 7.799999999999997, 0.05, 0.0
NODE, 23, 8.099999999999998, 0.05, 0.0
NODE, 24, 8.399999999999999, 0.05, 0.0
NODE, 25, 8.7, 0.05, 0.0
NODE, 26, 9.0, 0.05, 0.0
#
#
#
ELEMENT, ROD2N2D, 1, 0, 1, 3
ELEMENT, ROD2N2D, 2, 0, 2, 3
ELEMENT, ROD2N2D, 3, 0, 3, 4
ELEMENT, ROD2N2D, 4, 0, 2, 5
ELEMENT, ROD2N2D, 5, 0, 3, 5
ELEMENT, ROD2N2D, 6, 0, 4, 5
ELEMENT, BEAM2N2D, 7, 1, 6, 7
ELEMENT, BEAM2N2D, 8, 1, 7, 8
ELEMENT, BEAM2N2D, 9, 1, 8, 9
ELEMENT, BEAM2N2D, 10, 1, 9, 10
ELEMENT, BEAM2N2D, 11, 1, 10, 11
ELEMENT, BEAM2N2D, 12, 1, 11, 12
ELEMENT, BEAM2N2D, 13, 1, 12, 13
ELEMENT, BEAM2N2D, 14, 1, 13, 14
ELEMENT, BEAM2N2D, 15, 1, 14, 15
ELEMENT, BEAM2N2D, 16, 1, 15, 16
ELEMENT, BEAM2N2D, 17, 1, 16, 17
ELEMENT, BEAM2N2D, 18, 1, 17, 18
ELEMENT, BEAM2N2D, 19, 1, 18, 19
ELEMENT, BEAM2N2D, 20, 1, 19, 20
ELEMENT, BEAM2N2D, 21, 1, 20, 21
ELEMENT, BEAM2N2D, 22, 1, 21, 22
ELEMENT, BEAM2N2D, 23, 1, 22, 23
ELEMENT, BEAM2N2D, 24, 1, 23, 24
ELEMENT, BEAM2N2D, 25, 1, 24, 25
ELEMENT, BEAM2N2D, 26, 1, 25, 26
#
#
#
