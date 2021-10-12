#
#
#
#	results are a little bit different from
#	expected probably because there is no beam 
#	orientation setting in this program
#
#-----------------------------------------------#
#	EXPECTED DISPLACEMENTS						#
#												#
#	node 4										#
#	------										#
#    x: 2.312e-03, y: -1.882e-02, z: 1.266e-04	#
#	 magn: 1.897e-02							#
#-----------------------------------------------#
#
#
#
#
#------------------------------------
SOLUTION, solution-1, Static
#------------------------------------
	MESHES, 1
	LOADS, force_load-1
	BOUNDARIES, boundary-1
#------------------------------------
RESULTS, solution-1
#------------------------------------
	DISPLACEMENT, plot, 1, text, 2
	NODEFORCE, plot, 999, text, 1
	ELEMENTFORCE, plot, 1, text, 1
#
#
#
#
#
MATERIAL, Isotropic, steel, 200.0e9, 0.25, 1.
#
#
#
#          type   num material area	 Izz   Iyy
SECTION, BeamSect, 0, steel, 0.0014, 2.298337e-06, 1.73667e-06
SECTION, BeamSect, 1, steel, 0.000324, 7.9704e-08, 3.9852e-08
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
#
#
#
NODE,      1,           4.,         0.75,  0.449999988
NODE,      2,           6.,        1.125,  0.675000012
NODE,      3,   5.33333349,   1.33333337,  0.600000024
NODE,      4,           8.,          1.5,  0.899999976
NODE,      5,           2.,        0.375,  0.224999994
NODE,      6,           0.,           0.,           0.
NODE,      7,   2.66666675,   1.16666663,  0.300000012
NODE,      8,           0.,           1.,           0.
NODE,      9,           4.,         0.75,   1.54999995
NODE,     10,           6.,        1.125,   1.32500005
NODE,     11,   5.33333349,   1.33333337,   1.39999998
NODE,     12,           8.,          1.5,   1.10000002
NODE,     13,           2.,        0.375,   1.77499998
NODE,     14,           0.,           0.,           2.
NODE,     15,   2.66666675,   1.16666663,   1.70000005
NODE,     16,           0.,           1.,           2.
#
#
#
ELEMENT, BEAM2N,  1, 0,  1,  2
ELEMENT, BEAM2N,  2, 0,  3,  2
ELEMENT, BEAM2N,  3, 0,  4,  3
ELEMENT, BEAM2N,  4, 0,  2,  4
ELEMENT, BEAM2N,  5, 0,  5,  1
ELEMENT, BEAM2N,  6, 0,  6,  5
ELEMENT, BEAM2N,  7, 0,  1,  3
ELEMENT, BEAM2N,  8, 0,  7,  1
ELEMENT, BEAM2N,  9, 0,  8,  5
ELEMENT, BEAM2N, 10, 0,  5,  7
ELEMENT, BEAM2N, 11, 0,  7,  8
ELEMENT, BEAM2N, 12, 0,  3,  7
ELEMENT, BEAM2N, 13, 0,  9, 10
ELEMENT, BEAM2N, 14, 0, 11, 10
ELEMENT, BEAM2N, 15, 0, 12, 11
ELEMENT, BEAM2N, 16, 0, 10, 12
ELEMENT, BEAM2N, 17, 0, 13,  9
ELEMENT, BEAM2N, 18, 0, 14, 13
ELEMENT, BEAM2N, 19, 0,  9, 11
ELEMENT, BEAM2N, 20, 0, 15,  9
ELEMENT, BEAM2N, 21, 0, 16, 13
ELEMENT, BEAM2N, 22, 0, 13, 15
ELEMENT, BEAM2N, 23, 0, 15, 16
ELEMENT, BEAM2N, 24, 0, 11, 15
ELEMENT, BEAM2N, 25, 1,  5, 13
ELEMENT, BEAM2N, 26, 1,  5, 15
ELEMENT, BEAM2N, 27, 1,  7, 15
ELEMENT, BEAM2N, 28, 1,  1,  9
ELEMENT, BEAM2N, 29, 1,  1, 11
ELEMENT, BEAM2N, 30, 1,  3, 11
ELEMENT, BEAM2N, 31, 1,  3, 10
ELEMENT, BEAM2N, 32, 1,  2, 10
#
#
#
