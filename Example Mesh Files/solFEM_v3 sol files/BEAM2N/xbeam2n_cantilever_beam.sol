#
#
#
#
#
#
#-----------------------------------------------#
#	solution: xbeam2n_cantilever_beam-1			#
#-----------------------------------------------#
#	EXPECTED REACTION FORCES					#
#												#
#	node 1										#
#	------										#
#	 x:  0.0, y: 3000 N, mz: 2750 Nm			#
#												#
#		 F1*L^2									#
#	M1 = ------ + F2*L		RF1 = F1*L + F2		#	
#		    2									#
#												#
#-----------------------------------------------#
#	EXPECTED DISPLACEMENT						#
#												#
#	node 15										#
#	-------										#
#	 x: 0.0 m,  y: -0.0039108 m					#
#												#
#			F1*L^4	 F2*L^3						#
#	   -y = ------ + ------						#
#			 8*EI	  3*EI						#
#												#
#-----------------------------------------------#
#														(500 N/m)
#														  [F1]
#
#		  ---------------------------------------------------------------------------------------------------
#		  |		 |		|	   |      |		 |		|	   |	  |	     |	    |	   |	  |	     |		|
#		  |		 |		|	   |	  |		 |		|	   |	  |	  	 | 	    |	   |	  |	     |		|
#		  |		 |		|	   |	  |		 |		|	   |	  |      |	    |	   |	  |	     |		|
#		  V		 V		V	   V 	  V		 V 		V	   V	  V      V 	    V	   V	  V      V		V
#  <BC1>( 1)###( 2)###( 3)###( 4)###( 5)###( 6)###( 7)###( 8)###( 9)###(10)###(11)###(12)###(13)###(14)###(15)
#			 1		2	   3	  4		 5		6	   7	  8		 9		10	   11	  12	 13		14 ||
#																										   ||
#									[EI]																   ||
#																										   ||
#																										   ||
#																										  \  /
#																										   \/
#
#																										  [F2]
#																										(2500 N)
#
#		  |--------------------------------------------------------------------------------------------------|
#														[L]
#													   (1 m)
#
#
#
#--------------------------
SOLUTION, xbeam2n_cantilever_beam-1, Static
#--------------------------
	LOADS, distributed_load_F1
	LOADS, concentrated_force_F2
	BOUNDARIES, fixed_nodes_1
#--------------------------
RESULTS, xbeam2n_cantilever_beam-1
#--------------------------
	DISPLACEMENT, text, 3
	NODEFORCE, plot, 1
	ELEMENTFORCE, plot, 1, text, 1
#
#
#
#
#--------------------------
SOLUTION, xbeam2n_cantilever_beam-2, Eigenmodes
#--------------------------
	BOUNDARIES, fixed_nodes_1
#--------------------------
RESULTS, xbeam2n_cantilever_beam-2
#--------------------------
	MODESHAPES, 11
#
#
#
#
#--------------------------
SOLUTION, xbeam2n_cantilever_beam-3, ModalDynamic
#--------------------------
	BOUNDARIES, fixed_nodes_1
	DAMPINGS, damp_2
	LOADS, accel_nodes_1
#--------------------------
RESULTS, xbeam2n_cantilever_beam-3
#--------------------------
	DISPLACEMENT, plot, 3, 2, text, 3, 2
	VELOCITY, plot, 3, 2
	ACCELERATION, plot, 3, 2, text, 3, 2
	FRF_ACCEL, plot, 3, 2, text, 3, 2
	MODESHAPES, 12
#
#
#
#
#
#
#
#
#		  num nodes
SET_NODES, 1, 1
SET_NODES, 2, 2 - 15
SET_NODES, 3, 15
#
#
#			 num elements
SET_ELEMENTS, 1, 1 - 14
#
#
#		type	   num	load/damp name			filename
TABLE, Acceleration, 1, accel_nodes_1, id_sine_sweep.tab
TABLE, DampingRatio, 2, damp_2, id_damp1.tab
#
#
#        	type	   name	  	 E   		   v      p
MATERIAL, Isotropic, aluminum, 68900000000.0, 0.35, 2700.
#
#
#          type   num material area	 Izz
SECTION, BeamSect, 0, aluminum, 0.002, 3.3245867e-06, 1.3334167e-06, CrossSection, I-Beam, 0.1, 0.008, 0.005, 0.1, 0.008, 0.096
#
#
#		  type		name
DAMPING, Frequency, damp_2
#
#
#      type    			 name      node-/elementset force  vector
LOAD, ForceDistributed,  distributed_load_F1,   1,   500.0, 0.0, -1.0, 0.0
LOAD, ForceConcentrated, concentrated_force_F2, 3,  2500.0, 0.0, -1.0, 0.0
LOAD, Acceleration, 	 accel_nodes_1, 		1,    9.81, 0.0,  1.0, 0.0
#
#
#			  type			name	 nodeset disp DOFs
BOUNDARY, Displacement, fixed_nodes_1,	1,   0.0, 1, 2, 3, 4, 5, 6
#
#
#
#
#     num	   			   x    y    z
NODE, 1,      			  0.0, 0.0, 0.0
NODE, 2,  0.07142857142857142, 0.0, 0.0
NODE, 3,  0.14285714285714285, 0.0, 0.0
NODE, 4,  0.21428571428571427, 0.0, 0.0
NODE, 5,  0.28571428571428570, 0.0, 0.0
NODE, 6,  0.35714285714285715, 0.0, 0.0
NODE, 7,  0.42857142857142855, 0.0, 0.0
NODE, 8,  				  0.5, 0.0, 0.0
NODE, 9,  0.57142857142857140, 0.0, 0.0
NODE, 10, 0.64285714285714290, 0.0, 0.0
NODE, 11, 0.71428571428571430, 0.0, 0.0
NODE, 12, 0.78571428571428570, 0.0, 0.0
NODE, 13, 0.85714285714285710, 0.0, 0.0
NODE, 14, 0.92857142857142860, 0.0, 0.0
NODE, 15, 				  1.0, 0.0, 0.0
#
#
#
#         type  num sect n1  n2
ELEMENT, BEAM2N, 1,  0,   1,  2
ELEMENT, BEAM2N, 2,  0,   2,  3
ELEMENT, BEAM2N, 3,  0,   3,  4
ELEMENT, BEAM2N, 4,  0,   4,  5
ELEMENT, BEAM2N, 5,  0,   5,  6
ELEMENT, BEAM2N, 6,  0,   6,  7
ELEMENT, BEAM2N, 7,  0,   7,  8
ELEMENT, BEAM2N, 8,  0,   8,  9
ELEMENT, BEAM2N, 9,  0,   9, 10
ELEMENT, BEAM2N, 10, 0,  10, 11
ELEMENT, BEAM2N, 11, 0,  11, 12
ELEMENT, BEAM2N, 12, 0,  12, 13
ELEMENT, BEAM2N, 13, 0,  13, 14
ELEMENT, BEAM2N, 14, 0,  14, 15
#
#
#
