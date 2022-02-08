#
#
#
#
#-----------------------------------------------------------------------------------------------#
#		solution: xbeam2n2d_beam-1																#
#-----------------------------------------------#-----------------------------------------------#
#	EXPECTED REACTION FORCES					#	EXPECTED DISPLACEMENT						#
#												#												#
#	nodes 1 and 15								#	node 8										#
#	--------------								#	------										#
#	 x:  0.0, y: 200 N, mz: 0.0 Nmm				#	 x: 0.0 mm,  y: -0.181159 mm				#
#												#												#
#		RF = F1*L/2								#			5*F1*L^3							#
#												#	   -y = --------							#
#-----------------------------------------------#			 384*EI								#
#												#												#
#												#-----------------------------------------------#
#
#														(2 N/mm)
#														  [F1]
#
#		  ---------------------------------------------------------------------------------------------------
#		  |		 |		|	   |      |		 |		|	   |	  |	     |	    |	   |	  |	     |		|
#		  |		 |		|	   |	  |		 |		|	   |	  |	  	 | 	    |	   |	  |	     |		|
#		  |		 |		|	   |	  |		 |		|	   |	  |      |	    |	   |	  |	     |		|
#		  V		 V		V	   V 	  V		 V 		V	   V	  V      V 	    V	   V	  V      V		V
#		( 1)###( 2)###( 3)###( 4)###( 5)###( 6)###( 7)###( 8)###( 9)###(10)###(11)###(12)###(13)###(14)###(15)
#		 /\	 1		2	   3	  4		 5		6	   7	  8		 9		10	   11	  12	 13		14 /\
#		/  \																							  /  \
#	  --------						[EI]																--------
#	   [BC1]																							--------
#																										  [BC2]
#
#		  |------------------------------------------------------------------------------------------------|
#														[L]
#													  (200 mm)
#--------------------------
SOLUTION, xbeam2n2d_beam-1, Static
#--------------------------
	LOADS, distributed_load_F1
	BOUNDARIES, fixed_nodes_BC1
	BOUNDARIES, fixed_nodes_BC2
#--------------------------
RESULTS, xbeam2n2d_beam-1
#--------------------------
	DISPLACEMENT, text, 2
	NODEFORCE, plot, 1
	ELEMENTFORCE, plot, 1, text, 1
#
#
#
#
#
#
#
#-----------------------------------------------------------------------------------------------#
#		solution: xbeam2n2d_beam-2																#
#-----------------------------------------------#-----------------------------------------------#
#	EXPECTED REACTION FORCES					#	EXPECTED DISPLACEMENT						#
#												#												#
#	node 1										#												#
#	------										#				2*F1*L^4						#
#	 x:  0.0, y: 250 N, mz: 10000 Nmm			#	   -y_max = -------- = 0.075409	mm			#
#												#			 	 369*EI							#
#	node 15										#												#
#	-------										#-----------------------------------------------#
#	 x:  0.0, y: 150 N, mz: 0.0 Nmm				#
#												#
#		 F1*L^2			  5*F1*L	     3*F1*L #
#	M1 = ------		RF1 = ------   RF2 = ------ #	
#		   8 				8			   8	#
#												#
#-----------------------------------------------#
#
#														(2 N/mm)
#														  [F1]
#
#			  ---------------------------------------------------------------------------------------------------
#			  |		 |		|	   |      |		 |		|	   |	  |	     |	    |	   |	  |	     |		|
#			  |		 |		|	   |	  |		 |		|	   |	  |	  	 | 	    |	   |	  |	     |		|
#		  /|  |		 |		|	   |	  |		 |		|	   |	  |      |	    |	   |	  |	     |		|
#		  /|  V		 V		V	   V 	  V		 V 		V	   V	  V      V 	    V	   V	  V      V		V
#	 [BC3]/|( 1)###( 2)###( 3)###( 4)###( 5)###( 6)###( 7)###( 8)###( 9)###(10)###(11)###(12)###(13)###(14)###(15)
#		  /|	 1		2	   3	  4		 5		6	   7	  8		 9		10	   11	  12	 13		14 /\
#		  /|																								  /  \
#										[EI]																--------
#		 																									--------
#																											  [BC2]
#	
#			  |------------------------------------------------------------------------------------------------|
#														[L]
#													  (200 mm)
#--------------------------
SOLUTION, xbeam2n2d_beam-2, Static
#--------------------------
	LOADS, distributed_load_F1
	BOUNDARIES, fixed_nodes_BC3
	BOUNDARIES, fixed_nodes_BC2
#--------------------------
RESULTS, xbeam2n2d_beam-2
#--------------------------
	DISPLACEMENT, text, 2
	NODEFORCE, plot, 1
	ELEMENTFORCE, plot, 1, text, 1
#
#
#
#
#
#
#
#-----------------------------------------------------------------------------------------------#
#		solution: xbeam2n2d_beam-3																#
#-----------------------------------------------#-----------------------------------------------#
#	EXPECTED REACTION FORCES					#	EXPECTED DISPLACEMENT						#
#												#												#
#	nodes 1 and 15								#	node 8										#
#	--------------								#	------										#
#	 x:  0.0, y: 200 N, mz: 6666.7 Nmm			#	 x: 0.0 mm,  y: -0,03623 mm					#
#												#												#
#		F1*L^2			 F1*L	   				#			F1*L^4								#
#	M = ------		RF = ----					#	   -y = ------								#
#		  12			  2						#			384*EI								#
#												#												#
#-----------------------------------------------#-----------------------------------------------#
#
#														(2 N/mm)
#														  [F1]
#
#			  ---------------------------------------------------------------------------------------------------
#			  |		 |		|	   |      |		 |		|	   |	  |	     |	    |	   |	  |	     |		|
#			  |		 |		|	   |	  |		 |		|	   |	  |	  	 | 	    |	   |	  |	     |		|
#		  /|  |		 |		|	   |	  |		 |		|	   |	  |      |	    |	   |	  |	     |		| |\
#		  /|  V		 V		V	   V 	  V		 V 		V	   V	  V      V 	    V	   V	  V      V		V |\
#	 [BC3]/|( 1)###( 2)###( 3)###( 4)###( 5)###( 6)###( 7)###( 8)###( 9)###(10)###(11)###(12)###(13)###(14)###(15)|\[BC4]
#		  /|	 1		2	   3	  4		 5		6	   7	  8		 9		10	   11	  12	 13		14	  |\
#		  /|																								 	  |\
#										[EI]																
#																											
#	
#			  |------------------------------------------------------------------------------------------------|
#														[L]
#													  (200 mm)
#--------------------------
SOLUTION, xbeam2n2d_beam-3, Static
#--------------------------
	LOADS, distributed_load_F1
	BOUNDARIES, fixed_nodes_BC3
	BOUNDARIES, fixed_nodes_BC4
#--------------------------
RESULTS, xbeam2n2d_beam-3
#--------------------------
	DISPLACEMENT, text, 2
	NODEFORCE, plot, 1
	ELEMENTFORCE, plot, 1, text, 1
#
#
#
#
#
#
#
#-----------------------------------------------------------------------------------------------#
#		solution: xbeam2n2d_beam-4																#
#-----------------------------------------------#-----------------------------------------------#
#	EXPECTED REACTION FORCES					#	EXPECTED DISPLACEMENT						#
#												#												#
#	node 1										#	node 15										#
#	------										#	-------										#
#	 x:  0.0, y: 450 N, mz: 50000 Nmm			#	 x: 0.0 mm,  y: -2.319072 mm				#
#												#												#
#		 F1*L^2									#			F1*L^4	 F2*L^3						#
#	M1 = ------ + F2*L		RF1 = F1*L + F2		#	   -y = ------ + ------						#
#		    2									#			 8*EI	  3*EI						#
#												#												#
#-----------------------------------------------#-----------------------------------------------#
#
#														(2 N/mm)
#														  [F1]
#
#			  ---------------------------------------------------------------------------------------------------
#			  |		 |		|	   |      |		 |		|	   |	  |	     |	    |	   |	  |	     |		|
#			  |		 |		|	   |	  |		 |		|	   |	  |	  	 | 	    |	   |	  |	     |		|
#		  /|  |		 |		|	   |	  |		 |		|	   |	  |      |	    |	   |	  |	     |		|
#		  /|  V		 V		V	   V 	  V		 V 		V	   V	  V      V 	    V	   V	  V      V		V
#  	 [BC3]/|( 1)###( 2)###( 3)###( 4)###( 5)###( 6)###( 7)###( 8)###( 9)###(10)###(11)###(12)###(13)###(14)###(15)
#		  /|	 1		2	   3	  4		 5		6	   7	  8		 9		10	   11	  12	 13		14 ||
#		  /|																								   ||
#										[EI]																   ||
#																											   ||
#																											   ||
#																											  \  /
#																											   \/
#	
#																											  [F2]
#																											 (50 N)
#	
#			  |--------------------------------------------------------------------------------------------------|
#															[L]
#														  (200 mm)
#--------------------------
SOLUTION, xbeam2n2d_beam-4, Static
#--------------------------
	LOADS, distributed_load_F1
	LOADS, concentrated_load_F2
	BOUNDARIES, fixed_nodes_BC3
#--------------------------
RESULTS, xbeam2n2d_beam-4
#--------------------------
	DISPLACEMENT, text, 3
	NODEFORCE, plot, 1
	ELEMENTFORCE, plot, 1, text, 1
#
#
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
SET_NODES, 2, 8
SET_NODES, 3, 15
#
#
#			 num elements
SET_ELEMENTS, 1, 1 - 14
#
#
#        	type	   name	  	 E     v      p
MATERIAL, Isotropic, aluminum, 69000, 0.29, 2.7e-9
#
#
#          type   num material area	 Izz
SECTION, BeamSect, 1, aluminum, 100, 3333.333, 208.333, CrossSection, Rectangle, 5., 20., 0., 0.
#
#
#      type    			 name      node-/elementset force  vector
LOAD, ForceDistributed, distributed_load_F1,    1,    2.0, 0.0, -1.0, 0.0
LOAD, ForceConcentrated, concentrated_load_F2,  3,   50.0, 0.0, -1.0, 0.0
#
#
#			  type			name	     nodeset disp DOFs
BOUNDARY, Displacement, fixed_nodes_BC1,	1,   0.0, 1, 2
BOUNDARY, Displacement, fixed_nodes_BC2,	3,   0.0, 2
BOUNDARY, Displacement, fixed_nodes_BC3,	1,   0.0, 1, 2, 6
BOUNDARY, Displacement, fixed_nodes_BC4,	3,   0.0, 1, 2, 6
#
#
#
#
#     num   x     y
NODE,  1,     0.0,  0.0
NODE,  2,  14.285,  0.0
NODE,  3,   28.57,  0.0
NODE,  4,  42.855,  0.0
NODE,  5,   57.14,  0.0
NODE,  6,  71.425,  0.0
NODE,  7,   85.71,  0.0
NODE,  8,  99.995,  0.0
NODE,  9,  114.28,  0.0
NODE, 10, 128.565,  0.0
NODE, 11,  142.85,  0.0
NODE, 12, 157.135,  0.0
NODE, 13,  171.42,  0.0
NODE, 14, 185.705,  0.0
NODE, 15,   200.0,  0.0
#
#
#         type     num sect n1  n2
ELEMENT, BEAM2N2D,  1,   1,  1,  2
ELEMENT, BEAM2N2D,  2,   1,  2,  3
ELEMENT, BEAM2N2D,  3,   1,  3,  4
ELEMENT, BEAM2N2D,  4,   1,  4,  5
ELEMENT, BEAM2N2D,  5,   1,  5,  6
ELEMENT, BEAM2N2D,  6,   1,  6,  7
ELEMENT, BEAM2N2D,  7,   1,  7,  8
ELEMENT, BEAM2N2D,  8,   1,  8,  9
ELEMENT, BEAM2N2D,  9,   1,  9, 10
ELEMENT, BEAM2N2D, 10,   1, 10, 11
ELEMENT, BEAM2N2D, 11,   1, 11, 12
ELEMENT, BEAM2N2D, 12,   1, 12, 13
ELEMENT, BEAM2N2D, 13,   1, 13, 14
ELEMENT, BEAM2N2D, 14,   1, 14, 15
#
#
#
