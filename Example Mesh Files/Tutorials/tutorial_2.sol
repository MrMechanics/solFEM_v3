#
#
#
#
#
#
#	TUTORIAL 2 (ROD2N elements)
#
#
#	Show how to:
#	------------
#	Create mesh from scratch
#	Create nodes and elements
#	Copy elements and fuse nodes
#	Create nodesets and elementsets
#	Create material and section
#	Apply section
#	Create solutions
#	Apply boundary conditions
#	Apply uniform load
#	Write to *.sol file
#	Run solver from viewer
#	Load results from *.out file
#	
#
#
#
#
#
#
#------------------------------------
SOLUTION, tutorial_2-1, Static
#------------------------------------
	MESHES, 1
	LOADS, force_load-1
	BOUNDARIES, boundary-1
#------------------------------------
RESULTS, tutorial_2-1
#------------------------------------
	DISPLACEMENT, plot, 1
	STRESS, text, 1
	STRAIN, text, 1
	NODEFORCE, plot, 999
	ELEMENTFORCE, plot, 1
#
#
#
#
#------------------------------------
SOLUTION, tutorial_2-2, Eigenmodes
#------------------------------------
	MESHES, 1
	BOUNDARIES, boundary-2
#------------------------------------
RESULTS, tutorial_2-2
#------------------------------------
	MODESHAPES, 8
#
#
#
#
#
MATERIAL, Isotropic, steel, 200000000000.0, 0.25, 7800.0
#
#
#
SECTION, RodSect, 0, steel, 0.02
#
#
#
#
#
#
#
#
#
BOUNDARY, Displacement, boundary-1, 2, 0., 1, 2, 3, 4, 5, 6
BOUNDARY, Displacement, boundary-2, 2, 0., 1, 2, 3, 4, 5, 6
#
#
#
LOAD, Force, force_load-1, 1, 420000, 0., -1, 0.
#
#
#
#
#
#
#
#
#
SET_NODES, 1, 1, 3
SET_NODES, 2, 27 - 29
SET_NODES, 999, 1 - 5, 7, 9, 10, 12 - 14, 17 - 19, 22 - 24, 27 - 29
#
#
#
SET_ELEMENTS, 1, 1 - 53
#
#
#
NODE, 1, 0.0, 0.0, 0.0
NODE, 2, 1.0, 0.0, 0.0
NODE, 3, 0.0, 0.0, 1.0
NODE, 4, 1.0, 0.0, 1.0
NODE, 5, 1.0, 1.0, 0.5
NODE, 7, 2.0, 0.0, 0.0
NODE, 9, 2.0, 0.0, 1.0
NODE, 10, 2.0, 1.0, 0.5
NODE, 12, 3.0, 0.0, 1.0
NODE, 13, 3.0, 0.0, 0.0
NODE, 14, 3.0, 1.0, 0.5
NODE, 17, 4.0, 0.0, 1.0
NODE, 18, 4.0, 0.0, 0.0
NODE, 19, 4.0, 1.0, 0.5
NODE, 22, 5.0, 0.0, 1.0
NODE, 23, 5.0, 0.0, 0.0
NODE, 24, 5.0, 1.0, 0.5
NODE, 27, 6.0, 0.0, 1.0
NODE, 28, 6.0, 0.0, 0.0
NODE, 29, 6.0, 1.0, 0.5
#
#
#
ELEMENT, ROD2N, 1, 0, 1, 2
ELEMENT, ROD2N, 2, 0, 3, 4
ELEMENT, ROD2N, 3, 0, 1, 3
ELEMENT, ROD2N, 4, 0, 1, 4
ELEMENT, ROD2N, 5, 0, 1, 5
ELEMENT, ROD2N, 6, 0, 2, 5
ELEMENT, ROD2N, 7, 0, 3, 5
ELEMENT, ROD2N, 8, 0, 4, 5
ELEMENT, ROD2N, 9, 0, 2, 7
ELEMENT, ROD2N, 10, 0, 4, 9
ELEMENT, ROD2N, 11, 0, 2, 4
ELEMENT, ROD2N, 12, 0, 2, 9
ELEMENT, ROD2N, 13, 0, 2, 10
ELEMENT, ROD2N, 14, 0, 7, 10
ELEMENT, ROD2N, 15, 0, 4, 10
ELEMENT, ROD2N, 16, 0, 9, 10
ELEMENT, ROD2N, 17, 0, 9, 12
ELEMENT, ROD2N, 18, 0, 13, 14
ELEMENT, ROD2N, 19, 0, 9, 14
ELEMENT, ROD2N, 20, 0, 12, 14
ELEMENT, ROD2N, 21, 0, 7, 13
ELEMENT, ROD2N, 22, 0, 7, 9
ELEMENT, ROD2N, 23, 0, 7, 12
ELEMENT, ROD2N, 24, 0, 7, 14
ELEMENT, ROD2N, 25, 0, 12, 17
ELEMENT, ROD2N, 26, 0, 18, 19
ELEMENT, ROD2N, 27, 0, 12, 19
ELEMENT, ROD2N, 28, 0, 17, 19
ELEMENT, ROD2N, 29, 0, 13, 18
ELEMENT, ROD2N, 30, 0, 13, 12
ELEMENT, ROD2N, 31, 0, 13, 17
ELEMENT, ROD2N, 32, 0, 13, 19
ELEMENT, ROD2N, 33, 0, 17, 22
ELEMENT, ROD2N, 34, 0, 23, 24
ELEMENT, ROD2N, 35, 0, 17, 24
ELEMENT, ROD2N, 36, 0, 22, 24
ELEMENT, ROD2N, 37, 0, 18, 23
ELEMENT, ROD2N, 38, 0, 18, 17
ELEMENT, ROD2N, 39, 0, 18, 22
ELEMENT, ROD2N, 40, 0, 18, 24
ELEMENT, ROD2N, 41, 0, 22, 27
ELEMENT, ROD2N, 42, 0, 28, 29
ELEMENT, ROD2N, 43, 0, 22, 29
ELEMENT, ROD2N, 44, 0, 27, 29
ELEMENT, ROD2N, 45, 0, 23, 28
ELEMENT, ROD2N, 46, 0, 23, 22
ELEMENT, ROD2N, 47, 0, 23, 27
ELEMENT, ROD2N, 48, 0, 23, 29
ELEMENT, ROD2N, 49, 0, 5, 10
ELEMENT, ROD2N, 50, 0, 10, 14
ELEMENT, ROD2N, 51, 0, 14, 19
ELEMENT, ROD2N, 52, 0, 19, 24
ELEMENT, ROD2N, 53, 0, 24, 29
#
#
#
