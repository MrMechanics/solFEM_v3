#
#
#
#
#-----------------------------------------------------------------------------------#
#																					#
#		REACTION FORCES FROM TEXTBOOK:												#
#																					#
#	node 1						node 9						node 14					#
#	------						------						-------					#
#	 x: 0kN,  y: 45.75kN		 x: 0kN,  y: -20.9kN		 x: 0kN,  y: 125.14kN	#
#																					#
#								 													#
#			   ( 2)---( 3)---( 4)-------( 5)-------( 6)---( 7)---( 8)				#
#			   /| \    |	 /| \		 /\		   /| \	   |	 /|	\				#
#			  / |  \   |    / |  \		/  \	  / |  \   |	/ |  \				#
#			 /  |   \  |   /  |	  \	   /    \	 /	|	\  |   /  |   \				#
#		    /   |    \ |  /   |	   \  /	 	 \	/	|	 \ |  /	  |	   \			#
#		   /    |	  \| /	  |		\/		  \/	|	  \| /	  |		\			#
#  <BC1>( 1)---(18)---(17)---(16)---(15)	(13)---(12)---(11)---(10)---( 9)<BC2>	#
#						|	   |	   \ 	 /										#
#						|	   |		\   / 										#
#						|	   |		 \ /										#
#				   		v	   v		 (14)										#
#					  [F1]	  [F1]	    <BC2>										#
#																					#
#-----------------------------------------------------------------------------------#
#
#
#
#
#
#--------------------------
SOLUTION, xrod2n2d_frame_2, Static
#--------------------------
	LOADS, load_1
	BOUNDARIES, fixed_nodes
	BOUNDARIES, sliding_nodes
#--------------------------
RESULTS, xrod2n2d_frame_2
#--------------------------
	DISPLACEMENT, text, 2
	NODEFORCE, plot, 4
	ELEMENTFORCE, plot, 1, text, 1
	STRESS, plot, 1, text, 1
#
#
#
#
#
#		  num nodes
SET_NODES, 1, 1
SET_NODES, 2, 9, 14
SET_NODES, 3, 16, 17
SET_NODES, 4, 1 - 18
#
#
#
#			num elements
SET_ELEMENTS, 1, 1 - 32
#
#
#        	type	 name	  		E   v
MATERIAL, Isotropic, material-1, 200e9, 0.25
#
#
#		  type	 num material    area
SECTION, RodSect, 0, material-1,  0.02
#
#
#      type   			  name  nodeset force  vector
LOAD, ForceConcentrated, load_1,   3,   75000., 0., -1.
#
#
#				type		name	  nodeset disp DOFs
BOUNDARY, Displacement, fixed_nodes,	 1,   0.0, 1, 2
BOUNDARY, Displacement, sliding_nodes,   2,   0.0, 2
#
#
#
#     num   x     y
NODE,  1,  0.0,  0.0
NODE,  2,  3.0,  3.0
NODE,  3,  6.0,  3.0
NODE,  4,  9.0,  3.0
NODE,  5, 13.5,  3.0
NODE,  6, 18.0,  3.0
NODE,  7, 21.0,  3.0
NODE,  8, 24.0,  3.0
NODE,  9, 27.0,  0.0
NODE, 10, 24.0,  0.0
NODE, 11, 21.0,  0.0
NODE, 12, 18.0,  0.0
NODE, 13, 15.0,  0.0
NODE, 14, 13.5, -1.5
NODE, 15, 12.0,  0.0
NODE, 16,  9.0,  0.0
NODE, 17,  6.0,  0.0
NODE, 18,  3.0,  0.0
#
#
#
#         type   num sect n1  n2
ELEMENT, ROD2N2D,  1,  0,  1,  2
ELEMENT, ROD2N2D,  2,  0,  2,  3
ELEMENT, ROD2N2D,  3,  0,  3,  4
ELEMENT, ROD2N2D,  4,  0,  4,  5
ELEMENT, ROD2N2D,  5,  0,  5,  6
ELEMENT, ROD2N2D,  6,  0,  6,  7
ELEMENT, ROD2N2D,  7,  0,  7,  8
ELEMENT, ROD2N2D,  8,  0,  8,  9
ELEMENT, ROD2N2D,  9,  0,  9, 10
ELEMENT, ROD2N2D, 10,  0, 10, 11
ELEMENT, ROD2N2D, 11,  0, 11, 12
ELEMENT, ROD2N2D, 12,  0, 12, 13
ELEMENT, ROD2N2D, 13,  0, 13, 14
ELEMENT, ROD2N2D, 14,  0, 14, 15
ELEMENT, ROD2N2D, 15,  0, 15, 16
ELEMENT, ROD2N2D, 16,  0, 16, 17
ELEMENT, ROD2N2D, 17,  0, 17, 18
ELEMENT, ROD2N2D, 18,  0,  1, 18
ELEMENT, ROD2N2D, 19,  0,  2, 18
ELEMENT, ROD2N2D, 20,  0,  2, 17
ELEMENT, ROD2N2D, 21,  0,  3, 17
ELEMENT, ROD2N2D, 22,  0,  4, 17
ELEMENT, ROD2N2D, 23,  0,  4, 16
ELEMENT, ROD2N2D, 24,  0,  4, 15
ELEMENT, ROD2N2D, 25,  0,  5, 15
ELEMENT, ROD2N2D, 26,  0,  5, 13
ELEMENT, ROD2N2D, 27,  0,  6, 13
ELEMENT, ROD2N2D, 28,  0,  6, 12
ELEMENT, ROD2N2D, 29,  0,  6, 11
ELEMENT, ROD2N2D, 30,  0,  7, 11
ELEMENT, ROD2N2D, 31,  0,  8, 11
ELEMENT, ROD2N2D, 32,  0,  8, 10
#
#
#
#
