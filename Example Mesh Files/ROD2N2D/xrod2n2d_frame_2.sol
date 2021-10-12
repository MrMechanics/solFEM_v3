#
#
#
#
#-----------------------------------------------------------------------------------#
#																					#
#		ANSWERS FROM TEXTBOOK:														#
#																					#
#		Reaction Forces:  28.0 (node 1), 28.0 (node 12)								#
#		Displacements:	 [0.8475, -2.42194] (node 7), [1.695, 0.0] (node 12)		#
#		Element Forces:   -62.6099 (elements 7, 12), 56.0 (elements 1, 2, 5, 6),	#
#						  12.0 (element 15), 10.0 (elements 13, 17)					#
#																					#
#																					#
#								 9 __-( 6)-__ 10									#
#								_--		|	 --_									#
#					   8 __-( 4)_		|15		( 8)-__ 11							#
#					  _--	  |  -_19   |	20_-  |	   --_							#
#			 7	__( 2)__ 18	  |	   -_	|	_-	  |	  21  _(10)__  12				#
#			__--    |	--__  |14    -_ | _-	16|	 __--	|	--__				#
#		  --	  13|		--|		   -|-		  |--		|17		--				#
#  <BC1>( 1)------( 3)------( 5)------( 7)------( 9)------(11)------(12)<BC2>		#
#			   1	|	 2	  |	   3	|	 4	  |	   5	|	6					#
#					|		  |		    |		  |			|						#
#					|		  |			|		  |			|						#
#					v		  v			v		  v			v						#
#				  [F1]		[F1]	  [F2]		[F1]	  [F1]						#
#																					#
#-----------------------------------------------------------------------------------#
#
#
#
#
#
#--------------------------
SOLUTION, rod2n2d_2, Static
#--------------------------
	LOADS, load_1
	LOADS, load_2
	BOUNDARIES, fixed_nodes
	BOUNDARIES, sliding_nodes
#--------------------------
RESULTS, rod2n2d_2
#--------------------------
	DISPLACEMENT, text, 5
	NODEFORCE, plot, 5, text, 6
	ELEMENTFORCE, plot, 1, text, 1
#
#
#
#
#
#		  num nodes
SET_NODES, 1, 1
SET_NODES, 2, 12
SET_NODES, 3, 3, 5, 9, 11
SET_NODES, 4, 7
SET_NODES, 5, 1 - 12
SET_NODES, 6, 3, 5, 7, 9, 11
#
#
#
#			num elements
SET_ELEMENTS, 1, 1 - 21
SET_ELEMENTS, 2, 1 - 6
SET_ELEMENTS, 3, 7 - 12
#
#
#        	type	 name	  		E   v
MATERIAL, Isotropic, material-1, 1000., 0.29
#
#
#		  type	num material area
SECTION, RodSect, 1, material-1,  2.0
SECTION, RodSect, 2, material-1, 10.0
SECTION, RodSect, 3, material-1,  3.0
SECTION, RodSect, 4, material-1,  1.0
#
#
#      type   			  name  nodeset force  vector
LOAD, ForceConcentrated, load_1,   3,   10.0, 0.0, -1.0
LOAD, ForceConcentrated, load_2,   4,   16.0, 0.0, -1.0
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
NODE,  2, 10.0,  5.0
NODE,  3, 10.0,  0.0
NODE,  4, 20.0,  8.0
NODE,  5, 20.0,  0.0
NODE,  6, 30.0,  9.0
NODE,  7, 30.0,  0.0
NODE,  8, 40.0,  8.0
NODE,  9, 40.0,  0.0
NODE, 10, 50.0,  5.0
NODE, 11, 50.0,  0.0
NODE, 12, 60.0,  0.0
#
#
#
#         type   num sect n1  n2
ELEMENT, ROD2N2D,  1,  1,  1,  3
ELEMENT, ROD2N2D,  2,  1,  3,  5
ELEMENT, ROD2N2D,  3,  1,  5,  7
ELEMENT, ROD2N2D,  4,  1,  7,  9
ELEMENT, ROD2N2D,  5,  1,  9, 11
ELEMENT, ROD2N2D,  6,  1, 11, 12
ELEMENT, ROD2N2D,  7,  2,  1,  2
ELEMENT, ROD2N2D,  8,  2,  2,  4
ELEMENT, ROD2N2D,  9,  2,  4,  6
ELEMENT, ROD2N2D, 10,  2,  6,  8
ELEMENT, ROD2N2D, 11,  2,  8, 10
ELEMENT, ROD2N2D, 12,  2, 10, 12
ELEMENT, ROD2N2D, 13,  3,  2,  3
ELEMENT, ROD2N2D, 14,  3,  4,  5
ELEMENT, ROD2N2D, 15,  3,  6,  7
ELEMENT, ROD2N2D, 16,  3,  8,  9
ELEMENT, ROD2N2D, 17,  3, 10, 11
ELEMENT, ROD2N2D, 18,  4,  2,  5
ELEMENT, ROD2N2D, 19,  4,  4,  7
ELEMENT, ROD2N2D, 20,  4,  7,  8
ELEMENT, ROD2N2D, 21,  4,  9, 10
#
#
#
#
