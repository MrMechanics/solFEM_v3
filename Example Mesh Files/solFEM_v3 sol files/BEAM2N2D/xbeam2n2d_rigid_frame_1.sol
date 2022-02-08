#
#
#
#
#-----------------------------------------------#
#	REACTION FORCES AND ELEMENT FORCES			#
#		FROM TEXTBOOK							#
#												#
#	node 1										#
#	------										#
#	 x:  13.41kN, y: 100.75kN, mz: -28.52kNm	#
#												#
#	node 21										#
#	-------										#
#	 x: -56.97kN, y:      0kN, mz: 	   0kNm 	#
#												#
#	node 33										#
#	-------										#
#	 x: -24.40kN, y:  85.25kN, mz:	   0kNm 	#
#												#
#	elements 8-9								#
#	---------									#
#	 mz: 89.1kNm								#
#-----------------------------------------------#
#																	[L2]
#																	(6m)
#							  |-----------------------------------------------------------------------------------------------|
#																		  [F3]
#																		(25kN/m)
#							  -------------------------------------------------------------------------------------------------
#							  |		  |		  |		  |		  |		  |		  |		  |		  |		  |		  |		  |		  |
#							  |		  |		  |		  |		  |		  |		  |		  |		  |		  |		  |		  |		  |
#							  |		  |		  |		  |		  |		  |		  |		  |		  |		  |		  |		  |		  |   | |
#							  V		  V		  V		  V		  V		  V		  V		  V		  V		  V		  V		  V		  V  /| |
#		---			|------>( 9)####(10)####(11)####(12)####(13)####(14)####(15)####(16)####(17)####(18)####(19)####(20)####(21)/ | |[BC3] ---
#		 |			|		  #								 ||								 ||						|		  # \ | |		|
#		 |			|		  #								 ||			[EI]				 ||						|		  #  \| |		|
#		 |			|------>( 8)							 ||								 ||						|------>(22)  | |		|
#		 |			|		  #								 ||								 ||						|		  #				|
#		 |			|		  #								 ||								 ||						|		  #				|
#		 |			|------>( 7)							\  /							 ||						|------>(23)			|
#		 | 			|		  #								 \/								\  /					|		  #				|
#		 |			|		  #								[F1]							 \/						|		  #				|
#		 |			|------>( 6)						   (16kN)							[F2]					|------>(24)			|
#		 |			|		  #															   (20kN)					|		  #				|
#	[L1] |	 [F5]	|		  #																						|		  #				|
#	(4m) |	(8kN/m)	|------>( 5)																					|------>(25)			|
#		 |			|		  #																						|		  #				|
#		 |			|		  #																						|		  #				|
#		 |			|------>( 4)																					|------>(26)			| [L3]
#		 |			|		  #																				[F4]	|		  #				| (6m)
#		 |			|		  #																			   (6kN/m)	|		  #				|
#		 |			|------>( 3)																					|------>(27)			|
#		 |			|		  #																						|		  #				|
#		 |			|		  #																						|		  #				|
#		 |			|------>( 2)																					|------>(28)			|
#		 |			|		  #																						|		  #				|
#		 |			|		  #																						|		  #				|
#		 |			|------>( 1)																					|------>(29)			|
#		---				  --------																					|		  #				|
#						  / / / / 																					|		  #				|
#							[BC1]																					|------>(30)			|
#																													|		  #				|
#																													|		  #				|
#																													|------>(31)			|
#																													|		  #				|
#																													|		  #				|
#																													|------>(32)			|
#																													|		  #				|
#																													|		  #				|
#																													|------>(33)		   ---
#																															 /\
#																															/  \
#																														  --------
#																															[BC2]
#
#
#
#
#------------------------------------
SOLUTION, xbeam2n2d_rigid_frame_1-1, Static
#------------------------------------
	MESHES, 1
	LOADS, force_load-F1
	LOADS, force_load-F2
	LOADS, force_load-F3
	LOADS, force_load-F4
	LOADS, force_load-F5
	BOUNDARIES, boundary-BC1
	BOUNDARIES, boundary-BC2
	BOUNDARIES, boundary-BC3
#------------------------------------
RESULTS, xbeam2n2d_rigid_frame_1-1
#------------------------------------
	DISPLACEMENT, plot, 1
	NODEFORCE, plot, 999
	ELEMENTFORCE, plot, 1, text, 1
#
#
#
#
#
#
MATERIAL, Isotropic, steel, 200000000000.0, 0.25, 7870.0
#
#
#
SECTION, BeamSect, 0, steel, 0.004, 0.0005, 0.0
#
#
#		     type      name elm_set  x-vec
BEAMORIENT, BEAM2N2D, beams-1, 3, 1., 0., 0.
#
#
#
BOUNDARY, Displacement, boundary-BC1, 1, 0., 1, 2, 6
BOUNDARY, Displacement, boundary-BC2, 8, 0., 1, 2
BOUNDARY, Displacement, boundary-BC3, 2, 0., 1
#
#
#
LOAD, ForceConcentrated, force_load-F1, 3, 16000, 0., -1, 0.
LOAD, ForceConcentrated, force_load-F2, 4, 20000, 0., -1, 0.
LOAD, ForceDistributed, force_load-F3, 3, 25000, 0., -1, 0.
LOAD, ForceDistributed, force_load-F4, 4, 6000, 1, 0, 0.
LOAD, ForceDistributed, force_load-F5, 2, 8000, 1, 0, 0.
#
#
#
#
#
#
#
#
#
SET_NODES, 1, 1
SET_NODES, 2, 21
SET_NODES, 3, 13
SET_NODES, 4, 17
SET_NODES, 5, 9 - 20
SET_NODES, 6, 2 - 9
SET_NODES, 7, 22 - 32
SET_NODES, 8, 33
SET_NODES, 999, 1 - 33
#
#
#
SET_ELEMENTS, 1, 1 - 32
SET_ELEMENTS, 2, 1 - 8
SET_ELEMENTS, 3, 9 - 20
SET_ELEMENTS, 4, 21 - 32
#
#
#
NODE, 1, 0.0, 0.0, 0.0
NODE, 2, 0.0, 0.5, 0.0
NODE, 3, 0.0, 1.0, 0.0
NODE, 4, 0.0, 1.5, 0.0
NODE, 5, 0.0, 2.0, 0.0
NODE, 6, 0.0, 2.5, 0.0
NODE, 7, 0.0, 3.0, 0.0
NODE, 8, 0.0, 3.5, 0.0
NODE, 9, 0.0, 4.0, 0.0
NODE, 10, 0.5, 4.0, 0.0
NODE, 11, 1.0, 4.0, 0.0
NODE, 12, 1.5, 4.0, 0.0
NODE, 13, 2.0, 4.0, 0.0
NODE, 14, 2.5, 4.0, 0.0
NODE, 15, 3.0, 4.0, 0.0
NODE, 16, 3.5, 4.0, 0.0
NODE, 17, 4.0, 4.0, 0.0
NODE, 18, 4.5, 4.0, 0.0
NODE, 19, 5.0, 4.0, 0.0
NODE, 20, 5.5, 4.0, 0.0
NODE, 21, 6.0, 4.0, 0.0
NODE, 22, 6.0, 3.5, 0.0
NODE, 23, 6.0, 3.0, 0.0
NODE, 24, 6.0, 2.5, 0.0
NODE, 25, 6.0, 2.0, 0.0
NODE, 26, 6.0, 1.5, 0.0
NODE, 27, 6.0, 1.0, 0.0
NODE, 28, 6.0, 0.5, 0.0
NODE, 29, 6.0, 0.0, 0.0
NODE, 30, 6.0, -0.5, 0.0
NODE, 31, 6.0, -1.0, 0.0
NODE, 32, 6.0, -1.5, 0.0
NODE, 33, 6.0, -2.0, 0.0
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
ELEMENT, BEAM2N2D, 20, 0, 20, 21
ELEMENT, BEAM2N2D, 21, 0, 21, 22
ELEMENT, BEAM2N2D, 22, 0, 22, 23
ELEMENT, BEAM2N2D, 23, 0, 23, 24
ELEMENT, BEAM2N2D, 24, 0, 24, 25
ELEMENT, BEAM2N2D, 25, 0, 25, 26
ELEMENT, BEAM2N2D, 26, 0, 26, 27
ELEMENT, BEAM2N2D, 27, 0, 27, 28
ELEMENT, BEAM2N2D, 28, 0, 28, 29
ELEMENT, BEAM2N2D, 29, 0, 29, 30
ELEMENT, BEAM2N2D, 30, 0, 30, 31
ELEMENT, BEAM2N2D, 31, 0, 31, 32
ELEMENT, BEAM2N2D, 32, 0, 32, 33
#
#
#
