#
#
#
#
#-----------------------------------------------#
#												#
#				[w]								#
#		  ----------------						#
#		  |  |  |  |  |  |						#
#		  v  v  v  v  v  v		EI				#
#	<BC1>-------------------___					#
#				L			   --				#
#								 --				#
#								   -			#
#									|			#
#						   + ------	|<--[P]		#
#							   R				#
#												#
#	DISPLACEMENTS FROM TEXTBOOK					#
#												#
#		 	piPR^3	 LPR^3	 wRL^3				#
#	x_max = ------ + ----- + -----				#
#			 4EI	  EI	  6EI				#
#												#
#	node 20										#
#	-------										#
#	 x: -2.587E-3								#
#												#
#												#
#	REACTION FORCES FROM TEXTBOOK				#
#												#
#	node 1										#
#	------										#
#	 fx: 100 N, fy: 250 N, mz: 400 Nm			#
#												#
#-----------------------------------------------#
#
#
#
#
#
#
#------------------------------------
SOLUTION, xbeam2n2d_fixed_beam, Static
#------------------------------------
	MESHES, 1
	LOADS, force_load-1
	LOADS, force_load-2
	BOUNDARIES, boundary-1
#------------------------------------
RESULTS, xbeam2n2d_fixed_beam
#------------------------------------
	DISPLACEMENT, plot, 2, text, 2
	STRESS, plot, 1
	STRAIN, plot, 1
	NODEFORCE, plot, 999
	ELEMENTFORCE, plot, 1
#
#
#
#
#
MATERIAL, Isotropic, steel, 200e9, 0.25
#
#
#
SECTION, BeamSect, 0, steel, 0.0014, 2.298337e-06
#
#
#
#
#
#
BOUNDARY, Displacement, boundary-1, 1, 0., 1, 2, 3, 4, 5, 6
#
#
#
LOAD, ForceConcentrated, force_load-1, 2, 100, -1, 0, 0.
LOAD, ForceDistributed, force_load-2, 2, 125, 0., -1, 0.
#
#
#
SET_NODES, 1, 1
SET_NODES, 2, 20
SET_NODES, 3, 2 - 11
SET_NODES, 999, 1 - 20
#
#
#
SET_ELEMENTS, 1, 1 - 19
SET_ELEMENTS, 2, 1 - 10
#
#
#
NODE, 1, 0.0, 0.0, 0.0
NODE, 2, 0.2, 0.0, 0.0
NODE, 3, 0.4, 0.0, 0.0
NODE, 4, 0.6000000000000001, 0.0, 0.0
NODE, 5, 0.8, 0.0, 0.0
NODE, 6, 1.0, 0.0, 0.0
NODE, 7, 1.2, 0.0, 0.0
NODE, 8, 1.4, 0.0, 0.0
NODE, 9, 1.5999999999999999, 0.0, 0.0
NODE, 10, 1.7999999999999998, 0.0, 0.0
NODE, 11, 1.9999999999999998, 0.0, 0.0
NODE, 12, 2.260472266500395, -0.022788370481687803, 0.0
NODE, 13, 2.5130302149885027, -0.09046106882113714, 0.0
NODE, 14, 2.7499999999999996, -0.20096189432334155, 0.0
NODE, 15, 2.9641814145298087, -0.35093333532153226, 0.0
NODE, 16, 3.149066664678467, -0.5358185854701903, 0.0
NODE, 17, 3.299038105676658, -0.7499999999999992, 0.0
NODE, 18, 3.409538931178863, -0.9869697850114961, 0.0
NODE, 19, 3.4772116295183126, -1.2395277334996038, 0.0
NODE, 20, 3.500000000000001, -1.4999999999999993, 0.0
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
#
#
#
