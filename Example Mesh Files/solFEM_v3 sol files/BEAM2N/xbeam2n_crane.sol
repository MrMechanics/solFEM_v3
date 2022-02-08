#
#
#
#
#-----------------------------------------------#
#	EXPECTED DISPLACEMENTS						#
#												#
#	node 4										#
#	------										#
#    x: 2.312e-03, y: -1.882e-02, z: 1.266e-04	#
#	 magn: 1.897e-02							#
#												#
#-----------------------------------------------#---------------------------------------#
#	EXPECTED REACTION FORCES															#
#																						#
#	node 6																				#
#	------																				#
#    FX: 39.9 kN, FY: 7.47 kN, FZ: 4.49 kN, MX: -0.9 Nm, MY: 9.0 Nm, MZ: 17.9 Nm		#
#																						#
#	node 8																				#
#	------																				#
#    FX: -39.9 kN, FY: -2.47 kN, FZ: -4.49 kN, MX: -1.19 Nm, MY: -7.72 Nm, MZ: 41.1 Nm	#
#																						#
#	node 14																				#
#	------	-																			#
#    FX: 39.9 kN, FY: 7.47 kN, FZ: -4.49 kN, MX: 0.16 Nm, MY: -7.66 Nm, MZ: 18.0 Nm		#
#																						#
#	node 16																				#
#	-------																				#
#    FX: -39.9 kN, FY: -2.47 kN, FZ: 4.49 kN, MX: 0.85 Nm, MY: 5.2 Nm, MZ: 41.2 Nm		#
#																						#
#---------------------------------------------------------------------------------------#
#
#
#
#
#
#------------------------------------
SOLUTION, xbeam2n_crane-1, Static
#------------------------------------
	MESHES, 1
	LOADS, force_load-1
	BOUNDARIES, boundary-1
#------------------------------------
RESULTS, xbeam2n_crane-1
#------------------------------------
	DISPLACEMENT, plot, 1
	NODEFORCE, plot, 999
	ELEMENTFORCE, plot, 1
#
#
#
#
#
MATERIAL, Isotropic, steel, 200000000000.0, 0.25, 1.0
#
#
#
SECTION, BeamSect, 0, steel, 0.001400000000000001, 5.61666666666667e-07, 1.7366666666666681e-06, CrossSection, Rectangle, 0.1, 0.05, 0.09, 0.04
SECTION, BeamSect, 1, steel, 0.0005, 5.416666666666665e-08, 5.416666666666665e-08, CrossSection, Rectangle, 0.03, 0.03, 0.02, 0.02
#
#
#
BOUNDARY, Displacement, boundary-1, 1, 0., 1, 2, 3, 4, 5, 6
#
#
#
LOAD, Force, force_load-1, 2, 10000, 0., -1., 0.
#
#
#
SET_NODES, 1, 6, 8, 14, 16
SET_NODES, 2, 4, 12
SET_NODES, 999, 1 - 16
#
#
#
SET_ELEMENTS, 1, 1 - 32
SET_ELEMENTS, 3, 2, 7 - 10, 14, 19 - 22, 25 - 32
SET_ELEMENTS, 2, 1, 3 - 6, 11 - 13, 15 - 18, 23, 24
SET_ELEMENTS, 4, 1
SET_ELEMENTS, 5, 2
SET_ELEMENTS, 6, 3
SET_ELEMENTS, 7, 4 - 6
SET_ELEMENTS, 8, 7
SET_ELEMENTS, 9, 8
SET_ELEMENTS, 10, 9
SET_ELEMENTS, 11, 10
SET_ELEMENTS, 12, 11
SET_ELEMENTS, 13, 12
SET_ELEMENTS, 14, 13
SET_ELEMENTS, 15, 14
SET_ELEMENTS, 16, 15
SET_ELEMENTS, 17, 16, 18
SET_ELEMENTS, 18, 17, 18
SET_ELEMENTS, 19, 19
SET_ELEMENTS, 20, 20
SET_ELEMENTS, 21, 21
SET_ELEMENTS, 22, 22
SET_ELEMENTS, 23, 23
SET_ELEMENTS, 24, 24
SET_ELEMENTS, 25, 25, 27, 28, 30, 32
SET_ELEMENTS, 26, 26
SET_ELEMENTS, 27, 29
SET_ELEMENTS, 28, 31
#
#
#
NODE, 1, 4.0, 0.75, 0.449999988
NODE, 2, 6.0, 1.125, 0.675000012
NODE, 3, 5.33333349, 1.33333337, 0.600000024
NODE, 4, 8.0, 1.5, 0.899999976
NODE, 5, 2.0, 0.375, 0.224999994
NODE, 6, 0.0, 0.0, 0.0
NODE, 7, 2.66666675, 1.16666663, 0.300000012
NODE, 8, 0.0, 1.0, 0.0
NODE, 9, 4.0, 0.75, 1.54999995
NODE, 10, 6.0, 1.125, 1.32500005
NODE, 11, 5.33333349, 1.33333337, 1.39999998
NODE, 12, 8.0, 1.5, 1.10000002
NODE, 13, 2.0, 0.375, 1.77499998
NODE, 14, 0.0, 0.0, 2.0
NODE, 15, 2.66666675, 1.16666663, 1.70000005
NODE, 16, 0.0, 1.0, 2.0
#
#
#
ELEMENT, BEAM2N, 1, 0, 1, 2
ELEMENT, BEAM2N, 2, 1, 3, 2
ELEMENT, BEAM2N, 3, 0, 3, 4
ELEMENT, BEAM2N, 4, 0, 2, 4
ELEMENT, BEAM2N, 5, 0, 5, 1
ELEMENT, BEAM2N, 6, 0, 6, 5
ELEMENT, BEAM2N, 7, 1, 1, 3
ELEMENT, BEAM2N, 8, 1, 7, 1
ELEMENT, BEAM2N, 9, 1, 8, 5
ELEMENT, BEAM2N, 10, 1, 5, 7
ELEMENT, BEAM2N, 11, 0, 8, 7
ELEMENT, BEAM2N, 12, 0, 7, 3
ELEMENT, BEAM2N, 13, 0, 9, 10
ELEMENT, BEAM2N, 14, 1, 11, 10
ELEMENT, BEAM2N, 15, 0, 11, 12
ELEMENT, BEAM2N, 16, 0, 10, 12
ELEMENT, BEAM2N, 17, 0, 13, 9
ELEMENT, BEAM2N, 18, 0, 14, 13
ELEMENT, BEAM2N, 19, 1, 9, 11
ELEMENT, BEAM2N, 20, 1, 15, 9
ELEMENT, BEAM2N, 21, 1, 16, 13
ELEMENT, BEAM2N, 22, 1, 13, 15
ELEMENT, BEAM2N, 23, 0, 16, 15
ELEMENT, BEAM2N, 24, 0, 15, 11
ELEMENT, BEAM2N, 25, 1, 13, 5
ELEMENT, BEAM2N, 26, 1, 5, 15
ELEMENT, BEAM2N, 27, 1, 15, 7
ELEMENT, BEAM2N, 28, 1, 9, 1
ELEMENT, BEAM2N, 29, 1, 1, 11
ELEMENT, BEAM2N, 30, 1, 11, 3
ELEMENT, BEAM2N, 31, 1, 3, 10
ELEMENT, BEAM2N, 32, 1, 10, 2
#
#
#
