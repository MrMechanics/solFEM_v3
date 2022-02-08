#! /usr/bin/env python3
#
#
#	viewFEM.py
#  ------------
#
#	This is the viewFEM module. It reads results from
#	a finite element analysis in the form of *.out files.
#	These are binary files created by pickle, containing
#	node objects, element objects, mesh objects,
#	solution objects, etc. Results are from these and
#	viewed using PyQt5 gui with OpenGL.
#	


import sys
from copy import deepcopy

sys.path.insert(1, '../Objects')
sys.path.insert(1, '../Modules')

from camera import *
from geometry import *
from quaternion import *
from solFEM import *
from meshFEM import *
from helper import *
from selector import *
from converter import *

try:
	from OpenGL.GL import *
	from OpenGL.GLU import *
except:
	print(' Error PyOpenGL not installed properly!!')
	sys.exit()

try:
	from PyQt5 import QtGui, QtWidgets, QtCore
	from PyQt5.QtOpenGL import *
except:
	print(' Error PyQt5 not installed properly!!')
	sys.exit()





class UserInterface(QtWidgets.QMainWindow):
	'''
The main user interface (GUI). This holds all
toolbars and menus. The FE-viewer (Viewer object)
is an OpenGL widget running inside this framework.
'''
	def __init__(self):
		QtWidgets.QMainWindow.__init__(self)

		self.setWindowIcon(QtGui.QIcon('../Icons/icon_view_result.png'))
		self.setWindowTitle('viewFEM - Finite Element Viewer')
		self.statusBar().showMessage('  ready  ')

		self.model = Model(self)
		self.viewer = Viewer(self)

		self.current_savefile = 'None'

		self.new_deletion = {}
		self.new_mesh = {}
		self.new_node = {}
		self.new_node_movement = {}
		self.new_elements = {}
		self.new_extrusion = {}
		self.new_conversion = {}
		self.new_orientation = {}
		self.new_position = {}
		self.new_rotation = {}
		self.new_mesh_view = {}
		self.new_material = {}
		self.new_section = {}
		self.new_section_assignment = {}
		self.new_boundary = {}
		self.new_load = {}
		self.new_constraint = {}
		self.new_solution = {}
		self.new_solution_view = {}
		self.new_solfile = {}
		self.current_results = {'Solution': 'None', 'Result': 'None', 'Subresult': 'None'}

		self.new_file_import = {}
		self.new_results_open = {}
		self.new_model_open = {}
		
		exit = QtWidgets.QAction(QtGui.QIcon('../Icons/icon_exit.png'),'Exit', self)
		exit.setShortcut('Ctrl+Q')
		exit.setStatusTip('Exit application')
		exit.triggered.connect(self.close)
		
		newsession = QtWidgets.QAction(QtGui.QIcon('../Icons/icon_new_file.png'),'New', self)
		newsession.setStatusTip('Clear out current session')
		newsession.triggered.connect(self.clearModel)

		openfile = QtWidgets.QAction(QtGui.QIcon('../Icons/icon_open.png'),'Open', self)
		openfile.setStatusTip('Open *.out file')
		openfile.triggered.connect(self.openFile)

		importfrom = QtWidgets.QAction(QtGui.QIcon('../Icons/icon_import.png'),'Import', self)
		importfrom.setStatusTip('Import mesh from *.sol file')
		importfrom.triggered.connect(self.importFrom)

		export = QtWidgets.QAction(QtGui.QIcon('../Icons/icon_export.png'),'Export', self)
		export.setStatusTip('Export mesh to *.sol file')
		export.triggered.connect(self.exportMesh)

		savefile = QtWidgets.QAction(QtGui.QIcon('../Icons/icon_save.png'),'Save', self)
		savefile.setStatusTip('Save current session to *.mdl file')
		savefile.triggered.connect(self.saveFile)

		quicksave = QtWidgets.QAction(QtGui.QIcon('../Icons/icon_quick_save.png'),'Quick Save', self)
		quicksave.setShortcut('Ctrl+S')
		quicksave.setStatusTip('Save current session to *.mdl file')
		quicksave.triggered.connect(self.quickSaveFile)

		camerahelp = QtWidgets.QAction(QtGui.QIcon('../Icons/icon_origin_triad.png'),'Camera', self)
		camerahelp.setStatusTip('Help screen for instructions on how to move the camera')
		camerahelp.triggered.connect(self.cameraHelpScreen)

		selecthelp = QtWidgets.QAction(QtGui.QIcon('../Icons/icon_select_nodes.png'),'Selecting', self)
		selecthelp.setStatusTip('Help screen for instructions on how to select nodes and elements')
		selecthelp.triggered.connect(self.selectHelpScreen)

		meshhelp = QtWidgets.QAction(QtGui.QIcon('../Icons/icon_create_mesh.png'),'Meshes', self)
		meshhelp.setStatusTip('Help screen for creating, importing and manipulating mesh')
		meshhelp.triggered.connect(self.meshHelpScreen)

		materialhelp = QtWidgets.QAction(QtGui.QIcon('../Icons/icon_new_material.png'),'Materials', self)
		materialhelp.setStatusTip('Help screen for creating and using materials')
		materialhelp.triggered.connect(self.materialHelpScreen)

		sectionhelp = QtWidgets.QAction(QtGui.QIcon('../Icons/icon_beam_section.png'),'Sections', self)
		sectionhelp.setStatusTip('Help screen for creating and applying sections')
		sectionhelp.triggered.connect(self.sectionHelpScreen)

		solutionhelp = QtWidgets.QAction(QtGui.QIcon('../Icons/icon_current_solution.png'),'Solutions', self)
		solutionhelp.setStatusTip('Help screen for creating and setting up solutions')
		solutionhelp.triggered.connect(self.solutionHelpScreen)

		boundaryhelp = QtWidgets.QAction(QtGui.QIcon('../Icons/icon_boundary.png'),'Boundary Conditions', self)
		boundaryhelp.setStatusTip('Help screen for creating and applying boundary conditions')
		boundaryhelp.triggered.connect(self.boundaryHelpScreen)

		constrainthelp = QtWidgets.QAction(QtGui.QIcon('../Icons/icon_touch_lock.png'),'Multipoint Constraints', self)
		constrainthelp.setStatusTip('Help screen for creating and applying multipoint constraints')
		constrainthelp.triggered.connect(self.constraintHelpScreen)

		loadhelp = QtWidgets.QAction(QtGui.QIcon('../Icons/icon_uniform_load.png'),'Loads', self)
		loadhelp.setStatusTip('Help screen for creating and applying loads')
		loadhelp.triggered.connect(self.loadHelpScreen)

		solverhelp = QtWidgets.QAction(QtGui.QIcon('../Icons/icon_new_file.png'),'Solver Files', self)
		solverhelp.setStatusTip('Help screen for creating and running solver files')
		solverhelp.triggered.connect(self.solverHelpScreen)

		resulthelp = QtWidgets.QAction(QtGui.QIcon('../Icons/icon_current_results.png'),'Results', self)
		resulthelp.setStatusTip('Help screen for loading and displaying results')
		resulthelp.triggered.connect(self.resultHelpScreen)

		tutorialROD2N2D = QtWidgets.QAction(QtGui.QIcon('../Icons/pix_rod2_beam2.png'),'Tutorial 1', self)
		tutorialROD2N2D.setStatusTip('Launch tutorial 1 in new window')
		tutorialROD2N2D.triggered.connect(self.tutorialROD2N2DHelpScreen)

		tutorialROD2N = QtWidgets.QAction(QtGui.QIcon('../Icons/pix_rod2_beam2.png'),'Tutorial 2', self)
		tutorialROD2N.setStatusTip('Launch tutorial 2 in new window')
		tutorialROD2N.triggered.connect(self.tutorialROD2NHelpScreen)

		tutorialBEAM2N2D = QtWidgets.QAction(QtGui.QIcon('../Icons/pix_rod2_beam2.png'),'Tutorial 3', self)
		tutorialBEAM2N2D.setStatusTip('Launch tutorial 3 in new window')
		tutorialBEAM2N2D.triggered.connect(self.tutorialBEAM2N2DHelpScreen)

		tutorialBEAM2N = QtWidgets.QAction(QtGui.QIcon('../Icons/pix_rod2_beam2.png'),'Tutorial 4', self)
		tutorialBEAM2N.setStatusTip('Launch tutorial 4 in new window')
		tutorialBEAM2N.triggered.connect(self.tutorialBEAM2NHelpScreen)

		tutorialTRI3N = QtWidgets.QAction(QtGui.QIcon('../Icons/pix_tri3.png'),'Tutorial 5', self)
		tutorialTRI3N.setStatusTip('Launch tutorial 5 in new window')
		tutorialTRI3N.triggered.connect(self.tutorialTRI3NHelpScreen)

		tutorialTRI6N = QtWidgets.QAction(QtGui.QIcon('../Icons/pix_tri6.png'),'Tutorial 6', self)
		tutorialTRI6N.setStatusTip('Launch tutorial 6 in new window')
		tutorialTRI6N.triggered.connect(self.tutorialTRI6NHelpScreen)

		tutorialQUAD4N = QtWidgets.QAction(QtGui.QIcon('../Icons/pix_quad4.png'),'Tutorial 7', self)
		tutorialQUAD4N.setStatusTip('Launch tutorial 7 in new window')
		tutorialQUAD4N.triggered.connect(self.tutorialQUAD4NHelpScreen)

		tutorialQUAD8N = QtWidgets.QAction(QtGui.QIcon('../Icons/pix_quad8.png'),'Tutorial 8', self)
		tutorialQUAD8N.setStatusTip('Launch tutorial 8 in new window')
		tutorialQUAD8N.triggered.connect(self.tutorialQUAD8NHelpScreen)

		tutorialTET4N = QtWidgets.QAction(QtGui.QIcon('../Icons/pix_tet4.png'),'Tutorial 9', self)
		tutorialTET4N.setStatusTip('Launch tutorial 9 in new window')
		tutorialTET4N.triggered.connect(self.tutorialTET4NHelpScreen)

		tutorialTET10N = QtWidgets.QAction(QtGui.QIcon('../Icons/pix_tet10.png'),'Tutorial 10', self)
		tutorialTET10N.setStatusTip('Launch tutorial 10 in new window')
		tutorialTET10N.triggered.connect(self.tutorialTET10NHelpScreen)

		tutorialHEX8N = QtWidgets.QAction(QtGui.QIcon('../Icons/pix_hex8.png'),'Tutorial 11', self)
		tutorialHEX8N.setStatusTip('Launch tutorial 11 in new window')
		tutorialHEX8N.triggered.connect(self.tutorialHEX8NHelpScreen)

		tutorialHEX20N = QtWidgets.QAction(QtGui.QIcon('../Icons/pix_hex20.png'),'Tutorial 12', self)
		tutorialHEX20N.setStatusTip('Launch tutorial 12 in new window')
		tutorialHEX20N.triggered.connect(self.tutorialHEX20NHelpScreen)

		selectnodes = QtWidgets.QAction(QtGui.QIcon('../Icons/icon_select_nodes.png'),'Select Nodes', self)
		selectnodes.setStatusTip('Select nodes')
		selectnodes.triggered.connect(self.selectNodes)

		selectelements = QtWidgets.QAction(QtGui.QIcon('../Icons/icon_select_elements.png'),'Select Elements', self)
		selectelements.setStatusTip('Select elements')
		selectelements.triggered.connect(self.selectElements)

		delete = QtWidgets.QAction(QtGui.QIcon('../Icons/icon_delete.png'),'Delete', self)
		delete.setStatusTip('Delete sets, mesh, material, solutions, boundaries, loads...')
		delete.triggered.connect(self.deleteItem)

		resetview = QtWidgets.QAction(QtGui.QIcon('../Icons/icon_reset_view.png'),'Reset view', self)
		resetview.setShortcut('R')
		resetview.setStatusTip('Reset view to origin')
		resetview.triggered.connect(self.viewer.camera.reset)
		resetview.triggered.connect(self.viewer.update)

		centerview = QtWidgets.QAction(QtGui.QIcon('../Icons/icon_center_view.png'),'Center view', self)
		centerview.setShortcut('C')
		centerview.setStatusTip('Center/uncenter view on model')
		centerview.triggered.connect(self.centerModel)
		centerview.triggered.connect(self.viewer.camera.reset)
		centerview.triggered.connect(self.viewer.update)

		nodesview = QtWidgets.QAction(QtGui.QIcon('../Icons/icon_nodes.png'),'Nodes', self)
		nodesview.setShortcut('N')
		nodesview.setStatusTip('Toggle view of nodes on/off')
		nodesview.triggered.connect(self.nodesView)

		hide = QtWidgets.QAction(QtGui.QIcon('../Icons/icon_hide_elements.png'),'Hide Elements', self)
		hide.setStatusTip('Hide selected elements')
		hide.triggered.connect(self.hideElements)

		show = QtWidgets.QAction(QtGui.QIcon('../Icons/icon_show_elements.png'),'Show Elements', self)
		show.setStatusTip('Show all elements in mesh')
		show.triggered.connect(self.showElements)

		wireframe = QtWidgets.QAction(QtGui.QIcon('../Icons/icon_wireframe.png'),'Wireframe', self)
		wireframe.setShortcut('W')
		wireframe.setStatusTip('Change view to wireframe mode')
		wireframe.triggered.connect(self.wireframeView)

		shaded = QtWidgets.QAction(QtGui.QIcon('../Icons/icon_shaded.png'),'Shaded', self)
		shaded.setShortcut('S')
		shaded.setStatusTip('Change view to shaded mode')
		shaded.triggered.connect(self.shadedView)

		origin = QtWidgets.QAction(QtGui.QIcon('../Icons/icon_origin_triad.png'),'Origin', self)
		origin.setShortcut('O')
		origin.setStatusTip('Show origin coordinate system')
		origin.triggered.connect(self.showOrigin)
		
		meshtree = QtWidgets.QAction(QtGui.QIcon('../Icons/icon_empty.png'),'Mesh Tree', self)
		meshtree.setShortcut('H')
		meshtree.setStatusTip('Toggle Mesh Tree On/Off')
		meshtree.triggered.connect(self.showMeshTree)

		meshview = QtWidgets.QAction(QtGui.QIcon('../Icons/icon_current_mesh.png'),'Current Mesh...', self)
		meshview.setStatusTip('Select what mesh to view')
		meshview.triggered.connect(self.selectMesh)

		solutionview = QtWidgets.QAction(QtGui.QIcon('../Icons/icon_current_solution.png'),'Current Solution...', self)
		solutionview.setStatusTip('Select what solution to view')
		solutionview.triggered.connect(self.selectSolution)

		resultview = QtWidgets.QAction(QtGui.QIcon('../Icons/icon_current_results.png'),'Current Result...', self)
		resultview.setStatusTip('Select what result to view')
		resultview.triggered.connect(self.selectResult)

		highlightnode = QtWidgets.QAction(QtGui.QIcon('../Icons/icon_highlight_node.png'),'Node', self)
		highlightnode.setStatusTip('Highlight node')
		highlightnode.triggered.connect(self.highlightNode)

		highlightelement = QtWidgets.QAction(QtGui.QIcon('../Icons/icon_highlight_element.png'),'Element', self)
		highlightelement.setStatusTip('Highlight element')
		highlightelement.triggered.connect(self.highlightElement)

		highlightnodeset = QtWidgets.QAction(QtGui.QIcon('../Icons/icon_highlight_nodeset.png'),'Nodeset', self)
		highlightnodeset.setStatusTip('Highlight nodeset')
		highlightnodeset.triggered.connect(self.highlightNodeSet)

		highlightelementset = QtWidgets.QAction(QtGui.QIcon('../Icons/icon_highlight_elementset.png'),'Elementset', self)
		highlightelementset.setStatusTip('Highlight elementset')
		highlightelementset.triggered.connect(self.highlightElementSet)

		node = QtWidgets.QAction(QtGui.QIcon('../Icons/icon_new_node.png'),'Create Node', self)
		node.setStatusTip('Create a new node')
		node.triggered.connect(self.createNode)

		movenodes = QtWidgets.QAction(QtGui.QIcon('../Icons/icon_move_nodes.png'),'Move Nodes', self)
		movenodes.setStatusTip('Move the selected nodes')
		movenodes.triggered.connect(self.moveNodes)

		fusenodes = QtWidgets.QAction(QtGui.QIcon('../Icons/icon_fuse_nodes.png'),'Fuse Nodes', self)
		fusenodes.setStatusTip('Fuse selected nodes within specified tolerance')
		fusenodes.triggered.connect(self.fuseNodes)

		element = QtWidgets.QAction(QtGui.QIcon('../Icons/icon_new_elements.png'),'Create Elements', self)
		element.setStatusTip('Create new elements')
		element.triggered.connect(self.createElements)

		extrude = QtWidgets.QAction(QtGui.QIcon('../Icons/icon_extrude_elements.png'),'Extrude Elements', self)
		extrude.setStatusTip('Create new elements by extruding from selected elements')
		extrude.triggered.connect(self.extrudeElements)

		convert = QtWidgets.QAction(QtGui.QIcon('../Icons/icon_convert_elements.png'),'Convert Elements', self)
		convert.setStatusTip('Convert elements from one type to another')
		convert.triggered.connect(self.convertElements)

		insert = QtWidgets.QAction(QtGui.QIcon('../Icons/icon_insert_elements.png'),'Insert Elements', self)
		insert.setShortcut('I')
		insert.setStatusTip('Insert elements between selected nodes')
		insert.triggered.connect(self.insertElements)

		splitbeams = QtWidgets.QAction(QtGui.QIcon('../Icons/icon_split_beam.png'),'Split Beams', self)
		splitbeams.setStatusTip('Split beam elements into smaller elements')
		splitbeams.triggered.connect(self.splitBeams)

		beamorient = QtWidgets.QAction(QtGui.QIcon('../Icons/icon_beam_orient.png'),'Beam Orientation', self)
		beamorient.setStatusTip('Set orientation on beam elements')
		beamorient.triggered.connect(self.beamOrientation)

		mesh = QtWidgets.QAction(QtGui.QIcon('../Icons/icon_create_mesh.png'),'Create Mesh', self)
		mesh.setStatusTip('Create a mesh of several elementsets')
		mesh.triggered.connect(self.createMesh)

		resizeelements = QtWidgets.QAction(QtGui.QIcon('../Icons/icon_resize_elements.png'),'Resize Elements', self)
		resizeelements.setStatusTip('Resize selected elements')
		resizeelements.triggered.connect(self.resizeElements)

		getinfo = QtWidgets.QAction(QtGui.QIcon('../Icons/icon_get_info.png'),'Node/Element Info', self)
		getinfo.setStatusTip('Print out info about selected node/element')
		getinfo.triggered.connect(self.getNodeElementInfo)

		copynodes = QtWidgets.QAction(QtGui.QIcon('../Icons/icon_copy_nodes.png'),'Copy Nodes', self)
		copynodes.setStatusTip('Copy nodes and offset')
		copynodes.triggered.connect(self.copyNodes)

		copy = QtWidgets.QAction(QtGui.QIcon('../Icons/icon_copy.png'),'Copy Elements', self)
		copy.setStatusTip('Copy elements and offset')
		copy.triggered.connect(self.copyElements)

		mirrorcopy = QtWidgets.QAction(QtGui.QIcon('../Icons/icon_mirror_copy.png'),'Mirror Elements', self)
		mirrorcopy.setStatusTip('Mirror copy selected elements about x-, y- or z-plane')
		mirrorcopy.triggered.connect(self.mirrorCopyElements)

		move = QtWidgets.QAction(QtGui.QIcon('../Icons/icon_move_elements.png'),'Move Elements', self)
		move.setStatusTip('Move all elements in elementset by specified coordinates')
		move.triggered.connect(self.moveElements)

		rotate = QtWidgets.QAction(QtGui.QIcon('../Icons/icon_rotate_elements.png'),'Rotate Elements', self)
		rotate.setStatusTip('Rotate all elements in elementset around specified axis')
		rotate.triggered.connect(self.rotateElements)

		distance = QtWidgets.QAction(QtGui.QIcon('../Icons/icon_distance.png'),'Measure Distance', self)
		distance.setStatusTip('Measure distance between two selected nodes')
		distance.triggered.connect(self.measureDistance)

		renumberNodes = QtWidgets.QAction(QtGui.QIcon('../Icons/icon_link.png'),'Renumber Nodes', self)
		renumberNodes.setStatusTip('Renumber nodes from input')
		renumberNodes.triggered.connect(self.renumberNodes)

		renumberElements = QtWidgets.QAction(QtGui.QIcon('../Icons/icon_link.png'),'Renumber Elements', self)
		renumberElements.setStatusTip('Renumber elements from input')
		renumberElements.triggered.connect(self.renumberElements)

		nodeset = QtWidgets.QAction(QtGui.QIcon('../Icons/icon_create_nodeset.png'),'Create Nodeset', self)
		nodeset.setStatusTip('Create a nodeset')
		nodeset.triggered.connect(self.createNodeset)

		elementset = QtWidgets.QAction(QtGui.QIcon('../Icons/icon_create_elementset.png'),'Create Elementset', self)
		elementset.setStatusTip('Create an elementset')
		elementset.triggered.connect(self.createElementset)

		material = QtWidgets.QAction(QtGui.QIcon('../Icons/icon_new_material.png'),'Create Material', self)
		material.setStatusTip('Create a material')
		material.triggered.connect(self.newMaterial)

		section = QtWidgets.QAction(QtGui.QIcon('../Icons/icon_create_section.png'),'Create Section', self)
		section.setStatusTip('Create a Section')
		section.triggered.connect(self.newSection)

		beamsection = QtWidgets.QAction(QtGui.QIcon('../Icons/icon_beam_section.png'),'Modify Beam Section', self)
		beamsection.setStatusTip('Modify Beam Section')
		beamsection.triggered.connect(self.newBeamSection)

		applySection = QtWidgets.QAction(QtGui.QIcon('../Icons/icon_apply_section.png'),'Apply Section', self)
		applySection.setStatusTip('Apply section to elementset')
		applySection.triggered.connect(self.applySection)

		static = QtWidgets.QAction(QtGui.QIcon('../Icons/icon_static.png'),'Static', self)
		static.setStatusTip('Static solver')
		static.triggered.connect(self.solveStatic)

		eigenmodes = QtWidgets.QAction(QtGui.QIcon('../Icons/icon_eigenmodes.png'),'Eigenmodes', self)
		eigenmodes.setStatusTip('Eigenmodes solver')
		eigenmodes.triggered.connect(self.solveEigenmodes)

		modal = QtWidgets.QAction(QtGui.QIcon('../Icons/icon_modal_dynamic.png'),'Modal Dynamic', self)
		modal.setStatusTip('Modal Dynamic solver')
		modal.triggered.connect(self.solveModalDynamic)

		plastic = QtWidgets.QAction(QtGui.QIcon('../Icons/icon_static_plastic.png'),'Static Plastic', self)
		plastic.setStatusTip('Static Plastic solver')
		plastic.triggered.connect(self.solveStaticPlastic)

		heattransfer = QtWidgets.QAction(QtGui.QIcon('../Icons/icon_heat_transfer.png'),'Heat Transfer', self)
		heattransfer.setStatusTip('Heat Transfer solver')
		heattransfer.triggered.connect(self.solveHeatTransfer)

		touchlock = QtWidgets.QAction(QtGui.QIcon('../Icons/icon_touch_lock.png'),'Touch Lock', self)
		touchlock.setStatusTip('Apply touchlock constraints between two nodesets')
		touchlock.triggered.connect(self.applyTouchLockConstraint)

		nodelock = QtWidgets.QAction(QtGui.QIcon('../Icons/icon_point_lock.png'),'Node Lock', self)
		nodelock.setStatusTip('Apply nodelock constraint between one node and a set of nodes')
		nodelock.triggered.connect(self.applyNodeLockConstraint)
		
		spiderlock = QtWidgets.QAction(QtGui.QIcon('../Icons/icon_spider.png'),'Spider', self)
		spiderlock.setStatusTip('Create a spider between one node and a set of nodes')
		spiderlock.triggered.connect(self.createSpider)
		
		uniformload = QtWidgets.QAction(QtGui.QIcon('../Icons/icon_uniform_load.png'),'Uniform Load', self)
		uniformload.setStatusTip('Apply uniform load to nodeset')
		uniformload.triggered.connect(self.applyUniformLoad)

		concentratedload = QtWidgets.QAction(QtGui.QIcon('../Icons/icon_concentrated_load.png'),'Concentrated Load', self)
		concentratedload.setStatusTip('Apply concentrated load to nodeset')
		concentratedload.triggered.connect(self.applyConcentratedLoad)
		
		distributedload = QtWidgets.QAction(QtGui.QIcon('../Icons/icon_distributed_load.png'),'Distributed Load', self)
		distributedload.setStatusTip('Apply distributed load to elementset (beam elements only)')
		distributedload.triggered.connect(self.applyDistributedLoad)

		torqueload = QtWidgets.QAction(QtGui.QIcon('../Icons/icon_torque_load.png'),'Torque Load', self)
		torqueload.setStatusTip('Apply torque load to node (beam elements only)')
		torqueload.triggered.connect(self.applyTorqueLoad)

		gravityload = QtWidgets.QAction(QtGui.QIcon('../Icons/icon_gravity_load.png'),'Gravity Load', self)
		gravityload.setStatusTip('Apply gravity load to elementset')
		gravityload.triggered.connect(self.applyGravityLoad)

		dynamicload = QtWidgets.QAction(QtGui.QIcon('../Icons/icon_dynamic_load.png'),'Dynamic Load', self)
		dynamicload.setStatusTip('Apply dynamic load to nodeset')
		dynamicload.triggered.connect(self.applyDynamicLoad)

		displacement = QtWidgets.QAction(QtGui.QIcon('../Icons/icon_boundary.png'),'Displacement', self)
		displacement.setStatusTip('Apply displacement boundary to nodeset')
		displacement.triggered.connect(self.applyDisplacement)

		newsolfile = QtWidgets.QAction(QtGui.QIcon('../Icons/icon_new_file.png'),'Write sol-file...', self)
		newsolfile.setStatusTip('Write a sol-file that can be run directly in solver')
		newsolfile.triggered.connect(self.newSolFile)

		runsolver = QtWidgets.QAction(QtGui.QIcon('../Icons/icon_settings.png'),'Run sol-file in solver...', self)
		runsolver.setStatusTip('Run sol-file in the solver to generate results')
		runsolver.triggered.connect(self.runSolver)

		scalefactor = QtWidgets.QAction(QtGui.QIcon('../Icons/icon_scale_factor.png'),'Scale Factor', self)
		scalefactor.setStatusTip('Set the scale factor for view of displacements')
		scalefactor.triggered.connect(self.setScaleFactor)

		scalediagram = QtWidgets.QAction(QtGui.QIcon('../Icons/icon_scale_diagram.png'),'Scale Diagram', self)
		scalediagram.setStatusTip('Adjust the scale for shear and bending moment diagrams')
		scalediagram.triggered.connect(self.setShearBendingDiagram)

		average = QtWidgets.QAction(QtGui.QIcon('../Icons/icon_average.png'),'Average Stress/Strain', self)
		average.setStatusTip('View average stresses and strains')
		average.triggered.connect(self.viewAverage)

		animationspeed = QtWidgets.QAction(QtGui.QIcon('../Icons/icon_animation_speed.png'),'Speed', self)
		animationspeed.setStatusTip('Set the frame to frame speed for animations')
		animationspeed.triggered.connect(self.setAnimationSpeed)

		animationonoff = QtWidgets.QAction(QtGui.QIcon('../Icons/icon_start_pause.png'),'Play/Pause', self)
		animationonoff.setShortcut('P')
		animationonoff.setStatusTip('Turn animation on or off')
		animationonoff.triggered.connect(self.setAnimationOnOff)

		previousmode = QtWidgets.QAction(QtGui.QIcon('../Icons/icon_previous.png'),'Previous Mode', self)
		previousmode.setStatusTip('Change to previous eigenmode')
		previousmode.triggered.connect(self.previousEigenmode)

		nextmode = QtWidgets.QAction(QtGui.QIcon('../Icons/icon_next.png'),'Next Mode', self)
		nextmode.setStatusTip('Change to next eigenmode')
		nextmode.triggered.connect(self.nextEigenmode)

		empty1 = QtWidgets.QAction(QtGui.QIcon('../Icons/icon_empty.png'),' ', self)
		empty1.setEnabled(False)
		empty2 = QtWidgets.QAction(QtGui.QIcon('../Icons/icon_empty.png'),' ', self)
		empty2.setEnabled(False)
		empty3 = QtWidgets.QAction(QtGui.QIcon('../Icons/icon_empty.png'),' ', self)
		empty3.setEnabled(False)
		empty4 = QtWidgets.QAction(QtGui.QIcon('../Icons/icon_empty.png'),' ', self)
		empty4.setEnabled(False)
		empty5 = QtWidgets.QAction(QtGui.QIcon('../Icons/icon_empty.png'),' ', self)
		empty5.setEnabled(False)

		menubar = self.menuBar()
		fileMenu = menubar.addMenu('&File')
		fileMenu.addAction(newsession)
		fileMenu.addAction(importfrom)
		fileMenu.addAction(export)
		fileMenu.addAction(openfile)
		fileMenu.addAction(savefile)
		fileMenu.addAction(quicksave)
		fileMenu.addAction(exit)
		editMenu = menubar.addMenu('&Edit')
		editMenu.addAction(selectnodes)
		editMenu.addAction(selectelements)
		editMenu.addAction(delete)
		viewMenu = menubar.addMenu('&View')
		viewMenu.addAction(resetview)
		viewMenu.addAction(centerview)
		viewMenu.addAction(wireframe)
		viewMenu.addAction(shaded)
		viewMenu.addAction(nodesview)
		viewMenu.addAction(origin)
		viewMenu.addAction(meshtree)
		highlightMenu = viewMenu.addMenu('&Highlight')
		highlightMenu.addAction(highlightnode)
		highlightMenu.addAction(highlightelement)
		highlightMenu.addAction(highlightnodeset)
		highlightMenu.addAction(highlightelementset)
		meshMenu = menubar.addMenu('&Mesh')
		meshMenu.addAction(meshview)
		meshMenu.addAction(mesh)
		meshMenu.addAction(getinfo)
		nodeMenu = meshMenu.addMenu('&Nodes')
		nodeMenu.addAction(node)
		nodeMenu.addAction(copynodes)
		nodeMenu.addAction(movenodes)
		nodeMenu.addAction(fusenodes)
		nodeMenu.addAction(distance)
		nodeMenu.addAction(nodeset)
		nodeMenu.addAction(renumberNodes)
		elementMenu = meshMenu.addMenu('&Elements')
		elementMenu.addAction(element)
		elementMenu.addAction(extrude)
		elementMenu.addAction(insert)
		elementMenu.addAction(convert)
		elementMenu.addAction(copy)
		elementMenu.addAction(mirrorcopy)
		elementMenu.addAction(move)
		elementMenu.addAction(rotate)
		elementMenu.addAction(resizeelements)
		elementMenu.addAction(splitbeams)
		elementMenu.addAction(beamorient)
		elementMenu.addAction(elementset)
		elementMenu.addAction(renumberElements)
		materialMenu = meshMenu.addMenu('&Materials')
		materialMenu.addAction(material)
		sectionMenu = meshMenu.addMenu('&Sections')
		sectionMenu.addAction(section)
		sectionMenu.addAction(applySection)
		sectionMenu.addAction(beamsection)
		solverMenu = menubar.addMenu('&Solution')
		solverMenu.addAction(solutionview)
		solutionMenu = solverMenu.addMenu('&Solutions')
		solutionMenu.addAction(static)
		solutionMenu.addAction(eigenmodes)
		solutionMenu.addAction(modal)
		solutionMenu.addAction(plastic)
		solutionMenu.addAction(heattransfer)
		constraintsMenu = solverMenu.addMenu('&Constraints')
		constraintsMenu.addAction(touchlock)
		constraintsMenu.addAction(nodelock)
		constraintsMenu.addAction(spiderlock)
		boundMenu = solverMenu.addMenu('&Boundaries')
		boundMenu.addAction(displacement)
		loadsMenu = solverMenu.addMenu('&Loads')
		loadsMenu.addAction(uniformload)
		loadsMenu.addAction(concentratedload)
		loadsMenu.addAction(distributedload)
		loadsMenu.addAction(torqueload)
		loadsMenu.addAction(gravityload)
		loadsMenu.addAction(dynamicload)
		solverMenu.addAction(newsolfile)
		solverMenu.addAction(runsolver)
		resultMenu = menubar.addMenu('&Result')
		resultMenu.addAction(resultview)
		resultMenu.addAction(scalefactor)
		resultMenu.addAction(scalediagram)
		resultMenu.addAction(average)
		aniMenu = resultMenu.addMenu('&Animation')
		aniMenu.addAction(animationonoff)
		aniMenu.addAction(previousmode)
		aniMenu.addAction(nextmode)
		aniMenu.addAction(animationspeed)
		helpMenu = menubar.addMenu('&Help')
		helpMenu.addAction(camerahelp)
		helpMenu.addAction(selecthelp)
		helpMenu.addAction(meshhelp)
		helpMenu.addAction(materialhelp)
		helpMenu.addAction(sectionhelp)
		helpMenu.addAction(solutionhelp)
		helpMenu.addAction(boundaryhelp)
		helpMenu.addAction(constrainthelp)
		helpMenu.addAction(loadhelp)
		helpMenu.addAction(solverhelp)
		helpMenu.addAction(resulthelp)
		tutorialMenu = menubar.addMenu('&Tutorials')
		tutorialMenu.addAction(tutorialROD2N2D)
		tutorialMenu.addAction(tutorialROD2N)
		tutorialMenu.addAction(tutorialBEAM2N2D)
		tutorialMenu.addAction(tutorialBEAM2N)
		tutorialMenu.addAction(tutorialTRI3N)
		tutorialMenu.addAction(tutorialTRI6N)
		tutorialMenu.addAction(tutorialQUAD4N)
		tutorialMenu.addAction(tutorialQUAD8N)
		tutorialMenu.addAction(tutorialTET4N)
		tutorialMenu.addAction(tutorialTET10N)
		tutorialMenu.addAction(tutorialHEX8N)
		tutorialMenu.addAction(tutorialHEX20N)

		main_toolbar1 = QtWidgets.QToolBar('Main Toolbar Upper')
		main_toolbar1.setIconSize(QtCore.QSize(24,24))
		main_toolbar1.setMovable(False)
		main_toolbar1.addSeparator()
		main_toolbar1.addSeparator()
		main_toolbar1.addAction(meshview)
		main_toolbar1.addAction(solutionview)
		main_toolbar1.addAction(resultview)
		main_toolbar1.addSeparator()
		main_toolbar1.addSeparator()
		main_toolbar1.addAction(resetview)
		main_toolbar1.addAction(centerview)
		main_toolbar1.addAction(origin)
		main_toolbar1.addSeparator()
		main_toolbar1.addSeparator()
		main_toolbar1.addAction(highlightnode)
		main_toolbar1.addAction(highlightelement)
		main_toolbar1.addSeparator()
		main_toolbar1.addSeparator()
		main_toolbar1.addAction(mesh)
		main_toolbar1.addAction(element)
		main_toolbar1.addAction(extrude)
		main_toolbar1.addAction(insert)
		main_toolbar1.addAction(convert)
		main_toolbar1.addAction(resizeelements)
		main_toolbar1.addAction(beamorient)
		main_toolbar1.addAction(splitbeams)
		main_toolbar1.addSeparator()
		main_toolbar1.addSeparator()
		main_toolbar1.addAction(getinfo)
		main_toolbar1.addAction(nodeset)
		main_toolbar1.addAction(elementset)
		main_toolbar1.addSeparator()
		main_toolbar1.addSeparator()
		main_toolbar1.addAction(material)
		main_toolbar1.addAction(beamsection)
		main_toolbar1.addSeparator()
		main_toolbar1.addSeparator()
		main_toolbar1.addAction(static)
		main_toolbar1.addAction(plastic)
#		main_toolbar1.addAction(heattransfer)
		main_toolbar1.addSeparator()
		main_toolbar1.addSeparator()
		main_toolbar1.addAction(touchlock)
		main_toolbar1.addAction(nodelock)
		main_toolbar1.addSeparator()
		main_toolbar1.addSeparator()
		main_toolbar1.addAction(uniformload)
		main_toolbar1.addAction(concentratedload)
		main_toolbar1.addAction(dynamicload)
		main_toolbar1.addSeparator()
		main_toolbar1.addSeparator()
		main_toolbar1.addAction(average)
		main_toolbar1.addAction(scalefactor)
		main_toolbar1.addAction(scalediagram)
		main_toolbar1.addAction(newsolfile)
		main_toolbar1.addAction(runsolver)
		main_toolbar1.addSeparator()
		main_toolbar1.addSeparator()

		main_toolbar2 = QtWidgets.QToolBar('Main Toolbar Lower')
		main_toolbar2.setIconSize(QtCore.QSize(24,24))
		main_toolbar2.setMovable(False)
		main_toolbar2.addSeparator()
		main_toolbar2.addSeparator()
		main_toolbar2.addAction(selectnodes)
		main_toolbar2.addAction(selectelements)
		main_toolbar2.addAction(delete)
		main_toolbar2.addSeparator()
		main_toolbar2.addSeparator()
		main_toolbar2.addAction(shaded)
		main_toolbar2.addAction(wireframe)
		main_toolbar2.addAction(nodesview)
		main_toolbar2.addSeparator()
		main_toolbar2.addSeparator()
		main_toolbar2.addAction(highlightnodeset)
		main_toolbar2.addAction(highlightelementset)
		main_toolbar2.addSeparator()
		main_toolbar2.addSeparator()
		main_toolbar2.addAction(node)
		main_toolbar2.addAction(fusenodes)
		main_toolbar2.addAction(copynodes)
		main_toolbar2.addAction(movenodes)
		main_toolbar2.addAction(copy)
		main_toolbar2.addAction(mirrorcopy)
		main_toolbar2.addAction(move)
		main_toolbar2.addAction(rotate)
		main_toolbar2.addSeparator()
		main_toolbar2.addSeparator()
		main_toolbar2.addAction(distance)
		main_toolbar2.addAction(hide)
		main_toolbar2.addAction(show)
		main_toolbar2.addSeparator()
		main_toolbar2.addSeparator()
		main_toolbar2.addAction(section)
		main_toolbar2.addAction(applySection)
		main_toolbar2.addSeparator()
		main_toolbar2.addSeparator()
		main_toolbar2.addAction(eigenmodes)
		main_toolbar2.addAction(modal)
		main_toolbar2.addSeparator()
		main_toolbar2.addSeparator()
		main_toolbar2.addAction(displacement)
		main_toolbar2.addAction(spiderlock)
		main_toolbar2.addSeparator()
		main_toolbar2.addSeparator()
		main_toolbar2.addAction(distributedload)
		main_toolbar2.addAction(torqueload)
		main_toolbar2.addAction(gravityload)
		main_toolbar2.addSeparator()
		main_toolbar2.addSeparator()
		main_toolbar2.addAction(previousmode)
		main_toolbar2.addAction(nextmode)
		main_toolbar2.addAction(animationonoff)
		main_toolbar2.addAction(animationspeed)
		main_toolbar2.addAction(empty1)
		main_toolbar2.addSeparator()
		main_toolbar2.addSeparator()

		btnViewMesh = QtWidgets.QAction(QtGui.QIcon('../Icons/icon_view_mesh.png'),'Change view to Mesh', self)
		btnViewMesh.triggered.connect(self.btnViewMeshAction)
		btnViewMesh.setStatusTip('Change view to Mesh')
		btnViewConstraint = QtWidgets.QAction(QtGui.QIcon('../Icons/icon_view_constraint.png'),'Change view to Constraints', self)
		btnViewConstraint.triggered.connect(self.btnViewConstraintAction)
		btnViewConstraint.setStatusTip('Change view to Constraints')
		btnViewBoundary = QtWidgets.QAction(QtGui.QIcon('../Icons/icon_view_boundary.png'),'Change view to Boundaries', self)
		btnViewBoundary.triggered.connect(self.btnViewBoundaryAction)
		btnViewBoundary.setStatusTip('Change view to Boundaries')
		btnViewLoad = QtWidgets.QAction(QtGui.QIcon('../Icons/icon_view_load.png'),'Change view to Loads', self)
		btnViewLoad.triggered.connect(self.btnViewLoadAction)
		btnViewLoad.setStatusTip('Change view to Loads')
		btnViewSolution = QtWidgets.QAction(QtGui.QIcon('../Icons/icon_view_solution.png'),'Change view to Solutions', self)
		btnViewSolution.triggered.connect(self.btnViewSolutionAction)
		btnViewSolution.setStatusTip('Change view to Solution')
		btnViewResult = QtWidgets.QAction(QtGui.QIcon('../Icons/icon_view_result.png'),'Change view to Results', self)
		btnViewResult.triggered.connect(self.btnViewResultAction)
		btnViewResult.setStatusTip('Change view to Result')

		view_toolbar = QtWidgets.QToolBar('View Toolbar')
		view_toolbar.setIconSize(QtCore.QSize(48,48))
		view_toolbar.setMovable(False)
		view_toolbar.addAction(empty1)
		view_toolbar.addAction(empty2)
		view_toolbar.addSeparator()
		view_toolbar.addAction(btnViewMesh)
		view_toolbar.addSeparator()
		view_toolbar.addAction(btnViewConstraint)
		view_toolbar.addSeparator()
		view_toolbar.addAction(btnViewBoundary)
		view_toolbar.addSeparator()
		view_toolbar.addAction(btnViewLoad)
		view_toolbar.addSeparator()
		view_toolbar.addAction(btnViewSolution)
		view_toolbar.addSeparator()
		view_toolbar.addAction(btnViewResult)
		view_toolbar.addSeparator()
		view_toolbar.addSeparator()

		self.addToolBar(QtCore.Qt.LeftToolBarArea, view_toolbar)

		parentWidget = QtWidgets.QWidget()
		tool1 = QtWidgets.QToolBar()
		tool1.addWidget(main_toolbar1)
		tool2 = QtWidgets.QToolBar()
		tool2.addWidget(main_toolbar2)

		vbox = QtWidgets.QVBoxLayout()
		vbox.setContentsMargins(0,5,5,5)
		vbox.setSpacing(0)

		vbox.addWidget(tool1)
		vbox.addWidget(tool2)

		self.viewer.setSizePolicy( QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding )
		vbox.addWidget(self.viewer)

		parentWidget.setLayout(vbox)
		self.setCentralWidget(parentWidget)

		self.centerWindow()
		self.resize(1300,650)


	def centerWindow(self):
		'''
	Center Window on the Current Screen,
	with Multi-Monitor support
	'''
		self.showNormal()
		window_geometry = self.frameGeometry()
		self.resize(QtWidgets.QDesktopWidget().screenGeometry().width() // 1.3,
					QtWidgets.QDesktopWidget().screenGeometry().height() // 1.5)
		mousepointer_position = QtWidgets.QApplication.desktop().cursor().pos()
		screen = QtWidgets.QApplication.desktop().screenNumber(mousepointer_position)
		centerPoint = QtWidgets.QApplication.desktop().screenGeometry(screen).center()
		window_geometry.moveCenter(centerPoint)
		return bool(not self.move(window_geometry.topLeft()))


	def keyPressEvent(self, e):
		'''
	Capture the user holding down CTRL, SHIFT
	or ALT, to be used while clicking the mouse
	for manipulation of the camera.
	'''
		if e.key() == QtCore.Qt.Key_Control:
			self.viewer.activeCTRL = True
		if e.key() == QtCore.Qt.Key_Shift:
			self.viewer.activeSHIFT = True
		if e.key() == QtCore.Qt.Key_Alt:
			self.viewer.activeALT = True


	def keyReleaseEvent(self, e):
		'''
	Capture the user releasing CTRL, SHIFT
	or ALT, to be used while clicking the mouse
	for manipulation of the camera.
	'''
		if e.key() == QtCore.Qt.Key_Control:
			self.viewer.activeCTRL = False
		if e.key() == QtCore.Qt.Key_Shift:
			self.viewer.activeSHIFT = False
		if e.key() == QtCore.Qt.Key_Alt:
			self.viewer.activeALT = False


	def cameraHelpScreen(self):
		self.help = HelpScreen('camera')
	def selectHelpScreen(self):
		self.help = HelpScreen('selection')
	def meshHelpScreen(self):
		self.help = HelpScreen('meshes')
	def materialHelpScreen(self):
		self.help = HelpScreen('materials')
	def sectionHelpScreen(self):
		self.help = HelpScreen('sections')
	def solutionHelpScreen(self):
		self.help = HelpScreen('solutions')
	def boundaryHelpScreen(self):
		self.help = HelpScreen('boundaries')
	def constraintHelpScreen(self):
		self.help = HelpScreen('constraints')
	def loadHelpScreen(self):
		self.help = HelpScreen('loads')
	def solverHelpScreen(self):
		self.help = HelpScreen('solver')
	def resultHelpScreen(self):
		self.help = HelpScreen('results')
	def tutorialROD2N2DHelpScreen(self):
		self.help = HelpScreen('tutorial_ROD2N2D')
	def tutorialROD2NHelpScreen(self):
		self.help = HelpScreen('tutorial_ROD2N')
	def tutorialBEAM2N2DHelpScreen(self):
		self.help = HelpScreen('tutorial_BEAM2N2D')
	def tutorialBEAM2NHelpScreen(self):
		self.help = HelpScreen('tutorial_BEAM2N')
	def tutorialTRI3NHelpScreen(self):
		self.help = HelpScreen('tutorial_TRI3N')
	def tutorialTRI6NHelpScreen(self):
		self.help = HelpScreen('tutorial_TRI6N')
	def tutorialQUAD4NHelpScreen(self):
		self.help = HelpScreen('tutorial_QUAD4N')
	def tutorialQUAD8NHelpScreen(self):
		self.help = HelpScreen('tutorial_QUAD8N')
	def tutorialTET4NHelpScreen(self):
		self.help = HelpScreen('tutorial_TET4N')
	def tutorialTET10NHelpScreen(self):
		self.help = HelpScreen('tutorial_TET10N')
	def tutorialHEX8NHelpScreen(self):
		self.help = HelpScreen('tutorial_HEX8N')
	def tutorialHEX20NHelpScreen(self):
		self.help = HelpScreen('tutorial_HEX20N')


	def clearModel(self):
		'''
	Asks if user is certain they want to clear
	away current session and start a new one.
	If so, clear out all data in self.model.
	'''
		is_certain = QtWidgets.QMessageBox.question(self, 'New Session',
					'Are you sure you want to start a new session?\nAll unsaved data will be lost', \
						QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No, QtWidgets.QMessageBox.No)
		if is_certain == QtWidgets.QMessageBox.Yes:
			self.model.clearModel()
			print('\n\tAll data now cleared from current session.\n')
		else:
			pass


	def openFile(self):
		'''
	Open an existing *.out file or *.mdl file
	with the help of PyQt's built-in 
	QFileDialog class. 
	'''
		filename = QtWidgets.QFileDialog.getOpenFileName(self, 'Open file', './')[0]
		if filename[-4:] == '.out':
			self.new_results_open['file'] = filename
			self.viewer.update()
		elif filename[-4:] == '.mdl':
			self.current_savefile = filename
			self.new_model_open['file'] = filename
			self.viewer.update()
		else:
			print('\n\tUnknown file type. Accepted input is:')
			print('\t*.out, *.mdl')


	def importFrom(self):
		'''
	Import meshes, solutions, boundaries, loads, 
	elementsets and nodesets from a *.sol file,
	*.out file or *.mesh file with the help of PyQt's
	built-in QFileDialog class. 
	'''
		filename = QtWidgets.QFileDialog.getOpenFileName(self, 'Open file', './')[0]
		if filename[-4:] == '.out':
			print('\n\tImport mesh from *.out file not supported.')
			print('\tUse Open instead, and create an elementset')
			print('\tof that mesh to use in a new mesh.')
		elif filename[-4:] == '.sol':
			self.new_file_import['file'] = filename
			self.viewer.update()
		elif filename[-4:] == '.bdf':
			self.new_file_import['file'] = filename
			self.viewer.update()
		elif filename[-4:] == '.inp':
			self.new_file_import['file'] = filename
			self.viewer.update()
		elif filename[-4:] == '.mdl':
			print('\n\tImport mesh from *.mdl file not supported. Use Open.')
		else:
			print('\n\tUnknown file type. Accepted input is:')
			print('\t*.sol, *.bdf')
			

	def saveFile(self):
		'''
	Save specified meshes, solutions, boundaries,
	loads, elementsets and nodesets in a *.mesh 
	file with the help of PyQt's built-in 
	QFileDialog class. 
	'''
		filename = str(QtWidgets.QFileDialog.getSaveFileName(self, 'Save file', './')[0])
		modelfile = ''
		for i in range(len(filename)):
			if filename[-i-1] == '/' or filename[-i-1] == '\\':
				modelfile = str(filename[-i:-4])
				break
		if filename[-4:] == '.mdl':
			self.current_savefile = filename
			filename = filename[:-4]
		if os.path.exists(filename+'.mdl'):
			print('\n\tOverwriting model file '+modelfile+'.mdl\n')
		tmpmodel = Model(self)
		del tmpmodel.gui
		tmpmodel.nodesets	  = self.model.nodesets
		tmpmodel.elementsets  = self.model.elementsets
		tmpmodel.materials 	  = self.model.materials
		tmpmodel.sections 	  = self.model.sections
		tmpmodel.meshes 	  = self.model.meshes
		tmpmodel.displayLists = self.model.displayLists
		pickle.dump((tmpmodel,), open(filename+'.mdl', 'wb'))


	def quickSaveFile(self):
		'''
	Quick saves current session in *.mdl-file,
	or if model is not previously saved to *.mdl-file
	call function: saveFile()
	'''
		filename = self.current_savefile
		modelfile = ''
		for i in range(len(filename)):
			if filename[-i-1] == '/' or filename[-i-1] == '\\':
				modelfile = str(filename[-i:-4])
				break
		if os.path.exists(filename):
			print('\n\tOverwriting model file '+modelfile+'.mdl\n')
			tmpmodel = Model(self)
			del tmpmodel.gui
			tmpmodel.nodesets	  = self.model.nodesets
			tmpmodel.elementsets  = self.model.elementsets
			tmpmodel.materials 	  = self.model.materials
			tmpmodel.sections 	  = self.model.sections
			tmpmodel.meshes 	  = self.model.meshes
			tmpmodel.displayLists = self.model.displayLists
			pickle.dump((tmpmodel,), open(modelfile+'.mdl', 'wb'))
		else:
			self.saveFile()


	def exportMesh(self):
		'''
	Export current mesh to a *.sol file with
	the same name as the mesh.
	'''
		filename = str(QtWidgets.QFileDialog.getSaveFileName(self, 'Save file', './')[0])
		solfile = ''
		if filename[-4:] == '.sol':
			self.current_savefile = filename
			filename = filename[:-4]
		for i in range(len(filename)):
			if filename[-i-1] == '/' or filename[-i-1] == '\\':
				solfile = str(filename[-i:])
				break
		if os.path.exists(filename+'.sol'):
			print('\n\tOverwriting *.sol file '+solfile+'.sol\n')
		fobj = open(filename+'.sol','w')
		fobj.write('#\n#\n#\n')
		nodes = self.model.meshes[self.viewer.currentMesh].nodes
		for node in nodes:
			fobj.write('NODE, '+str(nodes[node].number)+', '+ \
								str(nodes[node].coord[0][0])+', '+ \
								str(nodes[node].coord[1][0])+', '+ \
								str(nodes[node].coord[2][0])+'\n')
		fobj.write('#\n#\n#\n')
		elements = self.model.meshes[self.viewer.currentMesh].elements
		for element in elements:
			fobj.write('ELEMENT, '+str(elements[element].type)+', '+ \
								   str(elements[element].number)+', 0')
			for node in elements[element].nodes:
				fobj.write(', '+str(node.number))
			fobj.write('\n')
		fobj.write('#\n#\n#\n')
		fobj.close()


	def newSolFile(self):
		'''
	Call up a dialog box to generate a *.sol file 
	with specific solutions chosen by the user.
	'''
		writeSolFile = {}
		used_sol_file_number = True
		filenum = 1
		while used_sol_file_number:
			if os.path.exists('sol_file-'+str(filenum)+'.sol'):
				filenum += 1
			else:
				used_sol_file_number = False
		writeSolFile['inputs'] = {'Name': 'sol_file-'+str(filenum)}
		writeSolFile['current'] = {'Solution': 'None'}
		if self.viewer.currentSolution != 'None':
			writeSolFile['current']['Solution'] = self.viewer.currentSolution
		writeSolFile['choices'] = [ ['Solution'], {} ]
		if len(self.model.meshes) != 0:
			if len(self.model.meshes[self.viewer.currentMesh].solutions) != 0:
				for solution in self.model.meshes[self.viewer.currentMesh].solutions:
					writeSolFile['choices'][1][solution] = []
					for result in self.model.meshes[self.viewer.currentMesh].solutions[solution]['Results']:
						writeSolFile['choices'][1][solution].append(result)
			else:
				print('\tNo solutions for current mesh to write to file.')
		else:
			print('\tNo meshes or solutions to write to file.')

		self.new_solfile = {}
		self.selectionWidget = InputSolFile(writeSolFile, self.new_solfile)
		self.selectionWidget.window_closed.connect(self.viewer.update)
		self.selectionWidget.show()


	def runSolver(self):
		'''
	Select *.sol-file to run in solver directly
	from the viewer.
	'''
		filename = QtWidgets.QFileDialog.getOpenFileName(self, 'Open file', './')[0]
		if filename[-4:] == '.sol':
			inputobj = InputData(filename)
			if inputobj.input_error == False:
				model = FEModel(inputobj)
			else:
				print('\n\tSolver aborted because of input error(s).')
		else:
			print('\n\tUnknown file type. Accepted input is:')
			print('\t*.sol')


	def deleteItem(self):
		'''
	Deletes selected item from model.
	'''
		if len(self.model.meshes) != 0:
			deleteItem = {}
			deleteItem['inputs'] = {}
			deleteItem['choices'] = [ ['Delete...', '---'],
									 { 'Node(s)':	 ['Selected'],
									   'Element(s)': ['Selected'],
									   'Nodeset':	 [],
									   'Elementset': [],
									   'Material':   [],
									   'Section':    [],
									   'Mesh':   	 [],
									   'Solution':   [],
									   'Boundary':   [],
									   'Constraint': [],
									   'Load':   	 [] } ]
			for nodeset in self.model.nodesets.keys():
				deleteItem['choices'][1]['Nodeset'].append(str(nodeset))
			for elementset in self.model.elementsets.keys():
				deleteItem['choices'][1]['Elementset'].append(str(elementset))
			for material in self.model.materials.keys():
				deleteItem['choices'][1]['Material'].append(material)
			for section in self.model.sections.keys():
				deleteItem['choices'][1]['Section'].append(section)
			for mesh in	self.model.meshes:
				deleteItem['choices'][1]['Mesh'].append(mesh)
				for solution in self.model.meshes[mesh].solutions:
					deleteItem['choices'][1]['Solution'].append(solution)
					for boundary in self.model.meshes[mesh].solutions[solution]['Boundaries']:
						deleteItem['choices'][1]['Boundary'].append(boundary)
					for constraint in self.model.meshes[mesh].solutions[solution]['Constraints']:
						deleteItem['choices'][1]['Constraint'].append(constraint)
					for load in self.model.meshes[mesh].solutions[solution]['Loads']:
						deleteItem['choices'][1]['Load'].append(load)
			for item in deleteItem['choices'][1]:
				if len(deleteItem['choices'][1][item]) == 0:
					deleteItem['choices'][1][item].append('none')
			if self.viewer.currentMesh == 'None':
				self.viewer.currentMesh = deleteItem['choices'][1][0]
			deleteItem['current'] = {'Delete...': 'Mesh', '---': self.viewer.currentMesh}
			deleteItem['inOrder'] = ['Delete...', '---']
			self.new_deletion = {}
			self.selectionWidget = InputDialog(deleteItem, 'Delete', self.new_deletion)
			self.selectionWidget.window_closed.connect(self.viewer.update)
			self.selectionWidget.show()
		else:
			print('\tThere are no meshes. Nothing to delete.')


	def selectNodes(self):
		'''
	Set mouse pointer to select nodes.
	'''
		if len(self.model.selected_elements) != 0:
			self.model.selected_elements.clear()
			self.viewer.update()
		self.model.selectOption = 'Nodes'
		self.statusBar().showMessage('  Selecting... nodes' )


	def selectElements(self):
		'''
	Set mouse pointer to select elements.
	'''
		if len(self.model.selected_nodes) != 0:
			self.model.selected_nodes.clear()
			self.viewer.update()
		self.model.selectOption = 'Elements'
		self.statusBar().showMessage('  Selecting... elements' )


	def getNodeElementInfo(self):
		'''
	Prints out the available info on the
	currently selected node/element.
	'''
		result = self.viewer.currentDisplayList['result']
		solution = self.viewer.currentDisplayList['solution']
		if len(self.model.selected_nodes) == 1:
			for node in self.model.selected_nodes:
				print('\n\tNode number:', self.model.selected_nodes[node].number)
				print('\tCoord: '+str(self.model.selected_nodes[node].coord[0][0])+',',
								  str(self.model.selected_nodes[node].coord[1][0])+',',
								  str(self.model.selected_nodes[node].coord[2][0]))
				if result != 'None':
					if solution in self.model.selected_nodes[node].solutions:
						if result == 'displacement':
							print('\tDisplacement [X, Y, Z, RX, RY, RZ, MAGN]')
							print('\t', self.model.selected_nodes[node].solutions[solution][result])
						elif result == 'nodeforce':
							if result in self.model.selected_nodes[node].solutions[solution]:
								print('\tNodeforce [FX, FY, FZ, MX, MY, MZ, MAGN]')
								print('\t', self.model.selected_nodes[node].solutions[solution][result])
						elif result == 'stress':
							if 'avg_stress' in self.model.selected_nodes[node].solutions[solution]:
								print('\tAverage stress [VonMises, MaxPrincipal, MinPrincipal, MaxShear]')
								print('\t', [self.model.selected_nodes[node].solutions[solution]['avg_stress']['VonMises'],
											 self.model.selected_nodes[node].solutions[solution]['avg_stress']['MaxPrinc'],
											 self.model.selected_nodes[node].solutions[solution]['avg_stress']['MinPrinc'],
											 self.model.selected_nodes[node].solutions[solution]['avg_stress']['MaxShear']])
						elif result == 'strain':
							if 'avg_strain' in self.model.selected_nodes[node].solutions[solution]:
								print('\tAverage strain [VonMises, MaxPrincipal, MinPrincipal, MaxShear]')
								print('\t', [self.model.selected_nodes[node].solutions[solution]['avg_strain']['VonMises'],
											 self.model.selected_nodes[node].solutions[solution]['avg_strain']['MaxPrinc'],
											 self.model.selected_nodes[node].solutions[solution]['avg_strain']['MinPrinc'],
											 self.model.selected_nodes[node].solutions[solution]['avg_strain']['MaxShear']])
						else:
							pass
		elif len(self.model.selected_elements) == 1:
			for element in self.model.selected_elements:
				print('\n\tElement number:', self.model.selected_elements[element].number)
				print('\tElement type:', self.model.selected_elements[element].type)
				elm_nodes = []
				for node in range(len(self.model.selected_elements[element].nodes)):
					elm_nodes.append(self.model.selected_elements[element].nodes[node].number)
				print('\tElement nodes:', elm_nodes)
				if result != 'None':
					if solution in self.model.selected_elements[element].solutions:
						if result == 'elementforce':
							print('\tElementforce [FX, FY1, FZ1, MX1, MY1, MZ1, FY2, FZ2, MX2, MY2, MZ2]')
							print('\t', self.model.selected_elements[element].solutions[solution][result])
						elif result in ['stress', 'strain']:
							print('\tS'+result[1:]+' [VonMises, MaxPrincipal, MinPrincipal, MaxShear]')
							VonMises = 0
							MaxPrincipal = 0
							MinPrincipal = 0
							MaxShear = 0
							for node in self.model.selected_elements[element].solutions[solution][result]['nodal']:
								if VonMises < self.model.selected_elements[element].solutions[solution][result]['nodal'][node]['VonMises']:
									VonMises = self.model.selected_elements[element].solutions[solution][result]['nodal'][node]['VonMises']
								if MaxPrincipal < self.model.selected_elements[element].solutions[solution][result]['nodal'][node]['MaxPrinc']:
									MaxPrincipal = self.model.selected_elements[element].solutions[solution][result]['nodal'][node]['MaxPrinc']
								if MinPrincipal > self.model.selected_elements[element].solutions[solution][result]['nodal'][node]['MinPrinc']:
									MinPrincipal = self.model.selected_elements[element].solutions[solution][result]['nodal'][node]['MinPrinc']
								if MaxShear < self.model.selected_elements[element].solutions[solution][result]['nodal'][node]['MaxShear']:
									MaxShear = self.model.selected_elements[element].solutions[solution][result]['nodal'][node]['MaxShear']
							print('\t', [VonMises, MaxPrincipal, MinPrincipal, MaxShear])
						else:
							pass
				print('\tElement section:', self.model.selected_elements[element].section)
#				if hasattr(self.model.selected_elements[element], 'crossSection'):
#					print('\tElement cross section:', self.model.selected_elements[element].crossSection)
#				if hasattr(self.model.selected_elements[element], 'orientation'):
#					print('\tElement orientation:', self.model.selected_elements[element].orientation['x-vec'],
#													self.model.selected_elements[element].orientation['y-vec'],
#													self.model.selected_elements[element].orientation['z-vec'])
		else:
			print('\n\tPlease select the node or element you wish')
			print('\tto print out the information about.')


	def selectMesh(self):
		'''
	Select the current mesh to be seen in the
	viewer from a dialog box.
	'''
		if len(self.model.meshes) != 0:
			self.model.nodesSelected = False
			self.model.elementsSelected = False
			self.model.selected_nodes.clear()
			self.model.selected_elements.clear()
			selectMesh = {}
			selectMesh['inputs'] = {}
			selectMesh['choices'] = [ ['Mesh'], [] ]
			for mesh in	self.model.meshes:
				selectMesh['choices'][1].append(mesh)
			if self.viewer.currentMesh == 'None':
				self.viewer.currentMesh = selectMesh['choices'][1][0]
			selectMesh['current'] = {'Mesh': self.viewer.currentMesh}
			selectMesh['inOrder'] = ['Mesh']
			self.new_mesh_view = {}
			self.selectionWidget = InputDialog(selectMesh, 'Current Mesh', self.new_mesh_view)
			self.selectionWidget.window_closed.connect(self.viewer.update)
			self.selectionWidget.show()
		else:
			print('\tNo meshes to select.')


	def selectSolution(self):
		'''
	Select the current solution to be seen in the
	viewer from a dialog box.
	'''
		if len(self.model.meshes) != 0:
			self.model.nodesSelected = False
			self.model.elementsSelected = False
			self.model.selected_nodes.clear()
			self.model.selected_elements.clear()
			selectSolution = {}
			selectSolution['inputs'] = {}
			selectSolution['choices'] = [ ['Mesh', 'Solution'], {} ]
			noSolutions = True
			for mesh in	self.model.meshes:
				if self.viewer.currentMesh == 'None':
					self.viewer.currentMesh = mesh
				if len(self.model.meshes[mesh].solutions) == 0:
					pass
				else:
					noSolutions = False
					selectSolution['choices'][1][mesh] = []
					for solution in self.model.meshes[mesh].solutions:
						selectSolution['choices'][1][mesh].append(solution)
			if noSolutions:
				print('\tNo solutions to select from')
			else:
				if self.viewer.currentSolution == 'None':
					if len(self.model.meshes[self.viewer.currentMesh].solutions) != 0:
						self.viewer.currentSolution = selectSolution['choices'][1][self.viewer.currentMesh][0]
					else:
						for mesh in self.model.meshes:
							if len(self.model.meshes[mesh].solutions) != 0:
								self.viewer.currentMesh = mesh
								break
						self.viewer.currentSolution = selectSolution['choices'][1][self.viewer.currentMesh][0]
				selectSolution['current'] = {'Mesh': self.viewer.currentMesh,
											 'Solution': self.viewer.currentSolution}
				selectSolution['inOrder'] = ['Mesh', 'Solution']
				self.new_solution_view = {}
				self.selectionWidget = InputDialog(selectSolution, 'Current Solution', self.new_solution_view)
				self.selectionWidget.window_closed.connect(self.viewer.update)
				self.selectionWidget.show()
		else:
			print('\tNo meshes to select solutions from.')


	def selectResult(self):
		'''
	Select the current result to be seen in the
	viewer from a dialog box.
	'''
		if len(self.model.results) != 0:
			self.model.nodesSelected = False
			self.model.elementsSelected = False
			self.model.selected_nodes.clear()
			self.model.selected_elements.clear()
			selectResult = {}
			selectResult['inputs'] = {}
			selectResult['choices'] = [ ['Solution', 'Result', 'Subresult'], {} ]
			selectResult['current'] = {'Solution': 'None', 'Result': 'None', 'Subresult': 'None'}
			for newResults in self.model.results:
				for solution in self.model.results[newResults].solutions:
					selectResult['current']['Solution'] = solution
					selectResult['choices'][1][solution] = {}
					if self.model.results[newResults].solutions[solution].type != 'ModalDynamic':
						for result in self.model.results[newResults].solutions[solution].results:
							if result == 'displacement':
								selectResult['choices'][1][solution]['displacement'] = ['x-dir', 'y-dir', 'z-dir', 'magnitude']
								selectResult['current']['Result'] = result
								selectResult['current']['Subresult'] = 'magnitude'
							elif (result == 'nodeforce') and ('plot' in self.model.results[newResults].solutions[solution].results[result]):
								selectResult['choices'][1][solution]['nodeforce'] = ['Force', 'Moment']
								selectResult['current']['Result'] = result
								selectResult['current']['Subresult'] = 'Force'
							elif (result == 'elementforce') and ('plot' in self.model.results[newResults].solutions[solution].results[result]):
								selectResult['choices'][1][solution]['elementforce'] = ['FX', 'FY', 'FZ', 'MX', 'MY', 'MZ']
								selectResult['current']['Result'] = result
								selectResult['current']['Subresult'] = 'FX'
							elif (result == 'stress') and ('plot' in self.model.results[newResults].solutions[solution].results[result]):
								selectResult['choices'][1][solution]['stress'] = ['VonMises', 'MaxPrinc', 'MinPrinc', 'MaxShear']
								selectResult['current']['Result'] = result
								selectResult['current']['Subresult'] = 'VonMises'
							elif (result == 'strain') and ('plot' in self.model.results[newResults].solutions[solution].results[result]):
								selectResult['choices'][1][solution]['strain'] = ['VonMises', 'MaxPrinc', 'MinPrinc', 'MaxShear']
								selectResult['current']['Result'] = result
								selectResult['current']['Subresult'] = 'VonMises'
							elif result == 'modeshapes':
								selectResult['choices'][1][solution]['modeshapes'] = []
								selectResult['current']['Result'] = result
								selectResult['current']['Subresult'] = 'mode1'
								for mode in range(len(self.model.results[newResults].solutions[solution].eigenfrequencies)):
									selectResult['choices'][1][solution]['modeshapes'].append('mode'+str(mode+1))
							else:
								pass
					else:
						if len(self.model.results[newResults].solutions[solution].displacement) > 0:
							selectResult['choices'][1][solution]['displacement'] = \
											['Node '+str(node) for node in self.model.results[newResults].solutions[solution].displacement]
							selectResult['current']['Result'] = 'displacement'
							selectResult['current']['Subresult'] = selectResult['choices'][1][solution]['displacement'][0]
						if len(self.model.results[newResults].solutions[solution].velocity) > 0:
							selectResult['choices'][1][solution]['velocity'] = \
											['Node '+str(node) for node in self.model.results[newResults].solutions[solution].velocity]
							selectResult['current']['Result'] = 'velocity'
							selectResult['current']['Subresult'] = selectResult['choices'][1][solution]['velocity'][0]
						if len(self.model.results[newResults].solutions[solution].acceleration) > 0:
							selectResult['choices'][1][solution]['acceleration'] = \
											['Node '+str(node) for node in self.model.results[newResults].solutions[solution].acceleration]
							selectResult['current']['Result'] = 'acceleration'
							selectResult['current']['Subresult'] = selectResult['choices'][1][solution]['acceleration'][0]
						if len(self.model.results[newResults].solutions[solution].frf_accel) > 0:
							selectResult['choices'][1][solution]['frf_accel'] = \
											['Node '+str(node) for node in self.model.results[newResults].solutions[solution].frf_accel]
							selectResult['current']['Result'] = 'frf_accel'
							selectResult['current']['Subresult'] = selectResult['choices'][1][solution]['frf_accel'][0]

						
			selectResult['inOrder'] = ['Solution', 'Result', 'Subresult']
			if len(self.current_results) != 0:
				if self.current_results['Solution'] != 'None':
					selectResult['current']['Solution'] = self.current_results['Solution']
					selectResult['current']['Result'] = self.current_results['Result']
					selectResult['current']['Subresult'] = self.current_results['Subresult']
			else:
				pass
			self.current_results = {}
			self.viewer.viewNewResults = True
			self.selectionWidget = InputDialog(selectResult, 'Current Result', self.current_results)
			self.selectionWidget.window_closed.connect(self.viewer.update)
			self.viewer.viewLoadingMessage = True
			self.viewer.update()
			self.selectionWidget.show()
		else:
			print('\tNo meshes to select solutions from.')


	def createMesh(self):
		'''
	Create a new mesh from elements in specific
	elementsets. User writes in name of mesh and
	the elementsets wanted in dialog box.
	'''
		createMesh = {}
		meshnum = 1
		for mesh in sorted(self.model.meshes):
			if mesh[:5] == 'mesh-':
				if mesh[5:].isdigit():
					meshnum = int(mesh[5:])+1
		createMesh['inputs'] = {'Name': 'mesh-'+str(meshnum), 'Elementsets': '1, 2, 4, 7'}
		createMesh['choices'] = [ [], [] ]
		createMesh['current'] = {}
		createMesh['inOrder'] = ['Name', 'Elementsets']
		self.new_mesh = {}
		self.selectionWidget = InputDialog(createMesh, 'Create Mesh', self.new_mesh)
		self.selectionWidget.window_closed.connect(self.viewer.update)
		self.selectionWidget.show()


	def resizeElements(self):
		'''
	Scales up or down the size of the selected 
	elements based on a scalar provided by the 
	user using dialog box.
	'''
		if self.viewer.currentMesh != 'None':
			text, ok = QtWidgets.QInputDialog.getText(self, 'Resize Elements', 'Resize the selected\nelements by a factor of:')
			if ok:
				try:
					factor = float(str(text))
				except ValueError:
					print('\n\tThe factor must be a number. Elements were not resized.')
				else:
					mesh = self.model.meshes[self.viewer.currentMesh]
					print('\n\tResizing mesh...', end=' ')
					nodes = []
					for element in self.model.selected_elements:
						for node in mesh.elements[element].nodes:
							if node.number not in nodes:
								nodes.append(node.number)
					coord_min = [mesh.nodes[nodes[ 0]].coord[0][0],
								 mesh.nodes[nodes[ 0]].coord[1][0],
								 mesh.nodes[nodes[ 0]].coord[2][0]]
					coord_max = [mesh.nodes[nodes[-1]].coord[0][0],
								 mesh.nodes[nodes[-1]].coord[1][0],
								 mesh.nodes[nodes[-1]].coord[2][0]]
					for node in nodes:
						if mesh.nodes[node].coord[0][0] < coord_min[0]:
							coord_min[0] = mesh.nodes[node].coord[0][0]
						if mesh.nodes[node].coord[1][0] < coord_min[1]:
							coord_min[1] = mesh.nodes[node].coord[1][0]
						if mesh.nodes[node].coord[2][0] < coord_min[2]:
							coord_min[2] = mesh.nodes[node].coord[2][0]
						if mesh.nodes[node].coord[0][0] > coord_max[0]:
							coord_max[0] = mesh.nodes[node].coord[0][0]
						if mesh.nodes[node].coord[1][0] > coord_max[1]:
							coord_max[1] = mesh.nodes[node].coord[1][0]
						if mesh.nodes[node].coord[2][0] > coord_max[2]:
							coord_max[2] = mesh.nodes[node].coord[2][0]
					center = [(coord_max[0]+coord_min[0])/2.,(coord_max[1]+coord_min[1])/2.,(coord_max[2]+coord_min[2])/2.]
					for node in nodes:
						mesh.nodes[node].coord[0][0] -= center[0]
						mesh.nodes[node].coord[0][0] *= factor
						mesh.nodes[node].coord[0][0] += center[0]
						mesh.nodes[node].coord[1][0] -= center[1]
						mesh.nodes[node].coord[1][0] *= factor
						mesh.nodes[node].coord[1][0] += center[1]
						mesh.nodes[node].coord[2][0] -= center[2]
						mesh.nodes[node].coord[2][0] *= factor
						mesh.nodes[node].coord[2][0] += center[2]
					self.model.selected_nodes.clear()
					self.model.nodesSelected = False
					print('finished.')
					x_max = max(mesh.nodes[i].coord[0][0] for i in mesh.nodes )
					x_min = min(mesh.nodes[i].coord[0][0] for i in mesh.nodes )
					y_max = max(mesh.nodes[i].coord[1][0] for i in mesh.nodes )
					y_min = min(mesh.nodes[i].coord[1][0] for i in mesh.nodes )
					z_max = max(mesh.nodes[i].coord[2][0] for i in mesh.nodes )
					z_min = min(mesh.nodes[i].coord[2][0] for i in mesh.nodes )
					mesh.viewScope = {'max': [x_max, y_max, z_max], 'min': [x_min, y_min, z_min]}
					mesh.viewRadius = 1.25*max( (x_max-x_min)/2., (y_max-y_min)/2., (z_max-z_min)/2. )
					self.model.buildDisplayList(mesh)
					self.new_mesh_view = {'Mesh': self.viewer.currentMesh}
					self.viewer.update()
		else:
			print('\n\tNo mesh currently selected.')


	def createNode(self):
		'''
	Creates a new node with coordinates and
	node number specified by user.
	'''
		if self.viewer.currentMesh != 'None':
			createNode = {}
			nodenum = 1
			if len(self.model.meshes[self.viewer.currentMesh].nodes) != 0:
				nodenum = max(self.model.meshes[self.viewer.currentMesh].nodes.keys())+1
			createNode['inputs'] = {'Number': str(nodenum), 'x-coordinate': '0.', 'y-coordinate': '0.', 'z-coordinate': '0.'}
			createNode['choices'] = [ [], [] ]
			createNode['current'] = {}
			createNode['inOrder'] = ['Number', 'x-coordinate', 'y-coordinate', 'z-coordinate']
			self.new_node = {}
			self.selectionWidget = InputDialog(createNode, 'Create Node', self.new_node)
			self.selectionWidget.window_closed.connect(self.viewer.update)
			self.selectionWidget.show()
		else:
			print('\n\tNo mesh currently selected.')


	def moveNodes(self):
		'''
	Moves the selected nodes in x-, y- and
	z-direction as specified by user.
	'''
		if self.viewer.currentMesh != 'None':
			if len(self.model.selected_nodes) != 0:
				moveNodes = {}
				moveNodes['inputs'] = {'x-direction': '0.', 'y-direction': '0.', 'z-direction': '0.'}
				moveNodes['choices'] = [ [], [] ]
				moveNodes['current'] = {}
				moveNodes['inOrder'] = ['x-direction', 'y-direction', 'z-direction']
				self.new_node_movement = {}
				self.selectionWidget = InputDialog(moveNodes, 'Move Nodes', self.new_node_movement)
				self.selectionWidget.window_closed.connect(self.viewer.update)
				self.selectionWidget.show()
			else:
				print('\n\tNo nodes selected.')
		else:
			print('\n\tNo mesh currently selected.')


	def fuseNodes(self):
		'''
	Fuses together nodes from different elements within
	tolerance set by user using dialog box. Nodes that are
	both inside the same element cannot be fused.
	'''
		if self.viewer.currentMesh != 'None':
			if len(self.model.selected_nodes) > 1:
				text, ok = QtWidgets.QInputDialog.getText(self, 'Fuse Nodes', 'Set tolerance of max distance\nbetween nodes you wish to fuse:')
				if ok:
					try:
						float(str(text))
					except ValueError:
						print('\n\tThe tolerance must be a number. No nodes were fused.')
					else:
						tolerance = float(str(text))
						mesh = self.model.meshes[self.viewer.currentMesh]
						fused_nodes = []
						for node1 in self.model.selected_nodes:
							for node2 in self.model.selected_nodes:
								if node1 != node2:
									distance = np.sqrt((mesh.nodes[node2].coord[0][0] - mesh.nodes[node1].coord[0][0])**2 + \
											   		   (mesh.nodes[node2].coord[1][0] - mesh.nodes[node1].coord[1][0])**2 + \
											   		   (mesh.nodes[node2].coord[2][0] - mesh.nodes[node1].coord[2][0])**2)
									if distance <= tolerance:
										fused_nodes.append(tuple(sorted([node1,node2])))
						fused_nodes = sorted(set(fused_nodes))
						to_be_deleted = sorted([i[1] for i in fused_nodes])
						confirm_to_be_deleted = []
						for element in mesh.elements:
							node_in_element = False
							elm_nodes = []
							for node in range(len(mesh.elements[element].nodes)):
								if mesh.elements[element].nodes[node].number in to_be_deleted:
									# also check that no nodes that are in
									# the same element are fused together
									if len(elm_nodes) == 0:
										for elm_node in mesh.elements[element].nodes:
											elm_nodes.append(mesh.elements[element].nodes[node].number)
									for node_combo in range(len(fused_nodes))[::-1]:
										if mesh.elements[element].nodes[node].number in fused_nodes[node_combo]:
											if fused_nodes[node_combo][0] in elm_nodes and fused_nodes[node_combo][1] in elm_nodes:
												print('\tCannot fuse together two nodes that are in the same element:')
												print('\tElement:', mesh.elements[element].number)
												print('\nNodes:', fused_nodes[node_combo][0], 'and', fused_nodes[node_combo][1])
											else:
												mesh.elements[element].nodes[node] = mesh.nodes[fused_nodes[node_combo][0]]
												confirm_to_be_deleted.append(fused_nodes[node_combo][1])
						print('\tDeleting node(s):', end=' ')
						deleted = []
						for node in to_be_deleted:
							if node in confirm_to_be_deleted:
								if node in mesh.nodes:
									del mesh.nodes[node]
									deleted.append(node)
#									print(node, end=' ')
#						print(' ')

#						print('\n\tCopying nodes:', end=' ')
						if len(deleted) > 8:
							for node in sorted(deleted)[:8]:
								print(str(node)+', ', end='')
							print('...')
						else:
							print(str(sorted(deleted)[0]), end='')
							for node in sorted(deleted)[1:]:
								print(', '+str(node), end='')
							print('\n')

						self.model.selected_nodes.clear()
						self.model.nodesSelected = False
						self.model.buildDisplayList(mesh)
						self.new_mesh_view = {'Mesh': self.viewer.currentMesh}
						self.viewer.update()
			else:
				print('\n\tPlease select the nodes you wish to fuse.')
		else:
			print('\n\tNo mesh currently selected.')


	def createElements(self):
		'''
	Create new element as specified by user input.
	'''
		if self.viewer.currentMesh != 'None':
			self.new_elements = {}
			self.elementsWidget = MakeElements(self.new_elements)
			self.elementsWidget.window_closed.connect(self.viewer.update)
			self.elementsWidget.show()
		else:
			print('\n\tNo mesh currently selected.')


	def extrudeElements(self):
		'''
	Extrudes new elements from selected element(s)
	by specific instructions from user.
	'''
		if self.viewer.currentMesh != 'None':
			elm_type = []
			for element in self.model.selected_elements:
				if self.model.selected_elements[element].type not in elm_type:
					elm_type.append(self.model.selected_elements[element].type)
			if len(elm_type) != 1:
				print('\n\tCan only extrude elements of the same type at once.')
			else:
				self.new_extrusion = {}
				self.elementsWidget = ExtrudeElements(self.model.selected_elements,elm_type[0],self.new_extrusion)
				self.elementsWidget.window_closed.connect(self.viewer.update)
				self.elementsWidget.show()
		else:
			print('\n\tNo mesh currently selected.')


	def insertElements(self):
		'''
	Inserts new elements between the nodes
	selected by user.
	'''
		if self.viewer.currentMesh != 'None':
			mesh = self.model.meshes[self.viewer.currentMesh]
			if len(self.model.selected_nodes) == 2:
				nodes = [0,0]
				for i, node in enumerate(self.model.selected_nodes):
					nodes[i] = node
				if len(mesh.elements) == 0:
					num = 1
				else:
					num = max(mesh.elements)+1
				mesh.elements[num] = Element(num,None,[mesh.nodes[nodes[0]],mesh.nodes[nodes[1]]])
				mesh.elements[num].type = 'BEAM2N'
				print('\n\tNew element number:', num)
				print('\tNodes:', nodes)
			elif len(self.model.selected_nodes) == 3:
				nodes = [0,0,0]
				for i, node in enumerate(self.model.selected_nodes):
					nodes[i] = node
				if mesh.nodes[nodes[1]].coord[0][0] < mesh.nodes[nodes[0]].coord[0][0]:
					nodes[0], nodes[1] = nodes[1], nodes[0]
				if mesh.nodes[nodes[2]].coord[0][0] < mesh.nodes[nodes[0]].coord[0][0]:
					nodes[0], nodes[2] = nodes[2], nodes[0]
				c0 = np.array([mesh.nodes[nodes[0]].coord[0][0],mesh.nodes[nodes[0]].coord[1][0],mesh.nodes[nodes[0]].coord[2][0]])
				c1 = np.array([mesh.nodes[nodes[1]].coord[0][0],mesh.nodes[nodes[1]].coord[1][0],mesh.nodes[nodes[1]].coord[2][0]])
				c2 = np.array([mesh.nodes[nodes[2]].coord[0][0],mesh.nodes[nodes[2]].coord[1][0],mesh.nodes[nodes[2]].coord[2][0]])
				if np.cross((c1-c0),(c2-c0))[2] <= 0.:
					nodes[2], nodes[1] = nodes[1], nodes[2]
				if len(mesh.elements) == 0:
					num = 1
				else:
					num = max(mesh.elements)+1
				mesh.elements[num] = Element(num,None,[mesh.nodes[nodes[0]],mesh.nodes[nodes[1]],mesh.nodes[nodes[2]]])
				mesh.elements[num].type = 'TRI3N'
				print('\n\tNew element number:', num)
				print('\tNodes:', nodes)
			elif len(self.model.selected_nodes) == 4:
				nodes = [0,0,0,0]
				for i, node in enumerate(self.model.selected_nodes):
					nodes[i] = node
				c0 = np.array([mesh.nodes[nodes[0]].coord[0][0],mesh.nodes[nodes[0]].coord[1][0],mesh.nodes[nodes[0]].coord[2][0]])
				c1 = np.array([mesh.nodes[nodes[1]].coord[0][0],mesh.nodes[nodes[1]].coord[1][0],mesh.nodes[nodes[1]].coord[2][0]])
				c2 = np.array([mesh.nodes[nodes[2]].coord[0][0],mesh.nodes[nodes[2]].coord[1][0],mesh.nodes[nodes[2]].coord[2][0]])
				c3 = np.array([mesh.nodes[nodes[3]].coord[0][0],mesh.nodes[nodes[3]].coord[1][0],mesh.nodes[nodes[3]].coord[2][0]])
				if (c3-c0).dot(np.cross((c1-c0),(c2-c0))) < 0.:
					nodes[2], nodes[3] = nodes[3], nodes[2]
				if len(mesh.elements) == 0:
					num = 1
				else:
					num = max(mesh.elements)+1
				mesh.elements[num] = Element(num,None,[mesh.nodes[nodes[0]],mesh.nodes[nodes[1]],
													   mesh.nodes[nodes[2]],mesh.nodes[nodes[3]]])
				mesh.elements[num].type = 'TET4N'
				print('\n\tNew element number:', num)
				print('\tNodes:', nodes)			
			else:
				print('\n\tNeed to write functionality for inserting')
				print('\tmultiple elements at once.')

			self.model.selected_nodes.clear()
			self.model.nodesSelected = False
			self.model.buildDisplayList(mesh)
			self.new_mesh_view = {'Mesh': self.viewer.currentMesh}
			self.viewer.update()

	def convertElements(self):
		'''
	Converts one type of elements into another
	type of elements as selected by user.
	'''
		if self.viewer.currentMesh != 'None':
			elm_type = []
			for element in self.model.selected_elements:
				if self.model.selected_elements[element].type not in elm_type:
					elm_type.append(self.model.selected_elements[element].type)
			if len(elm_type) != 1:
				print('\n\tCan only convert elements of the same type at once.')
			else:
				if elm_type[0] in ['TET10N', 'TRI6N']:
					print('\n\tCannot convert elements of type '+elm_type[0]+' to any other type.')
				else:
					newConversion = {}
					newConversion['inputs'] = {}
					newConversion['choices'] = [ ['Element type'], [] ]
					if elm_type[0] == 'HEX8N':
						newConversion['choices'][1] = ['HEX20N','TET4N','TET10N']
					elif elm_type[0] == 'HEX20N':
						newConversion['choices'][1] = ['TET10N']
					elif elm_type[0] == 'TET4N':
						newConversion['choices'][1] = ['TET10N']
					elif elm_type[0] == 'QUAD4N':
						newConversion['choices'][1] = ['QUAD8N', 'TRI3N', 'TRI6N']
					elif elm_type[0] == 'QUAD8N':
						newConversion['choices'][1] = ['TRI6N']
					elif elm_type[0] == 'TRI3N':
						newConversion['choices'][1] = ['TRI6N']
					elif elm_type[0] == 'ROD2N':
						newConversion['choices'][1] = ['BEAM2N', 'BEAM2N2D', 'ROD2N2D']
					elif elm_type[0] == 'BEAM2N':
						newConversion['choices'][1] = ['BEAM2N2D', 'ROD2N', 'ROD2N2D']
					elif elm_type[0] == 'ROD2N2D':
						newConversion['choices'][1] = ['BEAM2N', 'BEAM2N2D', 'ROD2N']
					elif elm_type[0] == 'BEAM2N2D':
						newConversion['choices'][1] = ['BEAM2N', 'ROD2N', 'ROD2N2D']
					else:
						print('Unknown element type: '+elm_type[0])
					newConversion['current'] = {'Element type': newConversion['choices'][1][0]}
					newConversion['inOrder'] = ['Element type']
					self.new_conversion = {}
					self.selectionWidget = InputDialog(newConversion, 'Convert Elements', self.new_conversion)
					self.selectionWidget.window_closed.connect(self.viewer.update)
					self.selectionWidget.show()
		else:
			print('\n\tNo mesh currently selected.')


	def splitBeams(self):
		'''
	Split beam elements into smaller
	beam elements.
	'''
		if self.viewer.currentMesh == None:
			print('\n\tNo mesh currently selected.')
		else:
			text, ok = QtWidgets.QInputDialog.getText(self, 'Split beam(s)', 'Number of elements:')
			if ok:
				if str(text).isdigit():
					n_split = int(text)
					mesh = self.model.meshes[self.viewer.currentMesh]
					for element in self.model.selected_elements:
						# first create the new nodes
						new_nodes = [mesh.elements[element].nodes[0]]
						# move original nodes so that node 1 is at origin
						move = (mesh.elements[element].nodes[0].coord[0][0],
								mesh.elements[element].nodes[0].coord[1][0],
								mesh.elements[element].nodes[0].coord[2][0])
						mesh.elements[element].nodes[0].coord[0][0] = 0.
						mesh.elements[element].nodes[0].coord[1][0] = 0.
						mesh.elements[element].nodes[0].coord[2][0] = 0.
						mesh.elements[element].nodes[1].coord[0][0] -= move[0]
						mesh.elements[element].nodes[1].coord[1][0] -= move[1]
						mesh.elements[element].nodes[1].coord[2][0] -= move[2]
						for node in range(n_split-1):
							num = max(mesh.nodes)+1
							mesh.nodes[num] = Node(num,(mesh.elements[element].nodes[1].coord[0][0]+ \
														mesh.elements[element].nodes[0].coord[0][0])*((node+1)/n_split),
													   (mesh.elements[element].nodes[1].coord[1][0]+ \
														mesh.elements[element].nodes[0].coord[1][0])*((node+1)/n_split),
													   (mesh.elements[element].nodes[1].coord[2][0]+ \
														mesh.elements[element].nodes[0].coord[2][0])*((node+1)/n_split))	
							new_nodes.append(mesh.nodes[num])
						new_nodes.append(mesh.elements[element].nodes[1])
						# move all nodes back to where the original nodes where
						for node in new_nodes:
							node.coord[0][0] += move[0]
							node.coord[1][0] += move[1]
							node.coord[2][0] += move[2]
						# then create smaller duplicates of original element
						for elm in range(n_split):
							num = max(mesh.elements)+1
							mesh.elements[num] = Element(num,None,[new_nodes[elm],new_nodes[elm+1]])
							mesh.elements[num].type = mesh.elements[element].type
					# then delete original elements
					for element in self.model.selected_elements:
						del mesh.elements[element]

					self.model.selected_elements.clear()
					self.model.elementsSelected = False
					self.model.buildDisplayList(mesh)
					self.new_mesh_view = {'Mesh': self.viewer.currentMesh}
					self.viewer.update()
				else:
					print('\n\tCan only split beam into a whole number of smaller elements, not '+str(text)+' elements.')


	def beamOrientation(self):
		'''
	Set beam orientation on beam elements.
	'''
		if self.viewer.currentMesh != 'None':
			elements = []
			for element in self.model.selected_elements:
				if self.model.selected_elements[element].type not in ['BEAM2N', 'BEAM2N2D']:
					print('\n\tCan only apply beam orientation on BEAM2N or BEAM2N2D.')
					print('\tElement', self.model.selected_elements[element].number, 'is a', self.model.selected_elements[element].type, 'element.')
				else:
					elements.append(element)
			if len(elements) > 0:
				orientBeam = {}
				orientBeam['inputs'] = {'x-vector': '1., 0., 0.',
										'y-vector': '0., 1., 0.'}
				orientBeam['choices'] = [ [], [] ]
				orientBeam['current'] = {}
				orientBeam['inOrder'] = ['x-vector', 'y-vector']
				self.new_node = {}
				self.selectionWidget = InputDialog(orientBeam, 'Beam orientation', self.new_orientation)
				self.selectionWidget.window_closed.connect(self.viewer.update)
				self.selectionWidget.show()
			else:
				print('\n\tNo beam elements selected to apply orientation.')
		else:
			print('\n\tNo mesh currently selected.')


	def hideElements(self):
		'''
	Hides selected elements from viewer.
	'''
		if self.viewer.viewResults:
			solution  = self.viewer.currentDisplayList['solution']
			result    = self.viewer.currentDisplayList['result']
			subresult = self.viewer.currentDisplayList['subresult']
			currentMesh = self.viewer.currentDisplayList['mesh']
			if result == 'modeshapes':
				print('\n\tNo hiding elements when result is modeshapes.')
			else:
				hide = self.model.selected_elements.keys()
				nodes = {}
				elements = {}
				for element in currentMesh.elements:
					if element not in hide:
						elements[element] = currentMesh.elements[element]
						for node in elements[element].nodes:
							if node.number not in nodes:
								nodes[node.number] = node
				self.model.meshes['tmpmesh'] = Mesh(nodes,elements)
				self.model.meshes['tmpmesh'].is3D = True

				self.model.meshes['tmpmesh'].solutions = currentMesh.solutions
				self.model.meshes['tmpmesh'].viewScope = currentMesh.viewScope
				self.model.meshes['tmpmesh'].viewRadius = currentMesh.viewRadius
				self.model.meshes['tmpmesh'].displayLists = {'solutions': {}}

				self.model.buildDisplayList(self.model.meshes['tmpmesh'],[solution,result,subresult])
				self.model.selected_elements.clear()
				self.model.selected_nodes.clear()
				self.viewer.viewNewResults = True
				self.current_results = {'Solution': solution, 'Result': result, 'Subresult': subresult}
				self.viewer.update()
		elif len(self.model.selected_elements) != 0:
			hide = self.model.selected_elements.keys()
			if self.viewer.currentMesh == 'None':
				currentMesh = self.viewer.currentDisplayList['mesh']
			else:
				currentMesh = self.model.meshes[self.viewer.currentMesh]
			nodes = {}
			elements = {}
			for element in currentMesh.elements:
				if element not in hide:
					elements[element] = currentMesh.elements[element]
					for node in elements[element].nodes:
						if node.number not in nodes:
							nodes[node.number] = node
			if self.viewer.currentMesh == 'tmpmesh':
				is3D = False
				if hasattr(self.model.meshes['tmpmesh'],'is3D'):
					is3D = True
				solutions  = self.model.meshes['tmpmesh'].solutions
				viewScope  = self.model.meshes['tmpmesh'].viewScope
				viewRadius = self.model.meshes['tmpmesh'].viewRadius
				self.model.meshes['tmpmesh'] = Mesh(nodes,elements)
				self.model.checkForSection(self.model.meshes['tmpmesh'])
				self.model.meshes['tmpmesh'].solutions  = solutions
				self.model.meshes['tmpmesh'].viewScope  = viewScope
				self.model.meshes['tmpmesh'].viewRadius = viewRadius
				self.model.meshes['tmpmesh'].displayLists = {'solutions': {}}
				if is3D:
					self.model.meshes['tmpmesh'].is3D = True
			else:
				self.viewer.currentMesh_reset = self.viewer.currentMesh
				self.model.meshes['tmpmesh'] = Mesh(nodes,elements)
				self.model.checkForSection(self.model.meshes['tmpmesh'])
				if hasattr(currentMesh,'is3D'):
					self.model.meshes['tmpmesh'].is3D = True
				self.model.meshes['tmpmesh'].solutions = currentMesh.solutions
				self.model.meshes['tmpmesh'].viewScope = currentMesh.viewScope
				self.model.meshes['tmpmesh'].viewRadius = currentMesh.viewRadius
				self.model.meshes['tmpmesh'].displayLists = {'solutions': {}}
			self.model.buildDisplayList(self.model.meshes['tmpmesh'])
			self.model.selected_elements.clear()
			self.model.selected_nodes.clear()
			self.new_mesh_view = {'Mesh': 'tmpmesh'}
			self.viewer.update()
		else:
			print('\n\tNo elements selected.')


	def showElements(self):
		'''
	Restores any hidden elements back into viewer.
	'''
		if hasattr(self.viewer,'currentMesh_reset'):
			self.viewer.currentMesh = self.viewer.currentMesh_reset
			self.model.buildDisplayList(self.model.meshes[self.viewer.currentMesh])
			self.new_mesh_view = {'Mesh': self.viewer.currentMesh}
			del self.model.meshes['tmpmesh']
			del self.viewer.currentMesh_reset
			self.viewer.update()
		elif self.viewer.currentDisplayList['solution'] == 'None':
			pass
		else:
			solution  = self.viewer.currentDisplayList['solution']
			result    = self.viewer.currentDisplayList['result']
			subresult = self.viewer.currentDisplayList['subresult']
			currentMesh = self.viewer.currentDisplayList['mesh']
			if result == 'modeshapes':
				print('\n\tNo hiding elements when result is modeshapes')
			else:
				self.model.buildDisplayList(currentMesh,[solution,result,subresult])
				self.model.selected_elements.clear()
				self.model.selected_nodes.clear()
				self.viewer.viewNewResults = True
				self.current_results = {'Solution': solution, 'Result': result, 'Subresult': subresult}
				self.viewer.update()


	def renumberNodes(self,first_number=False):
		'''
	Renumbers the selected nodes.
	'''
		if self.viewer.currentMesh == None:
			print('\n\tNo mesh currently selected.')
		else:
			if first_number == False:
				text, ok = QtWidgets.QInputDialog.getText(self, 'Renumber Nodes', 'First node number:')
			else:
				text = first_number
				ok = True
			if ok:
				if str(text).isdigit():
					firstNumber = int(text)
					newNumbers_in_range = False
					node_range = len(self.model.selected_nodes)
					for node in sorted(self.model.selected_nodes):
						if node in range(firstNumber,firstNumber+node_range):
							newNumbers_in_range = True
					if newNumbers_in_range:
						print('\n\tCannot change node numbers if any of the current node numbers')
						print('\tare inside the range of the new node numbers.')
					else:
						old_selected = sorted(self.model.selected_nodes.keys())
						new_selected = {}
						elements = self.model.meshes[self.viewer.currentMesh].elements
						nodes = self.model.meshes[self.viewer.currentMesh].nodes

						all_nodes = sorted(nodes.keys())
						for node in all_nodes:
							if node in old_selected:
								newNumber = firstNumber+old_selected.index(node)
								nodes[newNumber] = nodes[node]
								del nodes[node]
								nodes[newNumber].number = newNumber
								new_selected[newNumber] = nodes[newNumber]

						self.model.selected_nodes = new_selected
						print('\n\tRenumbering selected nodes in', self.viewer.currentMesh)
				else:
					print('\n\tThat is not an acceptable node number.')


	def renumberElements(self,first_number=False):
		'''
	Renumbers the selected elements.
	'''
		if self.viewer.currentMesh == None:
			print('\n\tNo mesh currently selected.')
		else:
			if first_number == False:
				text, ok = QtWidgets.QInputDialog.getText(self, 'Renumber Elements', 'First element number:')
			else:
				text = first_number
				ok = True
			if ok:
				if str(text).isdigit():
					newNumber = int(text)
					newNumbers_in_range = False
					element_range = len(self.model.selected_elements)
					for element in sorted(self.model.selected_elements):
						if element in range(newNumber,newNumber+element_range):
							newNumbers_in_range = True
					if newNumbers_in_range:
						print('\n\tCannot change element numbers if any of the current element numbers')
						print('\tare inside the range of the new element numbers.')
					else:
						new_selected = {}
						for element in sorted(self.model.selected_elements):
							self.model.meshes[self.viewer.currentMesh].elements[newNumber] = \
								self.model.meshes[self.viewer.currentMesh].elements.pop(element)
							new_selected[newNumber] = self.model.meshes[self.viewer.currentMesh].elements[newNumber]
							self.model.meshes[self.viewer.currentMesh].elements[newNumber].number = newNumber
							newNumber += 1
						self.model.selected_elements = new_selected
						print('\n\tRenumbering selected elements in', self.viewer.currentMesh)
				else:
					print('\n\tThat is not an acceptable element number.')


	def copyNodes(self):
		'''
	Copies the selected nodes and offsets
	their location by a vector specified by user.
	'''
		if self.model.nodesSelected == False:
			print('\n\tNo nodes selected.')
		else:
			text, ok = QtWidgets.QInputDialog.getText(self, 'Copy node(s)', 'Offset by vector:', \
														text=str(2*self.model.meshes[self.viewer.currentMesh].viewRadius)+', 0., 0.')
			if ok:
				try:
					vector = [float(x.strip()) for x in text.split(',')]
				except ValueError:
					print('\n\tWrong input given for offset vector. Must be specified')
					print('\twith three numbers separated by comma, example: 1., 0., 0.')
				else:
					if len(vector) != 3:
						print('\n\tWrong input given for offset vector. Must be specified')
						print('\twith three numbers separated by comma, example: 1., 0., 0.')
					else:
						mesh = self.model.meshes[self.viewer.currentMesh]
						# copy nodes and move with offset vector
						new_nodes = {}
						copied_nodes = []
						for node in self.model.selected_nodes:
							if mesh.nodes[node].number not in copied_nodes:
								copied_nodes.append(mesh.nodes[node].number)
								node_num = max(mesh.nodes)+1
								mesh.nodes[node_num] = Node(node_num,deepcopy(mesh.nodes[node].coord[0][0])+vector[0],
																	 deepcopy(mesh.nodes[node].coord[1][0])+vector[1],
																	 deepcopy(mesh.nodes[node].coord[2][0])+vector[2])
								new_nodes[mesh.nodes[node].number] = node_num
							
						print('\n\tCopying nodes:', end=' ')
						if len(self.model.selected_nodes) > 8:
							for node in sorted(self.model.selected_nodes)[:8]:
								print(str(node)+', ', end='')
							print('...')
						else:
							print(str(sorted(self.model.selected_nodes)[0]), end='')
							for node in sorted(self.model.selected_nodes)[1:]:
								print(', '+str(node), end='')
							print('\n')
						self.model.selected_nodes.clear()
						self.model.nodesSelected = False
						
						x_max = max(mesh.nodes[i].coord[0][0] for i in mesh.nodes )
						x_min = min(mesh.nodes[i].coord[0][0] for i in mesh.nodes )
						y_max = max(mesh.nodes[i].coord[1][0] for i in mesh.nodes )
						y_min = min(mesh.nodes[i].coord[1][0] for i in mesh.nodes )
						z_max = max(mesh.nodes[i].coord[2][0] for i in mesh.nodes )
						z_min = min(mesh.nodes[i].coord[2][0] for i in mesh.nodes )
						mesh.viewScope = {'max': [x_max, y_max, z_max], 'min': [x_min, y_min, z_min]}
						mesh.viewRadius = 1.25*max( (x_max-x_min)/2., (y_max-y_min)/2., (z_max-z_min)/2. )					
						self.model.buildDisplayList(mesh)
						self.new_mesh_view = {'Mesh': self.viewer.currentMesh}
						self.viewer.update()


	def copyElements(self):
		'''
	Copies the selected elements and offsets
	their location by a vector specified by user.
	'''
		if self.model.elementsSelected == False:
			print('\n\tNo elements selected.')
		else:
			text, ok = QtWidgets.QInputDialog.getText(self, 'Copy element(s)', 'Offset by vector:', \
														text=str(2*self.model.meshes[self.viewer.currentMesh].viewRadius)+', 0., 0.')
			if ok:
				try:
					vector = [float(x.strip()) for x in text.split(',')]
				except ValueError:
					print('\n\tWrong input given for offset vector. Must be specified')
					print('\twith three numbers separated by comma, example: 1., 0., 0.')
				else:
					if len(vector) != 3:
						print('\n\tWrong input given for offset vector. Must be specified')
						print('\twith three numbers separated by comma, example: 1., 0., 0.')
					else:
						mesh = self.model.meshes[self.viewer.currentMesh]
						# first copy nodes and move with offset vector
						new_nodes = {}
						copied_nodes = []
						element_nodes = {}
						for element in self.model.selected_elements:
							
							element_nodes[mesh.elements[element].number] = []
							for node in mesh.elements[element].nodes:
								if node.number not in copied_nodes:
									copied_nodes.append(node.number)
									node_num = max(mesh.nodes)+1
									mesh.nodes[node_num] = Node(node_num,deepcopy(node.coord[0][0])+vector[0],
																		 deepcopy(node.coord[1][0])+vector[1],
																		 deepcopy(node.coord[2][0])+vector[2])
									new_nodes[node.number] = node_num
									element_nodes[mesh.elements[element].number].append(mesh.nodes[node_num])
								else:
									element_nodes[mesh.elements[element].number].append(mesh.nodes[new_nodes[node.number]])
							
						# then copy the elements and map them to the
						# already copied nodes
						for element in self.model.selected_elements:
							elm_num = max(mesh.elements)+1
							mesh.elements[elm_num] = Element(elm_num,None,element_nodes[mesh.elements[element].number])
							mesh.elements[elm_num].type = mesh.elements[element].type

						print('\n\tCopying elements:', end=' ')
						if len(self.model.selected_elements) > 8:
							for element in sorted(self.model.selected_elements)[:8]:
								print(str(element)+', ', end='')
							print('...')
						else:
							print(str(sorted(self.model.selected_elements)[0]), end='')
							for element in sorted(self.model.selected_elements)[1:]:
								print(', '+str(element), end='')
							print('\n')
						self.model.selected_elements.clear()
						self.model.elementsSelected = False
						
						x_max = max(mesh.nodes[i].coord[0][0] for i in mesh.nodes )
						x_min = min(mesh.nodes[i].coord[0][0] for i in mesh.nodes )
						y_max = max(mesh.nodes[i].coord[1][0] for i in mesh.nodes )
						y_min = min(mesh.nodes[i].coord[1][0] for i in mesh.nodes )
						z_max = max(mesh.nodes[i].coord[2][0] for i in mesh.nodes )
						z_min = min(mesh.nodes[i].coord[2][0] for i in mesh.nodes )
						mesh.viewScope = {'max': [x_max, y_max, z_max], 'min': [x_min, y_min, z_min]}
						mesh.viewRadius = 1.25*max( (x_max-x_min)/2., (y_max-y_min)/2., (z_max-z_min)/2. )					
						self.model.buildDisplayList(mesh)
						self.new_mesh_view = {'Mesh': self.viewer.currentMesh}
						self.viewer.update()


	def mirrorCopyElements(self):
		'''
	Copies the selected elements and offsets
	their location by a vector specified by user.
	'''
		if self.model.elementsSelected == False:
			print('\n\tNo elements selected.')
		else:
			text, ok = QtWidgets.QInputDialog.getText(self, 'Mirror element(s)', 'About plane (ex. x-y):', text='x-y')
			if ok:
				plane = str(text)
				if plane not in ['x-y', 'X-Y', 'y-x', 'Y-X',
								 'x-z', 'X-Z', 'z-x', 'Z-X',
								 'y-z', 'Y-Z', 'z-y', 'Z-Y']:
					print('\n\tWrong input for plane to mirror elements about.')
					print('\tMust be either x-y, x-z or y-z.')
				else:
					x = y = z = 1
					if plane in ['x-y', 'X-Y', 'y-x', 'Y-X']:
						z = -1
						tet4_reshuffle = [1,0,2,3] # OK
						tet10_reshuffle = [1,0,2,3,4,6,5,8,7,9] # OK
						hex8_reshuffle = [3,2,1,0,7,6,5,4] # OK
						hex20_reshuffle = [3,2,1,0,7,6,5,4,10,9,8,11,15,14,13,12,18,17,16,19] # OK
					elif plane in ['x-z', 'X-Z', 'z-x', 'Z-X']:
						y = -1
						tet4_reshuffle = [1,0,2,3] # OK
						tet10_reshuffle = [1,0,2,3,4,6,5,8,7,9] # OK
						hex8_reshuffle = [4,5,6,7,0,1,2,3] # OK
						hex20_reshuffle = [4,5,6,7,0,1,2,3,16,17,18,19,12,13,14,15,8,9,10,11] # OK
						tri3_reshuffle = [1,0,2] # OK
						tri6_reshuffle = [1,0,2,3,5,4] # OK
						quad4_reshuffle = [3,2,1,0] # OK
						quad8_reshuffle = [6,5,4,3,2,1,0,7] # OK
					else:
						x = -1
						tet4_reshuffle = [1,0,2,3] # OK
						tet10_reshuffle = [1,0,2,3,4,6,5,8,7,9] # OK
						hex8_reshuffle = [1,0,3,2,5,4,7,6] # OK
						hex20_reshuffle = [1,0,3,2,5,4,7,6,8,11,10,9,13,12,15,14,16,19,18,17] # OK
						tri3_reshuffle = [1,0,2] # OK
						tri6_reshuffle = [1,0,2,3,5,4] # OK
						quad4_reshuffle = [1,0,3,2] # OK
						quad8_reshuffle = [2,1,0,7,6,5,4,3] # OK
					mesh = self.model.meshes[self.viewer.currentMesh]
					# first copy nodes and mirror with plane specified
					new_nodes = {}
					copied_nodes = []
					element_nodes = {}
					for element in self.model.selected_elements:
						if mesh.elements[element].type in ['BEAM2N2D', 'ROD2N2D', 'QUAD4N', 'QUAD8N', 'TRI3N', 'TRI6N'] and plane in ['x-y', 'X-Y']:
							print('\n\tCannot mirror copy 2D elements about x-y plane.')
							break
						element_nodes[mesh.elements[element].number] = []
						for node in mesh.elements[element].nodes:
							if node.number not in copied_nodes:
								copied_nodes.append(node.number)
								node_num = max(mesh.nodes)+1
								mesh.nodes[node_num] = Node(node_num,deepcopy(node.coord[0][0])*x,
																	 deepcopy(node.coord[1][0])*y,
																	 deepcopy(node.coord[2][0])*z)
								new_nodes[node.number] = node_num
								element_nodes[mesh.elements[element].number].append(mesh.nodes[node_num])
							else:
								element_nodes[mesh.elements[element].number].append(mesh.nodes[new_nodes[node.number]])
							
					# then copy the elements and map them to the
					# already copied nodes
					for element in self.model.selected_elements:
						if mesh.elements[element].type in ['BEAM2N2D', 'ROD2N2D', 'QUAD4N', 'QUAD8N', 'TRI3N', 'TRI6N'] and plane in ['x-y', 'X-Y']:
							break
						elm_num = max(mesh.elements)+1
						mesh.elements[elm_num] = Element(elm_num,None,element_nodes[mesh.elements[element].number])
						mesh.elements[elm_num].type = mesh.elements[element].type
						# reshuffle nodes because they were mirrored
						if mesh.elements[elm_num].type == 'TET4N':
							mesh.elements[elm_num].nodes = [mesh.elements[elm_num].nodes[x] for x in tet4_reshuffle]
						elif mesh.elements[elm_num].type == 'TET10N':
							mesh.elements[elm_num].nodes = [mesh.elements[elm_num].nodes[x] for x in tet10_reshuffle]
						elif mesh.elements[elm_num].type == 'HEX8N':
							mesh.elements[elm_num].nodes = [mesh.elements[elm_num].nodes[x] for x in hex8_reshuffle]
						elif mesh.elements[elm_num].type == 'HEX20N':
							mesh.elements[elm_num].nodes = [mesh.elements[elm_num].nodes[x] for x in hex20_reshuffle]
						elif mesh.elements[elm_num].type == 'TRI3N':
							mesh.elements[elm_num].nodes = [mesh.elements[elm_num].nodes[x] for x in tri3_reshuffle]
						elif mesh.elements[elm_num].type == 'TRI6N':
							mesh.elements[elm_num].nodes = [mesh.elements[elm_num].nodes[x] for x in tri6_reshuffle]
						elif mesh.elements[elm_num].type == 'QUAD4N':
							mesh.elements[elm_num].nodes = [mesh.elements[elm_num].nodes[x] for x in quad4_reshuffle]
						elif mesh.elements[elm_num].type == 'QUAD8N':
							mesh.elements[elm_num].nodes = [mesh.elements[elm_num].nodes[x] for x in quad8_reshuffle]
						else:
							pass

					print('\n\tCopying elements:', end=' ')
					if len(self.model.selected_elements) > 8:
						for element in sorted(self.model.selected_elements)[:8]:
							print(str(element)+', ', end='')
						print('...')
					else:
						print(str(sorted(self.model.selected_elements)[0]), end='')
						for element in sorted(self.model.selected_elements)[1:]:
							print(', '+str(element), end='')
						print('\n')
					self.model.selected_elements.clear()
					self.model.elementsSelected = False
						
					x_max = max(mesh.nodes[i].coord[0][0] for i in mesh.nodes )
					x_min = min(mesh.nodes[i].coord[0][0] for i in mesh.nodes )
					y_max = max(mesh.nodes[i].coord[1][0] for i in mesh.nodes )
					y_min = min(mesh.nodes[i].coord[1][0] for i in mesh.nodes )
					z_max = max(mesh.nodes[i].coord[2][0] for i in mesh.nodes )
					z_min = min(mesh.nodes[i].coord[2][0] for i in mesh.nodes )
					mesh.viewScope = {'max': [x_max, y_max, z_max], 'min': [x_min, y_min, z_min]}
					mesh.viewRadius = 1.25*max( (x_max-x_min)/2., (y_max-y_min)/2., (z_max-z_min)/2. )					
					self.model.buildDisplayList(mesh)
					self.new_mesh_view = {'Mesh': self.viewer.currentMesh}
					self.viewer.update()


	def moveElements(self):
		'''
	Moves the elements of a specified
	elementset in direction set by user.
	'''
		moveElm = {}
		moveElm['inputs'] = {'x-direction': '0.', 'y-direction': '0.', 'z-direction': '0.'}
		moveElm['choices'] = [ [], [] ]
		moveElm['current'] = {}
		moveElm['inOrder'] = ['x-direction', 'y-direction', 'z-direction']
		self.new_position = {}
		self.selectionWidget = InputDialog(moveElm, 'Move Elements', self.new_position)
		self.selectionWidget.window_closed.connect(self.viewer.update)
		self.selectionWidget.show()


	def rotateElements(self):
		'''
	Rotates the elements of a specified
	elementset as directed by user.
	'''
		rotateElm = {}
		rotateElm['inputs'] = {'Rotation axis node 1\n(uses only this if 2D elements)': '1', 'Rotation axis node 2': '2', 'Angle': '90'}
		rotateElm['choices'] = [ [], [] ]
		rotateElm['current'] = {}
		rotateElm['inOrder'] = ['Rotation axis node 1\n(uses only this if 2D elements)', 'Rotation axis node 2', 'Angle']
		self.new_rotation = {}
		self.selectionWidget = InputDialog(rotateElm, 'Rotate Elements', self.new_rotation)
		self.selectionWidget.window_closed.connect(self.viewer.update)
		self.selectionWidget.show()


	def measureDistance(self):
		'''
	Measure the distance between two selected nodes.
	'''
		if self.viewer.currentMesh != 'None':
			if len(self.model.selected_nodes.keys()) == 2:
				[node1, node2] = self.model.selected_nodes.keys()
				distance = np.sqrt((self.model.meshes[self.viewer.currentMesh].nodes[node1].coord[0][0] - \
									self.model.meshes[self.viewer.currentMesh].nodes[node2].coord[0][0])**2 + \
								   (self.model.meshes[self.viewer.currentMesh].nodes[node1].coord[1][0] - \
									self.model.meshes[self.viewer.currentMesh].nodes[node2].coord[1][0])**2 + \
								   (self.model.meshes[self.viewer.currentMesh].nodes[node1].coord[2][0] - \
									self.model.meshes[self.viewer.currentMesh].nodes[node2].coord[2][0])**2)
				print('\n\tNode number:', node1)
				print('\tCoord:', str(self.model.meshes[self.viewer.currentMesh].nodes[node1].coord[0][0]) \
									+', '+str(self.model.meshes[self.viewer.currentMesh].nodes[node1].coord[1][0]) \
									+', '+str(self.model.meshes[self.viewer.currentMesh].nodes[node1].coord[2][0]))
				print('\n\tNode number:', node2)
				print('\tCoord:', str(self.model.meshes[self.viewer.currentMesh].nodes[node2].coord[0][0]) \
									+', '+str(self.model.meshes[self.viewer.currentMesh].nodes[node2].coord[1][0]) \
									+', '+str(self.model.meshes[self.viewer.currentMesh].nodes[node2].coord[2][0]))
				print('\n\tDistance between nodes '+str(node2)+' and '+str(node1)+': '+str(distance))
			else:
				print('\n\tTo measure distance, select two nodes.')


	def createNodeset(self):
		'''
	Create a nodeset from selected nodes in viewer
	and nodeset number as specified by user in
	dialog box.
	'''
		next_nodeset = 1
		if len(self.model.nodesets) > 0:
			next_nodeset = max(self.model.nodesets)+1
		text, ok = QtWidgets.QInputDialog.getText(self, 'Create Nodeset', 'Nodeset number:', text=str(next_nodeset))
		if ok and (len(self.model.selected_nodes) != 0):
			if str(text).isdigit():
				self.model.nodesets[int(text)] = {}
				for node in self.model.selected_nodes:
					self.model.nodesets[int(text)][node] = self.model.selected_nodes[node]
				print('\n\tNodeset number', int(text), 'created')
				toprint = self.model.selected_nodes.keys()
				toprint = sorted(toprint)
				if len(toprint) > 8:
					print('\t[', end=' ') 
					for i in range(4):
						print(str(toprint[i])+',',end=' ')
					print('...',end=' ')
					print(str(toprint[-3])+',',end=' ')
					print(str(toprint[-2])+',',end=' ')
					print(str(toprint[-1])+' ]')
				else:
					print('\t'+str(toprint))
			else:
				print('\n\t'+text+' is not a valid nodeset number')


	def createElementset(self):
		'''
	Create an elementset from selected elements in
	viewer and elementset number as specified by user
	in dialog box.
	'''
		next_elementset = 1
		if len(self.model.elementsets) > 0:
			next_elementset = max(self.model.elementsets)+1
		text, ok = QtWidgets.QInputDialog.getText(self, 'Create Elementset', 'Elementset number:', text=str(next_elementset))
		if ok and (len(self.model.selected_elements) != 0):
			if str(text).isdigit():
				self.model.elementsets[int(text)] = {}
				for elm in self.model.selected_elements:
					self.model.elementsets[int(text)][elm] = self.model.selected_elements[elm]
				print('\n\tElementset number', int(text), 'created')
				toprint = self.model.selected_elements.keys()
				toprint = sorted(toprint)
				if len(toprint) > 8:
					print('\t[',end=' ')
					for i in range(4):
						print(str(toprint[i])+',',end=' ')
					print('...',end=' ')
					print(str(toprint[-3])+',',end=' ')
					print(str(toprint[-2])+',',end=' ')
					print(str(toprint[-1])+' ]')
				else:
					print('\t'+str(toprint))
			else:
				print('\n\t'+text+' is not a valid elementset number')


	def newMaterial(self):
		'''
	Create a new material by writing in name, elasticity
	modulus, poisson ratio and density into a dialog box.
	'''
		newMaterial = {}
		matnum = 1
		for material in sorted(self.model.materials):
			if material[:9] == 'material-':
				if material[9:].isdigit():
					matnum = int(material[9:])+1
		newMaterial['inputs'] = {'Name': 'material-'+str(matnum), 'Elasticity': '0.', 'Poisson ratio': '0.', 'Density': '0.' }
		newMaterial['choices'] = [ [], [] ]
		newMaterial['current'] = {}
		newMaterial['inOrder'] = ['Name', 'Elasticity', 'Poisson ratio', 'Density']
		self.new_material = {}
		self.selectionWidget = InputDialog(newMaterial, 'Create Material', self.new_material)
		self.selectionWidget.window_closed.connect(self.viewer.update)
		self.selectionWidget.show()


	def newSection(self):
		'''
	Create a new section by writing in name and section
	properties, and selecting a material in dialog box.
	'''
		if len(self.model.materials) != 0:
			newSection = {}
			sectnum = 1
			for section in sorted(self.model.sections):
				if section[:8] == 'section-':
					if section[8:].isdigit():
						sectnum = int(section[8:])+1
			newSection['inputs'] = {'Name': 'section-'+str(sectnum), 'Thickness (2D)': '0.',
									'Area (Rod or Beam)': '0.', 'Izz (Beam)': '0.', 'Iyy (Beam 3D)': '0.'}
			newSection['choices'] = [ ['Material'], [ ] ]
			for material in self.model.materials:
				newSection['choices'][1].append(material)
			newSection['current'] = {'Material': newSection['choices'][1][0]}
			newSection['inOrder'] = ['Name', 'Material', 'Thickness (2D)', 
									 'Area (Rod or Beam)', 'Izz (Beam)', 'Iyy (Beam 3D)']
			self.new_section = {}
			self.selectionWidget = InputDialog(newSection, 'Create Section', self.new_section)
			self.selectionWidget.window_closed.connect(self.viewer.update)
			self.selectionWidget.show()
		else:
			print('\n\tNo materials available. Section cannot be created.')


	def newBeamSection(self):
		'''
	Modify an existing section by selecting it and the
	desired type of beam cross-section with meassurements,
	to generate the properties (Area, Izz, Iyy) which define
	the cross-section.
	'''
		if len(self.model.sections) != 0:
			self.modified_section = {}
			for section in self.model.sections:
				self.modified_section[section] = self.model.sections[section] 
			self.elementsWidget = ModifyBeamSection(self.modified_section)
			self.elementsWidget.window_closed.connect(self.viewer.update)
			self.elementsWidget.show()
		else:
			print('\n\tNo sections available to be modified.')


	def applySection(self):
		'''
	Apply a selected section to specified
	elementsets in a dialog box.
	'''
		if len(self.model.sections) != 0:
			if len(self.model.elementsets) != 0:
				sectionAssignment = {}
				sectionAssignment['inputs'] = {'Elementsets': str(max(self.model.elementsets.keys()))}
				sectionAssignment['choices'] = [ ['Section'], [] ]
				for section in self.model.sections:
					sectionAssignment['choices'][1].append(section) 
				sectionAssignment['current'] = {'Section': sectionAssignment['choices'][1][0]}
				sectionAssignment['inOrder'] = ['Section', 'Elementsets']
				self.new_section_assignment = {}
				self.selectionWidget = InputDialog(sectionAssignment, 'Apply Section', self.new_section_assignment)
				self.selectionWidget.window_closed.connect(self.viewer.update)
				self.selectionWidget.show()
			else:
				print('\n\tNo elementsets to choose from.')
		else:
			print('\n\tNo sections available to apply.')


	def solveStatic(self):
		'''
	Create a new static solution by writing
	in the name and selecting the mesh in a
	dialog box.
	'''
		if len(self.model.meshes) != 0:
			newStatic = {}
			solnum = 1
			for mesh in self.model.meshes:
				for solution in self.model.meshes[mesh].solutions:
					if solution[:9] == 'solution-':
						if solution[9:].isdigit():
							if int(solution[9:])+1 > solnum:
								solnum = int(solution[9:])+1
			newStatic['inputs'] = {'Name': 'solution-'+str(solnum), 'Results': 'disp, strs, strn, nodf, elmf'}
			newStatic['choices'] = [ ['Mesh'], [] ]
			for mesh in self.model.meshes:
				newStatic['choices'][1].append(mesh)
			newStatic['current'] = {'Mesh': newStatic['choices'][1][0]}
			newStatic['inOrder'] = ['Name', 'Mesh', 'Results']
			self.new_solution = {'Type': 'Static'}
			self.selectionWidget = InputDialog(newStatic, 'Static Solution', self.new_solution)
			self.selectionWidget.window_closed.connect(self.viewer.update)
			self.selectionWidget.show()
		else:
			print('\n\tNo meshes to select. Cannot create solution without mesh.')


	def solveEigenmodes(self):
		'''
	Create a new eigenmodes solution by writing
	in the name and selecting the mesh in a
	dialog box.
	'''
		if len(self.model.meshes) != 0:
			newEigen = {}
			solnum = 1
			for mesh in self.model.meshes:
				for solution in self.model.meshes[mesh].solutions:
					if solution[:9] == 'solution-':
						if solution[9:].isdigit():
							if int(solution[9:])+1 > solnum:
								solnum = int(solution[9:])+1
			newEigen['inputs'] = {'Name': 'solution-'+str(solnum)}
			newEigen['choices'] = [ ['Mesh'], [] ]
			for mesh in self.model.meshes:
				newEigen['choices'][1].append(mesh)
			newEigen['current'] = {'Mesh': newEigen['choices'][1][0]}
			newEigen['inOrder'] = ['Name', 'Mesh']
			self.new_solution = {'Type': 'Eigenmodes', 'Results': 'modes'}
			self.selectionWidget = InputDialog(newEigen, 'Eigenmodes Solution', self.new_solution)
			self.selectionWidget.window_closed.connect(self.viewer.update)
			self.selectionWidget.show()
		else:
			print('\n\tNo meshes to select. Cannot create solution without mesh.')


	def solveStaticPlastic(self):
		print('\n\tFunctionality for static nonlinear analysis not written yet')


	def solveHeatTransfer(self):
		print('\n\tFunctionality for heat transfer analysis not written yet')


	def solveModalDynamic(self):
		'''
	Create a new modal dynamic solution by 
	writing in the name and selecting the 
	mesh in a dialog box.
	'''
		if len(self.model.meshes) != 0:
			newDynamic = {}
			solnum = 1
			for mesh in self.model.meshes:
				for solution in self.model.meshes[mesh].solutions:
					if solution[:9] == 'solution-':
						if solution[9:].isdigit():
							if int(solution[9:])+1 > solnum:
								solnum = int(solution[9:])+1
			newDynamic['inputs'] = {'Name': 'solution-'+str(solnum), 'Results': 'disp, velc, accl, frf'}
			newDynamic['choices'] = [ ['Mesh'], [] ]
			for mesh in self.model.meshes:
				newDynamic['choices'][1].append(mesh)
			newDynamic['current'] = {'Mesh': newDynamic['choices'][1][0]}
			newDynamic['inOrder'] = ['Name', 'Mesh', 'Results']
			self.new_solution = {'Type': 'ModalDynamic'}
			self.selectionWidget = InputDialog(newDynamic, 'ModalDynamic Solution', self.new_solution)
			self.selectionWidget.window_closed.connect(self.viewer.update)
			self.selectionWidget.show()
		else:
			print('\n\tNo meshes to select. Cannot create solution without mesh.')



	def createSpider(self):
		'''
	Creates a rigid spider of beam elements
	between one node and a set of nodes.
	'''
		if len(self.model.selected_nodes) != 1:
			print('\n\tOne specific node must be selected.')
		else:
			if self.model.nodesets == 0:
				print('\n\tNo nodesets to create spider with.')
			else:
				spider_nodeset = 1
				if len(self.model.nodesets) > 0:
					spider_nodeset = max(self.model.nodesets)
				text, ok = QtWidgets.QInputDialog.getText(self, 'Create Spider from Nodeset', 'Nodeset number:', text=str(spider_nodeset))
				if ok and str(text).isdigit():
					nodeset = int(text)
					if nodeset not in self.model.nodesets:
						print('\n\tNodeset', nodeset, 'does not exist.')
					else:
						if self.viewer.currentMesh == 'None':
							print('\n\tNo mesh currently selected.')
						else:
							mesh = self.model.meshes[self.viewer.currentMesh]
							node1 = list(self.model.selected_nodes.keys())[0]
							print('\n\tCreating spider from nodeset', nodeset, 'and node', node1)
							if 'unobtanium' not in self.model.materials:
								self.model.materials['unobtanium'] = {'Elasticity': 42e12,
																	  'Poisson ratio': 0.35,
																	  'Density': 69e-15}
							if 'unobtanium' not in self.model.sections:
								self.model.sections['unobtanium'] = {'Number': len(self.model.sections),
																	 'Area (Rod or Beam)': 1.,
																	 'Izz (Beam)': 0.08333333333333333,
																	 'Iyy (Beam 3D)': 0.08333333333333333,
																	 'Material': 'unobtanium'}
							for node in self.model.nodesets[int(text)]:
								elm_num = 1
								if len(mesh.elements) != 0:
									elm_num = max(mesh.elements)+1
								mesh.elements[elm_num] = Element(elm_num,'unobtanium',[mesh.nodes[node1],mesh.nodes[node]])
								mesh.elements[elm_num].type = 'BEAM2N'

							self.model.selected_nodes.clear()
							self.model.nodesSelected = False

							x_max = max(mesh.nodes[i].coord[0][0] for i in mesh.nodes )
							x_min = min(mesh.nodes[i].coord[0][0] for i in mesh.nodes )
							y_max = max(mesh.nodes[i].coord[1][0] for i in mesh.nodes )
							y_min = min(mesh.nodes[i].coord[1][0] for i in mesh.nodes )
							z_max = max(mesh.nodes[i].coord[2][0] for i in mesh.nodes )
							z_min = min(mesh.nodes[i].coord[2][0] for i in mesh.nodes )
							mesh.viewScope = {'max': [x_max, y_max, z_max], 'min': [x_min, y_min, z_min]}
							mesh.viewRadius = 1.25*max( (x_max-x_min)/2., (y_max-y_min)/2., (z_max-z_min)/2. )					
							self.model.buildDisplayList(mesh)
							self.new_mesh_view = {'Mesh': self.viewer.currentMesh}
							self.viewer.update()


	def applyTouchLockConstraint(self):
		'''
	Apply nodelock constraints between two different
	nodesets, locking nodes that are within a specified
	perimiter from each other.
	'''
		if len(self.model.meshes) != 0:
			if len(self.model.nodesets) > 1:
				newConstraint = {}
				constnum = 1
				for mesh in self.model.meshes:
					for solution in self.model.meshes[mesh].solutions:
						for constraint in self.model.meshes[mesh].solutions[solution]['Constraints']:
							if constraint[:10] == 'touchlock-':
								if constraint[10:].isdigit():
									if int(constraint[10:])+1 > constnum:
										constnum = int(constraint[10:])+1
				newConstraint['inputs'] = {'Name': 'touchlock-'+str(constnum),
										   'Nodeset1': str(sorted(self.model.nodesets.keys())[-2]),
										   'Nodeset2': str(sorted(self.model.nodesets.keys())[-1]),
										   'Tolerance': '0.1',
										   'DOFs': '1, 2, 3, 4, 5, 6'}
				newConstraint['choices'] = [ ['Mesh', 'Solution'], {} ]
				newConstraint['current'] = {'Mesh': None, 'Solution': None}
				noSolutions = True
				for mesh in	self.model.meshes:
					if len(self.model.meshes[mesh].solutions) != 0:
						noSolutions = False
						newConstraint['choices'][1][mesh] = []
						newConstraint['current']['Mesh'] = mesh
						for solution in self.model.meshes[mesh].solutions:
							newConstraint['choices'][1][mesh].append(solution)
							newConstraint['current']['Solution'] = solution
				if noSolutions:
					print('\n\tNo solutions to select from.')
				else:
					newConstraint['inOrder'] = ['Name', 'Mesh', 'Solution', 'Nodeset1', 'Nodeset2', 'Tolerance', 'DOFs']
					self.new_constraint = {'Type': 'TouchLock'}
					self.selectionWidget = InputDialog(newConstraint, 'New TouchLock Constraint', self.new_constraint)
					self.selectionWidget.window_closed.connect(self.viewer.update)
					self.selectionWidget.show()
			else:
				print('\n\tNot enough nodesets to apply constraints to.')
		else:
			print('\n\tNo meshes to select.')


	def applyNodeLockConstraint(self):
		'''
	Apply nodelock constraints between one node and
	all the nodes in a specified nodeset.
	'''
		if len(self.model.meshes) != 0:
			if len(self.model.nodesets) > 1:
				newConstraint = {}
				constnum = 1
				for mesh in self.model.meshes:
					for solution in self.model.meshes[mesh].solutions:
						for constraint in self.model.meshes[mesh].solutions[solution]['Constraints']:
							if constraint[:9] == 'nodelock-':
								if constraint[9:].isdigit():
									if int(constraint[9:])+1 > constnum:
										constnum = int(constraint[9:])+1
				newConstraint['inputs'] = {'Name': 'nodelock-'+str(constnum),
										   'Nodeset1': str(sorted(self.model.nodesets.keys())[-2]),
										   'Nodeset2': str(sorted(self.model.nodesets.keys())[-1]),
										   'DOFs': '1, 2, 3, 4, 5, 6'}
				newConstraint['choices'] = [ ['Mesh', 'Solution'], {} ]
				newConstraint['current'] = {'Mesh': None, 'Solution': None}
				noSolutions = True
				for mesh in	self.model.meshes:
					if len(self.model.meshes[mesh].solutions) != 0:
						noSolutions = False
						newConstraint['choices'][1][mesh] = []
						newConstraint['current']['Mesh'] = mesh
						for solution in self.model.meshes[mesh].solutions:
							newConstraint['choices'][1][mesh].append(solution)
							newConstraint['current']['Solution'] = solution
				if noSolutions:
					print('\n\tNo solutions to select from.')
				else:
					newConstraint['inOrder'] = ['Name', 'Mesh', 'Solution', 'Nodeset1', 'Nodeset2', 'DOFs']
					self.new_constraint = {'Type': 'NodeLock'}
					self.selectionWidget = InputDialog(newConstraint, 'New NodeLock Constraint', self.new_constraint)
					self.selectionWidget.window_closed.connect(self.viewer.update)
					self.selectionWidget.show()
			else:
				print('\n\tNot enough nodesets to apply constraints to.')
		else:
			print('\n\tNo meshes to select.')


	def applyDisplacement(self):
		'''
	Apply displacement boundary condition to solution
	by selecting mesh and solution, and writing in
	boundary condition properties in dialog box.
	'''
		if len(self.model.meshes) != 0:
			if len(self.model.nodesets) != 0:
				newDisplacement = {}
				boundnum = 1
				for mesh in self.model.meshes:
					for solution in self.model.meshes[mesh].solutions:
						for boundary in self.model.meshes[mesh].solutions[solution]['Boundaries']:
							if boundary[:9] == 'boundary-':
								if boundary[9:].isdigit():
									if int(boundary[9:])+1 > boundnum:
										boundnum = int(boundary[9:])+1
				newDisplacement['inputs'] = {'Name': 'boundary-'+str(boundnum),
											 'Nodeset': str(max(self.model.nodesets.keys())),
											 'Displacement': '0.',
											 'DOFs': '1, 2, 3, 4, 5, 6'}
				newDisplacement['choices'] = [ ['Mesh', 'Solution'], {} ]
				newDisplacement['current'] = {'Mesh': None, 'Solution': None}
				noSolutions = True
				for mesh in	self.model.meshes:
					if len(self.model.meshes[mesh].solutions) != 0:
						noSolutions = False
						newDisplacement['choices'][1][mesh] = []
						newDisplacement['current']['Mesh'] = mesh
						for solution in self.model.meshes[mesh].solutions:
							newDisplacement['choices'][1][mesh].append(solution)
							newDisplacement['current']['Solution'] = solution
				if noSolutions:
					print('\n\tNo solutions to select from.')
				else:
					newDisplacement['inOrder'] = ['Name', 'Mesh', 'Solution', 'Nodeset', 'Displacement', 'DOFs']
					self.new_boundary = {'Type': 'Displacement'}
					self.selectionWidget = InputDialog(newDisplacement, 'New Boundary Displacement', self.new_boundary)
					self.selectionWidget.window_closed.connect(self.viewer.update)
					self.selectionWidget.show()
			else:
				print('\n\tNo nodesets to apply displacement to.')
		else:
			print('\n\tNo meshes to select.')
		

	def applyUniformLoad(self):
		'''
	Apply uniform load to solution by selecting mesh 
	and solution, and writing in load properties in 
	dialog box.
	'''
		if len(self.model.meshes) != 0:
			if len(self.model.nodesets) != 0:
				newLoad = {}
				loadnum = 1
				for mesh in self.model.meshes:
					for solution in self.model.meshes[mesh].solutions:
						for load in self.model.meshes[mesh].solutions[solution]['Loads']:
							if load[:11] == 'force_load-':
								if load[11:].isdigit():
									if int(load[11:])+1 > loadnum:
										loadnum = int(load[11:])+1
				newLoad['inputs'] = {'Name': 'force_load-'+str(loadnum),
									 'Nodeset': str(max(self.model.nodesets.keys())),
									 'Force': '0.',
									 'x-vector': '0.',
									 'y-vector': '1.',
									 'z-vector': '0.'}
				newLoad['choices'] = [ ['Mesh', 'Solution'], {} ]
				newLoad['current'] = {'Mesh': None, 'Solution': None}
				noSolutions = True
				for mesh in	self.model.meshes:
					if len(self.model.meshes[mesh].solutions) != 0:
						noSolutions = False
						newLoad['choices'][1][mesh] = []
						newLoad['current']['Mesh'] = mesh
						for solution in self.model.meshes[mesh].solutions:
							newLoad['choices'][1][mesh].append(solution)
							newLoad['current']['Solution'] = solution
				if noSolutions:
					print('\n\tNo solutions to select from.')
				else:
					newLoad['inOrder'] = ['Name', 'Mesh', 'Solution', 'Nodeset',
										  'Force', 'x-vector', 'y-vector', 'z-vector']
					self.new_load = {'Type': 'Force'}
					self.selectionWidget = InputDialog(newLoad, 'New Uniform Load', self.new_load)
					self.selectionWidget.window_closed.connect(self.viewer.update)
					self.selectionWidget.show()
			else:
				print('\n\tNo nodesets to apply load to.')
		else:
			print('\n\tNo meshes to select.')


	def applyConcentratedLoad(self):
		'''
	Apply concentrated load to solution by selecting
	mesh and solution, and writing in load properties
	in dialog box.
	'''
		if len(self.model.meshes) != 0:
			if len(self.model.nodesets) != 0:
				newLoad = {}
				loadnum = 1
				for mesh in self.model.meshes:
					for solution in self.model.meshes[mesh].solutions:
						for load in self.model.meshes[mesh].solutions[solution]['Loads']:
							if load[:11] == 'force_load-':
								if load[11:].isdigit():
									if int(load[11:])+1 > loadnum:
										loadnum = int(load[11:])+1
				newLoad['inputs'] = {'Name': 'force_load-'+str(loadnum),
									 'Nodeset': str(max(self.model.nodesets.keys())),
									 'Force': '0.',
									 'x-vector': '0.',
									 'y-vector': '1.',
									 'z-vector': '0.'}
				newLoad['choices'] = [ ['Mesh', 'Solution'], {} ]
				newLoad['current'] = {'Mesh': None, 'Solution': None}
				noSolutions = True
				for mesh in	self.model.meshes:
					if len(self.model.meshes[mesh].solutions) != 0:
						noSolutions = False
						newLoad['choices'][1][mesh] = []
						newLoad['current']['Mesh'] = mesh
						for solution in self.model.meshes[mesh].solutions:
							newLoad['choices'][1][mesh].append(solution)
							newLoad['current']['Solution'] = solution
				if noSolutions:
					print('\n\tNo solutions to select from.')
				else:
					newLoad['inOrder'] = ['Name', 'Mesh', 'Solution', 'Nodeset',
										  'Force', 'x-vector', 'y-vector', 'z-vector']
					self.new_load = {'Type': 'ForceConcentrated'}
					self.selectionWidget = InputDialog(newLoad, 'New Concentrated Load', self.new_load)
					self.selectionWidget.window_closed.connect(self.viewer.update)
					self.selectionWidget.show()
			else:
				print('\n\tNo nodesets to apply load to.')
		else:
			print('\n\tNo meshes to select.')


	def applyDistributedLoad(self):
		'''
	Apply distributed load to solution by selecting
	mesh and solution, and writing in load properties
	in dialog box.
	'''
		if len(self.model.meshes) != 0:
			if len(self.model.elementsets) != 0:
				newLoad = {}
				loadnum = 1
				for mesh in self.model.meshes:
					for solution in self.model.meshes[mesh].solutions:
						for load in self.model.meshes[mesh].solutions[solution]['Loads']:
							if load[:11] == 'distr_load-':
								if load[11:].isdigit():
									if int(load[11:])+1 > loadnum:
										loadnum = int(load[10:])+1
				newLoad['inputs'] = {'Name': 'distr_load-'+str(loadnum),
									 'Elementset': str(max(self.model.elementsets.keys())),
									 'Force/Length': '0.',
									 'x-vector': '0.',
									 'y-vector': '-1.',
									 'z-vector': '0.'}
				newLoad['choices'] = [ ['Mesh', 'Solution'], {} ]
				newLoad['current'] = {'Mesh': None, 'Solution': None}
				noSolutions = True
				for mesh in	self.model.meshes:
					if len(self.model.meshes[mesh].solutions) != 0:
						noSolutions = False
						newLoad['choices'][1][mesh] = []
						newLoad['current']['Mesh'] = mesh
						for solution in self.model.meshes[mesh].solutions:
							newLoad['choices'][1][mesh].append(solution)
							newLoad['current']['Solution'] = solution
				if noSolutions:
					print('\n\tNo solutions to select from.')
				else:
					newLoad['inOrder'] = ['Name', 'Mesh', 'Solution', 'Elementset',
										  'Force/Length', 'x-vector', 'y-vector', 'z-vector']
					self.new_load = {'Type': 'ForceDistributed'}
					self.selectionWidget = InputDialog(newLoad, 'New Distributed Load', self.new_load)
					self.selectionWidget.window_closed.connect(self.viewer.update)
					self.selectionWidget.show()
			else:
				print('\n\tNo elementsets to apply loads to.')
		else:
			print('\n\tNo meshes to select.')


	def applyTorqueLoad(self):
		'''
	Apply torqe load to specified nodeset.
	'''
		if len(self.model.meshes) != 0:
			if len(self.model.nodesets) != 0:
				newLoad = {}
				loadnum = 1
				for mesh in self.model.meshes:
					for solution in self.model.meshes[mesh].solutions:
						for load in self.model.meshes[mesh].solutions[solution]['Loads']:
							if load[:12] == 'torque_load-':
								if load[12:].isdigit():
									if int(load[12:])+1 > loadnum:
										loadnum = int(load[12:])+1
				newLoad['inputs'] = {'Name': 'torque_load-'+str(loadnum),
									 'Nodeset': str(max(self.model.nodesets.keys())),
									 'Torque': '0.',
									 'mx-vector': '0.',
									 'my-vector': '0.',
									 'mz-vector': '1.'}
				newLoad['choices'] = [ ['Mesh', 'Solution'], {} ]
				newLoad['current'] = {'Mesh': None, 'Solution': None}
				noSolutions = True
				for mesh in	self.model.meshes:
					if len(self.model.meshes[mesh].solutions) != 0:
						noSolutions = False
						newLoad['choices'][1][mesh] = []
						newLoad['current']['Mesh'] = mesh
						for solution in self.model.meshes[mesh].solutions:
							newLoad['choices'][1][mesh].append(solution)
							newLoad['current']['Solution'] = solution
				if noSolutions:
					print('\n\tNo solutions to select from.')
				else:
					newLoad['inOrder'] = ['Name', 'Mesh', 'Solution', 'Nodeset',
										  'Torque', 'mx-vector', 'my-vector', 'mz-vector']
					self.new_load = {'Type': 'Torque'}
					self.selectionWidget = InputDialog(newLoad, 'New Torque Load', self.new_load)
					self.selectionWidget.window_closed.connect(self.viewer.update)
					self.selectionWidget.show()
			else:
				print('\n\tNo nodesets to apply load to.')
		else:
			print('\n\tNo meshes to select.')


	def applyGravityLoad(self):
		'''
	Apply gravity load to all elements in
	specified elementset.
	'''
		if len(self.model.meshes) != 0:
			if len(self.model.elementsets) != 0:
				newLoad = {}
				loadnum = 1
				for mesh in self.model.meshes:
					for solution in self.model.meshes[mesh].solutions:
						for load in self.model.meshes[mesh].solutions[solution]['Loads']:
							if load[:10] == 'grav_load-':
								if load[10:].isdigit():
									if int(load[10:])+1 > loadnum:
										loadnum = int(load[10:])+1
				newLoad['inputs'] = {'Name': 'grav_load-'+str(loadnum),
									 'Elementset': str(max(self.model.elementsets.keys())),
									 'Acceleration': '9.81',
									 'x-vector': '0.',
									 'y-vector': '-1.',
									 'z-vector': '0.'}
				newLoad['choices'] = [ ['Mesh', 'Solution'], {} ]
				newLoad['current'] = {'Mesh': None, 'Solution': None}
				noSolutions = True
				for mesh in	self.model.meshes:
					if len(self.model.meshes[mesh].solutions) != 0:
						noSolutions = False
						newLoad['choices'][1][mesh] = []
						newLoad['current']['Mesh'] = mesh
						for solution in self.model.meshes[mesh].solutions:
							newLoad['choices'][1][mesh].append(solution)
							newLoad['current']['Solution'] = solution
				if noSolutions:
					print('\n\tNo solutions to select from.')
				else:
					newLoad['inOrder'] = ['Name', 'Mesh', 'Solution', 'Elementset',
										  'Acceleration', 'x-vector', 'y-vector', 'z-vector']
					self.new_load = {'Type': 'Gravity'}
					self.selectionWidget = InputDialog(newLoad, 'New Gravity Load', self.new_load)
					self.selectionWidget.window_closed.connect(self.viewer.update)
					self.selectionWidget.show()
			else:
				print('\n\tNo elementsets to apply loads to.')
		else:
			print('\n\tNo meshes to select.')


	def applyDynamicLoad(self):
		'''
	Apply dynamic load to specified
	nodeset with force or acceleration
	scale factor.
	'''
		if len(self.model.meshes) != 0:
			if len(self.model.nodesets) != 0:
				newLoad = {}
				loadnum = 1
				for mesh in self.model.meshes:
					for solution in self.model.meshes[mesh].solutions:
						for load in self.model.meshes[mesh].solutions[solution]['Loads']:
							if load[:13] == 'dynamic_load-':
								if load[13:].isdigit():
									if int(load[13:])+1 > loadnum:
										loadnum = int(load[13:])+1
				newLoad['inputs'] = {'Name': 'dynamic_load-'+str(loadnum),
									 'Nodeset': str(max(self.model.nodesets.keys())),
									 'Force/Acceleration': '9.81',
									 'x-vector': '0.',
									 'y-vector': '1.',
									 'z-vector': '0.'}
				newLoad['choices'] = [ ['Mesh', 'Solution', 'Load Type'], {} ]
				newLoad['current'] = {'Mesh': None, 'Solution': None, 'Load Type': None}
				noSolutions = True
				for mesh in	self.model.meshes:
					if len(self.model.meshes[mesh].solutions) != 0:
						noSolutions = False
						newLoad['choices'][1][mesh] = {}
						newLoad['current']['Mesh'] = mesh
						for solution in self.model.meshes[mesh].solutions:
							newLoad['choices'][1][mesh][solution] = []
							newLoad['current']['Solution'] = solution
							newLoad['choices'][1][mesh][solution].append('Acceleration')
							newLoad['choices'][1][mesh][solution].append('ForceDynamic')
							newLoad['current']['Load Type'] = 'Base Acceleration'
							
				if noSolutions:
					print('\n\tNo solutions to select from.')
				else:
					newLoad['inOrder'] = ['Name', 'Mesh', 'Solution', 'Load Type', 'Nodeset',
										  'Force/Acceleration', 'x-vector', 'y-vector', 'z-vector']
					self.new_load = {'Type': 'Dynamic'}
					self.selectionWidget = InputDialog(newLoad, 'New Dynamic Load', self.new_load)
					self.selectionWidget.window_closed.connect(self.viewer.update)
					self.selectionWidget.show()
			else:
				print('\n\tNo nodesets to apply loads to.')
		else:
			print('\n\tNo meshes to select.')


	def highlightNode(self):
		'''
	Take node number from user in dialog box
	and highlight that node in viewer.
	'''
		text, ok = QtWidgets.QInputDialog.getText(self, 'Highlight Node(s)', 'Node number:')
		if ok:
			if str(text).isdigit():
				if int(text) in self.viewer.currentDisplayList['mesh'].nodes:
					self.model.nodesSelected = True
					self.model.elementsSelected = False
					if len(self.model.selected_nodes) != 0:
						self.model.selected_nodes.clear()
					self.model.selected_nodes[int(text)] = self.viewer.currentDisplayList['mesh'].nodes[int(text)]
					print('\n\tNode number:', int(text))
					print('\tCoord:', str(self.model.meshes[self.viewer.currentMesh].nodes[int(text)].coord[0][0]) \
										+', '+str(self.model.meshes[self.viewer.currentMesh].nodes[int(text)].coord[1][0]) \
										+', '+str(self.model.meshes[self.viewer.currentMesh].nodes[int(text)].coord[2][0]))
				else:
					print('\n\tNo node with that number ('+str(text)+') in current mesh.')
			else:
				print('\n\tThat is not an acceptable node number.')


	def highlightElement(self):
		'''
	Take element number from user in dialog box
	and highlight that element in viewer.
	'''
		text, ok = QtWidgets.QInputDialog.getText(self, 'Highlight Element(s)', 'Element number:')
		if ok:
			if str(text).isdigit():
				if int(text) in self.viewer.currentDisplayList['mesh'].elements:
					self.model.nodesSelected = False
					self.model.elementsSelected = True
					if len(self.model.selected_nodes) != 0:
						self.model.selected_nodes.clear()
					if len(self.model.selected_elements) != 0:
						self.model.selected_elements.clear()
					self.model.selected_elements[int(text)] = self.viewer.currentDisplayList['mesh'].elements[int(text)]
					for node in self.model.selected_elements[int(text)].nodes:
						self.model.selected_nodes[node.number] = self.viewer.currentDisplayList['mesh'].nodes[node.number]
					self.model.selectedElementsDisplay(self.viewer.currentDisplayList['mesh'])
					print('\n\tElement number:', int(text), '\n\tNodes:', end=' ')
					for node in self.model.selected_elements[int(text)].nodes:
						print(node.number,end=' ')
					print()
				else:
					print('\n\tNo element with that number ('+str(text)+') in current mesh.')
			else:
				print('\n\tThat is not an acceptable element number.')


	def highlightNodeSet(self):
		'''
	Take nodeset number from user in dialog box
	and highlight that nodeset in viewer.
	'''
		text, ok = QtWidgets.QInputDialog.getText(self, 'Highlight Nodeset', 'Nodeset number:')
		if ok:
			if str(text).isdigit():
				if int(text) in self.model.nodesets:
					nodesInCurrentMesh = True
					for node in self.model.nodesets[int(text)]:
						if node not in self.viewer.currentDisplayList['mesh'].nodes:
							nodesInCurrentMesh = False
					if nodesInCurrentMesh:
						self.model.nodesSelected = True
						self.model.elementsSelected = False
						if len(self.model.selected_nodes) != 0:
							self.model.selected_nodes.clear()
						for node in self.model.nodesets[int(text)]:
							self.model.selected_nodes[node] = self.model.nodesets[int(text)][node]
						print('\n\tNodeset '+str(text)+':')
						toprint = self.model.selected_nodes.keys()
						toprint = sorted(toprint)
						if len(toprint) > 8:
							print('\t[',end=' ') 
							for i in range(4):
								print(str(toprint[i])+',',end=' ')
							print('...',end=' ')
							print(str(toprint[-3])+',',end=' ')
							print(str(toprint[-2])+',',end=' ')
							print(str(toprint[-1])+' ]')
						else:
							print('\t'+str(toprint))
					else:
						print('\n\tThere are nodes in the selected nodeset ('+text+') that are not in the current mesh')
				else:
					print('\n\tNodeset', int(text), 'does not exist')
			else:
				print('\n\t', text, 'is not an acceptable nodeset number.')


	def highlightElementSet(self):
		'''
	Take elementset number from user in dialog box
	and highlight that elementset in viewer.
	'''
		text, ok = QtWidgets.QInputDialog.getText(self, 'Highlight Elementset', 'Elementset number:')
		if ok:
			if str(text).isdigit():
				if int(text) in self.model.elementsets:
					elementsInCurrentMesh = True
					for element in self.model.elementsets[int(text)]:
						if element not in self.viewer.currentDisplayList['mesh'].elements:
							elementsInCurrentMesh = False
					if elementsInCurrentMesh:
						self.model.nodesSelected = False
						self.model.elementsSelected = True
						if len(self.model.selected_nodes) != 0:
							self.model.selected_nodes.clear()
						if len(self.model.selected_elements) != 0:
							self.model.selected_elements.clear()
						for elm in self.model.elementsets[int(text)]:
							self.model.selected_elements[elm] = self.model.elementsets[int(text)][elm]
							for node in self.model.selected_elements[elm].nodes:
								if node.number in self.viewer.currentDisplayList['mesh'].nodes:
									self.model.selected_nodes[node.number] = self.viewer.currentDisplayList['mesh'].nodes[node.number]
						self.model.selectedElementsDisplay(self.viewer.currentDisplayList['mesh'])
						print('\n\tElementset '+str(text)+':')
						toprint = self.model.selected_elements.keys()
						toprint = sorted(toprint)
						if len(toprint) > 8:
							print('\t[',end=' ')
							for i in range(4):
								print(str(toprint[i])+',',end=' ')
							print('...',end=' ')
							print(str(toprint[-3])+',',end=' ')
							print(str(toprint[-2])+',',end=' ')
							print(str(toprint[-1])+' ]')
						else:
							print('\t'+str(toprint))
					else:
						print('\n\tThere are elements in the selected elementset ('+text+') that are not in the current mesh')
				else:
					print('\n\tElementset', int(text), 'does not exist')
			else:
				print('\n\t', text, 'is not an acceptable elementset number.')
				

	def updateDisplayList(self,view_geometry,view_mesh,view_results):
		if view_geometry:
			self.viewer.currentDisplayList['view radius'] = 2
			self.viewer.currentDisplayList['view scope'] = { 'max': [ 1., 1., 1.],
													  		 'min': [-1.,-1.,-1.] }
			self.viewer.currentDisplayList['displaylist'] = { 'nodes':		 None,
															  'wireframe':	 None,
															  'shaded':		 None,
															  'average':	 None,
															  'orientation': self.viewer.currentDisplayList['displaylist']['orientation']}

		elif view_results:
			if self.current_results['Solution'] == 'None':
				pass
			else:
				solution = self.current_results['Solution']
				result = self.current_results['Result']
				subresult = self.current_results['Subresult']
				self.viewer.currentDisplayList['solution'] = solution
				self.viewer.currentDisplayList['result'] = result
				self.viewer.currentDisplayList['subresult'] = subresult
				newResult = 'None'
				for newResults in self.model.results:
					for mesh in self.model.results[newResults].meshes:
						if self.viewer.currentDisplayList['solution'] in self.model.results[newResults].meshes[mesh].solutions:
							self.viewer.currentDisplayList['mesh'] = self.model.results[newResults].meshes[mesh]
							newResult = newResults
							break
				if 'info' in self.model.displayLists[solution][result][subresult]:
					self.viewer.currentDisplayList['info'] = self.model.displayLists[solution][result][subresult]['info']
				else:
					self.viewer.currentDisplayList['info'] = 'None'
				if 'avg_info' in self.model.displayLists[solution][result][subresult]:
					self.viewer.currentDisplayList['avg_info'] = self.model.displayLists[solution][result][subresult]['avg_info']
				else:
					self.viewer.currentDisplayList['avg_info'] = 'None'
				self.viewer.currentDisplayList['view radius'] = self.viewer.currentDisplayList['mesh'].viewRadius
				self.viewer.currentDisplayList['view scope'] = self.viewer.currentDisplayList['mesh'].viewScope
				if self.model.results[newResult].solutions[solution].type in ['Eigenmodes', 'ModalDynamic']:
					pass
				else:
					self.viewer.currentDisplayList['max_val'] = self.model.displayLists[solution][result][subresult]['max_val']
					self.viewer.currentDisplayList['min_val'] = self.model.displayLists[solution][result][subresult]['min_val']
					if 'avg_max_val' in self.model.displayLists[solution][result][subresult]:
						self.viewer.currentDisplayList['avg_max_val'] = self.model.displayLists[solution][result][subresult]['avg_max_val']
						self.viewer.currentDisplayList['avg_min_val'] = self.model.displayLists[solution][result][subresult]['avg_min_val']
					else:
						self.viewer.currentDisplayList['avg_max_val'] = None
						self.viewer.currentDisplayList['avg_min_val'] = None
					self.viewer.currentDisplayList['displaylist'] = { 'nodes':		 self.model.displayLists[solution][result][subresult]['nodes'],
																	  'wireframe':	 self.model.displayLists[solution][result][subresult]['wireframe'],
																	  'shaded':		 self.model.displayLists[solution][result][subresult]['shaded'],
																	  'orientation': self.viewer.currentDisplayList['displaylist']['orientation']}
					if 'average' in self.model.displayLists[solution][result][subresult]:
						self.viewer.currentDisplayList['displaylist']['average'] = self.model.displayLists[solution][result][subresult]['average']
					else:
						self.viewer.currentDisplayList['displaylist']['average'] = None
				
		elif view_mesh:
			if self.viewer.currentDisplayList['mesh'] != None:
				self.viewer.currentDisplayList['max_val'] = None
				self.viewer.currentDisplayList['min_val'] = None
				self.viewer.currentDisplayList['avg_max_val'] = None
				self.viewer.currentDisplayList['avg_min_val'] = None
				self.viewer.viewAverage = False
				self.viewer.currentDisplayList['view radius'] = self.viewer.currentDisplayList['mesh'].viewRadius
				self.viewer.currentDisplayList['view scope'] = self.viewer.currentDisplayList['mesh'].viewScope
				self.viewer.currentDisplayList['displaylist'] = {'nodes': 	    self.viewer.currentDisplayList['mesh'].displayLists['nodes'],
																 'wireframe':   self.viewer.currentDisplayList['mesh'].displayLists['wireframe'],
																 'shaded':	    self.viewer.currentDisplayList['mesh'].displayLists['shaded'],
																 'average':	    None,
																 'orientation': self.viewer.currentDisplayList['displaylist']['orientation']}

		else:
			pass
		self.viewer.camera.setSceneRadius( self.viewer.currentDisplayList['view radius'] )


	def nodesView(self):
		if self.viewer.viewNodes == True:
			self.viewer.viewNodes = False
		else:
			self.viewer.viewNodes = True
		self.viewer.update()

	def wireframeView(self):
		self.viewer.viewShaded = False
		self.viewer.viewWireframe = True
		self.viewer.update()

	def shadedView(self):
		self.viewer.viewShaded = True
		self.viewer.viewWireframe = False
		self.viewer.update()

	def centerModel(self):
		if self.viewer.modelCentered == True:
			self.viewer.modelCentered = False
			self.viewer.coordSys0_centered = self.viewer.coordSys0
		else:
			self.viewer.modelCentered = True
			self.viewer.coordSys0_centered = CoordSys3D( \
					Point3D(-(self.viewer.currentDisplayList['view scope']['max'][0]+self.viewer.currentDisplayList['view scope']['min'][0])/2.,
							-(self.viewer.currentDisplayList['view scope']['max'][1]+self.viewer.currentDisplayList['view scope']['min'][1])/2.,
							-(self.viewer.currentDisplayList['view scope']['max'][2]+self.viewer.currentDisplayList['view scope']['min'][2])/2.),
					Vector3D(1.,0.,0.),Vector3D(0.,1.,0.))

	def showOrigin(self):
		'''
	Wether or not to show an RGB triad at the 
	origin (coordinates 0., 0., 0.).
	'''
		if self.viewer.viewOrigin == False:
			self.viewer.viewOrigin = True
		else:
			self.viewer.viewOrigin = False
		self.viewer.update()

	def showMeshTree(self):
		'''
	Hides or shows the Mesh Tree.
	'''
		if self.viewer.viewMeshTree == False:
			self.viewer.viewMeshTree = True
		else:
			self.viewer.viewMeshTree = False
		self.viewer.update()

	def setScaleFactor(self):
		text, ok = QtWidgets.QInputDialog.getText(self, 'New scale factor', 'Scale factor:')
		if ok:
			try:
				print('\n\tCurrent scale factor:', self.model.scale_factor)
				self.model.scale_factor = float(text)
			except ValueError:
				print('\n\tScale factor must be a float.')
			else:
				if self.viewer.currentDisplayList['mesh'] != None:
					if self.viewer.currentDisplayList['solution'] != 'None':
						solution = self.current_results['Solution']
						result = self.current_results['Result']
						subresult = self.current_results['Subresult']
						newResults = None
						for newResults in self.model.results:
							if solution in self.model.results[newResults].solutions:
								print('\tNew scale factor', self.model.scale_factor)
								self.model.buildDisplayList(self.viewer.currentDisplayList['mesh'],[solution, result, subresult])
								break
		self.viewer.viewNewResults = True
		self.viewer.update()

	def setShearBendingDiagram(self):
		text, ok = QtWidgets.QInputDialog.getText(self, 'New shear or bending diagram scale', 'Shear/Bending diagram scale:')
		if ok:
			try:
				self.model.scaleShearBendDiagram = float(text)
			except ValueError:
				print('\n\tScale factor must be a float.')
			else:
				if self.viewer.currentDisplayList['mesh'] != None:
					if self.viewer.currentDisplayList['solution'] != 'None':
						solution = self.current_results['Solution']
						result = self.current_results['Result']
						subresult = self.current_results['Subresult']
						newResults = None
						for newResults in self.model.results:
							if solution in self.model.results[newResults].solutions:
								print('\n\tShear/Bending diagrams now scaled by:', self.model.scaleShearBendDiagram)
								self.model.buildDisplayList(self.viewer.currentDisplayList['mesh'],[solution, result, subresult])
								break
		self.viewer.viewNewResults = True
		self.viewer.update()

	def viewAverage(self):
		if self.viewer.viewAverage == True:
			self.viewer.viewAverage = False
		else:
			self.viewer.viewAverage = True
		self.viewer.update()

	def previousEigenmode(self):
		if self.viewer.currentDisplayList['result'] == 'modeshapes':
			modelresults = ''
			for res in self.model.results:
				if self.viewer.currentDisplayList['solution'] in self.model.results[res].solutions:
					modelresults = res
					break
			if modelresults != '':
				n = len(self.model.results[modelresults].solutions[self.viewer.currentDisplayList['solution']].eigenfrequencies)
				m = int(self.viewer.currentDisplayList['subresult'][4:])
				if m > 1:
					self.current_results = {}
					self.current_results['Solution'] = self.viewer.currentDisplayList['solution']
					self.current_results['Result'] = self.viewer.currentDisplayList['result']
					self.current_results['Subresult'] = 'mode'+str(m-1)
					self.viewer.viewNewResults = True
					self.viewer.viewLoadingMessage = True
					self.viewer.update()
				else:
					print('\n\tMode 1 is the first eigenmode.')

	def nextEigenmode(self):
		if self.viewer.currentDisplayList['result'] == 'modeshapes':
			modelresults = ''
			for res in self.model.results:
				if self.viewer.currentDisplayList['solution'] in self.model.results[res].solutions:
					modelresults = res
					break
			if modelresults != '':
				n = len(self.model.results[modelresults].solutions[self.viewer.currentDisplayList['solution']].eigenfrequencies)
				m = int(self.viewer.currentDisplayList['subresult'][4:])
				if m < n:
					self.current_results = {}
					self.current_results['Solution'] = self.viewer.currentDisplayList['solution']
					self.current_results['Result'] = self.viewer.currentDisplayList['result']
					self.current_results['Subresult'] = 'mode'+str(m+1)
					self.viewer.viewNewResults = True
					self.viewer.viewLoadingMessage = True
					self.viewer.update()
				else:
					print('\n\tMode', n, 'is the last eigenmode available.')

	def setAnimationOnOff(self):
		if self.viewer.viewAnimate == True:
			self.viewer.viewAnimate = False
		else:
			self.viewer.viewAnimate = True
		self.viewer.update()

	def setAnimationSpeed(self):
		text, ok = QtWidgets.QInputDialog.getText(self, 'New animation speed', 'Time between frames (s):')
		if ok:
#			self.viewer.viewAnimationSpeed = float(text)
			self.viewer.viewAnimationSpeed = [float(text)+(float(text)*0.5**2)*math.sin((pi*i)/12) for i in range(7)]
			self.viewer.viewAnimationSpeed = self.viewer.viewAnimationSpeed[::-1]
			self.viewer.viewAnimationSpeed += self.viewer.viewAnimationSpeed[:0:-1]
			print('\n\tNew frame to frame time for animation:', text)

	def btnViewMeshAction(self):
		self.updateDisplayList(False,True,False)
		self.statusBar().showMessage('  MESH  ')
		self.viewer.viewMesh = True
		self.viewer.viewGeometry = self.viewer.viewBoundaries = self.viewer.viewConstraints = \
			self.viewer.viewLoads = self.viewer.viewSolutions = self.viewer.viewResults = False
#		glClearColor(0.33, 0.43, 0.33, 1.0)
#		glClearDepth(1.0)
		self.viewer.update()
		
	def btnViewConstraintAction(self):
		self.updateDisplayList(False,True,False)
		self.statusBar().showMessage('  CONSTRAINTS  ')
		self.viewer.viewConstraints = True
		self.viewer.viewGeometry = self.viewer.viewMesh = self.viewer.viewBoundaries = \
			self.viewer.viewLoads = self.viewer.viewSolutions = self.viewer.viewResults = False
		self.viewer.update()
		
	def btnViewBoundaryAction(self):
		self.updateDisplayList(False,True,False)
		self.statusBar().showMessage('  BOUNDARIES  ')
		self.viewer.viewBoundaries = True
		self.viewer.viewGeometry = self.viewer.viewMesh = self.viewer.viewConstraints = \
			self.viewer.viewLoads = self.viewer.viewSolutions = self.viewer.viewResults = False
		self.viewer.update()
		
	def btnViewLoadAction(self):
		self.updateDisplayList(False,True,False)
		self.statusBar().showMessage('  LOADS  ')
		self.viewer.viewLoads = True
		self.viewer.viewGeometry = self.viewer.viewMesh = self.viewer.viewBoundaries = \
			self.viewer.viewConstraints = self.viewer.viewSolutions = self.viewer.viewResults = False
		self.viewer.update()
		
	def btnViewSolutionAction(self):
		self.updateDisplayList(False,True,False)
		self.statusBar().showMessage('  SOLUTIONS  ')
		self.viewer.viewSolutions = True
		self.viewer.viewGeometry = self.viewer.viewMesh = self.viewer.viewBoundaries = \
			self.viewer.viewConstraints = self.viewer.viewLoads = self.viewer.viewResults = False
		self.viewer.update()
		
	def btnViewResultAction(self):
		self.updateDisplayList(False,False,True)
		self.statusBar().showMessage('  RESULTS  ')
		self.viewer.viewResults = True
		self.viewer.viewGeometry = self.viewer.viewMesh = self.viewer.viewBoundaries = \
			self.viewer.viewConstraints = self.viewer.viewLoads = self.viewer.viewSolutions = False
#		glClearColor(0.336, 0.447, 0.588, 1.0)
#		glClearDepth(1.0)
		self.viewer.update()





class Viewer(QGLWidget):
	'''
3D viewer for rendering the geometry
and mesh with or without contour plots,
animations, loads, etc.
'''
	def __init__(self, gui):
		QGLWidget.__init__(self, gui)
		self.gui = gui
		self.model = gui.model

		self.setMouseTracking(True)
		self.setMinimumSize(500, 500)
		self.width = 100
		self.height = 100

		self.currentMesh = 'None'
		self.currentSolution = 'None'
		self.currentResults = 'None'

		self.viewLoadingMessage = False
		self.viewGeometry = False
		self.viewMesh = True
		self.viewBoundaries = False
		self.viewConstraints = False
		self.viewLoads = False
		self.viewSolutions = False
		self.viewResults = False
		self.viewNewResults = False
		self.viewOrigin = False
		self.viewNodes = False
		self.viewShaded = False
		self.viewAverage = False
		self.viewWireframe = True
		self.viewMeshTree = True
		self.viewAnimate = True
		self.viewFrame = 0
		self.veiwFrameRising = True
		self.viewAnimationSpeed = [0.05+(0.005**2)*math.sin((pi*i)/12) for i in range(7)]
		self.viewAnimationSpeed = self.viewAnimationSpeed[::-1]
		self.viewAnimationSpeed += self.viewAnimationSpeed[:0:-1]

		self.activeCTRL = False
		self.activeSHIFT = False
		self.activeALT = False
		self.oldx = self.oldy = 0
		self.mouseButtonPressed = False
		self.activeSelection = False
		self.selectionRectangleStart = [0,0]
		self.selectionRectangleEnd = [0,0]

		self.currentDisplayList = { 'mesh':			None,
									'solution': 	'None',
									'result': 		'None',
									'subresult':	'None',
									'info':			'None',
									'avg_info':		'None',
									'max_val':		None,
									'min_val':		None,
									'avg_max_val':	None,
									'avg_min_val':	None,
									'view radius': 	2,
									'view scope':  	{ 'max': [ 1., 1., 1.],
													  'min': [-1.,-1.,-1.] },
									'displaylist':	{ 'orientation': None,
													  'nodes':		 None,
													  'wireframe':	 None,
													  'shaded':		 None,
													  'average':	 None } }

		self.camera = Camera()
		self.camera.setSceneRadius( self.currentDisplayList['view radius'] )
		self.camera.reset()
		self.modelCentered = False

		self.coordSys0 = CoordSys3D(Point3D(0.,0.,0.),Vector3D(1.,0.,0.),Vector3D(0.,1.,0.))
		self.coordSys0_centered = CoordSys3D(Point3D(0.,0.,0.),Vector3D(1.,0.,0.),Vector3D(0.,1.,0.))


	def paintGL(self):

		# Render all 3D objects
		glMatrixMode( GL_PROJECTION )
		glLoadIdentity()
		self.camera.transform()
		glMatrixMode( GL_MODELVIEW )
		glLoadIdentity()

		glClear( GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT )

		glDepthFunc( GL_LEQUAL )
		glEnable( GL_DEPTH_TEST )
		glEnable( GL_CULL_FACE )
		glFrontFace( GL_CCW )
		glDisable( GL_LIGHTING )
		glShadeModel( GL_SMOOTH )
		
		# for transparent shear and bending moment diagrams
		glEnable(GL_BLEND)
		glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)

		self.viewport = glGetIntegerv( GL_VIEWPORT )
		self.projection = glGetDoublev( GL_PROJECTION_MATRIX )
		self.view_matrix = glGetDoublev( GL_MODELVIEW_MATRIX )

		if len(self.gui.new_file_import) != 0:
			if self.viewLoadingMessage == False:
				self.viewLoadingMessage = True
				self.update()
			else:
				self.model.importMesh(self.gui.new_file_import['file'])
				self.viewLoadingMessage = False
				self.gui.new_file_import.clear()

		if len(self.gui.new_results_open) != 0:
			if self.viewLoadingMessage == False:
				self.viewLoadingMessage = True
				self.update()
			else:
				self.model.readResults(self.gui.new_results_open['file'])
				self.viewLoadingMessage = False
				self.gui.new_results_open.clear()

		if len(self.gui.new_model_open) != 0:
			if self.viewLoadingMessage == False:
				self.viewLoadingMessage = True
				self.update()
			else:
				self.model.loadModel(self.gui.new_model_open['file'])
				self.viewLoadingMessage = False
				self.gui.new_model_open.clear()

		if len(self.gui.new_mesh) != 0:
			self.model.createNewMesh()
			self.gui.new_mesh.clear()

		if len(self.gui.new_solfile) != 0:
			self.model.writeSolFile(self.currentMesh)
			self.gui.new_solfile.clear()

		if len(self.gui.new_mesh_view) != 0:
			self.currentDisplayList['mesh'] = self.model.meshes[self.gui.new_mesh_view['Mesh']]
			self.currentDisplayList['solution'] = 'None'
			self.currentDisplayList['result'] = 'None'
			self.currentDisplayList['subresult'] = 'None'
			self.gui.updateDisplayList(False,True,False)
			self.gui.statusBar().showMessage('  MESH  ')
			self.viewGeometry = self.viewBoundaries = self.viewConstraints = self.viewLoads = self.viewSolutions = self.viewResults = False
			self.viewMesh = True
			self.model.elementsSelected = False
			self.currentMesh = self.gui.new_mesh_view['Mesh']
			self.currentSolution = 'None'
			self.gui.new_mesh_view.clear()
			pos = deepcopy(self.camera.position)
			trg = deepcopy(self.camera.target)
			self.gui.centerModel()
			self.camera.reset()
			self.gui.centerModel()
			self.camera.position = pos
			self.camera.target = trg			
			self.update()

		if len(self.gui.new_solution_view) != 0:
			self.currentDisplayList['mesh'] = self.model.meshes[self.gui.new_solution_view['Mesh']]
			self.currentMesh = self.gui.new_solution_view['Mesh']
			self.currentDisplayList['solution'] = self.gui.new_solution_view['Solution']
			self.currentDisplayList['result'] = 'None'
			self.currentDisplayList['subresult'] = 'None'
			self.gui.updateDisplayList(False,True,False)
			self.gui.statusBar().showMessage('  SOLUTION  ')
			self.viewGeometry = self.viewBoundaries = self.viewConstraints = self.viewLoads = self.viewMesh = self.viewResults = False
			self.viewSolutions = True
			self.model.elementsSelected = False
			self.currentSolution = self.gui.new_solution_view['Solution']
			self.currentResults = 'None'
			self.gui.new_solution_view.clear()
			self.update()

		if len(self.gui.new_material) != 0:
			self.model.createMaterial()
			self.gui.new_material.clear()

		if len(self.gui.new_section) != 0:
			self.model.createSection()
			self.gui.new_section.clear()

		if len(self.gui.new_section_assignment) != 0:
			self.model.applySection()
			self.gui.new_section_assignment.clear()

		if len(self.gui.new_solution) > 2:
			self.model.createSolution()
			self.gui.new_solution.clear()

		if len(self.gui.new_boundary) > 2:
			self.model.applyBoundary()
			self.gui.new_boundary.clear()

		if len(self.gui.new_load) > 1:
			self.model.applyLoad()
			self.gui.new_load.clear()

		if len(self.gui.new_constraint) > 1:
			self.model.applyConstraint()
			self.gui.new_constraint.clear()

		if len(self.gui.new_node) > 1:
			self.model.createNewNode()
			self.gui.new_node.clear()

		if len(self.gui.new_node_movement) > 1:
			self.model.moveSelectedNodes()
			self.gui.new_node_movement.clear()

		if len(self.gui.new_deletion) > 1:
			self.model.deleteFromModel()
			self.gui.new_deletion.clear()

		if len(self.gui.new_position) > 1:
			self.model.moveElements()
			self.gui.new_position.clear()

		if len(self.gui.new_rotation) > 1:
			self.model.rotateElements()
			self.gui.new_rotation.clear()

		if len(self.gui.new_elements) > 1:
			self.model.createNewElement()
			self.gui.new_elements.clear()

		if len(self.gui.new_extrusion) > 1:
			self.model.createNewExtrusion()
			self.gui.new_extrusion.clear()

		if len(self.gui.new_conversion) != 0:
			self.model.elementConversion()
			self.gui.new_conversion.clear()
			
		if len(self.gui.new_orientation) != 0:
			self.model.elementOrientation(True)
			self.gui.new_orientation.clear()

		if self.viewNewResults == True and len(self.gui.current_results) > 0:
			solution = self.gui.current_results['Solution']
			result = self.gui.current_results['Result']
			subresult = self.gui.current_results['Subresult']
			newResults = 'None'
			for newResult in self.model.results:
				if solution in self.model.results[newResult].solutions:
					newResults = newResult
			hasNoDisplayList = False
			if solution in self.model.displayLists:
				if result in self.model.displayLists[solution]:
					if subresult in self.model.displayLists[solution][result]:
						pass
					else:
						hasNoDisplayList = True
						self.model.displayLists[solution][result][subresult] = {}
				else:
					hasNoDisplayList = True
					self.model.displayLists[solution][result] = {}
					self.model.displayLists[solution][result][subresult] = {}
			else:
				hasNoDisplayList = True
				self.model.displayLists[solution] = {}
				self.model.displayLists[solution][result] = {}
				self.model.displayLists[solution][result][subresult] = {}
			if hasNoDisplayList:
				if newResults != 'None':
					if solution in self.model.results[newResults].solutions:
						self.model.buildDisplayList(self.model.results[newResults].solutions[solution].mesh,[solution,result,subresult])
			if newResults != 'None':
				if solution in self.model.results[newResults].solutions:
					if self.model.results[newResults].solutions[solution].type == 'ModalDynamic':
						node = int(subresult.split()[1])
						sol = self.model.results[newResults].solutions[solution]
						if result == 'displacement':
							for dof in sol.displacement[node]:
								plt.plot(sol.t,sol.displacement[node][dof],label=subresult+': '+dof)
								plt.xlabel('time (s)')
						elif result == 'velocity':
							for dof in sol.velocity[node]:
								plt.plot(sol.t,sol.velocity[node][dof],label=subresult+': '+dof)
								plt.xlabel('time (s)')
						elif result == 'acceleration':
							for dof in sol.acceleration[node]:
								plt.plot(sol.t,sol.acceleration[node][dof],label=subresult+': '+dof)
								plt.xlabel('time (s)')
						elif result == 'frf_accel':
							for dof in sol.frf_accel[node]:
								plt.plot(sol.f,sol.frf_accel[node][dof]['MAGN'],label=subresult+': '+dof)
								plt.xlabel('freq (hz)')
						else:
							print ('\n\tUnknown type of result for ModalDynamic solution:', result)
						plt.ylabel(result)
						if result == 'displacement':
							plt.ylabel('displacement\n(relative to base if acceleration load)')
						plt.title('ModalDynamics: '+solution)
						plt.legend()
						plt.show()
			self.gui.updateDisplayList(False,False,True)
			self.gui.statusBar().showMessage('  RESULTS  ')
			self.viewResults = True
			self.viewGeometry = self.viewMesh = self.viewBoundaries = \
				self.viewConstraints = self.viewLoads = self.viewSolutions = False
			self.viewNewResults = False
			self.gui.shadedView()
			self.viewLoadingMessage = False
			self.update()

		if self.modelCentered:
			glTranslatef(-(self.currentDisplayList['view scope']['max'][0]+self.currentDisplayList['view scope']['min'][0])/2.,
						 -(self.currentDisplayList['view scope']['max'][1]+self.currentDisplayList['view scope']['min'][1])/2.,
						 -(self.currentDisplayList['view scope']['max'][2]+self.currentDisplayList['view scope']['min'][2])/2.)

		if self.viewOrigin == True:
			glLineWidth(5.0)
			glColor(1.0, 0.0, 0.0)
			glBegin(GL_LINES)
			glVertex(0.,0.,0.)
			glVertex(0.15*self.currentDisplayList['view radius'], 0., 0.)
			glEnd()
			glColor(0.0, 1.0, 0.0)
			glBegin(GL_LINES)
			glVertex(0.,0.,0.)
			glVertex(0.,0.15*self.currentDisplayList['view radius'], 0.)
			glEnd()
			glColor(0.0, 0.0, 1.0)
			glBegin(GL_LINES)
			glVertex(0.,0.,0.)
			glVertex(0., 0., 0.15*self.currentDisplayList['view radius'])
			glEnd()
			if self.currentMesh != 'None':
				if 'orientation' not in self.currentDisplayList['mesh'].displayLists:
					self.currentDisplayList['mesh'].displayLists['orientation'] = glGenLists(1)
					glNewList(self.currentDisplayList['mesh'].displayLists['orientation'], GL_COMPILE)
					glEndList()
				if self.currentDisplayList['displaylist']['orientation'] == None: 
					self.currentDisplayList['displaylist']['orientation'] = self.currentDisplayList['mesh'].displayLists['orientation']
				glCallList(self.currentDisplayList['mesh'].displayLists['orientation'])


		if self.viewGeometry:
			pass
			
		elif self.viewMesh:
			pass

		elif self.viewBoundaries:
			if self.currentDisplayList['mesh'] != None:
				if 'solutions' in self.currentDisplayList['mesh'].displayLists:
					if self.currentDisplayList['solution'] in self.currentDisplayList['mesh'].solutions:
						if 'boundaries' in self.currentDisplayList['mesh'].displayLists['solutions'][self.currentDisplayList['solution']]:
							if len(self.currentDisplayList['mesh'].displayLists['solutions'][self.currentDisplayList['solution']]['boundaries']) != 0:
								for boundary in self.currentDisplayList['mesh'].displayLists['solutions'][self.currentDisplayList['solution']]['boundaries']:
										glCallList(self.currentDisplayList['mesh'].displayLists['solutions'][self.currentDisplayList['solution']]['boundaries'][boundary])

		elif self.viewConstraints:
			if self.currentDisplayList['mesh'] != None:
				if 'solutions' in self.currentDisplayList['mesh'].displayLists:
					if self.currentDisplayList['solution'] in self.currentDisplayList['mesh'].solutions:
						if 'constraints' in self.currentDisplayList['mesh'].displayLists['solutions'][self.currentDisplayList['solution']]:
							if len(self.currentDisplayList['mesh'].displayLists['solutions'][self.currentDisplayList['solution']]['constraints']) != 0:
								for constraint in self.currentDisplayList['mesh'].displayLists['solutions'][self.currentDisplayList['solution']]['constraints']:
										glCallList(self.currentDisplayList['mesh'].displayLists['solutions'][self.currentDisplayList['solution']]['constraints'][constraint])
	
		elif self.viewLoads:
			if self.currentDisplayList['mesh'] != None:
				if 'solutions' in self.currentDisplayList['mesh'].displayLists:
					if self.currentDisplayList['solution'] in self.currentDisplayList['mesh'].solutions:
						if 'loads' in self.currentDisplayList['mesh'].displayLists['solutions'][self.currentDisplayList['solution']]:
							if len(self.currentDisplayList['mesh'].displayLists['solutions'][self.currentDisplayList['solution']]['loads']) != 0:
								for load in self.currentDisplayList['mesh'].displayLists['solutions'][self.currentDisplayList['solution']]['loads']:
										glCallList(self.currentDisplayList['mesh'].displayLists['solutions'][self.currentDisplayList['solution']]['loads'][load])

		elif self.viewSolutions:
			if self.currentDisplayList['mesh'] != None:
				if 'solutions' in self.currentDisplayList['mesh'].displayLists:
					if self.currentDisplayList['solution'] in self.currentDisplayList['mesh'].solutions:
						if 'boundaries' in self.currentDisplayList['mesh'].displayLists['solutions'][self.currentDisplayList['solution']]:
							if len(self.currentDisplayList['mesh'].displayLists['solutions'][self.currentDisplayList['solution']]['boundaries']) != 0:
								for boundary in self.currentDisplayList['mesh'].displayLists['solutions'][self.currentDisplayList['solution']]['boundaries']:
										glCallList(self.currentDisplayList['mesh'].displayLists['solutions'][self.currentDisplayList['solution']] \
																																['boundaries'][boundary])
							if len(self.currentDisplayList['mesh'].displayLists['solutions'][self.currentDisplayList['solution']]['constraints']) != 0:
								for constraint in self.currentDisplayList['mesh'].displayLists['solutions'][self.currentDisplayList['solution']]['constraints']:
										glCallList(self.currentDisplayList['mesh'].displayLists['solutions'][self.currentDisplayList['solution']] \
																																['constraints'][constraint])
							if len(self.currentDisplayList['mesh'].displayLists['solutions'][self.currentDisplayList['solution']]['loads']) != 0:
								for load in self.currentDisplayList['mesh'].displayLists['solutions'][self.currentDisplayList['solution']]['loads']:
										glCallList(self.currentDisplayList['mesh'].displayLists['solutions'][self.currentDisplayList['solution']]['loads'][load])

		elif self.viewResults:
			pass

		else:
			pass

		if self.viewNodes:
			if self.currentDisplayList['result'] == 'modeshapes' and self.viewResults:
				glCallList(self.model.displayLists[self.currentDisplayList['solution']] \
								[self.currentDisplayList['result']][self.currentDisplayList['subresult']][self.viewFrame]['nodes'])
			elif self.currentDisplayList['displaylist']['nodes'] != None:
				glCallList(self.currentDisplayList['displaylist']['nodes'])
			else:
				pass

		if self.viewShaded:
			if self.currentDisplayList['result'] == 'modeshapes' and self.viewResults:
				glCallList(self.model.displayLists[self.currentDisplayList['solution']] \
								[self.currentDisplayList['result']][self.currentDisplayList['subresult']][self.viewFrame]['wireframe'])
				glCallList(self.model.displayLists[self.currentDisplayList['solution']] \
								[self.currentDisplayList['result']][self.currentDisplayList['subresult']][self.viewFrame]['shaded'])
			else:
				if self.currentDisplayList['displaylist']['wireframe'] != None:
					glCallList(self.currentDisplayList['displaylist']['wireframe'])
				if self.currentDisplayList['displaylist']['average'] != None and self.viewAverage:
					glCallList(self.currentDisplayList['displaylist']['average'])
				else:
					if self.currentDisplayList['displaylist']['shaded'] != None:
						glCallList(self.currentDisplayList['displaylist']['shaded'])
		elif self.viewWireframe:
			if self.currentDisplayList['result'] == 'modeshapes' and self.viewResults:
				glCallList(self.model.displayLists[self.currentDisplayList['solution']] \
								[self.currentDisplayList['result']][self.currentDisplayList['subresult']][self.viewFrame]['wireframe'])
			else:
				if self.currentDisplayList['displaylist']['wireframe'] != None:
					glCallList(self.currentDisplayList['displaylist']['wireframe'])
		else:
			pass

		if self.model.nodesSelected:
			glPointSize(10.0)
			glBegin(GL_POINTS)
			glColor3f(1.0, 0.0, 0.0)
			for point in self.model.selected_nodes:
				glVertex3f(self.currentDisplayList['mesh'].nodes[point].coord[0][0],
						   self.currentDisplayList['mesh'].nodes[point].coord[1][0],
						   self.currentDisplayList['mesh'].nodes[point].coord[2][0])
			glEnd()

		elif self.model.elementsSelected:
			if len(self.model.meshes) > 0:
				glCallList(self.currentDisplayList['mesh'].displayLists['selected elements'])
			else:
				self.model.selected_elements.clear()
				self.model.elementsSelected = False

		else:
			pass

		# Draw RGB triad in left corner
		glViewport(0, 0, self.width//3, self.height//3)
		if self.modelCentered:
			glTranslatef((self.currentDisplayList['view scope']['max'][0]+self.currentDisplayList['view scope']['min'][0])/2.,
						 (self.currentDisplayList['view scope']['max'][1]+self.currentDisplayList['view scope']['min'][1])/2.,
						 (self.currentDisplayList['view scope']['max'][2]+self.currentDisplayList['view scope']['min'][2])/2.)

		view_length = -(self.camera.position - self.camera.target).length()

		glLineWidth(5.0)
		glColor(1.0, 0.0, 0.0)
		# X-dir
		glBegin(GL_LINES)
		glVertex( self.camera.target.x(), self.camera.target.y(), self.camera.target.z())
		glVertex( self.camera.target.x() - 1.*view_length*0.2, self.camera.target.y(), self.camera.target.z())
		glEnd()
		glColor(0.0, 1.0, 0.0)
		# Y-dir
		glBegin(GL_LINES)
		glVertex( self.camera.target.x(), self.camera.target.y(), self.camera.target.z())
		glVertex( self.camera.target.x(), self.camera.target.y() - 1.*view_length*0.2, self.camera.target.z())
		glEnd()
		glColor(0.0, 0.0, 1.0)
		# Z-dir
		glBegin(GL_LINES)
		glVertex( self.camera.target.x(), self.camera.target.y(), self.camera.target.z())
		glVertex( self.camera.target.x(), self.camera.target.y(), self.camera.target.z() - 1.*view_length*0.2)
		glEnd()

		glLineWidth(2.0)
		glColor(1.0, 0.0, 0.0)
		# 3D-X
		glBegin(GL_LINES)
		glVertex( self.camera.target.x() - view_length*0.25, self.camera.target.y() - view_length*0.02, self.camera.target.z() + view_length*0.01)
		glVertex( self.camera.target.x() - view_length*0.21, self.camera.target.y() + view_length*0.02, self.camera.target.z() - view_length*0.01)
		glEnd()
		glBegin(GL_LINES)
		glVertex( self.camera.target.x() - view_length*0.21, self.camera.target.y() - view_length*0.02, self.camera.target.z() - view_length*0.01)
		glVertex( self.camera.target.x() - view_length*0.25, self.camera.target.y() + view_length*0.02, self.camera.target.z() + view_length*0.01)
		glEnd()
		glColor(0.0, 1.0, 0.0)
		# 3D-Y
		glBegin(GL_LINES)
		glVertex( self.camera.target.x(), self.camera.target.y() - view_length*0.23, self.camera.target.z())
		glVertex( self.camera.target.x() + view_length*0.02, self.camera.target.y() - view_length*0.25, self.camera.target.z() - view_length*0.01)
		glEnd()
		glBegin(GL_LINES)
		glVertex( self.camera.target.x(), self.camera.target.y() - view_length*0.23, self.camera.target.z())
		glVertex( self.camera.target.x() - view_length*0.02, self.camera.target.y() - view_length*0.25, self.camera.target.z() + view_length*0.01)
		glEnd()
		glBegin(GL_LINES)
		glVertex( self.camera.target.x(), self.camera.target.y() - view_length*0.23, self.camera.target.z())
		glVertex( self.camera.target.x(), self.camera.target.y() - view_length*0.21, self.camera.target.z())
		glEnd()
		glColor(0.0, 0.0, 1.0)
		# 3D-Z
		glBegin(GL_LINES)
		glVertex( self.camera.target.x() - view_length*0.02, self.camera.target.y() - view_length*0.02, self.camera.target.z() - view_length*0.235)
		glVertex( self.camera.target.x() + view_length*0.02, self.camera.target.y() + view_length*0.02, self.camera.target.z() - view_length*0.245)
		glEnd()
		glBegin(GL_LINES)
		glVertex( self.camera.target.x() - view_length*0.02, self.camera.target.y() - view_length*0.02, self.camera.target.z() - view_length*0.235)
		glVertex( self.camera.target.x() + view_length*0.02, self.camera.target.y() - view_length*0.02, self.camera.target.z() - view_length*0.245)
		glEnd()
		glBegin(GL_LINES)
		glVertex( self.camera.target.x() + view_length*0.02, self.camera.target.y() + view_length*0.02, self.camera.target.z() - view_length*0.245)
		glVertex( self.camera.target.x() - view_length*0.02, self.camera.target.y() + view_length*0.02, self.camera.target.z() - view_length*0.235)
		glEnd()

		glViewport(0, 0, self.width, self.height)


		# Render all 2D overlay
		glClear(GL_DEPTH_BUFFER_BIT)
		glMatrixMode(GL_PROJECTION)
		glLoadIdentity()
		gluOrtho2D(0, self.width, self.height, 0)
		glMatrixMode(GL_MODELVIEW)
		glLoadIdentity()

		if self.viewGeometry:
			glColor3f(1., 1., 1.)
			self.renderText(40, self.height-40, 'geometry viewing/editing not supported ...', QtGui.QFont( 'helvetica', 18 ) )
			
		elif self.viewMesh:
			if self.currentMesh == None:
				if self.viewMeshTree:
					self.drawMeshTree()
			else:
				if self.viewMeshTree:
					self.drawMeshTree(self.currentDisplayList['mesh'])

		elif self.viewBoundaries or self.viewConstraints or self.viewLoads or self.viewSolutions:
			if self.currentMesh == None:
				if self.viewMeshTree:
					self.drawMeshTree()
			else:
				if self.viewMeshTree:
					self.drawMeshTree(self.currentDisplayList['mesh'])
			if self.currentDisplayList['solution'] != 'None':
				self.writeInfo(self.currentDisplayList['solution'])

		elif self.viewResults:
			if self.viewAverage and self.currentDisplayList['avg_max_val'] != None:
				if self.currentDisplayList['result'] != 'modeshapes':
					if self.currentDisplayList['subresult'] in ['FY', 'FZ']:
						self.drawLegend(self.currentDisplayList['avg_max_val'],self.currentDisplayList['avg_min_val'],[True,False])
					elif self.currentDisplayList['subresult'] in ['MX', 'MY', 'MZ']:
						self.drawLegend(self.currentDisplayList['avg_max_val'],self.currentDisplayList['avg_min_val'],[False,True])
					else:
						self.drawLegend(self.currentDisplayList['avg_max_val'],self.currentDisplayList['avg_min_val'])
					self.writeInfo(self.currentDisplayList['solution'],self.currentDisplayList['result'],
									self.currentDisplayList['subresult'],self.currentDisplayList['avg_info'])
			else:
				if self.currentDisplayList['max_val'] != None:
					if self.currentDisplayList['result'] != 'modeshapes':
						if self.currentDisplayList['subresult'] in ['FY', 'FZ']:
							self.drawLegend(self.currentDisplayList['max_val'],self.currentDisplayList['min_val'],[True,False])
						elif self.currentDisplayList['subresult'] in ['MX', 'MY', 'MZ']:
							self.drawLegend(self.currentDisplayList['max_val'],self.currentDisplayList['min_val'],[False,True])
						else:
							self.drawLegend(self.currentDisplayList['max_val'],self.currentDisplayList['min_val'])
				self.writeInfo(self.currentDisplayList['solution'],self.currentDisplayList['result'],
									self.currentDisplayList['subresult'],self.currentDisplayList['info'])

		else:
			pass


		if self.mouseButtonPressed == True:
			if self.activeSelection == True:
				self.drawRectangle()

		if self.viewAnimate == True and self.currentDisplayList['result'] == 'modeshapes':
			if self.viewFrame == 12:
				self.veiwFrameRising = False
				self.viewFrame = 11
			elif self.viewFrame == 0:
				self.veiwFrameRising = True
				self.viewFrame = 1
			else:
				if self.veiwFrameRising == True:
					self.viewFrame += 1
				else:
					self.viewFrame -= 1
			time.sleep(self.viewAnimationSpeed[self.viewFrame])
			self.update()

		if self.viewLoadingMessage == True:
			glColor3f(1., 1., 1.)
			self.renderText((self.width/2.)-50, self.height/2., 'Loading...', QtGui.QFont( 'helvetica', 16 ) )

		glFlush()


	def resizeGL(self, widthInPixels, heightInPixels):
		self.camera.setViewportDimensions(widthInPixels, heightInPixels)
		self.width = widthInPixels
		self.height = heightInPixels
		glViewport(0, 0, widthInPixels, heightInPixels)


	def initializeGL(self):
		glClearColor(0.33, 0.43, 0.33, 1.0)
		glClearDepth(1.0)


	def mouseMoveEvent(self, mouseEvent):
		if int(mouseEvent.buttons()) != QtCore.Qt.NoButton:
			# user is dragging
			delta_x = mouseEvent.x() - self.oldx
			delta_y = self.oldy - mouseEvent.y()
			if int(mouseEvent.buttons()) & QtCore.Qt.LeftButton:
				if (self.activeCTRL and self.activeALT):
					self.camera.orbit(self.oldx,self.oldy,mouseEvent.x(),mouseEvent.y())
				else:
					self.activeSelection = True
					self.selectionRectangleEnd = [mouseEvent.x(), mouseEvent.y()]
			elif int(mouseEvent.buttons()) & QtCore.Qt.RightButton :
				self.camera.dollyCameraForward( 3*(delta_x+delta_y), False )
			elif int(mouseEvent.buttons()) & QtCore.Qt.MidButton :
				self.camera.translateSceneRightAndUp( delta_x, delta_y )
			self.update()
		self.oldx = mouseEvent.x()
		self.oldy = mouseEvent.y()


	def mouseDoubleClickEvent(self, mouseEvent):
		self.model.selected_elements.clear()
		self.model.elementsSelected = False
		self.model.selected_nodes.clear()
		self.model.nodesSelected = False
		self.update()


	def mousePressEvent(self, e):
		if self.mouseButtonPressed == False:
			self.selectionRectangleStart = [e.x(), e.y()]
		self.mouseButtonPressed = True


	def mouseReleaseEvent(self, e):

		self.mouseButtonPressed = False
		if self.activeSelection == True and self.currentDisplayList['mesh'] != None:
			nodes = self.nodeSelect()
			for node in self.currentDisplayList['mesh'].nodes:
				if node in nodes:
					if self.activeCTRL:
						if self.model.selectOption == 'Nodes':
							if (node in self.model.selected_nodes):
								del self.model.selected_nodes[node]
					elif self.activeSHIFT:
						self.model.selected_nodes[node] = self.currentDisplayList['mesh'].nodes[node]
					else:
						self.model.selected_nodes[node] = self.currentDisplayList['mesh'].nodes[node]
				else:
					if self.activeCTRL:
						pass
					elif self.activeSHIFT:
						pass
					else:
						if (node in self.model.selected_nodes):
							del self.model.selected_nodes[node]
			if self.model.selectOption == 'Nodes':
				self.model.nodesSelected = True
				self.model.elementsSelected = False
			elif self.model.selectOption == 'Elements' and self.currentDisplayList['mesh'] != None:
				for elm in self.currentDisplayList['mesh'].elements:
					selected = True
					for node in self.currentDisplayList['mesh'].elements[elm].nodes:
						if selected == False:
							break
						if node.number not in nodes:
							selected = False
					if selected == True:
						if self.activeCTRL:
							if (elm in self.model.selected_elements):
								del self.model.selected_elements[elm]
						elif self.activeSHIFT:
							self.model.selected_elements[elm] = self.currentDisplayList['mesh'].elements[elm]
						else:
							self.model.selected_elements[elm] = self.currentDisplayList['mesh'].elements[elm]
					else:
						if self.activeCTRL:
							pass
						elif self.activeSHIFT:
							pass
						else:
							if (elm in self.model.selected_elements):
								del self.model.selected_elements[elm]
				self.model.nodesSelected = False
				self.model.elementsSelected = True
				self.model.selectedElementsDisplay(self.currentDisplayList['mesh'])
			else:
				pass
			self.activeSelection = False
			self.update()
		

	def nodeSelect(self):
		if self.currentDisplayList['mesh'] != None:
			if self.selectionRectangleEnd[0] < self.selectionRectangleStart[0]:
				x = [self.selectionRectangleEnd[0], self.selectionRectangleStart[0],
					 self.selectionRectangleEnd[0], self.selectionRectangleStart[0]]
			else:
				x = [self.selectionRectangleStart[0], self.selectionRectangleEnd[0],
					 self.selectionRectangleStart[0], self.selectionRectangleEnd[0]]
			if self.selectionRectangleEnd[1] < self.selectionRectangleStart[1]:
				y = [self.height-self.selectionRectangleEnd[1], self.height-self.selectionRectangleEnd[1],
					 self.height-self.selectionRectangleStart[1], self.height-self.selectionRectangleStart[1]]
			else:
				y = [self.height-self.selectionRectangleStart[1], self.height-self.selectionRectangleStart[1],
					 self.height-self.selectionRectangleEnd[1], self.height-self.selectionRectangleEnd[1]]
			startpoint = [(0.,0.,0.),(0.,0.,0.),(0.,0.,0.),(0.,0.,0.)]
			endpoint = [(0.,0.,0.),(0.,0.,0.),(0.,0.,0.),(0.,0.,0.)]
			for i in range(4):
				try:
					startpoint[i] = gluUnProject(x[i], y[i], 0., self.view_matrix, self.projection, self.viewport)
					endpoint[i] = gluUnProject(x[i], y[i], 1., self.view_matrix, self.projection, self.viewport)
				except ValueError:
					pass
				else:
					ray_direction = (endpoint[i][0] - startpoint[i][0],
									 endpoint[i][1] - startpoint[i][1],
									 endpoint[i][2] - startpoint[i][2])
					endpoint[i] = (startpoint[i][0] + ray_direction[0],
								   startpoint[i][1] + ray_direction[1],
								   startpoint[i][2] + ray_direction[2])
			P = np.zeros((8,3))
			P[0] = np.array([startpoint[0][0], startpoint[0][1], startpoint[0][2]]) # front top left
			P[1] = np.array([startpoint[1][0], startpoint[1][1], startpoint[1][2]]) # front top right
			P[2] = np.array([startpoint[2][0], startpoint[2][1], startpoint[2][2]]) # front bottom left
			P[3] = np.array([startpoint[3][0], startpoint[3][1], startpoint[3][2]]) # front bottom right
			P[4] = np.array([  endpoint[0][0],   endpoint[0][1],   endpoint[0][2]]) # back top left
			P[5] = np.array([  endpoint[1][0],   endpoint[1][1],   endpoint[1][2]]) # back top right
			P[6] = np.array([  endpoint[2][0],   endpoint[2][1],   endpoint[2][2]]) # back bottom left
			P[7] = np.array([  endpoint[3][0],   endpoint[3][1],   endpoint[3][2]]) # back bottom right
			Frustum = []
			Frustum.append(np.cross((P[5]-P[1]),(P[4]-P[0]))) # top plane normal vector
			Frustum.append(np.cross((P[7]-P[3]),(P[5]-P[1]))) # right plane normal vector
			Frustum.append(np.cross((P[6]-P[2]),(P[7]-P[3]))) # bottom plane normal vector
			Frustum.append(np.cross((P[4]-P[0]),(P[6]-P[2]))) # left plane normal vector
			nodes = {}
			for node in self.currentDisplayList['mesh'].nodes:
				if self.modelCentered:
					point_to_check = np.array([self.currentDisplayList['mesh'].nodes[node].coord[0][0]+self.coordSys0_centered.origin.x(),
											   self.currentDisplayList['mesh'].nodes[node].coord[1][0]+self.coordSys0_centered.origin.y(),
											   self.currentDisplayList['mesh'].nodes[node].coord[2][0]+self.coordSys0_centered.origin.z()])
				else:
					point_to_check = np.array([self.currentDisplayList['mesh'].nodes[node].coord[0][0],
											   self.currentDisplayList['mesh'].nodes[node].coord[1][0],
											   self.currentDisplayList['mesh'].nodes[node].coord[2][0]])
				if np.dot(P[0]-point_to_check,Frustum[0]) < 0:
					pass
				elif np.dot(P[1]-point_to_check,Frustum[1]) < 0:
					pass
				elif np.dot(P[3]-point_to_check,Frustum[2]) < 0:
					pass
				elif np.dot(P[2]-point_to_check,Frustum[3]) < 0:
					pass
				else:
					nodes[node] = self.currentDisplayList['mesh'].nodes[node]
			return nodes


	def drawRectangle(self):
		glLineWidth(2.0)
		glColor3f(0., 0., 0.)

		glEnable(GL_LINE_STIPPLE)
		factor = 3
		pattern = 0x5555
		glLineStipple(factor, pattern)
 
		glBegin(GL_LINE_LOOP)
		glVertex2f(self.selectionRectangleStart[0], self.selectionRectangleStart[1])
		glVertex2f(self.selectionRectangleEnd[0],   self.selectionRectangleStart[1])
		glVertex2f(self.selectionRectangleEnd[0],   self.selectionRectangleEnd[1])
		glVertex2f(self.selectionRectangleStart[0], self.selectionRectangleEnd[1])
		glEnd()

		glDisable(GL_LINE_STIPPLE)

		
	def drawMeshTree(self,mesh=None):
		'''
	Write up a tree of current mesh properties,
	with nodes, elements, section assignments,
	solutions, boundaries, constraints and loads.
	'''
		inset = 350
		if mesh != None and not hasattr(mesh,'is3D'):
			for solution in self.model.meshes[self.currentMesh].solutions:
				length = len(solution)+len(self.model.meshes[self.currentMesh].solutions[solution]['Type'])
				if length > 25:
					inset = 400
				length = 1
				for boundary in self.model.meshes[self.currentMesh].solutions[solution]['Boundaries']:
					length = len(boundary)+len(self.model.meshes[self.currentMesh].solutions[solution]['Boundaries'][boundary]['Type'])
				for constraint in self.model.meshes[self.currentMesh].solutions[solution]['Constraints']:
					len2 = len(constraint)+len(self.model.meshes[self.currentMesh].solutions[solution]['Constraints'][constraint]['Type'])
					if len2 > length:
						length = len2
				for load in self.model.meshes[self.currentMesh].solutions[solution]['Loads']:
					len2 = len(load)+len(self.model.meshes[self.currentMesh].solutions[solution]['Loads'][load]['Type'])
					if len2 > length:
						length = len2
				if length > 32:
					inset = 540
				elif length > 24:
					inset = 480
				elif length > 16:
					inset = 420
				else:
					pass
		h = (self.height/2.)-180
		w = self.width-inset
		glColor3f(1., 1., 1.)
		if mesh == None:
			self.renderText(w, h, 'No mesh selected', QtGui.QFont( 'helvetica', 14 ))
		elif hasattr(mesh,'is3D') or self.currentMesh == 'None':
			self.renderText(w, h, 'Mesh from results:', QtGui.QFont( 'helvetica', 14 ))
			self.renderText(w, h+20, 'Copy into a new mesh', QtGui.QFont( 'helvetica', 14 ))
			self.renderText(w, h+40, 'by creating an element', QtGui.QFont( 'helvetica', 14 ))
			self.renderText(w, h+60, 'set of this mesh in', QtGui.QFont( 'helvetica', 14 ))
			self.renderText(w, h+80, 'order to use in a new', QtGui.QFont( 'helvetica', 14 ))
			self.renderText(w, h+100, 'finite element analysis.', QtGui.QFont( 'helvetica', 14 ))
		elif len(self.model.meshes[self.currentMesh].elements) == 0:
			self.renderText(w, h, 'Mesh ['+self.currentMesh+']', QtGui.QFont( 'helvetica', 14 ))
		else:
			self.renderText(w, h, 'Mesh ['+self.currentMesh+']', QtGui.QFont( 'helvetica', 14 ))
			self.renderText(w, h+22, '  |-- Nodes    [%d ... %d]' %       (min(mesh.nodes.keys()),max(mesh.nodes.keys())), QtGui.QFont( 'helvetica', 14 ))
			self.renderText(w, h+34, '  -', QtGui.QFont( 'helvetica', 14 ))
			self.renderText(w, h+46, '  |-- Elements [%d ... %d]' % (min(mesh.elements.keys()),max(mesh.elements.keys())), QtGui.QFont( 'helvetica', 14 ))
			self.renderText(w, h+58, '  -', QtGui.QFont( 'helvetica', 14 ))
			h += 70
			if mesh.sections_applied:
				self.renderText(w, h, '  |-- Sections (Applied)',     QtGui.QFont( 'helvetica', 14 ))
			else:
				self.renderText(w, h, '  |-- Sections (Not Applied)', QtGui.QFont( 'helvetica', 14 ))
			for section in mesh.sections:
				h += 20
				self.renderText(w, h, '  |    |-- '+section, QtGui.QFont( 'helvetica', 14 ))
			h += 24
			self.renderText(w, h-12, '  -', QtGui.QFont( 'helvetica', 14 ))
			self.renderText(w, h, '  |-- Solutions', QtGui.QFont( 'helvetica', 14 ))
			sol_num = len(mesh.solutions)
			for solution in mesh.solutions:
				if sol_num == 1:
					h += 20
					self.renderText(w, h, '       |-- '+solution+' ('+mesh.solutions[solution]['Type']+')', QtGui.QFont( 'helvetica', 14 ))
					h += 20
					self.renderText(w, h, '            |-- boundaries', QtGui.QFont( 'helvetica', 14 ))
					if len(mesh.solutions[solution]['Boundaries']) != 0:
						for boundary in mesh.solutions[solution]['Boundaries']:
							h += 20
							self.renderText(w, h, '            |    |-- '+boundary+' ('+mesh.solutions[solution]['Boundaries'][boundary]['Type']+')', QtGui.QFont( 'helvetica', 14 ))
					h += 20
					self.renderText(w, h, '            |-- constraints', QtGui.QFont( 'helvetica', 14 ))
					if len(mesh.solutions[solution]['Constraints']) != 0:
						for constraint in mesh.solutions[solution]['Constraints']:
							h += 20
							self.renderText(w, h, '            |    |-- '+constraint+' ('+mesh.solutions[solution]['Constraints'][constraint]['Type']+')', QtGui.QFont( 'helvetica', 14 ))
					h += 20
					self.renderText(w, h, '            |-- loads', QtGui.QFont( 'helvetica', 14 ))
					if len(mesh.solutions[solution]['Loads']) != 0:
						for load in mesh.solutions[solution]['Loads']:
							h += 20
							self.renderText(w, h, '                 |-- '+load+' ('+mesh.solutions[solution]['Loads'][load]['Type']+')', QtGui.QFont( 'helvetica', 14 ))
				else:
					sol_num -= 1
					h += 20
					self.renderText(w, h, '       |-- '+solution+' ('+mesh.solutions[solution]['Type']+')', QtGui.QFont( 'helvetica', 14 ))
					h += 20
					self.renderText(w, h, '       |    |-- boundaries', QtGui.QFont( 'helvetica', 14 ))
					if len(mesh.solutions[solution]['Boundaries']) != 0:
						for boundary in mesh.solutions[solution]['Boundaries']:
							h += 20
							self.renderText(w, h, '       |    |    |-- '+boundary+' ('+mesh.solutions[solution]['Boundaries'][boundary]['Type']+')', QtGui.QFont( 'helvetica', 14 ))
					h += 20
					self.renderText(w, h, '       |    |-- constraints', QtGui.QFont( 'helvetica', 14 ))
					if len(mesh.solutions[solution]['Constraints']) != 0:
						for constraint in mesh.solutions[solution]['Constraints']:
							h += 20
							self.renderText(w, h, '       |    |    |-- '+constraint+' ('+mesh.solutions[solution]['Constraints'][constraint]['Type']+')', QtGui.QFont( 'helvetica', 14 ))
					h += 20
					self.renderText(w, h, '       |    |-- loads', QtGui.QFont( 'helvetica', 14 ))
					if len(mesh.solutions[solution]['Loads']) != 0:
						for load in mesh.solutions[solution]['Loads']:
							h += 20
							self.renderText(w, h, '       |         |-- '+load+' ('+mesh.solutions[solution]['Loads'][load]['Type']+')', QtGui.QFont( 'helvetica', 14 ))


	def drawLegend(self,max_val,min_val,shear_bend=[False, False]):
		'''
	Draw legend using maximum and minimum values
	for the contour plot rendered. Displacements,
	Stresses, Strains or Nodeforces.
	'''
		disp_colors = [ (  0.0,   0.0,   1.0), # blue
						(  0.0, 0.333,   1.0),  
						(  0.0, 0.666,   1.0),  
						(  0.0,   1.0,   1.0),  
						(  0.0,   1.0, 0.666),  
						(  0.0,   1.0, 0.333),
						(  0.0,   1.0,   0.0), # green
						(0.333,   1.0,   0.0),  
						(0.666,   1.0,   0.0),  
						(  1.0,   1.0,   0.0),  
						(  1.0, 0.666,   0.0),  
						(  1.0, 0.333,   0.0),
						(  1.0,   0.0,   0.0) ] # red
		if shear_bend[0]:
			sc = (0.8, 0.4, 0.1)
			disp_colors = [ sc, sc, sc, sc, sc, sc, sc, sc, sc, sc, sc, sc, sc ]
		if shear_bend[1]:
			bc = (0.5, 0.1, 0.5)
			disp_colors = [ bc, bc, bc, bc, bc, bc, bc, bc, bc, bc, bc, bc, bc ]
		glColor3f(disp_colors[0][0], disp_colors[0][1], disp_colors[0][2])
		glRectf(self.width-80, (self.height/2.)+180, self.width-40, (self.height/2.)+150)
		glColor3f(disp_colors[1][0], disp_colors[1][1], disp_colors[1][2])
		glRectf(self.width-80, (self.height/2.)+150, self.width-40, (self.height/2.)+120)
		glColor3f(disp_colors[2][0], disp_colors[2][1], disp_colors[2][2])
		glRectf(self.width-80, (self.height/2.)+120, self.width-40, (self.height/2.)+ 90)
		glColor3f(disp_colors[3][0], disp_colors[3][1], disp_colors[3][2])
		glRectf(self.width-80, (self.height/2.)+ 90, self.width-40, (self.height/2.)+ 60)
		glColor3f(disp_colors[4][0], disp_colors[4][1], disp_colors[4][2])
		glRectf(self.width-80, (self.height/2.)+ 60, self.width-40, (self.height/2.)- 30)
		glColor3f(disp_colors[5][0], disp_colors[5][1], disp_colors[5][2])
		glRectf(self.width-80, (self.height/2.)- 30, self.width-40, (self.height/2.)-  0)
		glColor3f(disp_colors[6][0], disp_colors[6][1], disp_colors[6][2])
		glRectf(self.width-80, (self.height/2.)-  0, self.width-40, (self.height/2.)- 30)
		glColor3f(disp_colors[7][0], disp_colors[7][1], disp_colors[7][2])
		glRectf(self.width-80, (self.height/2.)- 30, self.width-40, (self.height/2.)- 60)
		glColor3f(disp_colors[8][0], disp_colors[8][1], disp_colors[8][2])
		glRectf(self.width-80, (self.height/2.)- 60, self.width-40, (self.height/2.)- 90)
		glColor3f(disp_colors[9][0], disp_colors[9][1], disp_colors[9][2])
		glRectf(self.width-80, (self.height/2.)- 90, self.width-40, (self.height/2.)-120)
		glColor3f(disp_colors[10][0], disp_colors[10][1], disp_colors[10][2])
		glRectf(self.width-80, (self.height/2.)-120, self.width-40, (self.height/2.)-150)
		glColor3f(disp_colors[11][0], disp_colors[11][1], disp_colors[11][2])
		glRectf(self.width-80, (self.height/2.)-150, self.width-40, (self.height/2.)-180)
		glColor3f(disp_colors[12][0], disp_colors[12][1], disp_colors[12][2])
		glRectf(self.width-80, (self.height/2.)-180, self.width-40, (self.height/2.)-210)

		# values
		glColor3f(1., 1., 1.)
		self.renderText(self.width-190, (self.height/2.)-185, '%6.3E' % (max_val), QtGui.QFont( 'helvetica', 13 ) )
		self.renderText(self.width-190, (self.height/2.)-155, '%6.3E' % (min_val+(max_val-min_val)*11./12.), QtGui.QFont( 'helvetica', 13 ) )
		self.renderText(self.width-190, (self.height/2.)-125, '%6.3E' % (min_val+(max_val-min_val)*10./12.), QtGui.QFont( 'helvetica', 13 ) )
		self.renderText(self.width-190, (self.height/2.)- 95, '%6.3E' % (min_val+(max_val-min_val)*9./12.), QtGui.QFont( 'helvetica', 13 ) )
		self.renderText(self.width-190, (self.height/2.)- 65, '%6.3E' % (min_val+(max_val-min_val)*8./12.), QtGui.QFont( 'helvetica', 13 ) )
		self.renderText(self.width-190, (self.height/2.)- 35, '%6.3E' % (min_val+(max_val-min_val)*7./12.), QtGui.QFont( 'helvetica', 13 ) )
		self.renderText(self.width-190, (self.height/2.)-  5, '%6.3E' % (min_val+(max_val-min_val)*6./12.), QtGui.QFont( 'helvetica', 13 ) )
		self.renderText(self.width-190, (self.height/2.)+ 25, '%6.3E' % (min_val+(max_val-min_val)*5./12.), QtGui.QFont( 'helvetica', 13 ) )
		self.renderText(self.width-190, (self.height/2.)+ 55, '%6.3E' % (min_val+(max_val-min_val)*4./12.), QtGui.QFont( 'helvetica', 13 ) )
		self.renderText(self.width-190, (self.height/2.)+ 85, '%6.3E' % (min_val+(max_val-min_val)*3./12.), QtGui.QFont( 'helvetica', 13 ) )
		self.renderText(self.width-190, (self.height/2.)+115, '%6.3E' % (min_val+(max_val-min_val)*2./12.), QtGui.QFont( 'helvetica', 13 ) )
		self.renderText(self.width-190, (self.height/2.)+145, '%6.3E' % (min_val+(max_val-min_val)*1./12.), QtGui.QFont( 'helvetica', 13 ) )
		self.renderText(self.width-190, (self.height/2.)+175, '%6.3E' % (min_val), QtGui.QFont( 'helvetica', 13 ) )


	def writeInfo(self,solution,result=None,subresult=None,info=None):
		'''
	Write info about current solution
	and/or result in a 2D overlay.
	'''
		glColor3f(1., 1., 1.)
		self.renderText(self.width/3-60, self.height-90, 'Solution: '+solution, QtGui.QFont( 'helvetica', 15 ) )
		if result == None:
			pass
		else:
			if subresult == None:
				self.renderText(self.width/3-60, self.height-60, 'Result: '+result, QtGui.QFont( 'helvetica', 15 ) )
				self.renderText(self.width/3-60, self.height-30, 'Deform scale factor: '+str(self.model.scale_factor), QtGui.QFont( 'helvetica', 15 ) )
			else:
				self.renderText(self.width/3-60, self.height-60, 'Result: '+result+', '+subresult, QtGui.QFont( 'helvetica', 15 ) )
				self.renderText(self.width/3-60, self.height-30, 'Deform scale factor: '+str(self.model.scale_factor), QtGui.QFont( 'helvetica', 15 ) )
				if info != None:
					self.renderText(60, 60, info, QtGui.QFont( 'helvetica', 15 ) )
		




class Model(object):
	'''
Class describing the 3D model to be
rendered by the viewer. Builds
OpenGL display lists from .out-files
or .sol-files.
'''
	def __init__(self, gui):

		self.gui = gui
		
		self.nodesets = {}
		self.elementsets = {}
		self.materials = {'6061-T6_aluminum (N m kg)': 	 {'Elasticity':   689e8, 'Poisson ratio': 0.35, 'Density':   2700.},
						  '1010_carbon_steel (N m kg)':	 {'Elasticity':   205e9, 'Poisson ratio': 0.29, 'Density':   7870.},
						  '316_stainless_steel (N m kg)':  {'Elasticity':   193e9, 'Poisson ratio': 0.27, 'Density':   7870.},
						  'Grade2_titanium (N m kg)':	 	 {'Elasticity':   105e9, 'Poisson ratio': 0.37, 'Density':   4510.},
						  '6061-T6_aluminum (N mm kg)': 	 {'Elasticity':  68900., 'Poisson ratio': 0.35, 'Density':  2.7e-9},
						  '1010_carbon_steel (N mm kg)':	 {'Elasticity': 205000., 'Poisson ratio': 0.29, 'Density': 7.87e-9},
						  '316_stainless_steel (N mm kg)': {'Elasticity': 193000., 'Poisson ratio': 0.27, 'Density': 7.87e-9},
						  'Grade2_titanium (N mm kg)':	 {'Elasticity': 105000., 'Poisson ratio': 0.37, 'Density': 4.51e-9} }
		self.sections = {}
		self.meshes = {}
		self.results = {}

		self.nodesSelected = False
		self.selected_nodes = {}
		self.elementsSelected = False
		self.selected_elements = {}
		self.selectOption = 'Nodes'

		self.scaleShearBendDiagram = 1.
		self.scale_factor = 20.
		self.displayLists = {}


	def clearModel(self):
		'''
	Clears out all data in model from
	current session.
	'''
		self.gui.viewer.currentMesh = 'None'
		self.gui.viewer.currentSolution = 'None'
		self.gui.viewer.currentResults = 'None'
		self.gui.current_results = {'Solution': 'None', 'Result': 'None', 'Subresult': 'None'}
		self.gui.viewer.viewShaded = False
		self.gui.viewer.currentDisplayList = {  'mesh':			None,
												'solution': 	'None',
												'result': 		'None',
												'subresult':	'None',
												'info':			'None',
												'avg_info':		'None',
												'max_val':		None,
												'min_val':		None,
												'avg_max_val':	None,
												'avg_min_val':	None,
												'view radius': 	2,
												'view scope':  	{ 'max': [ 1., 1., 1.],
																  'min': [-1.,-1.,-1.] },
												'displaylist':	{ 'orientation': None,
																  'nodes':		 None,
																  'wireframe':	 None,
																  'shaded':		 None,
																  'average':	 None } }

		self.nodesSelected = False
		self.selected_nodes = {}
		self.elementsSelected = False
		self.selected_elements = {}

		self.nodesets.clear()
		self.elementsets.clear()
		self.results.clear()
		self.meshes.clear()
		self.materials = {'6061-T6_aluminum (N m kg)': 	 {'Elasticity':   689e8, 'Poisson ratio': 0.35, 'Density':   2700.},
						  '1010_carbon_steel (N m kg)':	 {'Elasticity':   205e9, 'Poisson ratio': 0.29, 'Density':   7870.},
						  '316_stainless_steel (N m kg)':  {'Elasticity':   193e9, 'Poisson ratio': 0.27, 'Density':   7870.},
						  'Grade2_titanium (N m kg)':	 	 {'Elasticity':   105e9, 'Poisson ratio': 0.37, 'Density':   4510.},
						  '6061-T6_aluminum (N mm kg)': 	 {'Elasticity':  68900., 'Poisson ratio': 0.35, 'Density':  2.7e-9},
						  '1010_carbon_steel (N mm kg)':	 {'Elasticity': 205000., 'Poisson ratio': 0.29, 'Density': 7.87e-9},
						  '316_stainless_steel (N mm kg)': {'Elasticity': 193000., 'Poisson ratio': 0.27, 'Density': 7.87e-9},
						  'Grade2_titanium (N mm kg)':	 {'Elasticity': 105000., 'Poisson ratio': 0.37, 'Density': 4.51e-9} }
		self.sections.clear()
		self.displayLists.clear()
		self.gui.viewer.update()


	def deleteFromModel(self):
		'''
	Deletes selected items from self.model.
	'''
		if self.gui.new_deletion['---'] == 'none':
			pass
		elif self.gui.new_deletion['Delete...'] in ['Element(s)', 'Node(s)']:
			mesh = self.meshes[self.gui.viewer.currentMesh]
			if self.gui.new_deletion['Delete...'] == 'Element(s)':
				print('\n\tDeleting selected elements:',end=' ')
				if len(self.selected_elements) < 9:
					print(sorted(self.selected_elements.keys()))
				else:
					d = sorted(self.selected_elements.keys())
					print('['+str(d[0])+', '+str(d[1])+', '+str(d[2])+', '+str(d[3])+', '+str(d[4])+ \
							', '+str(d[5])+', '+str(d[6])+', '+str(d[7])+', ...]')
				for element in self.selected_elements:
					del_nodes = []
					for node in range(len(mesh.elements[element].nodes)):
						del_node = True
						for elm in mesh.elements:
							if elm != element and mesh.elements[element].nodes[node] in \
																	mesh.elements[elm].nodes:
								del_node = False
						if del_node:
							del_nodes.append(mesh.elements[element].nodes[node])
					for node in mesh.elements[element].nodes:
						if node in del_nodes:
							del mesh.nodes[node.number]
					del mesh.elements[element]
			else:
				print('\n\tDeleting selected nodes:',end=' ')
				if len(self.selected_nodes) < 9:
					print(sorted(self.selected_nodes.keys()))
				else:
					d = sorted(self.selected_nodes.keys())
					print('['+str(d[0])+', '+str(d[1])+', '+str(d[2])+', '+str(d[3])+', '+str(d[4])+ \
							', '+str(d[5])+', '+str(d[6])+', '+str(d[7])+', ...]')
				for node in self.selected_nodes:
					del_node = True
					for element in mesh.elements:
						if self.selected_nodes[node] in mesh.elements[element].nodes:
							del_node = False
					if del_node:
						del mesh.nodes[node]
					else:
						print('\n\tCannot delete node', node, 'because it is attached to an element')

			self.nodesSelected = False
			self.selected_nodes.clear()
			self.elementsSelected = False
			self.selected_elements.clear()

			if len(mesh.nodes) != 0:
				x_max = max(mesh.nodes[i].coord[0][0] for i in mesh.nodes )
				x_min = min(mesh.nodes[i].coord[0][0] for i in mesh.nodes )
				y_max = max(mesh.nodes[i].coord[1][0] for i in mesh.nodes )
				y_min = min(mesh.nodes[i].coord[1][0] for i in mesh.nodes )
				z_max = max(mesh.nodes[i].coord[2][0] for i in mesh.nodes )
				z_min = min(mesh.nodes[i].coord[2][0] for i in mesh.nodes )
			else:
				x_max = x_min = y_max = y_min = z_max = z_min = 0
			mesh.viewScope = {'max': [x_max, y_max, z_max], 'min': [x_min, y_min, z_min]}
			mesh.viewRadius = 1.25*max( (x_max-x_min)/2., (y_max-y_min)/2., (z_max-z_min)/2. )
			self.buildDisplayList(mesh)
			self.gui.new_mesh_view = {'Mesh': self.gui.viewer.currentMesh}
			self.elementOrientation()
			self.gui.viewer.update()
			
		elif self.gui.new_deletion['Delete...'] == 'Nodeset':
			del self.nodesets[int(self.gui.new_deletion['---'])]
			print('\n\tDeleting nodeset', self.gui.new_deletion['---'])
		elif self.gui.new_deletion['Delete...'] == 'Elementset':
			del self.elementsets[int(self.gui.new_deletion['---'])]
			print('\n\tDeleting elementset', self.gui.new_deletion['---'])

		elif self.gui.new_deletion['Delete...'] == 'Material':
			del self.materials[self.gui.new_deletion['---']]
			print('\n\tDeleting material', self.gui.new_deletion['---'])
			sect_to_delete = []
			for section in self.sections:
				if self.sections[section]['Material'] == self.gui.new_deletion['---']:
					sect_to_delete.append(section)
					print('\n\tDeleting section', section, 'because it has material', self.gui.new_deletion['---'])
					for mesh in self.meshes:
						for element in self.meshes[mesh].elements:
							if self.meshes[mesh].elements[element].section == section:
								self.meshes[mesh].elements[element].section = None
			for sect in range(len(sect_to_delete)):
				del self.sections[sect_to_delete[sect]]
			for mesh in self.meshes:
				self.checkForSection(self.meshes[mesh])

		elif self.gui.new_deletion['Delete...'] == 'Section':
			print('\n\tDeleting section', self.gui.new_deletion['---'])
			for mesh in self.meshes:
				for element in self.meshes[mesh].elements:
					if self.meshes[mesh].elements[element].section == self.gui.new_deletion['---']:
						self.meshes[mesh].elements[element].section = None
			del self.sections[self.gui.new_deletion['---']]
			for mesh in self.meshes:
				self.checkForSection(self.meshes[mesh])

		elif self.gui.new_deletion['Delete...'] == 'Mesh':
			print('\n\tDeleting mesh', self.gui.new_deletion['---'])
			if self.gui.viewer.currentDisplayList['mesh'] == self.meshes[self.gui.new_deletion['---']]:
				self.gui.viewer.currentMesh = 'None'
				self.gui.viewer.currentDisplayList = {  'mesh':			None,
														'solution': 	'None',
														'result': 		'None',
														'subresult':	'None',
														'info':			'None',
														'avg_info':		'None',
														'max_val':		None,
														'min_val':		None,
														'avg_max_val':	None,
														'avg_min_val':	None,
														'view radius': 	2,
														'view scope':  	{ 'max': [ 1., 1., 1.],
																		  'min': [-1.,-1.,-1.] },
														'displaylist':	{ 'nodes':		None,
																		  'wireframe':	None,
																		  'shaded':		None,
																		  'average':	None } }
			del self.meshes[self.gui.new_deletion['---']]

		elif self.gui.new_deletion['Delete...'] == 'Solution':
			for mesh in self.meshes:
				print('\n\tDeleting solution', self.gui.new_deletion['---'], 'from mesh', mesh)
				del self.meshes[mesh].solutions[self.gui.new_deletion['---']]
				del self.meshes[mesh].displayLists['solutions'][self.gui.new_deletion['---']]
				if self.gui.viewer.currentDisplayList['solution'] == self.gui.new_deletion['---']:
					self.gui.viewer.currentDisplayList['solution'] = 'None'
		elif self.gui.new_deletion['Delete...'] == 'Boundary':
			for mesh in self.meshes:
				for solution in self.meshes[mesh].solutions:
					del_from_solution = False
					for boundary in self.meshes[mesh].solutions[solution]['Boundaries']:
						if boundary == self.gui.new_deletion['---']:
							print('\n\tDeleting boundary', boundary, 'from solution', solution)
							del_from_solution = True
					if del_from_solution:
						del self.meshes[mesh].solutions[solution]['Boundaries'][self.gui.new_deletion['---']]
						del self.meshes[mesh].displayLists['solutions'][solution]['boundaries'][self.gui.new_deletion['---']]
		elif self.gui.new_deletion['Delete...'] == 'Constraint':
			for mesh in self.meshes:
				for solution in self.meshes[mesh].solutions:
					del_from_solution = False
					for constraint in self.meshes[mesh].solutions[solution]['Constraints']:
						if constraint == self.gui.new_deletion['---']:
							print('\n\tDeleting constraint', constraint, 'from solution', solution)
							del_from_solution = True
					if del_from_solution:
						del self.meshes[mesh].solutions[solution]['Constraints'][self.gui.new_deletion['---']]
						del self.meshes[mesh].displayLists['solutions'][solution]['constraints'][self.gui.new_deletion['---']]
		elif self.gui.new_deletion['Delete...'] == 'Load':
			for mesh in self.meshes:
				for solution in self.meshes[mesh].solutions:
					del_from_solution = False
					for load in self.meshes[mesh].solutions[solution]['Loads']:
						if load == self.gui.new_deletion['---']:
							print('\n\tDeleting load', load, 'from solution', solution)
							del_from_solution = True
					if del_from_solution:
						del self.meshes[mesh].solutions[solution]['Loads'][self.gui.new_deletion['---']]
						del self.meshes[mesh].displayLists['solutions'][solution]['loads'][self.gui.new_deletion['---']]
		else:
			print('\n\tUnknown delete category:', self.gui.new_deletion['Delete...'])


	def createNewNode(self):
		'''
	Creates a new node from user input.
	'''
		mesh = self.meshes[self.gui.viewer.currentMesh]
		if self.gui.viewer.currentMesh == 'None':
			print('\n\tNo mesh currently selected.')
			print('\tNew node not created.')
		elif int(self.gui.new_node['Number']) in mesh.nodes:
			print('\n\tNode number', self.gui.new_node['Number'], 'already exists.')
			print('\tNew node not created.')
		else:
			mesh.nodes[int(self.gui.new_node['Number'])] = \
							Node(int(self.gui.new_node['Number']), float(self.gui.new_node['x-coordinate']), \
									float(self.gui.new_node['y-coordinate']), float(self.gui.new_node['z-coordinate']))
			self.buildDisplayList(mesh)
			self.gui.new_mesh_view = {'Mesh': self.gui.viewer.currentMesh}
			print('\n\tNew node number: '+self.gui.new_node['Number'])
			print('\tCoord:', float(self.gui.new_node['x-coordinate']), float(self.gui.new_node['y-coordinate']), float(self.gui.new_node['z-coordinate']))

			x_max = max(mesh.nodes[i].coord[0][0] for i in mesh.nodes )
			x_min = min(mesh.nodes[i].coord[0][0] for i in mesh.nodes )
			y_max = max(mesh.nodes[i].coord[1][0] for i in mesh.nodes )
			y_min = min(mesh.nodes[i].coord[1][0] for i in mesh.nodes )
			z_max = max(mesh.nodes[i].coord[2][0] for i in mesh.nodes )
			z_min = min(mesh.nodes[i].coord[2][0] for i in mesh.nodes )
			mesh.viewScope = {'max': [x_max, y_max, z_max], 'min': [x_min, y_min, z_min]}
			mesh.viewRadius = 1.25*max( (x_max-x_min)/2., (y_max-y_min)/2., (z_max-z_min)/2. )
			self.buildDisplayList(mesh)
			self.gui.new_mesh_view = {'Mesh': self.gui.viewer.currentMesh}
			self.elementOrientation()
			self.gui.viewer.update()


	def moveSelectedNodes(self,x=None,y=None,z=None):
		'''
	Moves the selected nodes in direction and
	distance given by user input.
	'''
		mesh = self.meshes[self.gui.viewer.currentMesh]
		try:
			if x == None:
				float(self.gui.new_node_movement['x-direction'])
				float(self.gui.new_node_movement['y-direction'])
				float(self.gui.new_node_movement['z-direction'])
		except ValueError:
			print('\n\tx-, y- and z-direction specified must be a number.')		
		else:
			if x == None:
				x_dir = float(self.gui.new_node_movement['x-direction'])
				y_dir = float(self.gui.new_node_movement['y-direction'])
				z_dir = float(self.gui.new_node_movement['z-direction'])
			else:
				x_dir = x
				y_dir = y
				z_dir = z
			for node in self.selected_nodes:
				mesh.nodes[node].coord[0][0] += x_dir
				mesh.nodes[node].coord[1][0] += y_dir
				mesh.nodes[node].coord[2][0] += z_dir
			self.nodesSelected = False
			self.selected_nodes.clear()

			x_max = max(mesh.nodes[i].coord[0][0] for i in mesh.nodes )
			x_min = min(mesh.nodes[i].coord[0][0] for i in mesh.nodes )
			y_max = max(mesh.nodes[i].coord[1][0] for i in mesh.nodes )
			y_min = min(mesh.nodes[i].coord[1][0] for i in mesh.nodes )
			z_max = max(mesh.nodes[i].coord[2][0] for i in mesh.nodes )
			z_min = min(mesh.nodes[i].coord[2][0] for i in mesh.nodes )
			mesh.viewScope = {'max': [x_max, y_max, z_max], 'min': [x_min, y_min, z_min]}
			mesh.viewRadius = 1.25*max( (x_max-x_min)/2., (y_max-y_min)/2., (z_max-z_min)/2. )
			self.buildDisplayList(mesh)
			self.gui.new_mesh_view = {'Mesh': self.gui.viewer.currentMesh}
			self.elementOrientation()
			self.gui.viewer.update()


	def createNewElement(self):
		'''
	Creates new elements as specified by
	user input.
	'''
		nodes = []
		mesh = self.meshes[self.gui.viewer.currentMesh]
		if self.gui.new_elements['Node 1'] != '':
			if self.gui.new_elements['Node 1'].isdigit():
				if int(self.gui.new_elements['Node 1']) in mesh.nodes:
					nodes.append(mesh.nodes[int(self.gui.new_elements['Node 1'])])
				else:
					print('\n\tFirst node '+self.gui.new_elements['Node 1']+' does not exist, creating new one.')
			else:
				print('\n\tFirst node '+self.gui.new_elements['Node 1']+' is not a valid node number.')
		if self.gui.new_elements['Node 2'] != '' and len(nodes) != 0:
			if self.gui.new_elements['Node 2'].isdigit():
				if int(self.gui.new_elements['Node 2']) in mesh.nodes:
					nodes.append(mesh.nodes[int(self.gui.new_elements['Node 2'])])
				else:
					print('\n\tSecond node '+self.gui.new_elements['Node 2']+' does not exist, creating new one.')
			else:
				print('\n\tSecond node '+self.gui.new_elements['Node 2']+' is not a valid node number.')

		element_number = 1
		if len(mesh.elements) != 0:
			element_number = max(mesh.elements) +1

		element_size = 1.
		try:
			float(self.gui.new_elements['Element size'])
		except ValueError:
			print('\n\t'+self.gui.new_elements['Element size']+' is not a valid element size')
		else:
			is_3D = False
			element_created = True
			for node in nodes:
				mesh.nodes[node.number] = node
				if mesh.nodes[node.number].coord[2][0] != 0.:
					is_3D = True
			element_size = float(self.gui.new_elements['Element size'])

			start_point = [0.,0.,0.]
			direction   = [1.,0.,0.]
			angle = 0.
			node_number = 1
			if len(mesh.nodes) != 0:
				node_number = max(mesh.nodes) +1
				start_point = [0.,0.,2.0*mesh.viewRadius]

			if len(nodes) == 1:
				start_point = [nodes[0].coord[0][0], nodes[0].coord[1][0], nodes[0].coord[2][0]]
				if len(mesh.nodes) != 0:
					node_number = max(mesh.nodes)
				else:
					node_number = nodes[0].number
				nodes.append(Node(node_number+1, start_point[0]+element_size*direction[0], start_point[1], start_point[2]))

			elif len(nodes) == 2:
				if self.gui.new_elements['Element type'] not in ['BEAM2N', 'BEAM2N2D', 'ROD2N', 'ROD2N2D']:
					start_point = [nodes[0].coord[0][0],nodes[0].coord[1][0],nodes[0].coord[2][0]]
					if len(mesh.nodes) != 0:
						node_number = max(mesh.nodes)
					else:
						node_number = nodes[0].number
					direction   = normalize([nodes[1].coord[0][0]-nodes[0].coord[0][0],
								   			 nodes[1].coord[1][0]-nodes[0].coord[1][0],
								   			 nodes[1].coord[2][0]-nodes[0].coord[2][0]])
					rotation_axis_point2 = np.add(start_point,np.cross([1.,0.,0.],direction))
					angle = np.arccos(np.dot([1.,0.,0.],direction))
					element_size = np.sqrt((nodes[1].coord[0][0]-nodes[0].coord[0][0])**2 + \
										   (nodes[1].coord[1][0]-nodes[0].coord[1][0])**2 + \
										   (nodes[1].coord[2][0]-nodes[0].coord[2][0])**2)
					nodes[1].coord[0][0] = start_point[0]+element_size
					nodes[1].coord[1][0] = start_point[1]
					nodes[1].coord[2][0] = start_point[2]
			else:
				nodes.append(Node(node_number,	 start_point[0],			  start_point[1], start_point[2]))
				nodes.append(Node(node_number+1, start_point[0]+element_size, start_point[1], start_point[2]))				

			if self.gui.new_elements['Element type'] == 'BEAM2N':
				print('\n\tNew BEAM2N element...')
				if angle != 0:
					moved_nodes = []
					for node in range(len(nodes)):
						if nodes[node].number in moved_nodes:
							pass
						else:
							moved_nodes.append(nodes[node].number)
							point0 = [nodes[node].coord[0][0],
									  nodes[node].coord[1][0],
									  nodes[node].coord[2][0]]
							point1 = rotatePointAboutAxis(point0,start_point,rotation_axis_point2,angle)
							nodes[node].coord[0][0] = point1[0]
							nodes[node].coord[1][0] = point1[1]
							nodes[node].coord[2][0] = point1[2]
				for node in nodes:
					mesh.nodes[node.number] = node
				mesh.elements[element_number] = Element(element_number,None,nodes)
				mesh.elements[element_number].type = 'BEAM2N'

			elif self.gui.new_elements['Element type'] == 'BEAM2N2D':
				if is_3D:
					print('\n\tCannot create BEAM2N2D element with node that has a z-coordinate other than 0.')
					element_created = False
				else:
					print('\n\tNew BEAM2N2D element...')
					if angle != 0:
						moved_nodes = []
						for node in range(len(nodes)):
							if nodes[node].number in moved_nodes:
								pass
							else:
								moved_nodes.append(nodes[node].number)
								point0 = [nodes[node].coord[0][0],
										  nodes[node].coord[1][0],
										  nodes[node].coord[2][0]]
								point1 = rotatePointAboutAxis(point0,start_point,rotation_axis_point2,angle)
								nodes[node].coord[0][0] = point1[0]
								nodes[node].coord[1][0] = point1[1]
								nodes[node].coord[2][0] = point1[2]
					for node in nodes:
						mesh.nodes[node.number] = node
					mesh.elements[element_number] = Element(element_number,None,nodes)
					mesh.elements[element_number].type = 'BEAM2N2D'
				
			elif self.gui.new_elements['Element type'] == 'ROD2N':
				print('\n\tNew ROD2N element...')
				if angle != 0:
					moved_nodes = []
					for node in range(len(nodes)):
						if nodes[node].number in moved_nodes:
							pass
						else:
							moved_nodes.append(nodes[node].number)
							point0 = [nodes[node].coord[0][0],
									  nodes[node].coord[1][0],
									  nodes[node].coord[2][0]]
							point1 = rotatePointAboutAxis(point0,start_point,rotation_axis_point2,angle)
							nodes[node].coord[0][0] = point1[0]
							nodes[node].coord[1][0] = point1[1]
							nodes[node].coord[2][0] = point1[2]
				for node in nodes:
					mesh.nodes[node.number] = node
				mesh.elements[element_number] = Element(element_number,None,nodes)
				mesh.elements[element_number].type = 'ROD2N'

			elif self.gui.new_elements['Element type'] == 'ROD2N2D':
				if is_3D:
					print('\n\tCannot create ROD2N2D element with node that has a z-coordinate other than 0.')
					element_created = False
				else:
					print('\n\tNew ROD2N2D element...')
					if angle != 0:
						moved_nodes = []
						for node in range(len(nodes)):
							if nodes[node].number in moved_nodes:
								pass
							else:
								moved_nodes.append(nodes[node].number)
								point0 = [nodes[node].coord[0][0],
										  nodes[node].coord[1][0],
										  nodes[node].coord[2][0]]
								point1 = rotatePointAboutAxis(point0,start_point,rotation_axis_point2,angle)
								nodes[node].coord[0][0] = point1[0]
								nodes[node].coord[1][0] = point1[1]
								nodes[node].coord[2][0] = point1[2]
					for node in nodes:
						mesh.nodes[node.number] = node
					mesh.elements[element_number] = Element(element_number,None,nodes)
					mesh.elements[element_number].type = 'ROD2N2D'

			elif self.gui.new_elements['Element type'] == 'QUAD4N':
				if is_3D:
					print('\n\tCannot create QUAD4N element with node that has a z-coordinate other than 0.')
					element_created = False
				else:
					print('\n\tNew QUAD4N element...')
					nodes.append(Node(node_number+2, start_point[0]+element_size, start_point[1]+element_size, start_point[2]))
					nodes.append(Node(node_number+3, start_point[0],			  start_point[1]+element_size, start_point[2]))
					if angle != 0:
						moved_nodes = []
						for node in range(len(nodes)):
							if nodes[node].number in moved_nodes:
								pass
							else:
								moved_nodes.append(nodes[node].number)
								point0 = [nodes[node].coord[0][0],
										  nodes[node].coord[1][0],
										  nodes[node].coord[2][0]]
								point1 = rotatePointAboutAxis(point0,start_point,rotation_axis_point2,angle)
								nodes[node].coord[0][0] = point1[0]
								nodes[node].coord[1][0] = point1[1]
								nodes[node].coord[2][0] = point1[2]
					for node in nodes:
						mesh.nodes[node.number] = node
					mesh.elements[element_number] = Element(element_number,None,nodes)
					mesh.elements[element_number].type = 'QUAD4N'

			elif self.gui.new_elements['Element type'] == 'HEX8N':
				print('\n\tNew HEX8N element...')

				nodes.append(Node(node_number+2, start_point[0]+element_size, start_point[1],			   start_point[2]-element_size))
				nodes.append(Node(node_number+3, start_point[0],			  start_point[1], 			   start_point[2]-element_size))
				nodes.append(Node(node_number+4, start_point[0],			  start_point[1]+element_size, start_point[2]))
				nodes.append(Node(node_number+5, start_point[0]+element_size, start_point[1]+element_size, start_point[2]))
				nodes.append(Node(node_number+6, start_point[0]+element_size, start_point[1]+element_size, start_point[2]-element_size))
				nodes.append(Node(node_number+7, start_point[0],			  start_point[1]+element_size, start_point[2]-element_size))
				if angle != 0:
					moved_nodes = []
					for node in range(len(nodes)):
						if nodes[node].number in moved_nodes:
							pass
						else:
							moved_nodes.append(nodes[node].number)
							point0 = [nodes[node].coord[0][0],
									  nodes[node].coord[1][0],
									  nodes[node].coord[2][0]]
							point1 = rotatePointAboutAxis(point0,start_point,rotation_axis_point2,angle)
							nodes[node].coord[0][0] = point1[0]
							nodes[node].coord[1][0] = point1[1]
							nodes[node].coord[2][0] = point1[2]
				for node in nodes:
					mesh.nodes[node.number] = node
				mesh.elements[element_number] = Element(element_number,None,nodes)
				mesh.elements[element_number].type = 'HEX8N'
	
			else:
				print('\n\tUnknown element type:', self.gui.new_elements['Element type'])

		if element_created:
			print('\tNew element:', element_number)
			print('\tElement nodes:', [mesh.elements[element_number].nodes[x].number for x in \
															range(len(mesh.elements[element_number].nodes))])
			x_max = max(mesh.nodes[i].coord[0][0] for i in mesh.nodes)
			x_min = min(mesh.nodes[i].coord[0][0] for i in mesh.nodes)
			y_max = max(mesh.nodes[i].coord[1][0] for i in mesh.nodes)
			y_min = min(mesh.nodes[i].coord[1][0] for i in mesh.nodes)
			z_max = max(mesh.nodes[i].coord[2][0] for i in mesh.nodes)
			z_min = min(mesh.nodes[i].coord[2][0] for i in mesh.nodes)
			mesh.viewScope = {'max': [x_max, y_max, z_max], 'min': [x_min, y_min, z_min]}
			mesh.viewRadius = 1.25*max( (x_max-x_min)/2., (y_max-y_min)/2., (z_max-z_min)/2. )
			self.buildDisplayList(mesh)
			self.gui.new_mesh_view = {'Mesh': self.gui.viewer.currentMesh}
			self.elementOrientation()
			for mesh in self.meshes:
				self.checkForSection(self.meshes[mesh])
			self.gui.viewer.update()


	def elementOrientation(self,newOrientation=False):
		'''
	Applies an orientation to the selected
	elements with input from user. Only applies
	to BEAM2N and BEAM2N2D elements.
	'''
		if self.gui.viewer.currentMesh != 'None':
			mesh = self.meshes[self.gui.viewer.currentMesh]
			if 'orientation' not in mesh.displayLists:
				mesh.displayLists['orientation'] = glGenLists(1)
			glNewList(mesh.displayLists['orientation'], GL_COMPILE)
			for element in mesh.elements:
				if mesh.elements[element].type in ['BEAM2N', 'BEAM2N2D']:
					if element in self.selected_elements and newOrientation:
						x = np.array([float(x.strip()) for x in self.gui.new_orientation['x-vector'].split(',')])
						y = np.array([float(y.strip()) for y in self.gui.new_orientation['y-vector'].split(',')])

						x21 = mesh.elements[element].nodes[1].coord[0][0]-mesh.elements[element].nodes[0].coord[0][0]
						y21 = mesh.elements[element].nodes[1].coord[1][0]-mesh.elements[element].nodes[0].coord[1][0]
						z21 = mesh.elements[element].nodes[1].coord[2][0]-mesh.elements[element].nodes[0].coord[2][0]

						mesh.elements[element].length = sqrt(x21**2 + y21**2 + z21**2)

						x1 = mesh.elements[element].nodes[0].coord[0][0]
						x2 = mesh.elements[element].nodes[1].coord[0][0]
						y1 = mesh.elements[element].nodes[0].coord[1][0]
						y2 = mesh.elements[element].nodes[1].coord[1][0]
						z1 = mesh.elements[element].nodes[0].coord[2][0]
						z2 = mesh.elements[element].nodes[1].coord[2][0]

						if x21 < 0. and x[0] < 0.:
							xv = np.array([x21, y21, z21])
						elif x21 > 0. and x[0] > 0.:
							xv = np.array([x21, y21, z21])
						else:
							# if node order not alligned with beam orientation,
							# switch nodes 1 and 2 to allign them
							mesh.elements[element].nodes[0], mesh.elements[element].nodes[1] = mesh.elements[element].nodes[1], mesh.elements[element].nodes[0]
							x21 = mesh.elements[element].nodes[1].coord[0][0]-mesh.elements[element].nodes[0].coord[0][0]
							y21 = mesh.elements[element].nodes[1].coord[1][0]-mesh.elements[element].nodes[0].coord[1][0]
							z21 = mesh.elements[element].nodes[1].coord[2][0]-mesh.elements[element].nodes[0].coord[2][0]
							xv = np.array([x21, y21, z21])
							x1 = mesh.elements[element].nodes[0].coord[0][0]
							x2 = mesh.elements[element].nodes[1].coord[0][0]
							y1 = mesh.elements[element].nodes[0].coord[1][0]
							y2 = mesh.elements[element].nodes[1].coord[1][0]
							z1 = mesh.elements[element].nodes[0].coord[2][0]
							z2 = mesh.elements[element].nodes[1].coord[2][0]

						xu = xv/mesh.elements[element].length
						yu = y/np.sqrt(y[0]**2+y[1]**2+y[2]**2)
						if xu.dot(yu) in [-1.,1.]:
							print('\n\tWARNING!!! Element', mesh.elements[element].number)
							print('\ty-vector cannot be the same as vector from node 1 to node 2.')
							print('\tChanging it to be perpendicular to x-vector')
							y = np.array([np.random.rand(),np.random.rand(),np.random.rand()]) 
						n1_offset = np.array([x1,y1,z1]) + y
						n2_offset = np.array([x2,y2,z2]) + y
						n_offset = n1_offset + 0.5*(n2_offset-n1_offset)
						ov = n_offset - np.array([x1,y1,z1])
						yv = ov - np.dot(ov,xu)*xu
						mag = sqrt(yv[0]**2 + yv[1]**2 + yv[2]**2)
						if mag == 0.:
							yu = yv
						else:
							yu = yv/mag
						if mesh.elements[element].type == 'BEAM2N2D':
							zu = np.array([0.,0.,1.])
							yu = np.cross(zu, xu)
						else:
							zu = np.cross(xu, yu)
						mesh.elements[element].orientation = {'x-vec': xu, 'y-vec': yu, 'z-vec': zu}

					if hasattr(mesh.elements[element],'orientation'):
						xu = mesh.elements[element].orientation['x-vec']
						yu = mesh.elements[element].orientation['y-vec']
						zu = mesh.elements[element].orientation['z-vec']
						x0 = (mesh.elements[element].nodes[1].coord[0][0] + mesh.elements[element].nodes[0].coord[0][0])/2. + yu[0]*0.01*mesh.elements[element].length
						y0 = (mesh.elements[element].nodes[1].coord[1][0] + mesh.elements[element].nodes[0].coord[1][0])/2. + yu[1]*0.01*mesh.elements[element].length
						z0 = (mesh.elements[element].nodes[1].coord[2][0] + mesh.elements[element].nodes[0].coord[2][0])/2. + yu[2]*0.01*mesh.elements[element].length
						scale = 0.15*mesh.elements[element].length
						glColor(1.0, 0.0, 0.0)
						glBegin(GL_LINES)
						glVertex(x0,y0,z0)
						glVertex(x0+xu[0]*scale,y0+xu[1]*scale,z0+xu[2]*scale)
						glEnd()
						glColor(0.0, 1.0, 0.0)
						glBegin(GL_LINES)
						glVertex(x0,y0,z0)
						glVertex(x0+yu[0]*scale,y0+yu[1]*scale,z0+yu[2]*scale)
						glEnd()
						glColor(0.0, 0.0, 1.0)
						glBegin(GL_LINES)
						glVertex(x0,y0,z0)
						glVertex(x0+zu[0]*scale,y0+zu[1]*scale,z0+zu[2]*scale)
						glEnd()
			glEndList()
			self.gui.viewer.currentDisplayList['displaylist']['orientation'] = mesh.displayLists['orientation']


	def elementConversion(self):
		'''
	Takes an element and converts it from one type
	to another type, or several of another type.
	Conversions: 1 HEX8N    --> 1 HEX20N
				 1 HEX8N    --> 4 TET4N
				 1 HEX8N    --> 4 TET10N
				 1 HEX20N   --> 4 TET10N
				 1 TET4N    --> 1 TET10N
				 1 QUAD4N   --> 1 QUAD8N
				 1 QUAD4N   --> 2 TRI3N
				 1 QUAD4N   --> 2 TRI6N
				 1 QUAD8N	--> 2 TRI6N
				 1 TRI4N    --> 1 TRI6N
				 1 ROD2N    --> 1 BEAM2N
				 1 BEAM2N   --> 1 ROD2N
				 1 ROD2N2D  --> 1 BEAM2N2D
				 1 BEAM2N2D --> 1 ROD2N2D
	'''
		mesh = self.meshes[self.gui.viewer.currentMesh]
		element_type = None
		new_element_type = self.gui.new_conversion['Element type']
		for element in self.selected_elements:
			element_type = mesh.elements[element].type
			break
		print('\n\tConverting selected elements from '+element_type+' to '+new_element_type+'...', end=' ')
		edge_nodes = []
		nodes_between = {}
		if element_type == 'HEX8N':
			if new_element_type == 'HEX20N':
				# (1,2) -->  9, (2,3) --> 10, (3,4) --> 11, (1,4) --> 12, (1,5) --> 13, (2,6) --> 14
				# (3,7) --> 15, (4,8) --> 16, (5,6) --> 17, (6,7) --> 18, (7,8) --> 19, (5,8) --> 20
				edge_nodes = [(0,1), (1,2), (2,3), (0,3), (0,4), (1,5),
							  (2,6), (3,7), (4,5), (5,6), (6,7), (4,7)]
			elif new_element_type == 'TET4N':
				# no edges divided
				edge_nodes = []
			else:
				# (1,2) -->  9, (2,3) --> 10, (3,4) --> 11, (1,4) --> 12, (1,5) --> 13, (2,6) --> 14
				# (3,7) --> 15, (4,8) --> 16, (5,6) --> 17, (6,7) --> 18, (7,8) --> 19, (5,8) --> 20
				# (1,3) --> 21, (1,6) --> 22, (3,6) --> 23, (3,8) --> 24, (1,8) --> 25, (6,8) --> 26
				edge_nodes = [(0,1), (1,2), (2,3), (0,3), (0,4), (1,5),
							  (2,6), (3,7), (4,5), (5,6), (6,7), (4,7),
							  (0,2), (0,5), (2,5), (2,7), (0,7), (5,7)]
		elif element_type == 'HEX20N':
			# (1,3) --> 21, (1,6) --> 22, (3,6) --> 23, (3,8) --> 24, (1,8) --> 25, (6,8) --> 26
			edge_nodes = [(0,2), (0,5), (2,5), (2,7), (0,7), (5,7)]
		elif element_type == 'TET4N':
			# (1,2) -->  5, (2,3) --> 6, (1,3) --> 7, (1,4) --> 8, (2,4) --> 9, (3,4) --> 10
			edge_nodes = [(0,1), (1,2), (0,2), (0,3), (1,3), (2,3)]
		elif element_type == 'QUAD4N':
			if new_element_type == 'QUAD8N':
				# (1,2) -->  5, (2,3) --> 6, (3,4) --> 7, (1,4) --> 8
				edge_nodes = [(0,1), (1,2), (2,3), (0,3)]
			elif new_element_type == 'TRI3N':
				# no edges divided
				edge_nodes = []
			else:
				# (1,2) -->  5, (2,3) --> 6, (3,4) --> 7, (1,4) --> 8, (2,4) --> 9
				edge_nodes = [(0,1), (1,2), (2,3), (0,3), (1,3)]
		elif element_type == 'QUAD8N':
			# (3,7) -->  9
			edge_nodes = [(2,6)]
		elif element_type == 'TRI3N':
			# (1,2) -->  4, (2,3) --> 5, (1,3) --> 6
			edge_nodes = [(0,1), (1,2), (0,2)]
		elif element_type in ['BEAM2N', 'BEAM2N2D', 'ROD2N', 'ROD2N2D']:
			pass
		else:
			print('\n\tFunctionality not written for this element type yet')

		for element in self.selected_elements:
			for edge in range(len(edge_nodes)):
				if tuple(sorted([mesh.elements[element].nodes[edge_nodes[edge][0]].number,
								 mesh.elements[element].nodes[edge_nodes[edge][1]].number])) in nodes_between:
					mesh.elements[element].nodes.append(mesh.nodes[nodes_between[tuple(sorted([mesh.elements[element].nodes[edge_nodes[edge][0]].number,
																		mesh.elements[element].nodes[edge_nodes[edge][1]].number]))]])
				else:
					mesh.nodes[max(mesh.nodes)+1] = Node(max(mesh.nodes)+1,
					 (mesh.elements[element].nodes[edge_nodes[edge][0]].coord[0][0]+mesh.elements[element].nodes[edge_nodes[edge][1]].coord[0][0])/2.,
					 (mesh.elements[element].nodes[edge_nodes[edge][0]].coord[1][0]+mesh.elements[element].nodes[edge_nodes[edge][1]].coord[1][0])/2.,
					 (mesh.elements[element].nodes[edge_nodes[edge][0]].coord[2][0]+mesh.elements[element].nodes[edge_nodes[edge][1]].coord[2][0])/2.)
					nodes_between[tuple(sorted([mesh.elements[element].nodes[edge_nodes[edge][0]].number,
												mesh.elements[element].nodes[edge_nodes[edge][1]].number]))] = max(mesh.nodes)
					mesh.elements[element].nodes.append(mesh.nodes[max(mesh.nodes)])
			if element_type in ['BEAM2N', 'ROD2N']:
				mesh.elements[element].type = new_element_type
			elif element_type in ['BEAM2N2D', 'ROD2N2D']:
				mesh.elements[element].type = new_element_type
			elif element_type == 'QUAD4N':
				if new_element_type == 'QUAD8N':
					rearrange = [0,4,1,5,2,6,3,7]
					mesh.elements[element].nodes = [mesh.elements[element].nodes[i] for i in rearrange]
					mesh.elements[element].type = 'QUAD8N'
				else:
					rearrange = []
					if new_element_type == 'TRI3N':
						rearrange = [[0,1,3],[1,2,3]]
					else:
						rearrange = [[0,1,3,4,8,7],[1,2,3,5,6,8]]
					new_element_number = max(mesh.elements)+1
					mesh.elements[new_element_number] = Element(new_element_number,None,mesh.elements[element].nodes)
					mesh.elements[new_element_number].type = new_element_type
					mesh.elements[new_element_number].nodes = [mesh.elements[element].nodes[i] for i in rearrange[1]]
					mesh.elements[element].nodes = [mesh.elements[element].nodes[i] for i in rearrange[0]]
					mesh.elements[element].type = new_element_type
			elif element_type == 'QUAD8N':
				rearrange = [[0,2,6,1,8,7],[2,4,6,3,5,8]]
				new_element_number = max(mesh.elements)+1
				mesh.elements[new_element_number] = Element(new_element_number,None,mesh.elements[element].nodes)
				mesh.elements[new_element_number].type = new_element_type
				mesh.elements[new_element_number].nodes = [mesh.elements[element].nodes[i] for i in rearrange[1]]
				mesh.elements[element].nodes = [mesh.elements[element].nodes[i] for i in rearrange[0]]
				mesh.elements[element].type = new_element_type
			elif element_type == 'TRI3N':
				mesh.elements[element].type = 'TRI6N'
			elif element_type == 'HEX8N':
				if new_element_type == 'HEX20N':
					mesh.elements[element].type = 'HEX20N'
				else:
					rearrange = []
					if new_element_type == 'TET4N':
						rearrange = [[0,1,2,5],[0,2,3,7],[0,4,5,7],[2,5,6,7],[0,5,2,7]]
					else:
						rearrange = [[0,1,2,5,8,9,20,21,13,22],[0,2,3,7,20,10,11,24,23,15],
									 [0,4,5,7,12,16,21,24,19,25],[2,5,6,7,22,17,14,23,25,18],
									 [0,5,2,7,21,22,20,24,25,23]]
					for elm in range(4):
						new_element_number = max(mesh.elements)+1
						mesh.elements[new_element_number] = Element(new_element_number,None,mesh.elements[element].nodes)
						mesh.elements[new_element_number].type = new_element_type
						mesh.elements[new_element_number].nodes = [mesh.elements[element].nodes[i] for i in rearrange[elm+1]]
					mesh.elements[element].nodes = [mesh.elements[element].nodes[i] for i in rearrange[0]]
					mesh.elements[element].type = new_element_type
			elif element_type == 'HEX20N':
					rearrange = [[0,1,2,5,8,9,20,21,13,22],[0,2,3,7,20,10,11,24,23,15],
								 [0,4,5,7,12,16,21,24,19,25],[2,5,6,7,22,17,14,23,25,18],
								 [0,5,2,7,21,22,20,24,25,23]]
					for elm in range(4):
						new_element_number = max(mesh.elements)+1
						mesh.elements[new_element_number] = Element(new_element_number,None,mesh.elements[element].nodes)
						mesh.elements[new_element_number].type = 'TET10N'
						mesh.elements[new_element_number].nodes = [mesh.elements[element].nodes[i] for i in rearrange[elm+1]]
					mesh.elements[element].nodes = [mesh.elements[element].nodes[i] for i in rearrange[0]]
					mesh.elements[element].type = 'TET10N'
			elif element_type == 'TET4N':
				mesh.elements[element].type = 'TET10N'
			else:
				print('\n\tSOMETHING WENT WRONG!!!\n', element_type, 'cannot convert to', new_element_type)

		self.buildDisplayList(mesh)
		self.gui.new_mesh_view = {'Mesh': self.gui.viewer.currentMesh}
		self.elementOrientation()
		self.gui.viewer.update()
		print('finished.')


	def createNewExtrusion(self):
		'''
	Extrudes new elements from existing elements
	as specified by user input.
	'''
		elements = []
		mesh = self.meshes[self.gui.viewer.currentMesh]
		if self.gui.new_extrusion['Extrude direction'] == self.gui.new_extrusion['Extrude angle axis'] and self.gui.new_extrusion['Extrude scenario'] == 'angled':
			print('\n\tExtrude direction cannot be the same as Extrude angle axis')
		elif self.gui.new_extrusion['Element type'] in ['BEAM2N', 'BEAM2N2D', 'ROD2N', 'ROD2N2D', 'QUAD4N', 'HEX8N']:
			print('\n\tExtruding new element(s):',end=' ')
			# first find the four nodes in each element
			# that lie furthest in the extrude direction
			# by using a coordinate system set in the
			# middle of the selected element
			# then create four new nodes from those four
			# nodes, or less if any of them have already
			# been extruded
			# finally create a new element with the first
			# four nodes and the four new nodes
			extr_dir = self.gui.new_extrusion['Extrude direction'].split(',')
			extr_dir = np.array([float(extr_dir[0]), float(extr_dir[1]), float(extr_dir[2])])
			extr_dir /= np.linalg.norm(extr_dir)
			x_axis = Vector3D(extr_dir[0],extr_dir[1],extr_dir[2])
			y_axis = Vector3D(0,0,0)
			r_angle = np.radians(float(self.gui.new_extrusion['Extrude angle']))/int(self.gui.new_extrusion['Extrude number'])
			r_axis = self.gui.new_extrusion['Extrude angle axis'].split(',')
			r_axis = np.array([float(r_axis[0]), float(r_axis[1]), float(r_axis[2])])
			r_axis /= np.linalg.norm(r_axis)
			if self.gui.new_extrusion['Element type'] in ['BEAM2N2D', 'ROD2N2D', 'QUAD4N']:
				if r_axis[0] != 0. or r_axis[1] != 0:
					r_axis = np.array([0,0,1])
					print('\n\t2D elements can only rotate around z-axis,')
					print('\tmeaning [0,0,-1] or [0,0,1]')
					print('\tRotation axis changed to [0,0,1]')
			r_radius = float(self.gui.new_extrusion['Extrude angle radius'])
			rot_origin = False
			rot_axis_point0 = False
			rot_axis_point1 = False
			elm_size = None
			extr_num_check = None
			for extr_num in range(int(self.gui.new_extrusion['Extrude number'])):
				elm_extr_nodes = {}
				extruded_elements = {}
				for element in self.selected_elements:
					elm_extr_nodes[element] = []
					x_min = y_min = z_min = x_max = y_max = z_max = None
					for node in mesh.elements[element].nodes:
						if x_min == None:
							x_min = node.coord[0][0]
							y_min = node.coord[1][0]
							z_min = node.coord[2][0]
							x_max = node.coord[0][0]
							y_max = node.coord[1][0]
							z_max = node.coord[2][0]
						else:
							if x_min > node.coord[0][0]:
								x_min = node.coord[0][0]
							if x_max < node.coord[0][0]:
								x_max = node.coord[0][0]
							if y_min > node.coord[1][0]:
								y_min = node.coord[1][0]
							if y_max < node.coord[1][0]:
								y_max = node.coord[1][0]
							if z_min > node.coord[2][0]:
								z_min = node.coord[2][0]
							if z_max < node.coord[2][0]:
								z_max = node.coord[2][0]
					origin = Point3D(x_min+(x_max-x_min)/2., y_min+(y_max-y_min)/2., z_min+(z_max-z_min)/2.)
					
					if extr_num_check != extr_num:
						extr_num_check = extr_num
						quat_x_axis = Quaternion()
						quat_x_axis.vectorToQuat(x_axis.coordinates)
						r_quat = Quaternion()
						r_quat.axisAngleToQuat(r_axis, r_angle)
						quat_new_dir = r_quat.multi(quat_x_axis.multi(r_quat.conj()))
						x_axis = np.array([quat_new_dir.i, quat_new_dir.j, quat_new_dir.k])
						x_axis /= np.linalg.norm(extr_dir)
						y_axis = np.random.randn(3)
						y_axis -= y_axis.dot(x_axis)*x_axis
						x_axis /= np.linalg.norm(x_axis)
						x_axis = Vector3D(x_axis[0],x_axis[1],x_axis[2])
						y_axis /= np.linalg.norm(y_axis)
						y_axis = Vector3D(y_axis[0],y_axis[1],y_axis[2])
					elm_center_csys = CoordSys3D(origin, x_axis, y_axis)
					for node in mesh.elements[element].nodes:
						if elm_center_csys.mapFrom(self.gui.viewer.coordSys0,Point3D(node.coord[0][0],node.coord[1][0],node.coord[2][0])).x() > 0:
							elm_extr_nodes[element].append([node.number,mesh.elements[element].nodes.index(node)])
							if float(self.gui.new_extrusion['Extrude angle']) != 0.:
								if rot_origin == False:
									rot_origin = True
									radius_vect = np.cross(r_axis,extr_dir)
									radius_vect /= np.linalg.norm(radius_vect)
									rot_axis_point0 = [mesh.nodes[node.number].coord[0][0]+radius_vect[0]*r_radius,
													   mesh.nodes[node.number].coord[1][0]+radius_vect[1]*r_radius,
													   mesh.nodes[node.number].coord[2][0]+radius_vect[2]*r_radius]
									rot_axis_point1 = [rot_axis_point0[0]+r_axis[0],
													   rot_axis_point0[1]+r_axis[1],
													   rot_axis_point0[2]+r_axis[2]]
				extr_nodes = {}
				if float(self.gui.new_extrusion['Extrude angle']) == 0.:
					for element in elm_extr_nodes:
						if elm_size == None:
							elm_size = np.sqrt((mesh.elements[element].nodes[1].coord[0][0] - mesh.elements[element].nodes[0].coord[0][0])**2 + \
											   (mesh.elements[element].nodes[1].coord[1][0] - mesh.elements[element].nodes[0].coord[1][0])**2 + \
											   (mesh.elements[element].nodes[1].coord[2][0] - mesh.elements[element].nodes[0].coord[2][0])**2)
						elm_nodes = elm_extr_nodes[element]
						for node in range(len(elm_extr_nodes[element])):
							if elm_extr_nodes[element][node][0] not in extr_nodes:
								extr_nodes[elm_extr_nodes[element][node][0]] = max(mesh.nodes)+1
								mesh.nodes[extr_nodes[elm_extr_nodes[element][node][0]]] = Node(extr_nodes[elm_extr_nodes[element][node][0]],
																							 mesh.nodes[elm_extr_nodes[element][node][0]].coord[0][0] + elm_size*extr_dir[0],
																							 mesh.nodes[elm_extr_nodes[element][node][0]].coord[1][0] + elm_size*extr_dir[1],
																							 mesh.nodes[elm_extr_nodes[element][node][0]].coord[2][0] + elm_size*extr_dir[2])
								elm_nodes.append([extr_nodes[elm_extr_nodes[element][node][0]],elm_extr_nodes[element][node][1]])
							else:
								elm_nodes.append([extr_nodes[elm_extr_nodes[element][node][0]],elm_extr_nodes[element][node][1]])

						if self.gui.new_extrusion['Element type'] == 'HEX8N':
							new_node_internal = [elm_extr_nodes[element][i][1] for i in range(4)]
							# index the nodes inside the element
							# by using the fact that node X with
							# index I in the old element will 
							# extrude to node Y with index I in
							# the new element. node X in the new
							# element can only be extruded from
							# one of three nodes on the old element,
							# which means node X can only have one
							# of three index locations in the new
							# element. Two of these will be occupied
							# already by the other extruded nodes,
							# leaving one possible index location
							# for node X in the new element.
							for node in range(4):
								internal = None
								if elm_extr_nodes[element][node][1] == 0:
									# 1, 3 or 4
									if 1 not in new_node_internal:
										internal = 1
									elif 3 not in new_node_internal:
										internal = 3
									elif 4 not in new_node_internal:
										internal = 4								
								if elm_extr_nodes[element][node][1] == 1:
									# 0, 2 or 5
									if 0 not in new_node_internal:
										internal = 0
									elif 2 not in new_node_internal:
										internal = 2
									elif 5 not in new_node_internal:
										internal = 5
								if elm_extr_nodes[element][node][1] == 2:
									# 1, 3 or 6
									if 1 not in new_node_internal:
										internal = 1
									elif 3 not in new_node_internal:
										internal = 3
									elif 6 not in new_node_internal:
										internal = 6
								if elm_extr_nodes[element][node][1] == 3:
									# 0, 2 or 7
									if 0 not in new_node_internal:
										internal = 0
									elif 2 not in new_node_internal:
										internal = 2
									elif 7 not in new_node_internal:
										internal = 7
								if elm_extr_nodes[element][node][1] == 4:
									# 0, 5 or 7
									if 0 not in new_node_internal:
										internal = 0
									elif 5 not in new_node_internal:
										internal = 5
									elif 7 not in new_node_internal:
										internal = 7
								if elm_extr_nodes[element][node][1] == 5:
									# 1, 4 or 6
									if 1 not in new_node_internal:
										internal = 1
									elif 4 not in new_node_internal:
										internal = 4
									elif 6 not in new_node_internal:
										internal = 6
								if elm_extr_nodes[element][node][1] == 6:
									# 2, 5 or 7
									if 2 not in new_node_internal:
										internal = 2
									elif 5 not in new_node_internal:
										internal = 5
									elif 7 not in new_node_internal:
										internal = 7
								if elm_extr_nodes[element][node][1] == 7:
									# 3, 4 or 6
									if 3 not in new_node_internal:
										internal = 3
									elif 4 not in new_node_internal:
										internal = 4
									elif 6 not in new_node_internal:
										internal = 6
								elm_extr_nodes[element][node][1] = internal
							new_node_order = {}
							for node in range(8):
								new_node_order[elm_extr_nodes[element][node][1]] = elm_extr_nodes[element][node][0]
							for node in new_node_order:
								elm_nodes[node] = mesh.nodes[new_node_order[node]]
													
							elm_num = max(mesh.elements)+1
							elements.append(elm_num)
							mesh.elements[elm_num] = Element(elm_num,None,elm_nodes)
							mesh.elements[elm_num].type = 'HEX8N'
							extruded_elements[elm_num] = mesh.elements[elm_num]

						elif self.gui.new_extrusion['Element type'] in ['BEAM2N', 'BEAM2N2D', 'ROD2N', 'ROD2N2D']:
							for node in range(2):
								elm_nodes[node] = mesh.nodes[elm_nodes[node][0]]
							elm_num = max(mesh.elements)+1
							elements.append(elm_num)
							mesh.elements[elm_num] = Element(elm_num,None,elm_nodes)
							mesh.elements[elm_num].type = self.gui.new_extrusion['Element type']
							extruded_elements[elm_num] = mesh.elements[elm_num]
						
						else:
							new_node_internal = [elm_extr_nodes[element][i][1] for i in range(2)]
							# index the nodes inside the element
							# by using the fact that node A with
							# index I in the old element will 
							# extrude to node B with index I in
							# the new element. node A in the new
							# element can only be extruded from
							# one of two nodes on the old element,
							# which means node B can only have one
							# of two index locations in the new
							# element. One of these will be occupied
							# already by the other extruded node,
							# leaving one possible index location
							# for node A in the new element.
							for node in range(2):
								internal = None
								if elm_extr_nodes[element][node][1] == 0:
									# 2 or 4
									if 1 not in new_node_internal:
										internal = 1
									elif 3 not in new_node_internal:
										internal = 3								
								if elm_extr_nodes[element][node][1] == 1:
									# 1 or 3
									if 0 not in new_node_internal:
										internal = 0
									elif 2 not in new_node_internal:
										internal = 2
								if elm_extr_nodes[element][node][1] == 2:
									# 2 or 4
									if 1 not in new_node_internal:
										internal = 1
									elif 3 not in new_node_internal:
										internal = 3
								if elm_extr_nodes[element][node][1] == 3:
									# 1 or 3
									if 0 not in new_node_internal:
										internal = 0
									elif 2 not in new_node_internal:
										internal = 2
								elm_extr_nodes[element][node][1] = internal
							new_node_order = {}
							for node in range(4):
								new_node_order[elm_extr_nodes[element][node][1]] = elm_extr_nodes[element][node][0]
							for node in new_node_order:
								elm_nodes[node] = mesh.nodes[new_node_order[node]]

							elm_num = max(mesh.elements)+1
							elements.append(elm_num)
							mesh.elements[elm_num] = Element(elm_num,None,elm_nodes)
							mesh.elements[elm_num].type = 'QUAD4N'
							extruded_elements[elm_num] = mesh.elements[elm_num]
							
				else:
					# extrude with angle
					# recalculate extrude direction
					# for every increment
					quat_extr_dir = Quaternion()
					quat_extr_dir.vectorToQuat(extr_dir)

					r_quat = Quaternion()
					r_quat.axisAngleToQuat(r_axis, r_angle)
					quat_new_dir = r_quat.multi(quat_extr_dir.multi(r_quat.conj()))
					extr_dir = np.array([quat_new_dir.i, quat_new_dir.j, quat_new_dir.k])
					extr_dir /= np.linalg.norm(extr_dir)
					for element in elm_extr_nodes:
						if elm_size == None:
							elm_size = np.sqrt((mesh.elements[element].nodes[1].coord[0][0] - mesh.elements[element].nodes[0].coord[0][0])**2 + \
											   (mesh.elements[element].nodes[1].coord[1][0] - mesh.elements[element].nodes[0].coord[1][0])**2 + \
											   (mesh.elements[element].nodes[1].coord[2][0] - mesh.elements[element].nodes[0].coord[2][0])**2)
						elm_nodes = elm_extr_nodes[element]
						for node in range(len(elm_extr_nodes[element])):
							if elm_extr_nodes[element][node][0] not in extr_nodes:
								# use quaternions to create new nodes by
								# rotating the old nodes around the radius
								# and rotation axis specified by the user
								# (rot_axis_point0 and rot_axis_point1)
								extr_nodes[elm_extr_nodes[element][node][0]] = max(mesh.nodes)+1
								point0 = [mesh.nodes[elm_extr_nodes[element][node][0]].coord[0][0],
										  mesh.nodes[elm_extr_nodes[element][node][0]].coord[1][0],
										  mesh.nodes[elm_extr_nodes[element][node][0]].coord[2][0]]
								point1 = rotatePointAboutAxis(point0,rot_axis_point0,rot_axis_point1,r_angle)
								mesh.nodes[extr_nodes[elm_extr_nodes[element][node][0]]] = Node(extr_nodes[elm_extr_nodes[element][node][0]], point1[0], point1[1], point1[2])
								elm_nodes.append([extr_nodes[elm_extr_nodes[element][node][0]],elm_extr_nodes[element][node][1]])
							else:
								elm_nodes.append([extr_nodes[elm_extr_nodes[element][node][0]],elm_extr_nodes[element][node][1]])

						if self.gui.new_extrusion['Element type'] == 'HEX8N':
							new_node_internal = [elm_extr_nodes[element][i][1] for i in range(4)]
							# index the nodes inside the element
							# by using the fact that node X with
							# index I in the old element will 
							# extrude to node Y with index I in
							# the new element. node X in the new
							# element can only be extruded from
							# one of three nodes on the old element,
							# which means node X can only have one
							# of three index locations in the new
							# element. Two of these will be occupied
							# already by the other extruded nodes,
							# leaving one possible index location
							# for node X in the new element.
							for node in range(4):
								internal = None
								if elm_extr_nodes[element][node][1] == 0:
									# 1, 3 or 4
									if 1 not in new_node_internal:
										internal = 1
									elif 3 not in new_node_internal:
										internal = 3
									elif 4 not in new_node_internal:
										internal = 4								
								if elm_extr_nodes[element][node][1] == 1:
									# 0, 2 or 5
									if 0 not in new_node_internal:
										internal = 0
									elif 2 not in new_node_internal:
										internal = 2
									elif 5 not in new_node_internal:
										internal = 5
								if elm_extr_nodes[element][node][1] == 2:
									# 1, 3 or 6
									if 1 not in new_node_internal:
										internal = 1
									elif 3 not in new_node_internal:
										internal = 3
									elif 6 not in new_node_internal:
										internal = 6
								if elm_extr_nodes[element][node][1] == 3:
									# 0, 2 or 7
									if 0 not in new_node_internal:
										internal = 0
									elif 2 not in new_node_internal:
										internal = 2
									elif 7 not in new_node_internal:
										internal = 7
								if elm_extr_nodes[element][node][1] == 4:
									# 0, 5 or 7
									if 0 not in new_node_internal:
										internal = 0
									elif 5 not in new_node_internal:
										internal = 5
									elif 7 not in new_node_internal:
										internal = 7
								if elm_extr_nodes[element][node][1] == 5:
									# 1, 4 or 6
									if 1 not in new_node_internal:
										internal = 1
									elif 4 not in new_node_internal:
										internal = 4
									elif 6 not in new_node_internal:
										internal = 6
								if elm_extr_nodes[element][node][1] == 6:
									# 2, 5 or 7
									if 2 not in new_node_internal:
										internal = 2
									elif 5 not in new_node_internal:
										internal = 5
									elif 7 not in new_node_internal:
										internal = 7
								if elm_extr_nodes[element][node][1] == 7:
									# 3, 4 or 6
									if 3 not in new_node_internal:
										internal = 3
									elif 4 not in new_node_internal:
										internal = 4
									elif 6 not in new_node_internal:
										internal = 6
								elm_extr_nodes[element][node][1] = internal
							new_node_order = {}
							for node in range(8):
								new_node_order[elm_extr_nodes[element][node][1]] = elm_extr_nodes[element][node][0]
							for node in new_node_order:
								elm_nodes[node] = mesh.nodes[new_node_order[node]]

							elm_num = max(mesh.elements)+1
							elements.append(elm_num)
							mesh.elements[elm_num] = Element(elm_num,None,elm_nodes)
							mesh.elements[elm_num].type = 'HEX8N'
							extruded_elements[elm_num] = mesh.elements[elm_num]


						elif self.gui.new_extrusion['Element type'] in ['BEAM2N', 'BEAM2N2D', 'ROD2N', 'ROD2N2D']:
							for node in range(2):
								elm_nodes[node] = mesh.nodes[elm_nodes[node][0]]
							elm_num = max(mesh.elements)+1
							elements.append(elm_num)
							mesh.elements[elm_num] = Element(elm_num,None,elm_nodes)
							mesh.elements[elm_num].type = self.gui.new_extrusion['Element type']
							extruded_elements[elm_num] = mesh.elements[elm_num]
						
						else:
							new_node_internal = [elm_extr_nodes[element][i][1] for i in range(2)]
							# index the nodes inside the element
							# by using the fact that node A with
							# index I in the old element will 
							# extrude to node B with index I in
							# the new element. node A in the new
							# element can only be extruded from
							# one of two nodes on the old element,
							# which means node B can only have one
							# of two index locations in the new
							# element. One of these will be occupied
							# already by the other extruded node,
							# leaving one possible index location
							# for node A in the new element.
							for node in range(2):
								internal = None
								if elm_extr_nodes[element][node][1] == 0:
									# 2 or 4
									if 1 not in new_node_internal:
										internal = 1
									elif 3 not in new_node_internal:
										internal = 3								
								if elm_extr_nodes[element][node][1] == 1:
									# 1 or 3
									if 0 not in new_node_internal:
										internal = 0
									elif 2 not in new_node_internal:
										internal = 2
								if elm_extr_nodes[element][node][1] == 2:
									# 2 or 4
									if 1 not in new_node_internal:
										internal = 1
									elif 3 not in new_node_internal:
										internal = 3
								if elm_extr_nodes[element][node][1] == 3:
									# 1 or 3
									if 0 not in new_node_internal:
										internal = 0
									elif 2 not in new_node_internal:
										internal = 2
								elm_extr_nodes[element][node][1] = internal
							new_node_order = {}
							for node in range(4):
								new_node_order[elm_extr_nodes[element][node][1]] = elm_extr_nodes[element][node][0]
							for node in new_node_order:
								elm_nodes[node] = mesh.nodes[new_node_order[node]]

							elm_num = max(mesh.elements)+1
							elements.append(elm_num)
							mesh.elements[elm_num] = Element(elm_num,None,elm_nodes)
							mesh.elements[elm_num].type = 'QUAD4N'
							extruded_elements[elm_num] = mesh.elements[elm_num]

				self.selected_elements = extruded_elements
				
		else:
			print('\n\tCannot extrude this element type:', self.gui.new_extrusion['Element type'])

		x_max = max(mesh.nodes[i].coord[0][0] for i in mesh.nodes )
		x_min = min(mesh.nodes[i].coord[0][0] for i in mesh.nodes )
		y_max = max(mesh.nodes[i].coord[1][0] for i in mesh.nodes )
		y_min = min(mesh.nodes[i].coord[1][0] for i in mesh.nodes )
		z_max = max(mesh.nodes[i].coord[2][0] for i in mesh.nodes )
		z_min = min(mesh.nodes[i].coord[2][0] for i in mesh.nodes )
		mesh.viewScope = {'max': [x_max, y_max, z_max], 'min': [x_min, y_min, z_min]}
		mesh.viewRadius = 1.25*max( (x_max-x_min)/2., (y_max-y_min)/2., (z_max-z_min)/2. )
		self.buildDisplayList(mesh)
		self.gui.new_mesh_view = {'Mesh': self.gui.viewer.currentMesh}
		self.elementOrientation()
		for mesh in self.meshes:
			self.checkForSection(self.meshes[mesh])
		self.gui.viewer.update()

		if len(elements) == 0:
			pass
		elif len(elements) < 9:
			print(elements)
		else:
			print('['+str(elements[0])+', ... '+str(elements[-1])+']')


	def moveElements(self):
		'''
	Moves all elements in specified elementset
	to new position given by user input.
	'''
		if self.gui.viewer.currentMesh == 'None':
			print('\n\tNo mesh currently selected.')
		elif self.elementsSelected:
			mesh = self.meshes[self.gui.viewer.currentMesh]
			try:
				x = float(self.gui.new_position['x-direction'])
				y = float(self.gui.new_position['y-direction'])
				z = float(self.gui.new_position['z-direction'])
			except ValueError:
				print('\n\tx, y and z directions must be floats')
			else:
				self.selected_nodes.clear()
				for element in self.selected_elements:
					for node in self.selected_elements[element].nodes:
						if node.number not in self.selected_nodes:
							self.selected_nodes[node.number] = node
				self.nodesSelected = True
				self.moveSelectedNodes(x, y, z)
				self.elementsSelected = False
				self.selected_elements.clear()
				self.gui.viewer.update()
		else:
			print('\n\tNo elements currently selected.')


	def rotateElements(self):
		'''
	Rotates all elements in specified elementset
	around axis given by user input to new position.
	'''
		if self.gui.viewer.currentMesh == 'None':
			print('\n\tNo mesh currently selected.')
			print('\tNo elements moved.')
		elif self.elementsSelected:
			try:
				node1 = int(self.gui.new_rotation['Rotation axis node 1\n(uses only this if 2D elements)'])
				angle = np.radians(float(self.gui.new_rotation['Angle']))
			except ValueError:
				print('\n\tRotation axis node 1 must be an integer')
				print('\tand the angle must be float.')
			else:
				is2d = False
				for element in self.selected_elements:
					if self.selected_elements[element].type in ['ROD2N2D', 'BEAM2N2D', 'TRI3N', 'TRI6N', 'QUAD4N', 'QUAD8N']:
						is2d = True
						break

				mesh = self.meshes[self.gui.viewer.currentMesh]
				if is2d:
					if node1 in mesh.nodes:
						node1_coord = [mesh.nodes[node1].coord[0][0],
									   mesh.nodes[node1].coord[1][0],
									   mesh.nodes[node1].coord[2][0]]
						node2_coord = [mesh.nodes[node1].coord[0][0],
									   mesh.nodes[node1].coord[1][0],
									   mesh.nodes[node1].coord[2][0]+1]
						moved_nodes = []
						for element in self.selected_elements:
							for node in range(len(mesh.elements[element].nodes)):
								if mesh.elements[element].nodes[node].number in moved_nodes:
									pass
								else:
									moved_nodes.append(mesh.elements[element].nodes[node].number)
									point0 = [mesh.elements[element].nodes[node].coord[0][0],
											  mesh.elements[element].nodes[node].coord[1][0],
											  mesh.elements[element].nodes[node].coord[2][0]]
									point1 = rotatePointAboutAxis(point0,node1_coord,node2_coord,angle)
									mesh.elements[element].nodes[node].coord[0][0] = point1[0]
									mesh.elements[element].nodes[node].coord[1][0] = point1[1]
									mesh.elements[element].nodes[node].coord[2][0] = point1[2]

						x_max = max(mesh.nodes[i].coord[0][0] for i in mesh.nodes )
						x_min = min(mesh.nodes[i].coord[0][0] for i in mesh.nodes )
						y_max = max(mesh.nodes[i].coord[1][0] for i in mesh.nodes )
						y_min = min(mesh.nodes[i].coord[1][0] for i in mesh.nodes )
						z_max = max(mesh.nodes[i].coord[2][0] for i in mesh.nodes )
						z_min = min(mesh.nodes[i].coord[2][0] for i in mesh.nodes )
						mesh.viewScope = {'max': [x_max, y_max, z_max], 'min': [x_min, y_min, z_min]}
						mesh.viewRadius = 1.25*max( (x_max-x_min)/2., (y_max-y_min)/2., (z_max-z_min)/2. )
						self.buildDisplayList(mesh)
						self.gui.new_mesh_view = {'Mesh': self.gui.viewer.currentMesh}
						self.elementOrientation()
						self.gui.viewer.update()
						print('\n\tElements', end=' ')
						for i, element in enumerate(self.selected_elements):
							print(str(element)+', ', end='')
							if i > 7:
								break
						print('... rotated around node', node1_coord, float(self.gui.new_rotation['Angle']), 'degrees.')
					else:
						print('\n\tNo node by that number:', node1)
				
				else:
					try:
						node2 = int(self.gui.new_rotation['Rotation axis node 2'])
					except ValueError:
						print('\n\tRotation axis node 2 must be an integer')
					else:
						if node1 in mesh.nodes and node2 in mesh.nodes:
							node1_coord = [mesh.nodes[node1].coord[0][0],
										   mesh.nodes[node1].coord[1][0],
										   mesh.nodes[node1].coord[2][0]]
							node2_coord = [mesh.nodes[node2].coord[0][0],
										   mesh.nodes[node2].coord[1][0],
										   mesh.nodes[node2].coord[2][0]]
							moved_nodes = []
							for element in self.selected_elements:
								for node in range(len(mesh.elements[element].nodes)):
									if mesh.elements[element].nodes[node].number in moved_nodes:
										pass
									else:
										moved_nodes.append(mesh.elements[element].nodes[node].number)
										point0 = [mesh.elements[element].nodes[node].coord[0][0],
												  mesh.elements[element].nodes[node].coord[1][0],
												  mesh.elements[element].nodes[node].coord[2][0]]
										point1 = rotatePointAboutAxis(point0,node1_coord,node2_coord,angle)
										mesh.elements[element].nodes[node].coord[0][0] = point1[0]
										mesh.elements[element].nodes[node].coord[1][0] = point1[1]
										mesh.elements[element].nodes[node].coord[2][0] = point1[2]

							x_max = max(mesh.nodes[i].coord[0][0] for i in mesh.nodes )
							x_min = min(mesh.nodes[i].coord[0][0] for i in mesh.nodes )
							y_max = max(mesh.nodes[i].coord[1][0] for i in mesh.nodes )
							y_min = min(mesh.nodes[i].coord[1][0] for i in mesh.nodes )
							z_max = max(mesh.nodes[i].coord[2][0] for i in mesh.nodes )
							z_min = min(mesh.nodes[i].coord[2][0] for i in mesh.nodes )
							mesh.viewScope = {'max': [x_max, y_max, z_max], 'min': [x_min, y_min, z_min]}
							mesh.viewRadius = 1.25*max( (x_max-x_min)/2., (y_max-y_min)/2., (z_max-z_min)/2. )
							self.buildDisplayList(mesh)
							self.gui.new_mesh_view = {'Mesh': self.gui.viewer.currentMesh}
							self.elementOrientation()
							self.gui.viewer.update()
							print('\n\tElements', end=' ')
							for i, element in enumerate(self.selected_elements):
								print(str(element)+', ', end='')
								if i > 7:
									break
							print('... rotated around axis', node1_coord, node2_coord, float(self.gui.new_rotation['Angle']), 'degrees.')
						else:
							print('\n\tNo node(s) by that number:', node1, node2)
		else:
			print('\n\tNo elements selected.')


	def importMesh(self,filename):
		'''
	Imports mesh from file. If importing mesh
	from Gmsh as *.bdf file, first convert and
	create a *.sol file before importing.
	'''
		if filename[-4:] == '.bdf':
			print('\n\tConverting bdf-file to sol-file for import ...')
			mesh = ConvertMesh(filename,'.bdf')
			mesh.writeSol(filename[:-4])
			filename = filename[:-4]+'.sol'
		if filename[-4:] == '.inp':
			print('\n\tConverting inp-file to sol-file for import ...')
			mesh = ConvertMesh(filename,'.inp')
			mesh.writeSol(filename[:-4])
			filename = filename[:-4]+'.sol'
		try:
			if filename[-4:] == '.sol':
				fobj = open(filename, 'r')
		except OSError as e:
			print('\n\n  *** ERROR!!!', e)
		else:
			for i in range(len(filename)):
				if filename[-i-1] == '/' or filename[-i-1] == '\\':
					filename = filename[-i:-4]
					break
			print('\n\tImporting mesh from', filename+'.sol')
			
			# find first node and element number
			# for renumbering if one or no solutions
			first_node = 1
			first_element = 1
			for mesh_num in self.meshes:
				if len(self.meshes[mesh_num].nodes) > 0:
					if first_node < max(self.meshes[mesh_num].nodes):
						first_node = max(self.meshes[mesh_num].nodes)+1
				if len(self.meshes[mesh_num].elements) > 0:
					if first_element < max(self.meshes[mesh_num].elements):
						first_element = max(self.meshes[mesh_num].elements)+1

			meshes = {}

			solutions = {}
			currentsol = 'none'
			elementsets = {}
			nodesets = {}
			boundaries = {}
			constraints = {}
			loads = {}

			materials = {}
			sections = {}
			beamorients = {}

			nodes = {}
			elements = {}

			for eachLine in fobj:
				tmpline = [x.strip() for x in eachLine.split(',')]
				if tmpline[0][0] == '#':
					pass
				# solutions
				elif tmpline[0] == 'SOLUTION':
					solutions[tmpline[1]] = {'Type': tmpline[2],
											 'Boundaries': {},
											 'Constraints': {},
											 'Loads': {},
											 'Results': []}
					currentsol = tmpline[1]
				elif tmpline[0] == 'MESHES':
					meshname = filename+'-'+str(len(meshes)+1)
					meshes[meshname] = [int(x) for x in tmpline[1:]]
					if currentsol != 'none':
						solutions[currentsol]['mesh'] = meshname
				elif tmpline[0] == 'BOUNDARIES':
					if currentsol != 'none':
						solutions[currentsol]['Boundaries'][tmpline[1]] = {}
				elif tmpline[0] == 'CONSTRAINTS':
					if currentsol != 'none':
						solutions[currentsol]['Constraints'][tmpline[1]] = {}
				elif tmpline[0] == 'LOADS':
					if currentsol != 'none':
						solutions[currentsol]['Loads'][tmpline[1]] = {}
#				elif tmpline[0] == 'DAMPINGS':
#					if currentsol != 'none':
#						solutions[currentsol]['Dampings'][tmpline[1]] = {}
				# results
				elif tmpline[0] == 'RESULTS':
					currentsol = tmpline[1]
				elif tmpline[0] == 'DISPLACEMENT':
					if currentsol != 'none':
						solutions[currentsol]['Results'].append('disp')
				elif tmpline[0] == 'NODEFORCE':
					if currentsol != 'none':
						solutions[currentsol]['Results'].append('nodf')
				elif tmpline[0] == 'ELEMENTFORCE':
					if currentsol != 'none':
						solutions[currentsol]['Results'].append('elmf')
				elif tmpline[0] == 'STRESS':
					if currentsol != 'none':
						solutions[currentsol]['Results'].append('strs')
				elif tmpline[0] == 'STRAIN':
					if currentsol != 'none':
						solutions[currentsol]['Results'].append('strn')
				elif tmpline[0] == 'MODESHAPES':
					if currentsol != 'none':
						solutions[currentsol]['Results'].append('modes')
				elif tmpline[0] == 'ACCELERATION':
					if currentsol != 'none':
						solutions[currentsol]['Results'].append('accl')
				elif tmpline[0] == 'VELOCITY':
					if currentsol != 'none':
						solutions[currentsol]['Results'].append('velc')
				elif tmpline[0] == 'FRF_ACCEL':
					if currentsol != 'none':
						solutions[currentsol]['Results'].append('frf')
				# nodesets
				elif tmpline[0] == 'SET_NODES':
					setnum = int(tmpline[1])
					nodesets[setnum] = {}
					tmpnodeset = tmpline[2:]
					for n in tmpnodeset:
						try:
							nodesets[setnum][int(n)] = True
						except ValueError:
							m = n.split('-')
							for i in range(int(m[1])-int(m[0])+1):
								nodesets[setnum][int(m[0])+i] = True
				# elementsets
				elif tmpline[0] == 'SET_ELEMENTS':
					setnum = int(tmpline[1])
					elementsets[setnum] = {}
					tmpelementset = tmpline[2:]
					for n in tmpelementset:
						try:
							elementsets[setnum][int(n)] = True
						except ValueError:
							m = n.split('-')
							for i in range(int(m[1])-int(m[0])+1):
								elementsets[setnum][int(m[0])+i] = True
				# materials
				elif tmpline[0] == 'MATERIAL':
					materials[tmpline[2]] = {'Elasticity': float(tmpline[3]),
											 'Poisson ratio': float(tmpline[4])}
					if len(tmpline) > 5:
						materials[tmpline[2]]['Density'] = float(tmpline[5])
					else:
						materials[tmpline[2]]['Density'] = 1.
				elif tmpline[0] == 'SECTION':
					sections['sect-'+tmpline[2]] = {'Number': int(tmpline[2]),
													'Material': tmpline[3]}
					if tmpline[1] in ['RodSect', 'BeamSect']:
						sections['sect-'+tmpline[2]]['Area (Rod or Beam)'] = float(tmpline[4])
						if tmpline[1] == 'BeamSect':
							sections['sect-'+tmpline[2]]['Izz (Beam)'] = float(tmpline[5])
						if len(tmpline) > 6 and tmpline[5] != 'CrossSection':
							sections['sect-'+tmpline[2]]['Iyy (Beam 3D)'] = float(tmpline[5])
						if 'CrossSection' in tmpline:
							cs_index = tmpline.index('CrossSection')
							if 'Rectangle' in tmpline:
								sections['sect-'+tmpline[2]]['Cross section'] = { 'Type': 'Rectangle',
																				  'width, w': float(tmpline[cs_index+2]),
																				  'height, h': float(tmpline[cs_index+3]),
																				  'inner width, iw': float(tmpline[cs_index+4]),
																				  'inner height, ih': float(tmpline[cs_index+5]) }
							elif 'Circle' in tmpline:
								sections['sect-'+tmpline[2]]['Cross section'] = { 'Type': 'Circle',
																		 		  'radius, r': float(tmpline[cs_index+2]),
																		 		  'inner radius, ir': float(tmpline[cs_index+3]) }
							elif 'I-Beam' in tmpline:
								sections['sect-'+tmpline[2]]['Cross section'] = { 'Type': 'I-Beam',
																				  'top width, tw': float(tmpline[cs_index+2]),
																				  'top thickness, tt': float(tmpline[cs_index+3]),
																				  'middle thickness, mt': float(tmpline[cs_index+4]),
																				  'bottom width, bw': float(tmpline[cs_index+5]),
																				  'bottom thickness, bt': float(tmpline[cs_index+6]),
																				  'height, h': float(tmpline[cs_index+7])}
							elif 'C-Beam' in tmpline:
								sections['sect-'+tmpline[2]]['Cross section'] = { 'Type': 'C-Beam',
																				  'top width, tw': float(tmpline[cs_index+2]),
																				  'top thickness, tt': float(tmpline[cs_index+3]),
																				  'middle thickness, mt': float(tmpline[cs_index+4]),
																				  'bottom width, bw': float(tmpline[cs_index+5]),
																				  'bottom thickness, bt': float(tmpline[cs_index+6]),
																				  'height, h': float(tmpline[cs_index+7])}
							elif 'T-Beam' in tmpline:
								sections['sect-'+tmpline[2]]['Cross section'] = { 'Type': 'T-Beam',
																				  'top width, tw': float(tmpline[cs_index+2]),
																				  'top thickness, tt': float(tmpline[cs_index+3]),
																				  'middle thickness, mt': float(tmpline[cs_index+4]),
																				  'height, h': float(tmpline[cs_index+5])}
							elif 'L-Beam' in tmpline:
								sections['sect-'+tmpline[2]]['Cross section'] = { 'Type': 'L-Beam',
																				  'side thickness, st': float(tmpline[cs_index+2]),
																				  'bottom width, bw': float(tmpline[cs_index+3]),
																				  'bottom thickness, bt': float(tmpline[cs_index+4]),
																				  'height, h': float(tmpline[cs_index+5])}
							else:
								print('\n\tUnknown cross section type for section sect-', tmpline[2])
					elif tmpline[1] in ['PlaneSect', 'PlateSect']:
						sections['sect-'+tmpline[2]]['Thickness (2D)'] = float(tmpline[4])
					else:
						pass
				# maybe later
				elif tmpline[0] == 'BEAMORIENT':
					pass
				elif tmpline[0] == 'DAMPING':
					pass
				elif tmpline[0] == 'TABLE':
					pass
				# boundaries
				elif tmpline[0] == 'BOUNDARY':
					for sol in solutions:
						if tmpline[2] in solutions[sol]['Boundaries']:
							solutions[sol]['Boundaries'][tmpline[2]] = {'Type': tmpline[1],
																		'Nodeset': tmpline[3],
																		'DOFs': [int(x) for x in tmpline[5:]]}
							if tmpline[1] == 'Displacement':
								solutions[sol]['Boundaries'][tmpline[2]]['Displacement'] = tmpline[4]
				# constraints
				elif tmpline[0] == 'CONSTRAINT':
					for sol in solutions:
						if tmpline[2] in solutions[sol]['Constraints']:
							solutions[sol]['Constraints'][tmpline[2]] = {'Type': tmpline[1],
																		 'Nodeset1': tmpline[3],
																		 'Nodeset2': tmpline[4]}
							if tmpline[1] == 'TouchLock':
								solutions[sol]['Constraints'][tmpline[2]]['Tolerance'] = tmpline[5]
								solutions[sol]['Constraints'][tmpline[2]]['DOFs'] = [int(x) for x in tmpline[6:]]
							else:
								solutions[sol]['Constraints'][tmpline[2]]['DOFs'] = [int(x) for x in tmpline[5:]]
				# loads
				elif tmpline[0] == 'LOAD':
					for sol in solutions:
						if tmpline[2] in solutions[sol]['Loads']:
							solutions[sol]['Loads'][tmpline[2]] = {'Type': tmpline[1],
																   'x-vector': tmpline[5],
																   'y-vector': tmpline[6]}
							if len(tmpline) > 7:
								solutions[sol]['Loads'][tmpline[2]]['z-vector'] = tmpline[7]
							else:
								solutions[sol]['Loads'][tmpline[2]]['z-vector'] = 0.
							if tmpline[1] in ['Force','ForceConcentrated','ForceDynamic','Acceleration']:
								solutions[sol]['Loads'][tmpline[2]]['Force'] = tmpline[4]
								solutions[sol]['Loads'][tmpline[2]]['Nodeset'] = tmpline[3]
							if tmpline[1] == 'Torque':
								solutions[sol]['Loads'][tmpline[2]]['Torque'] = tmpline[4]
								solutions[sol]['Loads'][tmpline[2]]['Nodeset'] = tmpline[3]
							if tmpline[1] == 'ForceDistributed':
								solutions[sol]['Loads'][tmpline[2]]['Force/Length'] = tmpline[4]
								solutions[sol]['Loads'][tmpline[2]]['Elementset'] = tmpline[3]
							if tmpline[1] == 'Gravity':
								solutions[sol]['Loads'][tmpline[2]]['Acceleration'] = tmpline[4]
								solutions[sol]['Loads'][tmpline[2]]['Elementset'] = tmpline[3]
							if tmpline[1] == 'ForceDistributed':
								solutions[sol]['Loads'][tmpline[2]]['Force'] = tmpline[4]
								solutions[sol]['Loads'][tmpline[2]]['Elementset'] = tmpline[3]
							else:
								pass								

				elif tmpline[0] == 'NODE':
					nodes[int(tmpline[1])] = Node(int(tmpline[1]),float(tmpline[2]),float(tmpline[3]))
					if len(tmpline) > 4:
						nodes[int(tmpline[1])].coord[2][0] = float(tmpline[4])

				elif tmpline[0] == 'ELEMENT':
					elmnodes = [nodes[int(x)] for x in tmpline[4:]]
					elmsect = 'sect-'+tmpline[3]
					if elmsect not in sections:
						elmsect = None
					elements[int(tmpline[2])] = Element(int(tmpline[2]),elmsect,elmnodes)
					elements[int(tmpline[2])].type = tmpline[1]
				else:
					pass

			# create elementset 999 with all elements
			elementsets[999] = {}
			for element in elements:
				elementsets[999][elements[element].number] = elements[element]
			# if not 'mesh' in solution add mesh
			if len(meshes) == 0:
				meshes[filename] = [999]
			for sol in solutions:
				if 'mesh' not in solutions[sol]:
					solutions[sol]['mesh'] = filename

			# insert nodes and elements into
			# nodesets and elementsets
			for nset in nodesets:
				for node in nodesets[nset]:
					if node in nodes:
						nodesets[nset][node] = nodes[node]
			for elmset in elementsets:
				for elm in elementsets[elmset]:
					if elm in elements:
						elementsets[elmset][elm] = elements[elm]

			for nodeset in nodesets:
				self.nodesets[nodeset] = nodesets[nodeset]
			for elementset in elementsets:
				self.elementsets[elementset] = elementsets[elementset]
			for material in materials:
				self.materials[material] = materials[material]
			for section in sections:
				self.sections[section] = sections[section]

			filename = str(filename)
			print('\tCreating new mesh(es): ', end='')
			for meshname in meshes:
				print(meshname+', ', end='')
				meshnodes = {}
				meshelements = {}
				for elmset in meshes[meshname]:
					for elm in elementsets[elmset]:
						if elm not in meshelements:
							meshelements[elm] = elements[elm]
							for node in elements[elm].nodes:
								if node.number not in meshnodes:
									meshnodes[node.number] = node
				self.meshes[meshname] = Mesh(meshnodes,meshelements)
				self.meshes[meshname].nodesets = {}
				self.meshes[meshname].elementsets = {}
				self.meshes[meshname].materials = {}
				self.meshes[meshname].solutions = {}
				self.meshes[meshname].displayLists = {'solutions': {}}
				for sol in solutions:
					if solutions[sol]['mesh'] == meshname:
						self.meshes[meshname].solutions[sol] = solutions[sol]
						self.meshes[meshname].displayLists['solutions'][sol] = {'boundaries': {},
																				'constraints': {},
																				'loads': {}}
				x_max = max(self.meshes[meshname].nodes[i].coord[0][0] for i in self.meshes[meshname].nodes )
				x_min = min(self.meshes[meshname].nodes[i].coord[0][0] for i in self.meshes[meshname].nodes )
				y_max = max(self.meshes[meshname].nodes[i].coord[1][0] for i in self.meshes[meshname].nodes )
				y_min = min(self.meshes[meshname].nodes[i].coord[1][0] for i in self.meshes[meshname].nodes )
				z_max = max(self.meshes[meshname].nodes[i].coord[2][0] for i in self.meshes[meshname].nodes )
				z_min = min(self.meshes[meshname].nodes[i].coord[2][0] for i in self.meshes[meshname].nodes )
				self.meshes[meshname].viewScope = {'max': [x_max, y_max, z_max], 'min': [x_min, y_min, z_min]}
				self.meshes[meshname].viewRadius = 1.25*max( (x_max-x_min)/2., (y_max-y_min)/2., (z_max-z_min)/2. )
				self.buildDisplayList(self.meshes[meshname])
				self.gui.new_mesh_view = {'Mesh': meshname}
				self.elementOrientation()
				for solution in self.meshes[meshname].solutions:
					sol = self.meshes[meshname].solutions[solution]
					for boundary in sol['Boundaries']:
						self.gui.new_boundary = {'Mesh':		 meshname,
												 'Name':		 boundary,
												 'Solution':	 solution,
												 'Type':		 sol['Boundaries'][boundary]['Type'],
												 'Nodeset':		 sol['Boundaries'][boundary]['Nodeset'],
												 'Displacement': sol['Boundaries'][boundary]['Displacement'],
												 'DOFs':		 str(sol['Boundaries'][boundary]['DOFs'])[1:-1] }
						self.applyBoundary()
						self.gui.new_boundary.clear()
					for constraint in sol['Constraints']:
						self.gui.new_constraint = {'Mesh':		meshname,
												   'Name':	 	constraint,
												   'Solution':	solution,
												   'Type':	 	sol['Constraints'][constraint]['Type'],
												   'Nodeset1':	sol['Constraints'][constraint]['Nodeset1'],
												   'Nodeset2':	sol['Constraints'][constraint]['Nodeset2'],
												   'DOFs':		sol['Constraints'][constraint]['DOFs'] }
						if 'Tolerance' in sol['Constraints'][constraint]:
							self.gui.new_constraint['Tolerance'] = sol['Constraints'][constraint]['Tolerance']
						self.applyConstraint()
						self.gui.new_constraint.clear()
					for load in sol['Loads']:
						self.gui.new_load = {'Mesh':	 meshname,
											 'Name':	 load,
											 'Solution': solution,
											 'Type':	 sol['Loads'][load]['Type'],
											 'x-vector': sol['Loads'][load]['x-vector'],
											 'y-vector': sol['Loads'][load]['y-vector'],
											 'z-vector': sol['Loads'][load]['z-vector'] }
						if 'Nodeset' in sol['Loads'][load]:
							self.gui.new_load['Nodeset'] = sol['Loads'][load]['Nodeset']
						if 'Elementset' in sol['Loads'][load]:
							self.gui.new_load['Elementset'] = sol['Loads'][load]['Elementset']
						if 'Force' in sol['Loads'][load]:
							self.gui.new_load['Force'] = sol['Loads'][load]['Force']
						if 'Force/Length' in sol['Loads'][load]:
							self.gui.new_load['Force/Length'] = sol['Loads'][load]['Force/Length']
						if 'Torque' in sol['Loads'][load]:
							self.gui.new_load['Torque'] = sol['Loads'][load]['Torque']
							self.gui.new_load['mx-vector'] = sol['Loads'][load]['x-vector']
							self.gui.new_load['my-vector'] = sol['Loads'][load]['y-vector']
							self.gui.new_load['mz-vector'] = sol['Loads'][load]['z-vector']
						if 'Acceleration' in sol['Loads'][load]:
							self.gui.new_load['Acceleration'] = sol['Loads'][load]['Acceleration']
						self.applyLoad()
						self.gui.new_load.clear()

				if len(meshes) == 1:
					if len(self.meshes) > 1:
						if len(solutions) == 0:
							self.gui.viewer.currentMesh = meshname
							self.selected_nodes = {}
							for n in self.meshes[meshname].nodes:
								self.selected_nodes[n] = self.meshes[meshname].nodes[n]
							self.nodesSelected = True
							if first_node in self.selected_nodes:
								first_node = max(self.selected_nodes)+1
							self.gui.renumberNodes(first_node)
							self.selected_nodes.clear()
							self.nodesSelected = False
							self.selected_elements = {}
							for e in self.meshes[meshname].elements:
								self.selected_elements[e] = self.meshes[meshname].elements
							self.elementsSelected = True
							if first_element in self.selected_elements:
								first_element = max(self.selected_elements)+1
							self.gui.renumberElements(first_element)						
							self.selected_elements.clear()
							self.elementsSelected = False

#			print('...')
		for mesh in self.meshes:
			self.checkForSection(self.meshes[mesh])


	def loadModel(self,filename):
		'''
	Loads *.mesh file and creates new current
	session with model from that file.
	'''
		modelfile = ''
		for i in range(len(filename)):
			if filename[-i-1] == '/' or filename[-i-1] == '\\':
				modelfile = str(filename[-i:-4])
				break
		print('\n\n\tOpening file', modelfile+'.mdl')

		tmpmodel = pickle.load(open(filename,'rb'))[0]

		self.clearModel()
		self.nodesets	  = tmpmodel.nodesets
		self.elementsets  = tmpmodel.elementsets
		self.materials 	  = tmpmodel.materials
		self.sections 	  = tmpmodel.sections
		self.meshes 	  = tmpmodel.meshes
		self.displayLists = tmpmodel.displayLists
		for mesh in self.meshes:
			self.buildDisplayList(self.meshes[mesh])	
			self.gui.new_mesh_view = {'Mesh': mesh}
			self.elementOrientation()
			for solution in self.meshes[mesh].solutions:
				sol = self.meshes[mesh].solutions[solution]
				for boundary in sol['Boundaries']:
					self.gui.new_boundary = {'Mesh':		 mesh,
											 'Name':		 boundary,
											 'Solution':	 solution,
											 'Type':		 sol['Boundaries'][boundary]['Type'],
											 'Nodeset':		 sol['Boundaries'][boundary]['Nodeset'],
											 'Displacement': sol['Boundaries'][boundary]['Displacement'],
											 'DOFs':		 str(sol['Boundaries'][boundary]['DOFs'])[1:-1] }
					self.applyBoundary()
					self.gui.new_boundary.clear()
				for constraint in sol['Constraints']:
					self.gui.new_constraint = {'Mesh':		mesh,
											   'Name':	 	constraint,
											   'Solution':	solution,
											   'Type':	 	sol['Constraints'][constraint]['Type'],
											   'Nodeset1':	sol['Constraints'][constraint]['Nodeset1'],
											   'Nodeset2':	sol['Constraints'][constraint]['Nodeset2'],
											   'DOFs':		sol['Constraints'][constraint]['DOFs'] }
					if 'Tolerance' in sol['Constraints'][constraint]:
						self.gui.new_constraint['Tolerance'] = sol['Constraints'][constraint]['Tolerance']
					self.applyConstraint()
					self.gui.new_constraint.clear()
				for load in sol['Loads']:
					self.gui.new_load = {'Mesh':	 mesh,
										 'Name':	 load,
										 'Solution': solution,
										 'Type':	 sol['Loads'][load]['Type'],
										 'x-vector': sol['Loads'][load]['x-vector'],
										 'y-vector': sol['Loads'][load]['y-vector'],
										 'z-vector': sol['Loads'][load]['z-vector'] }
					if 'Nodeset' in sol['Loads'][load]:
						self.gui.new_load['Nodeset'] = sol['Loads'][load]['Nodeset']
					if 'Elementset' in sol['Loads'][load]:
						self.gui.new_load['Elementset'] = sol['Loads'][load]['Elementset']
					if 'Force' in sol['Loads'][load]:
						self.gui.new_load['Force'] = sol['Loads'][load]['Force']
					if 'Force/Length' in sol['Loads'][load]:
						self.gui.new_load['Force/Length'] = sol['Loads'][load]['Force/Length']
					if 'Torque' in sol['Loads'][load]:
						self.gui.new_load['Torque'] = sol['Loads'][load]['Torque']
						self.gui.new_load['mx-vector'] = sol['Loads'][load]['x-vector']
						self.gui.new_load['my-vector'] = sol['Loads'][load]['y-vector']
						self.gui.new_load['mz-vector'] = sol['Loads'][load]['z-vector']
					if 'Acceleration' in sol['Loads'][load]:
						self.gui.new_load['Acceleration'] = sol['Loads'][load]['Acceleration']
					self.applyLoad()
					self.gui.new_load.clear()
		self.gui.shadedView()
		self.gui.wireframeView()


	def readResults(self,filename):
		'''
	Opens .out-file and reads in the results
	so they can be accessed by the viewer.
	'''
		newResults = 'None'
		for i in range(len(filename)):
			if filename[-i-1] == '/' or filename[-i-1] == '\\':
				newResults = str(filename[-i:-4])
				break
		print('\n\n\tOpening file', newResults+'.out')
		print('\t--------------------------------',end=' ')
		self.results[newResults] = pickle.load(open(filename,'rb'))[0]

		print('\n\tNew meshes available...')
		for mesh in self.results[newResults].meshes:
			x_max = max(self.results[newResults].meshes[mesh].nodes[i].coord[0][0] for i in self.results[newResults].meshes[mesh].nodes )
			x_min = min(self.results[newResults].meshes[mesh].nodes[i].coord[0][0] for i in self.results[newResults].meshes[mesh].nodes )
			y_max = max(self.results[newResults].meshes[mesh].nodes[i].coord[1][0] for i in self.results[newResults].meshes[mesh].nodes )
			y_min = min(self.results[newResults].meshes[mesh].nodes[i].coord[1][0] for i in self.results[newResults].meshes[mesh].nodes )
			z_max = max(self.results[newResults].meshes[mesh].nodes[i].coord[2][0] for i in self.results[newResults].meshes[mesh].nodes )
			z_min = min(self.results[newResults].meshes[mesh].nodes[i].coord[2][0] for i in self.results[newResults].meshes[mesh].nodes )
			self.results[newResults].meshes[mesh].viewScope = {'max': [x_max, y_max, z_max], 'min': [x_min, y_min, z_min]}
			self.results[newResults].meshes[mesh].viewRadius = 1.25*max( (x_max-x_min)/2., (y_max-y_min)/2., (z_max-z_min)/2. )
			self.results[newResults].meshes[mesh].displayLists = {}

			for element in self.results[newResults].meshes[mesh].elements:
				self.results[newResults].meshes[mesh].elements[element].section = None
			self.checkForSection(self.results[newResults].meshes[mesh])

			print('\t'+newResults+'_mesh-'+str(mesh+1))
			self.meshes[newResults+'_mesh-'+str(mesh+1)] = self.results[newResults].meshes[mesh]
			self.buildDisplayList(self.results[newResults].meshes[mesh])

		print('\n\tNew results available from solutions...',end=' ')
		for solution in self.results[newResults].solutions:
			print('\n\t', solution+':',end=' ')
			toprint = []
			for result in self.results[newResults].solutions[solution].results:
				if (result == 'modeshapes') or (result == 'displacement'):
					toprint.append(result)
				elif 'plot' in self.results[newResults].solutions[solution].results[result]:
					toprint.append(result)
				else:
					pass
			i = 0
			for result in toprint:
				if i == 0:
					print(result,end=' ')
					i += 1
				else:
					print('-', result,end=' ')
		print('\n')
		for mesh in self.meshes:
			self.checkForSection(self.meshes[mesh])


	def createNewMesh(self):
		'''
	Creates a new mesh.
	'''
		print('\n\tCreating new Mesh ('+self.gui.new_mesh['Name']+')')
		nodes = {}
		elements = {}
		try:
			elmsets = [int(x.strip()) for x in self.gui.new_mesh['Elementsets'].split(',')]
		except ValueError:
			print('\n\tElement sets must be integers (separated by commas).')
			print('\tExample: 2, 3, 5, 9')
		else:
			start_node_num = 0
			start_elm_num  = 0
			for elmset in elmsets:
				if elmset in self.elementsets:
					if max(self.elementsets[elmset]) > start_elm_num:
						start_elm_num = max(self.elementsets[elmset])
					for elm in self.elementsets[elmset]:
						elements[elm] = Element(deepcopy(self.elementsets[elmset][elm].number), None,
												[None for i in range(len(self.elementsets[elmset][elm].nodes))])
						elements[elm].type = deepcopy(self.elementsets[elmset][elm].type)
						for node in range(len(self.elementsets[elmset][elm].nodes)):
							nodenum = deepcopy(self.elementsets[elmset][elm].nodes[node].number)
							if nodenum > start_node_num:
								start_node_num = nodenum
							if nodenum not in nodes:
								nodes[nodenum] = deepcopy(self.elementsets[elmset][elm].nodes[node])
								elements[elm].nodes[node] = nodes[nodenum]
							else:
								elements[elm].nodes[node] = nodes[nodenum]
				else:
					print('\tElementset', elmset, 'not found. Not applied to mesh.')

			new_elements = {}
			for e, element in enumerate(elements):
				new_elements[start_elm_num+1+e] = elements[element]
				new_elements[start_elm_num+1+e].number = start_elm_num+1+e
			new_nodes = {}
			for n, node in enumerate(nodes):
				new_nodes[start_node_num+1+n] = nodes[node]
				new_nodes[start_node_num+1+n].number = start_node_num+1+n
			elements = new_elements
			nodes = new_nodes

			print('\tNodes:',end=' ')
			toprint = nodes.keys()
			toprint = sorted(toprint)
			if len(toprint) > 8:
				print('[',end=' ')
				for i in range(4):
					print(str(toprint[i])+',',end=' ')
				print('...',end=' ')
				print(str(toprint[-3])+',',end=' ')
				print(str(toprint[-2])+',',end=' ')
				print(str(toprint[-1])+' ]')
			else:
				print(str(toprint))
			print('\tElements:',end=' ')
			toprint = elements.keys()
			toprint = sorted(toprint)
			if len(toprint) > 8:
				print('[',end=' ') 
				for i in range(4):
					print(str(toprint[i])+',',end=' ')
				print('...',end=' ')
				print(str(toprint[-3])+',',end=' ')
				print(str(toprint[-2])+',',end=' ')
				print(str(toprint[-1])+' ]')
			else:
				print(str(toprint))

			self.meshes[self.gui.new_mesh['Name']] = Mesh(nodes,elements)
			mesh = self.meshes[self.gui.new_mesh['Name']]
			mesh.nodesets = {}
			mesh.elementsets = {}
			mesh.materials = {}
			mesh.solutions = {}
			for elmset in elmsets:
				if elmset in self.elementsets:
					mesh.elementsets[elmset] = self.elementsets[elmset]
			if len(mesh.elementsets) != 0:
				x_max = max(mesh.nodes[i].coord[0][0] for i in mesh.nodes )
				x_min = min(mesh.nodes[i].coord[0][0] for i in mesh.nodes )
				y_max = max(mesh.nodes[i].coord[1][0] for i in mesh.nodes )
				y_min = min(mesh.nodes[i].coord[1][0] for i in mesh.nodes )
				z_max = max(mesh.nodes[i].coord[2][0] for i in mesh.nodes )
				z_min = min(mesh.nodes[i].coord[2][0] for i in mesh.nodes )
				mesh.viewScope = {'max': [x_max, y_max, z_max], 'min': [x_min, y_min, z_min]}
				mesh.viewRadius = 1.25*max( (x_max-x_min)/2., (y_max-y_min)/2., (z_max-z_min)/2. )
			else:
				mesh.viewScope = {'max': [1., 1., 1.], 'min': [1., 1., 1.]}
				mesh.viewRadius = 2.
			mesh.displayLists = {'solutions': {}}
			self.buildDisplayList(mesh)
			self.gui.new_mesh_view = {'Mesh': self.gui.new_mesh['Name']}
			self.elementOrientation()
			for mesh in self.meshes:
				self.checkForSection(self.meshes[mesh])


	def createMaterial(self):
		'''
	Creates a new material.
	'''
		self.materials[self.gui.new_material['Name']] = {}
		for prop in self.gui.new_material:
			if prop == 'Name':
				pass
			else:
				self.materials[self.gui.new_material['Name']][prop] = float(self.gui.new_material[prop])
		print('\n\tNew material created:\n\t', self.materials[self.gui.new_material['Name']], '\n\t')
		print('\tAll materials:')
		for material in self.materials:
			print('\t', material, '-', self.materials[material])


	def createSection(self):
		'''
	Creates a new section.
	'''
		sectnum = len(self.sections)
		self.sections[self.gui.new_section['Name']] = {}
		if self.gui.new_section['Material'] in self.materials:
			for prop in self.gui.new_section:
				if prop == 'Name':
					self.sections[self.gui.new_section['Name']]['Number'] = sectnum
				elif prop == 'Material':
					self.sections[self.gui.new_section['Name']][prop] = self.gui.new_section[prop]
				else:
					self.sections[self.gui.new_section['Name']][prop] = float(self.gui.new_section[prop])
			print('\n\tNew section created:\n\t', self.sections[self.gui.new_section['Name']], '\n\t')
			print('\tAll sections:')
			for section in self.sections:
				print('\t', section, '-', self.sections[section])
		else:
			print('\n\tNo material by that name ('+self.gui.new_section['Material']+'). Section not created...')


	def applySection(self):
		'''
	Applies a selected section to specified elementsets.
	'''
		elmsets = []
		current = ''
		count = 0
		for i in self.gui.new_section_assignment['Elementsets']:
			if i == ',':
				elmsets.append(int(current))
				current = ''
				count += 1
			elif count == (len(self.gui.new_section_assignment['Elementsets'])-1):
				current += i
				elmsets.append(int(current))
			else:
				current += i
				count += 1
		for elmset in elmsets:
			if elmset in self.elementsets:
				for element in self.elementsets[elmset]:
					self.elementsets[elmset][element].section = self.gui.new_section_assignment['Section']
				print('\n\tSection', self.gui.new_section_assignment['Section'], 'applied to elementset', elmset)
			else:
				print('\n\tNo elementset by that number ('+str(elmset)+').')
				print('\tNo section applied there...')
		for mesh in self.meshes:
			self.checkForSection(self.meshes[mesh])


	def checkForSection(self,mesh):
		'''
	Checks what sections are applied to elements
	in mesh and if all elements have been
	applied a section.
	'''
		mesh.sections = []
		mesh.sections_applied = True
		for element in mesh.elements:
			if mesh.elements[element].section != None:
				for section in self.sections:
					if mesh.elements[element].section == section:
						if section not in mesh.sections:
							mesh.sections.append(section)
			else:
				mesh.sections_applied = False


	def createSolution(self):
		'''
	Create a new solution.
	'''
		if self.gui.new_solution['Mesh'] in self.meshes:
			if hasattr(self.meshes[self.gui.new_solution['Mesh']], 'is3D'):
				print('\n\tCannot use mesh that already has results to create')
				print('\tnew solutions. User must create a new mesh from an')
				print('\telementset of this mesh and then create new solutions')
				print('\twith the new mesh.')
				return
			self.meshes[self.gui.new_solution['Mesh']].solutions[self.gui.new_solution['Name']] = \
						{'Type': self.gui.new_solution['Type'], 'Boundaries': {}, 'Loads': {}, 'Constraints': {}}
			self.meshes[self.gui.new_solution['Mesh']].solutions[self.gui.new_solution['Name']]['Results'] = []

			results = []
			current = ''
			count = 0
			for i in self.gui.new_solution['Results']:
				if i == ',':
					results.append(current)
					current = ''
					count += 1
				elif i == ' ':
					count += 1
				elif count == (len(self.gui.new_solution['Results'])-1):
					current += i
					results.append(current)
				else:
					current += i
					count += 1

			wrong_input = False
			for result in results:
				if result in ['disp', 'velc', 'accl', 'strs', 'strn', 'nodf', 'elmf', 'modes', 'frf']:
					self.meshes[self.gui.new_solution['Mesh']].solutions[self.gui.new_solution['Name']]['Results'].append(result)
				else:
					wrong_input = True
			if self.gui.new_solution['Type'] == 'ModalDynamic':
				self.meshes[self.gui.new_solution['Mesh']].solutions[self.gui.new_solution['Name']]['Results'].append('modes')
				self.meshes[self.gui.new_solution['Mesh']].solutions[self.gui.new_solution['Name']]['Results'].append('dampratio')
				self.meshes[self.gui.new_solution['Mesh']].solutions[self.gui.new_solution['Name']]['Results'].append('forcetable')
			if wrong_input == True:
				print('\tWrong input requested for solution.')
				print('\tAcceptable inputs are:')
				print('\tdisp  - node displacements')
				print('\tvelc  - node velocities')
				print('\taccl  - node accelerations')
				print('\tstrs  - element stresses')
				print('\tstrn  - element strains')
				print('\tnodf  - node forces')
				print('\telmf  - element forces')
				print('\tmodes - eigenmodes')
				print('\tfrf   - frequency response acceleration')
			self.meshes[self.gui.new_solution['Mesh']].displayLists['solutions'][self.gui.new_solution['Name']] = \
																			{'constraints': {}, 'boundaries': {}, 'loads': {}}
			print('\n\tCreating new '+self.gui.new_solution['Type']+' solution ('+self.gui.new_solution['Name']+')')
			print('\t', self.meshes[self.gui.new_solution['Mesh']].solutions[self.gui.new_solution['Name']])
		else:
			print('\n\tNo mesh by that name ('+self.gui.new_solution['Mesh']+').')
			print('\tNo solution created...')

		
	def applyConstraint(self):
		'''
	Applies lagrangian multiplier constraints
	between nodes specified in two nodesets.
	'''
		if self.gui.new_constraint['Nodeset1'].isdigit() and \
			self.gui.new_constraint['Nodeset2'].isdigit():
			if (int(self.gui.new_constraint['Nodeset1']) in self.nodesets) and \
				(int(self.gui.new_constraint['Nodeset2']) in self.nodesets):
				nodecheck = True
				for node in self.nodesets[int(self.gui.new_constraint['Nodeset1'])]:
					if node not in self.meshes[self.gui.new_constraint['Mesh']].nodes:
						nodecheck = False
				for node in self.nodesets[int(self.gui.new_constraint['Nodeset2'])]:
					if node not in self.meshes[self.gui.new_constraint['Mesh']].nodes:
						nodecheck = False
				if nodecheck == True:
					self.meshes[self.gui.new_constraint['Mesh']].nodesets[int(self.gui.new_constraint['Nodeset1'])] = \
																		list(self.nodesets[int(self.gui.new_constraint['Nodeset1'])].keys())
					self.meshes[self.gui.new_constraint['Mesh']].nodesets[int(self.gui.new_constraint['Nodeset2'])] = \
																		list(self.nodesets[int(self.gui.new_constraint['Nodeset2'])].keys())
					self.meshes[self.gui.new_constraint['Mesh']].solutions[self.gui.new_constraint['Solution']] \
						['Constraints'][self.gui.new_constraint['Name']] = { 'Nodeset1': self.gui.new_constraint['Nodeset1'],
							'Nodeset2': self.gui.new_constraint['Nodeset2'], 'Type': self.gui.new_constraint['Type'] }
					if self.gui.new_constraint['Type'] == 'TouchLock':
						self.meshes[self.gui.new_constraint['Mesh']].solutions[self.gui.new_constraint['Solution']] \
						['Constraints'][self.gui.new_constraint['Name']]['Tolerance'] = self.gui.new_constraint['Tolerance']
					DOFs = []
					dof = str(self.gui.new_constraint['DOFs'])
					dof = dof.replace('[','')
					dof = dof.replace(']','')
					dof = dof.split(',')
					for i in range(len(dof)):
						DOFs.append(int(dof[i]))
					self.meshes[self.gui.new_constraint['Mesh']].solutions[self.gui.new_constraint['Solution']] \
						['Constraints'][self.gui.new_constraint['Name']]['DOFs'] = DOFs
					print('\n\t'+self.gui.new_constraint['Type']+' constraint applied to nodesets',end=' ')
					print(int(self.gui.new_constraint['Nodeset1']), 'and', int(self.gui.new_constraint['Nodeset2']),end=' ')
					print('in', self.gui.new_constraint['Mesh'])
					print('\tConstraints in ('+self.gui.new_constraint['Mesh']+'):')
					print('\t', self.meshes[self.gui.new_constraint['Mesh']].solutions[self.gui.new_constraint['Solution']]['Constraints'])
					self.meshes[self.gui.new_constraint['Mesh']].displayLists['solutions'][self.gui.new_constraint['Solution']] \
																	['constraints'][self.gui.new_constraint['Name']] = glGenLists(1)
					glNewList(self.meshes[self.gui.new_constraint['Mesh']].displayLists['solutions'][self.gui.new_constraint['Solution']] \
																			['constraints'][self.gui.new_constraint['Name']], GL_COMPILE)
					glPointSize(13.0)
					glBegin(GL_POINTS)
					glColor3f(8.0, 0.4, 0.0)
					for node in self.nodesets[int(self.gui.new_constraint['Nodeset1'])]:
						glVertex3f(self.nodesets[int(self.gui.new_constraint['Nodeset1'])][node].coord[0][0], 
								   self.nodesets[int(self.gui.new_constraint['Nodeset1'])][node].coord[1][0], 
								   self.nodesets[int(self.gui.new_constraint['Nodeset1'])][node].coord[2][0])
					for node in self.nodesets[int(self.gui.new_constraint['Nodeset2'])]:
						glVertex3f(self.nodesets[int(self.gui.new_constraint['Nodeset2'])][node].coord[0][0], 
								   self.nodesets[int(self.gui.new_constraint['Nodeset2'])][node].coord[1][0], 
								   self.nodesets[int(self.gui.new_constraint['Nodeset2'])][node].coord[2][0])
					glEnd()
					glLineWidth(9.0)
					if self.gui.new_constraint['Type'] == 'NodeLock':
						for node2 in self.nodesets[int(self.gui.new_constraint['Nodeset2'])]:
							for node1 in self.nodesets[int(self.gui.new_constraint['Nodeset1'])]:
								glBegin(GL_LINES)
								glColor3f(8.0, 0.4, 0.0)
								glVertex3f(self.nodesets[int(self.gui.new_constraint['Nodeset1'])][node1].coord[0][0],
										   self.nodesets[int(self.gui.new_constraint['Nodeset1'])][node1].coord[1][0], 
										   self.nodesets[int(self.gui.new_constraint['Nodeset1'])][node1].coord[2][0])
								glVertex3f(self.nodesets[int(self.gui.new_constraint['Nodeset2'])][node2].coord[0][0],
										   self.nodesets[int(self.gui.new_constraint['Nodeset2'])][node2].coord[1][0], 
										   self.nodesets[int(self.gui.new_constraint['Nodeset2'])][node2].coord[2][0])
								glEnd()
					glEndList()
				else:
					print('\n\tThere are nodes in the nodesets that are not in the selected mesh')
					print('\tNo constraint applied...')
			else:
				print('\n\tNo nodeset by that number ('+self.gui.new_constraint['Nodeset1']+' and/or ',end=' ')
				print(self.gui.new_constraint['Nodeset1']+').',end=' ')
				print('\tNo constraint applied...')
		else:
			print('\n\t'+self.gui.new_constraint['Nodeset1'], 'and/or', self.gui.new_constraint['Nodeset1'],end=' ')
			print('is not an acceptable input for Nodeset.')
			print('\tNodesets need to be specified as an integer.')
			print('\tNo constraint applied...')


	def applyBoundary(self):
		'''
	Applies boundary to a selected set of nodes.
	'''
		if self.gui.new_boundary['Nodeset'].isdigit():
			if int(self.gui.new_boundary['Nodeset']) in self.nodesets:
				nodecheck = True
				for node in self.nodesets[int(self.gui.new_boundary['Nodeset'])]:
					if node not in self.meshes[self.gui.new_boundary['Mesh']].nodes:
						nodecheck = False
				if nodecheck == True:
					self.meshes[self.gui.new_boundary['Mesh']].nodesets[int(self.gui.new_boundary['Nodeset'])] = \
																		list(self.nodesets[int(self.gui.new_boundary['Nodeset'])].keys())
					self.meshes[self.gui.new_boundary['Mesh']].solutions[self.gui.new_boundary['Solution']] \
						['Boundaries'][self.gui.new_boundary['Name']] = { 'Nodeset': self.gui.new_boundary['Nodeset'],
							'Displacement': self.gui.new_boundary['Displacement'], 'Type': self.gui.new_boundary['Type']}
					DOFs = []
					current = ''
					count = 0
					for i in self.gui.new_boundary['DOFs']:
						if i == ',':
							DOFs.append(int(current))
							current = ''
							count += 1
						elif count == (len(self.gui.new_boundary['DOFs'])-1):
							current += i
							DOFs.append(int(current))
						else:
							current += i
							count += 1
					self.meshes[self.gui.new_boundary['Mesh']].solutions[self.gui.new_boundary['Solution']] \
						['Boundaries'][self.gui.new_boundary['Name']]['DOFs'] = DOFs
					print('\n\tDisplacement boundary applied to nodeset',end=' ')
					print(int(self.gui.new_boundary['Nodeset']), 'in', self.gui.new_boundary['Mesh'])
					print('\tBoundaries in ('+self.gui.new_boundary['Mesh']+'):')
					print('\t', self.meshes[self.gui.new_boundary['Mesh']].solutions[self.gui.new_boundary['Solution']]['Boundaries'])
					self.meshes[self.gui.new_boundary['Mesh']].displayLists['solutions'][self.gui.new_boundary['Solution']] \
																	['boundaries'][self.gui.new_boundary['Name']] = glGenLists(1)
					glNewList(self.meshes[self.gui.new_boundary['Mesh']].displayLists['solutions'][self.gui.new_boundary['Solution']] \
																			['boundaries'][self.gui.new_boundary['Name']], GL_COMPILE)
					glPointSize(13.0)
					glBegin(GL_POINTS)
					glColor3f(0.2, 0.4, 0.6)
					for node in self.nodesets[int(self.gui.new_boundary['Nodeset'])]:
						glVertex3f(self.nodesets[int(self.gui.new_boundary['Nodeset'])][node].coord[0][0], 
								   self.nodesets[int(self.gui.new_boundary['Nodeset'])][node].coord[1][0], 
								   self.nodesets[int(self.gui.new_boundary['Nodeset'])][node].coord[2][0])
					glEnd()
					glLineWidth(9.0)
					for DOF in DOFs:
						for node in self.nodesets[int(self.gui.new_boundary['Nodeset'])]:
							glBegin(GL_LINES)
							glColor3f(0.2, 0.4, 0.6)
							glVertex3f(self.nodesets[int(self.gui.new_boundary['Nodeset'])][node].coord[0][0],
									   self.nodesets[int(self.gui.new_boundary['Nodeset'])][node].coord[1][0], 
									   self.nodesets[int(self.gui.new_boundary['Nodeset'])][node].coord[2][0])
							if DOF == 1:
								glVertex3f(self.nodesets[int(self.gui.new_boundary['Nodeset'])][node].coord[0][0] \
											+0.07*self.meshes[self.gui.new_boundary['Mesh']].viewRadius, 
										   self.nodesets[int(self.gui.new_boundary['Nodeset'])][node].coord[1][0], 
										   self.nodesets[int(self.gui.new_boundary['Nodeset'])][node].coord[2][0])
							elif DOF == 2:
								glVertex3f(self.nodesets[int(self.gui.new_boundary['Nodeset'])][node].coord[0][0],
										   self.nodesets[int(self.gui.new_boundary['Nodeset'])][node].coord[1][0] \
											+0.07*self.meshes[self.gui.new_boundary['Mesh']].viewRadius, 
										   self.nodesets[int(self.gui.new_boundary['Nodeset'])][node].coord[2][0])
							elif DOF == 3:
								glVertex3f(self.nodesets[int(self.gui.new_boundary['Nodeset'])][node].coord[0][0],
										   self.nodesets[int(self.gui.new_boundary['Nodeset'])][node].coord[1][0], 
										   self.nodesets[int(self.gui.new_boundary['Nodeset'])][node].coord[2][0] \
											+0.07*self.meshes[self.gui.new_boundary['Mesh']].viewRadius)
							else:
								pass
							glEnd()
					glEndList()
				else:
					print('\n\tThere are nodes in the nodeset that are not in the selected mesh')
					print('\tNo boundary applied...')
			else:
				print('\n\tNo nodeset by that number ('+self.gui.new_boundary['Nodeset']+').',end=' ')
				print('\tNo boundary applied...')
		else:
			print('\n\t'+self.gui.new_boundary['Nodeset'], 'is not an acceptable input for Nodeset.')
			print('\tNodeset needs to be specified as an integer.')
			print('\tNo boundary applied...')


	def applyLoad(self):
		'''
	Applies load to a selected set of nodes or elements.
	'''
		if self.gui.new_load['Type'] in ['Force', 'ForceConcentrated', 'Dynamic']:
			if self.gui.new_load['Nodeset'].isdigit():
				if int(self.gui.new_load['Nodeset']) in self.nodesets:
					nodecheck = True
					for node in self.nodesets[int(self.gui.new_load['Nodeset'])]:
						if node not in self.meshes[self.gui.new_load['Mesh']].nodes:
							nodecheck = False
					if nodecheck == True:
						self.meshes[self.gui.new_load['Mesh']].nodesets[int(self.gui.new_load['Nodeset'])] = \
																			list(self.nodesets[int(self.gui.new_load['Nodeset'])].keys())
						if self.gui.new_load['Type'] == 'Dynamic':
							self.gui.new_load['Force'] = self.gui.new_load['Force/Acceleration']
							self.gui.new_load['Type'] = self.gui.new_load['Load Type']
						self.meshes[self.gui.new_load['Mesh']].solutions[self.gui.new_load['Solution']] \
							['Loads'][self.gui.new_load['Name']] = {'Nodeset': self.gui.new_load['Nodeset'],
								'Force': self.gui.new_load['Force'], 'x-vector': self.gui.new_load['x-vector'],
								'y-vector': self.gui.new_load['y-vector'], 'z-vector': self.gui.new_load['z-vector'],
								'Type': self.gui.new_load['Type']}
						print('\n\t', self.gui.new_load['Type'], 'load applied to nodeset',end=' ')
						print(int(self.gui.new_load['Nodeset']), 'in', self.gui.new_load['Mesh'])
						print('\tLoads in ('+self.gui.new_load['Mesh']+'):')
						print('\t', self.meshes[self.gui.new_load['Mesh']].solutions[self.gui.new_load['Solution']]['Loads'])

						self.meshes[self.gui.new_load['Mesh']].displayLists['solutions'][self.gui.new_load['Solution']] \
																		['loads'][self.gui.new_load['Name']] = glGenLists(1)
						glNewList(self.meshes[self.gui.new_load['Mesh']].displayLists['solutions'][self.gui.new_load['Solution']] \
																				['loads'][self.gui.new_load['Name']], GL_COMPILE)
						glLineWidth(9.0)
						for node in self.nodesets[int(self.gui.new_load['Nodeset'])]:
							glBegin(GL_LINES)
							glColor3f(0.7, 0.15, 0.15)
							glVertex3f(self.nodesets[int(self.gui.new_load['Nodeset'])][node].coord[0][0],
									   self.nodesets[int(self.gui.new_load['Nodeset'])][node].coord[1][0], 
									   self.nodesets[int(self.gui.new_load['Nodeset'])][node].coord[2][0])
							x = float(self.gui.new_load['x-vector'])
							y = float(self.gui.new_load['y-vector'])
							z = float(self.gui.new_load['z-vector'])
							max_xyz = max(abs(x),abs(y),abs(z))
							if max_xyz == 0.:
								max_xyz = 0.1
							x = -x/max_xyz
							y = -y/max_xyz
							z = -z/max_xyz
							glVertex3f(self.nodesets[int(self.gui.new_load['Nodeset'])][node].coord[0][0] \
										+x*0.1*self.meshes[self.gui.new_load['Mesh']].viewRadius, 
									   self.nodesets[int(self.gui.new_load['Nodeset'])][node].coord[1][0] \
										+y*0.1*self.meshes[self.gui.new_load['Mesh']].viewRadius, 
									   self.nodesets[int(self.gui.new_load['Nodeset'])][node].coord[2][0] \
										+z*0.1*self.meshes[self.gui.new_load['Mesh']].viewRadius)
							glEnd()
							angle = np.pi/4
							if (x == 0) and (y == 0):
								x_arrow = x*np.cos(angle) - z*np.sin(angle)
								y_arrow = y
								z_arrow = x*np.sin(angle) + z*np.cos(angle)
							else:
								x_arrow = x*np.cos(angle) - y*np.sin(angle)
								y_arrow = x*np.sin(angle) + y*np.cos(angle)
								z_arrow = z
							glBegin(GL_LINES)
							glColor3f(0.7, 0.15, 0.15)
							glVertex3f(self.nodesets[int(self.gui.new_load['Nodeset'])][node].coord[0][0],
									   self.nodesets[int(self.gui.new_load['Nodeset'])][node].coord[1][0], 
									   self.nodesets[int(self.gui.new_load['Nodeset'])][node].coord[2][0])
							glVertex3f(self.nodesets[int(self.gui.new_load['Nodeset'])][node].coord[0][0] \
										+x_arrow*0.02*self.meshes[self.gui.new_load['Mesh']].viewRadius, 
									   self.nodesets[int(self.gui.new_load['Nodeset'])][node].coord[1][0] \
										+y_arrow*0.02*self.meshes[self.gui.new_load['Mesh']].viewRadius, 
									   self.nodesets[int(self.gui.new_load['Nodeset'])][node].coord[2][0] \
										+z_arrow*0.02*self.meshes[self.gui.new_load['Mesh']].viewRadius)
							glEnd()
							angle = -np.pi/4
							if (x == 0) and (y == 0):
								x_arrow = x*np.cos(angle) - z*np.sin(angle)
								y_arrow = y
								z_arrow = x*np.sin(angle) + z*np.cos(angle)
							else:
								x_arrow = x*np.cos(angle) - y*np.sin(angle)
								y_arrow = x*np.sin(angle) + y*np.cos(angle)
								z_arrow = z
							glBegin(GL_LINES)
							glColor3f(0.7, 0.15, 0.15)
							glVertex3f(self.nodesets[int(self.gui.new_load['Nodeset'])][node].coord[0][0],
									   self.nodesets[int(self.gui.new_load['Nodeset'])][node].coord[1][0], 
									   self.nodesets[int(self.gui.new_load['Nodeset'])][node].coord[2][0])
							glVertex3f(self.nodesets[int(self.gui.new_load['Nodeset'])][node].coord[0][0] \
										+x_arrow*0.02*self.meshes[self.gui.new_load['Mesh']].viewRadius, 
									   self.nodesets[int(self.gui.new_load['Nodeset'])][node].coord[1][0] \
										+y_arrow*0.02*self.meshes[self.gui.new_load['Mesh']].viewRadius, 
									   self.nodesets[int(self.gui.new_load['Nodeset'])][node].coord[2][0] \
										+z_arrow*0.02*self.meshes[self.gui.new_load['Mesh']].viewRadius)
							glEnd()
						glEndList()
					else:
						print('\n\tThere are nodes in the nodeset that are not in the selected mesh')
						print('\tNo load applied...')
				else:
					print('\n\tNo nodeset by that number ('+self.gui.new_load['Nodeset']+').',end=' ')
					print('\tNo load applied...')
			else:
				print('\n\t'+self.gui.new_load['Nodeset'], 'is not an acceptable input for Nodeset.')
				print('\tNodeset needs to be specified as an integer.')
				print('\tNo load applied...')

		elif self.gui.new_load['Type'] == 'ForceDistributed':
			if self.gui.new_load['Elementset'].isdigit():
				if int(self.gui.new_load['Elementset']) in self.elementsets:
					elementcheck = True
					elementtypecheck = True
					for element in self.elementsets[int(self.gui.new_load['Elementset'])]:
						if element not in self.meshes[self.gui.new_load['Mesh']].elements:
							elementcheck = False
						else:
							if self.meshes[self.gui.new_load['Mesh']].elements[element].type not in ['BEAM2N2D', 'BEAM2N']:
								elementtypecheck = False
					if elementcheck == True:
						if elementtypecheck == True:
							self.meshes[self.gui.new_load['Mesh']].elementsets[int(self.gui.new_load['Elementset'])] = \
																				list(self.elementsets[int(self.gui.new_load['Elementset'])].keys())
							self.meshes[self.gui.new_load['Mesh']].solutions[self.gui.new_load['Solution']] \
								['Loads'][self.gui.new_load['Name']] = {'Elementset': self.gui.new_load['Elementset'],
								 'Force/Length': self.gui.new_load['Force/Length'], 'x-vector': self.gui.new_load['x-vector'],
								 'y-vector': self.gui.new_load['y-vector'], 'z-vector': self.gui.new_load['z-vector'],
								 'Type': self.gui.new_load['Type']}
							print('\n\t', self.gui.new_load['Type'], 'load applied to elementset',end=' ')
							print(int(self.gui.new_load['Elementset']), 'in', self.gui.new_load['Mesh'])
							print('\tLoads in ('+self.gui.new_load['Mesh']+'):')
							print('\t', self.meshes[self.gui.new_load['Mesh']].solutions[self.gui.new_load['Solution']]['Loads'])

							self.meshes[self.gui.new_load['Mesh']].displayLists['solutions'][self.gui.new_load['Solution']] \
																			['loads'][self.gui.new_load['Name']] = glGenLists(1)
							glNewList(self.meshes[self.gui.new_load['Mesh']].displayLists['solutions'][self.gui.new_load['Solution']] \
																					['loads'][self.gui.new_load['Name']], GL_COMPILE)
							glLineWidth(9.0)
							glColor3f(0.7, 0.15, 0.15)
							for element in self.elementsets[int(self.gui.new_load['Elementset'])]:
								n1 = []
								n2 = []
								for i, node in enumerate(self.meshes[self.gui.new_load['Mesh']].elements[element].nodes):
									glBegin(GL_LINES)
									glVertex3f(node.coord[0][0], node.coord[1][0], node.coord[2][0])
									x = float(self.gui.new_load['x-vector'])
									y = float(self.gui.new_load['y-vector'])
									z = float(self.gui.new_load['z-vector'])
									max_xyz = max(abs(x),abs(y),abs(z))
									if max_xyz == 0.:
										max_xyz = 0.1
									x = -x/max_xyz
									y = -y/max_xyz
									z = -z/max_xyz
									glVertex3f(node.coord[0][0] + x*0.1*self.meshes[self.gui.new_load['Mesh']].viewRadius, 
											   node.coord[1][0] + y*0.1*self.meshes[self.gui.new_load['Mesh']].viewRadius, 
											   node.coord[2][0] + z*0.1*self.meshes[self.gui.new_load['Mesh']].viewRadius)
									glEnd()
									angle = np.pi/4
									if (x == 0) and (y == 0):
										x_arrow = x*np.cos(angle) - z*np.sin(angle)
										y_arrow = y
										z_arrow = x*np.sin(angle) + z*np.cos(angle)
									else:
										x_arrow = x*np.cos(angle) - y*np.sin(angle)
										y_arrow = x*np.sin(angle) + y*np.cos(angle)
										z_arrow = z
									glBegin(GL_LINES)
									glVertex3f(node.coord[0][0], node.coord[1][0], node.coord[2][0])
									glVertex3f(node.coord[0][0] + x_arrow*0.02*self.meshes[self.gui.new_load['Mesh']].viewRadius, 
											   node.coord[1][0] + y_arrow*0.02*self.meshes[self.gui.new_load['Mesh']].viewRadius, 
											   node.coord[2][0] + z_arrow*0.02*self.meshes[self.gui.new_load['Mesh']].viewRadius)
									glEnd()
									angle = -np.pi/4
									if (x == 0) and (y == 0):
										x_arrow = x*np.cos(angle) - z*np.sin(angle)
										y_arrow = y
										z_arrow = x*np.sin(angle) + z*np.cos(angle)
									else:
										x_arrow = x*np.cos(angle) - y*np.sin(angle)
										y_arrow = x*np.sin(angle) + y*np.cos(angle)
										z_arrow = z
									glBegin(GL_LINES)
									glVertex3f(node.coord[0][0], node.coord[1][0], node.coord[2][0])
									glVertex3f(node.coord[0][0] + x_arrow*0.02*self.meshes[self.gui.new_load['Mesh']].viewRadius, 
											   node.coord[1][0] + y_arrow*0.02*self.meshes[self.gui.new_load['Mesh']].viewRadius, 
											   node.coord[2][0] + z_arrow*0.02*self.meshes[self.gui.new_load['Mesh']].viewRadius)
									glEnd()
									if i == 0:
										n1 = [node.coord[0][0] + x*0.1*self.meshes[self.gui.new_load['Mesh']].viewRadius, 
											  node.coord[1][0] + y*0.1*self.meshes[self.gui.new_load['Mesh']].viewRadius, 
											  node.coord[2][0] + z*0.1*self.meshes[self.gui.new_load['Mesh']].viewRadius]
									else:
										n2 = [node.coord[0][0] + x*0.1*self.meshes[self.gui.new_load['Mesh']].viewRadius, 
											  node.coord[1][0] + y*0.1*self.meshes[self.gui.new_load['Mesh']].viewRadius, 
											  node.coord[2][0] + z*0.1*self.meshes[self.gui.new_load['Mesh']].viewRadius]
								glBegin(GL_LINES)
								glVertex3f(n1[0], n1[1], n1[2])
								glVertex3f(n2[0], n2[1], n2[2])
								glEnd()
							glEndList()
						else:
							print('\n\tThere are elements in the elementset which are not BEAM2N or BEAM2N2D elements.')
							print('\tNo load applied...')
					else:
						print('\n\tThere are elements in the nodeset which are not in the selected mesh')
						print('\tNo load applied...')
				else:
					print('\n\tNo elementset by that number ('+self.gui.new_load['Elementset']+').',end=' ')
					print('\tNo load applied...')
			else:
				print('\n\t'+self.gui.new_load['Elementset'], 'is not an acceptable input for Elementset.')
				print('\tElementset needs to be specified as an integer.')
				print('\tNo load applied...')

		elif self.gui.new_load['Type'] == 'Torque':
			if self.gui.new_load['Nodeset'].isdigit():
				if int(self.gui.new_load['Nodeset']) in self.nodesets:
					nodecheck = True
					for node in self.nodesets[int(self.gui.new_load['Nodeset'])]:
						if node not in self.meshes[self.gui.new_load['Mesh']].nodes:
							nodecheck = False
					if nodecheck == True:
						self.meshes[self.gui.new_load['Mesh']].nodesets[int(self.gui.new_load['Nodeset'])] = \
																			list(self.nodesets[int(self.gui.new_load['Nodeset'])].keys())
						self.meshes[self.gui.new_load['Mesh']].solutions[self.gui.new_load['Solution']] \
							['Loads'][self.gui.new_load['Name']] = {'Nodeset': self.gui.new_load['Nodeset'],
								'Torque': self.gui.new_load['Torque'], 'x-vector': self.gui.new_load['mx-vector'],
								'y-vector': self.gui.new_load['my-vector'], 'z-vector': self.gui.new_load['mz-vector'],
								'Type': self.gui.new_load['Type']}
						print('\n\t', self.gui.new_load['Type'], 'load applied to nodeset',end=' ')
						print(int(self.gui.new_load['Nodeset']), 'in', self.gui.new_load['Mesh'])
						print('\tLoads in ('+self.gui.new_load['Mesh']+'):')
						print('\t', self.meshes[self.gui.new_load['Mesh']].solutions[self.gui.new_load['Solution']]['Loads'])

						self.meshes[self.gui.new_load['Mesh']].displayLists['solutions'][self.gui.new_load['Solution']] \
																		['loads'][self.gui.new_load['Name']] = glGenLists(1)
						glNewList(self.meshes[self.gui.new_load['Mesh']].displayLists['solutions'][self.gui.new_load['Solution']] \
																				['loads'][self.gui.new_load['Name']], GL_COMPILE)
						glLineWidth(9.0)
						for node in self.nodesets[int(self.gui.new_load['Nodeset'])]:

							origin = [ self.nodesets[int(self.gui.new_load['Nodeset'])][node].coord[0][0],
									   self.nodesets[int(self.gui.new_load['Nodeset'])][node].coord[1][0], 
									   self.nodesets[int(self.gui.new_load['Nodeset'])][node].coord[2][0] ]
							length = np.sqrt((float(self.gui.new_load['mx-vector'])**2) + \
											 (float(self.gui.new_load['my-vector'])**2) + \
											 (float(self.gui.new_load['mz-vector'])**2))
							mx = float(self.gui.new_load['mx-vector'])
							my = float(self.gui.new_load['my-vector'])
							mz = float(self.gui.new_load['mz-vector'])

							if abs(mx) < 0.001 and abs(my) > 0.001:
								n1_offset = np.array([origin[0]-1, origin[1], origin[2]])
								n2_offset = np.array([origin[0]+mx-1, origin[1]+my, origin[2]+mz])
							else:
								n1_offset = np.array([origin[0], origin[1]+1, origin[2]])
								n2_offset = np.array([origin[0]+mx, origin[1]+my+1, origin[2]+mz])
							mv = np.array([mx, my, mz])
							xu = mv/length
							n_offset = n1_offset + 0.5*(n2_offset-n1_offset)
							ov = n_offset - np.array([origin[0],origin[1],origin[2]])
							yv = ov - np.dot(ov,xu)*xu
							mag = sqrt(yv[0]**2 + yv[1]**2 + yv[2]**2)
							if mag == 0.:
								yu = yv
							else:
								yu = yv/mag
							zu = np.cross(xu, yu)

							scale = 0.1*self.meshes[self.gui.new_load['Mesh']].viewRadius
							vertices = []
							arrow = []
							for v in range(18):
								d = 24/(v+1)
								vc = np.cos(2*np.pi/d)
								vs = np.sin(2*np.pi/d)
								vertices.append([ origin[0]+vs*yu[0]*scale+vc*zu[0]*scale,
												  origin[1]+vs*yu[1]*scale+vc*zu[1]*scale,
												  origin[2]+vs*yu[2]*scale+vc*zu[2]*scale ])
								if v == 1:
									arrow.append([ origin[0]+vs*yu[0]*1.3*scale+vc*zu[0]*1.3*scale,
												   origin[1]+vs*yu[1]*1.3*scale+vc*zu[1]*1.3*scale,
												   origin[2]+vs*yu[2]*1.3*scale+vc*zu[2]*1.3*scale ])
									arrow.append([ origin[0]+vs*yu[0]*0.7*scale+vc*zu[0]*0.7*scale,
												   origin[1]+vs*yu[1]*0.7*scale+vc*zu[1]*0.7*scale,
												   origin[2]+vs*yu[2]*0.7*scale+vc*zu[2]*0.7*scale ])
							glColor3f(0.7, 0.15, 0.15)
							for v in range(17):
								glBegin(GL_LINES)
								glVertex3f(vertices[v][0],vertices[v][1],vertices[v][2])
								glVertex3f(vertices[v+1][0],vertices[v+1][1],vertices[v+1][2])
								glEnd()
							glBegin(GL_LINES)
							glVertex3f(vertices[0][0],vertices[0][1],vertices[0][2])
							glVertex3f(arrow[0][0],arrow[0][1],arrow[0][2])
							glEnd()
							glBegin(GL_LINES)
							glVertex3f(vertices[0][0],vertices[0][1],vertices[0][2])
							glVertex3f(arrow[1][0],arrow[1][1],arrow[1][2])
							glEnd()

							glBegin(GL_LINES)
							glColor3f(0.7, 0.15, 0.15)
							glVertex3f(self.nodesets[int(self.gui.new_load['Nodeset'])][node].coord[0][0],
									   self.nodesets[int(self.gui.new_load['Nodeset'])][node].coord[1][0], 
									   self.nodesets[int(self.gui.new_load['Nodeset'])][node].coord[2][0])
							x = float(self.gui.new_load['mx-vector'])
							y = float(self.gui.new_load['my-vector'])
							z = float(self.gui.new_load['mz-vector'])
							max_xyz = max(abs(x),abs(y),abs(z))
							if max_xyz == 0.:
								max_xyz = 0.1
							x = -x/max_xyz
							y = -y/max_xyz
							z = -z/max_xyz
							glVertex3f(self.nodesets[int(self.gui.new_load['Nodeset'])][node].coord[0][0] \
										+x*0.1*self.meshes[self.gui.new_load['Mesh']].viewRadius, 
									   self.nodesets[int(self.gui.new_load['Nodeset'])][node].coord[1][0] \
										+y*0.1*self.meshes[self.gui.new_load['Mesh']].viewRadius, 
									   self.nodesets[int(self.gui.new_load['Nodeset'])][node].coord[2][0] \
										+z*0.1*self.meshes[self.gui.new_load['Mesh']].viewRadius)
							glEnd()
							angle = np.pi/4
							if (x == 0) and (y == 0):
								x_arrow = x*np.cos(angle) - z*np.sin(angle)
								y_arrow = y
								z_arrow = x*np.sin(angle) + z*np.cos(angle)
							else:
								x_arrow = x*np.cos(angle) - y*np.sin(angle)
								y_arrow = x*np.sin(angle) + y*np.cos(angle)
								z_arrow = z
							glBegin(GL_LINES)
							glColor3f(0.7, 0.15, 0.15)
							glVertex3f(self.nodesets[int(self.gui.new_load['Nodeset'])][node].coord[0][0],
									   self.nodesets[int(self.gui.new_load['Nodeset'])][node].coord[1][0], 
									   self.nodesets[int(self.gui.new_load['Nodeset'])][node].coord[2][0])
							glVertex3f(self.nodesets[int(self.gui.new_load['Nodeset'])][node].coord[0][0] \
										+x_arrow*0.02*self.meshes[self.gui.new_load['Mesh']].viewRadius, 
									   self.nodesets[int(self.gui.new_load['Nodeset'])][node].coord[1][0] \
										+y_arrow*0.02*self.meshes[self.gui.new_load['Mesh']].viewRadius, 
									   self.nodesets[int(self.gui.new_load['Nodeset'])][node].coord[2][0] \
										+z_arrow*0.02*self.meshes[self.gui.new_load['Mesh']].viewRadius)
							glEnd()
							angle = np.pi/4
							if (x == 0) and (y == 0):
								x_arrow = x*np.cos(angle) - z*np.sin(angle)
								y_arrow = y
								z_arrow = x*np.sin(angle) + z*np.cos(angle)
							else:
								x_arrow = x*np.cos(angle) - y*np.sin(angle)
								y_arrow = x*np.sin(angle) + y*np.cos(angle)
								z_arrow = z
							glBegin(GL_LINES)
							glColor3f(0.7, 0.15, 0.15)
							glVertex3f(self.nodesets[int(self.gui.new_load['Nodeset'])][node].coord[0][0] \
										+x*0.02*self.meshes[self.gui.new_load['Mesh']].viewRadius, 
									   self.nodesets[int(self.gui.new_load['Nodeset'])][node].coord[1][0] \
										+y*0.02*self.meshes[self.gui.new_load['Mesh']].viewRadius, 
									   self.nodesets[int(self.gui.new_load['Nodeset'])][node].coord[2][0] \
										+z*0.02*self.meshes[self.gui.new_load['Mesh']].viewRadius)
							glVertex3f(self.nodesets[int(self.gui.new_load['Nodeset'])][node].coord[0][0] \
										+x*0.02*self.meshes[self.gui.new_load['Mesh']].viewRadius \
										+x_arrow*0.02*self.meshes[self.gui.new_load['Mesh']].viewRadius, 
									   self.nodesets[int(self.gui.new_load['Nodeset'])][node].coord[1][0] \
										+y*0.02*self.meshes[self.gui.new_load['Mesh']].viewRadius \
										+y_arrow*0.02*self.meshes[self.gui.new_load['Mesh']].viewRadius, 
									   self.nodesets[int(self.gui.new_load['Nodeset'])][node].coord[2][0] \
										+z*0.02*self.meshes[self.gui.new_load['Mesh']].viewRadius \
										+z_arrow*0.02*self.meshes[self.gui.new_load['Mesh']].viewRadius)
							glEnd()
						glEndList()
					else:
						print('\n\tThere are nodes in the nodeset that are not in the selected mesh')
						print('\tNo load applied...')
				else:
					print('\n\tNo nodeset by that number ('+self.gui.new_load['Nodeset']+').',end=' ')
					print('\tNo load applied...')
			else:
				print('\n\t'+self.gui.new_load['Nodeset'], 'is not an acceptable input for Nodeset.')
				print('\tNodeset needs to be specified as an integer.')
				print('\tNo load applied...')

		elif self.gui.new_load['Type'] == 'Gravity':
			if self.gui.new_load['Elementset'].isdigit():
				if int(self.gui.new_load['Elementset']) in self.elementsets:
					elementcheck = True
					for element in self.elementsets[int(self.gui.new_load['Elementset'])]:
						if element not in self.meshes[self.gui.new_load['Mesh']].elements:
							elementcheck = False
					if elementcheck == True:
						self.meshes[self.gui.new_load['Mesh']].elementsets[int(self.gui.new_load['Elementset'])] = \
																			list(self.elementsets[int(self.gui.new_load['Elementset'])].keys())
						self.meshes[self.gui.new_load['Mesh']].solutions[self.gui.new_load['Solution']] \
							['Loads'][self.gui.new_load['Name']] = {'Elementset': self.gui.new_load['Elementset'],
								'Acceleration': self.gui.new_load['Acceleration'], 'x-vector': self.gui.new_load['x-vector'],
								'y-vector': self.gui.new_load['y-vector'], 'z-vector': self.gui.new_load['z-vector'],
								'Type': self.gui.new_load['Type']}
						print('\n\t', self.gui.new_load['Type'], 'load applied to elementset',end=' ')
						print(int(self.gui.new_load['Elementset']), 'in', self.gui.new_load['Mesh'])
						print('\tLoads in ('+self.gui.new_load['Mesh']+'):')
						print('\t', self.meshes[self.gui.new_load['Mesh']].solutions[self.gui.new_load['Solution']]['Loads'])

						self.meshes[self.gui.new_load['Mesh']].displayLists['solutions'][self.gui.new_load['Solution']] \
																		['loads'][self.gui.new_load['Name']] = glGenLists(1)
						glNewList(self.meshes[self.gui.new_load['Mesh']].displayLists['solutions'][self.gui.new_load['Solution']] \
																				['loads'][self.gui.new_load['Name']], GL_COMPILE)
						number_of_elements = len(self.elementsets[int(self.gui.new_load['Elementset'])])
						number_of_load_arrows = 0
						all_elements = False
						if number_of_elements < 12:
							all_elements = True
						else:
							number_of_load_arrows = number_of_elements/4
						glLineWidth(9.0)
						glColor3f(0.7, 0.15, 0.15)
						count = 0
						for element in self.elementsets[int(self.gui.new_load['Elementset'])]:
							if count == number_of_load_arrows:
								if self.elementsets[int(self.gui.new_load['Elementset'])][element].type in ['ROD2N','ROD2N2D','BEAM2N','BEAM2N2D']:
									start_vector = [self.elementsets[int(self.gui.new_load['Elementset'])][element].nodes[0].coord[0][0] + \
													(self.elementsets[int(self.gui.new_load['Elementset'])][element].nodes[1].coord[0][0] - \
													 self.elementsets[int(self.gui.new_load['Elementset'])][element].nodes[0].coord[0][0])/2., 
												   self.elementsets[int(self.gui.new_load['Elementset'])][element].nodes[0].coord[1][0] + \
													(self.elementsets[int(self.gui.new_load['Elementset'])][element].nodes[1].coord[1][0] - \
													 self.elementsets[int(self.gui.new_load['Elementset'])][element].nodes[0].coord[1][0])/2., 
												   self.elementsets[int(self.gui.new_load['Elementset'])][element].nodes[0].coord[2][0] + \
													(self.elementsets[int(self.gui.new_load['Elementset'])][element].nodes[1].coord[2][0] - \
													 self.elementsets[int(self.gui.new_load['Elementset'])][element].nodes[0].coord[2][0])/2.]
								elif self.elementsets[int(self.gui.new_load['Elementset'])][element].type in ['TRI3N','TRI6N']:
									start_vector = [self.elementsets[int(self.gui.new_load['Elementset'])][element].nodes[0].coord[0][0] + \
													(self.elementsets[int(self.gui.new_load['Elementset'])][element].nodes[1].coord[0][0] - \
													 self.elementsets[int(self.gui.new_load['Elementset'])][element].nodes[0].coord[0][0])/3. + \
													(self.elementsets[int(self.gui.new_load['Elementset'])][element].nodes[2].coord[0][0] - \
													 self.elementsets[int(self.gui.new_load['Elementset'])][element].nodes[0].coord[0][0])/3., 
												   self.elementsets[int(self.gui.new_load['Elementset'])][element].nodes[0].coord[1][0] + \
													(self.elementsets[int(self.gui.new_load['Elementset'])][element].nodes[1].coord[1][0] - \
													 self.elementsets[int(self.gui.new_load['Elementset'])][element].nodes[0].coord[1][0])/3. + \
													(self.elementsets[int(self.gui.new_load['Elementset'])][element].nodes[2].coord[1][0] - \
													 self.elementsets[int(self.gui.new_load['Elementset'])][element].nodes[0].coord[1][0])/3., 
												   self.elementsets[int(self.gui.new_load['Elementset'])][element].nodes[0].coord[2][0] + \
													(self.elementsets[int(self.gui.new_load['Elementset'])][element].nodes[1].coord[2][0] - \
													 self.elementsets[int(self.gui.new_load['Elementset'])][element].nodes[0].coord[2][0])/3. + \
													(self.elementsets[int(self.gui.new_load['Elementset'])][element].nodes[2].coord[2][0] - \
													 self.elementsets[int(self.gui.new_load['Elementset'])][element].nodes[0].coord[2][0])/3.]
								elif self.elementsets[int(self.gui.new_load['Elementset'])][element].type in ['TET4N','TET10N']:
									start_vector = [self.elementsets[int(self.gui.new_load['Elementset'])][element].nodes[0].coord[0][0] + \
													(self.elementsets[int(self.gui.new_load['Elementset'])][element].nodes[1].coord[0][0] - \
													 self.elementsets[int(self.gui.new_load['Elementset'])][element].nodes[0].coord[0][0])/3. + \
													(self.elementsets[int(self.gui.new_load['Elementset'])][element].nodes[2].coord[0][0] - \
													 self.elementsets[int(self.gui.new_load['Elementset'])][element].nodes[0].coord[0][0])/3. + \
													(self.elementsets[int(self.gui.new_load['Elementset'])][element].nodes[3].coord[0][0] - \
													 self.elementsets[int(self.gui.new_load['Elementset'])][element].nodes[0].coord[0][0])/3., 
												   self.elementsets[int(self.gui.new_load['Elementset'])][element].nodes[0].coord[1][0] + \
													(self.elementsets[int(self.gui.new_load['Elementset'])][element].nodes[1].coord[1][0] - \
													 self.elementsets[int(self.gui.new_load['Elementset'])][element].nodes[0].coord[1][0])/3. + \
													(self.elementsets[int(self.gui.new_load['Elementset'])][element].nodes[2].coord[1][0] - \
													 self.elementsets[int(self.gui.new_load['Elementset'])][element].nodes[0].coord[1][0])/3. + \
													(self.elementsets[int(self.gui.new_load['Elementset'])][element].nodes[3].coord[1][0] - \
													 self.elementsets[int(self.gui.new_load['Elementset'])][element].nodes[0].coord[1][0])/3., 
												   self.elementsets[int(self.gui.new_load['Elementset'])][element].nodes[0].coord[2][0] + \
													(self.elementsets[int(self.gui.new_load['Elementset'])][element].nodes[1].coord[2][0] - \
													 self.elementsets[int(self.gui.new_load['Elementset'])][element].nodes[0].coord[2][0])/3. + \
													(self.elementsets[int(self.gui.new_load['Elementset'])][element].nodes[2].coord[2][0] - \
													 self.elementsets[int(self.gui.new_load['Elementset'])][element].nodes[0].coord[2][0])/3. + \
													(self.elementsets[int(self.gui.new_load['Elementset'])][element].nodes[3].coord[2][0] - \
													 self.elementsets[int(self.gui.new_load['Elementset'])][element].nodes[0].coord[2][0])/3.]
								elif self.elementsets[int(self.gui.new_load['Elementset'])][element].type == 'QUAD4N':
									start_vector = [self.elementsets[int(self.gui.new_load['Elementset'])][element].nodes[0].coord[0][0] + \
													(self.elementsets[int(self.gui.new_load['Elementset'])][element].nodes[2].coord[0][0] - \
													 self.elementsets[int(self.gui.new_load['Elementset'])][element].nodes[0].coord[0][0])/2., 
												   self.elementsets[int(self.gui.new_load['Elementset'])][element].nodes[0].coord[1][0] + \
													(self.elementsets[int(self.gui.new_load['Elementset'])][element].nodes[2].coord[1][0] - \
													 self.elementsets[int(self.gui.new_load['Elementset'])][element].nodes[0].coord[1][0])/2., 
												   self.elementsets[int(self.gui.new_load['Elementset'])][element].nodes[0].coord[2][0] + \
													(self.elementsets[int(self.gui.new_load['Elementset'])][element].nodes[2].coord[2][0] - \
													 self.elementsets[int(self.gui.new_load['Elementset'])][element].nodes[0].coord[2][0])/2.]
								elif self.elementsets[int(self.gui.new_load['Elementset'])][element].type == 'QUAD8N':
									start_vector = [self.elementsets[int(self.gui.new_load['Elementset'])][element].nodes[0].coord[0][0] + \
													(self.elementsets[int(self.gui.new_load['Elementset'])][element].nodes[4].coord[0][0] - \
													 self.elementsets[int(self.gui.new_load['Elementset'])][element].nodes[0].coord[0][0])/2., 
												   self.elementsets[int(self.gui.new_load['Elementset'])][element].nodes[0].coord[1][0] + \
													(self.elementsets[int(self.gui.new_load['Elementset'])][element].nodes[4].coord[1][0] - \
													 self.elementsets[int(self.gui.new_load['Elementset'])][element].nodes[0].coord[1][0])/2., 
												   self.elementsets[int(self.gui.new_load['Elementset'])][element].nodes[0].coord[2][0] + \
													(self.elementsets[int(self.gui.new_load['Elementset'])][element].nodes[4].coord[2][0] - \
													 self.elementsets[int(self.gui.new_load['Elementset'])][element].nodes[0].coord[2][0])/2.]
								elif self.elementsets[int(self.gui.new_load['Elementset'])][element].type in ['HEX8N','HEX20N']:
									start_vector = [self.elementsets[int(self.gui.new_load['Elementset'])][element].nodes[0].coord[0][0] + \
													(self.elementsets[int(self.gui.new_load['Elementset'])][element].nodes[6].coord[0][0] - \
													 self.elementsets[int(self.gui.new_load['Elementset'])][element].nodes[0].coord[0][0])/2., 
												   self.elementsets[int(self.gui.new_load['Elementset'])][element].nodes[0].coord[1][0] + \
													(self.elementsets[int(self.gui.new_load['Elementset'])][element].nodes[6].coord[1][0] - \
													 self.elementsets[int(self.gui.new_load['Elementset'])][element].nodes[0].coord[1][0])/2., 
												   self.elementsets[int(self.gui.new_load['Elementset'])][element].nodes[0].coord[2][0] + \
													(self.elementsets[int(self.gui.new_load['Elementset'])][element].nodes[6].coord[2][0] - \
													 self.elementsets[int(self.gui.new_load['Elementset'])][element].nodes[0].coord[2][0])/2.]
								else:
									pass

								glBegin(GL_LINES)
								glColor3f(0.7, 0.15, 0.15)
								glVertex3f(start_vector[0], start_vector[1], start_vector[2])
								x = float(self.gui.new_load['x-vector'])
								y = float(self.gui.new_load['y-vector'])
								z = float(self.gui.new_load['z-vector'])
								max_xyz = max(abs(x),abs(y),abs(z))
								if max_xyz == 0.:
									max_xyz = 0.1
								x = -x/max_xyz
								y = -y/max_xyz
								z = -z/max_xyz
								glVertex3f(start_vector[0] - x*0.1*self.meshes[self.gui.new_load['Mesh']].viewRadius, 
										   start_vector[1] - y*0.1*self.meshes[self.gui.new_load['Mesh']].viewRadius, 
										   start_vector[2] - z*0.1*self.meshes[self.gui.new_load['Mesh']].viewRadius)
								glEnd()
								angle = [np.pi/4, -np.pi/4]
								if (x == 0) and (y == 0):
									x_arrow = [x*np.cos(angle[0]) - z*np.sin(angle[0]), x*np.cos(angle[1]) - z*np.sin(angle[1])]
									y_arrow = [y, y]
									z_arrow = [x*np.sin(angle[0]) + z*np.cos(angle[0]), x*np.sin(angle[1]) + z*np.cos(angle[1])]
								else:
									x_arrow = [x*np.cos(angle[0]) - y*np.sin(angle[0]), x*np.cos(angle[1]) - y*np.sin(angle[1])]
									y_arrow = [x*np.sin(angle[0]) + y*np.cos(angle[0]), x*np.sin(angle[0]) + y*np.cos(angle[0])]
									z_arrow = [z, z]
								for i in range(2):
									glBegin(GL_LINES)
									glColor3f(0.7, 0.15, 0.15)
									glVertex3f(start_vector[0] - x*0.1*self.meshes[self.gui.new_load['Mesh']].viewRadius, 
											   start_vector[1] - y*0.1*self.meshes[self.gui.new_load['Mesh']].viewRadius, 
											   start_vector[2] - z*0.1*self.meshes[self.gui.new_load['Mesh']].viewRadius)
									glVertex3f(start_vector[0] - x*0.1*self.meshes[self.gui.new_load['Mesh']].viewRadius \
												+x_arrow[i]*0.02*self.meshes[self.gui.new_load['Mesh']].viewRadius, 
											   start_vector[1] - y*0.1*self.meshes[self.gui.new_load['Mesh']].viewRadius \
												+y_arrow[i]*0.02*self.meshes[self.gui.new_load['Mesh']].viewRadius, 
											   start_vector[2] - z*0.1*self.meshes[self.gui.new_load['Mesh']].viewRadius \
												+z_arrow[i]*0.02*self.meshes[self.gui.new_load['Mesh']].viewRadius)
									glEnd()
								if all_elements:
									number_of_load_arrows += 1
								else:
									number_of_load_arrows += 4
							else:
								pass
							count += 1
						glEndList()
					else:
						print('\n\tThere are elements in the elementset that are not in the selected mesh')
						print('\tNo load applied...')
				else:
					print('\n\tNo elementset by that number ('+self.gui.new_load['Elementset']+').',end=' ')
					print('\tNo load applied...')
			else:
				print('\n\t'+self.gui.new_load['Elementset'], 'is not an acceptable input for Elementset.')
				print('\tElementset needs to be specified as an integer.')
				print('\tNo load applied...')
			
		else:
			pass


	def writeSolFile(self,mesh):
		'''
	Writes *.sol-file for the solFEM module.
	'''
		if not self.meshes[mesh].sections_applied:
			print('\n\tMust apply section to all elements in mesh.')
			print('\tNo *.sol-file written.')
			return

		# check elements for specified beam orientation and
		# create new element sets for the ones that have one
		beam_orients = {}
		for element in self.meshes[mesh].elements:
			if hasattr(self.meshes[mesh].elements[element],'orientation'):
				if len(beam_orients) == 0:
					beam_orients['beams-'+str(len(beam_orients)+1)] = {'elements': {element: self.meshes[mesh].elements[element]},
																	   'x-vec': self.meshes[mesh].elements[element].orientation['x-vec'],
																	   'y-vec': self.meshes[mesh].elements[element].orientation['y-vec'],
																	   'type': self.meshes[mesh].elements[element].type}
				else:
					same = False
					for beams in beam_orients:
						if beam_orients[beams]['x-vec'].dot(self.meshes[mesh].elements[element].orientation['x-vec']) in [-1., 1.] and \
								beam_orients[beams]['y-vec'].dot(self.meshes[mesh].elements[element].orientation['y-vec']) in [-1., 1.] and \
								self.meshes[mesh].elements[element].type == beam_orients[beams]['type']:
							beam_orients[beams]['elements'][element] = self.meshes[mesh].elements[element]
							same = True
					if not same:
						beam_orients['beams-'+str(len(beam_orients)+1)] = {'elements': {element: self.meshes[mesh].elements[element]},
																		   'x-vec': self.meshes[mesh].elements[element].orientation['x-vec'],
																		   'y-vec': self.meshes[mesh].elements[element].orientation['y-vec'],
																		   'type': self.meshes[mesh].elements[element].type}
		for beams in beam_orients:
			beam_orients[beams]['elementset'] = max(self.elementsets)+1
			self.elementsets[max(self.elementsets)+1] = beam_orients[beams]['elements']

		nodeset_all = self.meshes[mesh].nodes.keys()
		nodeset_all = sorted(nodeset_all)
		nodeset_all_number = 999
		nodeset_all_exists = False
		for nodeset in self.nodesets:
			tmpset = self.nodesets[nodeset].keys()
			if nodeset_all == sorted(tmpset):
				nodeset_all_number = nodeset
				nodeset_all_exists = True
		if not nodeset_all_exists:
			self.nodesets[999] = {}
			for node in self.meshes[mesh].nodes:
				self.nodesets[999][node] = self.meshes[mesh].nodes[node]

		elementset_all = self.meshes[mesh].elements.keys()
		elementset_all = sorted(elementset_all)
		elementset_all_number = 999
		elementset_all_exists = False
		for elementset in self.elementsets:
			tmpset = self.elementsets[elementset].keys()
			if elementset_all == sorted(tmpset):
				elementset_all_number = elementset
				elementset_all_exists = True
		if not elementset_all_exists:
			self.elementsets[999] = {}
			for element in self.meshes[mesh].elements:
				self.elementsets[999][element] = self.meshes[mesh].elements[element]


		# start writing to file
		if os.path.exists(self.gui.new_solfile['Name']+'.sol'):
			print('\n\tOverwriting solution file '+self.gui.new_solfile['Name']+'.sol\n')
		else:
			print('\n\tWriting solfile: '+self.gui.new_solfile['Name']+'.sol')
		fobj = open(self.gui.new_solfile['Name']+'.sol', 'w')

		n_damp = 1
		dampings = {}
		# Write in all the solutions
		for solution in self.gui.new_solfile['Solution']:
			fobj.write('#\n#\n#------------------------------------\n')
			fobj.write('SOLUTION, '+solution+', '+self.meshes[mesh].solutions[solution]['Type']+'\n')
			fobj.write('#------------------------------------\n')
			fobj.write('\tMESHES, '+str(elementset_all_number)+'\n')
			for load in self.meshes[mesh].solutions[solution]['Loads']:
				fobj.write('\tLOADS, '+load+'\n')
			for boundary in self.meshes[mesh].solutions[solution]['Boundaries']:
				fobj.write('\tBOUNDARIES, '+boundary+'\n')
			for constraint in self.meshes[mesh].solutions[solution]['Constraints']:
				fobj.write('\tCONSTRAINTS, '+constraint+'\n')
			if self.meshes[mesh].solutions[solution]['Type'] == 'ModalDynamic':
				fobj.write('\tDAMPINGS, damp_'+str(n_damp)+'\n')
				dampings[solution] = n_damp
				n_damp += 1
			fobj.write('#------------------------------------\n')
			fobj.write('RESULTS, '+solution+'\n')
			fobj.write('#------------------------------------')
			for result in self.gui.new_solfile['Solution'][solution]:
				if result in ['disp', 'velc', 'accl', 'frf', 'nodf']:
					towrite = ''
					if result == 'disp':
						towrite += '\n\tDISPLACEMENT'
					if result == 'velc':
						towrite += '\n\tVELOCITY'
					if result == 'accl':
						towrite += '\n\tACCELERATION'
					if result == 'frf':
						towrite += '\n\tFRF_ACCEL'
					if result == 'nodf':
						towrite += '\n\tNODEFORCE'
					if 'plot' in self.gui.new_solfile['Solution'][solution][result]:
						if self.gui.new_solfile['Solution'][solution][result]['plot'] == 'All':
							towrite += ', plot, '+str(nodeset_all_number)
						else:
							towrite += ', plot, '+str(self.gui.new_solfile['Solution'][solution][result]['plot'])
					if 'text' in self.gui.new_solfile['Solution'][solution][result]:
						if self.gui.new_solfile['Solution'][solution][result]['text'] == 'All':
							towrite += ', text, '+str(nodeset_all_number)
						else:
							towrite += ', text, '+str(self.gui.new_solfile['Solution'][solution][result]['text'])
					if ',' in towrite:
						fobj.write(towrite)
				if result in ['elmf', 'strs', 'strn']:
					towrite = ''
					if result == 'elmf':
						towrite += '\n\tELEMENTFORCE'
					if result == 'strs':
						towrite += '\n\tSTRESS'
					if result == 'strn':
						towrite += '\n\tSTRAIN'
					if 'plot' in self.gui.new_solfile['Solution'][solution][result]:
						if self.gui.new_solfile['Solution'][solution][result]['plot'] == 'All':
							towrite += ', plot, '+str(elementset_all_number)
						else:
							towrite += ', plot, '+str(self.gui.new_solfile['Solution'][solution][result]['plot'])
					if 'text' in self.gui.new_solfile['Solution'][solution][result]:
						if self.gui.new_solfile['Solution'][solution][result]['text'] == 'All':
							towrite += ', text, '+str(elementset_all_number)
						else:
							towrite += ', text, '+str(self.gui.new_solfile['Solution'][solution][result]['text'])
					if ',' in towrite:
						fobj.write(towrite)
				if result == 'modes':
					fobj.write('\n\tMODESHAPES, '+str(self.gui.new_solfile['Solution'][solution][result]['plot']))
			fobj.write('\n#\n#\n')
		fobj.write('#\n#\n#\n')

		# Define materials
		materials = {}
		for section in self.meshes[mesh].sections:
			materials[self.sections[section]['Material']] = self.materials[self.sections[section]['Material']]
		for material in materials:
			fobj.write('MATERIAL, Isotropic, '+material+', '+str(self.materials[material]['Elasticity'])+', '+ \
						str(self.materials[material]['Poisson ratio'])+', '+str(self.materials[material]['Density'])+'\n')
		fobj.write('#\n#\n#\n')

		# Define sections
		for element in self.meshes[mesh].elements:
			if self.meshes[mesh].elements[element].type in ['ROD2N', 'ROD2N2D']:
				self.sections[self.meshes[mesh].elements[element].section]['Type'] = 'RodSect'
			elif self.meshes[mesh].elements[element].type in ['BEAM2N', 'BEAM2N2D']:
				self.sections[self.meshes[mesh].elements[element].section]['Type'] = 'BeamSect'
			elif self.meshes[mesh].elements[element].type in ['TRI3N', 'TRI6N', 'QUAD4N', 'QUAD8N']:
				self.sections[self.meshes[mesh].elements[element].section]['Type'] = 'PlaneSect'
			elif self.meshes[mesh].elements[element].type in ['TET4N', 'TET10N', 'HEX8N', 'HEX20N']:
				self.sections[self.meshes[mesh].elements[element].section]['Type'] = 'SolidSect'
			else:
				print('\n\tSection:', self.meshes[mesh].elements[element].section, 'applied to unknown type of element.')

		for section in self.sections:
			if 'Type' in self.sections[section]:
				fobj.write('SECTION, '+str(self.sections[section]['Type'])+', '+ \
							str(self.sections[section]['Number'])+', '+str(self.sections[section]['Material']))
				if self.sections[section]['Type'] == 'SolidSect':
					pass
				elif self.sections[section]['Type'] == 'RodSect':
					fobj.write(', '+str(self.sections[section]['Area (Rod or Beam)']))
					if 'Cross section' in self.sections[section]:
						fobj.write(', CrossSection, '+str(self.sections[section]['Cross section']['Type']))
						if self.sections[section]['Cross section']['Type'] == 'Rectangle':
							fobj.write(', '+str(self.sections[section]['Cross section']['width, w']))
							fobj.write(', '+str(self.sections[section]['Cross section']['height, h']))
							fobj.write(', '+str(self.sections[section]['Cross section']['inner width, iw']))
							fobj.write(', '+str(self.sections[section]['Cross section']['inner height, ih']))
						elif self.sections[section]['Cross section']['Type'] == 'Circle':
							fobj.write(', '+str(self.sections[section]['Cross section']['radius, r']))
							fobj.write(', '+str(self.sections[section]['Cross section']['inner radius, ir']))
						elif self.sections[section]['Cross section']['Type'] == 'L-Beam':
							fobj.write(', '+str(self.sections[section]['Cross section']['side thickness, st']))
							fobj.write(', '+str(self.sections[section]['Cross section']['bottom width, bw']))
							fobj.write(', '+str(self.sections[section]['Cross section']['bottom thickness, bt']))
							fobj.write(', '+str(self.sections[section]['Cross section']['height, h']))
						elif self.sections[section]['Cross section']['Type'] == 'I-Beam':
							fobj.write(', '+str(self.sections[section]['Cross section']['top width, tw']))
							fobj.write(', '+str(self.sections[section]['Cross section']['top thickness, tt']))
							fobj.write(', '+str(self.sections[section]['Cross section']['middle thickness, mt']))
							fobj.write(', '+str(self.sections[section]['Cross section']['bottom width, bw']))
							fobj.write(', '+str(self.sections[section]['Cross section']['bottom thickness, bt']))
							fobj.write(', '+str(self.sections[section]['Cross section']['height, h']))
						elif self.sections[section]['Cross section']['Type'] == 'C-Beam':
							fobj.write(', '+str(self.sections[section]['Cross section']['top width, tw']))
							fobj.write(', '+str(self.sections[section]['Cross section']['top thickness, tt']))
							fobj.write(', '+str(self.sections[section]['Cross section']['middle thickness, mt']))
							fobj.write(', '+str(self.sections[section]['Cross section']['bottom width, bw']))
							fobj.write(', '+str(self.sections[section]['Cross section']['bottom thickness, bt']))
							fobj.write(', '+str(self.sections[section]['Cross section']['height, h']))
						elif self.sections[section]['Cross section']['Type'] == 'T-Beam':
							fobj.write(', '+str(self.sections[section]['Cross section']['top width, tw']))
							fobj.write(', '+str(self.sections[section]['Cross section']['top thickness, tt']))
							fobj.write(', '+str(self.sections[section]['Cross section']['middle thickness, mt']))
							fobj.write(', '+str(self.sections[section]['Cross section']['height, h']))
				elif self.sections[section]['Type'] == 'BeamSect':
					fobj.write(', '+str(self.sections[section]['Area (Rod or Beam)'])+', '+ \
							str(self.sections[section]['Izz (Beam)'])+', '+str(self.sections[section]['Iyy (Beam 3D)']))
					if 'Cross section' in self.sections[section]:
						fobj.write(', CrossSection, '+str(self.sections[section]['Cross section']['Type']))
						if self.sections[section]['Cross section']['Type'] == 'Rectangle':
							fobj.write(', '+str(self.sections[section]['Cross section']['width, w']))
							fobj.write(', '+str(self.sections[section]['Cross section']['height, h']))
							fobj.write(', '+str(self.sections[section]['Cross section']['inner width, iw']))
							fobj.write(', '+str(self.sections[section]['Cross section']['inner height, ih']))
						elif self.sections[section]['Cross section']['Type'] == 'Circle':
							fobj.write(', '+str(self.sections[section]['Cross section']['radius, r']))
							fobj.write(', '+str(self.sections[section]['Cross section']['inner radius, ir']))
						elif self.sections[section]['Cross section']['Type'] == 'L-Beam':
							fobj.write(', '+str(self.sections[section]['Cross section']['side thickness, st']))
							fobj.write(', '+str(self.sections[section]['Cross section']['bottom width, bw']))
							fobj.write(', '+str(self.sections[section]['Cross section']['bottom thickness, bt']))
							fobj.write(', '+str(self.sections[section]['Cross section']['height, h']))
						elif self.sections[section]['Cross section']['Type'] == 'I-Beam':
							fobj.write(', '+str(self.sections[section]['Cross section']['top width, tw']))
							fobj.write(', '+str(self.sections[section]['Cross section']['top thickness, tt']))
							fobj.write(', '+str(self.sections[section]['Cross section']['middle thickness, mt']))
							fobj.write(', '+str(self.sections[section]['Cross section']['bottom width, bw']))
							fobj.write(', '+str(self.sections[section]['Cross section']['bottom thickness, bt']))
							fobj.write(', '+str(self.sections[section]['Cross section']['height, h']))
						elif self.sections[section]['Cross section']['Type'] == 'C-Beam':
							fobj.write(', '+str(self.sections[section]['Cross section']['top width, tw']))
							fobj.write(', '+str(self.sections[section]['Cross section']['top thickness, tt']))
							fobj.write(', '+str(self.sections[section]['Cross section']['middle thickness, mt']))
							fobj.write(', '+str(self.sections[section]['Cross section']['bottom width, bw']))
							fobj.write(', '+str(self.sections[section]['Cross section']['bottom thickness, bt']))
							fobj.write(', '+str(self.sections[section]['Cross section']['height, h']))
						elif self.sections[section]['Cross section']['Type'] == 'T-Beam':
							fobj.write(', '+str(self.sections[section]['Cross section']['top width, tw']))
							fobj.write(', '+str(self.sections[section]['Cross section']['top thickness, tt']))
							fobj.write(', '+str(self.sections[section]['Cross section']['middle thickness, mt']))
							fobj.write(', '+str(self.sections[section]['Cross section']['height, h']))
				elif self.sections[section]['Type'] == 'PlaneSect':
					fobj.write(', '+str(self.sections[section]['Thickness (2D)']))
				else:
					pass
				fobj.write('\n')
		fobj.write('#\n#\n#\n')

		# Define beam orientations
		for beams in beam_orients:
			fobj.write('BEAMORIENT, '+beam_orients[beams]['type']+', '+beams+', '+str(beam_orients[beams]['elementset'])+ \
						', '+str(beam_orients[beams]['x-vec'][0])+', '+str(beam_orients[beams]['x-vec'][1])+', '+str(beam_orients[beams]['x-vec'][2])+ \
						', '+str(beam_orients[beams]['y-vec'][0])+', '+str(beam_orients[beams]['y-vec'][1])+', '+str(beam_orients[beams]['y-vec'][2]))
			fobj.write('\n')
		fobj.write('#\n#\n#\n')

		# Define constraints
		for solution in self.gui.new_solfile['Solution']:
			for constraint in self.meshes[mesh].solutions[solution]['Constraints']:
				fobj.write('CONSTRAINT, '+self.meshes[mesh].solutions[solution]['Constraints'][constraint]['Type']+', '+constraint)
				fobj.write(', '+str(self.meshes[mesh].solutions[solution]['Constraints'][constraint]['Nodeset1'])+', '+ \
							str(self.meshes[mesh].solutions[solution]['Constraints'][constraint]['Nodeset2']))
				if self.meshes[mesh].solutions[solution]['Constraints'][constraint]['Type'] == 'TouchLock':
					fobj.write(', '+str(self.meshes[mesh].solutions[solution]['Constraints'][constraint]['Tolerance']))
				for dof in self.meshes[mesh].solutions[solution]['Constraints'][constraint]['DOFs']:
					fobj.write(', '+str(dof))
				fobj.write('\n')
		fobj.write('#\n#\n#\n')

		# Define boundaries
		for solution in self.gui.new_solfile['Solution']:
			for boundary in self.meshes[mesh].solutions[solution]['Boundaries']:
				fobj.write('BOUNDARY, '+self.meshes[mesh].solutions[solution]['Boundaries'][boundary]['Type']+', '+ \
				 boundary+', '+str(self.meshes[mesh].solutions[solution]['Boundaries'][boundary]['Nodeset'])+', '+ \
				 str(self.meshes[mesh].solutions[solution]['Boundaries'][boundary]['Displacement']))
				for DOF in range(len(self.meshes[mesh].solutions[solution]['Boundaries'][boundary]['DOFs'])):
					fobj.write(', '+str(self.meshes[mesh].solutions[solution]['Boundaries'][boundary]['DOFs'][DOF]))
				fobj.write('\n')
		fobj.write('#\n#\n#\n')

		# Define loads
		for solution in self.gui.new_solfile['Solution']:
			for load in self.meshes[mesh].solutions[solution]['Loads']:
				fobj.write('LOAD, '+self.meshes[mesh].solutions[solution]['Loads'][load]['Type']+', '+load)
				if self.meshes[mesh].solutions[solution]['Loads'][load]['Type'] == 'Gravity':
					fobj.write(', '+str(self.meshes[mesh].solutions[solution]['Loads'][load]['Elementset'])+', '+ \
								str(self.meshes[mesh].solutions[solution]['Loads'][load]['Acceleration'])+', ')
				elif self.meshes[mesh].solutions[solution]['Loads'][load]['Type'] == 'ForceDistributed':
					fobj.write(', '+str(self.meshes[mesh].solutions[solution]['Loads'][load]['Elementset'])+', '+ \
								str(self.meshes[mesh].solutions[solution]['Loads'][load]['Force/Length'])+', ')
				elif self.meshes[mesh].solutions[solution]['Loads'][load]['Type'] == 'Torque':
					fobj.write(', '+str(self.meshes[mesh].solutions[solution]['Loads'][load]['Nodeset'])+', '+ \
								str(self.meshes[mesh].solutions[solution]['Loads'][load]['Torque'])+', ')
				else:
					fobj.write(', '+str(self.meshes[mesh].solutions[solution]['Loads'][load]['Nodeset'])+', '+ \
								str(self.meshes[mesh].solutions[solution]['Loads'][load]['Force'])+', ')
				fobj.write(str(self.meshes[mesh].solutions[solution]['Loads'][load]['x-vector'])+', '+ \
							str(self.meshes[mesh].solutions[solution]['Loads'][load]['y-vector'])+', '+ \
							str(self.meshes[mesh].solutions[solution]['Loads'][load]['z-vector']))
				fobj.write('\n')
		fobj.write('#\n#\n#\n')
		
		# Dampings if ModalDynamic
		n_damp = 1
		t_damp = {}
		for solution in self.gui.new_solfile['Solution']:
			if self.meshes[mesh].solutions[solution]['Type'] == 'ModalDynamic':
				fobj.write('DAMPING')
				try:
					float(self.gui.new_solfile['Solution'][solution]['dampratio'])
				except ValueError:
					fobj.write(', Frequency, damp_'+str(dampings[solution])+'\n')
					t_damp[solution] = self.gui.new_solfile['Solution'][solution]['dampratio']
				else:
					fobj.write(', Viscous, damp_'+str(dampings[solution])+', '+self.gui.new_solfile['Solution'][solution]['dampratio']+'\n')
		fobj.write('#\n#\n#\n')

		# Tables if ModalDynamic
		tab_num = 1
		for solution in self.gui.new_solfile['Solution']:
			if self.meshes[mesh].solutions[solution]['Type'] == 'ModalDynamic':
				if solution in t_damp:
					fobj.write('TABLE, DampingRatio, '+str(tab_num)+', damp_'+str(dampings[solution])+', '+t_damp[solution]+'\n')
					tab_num += 1
				for load in self.meshes[mesh].solutions[solution]['Loads']:
					fobj.write('TABLE, '+self.meshes[mesh].solutions[solution]['Loads'][load]['Type']+', '+str(tab_num))
					fobj.write(', '+load+', '+self.gui.new_solfile['Solution'][solution]['forcetable']+'\n')
					tab_num += 1
		fobj.write('#\n#\n#\n')

		# List up all nodesets and element sets
		for nodeset in self.nodesets:
			fobj.write('SET_NODES, '+str(nodeset))
			previous = None
			preprevious = None
			summing = False
			stripe = False
			nodes = self.nodesets[nodeset].keys()
			nodes = sorted(nodes)
			for node in nodes:
				if (node-1) == previous:
					if summing == False:
						if node == nodes[-1]:
							fobj.write(', '+str(node))
						else:
							summing = True
					else:
						if (node-2) == preprevious:
							if stripe == False:
								fobj.write(' - ')
								stripe = True
								if node == nodes[-1]:
									fobj.write(str(node))
							elif node == nodes[-1]:
								fobj.write(str(node))
							else:
								pass
						elif node == nodes[-1]:
							fobj.write(str(node))
						else:
							pass
				else:
					if summing == True:
						summing = False
						if (node-2) != preprevious:
							if stripe == True:
								fobj.write(str(previous)+', '+str(node))
							if stripe == False:
								fobj.write(', '+str(previous)+', '+str(node))
						stripe = False
					else:
						fobj.write(', '+str(node))
				preprevious = previous
				previous = node
			fobj.write('\n')
		fobj.write('#\n#\n#\n')

		for elementset in self.elementsets:
			fobj.write('SET_ELEMENTS, '+str(elementset))
			previous = None
			preprevious = None
			summing = False
			stripe = False
			elements = self.elementsets[elementset].keys()
			elements = sorted(elements)
			for element in elements:
				if (element-1) == previous:
					if summing == False:
						if element == elements[-1]:
							fobj.write(', '+str(element))
						else:
							summing = True
					else:
						if (element-2) == preprevious:
							if stripe == False:
								fobj.write(' - ')
								stripe = True
								if element == elements[-1]:
									fobj.write(str(element))
							elif element == elements[-1]:
								fobj.write(str(element))
							else:
								pass
						elif element == elements[-1]:
							fobj.write(str(element))
						else:
							pass
				else:
					if summing == True:
						summing = False
						if (element-2) != preprevious:
							if stripe == True:
								fobj.write(str(previous)+', '+str(element))
							if stripe == False:
								fobj.write(', '+str(previous)+', '+str(element))
						stripe = False
					else:
						fobj.write(', '+str(element))
				preprevious = previous
				previous = element
			fobj.write('\n')
		fobj.write('#\n#\n#\n')

		# Write up all nodes 
		for node in nodeset_all:
			fobj.write('NODE, '+str(node)+', '+str(self.meshes[mesh].nodes[node].coord[0][0])+', '+ \
											   str(self.meshes[mesh].nodes[node].coord[1][0])+', '+ \
											   str(self.meshes[mesh].nodes[node].coord[2][0])+'\n')
		fobj.write('#\n#\n#\n')

		# Write up all elements
		for element in elementset_all:
			fobj.write('ELEMENT, '+self.meshes[mesh].elements[element].type+', '+str(element)+', '+ \
								   str(self.sections[self.meshes[mesh].elements[element].section]['Number']))
			for node in self.meshes[mesh].elements[element].nodes:
				fobj.write(', '+str(node.number))
			fobj.write('\n')
		fobj.write('#\n#\n#\n')

		fobj.close()


	def selectedElementsDisplay(self,mesh):
		'''
	Create a displaylist for the currently selected elements.
	'''
		mesh.displayLists['selected elements'] = glGenLists(1)

		nodes = self.selected_nodes
		elements = self.selected_elements

		glNewList(mesh.displayLists['selected elements'], GL_COMPILE)

		glLineWidth(5.0)
		for j in elements:
			nodelines = []
			if elements[j].type == 'ROD2N2D':
				glLineWidth(8.0)
				nodelines = [[0,1]]
			if elements[j].type == 'ROD2N':
				glLineWidth(8.0)
				nodelines = [[0,1]]
			if elements[j].type == 'BEAM2N2D':
				glLineWidth(8.0)
				nodelines = [[0,1]]
			if elements[j].type == 'BEAM2N':
				glLineWidth(8.0)
				nodelines = [[0,1]]
			if elements[j].type == 'TRI3N':
				nodelines = [[0,1], [1,2], [2,0]]
			if elements[j].type == 'TRI6N':
				nodelines = [[0,3], [3,1], [1,4], [4,2], [2,5], [5,0]]
			if elements[j].type == 'QUAD4N':
				nodelines = [[0,1], [1,2], [2,3], [0,3]]
			if elements[j].type == 'QUAD8N':
				nodelines = [[0,1], [1,2], [2,3], [3,4], [4,5], [5,6], [6,7], [7,0]]
			if elements[j].type == 'TET4N':
				nodelines = [[0,1], [1,2], [0,2], [0,3], [1,3], [2,3]]
			if elements[j].type == 'TET10N':
				nodelines = [[0,4], [1,4], [1,5], [2,5], [0,6], [2,6], [0,7], [3,7], [1,8], [3,8], [2,9], [3,9]]
			if elements[j].type == 'HEX8N':
				nodelines = [[0,1], [1,2], [2,3], [0,3], [0,4], [1,5], [2,6], [3,7], [4,5], [5,6], [6,7], [4,7]]
			if elements[j].type == 'HEX20N':
				nodelines = [[ 0, 8], [ 8, 1], [ 1, 9], [ 9, 2], [ 2,10], [10, 3], [ 3,11], [11, 0], 
							 [ 0,12], [12, 4], [ 1,13], [13, 5], [ 2,14], [14, 6], [ 3,15], [15, 7],
							 [ 4,16], [16, 5], [ 5,17], [17, 6], [ 6,18], [18, 7], [ 7,19], [19, 4]]

			for k in range(len(nodelines)):
				glBegin(GL_LINES)
				glColor3f(1.0, 0.0, 0.0)
				glVertex3f(nodes[elements[j].nodes[nodelines[k][0]].number].coord[0][0],
						   nodes[elements[j].nodes[nodelines[k][0]].number].coord[1][0],
						   nodes[elements[j].nodes[nodelines[k][0]].number].coord[2][0])
				glVertex3f(nodes[elements[j].nodes[nodelines[k][1]].number].coord[0][0],
						   nodes[elements[j].nodes[nodelines[k][1]].number].coord[1][0],
						   nodes[elements[j].nodes[nodelines[k][1]].number].coord[2][0])
				glEnd()

		glEndList()		


	def buildDisplayList(self,mesh,withResults=[None,None,None]):
		'''
	Draw nodes, edges and faces (tri or quad) for
	all elements in mesh
	'''
		solution = withResults[0]
		result = withResults[1]
		subresult = withResults[2]

		newResult = 'None'
		for newResults in self.results:
			if solution in self.results[newResults].solutions:
				newResult = newResults

		nodes = mesh.nodes
		elements = mesh.elements

		if solution == None:
			mesh.displayLists['nodes'] = glGenLists(1)
			mesh.displayLists['wireframe'] = glGenLists(1)
			mesh.displayLists['shaded'] = glGenLists(1)

			# nodes, original model
			glNewList(mesh.displayLists['nodes'], GL_COMPILE)

			glPointSize(5.0)
			glBegin(GL_POINTS)
			glColor3f(0.05, 0.1, 0.05)
			for i in nodes:
				glVertex3f(nodes[i].coord[0][0], 
						   nodes[i].coord[1][0],
						   nodes[i].coord[2][0])
			glEnd()
			glEndList()

			# wireframe mode, original model, lines only
			glNewList(mesh.displayLists['wireframe'], GL_COMPILE)

			glLineWidth(3.0)
			for j in elements:
				nodelines = []
				if elements[j].type == 'ROD2N2D':
					nodelines = [[0,1]]
				if elements[j].type == 'ROD2N':
					nodelines = [[0,1]]
				if elements[j].type == 'BEAM2N2D':
					nodelines = [[0,1]]
				if elements[j].type == 'BEAM2N':
					nodelines = [[0,1]]
				if elements[j].type == 'TRI3N':
					nodelines = [[0,1], [1,2], [2,0]]
				if elements[j].type == 'TRI6N':
					nodelines = [[0,3], [3,1], [1,4], [4,2], [2,5], [5,0]]
				if elements[j].type == 'QUAD4N':
					nodelines = [[0,1], [1,2], [2,3], [0,3]]
				if elements[j].type == 'QUAD8N':
					nodelines = [[0,1], [1,2], [2,3], [3,4], [4,5], [5,6], [6,7], [7,0]]
				if elements[j].type == 'TET4N':
					nodelines = [[0,1], [1,2], [0,2], [0,3], [1,3], [2,3]]
				if elements[j].type == 'TET10N':
					nodelines = [[0,4], [1,4], [1,5], [2,5], [0,6], [2,6], [0,7], [3,7], [1,8], [3,8], [2,9], [3,9]]
				if elements[j].type == 'HEX8N':
					nodelines = [[0,1], [1,2], [2,3], [0,3], [0,4], [1,5], [2,6], [3,7], [4,5], [5,6], [6,7], [4,7]]
				if elements[j].type == 'HEX20N':
					nodelines = [[ 0, 8], [ 8, 1], [ 1, 9], [ 9, 2], [ 2,10], [10, 3], [ 3,11], [11, 0], 
								 [ 0,12], [12, 4], [ 1,13], [13, 5], [ 2,14], [14, 6], [ 3,15], [15, 7],
								 [ 4,16], [16, 5], [ 5,17], [17, 6], [ 6,18], [18, 7], [ 7,19], [19, 4]]

				for k in range(len(nodelines)):
					glBegin(GL_LINES)
					glColor3f(0.05, 0.1, 0.05)
					glVertex3f(nodes[elements[j].nodes[nodelines[k][0]].number].coord[0][0],
							   nodes[elements[j].nodes[nodelines[k][0]].number].coord[1][0],
							   nodes[elements[j].nodes[nodelines[k][0]].number].coord[2][0])
					glVertex3f(nodes[elements[j].nodes[nodelines[k][1]].number].coord[0][0],
							   nodes[elements[j].nodes[nodelines[k][1]].number].coord[1][0],
							   nodes[elements[j].nodes[nodelines[k][1]].number].coord[2][0])
					glEnd()
			glEndList()


			# shaded mode, original model, element faces
			glNewList(mesh.displayLists['shaded'], GL_COMPILE)

			for j in elements:
				facenodes = []
				if elements[j].type == 'TRI3N':
					facenodes = [[0,1,2]]
				if elements[j].type == 'TRI6N':
					facenodes = [[0,3,5], [3,1,4], [4,2,5], [5,3,4]]
				if elements[j].type == 'QUAD4N':
					facenodes = [[0,1,3], [1,2,3]]
				if elements[j].type == 'QUAD8N':
					facenodes = [[0,1,7], [1,2,3], [3,4,5], [5,6,7], [1,3,7], [5,7,3]]
				if elements[j].type == 'TET4N':
					facenodes = [[0,1,3], [1,2,3], [2,0,3], [0,2,1]]
				if elements[j].type == 'TET10N':
					facenodes = [[0,4,7], [7,4,8], [8,4,1], [7,8,3], [1,5,8], [8,5,9], [9,3,8], [5,2,9],
								 [2,6,9], [9,6,7], [6,0,7], [9,7,3], [5,6,2], [4,0,6], [6,5,4], [4,5,1]]
				if elements[j].type == 'HEX8N':
					facenodes = [[2,1,0], [0,3,2], [3,7,2], [2,7,6], [7,3,0], [0,4,7], [5,6,7], [7,4,5],
								 [1,2,6], [1,6,5], [1,4,0], [5,4,1]]
				if elements[j].type == 'HEX20N':
					facenodes = [[ 0, 8,12], [ 8, 1,13], [13, 5,16], [16, 4,12], [ 8,13,12], [12,13,16],
								 [ 2,10,14], [10, 3,15], [15, 7,18], [18, 6,14], [15,14,10], [18,14,15],
								 [ 1, 9,13], [ 9, 2,14], [14, 6,17], [17, 5,13], [13, 9,14], [13,14,17],
								 [ 3,11,15], [15,19, 7], [19,12, 4], [12,11, 0], [12,15,11], [12,19,15],
								 [ 9, 1, 8], [ 2, 9,10], [ 3,10,11], [ 0,11, 8], [ 9, 8,10], [10, 8,11],
								 [ 5,17,16], [17, 6,18], [18, 7,19], [19, 4,16], [16,17,18], [18,19,16]]

				for k in range(len(facenodes)):
					glBegin(GL_TRIANGLES)
					glColor3f(0.2, 0.4, 0.2)
					glVertex3f(nodes[elements[j].nodes[facenodes[k][0]].number].coord[0][0],
							   nodes[elements[j].nodes[facenodes[k][0]].number].coord[1][0],
							   nodes[elements[j].nodes[facenodes[k][0]].number].coord[2][0])
					glVertex3f(nodes[elements[j].nodes[facenodes[k][1]].number].coord[0][0],
							   nodes[elements[j].nodes[facenodes[k][1]].number].coord[1][0],
							   nodes[elements[j].nodes[facenodes[k][1]].number].coord[2][0])
					glVertex3f(nodes[elements[j].nodes[facenodes[k][2]].number].coord[0][0],
							   nodes[elements[j].nodes[facenodes[k][2]].number].coord[1][0],
							   nodes[elements[j].nodes[facenodes[k][2]].number].coord[2][0])
					glEnd()

				if elements[j].type in ['BEAM2N2D', 'BEAM2N', 'ROD2N2D', 'ROD2N']:
					if elements[j].section != None:
						if 'Cross section' in self.sections[elements[j].section] and hasattr(elements[j],'orientation'):

							faces = []
							lines = []
							x_vec = elements[j].orientation['x-vec']
							y_vec = elements[j].orientation['y-vec']
							z_vec = elements[j].orientation['z-vec']

							if self.sections[elements[j].section]['Cross section']['Type'] == 'Rectangle':

								w  = self.sections[elements[j].section]['Cross section']['width, w']
								h  = self.sections[elements[j].section]['Cross section']['height, h']
								iw = self.sections[elements[j].section]['Cross section']['inner width, iw']
								ih = self.sections[elements[j].section]['Cross section']['inner height, ih']
								w  = w/2.
								h  = h/2.
								iw = iw/2.
								ih = ih/2.
								v_11 = [nodes[elements[j].nodes[0].number].coord[0][0]-y_vec[0]*h-z_vec[0]*w,
										nodes[elements[j].nodes[0].number].coord[1][0]-y_vec[1]*h-z_vec[1]*w,
										nodes[elements[j].nodes[0].number].coord[2][0]-y_vec[2]*h-z_vec[2]*w ]
								v_12 = [nodes[elements[j].nodes[0].number].coord[0][0]-y_vec[0]*h+z_vec[0]*w,
										nodes[elements[j].nodes[0].number].coord[1][0]-y_vec[1]*h+z_vec[1]*w,
										nodes[elements[j].nodes[0].number].coord[2][0]-y_vec[2]*h+z_vec[2]*w ]
								v_13 = [nodes[elements[j].nodes[0].number].coord[0][0]+y_vec[0]*h+z_vec[0]*w,
										nodes[elements[j].nodes[0].number].coord[1][0]+y_vec[1]*h+z_vec[1]*w,
										nodes[elements[j].nodes[0].number].coord[2][0]+y_vec[2]*h+z_vec[2]*w ]
								v_14 = [nodes[elements[j].nodes[0].number].coord[0][0]+y_vec[0]*h-z_vec[0]*w,
										nodes[elements[j].nodes[0].number].coord[1][0]+y_vec[1]*h-z_vec[1]*w,
										nodes[elements[j].nodes[0].number].coord[2][0]+y_vec[2]*h-z_vec[2]*w ]
								v_21 = [nodes[elements[j].nodes[1].number].coord[0][0]-y_vec[0]*h-z_vec[0]*w,
										nodes[elements[j].nodes[1].number].coord[1][0]-y_vec[1]*h-z_vec[1]*w,
										nodes[elements[j].nodes[1].number].coord[2][0]-y_vec[2]*h-z_vec[2]*w ]
								v_22 = [nodes[elements[j].nodes[1].number].coord[0][0]-y_vec[0]*h+z_vec[0]*w,
										nodes[elements[j].nodes[1].number].coord[1][0]-y_vec[1]*h+z_vec[1]*w,
										nodes[elements[j].nodes[1].number].coord[2][0]-y_vec[2]*h+z_vec[2]*w ]
								v_23 = [nodes[elements[j].nodes[1].number].coord[0][0]+y_vec[0]*h+z_vec[0]*w,
										nodes[elements[j].nodes[1].number].coord[1][0]+y_vec[1]*h+z_vec[1]*w,
										nodes[elements[j].nodes[1].number].coord[2][0]+y_vec[2]*h+z_vec[2]*w ]
								v_24 = [nodes[elements[j].nodes[1].number].coord[0][0]+y_vec[0]*h-z_vec[0]*w,
										nodes[elements[j].nodes[1].number].coord[1][0]+y_vec[1]*h-z_vec[1]*w,
										nodes[elements[j].nodes[1].number].coord[2][0]+y_vec[2]*h-z_vec[2]*w ]
								if iw != 0. or ih != 0.:
									v_15 = [nodes[elements[j].nodes[0].number].coord[0][0]-y_vec[0]*ih-z_vec[0]*iw,
											nodes[elements[j].nodes[0].number].coord[1][0]-y_vec[1]*ih-z_vec[1]*iw,
											nodes[elements[j].nodes[0].number].coord[2][0]-y_vec[2]*ih-z_vec[2]*iw ]
									v_16 = [nodes[elements[j].nodes[0].number].coord[0][0]-y_vec[0]*ih+z_vec[0]*iw,
											nodes[elements[j].nodes[0].number].coord[1][0]-y_vec[1]*ih+z_vec[1]*iw,
											nodes[elements[j].nodes[0].number].coord[2][0]-y_vec[2]*ih+z_vec[2]*iw ]
									v_17 = [nodes[elements[j].nodes[0].number].coord[0][0]+y_vec[0]*ih+z_vec[0]*iw,
											nodes[elements[j].nodes[0].number].coord[1][0]+y_vec[1]*ih+z_vec[1]*iw,
											nodes[elements[j].nodes[0].number].coord[2][0]+y_vec[2]*ih+z_vec[2]*iw ]
									v_18 = [nodes[elements[j].nodes[0].number].coord[0][0]+y_vec[0]*ih-z_vec[0]*iw,
											nodes[elements[j].nodes[0].number].coord[1][0]+y_vec[1]*ih-z_vec[1]*iw,
											nodes[elements[j].nodes[0].number].coord[2][0]+y_vec[2]*ih-z_vec[2]*iw ]
									v_25 = [nodes[elements[j].nodes[1].number].coord[0][0]-y_vec[0]*ih-z_vec[0]*iw,
											nodes[elements[j].nodes[1].number].coord[1][0]-y_vec[1]*ih-z_vec[1]*iw,
											nodes[elements[j].nodes[1].number].coord[2][0]-y_vec[2]*ih-z_vec[2]*iw ]
									v_26 = [nodes[elements[j].nodes[1].number].coord[0][0]-y_vec[0]*ih+z_vec[0]*iw,
											nodes[elements[j].nodes[1].number].coord[1][0]-y_vec[1]*ih+z_vec[1]*iw,
											nodes[elements[j].nodes[1].number].coord[2][0]-y_vec[2]*ih+z_vec[2]*iw ]
									v_27 = [nodes[elements[j].nodes[1].number].coord[0][0]+y_vec[0]*ih+z_vec[0]*iw,
											nodes[elements[j].nodes[1].number].coord[1][0]+y_vec[1]*ih+z_vec[1]*iw,
											nodes[elements[j].nodes[1].number].coord[2][0]+y_vec[2]*ih+z_vec[2]*iw ]
									v_28 = [nodes[elements[j].nodes[1].number].coord[0][0]+y_vec[0]*ih-z_vec[0]*iw,
											nodes[elements[j].nodes[1].number].coord[1][0]+y_vec[1]*ih-z_vec[1]*iw,
											nodes[elements[j].nodes[1].number].coord[2][0]+y_vec[2]*ih-z_vec[2]*iw ]

								lines = [[v_11,v_12],[v_12,v_13],[v_13,v_14],[v_14,v_11],
										 [v_21,v_22],[v_22,v_23],[v_23,v_24],[v_24,v_21],
										 [v_11,v_21],[v_12,v_22],[v_13,v_23],[v_14,v_24]]
								faces = [[v_13,v_12,v_22],[v_22,v_23,v_13],
										 [v_14,v_13,v_23],[v_23,v_24,v_14],
										 [v_11,v_14,v_24],[v_24,v_21,v_11],
										 [v_12,v_11,v_21],[v_21,v_22,v_12]]

								if iw == 0. or ih == 0.:
									faces += [[v_11,v_12,v_13],[v_13,v_14,v_11],
											  [v_21,v_24,v_23],[v_23,v_22,v_21]]
								else:
									lines += [[v_15,v_16],[v_16,v_17],[v_17,v_18],[v_18,v_15],
											  [v_25,v_26],[v_26,v_27],[v_27,v_28],[v_28,v_25],
											  [v_15,v_25],[v_16,v_26],[v_17,v_27],[v_18,v_28]]
									faces += [[v_15,v_11,v_12],[v_12,v_16,v_15],
											  [v_16,v_12,v_13],[v_13,v_17,v_16],
											  [v_17,v_13,v_14],[v_14,v_18,v_17],
											  [v_18,v_14,v_11],[v_11,v_15,v_18],
											  [v_26,v_22,v_21],[v_21,v_25,v_26],
											  [v_22,v_26,v_23],[v_26,v_27,v_23],
											  [v_23,v_27,v_24],[v_27,v_28,v_24],
											  [v_24,v_28,v_21],[v_25,v_21,v_28],
											  [v_17,v_27,v_16],[v_27,v_26,v_16],
											  [v_18,v_28,v_17],[v_28,v_27,v_17],
											  [v_15,v_25,v_18],[v_25,v_28,v_18],
											  [v_25,v_15,v_26],[v_15,v_16,v_26]]

							elif self.sections[elements[j].section]['Cross section']['Type'] == 'Circle':

								r  = self.sections[elements[j].section]['Cross section']['radius, r']
								ir  = self.sections[elements[j].section]['Cross section']['inner radius, ir']
								vertices1 = []
								vertices2 = []
								pnts = 24
								for v in range(pnts):
									d = pnts/(v+1)
									vc = np.cos(2*np.pi/d)
									vs = np.sin(2*np.pi/d)
									vertices1.append([nodes[elements[j].nodes[0].number].coord[0][0]+vs*y_vec[0]*r+vc*z_vec[0]*r,
													  nodes[elements[j].nodes[0].number].coord[1][0]+vs*y_vec[1]*r+vc*z_vec[1]*r,
													  nodes[elements[j].nodes[0].number].coord[2][0]+vs*y_vec[2]*r+vc*z_vec[2]*r ])
									vertices2.append([nodes[elements[j].nodes[1].number].coord[0][0]+vs*y_vec[0]*r+vc*z_vec[0]*r,
													  nodes[elements[j].nodes[1].number].coord[1][0]+vs*y_vec[1]*r+vc*z_vec[1]*r,
													  nodes[elements[j].nodes[1].number].coord[2][0]+vs*y_vec[2]*r+vc*z_vec[2]*r ])
								if ir != 0.:
									ivertices1 = []
									ivertices2 = []
									for v in range(pnts):
										d = pnts/(v+1)
										vc = np.cos(2*np.pi/d)
										vs = np.sin(2*np.pi/d)
										ivertices1.append([nodes[elements[j].nodes[0].number].coord[0][0]+vs*y_vec[0]*ir+vc*z_vec[0]*ir,
														   nodes[elements[j].nodes[0].number].coord[1][0]+vs*y_vec[1]*ir+vc*z_vec[1]*ir,
														   nodes[elements[j].nodes[0].number].coord[2][0]+vs*y_vec[2]*ir+vc*z_vec[2]*ir ])
										ivertices2.append([nodes[elements[j].nodes[1].number].coord[0][0]+vs*y_vec[0]*ir+vc*z_vec[0]*ir,
														   nodes[elements[j].nodes[1].number].coord[1][0]+vs*y_vec[1]*ir+vc*z_vec[1]*ir,
														   nodes[elements[j].nodes[1].number].coord[2][0]+vs*y_vec[2]*ir+vc*z_vec[2]*ir ])

								lines = []
								faces = []
								for v in range(pnts):
									lines.append([vertices1[v-1],vertices1[v]])
									lines.append([vertices2[v-1],vertices2[v]])
								lines.append([vertices1[0],vertices2[0]])

								if ir != 0.:
									for v in range(pnts):
										lines.append([ivertices1[v-1],ivertices1[v]])
										lines.append([ivertices2[v-1],ivertices2[v]])
									lines.append([ivertices1[0],ivertices2[0]])
									for v in range(pnts-1):
										faces.append([ivertices1[v],vertices1[v],vertices1[v+1]])
										faces.append([vertices1[v+1],ivertices1[v+1],ivertices1[v]])
										faces.append([ivertices2[v],vertices2[v+1],vertices2[v]])
										faces.append([vertices2[v+1],ivertices2[v],ivertices2[v+1]])
										faces.append([vertices1[v],vertices2[v],vertices2[v+1]])
										faces.append([vertices2[v+1],vertices1[v+1],vertices1[v]])
										faces.append([ivertices1[v],ivertices1[v+1],ivertices2[v]])
										faces.append([ivertices1[v+1],ivertices2[v+1],ivertices2[v]])
									faces.append([ivertices1[-1],vertices1[-1],vertices1[0]])
									faces.append([vertices1[0],ivertices1[0],ivertices1[-1]])
									faces.append([ivertices2[-1],vertices2[0],vertices2[-1]])
									faces.append([vertices2[0],ivertices2[-1],ivertices2[0]])
									faces.append([vertices1[-1],vertices2[-1],vertices2[0]])
									faces.append([vertices2[0],vertices1[0],vertices1[-1]])
									faces.append([ivertices1[-1],ivertices1[0],ivertices2[-1]])
									faces.append([ivertices1[0],ivertices2[0],ivertices2[-1]])
									
								else:
									vertices1.append([nodes[elements[j].nodes[0].number].coord[0][0],
													  nodes[elements[j].nodes[0].number].coord[1][0],
													  nodes[elements[j].nodes[0].number].coord[2][0] ])
									vertices2.append([nodes[elements[j].nodes[1].number].coord[0][0],
													  nodes[elements[j].nodes[1].number].coord[1][0],
													  nodes[elements[j].nodes[1].number].coord[2][0] ])
									for v in range(pnts):
										faces.append([vertices1[-1],vertices1[v],vertices1[v+1]])
										faces.append([vertices2[-1],vertices2[v+1],vertices2[v]])
										faces.append([vertices1[v],vertices2[v],vertices2[v+1]])
										faces.append([vertices2[v+1],vertices1[v+1],vertices1[v]])
									faces.append([vertices1[-1],vertices1[-2],vertices1[0]])
									faces.append([vertices2[-1],vertices2[0],vertices2[-2]])
									faces.append([vertices1[-2],vertices2[-2],vertices2[0]])
									faces.append([vertices2[0],vertices1[0],vertices1[-2]])

							elif self.sections[elements[j].section]['Cross section']['Type'] == 'L-Beam':

								bw  = self.sections[elements[j].section]['Cross section']['bottom width, bw']
								bt = self.sections[elements[j].section]['Cross section']['bottom thickness, bt']
								st = self.sections[elements[j].section]['Cross section']['side thickness, st']
								h  = self.sections[elements[j].section]['Cross section']['height, h']
								A1  = st*(h-bt)
								A2  = bt*bw
								A   = A1+A2
								yC1 = (h/2.)+bt
								yC2 = bt/2.
								zC1 = st/2.
								zC2 = bw/2.
								if A != 0.:
									yC = (A1*yC1+A2*yC2)/A
									zC = (A1*zC1+A2*zC2)/A
								else:
									yC = 0.
									zC = 0.
								v_11  = [nodes[elements[j].nodes[0].number].coord[0][0]-y_vec[0]*yC-z_vec[0]*zC,
										 nodes[elements[j].nodes[0].number].coord[1][0]-y_vec[1]*yC-z_vec[1]*zC,
										 nodes[elements[j].nodes[0].number].coord[2][0]-y_vec[2]*yC-z_vec[2]*zC ]
								v_12  = [nodes[elements[j].nodes[0].number].coord[0][0]-y_vec[0]*yC+z_vec[0]*(bw-zC),
										 nodes[elements[j].nodes[0].number].coord[1][0]-y_vec[1]*yC+z_vec[1]*(bw-zC),
										 nodes[elements[j].nodes[0].number].coord[2][0]-y_vec[2]*yC+z_vec[2]*(bw-zC) ]
								v_13  = [nodes[elements[j].nodes[0].number].coord[0][0]-y_vec[0]*(yC-bt)+z_vec[0]*(bw-zC),
										 nodes[elements[j].nodes[0].number].coord[1][0]-y_vec[1]*(yC-bt)+z_vec[1]*(bw-zC),
										 nodes[elements[j].nodes[0].number].coord[2][0]-y_vec[2]*(yC-bt)+z_vec[2]*(bw-zC) ]
								v_14  = [nodes[elements[j].nodes[0].number].coord[0][0]-y_vec[0]*(yC-bt)-z_vec[0]*(zC-st),
										 nodes[elements[j].nodes[0].number].coord[1][0]-y_vec[1]*(yC-bt)-z_vec[1]*(zC-st),
										 nodes[elements[j].nodes[0].number].coord[2][0]-y_vec[2]*(yC-bt)-z_vec[2]*(zC-st) ]
								v_15  = [nodes[elements[j].nodes[0].number].coord[0][0]+y_vec[0]*(h-yC)-z_vec[0]*(zC-st),
										 nodes[elements[j].nodes[0].number].coord[1][0]+y_vec[1]*(h-yC)-z_vec[1]*(zC-st),
										 nodes[elements[j].nodes[0].number].coord[2][0]+y_vec[2]*(h-yC)-z_vec[2]*(zC-st) ]
								v_16  = [nodes[elements[j].nodes[0].number].coord[0][0]+y_vec[0]*(h-yC)-z_vec[0]*zC,
										 nodes[elements[j].nodes[0].number].coord[1][0]+y_vec[1]*(h-yC)-z_vec[1]*zC,
										 nodes[elements[j].nodes[0].number].coord[2][0]+y_vec[2]*(h-yC)-z_vec[2]*zC ]
								v_21  = [nodes[elements[j].nodes[1].number].coord[0][0]-y_vec[0]*yC-z_vec[0]*zC,
										 nodes[elements[j].nodes[1].number].coord[1][0]-y_vec[1]*yC-z_vec[1]*zC,
										 nodes[elements[j].nodes[1].number].coord[2][0]-y_vec[2]*yC-z_vec[2]*zC ]
								v_22  = [nodes[elements[j].nodes[1].number].coord[0][0]-y_vec[0]*yC+z_vec[0]*(bw-zC),
										 nodes[elements[j].nodes[1].number].coord[1][0]-y_vec[1]*yC+z_vec[1]*(bw-zC),
										 nodes[elements[j].nodes[1].number].coord[2][0]-y_vec[2]*yC+z_vec[2]*(bw-zC) ]
								v_23  = [nodes[elements[j].nodes[1].number].coord[0][0]-y_vec[0]*(yC-bt)+z_vec[0]*(bw-zC),
										 nodes[elements[j].nodes[1].number].coord[1][0]-y_vec[1]*(yC-bt)+z_vec[1]*(bw-zC),
										 nodes[elements[j].nodes[1].number].coord[2][0]-y_vec[2]*(yC-bt)+z_vec[2]*(bw-zC) ]
								v_24  = [nodes[elements[j].nodes[1].number].coord[0][0]-y_vec[0]*(yC-bt)-z_vec[0]*(zC-st),
										 nodes[elements[j].nodes[1].number].coord[1][0]-y_vec[1]*(yC-bt)-z_vec[1]*(zC-st),
										 nodes[elements[j].nodes[1].number].coord[2][0]-y_vec[2]*(yC-bt)-z_vec[2]*(zC-st) ]
								v_25  = [nodes[elements[j].nodes[1].number].coord[0][0]+y_vec[0]*(h-yC)-z_vec[0]*(zC-st),
										 nodes[elements[j].nodes[1].number].coord[1][0]+y_vec[1]*(h-yC)-z_vec[1]*(zC-st),
										 nodes[elements[j].nodes[1].number].coord[2][0]+y_vec[2]*(h-yC)-z_vec[2]*(zC-st) ]
								v_26  = [nodes[elements[j].nodes[1].number].coord[0][0]+y_vec[0]*(h-yC)-z_vec[0]*zC,
										 nodes[elements[j].nodes[1].number].coord[1][0]+y_vec[1]*(h-yC)-z_vec[1]*zC,
										 nodes[elements[j].nodes[1].number].coord[2][0]+y_vec[2]*(h-yC)-z_vec[2]*zC ]

								lines = [[v_11,v_12],[v_12,v_13],[v_13,v_14],[v_14,v_15],[v_15,v_16],[v_16,v_11],
										 [v_21,v_22],[v_22,v_23],[v_23,v_24],[v_24,v_25],[v_25,v_26],[v_26,v_21],
										 [v_11,v_21],[v_12,v_22],[v_13,v_23],[v_14,v_24],[v_15,v_25],[v_16,v_26]]
								faces = [[v_11,v_12,v_13],[v_13,v_14,v_11],
										 [v_11,v_14,v_16],[v_16,v_14,v_15],
										 [v_23,v_22,v_21],[v_21,v_24,v_23],
										 [v_24,v_21,v_26],[v_24,v_26,v_25],
										 [v_11,v_21,v_12],[v_12,v_21,v_22],
										 [v_11,v_16,v_26],[v_26,v_21,v_11],
										 [v_16,v_15,v_26],[v_26,v_15,v_25],
										 [v_13,v_12,v_22],[v_22,v_23,v_13],
										 [v_14,v_13,v_24],[v_24,v_13,v_23],
										 [v_14,v_24,v_25],[v_25,v_15,v_14]]

							elif self.sections[elements[j].section]['Cross section']['Type'] == 'I-Beam':
								tw = self.sections[elements[j].section]['Cross section']['top width, tw']
								tt = self.sections[elements[j].section]['Cross section']['top thickness, tt']
								mt = self.sections[elements[j].section]['Cross section']['middle thickness, mt']
								bw = self.sections[elements[j].section]['Cross section']['bottom width, bw']
								bt = self.sections[elements[j].section]['Cross section']['bottom thickness, bt']
								h  = self.sections[elements[j].section]['Cross section']['height, h']
								tw = tw/2.
								tt = tt
								mt = mt/2.
								bw = bw/2.
								bt = bt
								h  = h/2.
								v_11  = [nodes[elements[j].nodes[0].number].coord[0][0]-y_vec[0]*h-z_vec[0]*bw,
										 nodes[elements[j].nodes[0].number].coord[1][0]-y_vec[1]*h-z_vec[1]*bw,
										 nodes[elements[j].nodes[0].number].coord[2][0]-y_vec[2]*h-z_vec[2]*bw ]
								v_12  = [nodes[elements[j].nodes[0].number].coord[0][0]-y_vec[0]*h+z_vec[0]*bw,
										 nodes[elements[j].nodes[0].number].coord[1][0]-y_vec[1]*h+z_vec[1]*bw,
										 nodes[elements[j].nodes[0].number].coord[2][0]-y_vec[2]*h+z_vec[2]*bw ]
								v_13  = [nodes[elements[j].nodes[0].number].coord[0][0]-y_vec[0]*(h-bt)+z_vec[0]*bw,
										 nodes[elements[j].nodes[0].number].coord[1][0]-y_vec[1]*(h-bt)+z_vec[1]*bw,
										 nodes[elements[j].nodes[0].number].coord[2][0]-y_vec[2]*(h-bt)+z_vec[2]*bw ]
								v_14  = [nodes[elements[j].nodes[0].number].coord[0][0]-y_vec[0]*(h-bt)+z_vec[0]*mt,
										 nodes[elements[j].nodes[0].number].coord[1][0]-y_vec[1]*(h-bt)+z_vec[1]*mt,
										 nodes[elements[j].nodes[0].number].coord[2][0]-y_vec[2]*(h-bt)+z_vec[2]*mt ]
								v_15  = [nodes[elements[j].nodes[0].number].coord[0][0]-y_vec[0]*(h-bt)-z_vec[0]*mt,
										 nodes[elements[j].nodes[0].number].coord[1][0]-y_vec[1]*(h-bt)-z_vec[1]*mt,
										 nodes[elements[j].nodes[0].number].coord[2][0]-y_vec[2]*(h-bt)-z_vec[2]*mt ]
								v_16  = [nodes[elements[j].nodes[0].number].coord[0][0]-y_vec[0]*(h-bt)-z_vec[0]*bw,
										 nodes[elements[j].nodes[0].number].coord[1][0]-y_vec[1]*(h-bt)-z_vec[1]*bw,
										 nodes[elements[j].nodes[0].number].coord[2][0]-y_vec[2]*(h-bt)-z_vec[2]*bw ]
								v_17  = [nodes[elements[j].nodes[0].number].coord[0][0]+y_vec[0]*(h-tt)-z_vec[0]*tw,
										 nodes[elements[j].nodes[0].number].coord[1][0]+y_vec[1]*(h-tt)-z_vec[1]*tw,
										 nodes[elements[j].nodes[0].number].coord[2][0]+y_vec[2]*(h-tt)-z_vec[2]*tw ]
								v_18  = [nodes[elements[j].nodes[0].number].coord[0][0]+y_vec[0]*(h-tt)-z_vec[0]*mt,
										 nodes[elements[j].nodes[0].number].coord[1][0]+y_vec[1]*(h-tt)-z_vec[1]*mt,
										 nodes[elements[j].nodes[0].number].coord[2][0]+y_vec[2]*(h-tt)-z_vec[2]*mt ]
								v_19  = [nodes[elements[j].nodes[0].number].coord[0][0]+y_vec[0]*(h-tt)+z_vec[0]*mt,
										 nodes[elements[j].nodes[0].number].coord[1][0]+y_vec[1]*(h-tt)+z_vec[1]*mt,
										 nodes[elements[j].nodes[0].number].coord[2][0]+y_vec[2]*(h-tt)+z_vec[2]*mt ]
								v_110 = [nodes[elements[j].nodes[0].number].coord[0][0]+y_vec[0]*(h-tt)+z_vec[0]*tw,
										 nodes[elements[j].nodes[0].number].coord[1][0]+y_vec[1]*(h-tt)+z_vec[1]*tw,
										 nodes[elements[j].nodes[0].number].coord[2][0]+y_vec[2]*(h-tt)+z_vec[2]*tw ]
								v_111 = [nodes[elements[j].nodes[0].number].coord[0][0]+y_vec[0]*h+z_vec[0]*tw,
										 nodes[elements[j].nodes[0].number].coord[1][0]+y_vec[1]*h+z_vec[1]*tw,
										 nodes[elements[j].nodes[0].number].coord[2][0]+y_vec[2]*h+z_vec[2]*tw ]
								v_112 = [nodes[elements[j].nodes[0].number].coord[0][0]+y_vec[0]*h-z_vec[0]*tw,
										 nodes[elements[j].nodes[0].number].coord[1][0]+y_vec[1]*h-z_vec[1]*tw,
										 nodes[elements[j].nodes[0].number].coord[2][0]+y_vec[2]*h-z_vec[2]*tw ]
								v_21  = [nodes[elements[j].nodes[1].number].coord[0][0]-y_vec[0]*h-z_vec[0]*bw,
										 nodes[elements[j].nodes[1].number].coord[1][0]-y_vec[1]*h-z_vec[1]*bw,
										 nodes[elements[j].nodes[1].number].coord[2][0]-y_vec[2]*h-z_vec[2]*bw ]
								v_22  = [nodes[elements[j].nodes[1].number].coord[0][0]-y_vec[0]*h+z_vec[0]*bw,
										 nodes[elements[j].nodes[1].number].coord[1][0]-y_vec[1]*h+z_vec[1]*bw,
										 nodes[elements[j].nodes[1].number].coord[2][0]-y_vec[2]*h+z_vec[2]*bw ]
								v_23  = [nodes[elements[j].nodes[1].number].coord[0][0]-y_vec[0]*(h-bt)+z_vec[0]*bw,
										 nodes[elements[j].nodes[1].number].coord[1][0]-y_vec[1]*(h-bt)+z_vec[1]*bw,
										 nodes[elements[j].nodes[1].number].coord[2][0]-y_vec[2]*(h-bt)+z_vec[2]*bw ]
								v_24  = [nodes[elements[j].nodes[1].number].coord[0][0]-y_vec[0]*(h-bt)+z_vec[0]*mt,
										 nodes[elements[j].nodes[1].number].coord[1][0]-y_vec[1]*(h-bt)+z_vec[1]*mt,
										 nodes[elements[j].nodes[1].number].coord[2][0]-y_vec[2]*(h-bt)+z_vec[2]*mt ]
								v_25  = [nodes[elements[j].nodes[1].number].coord[0][0]-y_vec[0]*(h-bt)-z_vec[0]*mt,
										 nodes[elements[j].nodes[1].number].coord[1][0]-y_vec[1]*(h-bt)-z_vec[1]*mt,
										 nodes[elements[j].nodes[1].number].coord[2][0]-y_vec[2]*(h-bt)-z_vec[2]*mt ]
								v_26  = [nodes[elements[j].nodes[1].number].coord[0][0]-y_vec[0]*(h-bt)-z_vec[0]*bw,
										 nodes[elements[j].nodes[1].number].coord[1][0]-y_vec[1]*(h-bt)-z_vec[1]*bw,
										 nodes[elements[j].nodes[1].number].coord[2][0]-y_vec[2]*(h-bt)-z_vec[2]*bw ]
								v_27  = [nodes[elements[j].nodes[1].number].coord[0][0]+y_vec[0]*(h-tt)-z_vec[0]*tw,
										 nodes[elements[j].nodes[1].number].coord[1][0]+y_vec[1]*(h-tt)-z_vec[1]*tw,
										 nodes[elements[j].nodes[1].number].coord[2][0]+y_vec[2]*(h-tt)-z_vec[2]*tw ]
								v_28  = [nodes[elements[j].nodes[1].number].coord[0][0]+y_vec[0]*(h-tt)-z_vec[0]*mt,
										 nodes[elements[j].nodes[1].number].coord[1][0]+y_vec[1]*(h-tt)-z_vec[1]*mt,
										 nodes[elements[j].nodes[1].number].coord[2][0]+y_vec[2]*(h-tt)-z_vec[2]*mt ]
								v_29  = [nodes[elements[j].nodes[1].number].coord[0][0]+y_vec[0]*(h-tt)+z_vec[0]*mt,
										 nodes[elements[j].nodes[1].number].coord[1][0]+y_vec[1]*(h-tt)+z_vec[1]*mt,
										 nodes[elements[j].nodes[1].number].coord[2][0]+y_vec[2]*(h-tt)+z_vec[2]*mt ]
								v_210 = [nodes[elements[j].nodes[1].number].coord[0][0]+y_vec[0]*(h-tt)+z_vec[0]*tw,
										 nodes[elements[j].nodes[1].number].coord[1][0]+y_vec[1]*(h-tt)+z_vec[1]*tw,
										 nodes[elements[j].nodes[1].number].coord[2][0]+y_vec[2]*(h-tt)+z_vec[2]*tw ]
								v_211 = [nodes[elements[j].nodes[1].number].coord[0][0]+y_vec[0]*h+z_vec[0]*tw,
										 nodes[elements[j].nodes[1].number].coord[1][0]+y_vec[1]*h+z_vec[1]*tw,
										 nodes[elements[j].nodes[1].number].coord[2][0]+y_vec[2]*h+z_vec[2]*tw ]
								v_212 = [nodes[elements[j].nodes[1].number].coord[0][0]+y_vec[0]*h-z_vec[0]*tw,
										 nodes[elements[j].nodes[1].number].coord[1][0]+y_vec[1]*h-z_vec[1]*tw,
										 nodes[elements[j].nodes[1].number].coord[2][0]+y_vec[2]*h-z_vec[2]*tw ]

								lines = [[v_11,v_12],[v_12,v_13],[v_13,v_14],[v_14,v_19],
										 [v_19,v_110],[v_110,v_111],[v_111,v_112],[v_112,v_17],
										 [v_17,v_18],[v_18,v_15],[v_15,v_16],[v_16,v_11],
										 [v_21,v_22],[v_22,v_23],[v_23,v_24],[v_24,v_29],
										 [v_29,v_210],[v_210,v_211],[v_211,v_212],[v_212,v_27],
										 [v_27,v_28],[v_28,v_25],[v_25,v_26],[v_26,v_21],
										 [v_11,v_21],[v_12,v_22],[v_13,v_23],[v_14,v_24],
										 [v_15,v_25],[v_16,v_26],[v_17,v_27],[v_18,v_28],
										 [v_19,v_29],[v_110,v_210],[v_111,v_211],[v_112,v_212]]
								faces = [[v_11,v_12,v_13],[v_13,v_16,v_11],
										 [v_15,v_14,v_19],[v_19,v_18,v_15],
										 [v_112,v_17,v_110],[v_110,v_111,v_112],
										 [v_23,v_22,v_21],[v_21,v_26,v_23],
										 [v_29,v_24,v_25],[v_25,v_28,v_29],
										 [v_210,v_27,v_212],[v_212,v_211,v_210],
										 [v_19,v_14,v_24],[v_24,v_29,v_19],
										 [v_15,v_18,v_28],[v_28,v_25,v_15],
										 [v_13,v_12,v_22],[v_22,v_23,v_13],
										 [v_11,v_16,v_26],[v_26,v_21,v_11],
										 [v_111,v_110,v_210],[v_210,v_211,v_111],
										 [v_17,v_112,v_212],[v_212,v_27,v_17],
										 [v_11,v_21,v_12],[v_21,v_22,v_12],
										 [v_112,v_111,v_212],[v_212,v_111,v_211],
										 [v_14,v_13,v_24],[v_24,v_13,v_23],
										 [v_16,v_15,v_26],[v_26,v_15,v_25],
										 [v_18,v_17,v_27],[v_27,v_28,v_18],
										 [v_110,v_19,v_29],[v_29,v_210,v_110]]

							elif self.sections[elements[j].section]['Cross section']['Type'] == 'C-Beam':
								tw = self.sections[elements[j].section]['Cross section']['top width, tw']
								tt = self.sections[elements[j].section]['Cross section']['top thickness, tt']
								mt = self.sections[elements[j].section]['Cross section']['middle thickness, mt']
								bw = self.sections[elements[j].section]['Cross section']['bottom width, bw']
								bt = self.sections[elements[j].section]['Cross section']['bottom thickness, bt']
								h  = self.sections[elements[j].section]['Cross section']['height, h']
								A1  = tt*tw
								A2  = mt*(h-tt-bt)
								A3  = bt*bw
								A   = A1+A2+A3
								zC1 = tw/2.
								zC2 = mt/2.
								zC3 = bw/2.
								yC1 = h-(tt/2.)
								yC2 = (h-tt)/2.
								yC3 = bt/2.
								if A != 0.:
									zC = (A1*zC1+A2*zC2+A3*zC3)/A
									yC = (A1*yC1+A2*yC2+A3*yC3)/A
								else:
									zC = 0.
									yC = 0.
								v_11  = [nodes[elements[j].nodes[0].number].coord[0][0]-y_vec[0]*yC-z_vec[0]*zC,
										 nodes[elements[j].nodes[0].number].coord[1][0]-y_vec[1]*yC-z_vec[1]*zC,
										 nodes[elements[j].nodes[0].number].coord[2][0]-y_vec[2]*yC-z_vec[2]*zC ]
								v_12  = [nodes[elements[j].nodes[0].number].coord[0][0]-y_vec[0]*yC+z_vec[0]*(bw-zC),
										 nodes[elements[j].nodes[0].number].coord[1][0]-y_vec[1]*yC+z_vec[1]*(bw-zC),
										 nodes[elements[j].nodes[0].number].coord[2][0]-y_vec[2]*yC+z_vec[2]*(bw-zC) ]
								v_13  = [nodes[elements[j].nodes[0].number].coord[0][0]-y_vec[0]*(yC-bt)+z_vec[0]*(bw-zC),
										 nodes[elements[j].nodes[0].number].coord[1][0]-y_vec[1]*(yC-bt)+z_vec[1]*(bw-zC),
										 nodes[elements[j].nodes[0].number].coord[2][0]-y_vec[2]*(yC-bt)+z_vec[2]*(bw-zC) ]
								v_14  = [nodes[elements[j].nodes[0].number].coord[0][0]-y_vec[0]*(yC-bt)-z_vec[0]*(zC-mt),
										 nodes[elements[j].nodes[0].number].coord[1][0]-y_vec[1]*(yC-bt)-z_vec[1]*(zC-mt),
										 nodes[elements[j].nodes[0].number].coord[2][0]-y_vec[2]*(yC-bt)-z_vec[2]*(zC-mt) ]
								v_15  = [nodes[elements[j].nodes[0].number].coord[0][0]+y_vec[0]*(h-yC-tt)-z_vec[0]*(zC-mt),
										 nodes[elements[j].nodes[0].number].coord[1][0]+y_vec[1]*(h-yC-tt)-z_vec[1]*(zC-mt),
										 nodes[elements[j].nodes[0].number].coord[2][0]+y_vec[2]*(h-yC-tt)-z_vec[2]*(zC-mt) ]
								v_16  = [nodes[elements[j].nodes[0].number].coord[0][0]+y_vec[0]*(h-yC-tt)+z_vec[0]*(tw-zC),
										 nodes[elements[j].nodes[0].number].coord[1][0]+y_vec[1]*(h-yC-tt)+z_vec[1]*(tw-zC),
										 nodes[elements[j].nodes[0].number].coord[2][0]+y_vec[2]*(h-yC-tt)+z_vec[2]*(tw-zC) ]
								v_17  = [nodes[elements[j].nodes[0].number].coord[0][0]+y_vec[0]*(h-yC)+z_vec[0]*(tw-zC),
										 nodes[elements[j].nodes[0].number].coord[1][0]+y_vec[1]*(h-yC)+z_vec[1]*(tw-zC),
										 nodes[elements[j].nodes[0].number].coord[2][0]+y_vec[2]*(h-yC)+z_vec[2]*(tw-zC) ]
								v_18  = [nodes[elements[j].nodes[0].number].coord[0][0]+y_vec[0]*(h-yC)-z_vec[0]*zC,
										 nodes[elements[j].nodes[0].number].coord[1][0]+y_vec[1]*(h-yC)-z_vec[1]*zC,
										 nodes[elements[j].nodes[0].number].coord[2][0]+y_vec[2]*(h-yC)-z_vec[2]*zC ]
								v_21  = [nodes[elements[j].nodes[1].number].coord[0][0]-y_vec[0]*yC-z_vec[0]*zC,
										 nodes[elements[j].nodes[1].number].coord[1][0]-y_vec[1]*yC-z_vec[1]*zC,
										 nodes[elements[j].nodes[1].number].coord[2][0]-y_vec[2]*yC-z_vec[2]*zC ]
								v_22  = [nodes[elements[j].nodes[1].number].coord[0][0]-y_vec[0]*yC+z_vec[0]*(bw-zC),
										 nodes[elements[j].nodes[1].number].coord[1][0]-y_vec[1]*yC+z_vec[1]*(bw-zC),
										 nodes[elements[j].nodes[1].number].coord[2][0]-y_vec[2]*yC+z_vec[2]*(bw-zC) ]
								v_23  = [nodes[elements[j].nodes[1].number].coord[0][0]-y_vec[0]*(yC-bt)+z_vec[0]*(bw-zC),
										 nodes[elements[j].nodes[1].number].coord[1][0]-y_vec[1]*(yC-bt)+z_vec[1]*(bw-zC),
										 nodes[elements[j].nodes[1].number].coord[2][0]-y_vec[2]*(yC-bt)+z_vec[2]*(bw-zC) ]
								v_24  = [nodes[elements[j].nodes[1].number].coord[0][0]-y_vec[0]*(yC-bt)-z_vec[0]*(zC-mt),
										 nodes[elements[j].nodes[1].number].coord[1][0]-y_vec[1]*(yC-bt)-z_vec[1]*(zC-mt),
										 nodes[elements[j].nodes[1].number].coord[2][0]-y_vec[2]*(yC-bt)-z_vec[2]*(zC-mt) ]
								v_25  = [nodes[elements[j].nodes[1].number].coord[0][0]+y_vec[0]*(h-yC-tt)-z_vec[0]*(zC-mt),
										 nodes[elements[j].nodes[1].number].coord[1][0]+y_vec[1]*(h-yC-tt)-z_vec[1]*(zC-mt),
										 nodes[elements[j].nodes[1].number].coord[2][0]+y_vec[2]*(h-yC-tt)-z_vec[2]*(zC-mt) ]
								v_26  = [nodes[elements[j].nodes[1].number].coord[0][0]+y_vec[0]*(h-yC-tt)+z_vec[0]*(tw-zC),
										 nodes[elements[j].nodes[1].number].coord[1][0]+y_vec[1]*(h-yC-tt)+z_vec[1]*(tw-zC),
										 nodes[elements[j].nodes[1].number].coord[2][0]+y_vec[2]*(h-yC-tt)+z_vec[2]*(tw-zC) ]
								v_27  = [nodes[elements[j].nodes[1].number].coord[0][0]+y_vec[0]*(h-yC)+z_vec[0]*(tw-zC),
										 nodes[elements[j].nodes[1].number].coord[1][0]+y_vec[1]*(h-yC)+z_vec[1]*(tw-zC),
										 nodes[elements[j].nodes[1].number].coord[2][0]+y_vec[2]*(h-yC)+z_vec[2]*(tw-zC) ]
								v_28  = [nodes[elements[j].nodes[1].number].coord[0][0]+y_vec[0]*(h-yC)-z_vec[0]*zC,
										 nodes[elements[j].nodes[1].number].coord[1][0]+y_vec[1]*(h-yC)-z_vec[1]*zC,
										 nodes[elements[j].nodes[1].number].coord[2][0]+y_vec[2]*(h-yC)-z_vec[2]*zC ]

								lines = [[v_11,v_12],[v_12,v_13],[v_13,v_14],[v_14,v_15],
										 [v_15,v_16],[v_16,v_17],[v_17,v_18],[v_18,v_11],
										 [v_21,v_22],[v_22,v_23],[v_23,v_24],[v_24,v_25],
										 [v_25,v_26],[v_26,v_27],[v_27,v_28],[v_28,v_21],
										 [v_11,v_21],[v_12,v_22],[v_13,v_23],[v_14,v_24],
										 [v_15,v_25],[v_16,v_26],[v_17,v_27],[v_18,v_28]]
								faces = [[v_11,v_12,v_13],[v_13,v_14,v_11],
										 [v_11,v_14,v_18],[v_18,v_14,v_15],
										 [v_15,v_16,v_17],[v_17,v_18,v_15],
										 [v_23,v_22,v_21],[v_21,v_24,v_23],
										 [v_24,v_21,v_28],[v_24,v_28,v_25],
										 [v_26,v_25,v_27],[v_28,v_27,v_25],
										 [v_11,v_21,v_12],[v_12,v_21,v_22],
										 [v_11,v_18,v_28],[v_28,v_21,v_11],
										 [v_18,v_17,v_28],[v_28,v_17,v_27],
										 [v_16,v_26,v_27],[v_27,v_17,v_16],
										 [v_16,v_15,v_25],[v_25,v_26,v_16],
										 [v_14,v_24,v_25],[v_25,v_15,v_14],
										 [v_13,v_24,v_14],[v_24,v_13,v_23],
										 [v_13,v_12,v_22],[v_22,v_23,v_13]]

							elif self.sections[elements[j].section]['Cross section']['Type'] == 'T-Beam':
								tw = self.sections[elements[j].section]['Cross section']['top width, tw']
								tt = self.sections[elements[j].section]['Cross section']['top thickness, tt']
								mt = self.sections[elements[j].section]['Cross section']['middle thickness, mt']
								h  = self.sections[elements[j].section]['Cross section']['height, h']
								A1  = mt*(h-tt)
								A2  = tt*tw
								A   = A1+A2
								yC1 = h-(tt/2.)
								yC2 = (h-tt)/2.
								if A != 0.:
									yC = (A1*yC1+A2*yC2)/A
								else:
									yC = 0.
								tw = tw/2.
								tt = tt
								mt = mt/2.
								v_11  = [nodes[elements[j].nodes[0].number].coord[0][0]-y_vec[0]*yC-z_vec[0]*mt,
										 nodes[elements[j].nodes[0].number].coord[1][0]-y_vec[1]*yC-z_vec[1]*mt,
										 nodes[elements[j].nodes[0].number].coord[2][0]-y_vec[2]*yC-z_vec[2]*mt ]
								v_12  = [nodes[elements[j].nodes[0].number].coord[0][0]-y_vec[0]*yC+z_vec[0]*mt,
										 nodes[elements[j].nodes[0].number].coord[1][0]-y_vec[1]*yC+z_vec[1]*mt,
										 nodes[elements[j].nodes[0].number].coord[2][0]-y_vec[2]*yC+z_vec[2]*mt ]
								v_17  = [nodes[elements[j].nodes[0].number].coord[0][0]+y_vec[0]*(h-yC-tt)-z_vec[0]*tw,
										 nodes[elements[j].nodes[0].number].coord[1][0]+y_vec[1]*(h-yC-tt)-z_vec[1]*tw,
										 nodes[elements[j].nodes[0].number].coord[2][0]+y_vec[2]*(h-yC-tt)-z_vec[2]*tw ]
								v_18  = [nodes[elements[j].nodes[0].number].coord[0][0]+y_vec[0]*(h-yC-tt)-z_vec[0]*mt,
										 nodes[elements[j].nodes[0].number].coord[1][0]+y_vec[1]*(h-yC-tt)-z_vec[1]*mt,
										 nodes[elements[j].nodes[0].number].coord[2][0]+y_vec[2]*(h-yC-tt)-z_vec[2]*mt ]
								v_19  = [nodes[elements[j].nodes[0].number].coord[0][0]+y_vec[0]*(h-yC-tt)+z_vec[0]*mt,
										 nodes[elements[j].nodes[0].number].coord[1][0]+y_vec[1]*(h-yC-tt)+z_vec[1]*mt,
										 nodes[elements[j].nodes[0].number].coord[2][0]+y_vec[2]*(h-yC-tt)+z_vec[2]*mt ]
								v_110 = [nodes[elements[j].nodes[0].number].coord[0][0]+y_vec[0]*(h-yC-tt)+z_vec[0]*tw,
										 nodes[elements[j].nodes[0].number].coord[1][0]+y_vec[1]*(h-yC-tt)+z_vec[1]*tw,
										 nodes[elements[j].nodes[0].number].coord[2][0]+y_vec[2]*(h-yC-tt)+z_vec[2]*tw ]
								v_111 = [nodes[elements[j].nodes[0].number].coord[0][0]+y_vec[0]*(h-yC)+z_vec[0]*tw,
										 nodes[elements[j].nodes[0].number].coord[1][0]+y_vec[1]*(h-yC)+z_vec[1]*tw,
										 nodes[elements[j].nodes[0].number].coord[2][0]+y_vec[2]*(h-yC)+z_vec[2]*tw ]
								v_112 = [nodes[elements[j].nodes[0].number].coord[0][0]+y_vec[0]*(h-yC)-z_vec[0]*tw,
										 nodes[elements[j].nodes[0].number].coord[1][0]+y_vec[1]*(h-yC)-z_vec[1]*tw,
										 nodes[elements[j].nodes[0].number].coord[2][0]+y_vec[2]*(h-yC)-z_vec[2]*tw ]
								v_21  = [nodes[elements[j].nodes[1].number].coord[0][0]-y_vec[0]*yC-z_vec[0]*mt,
										 nodes[elements[j].nodes[1].number].coord[1][0]-y_vec[1]*yC-z_vec[1]*mt,
										 nodes[elements[j].nodes[1].number].coord[2][0]-y_vec[2]*yC-z_vec[2]*mt ]
								v_22  = [nodes[elements[j].nodes[1].number].coord[0][0]-y_vec[0]*yC+z_vec[0]*mt,
										 nodes[elements[j].nodes[1].number].coord[1][0]-y_vec[1]*yC+z_vec[1]*mt,
										 nodes[elements[j].nodes[1].number].coord[2][0]-y_vec[2]*yC+z_vec[2]*mt ]
								v_27  = [nodes[elements[j].nodes[1].number].coord[0][0]+y_vec[0]*(h-yC-tt)-z_vec[0]*tw,
										 nodes[elements[j].nodes[1].number].coord[1][0]+y_vec[1]*(h-yC-tt)-z_vec[1]*tw,
										 nodes[elements[j].nodes[1].number].coord[2][0]+y_vec[2]*(h-yC-tt)-z_vec[2]*tw ]
								v_28  = [nodes[elements[j].nodes[1].number].coord[0][0]+y_vec[0]*(h-yC-tt)-z_vec[0]*mt,
										 nodes[elements[j].nodes[1].number].coord[1][0]+y_vec[1]*(h-yC-tt)-z_vec[1]*mt,
										 nodes[elements[j].nodes[1].number].coord[2][0]+y_vec[2]*(h-yC-tt)-z_vec[2]*mt ]
								v_29  = [nodes[elements[j].nodes[1].number].coord[0][0]+y_vec[0]*(h-yC-tt)+z_vec[0]*mt,
										 nodes[elements[j].nodes[1].number].coord[1][0]+y_vec[1]*(h-yC-tt)+z_vec[1]*mt,
										 nodes[elements[j].nodes[1].number].coord[2][0]+y_vec[2]*(h-yC-tt)+z_vec[2]*mt ]
								v_210 = [nodes[elements[j].nodes[1].number].coord[0][0]+y_vec[0]*(h-yC-tt)+z_vec[0]*tw,
										 nodes[elements[j].nodes[1].number].coord[1][0]+y_vec[1]*(h-yC-tt)+z_vec[1]*tw,
										 nodes[elements[j].nodes[1].number].coord[2][0]+y_vec[2]*(h-yC-tt)+z_vec[2]*tw ]
								v_211 = [nodes[elements[j].nodes[1].number].coord[0][0]+y_vec[0]*(h-yC)+z_vec[0]*tw,
										 nodes[elements[j].nodes[1].number].coord[1][0]+y_vec[1]*(h-yC)+z_vec[1]*tw,
										 nodes[elements[j].nodes[1].number].coord[2][0]+y_vec[2]*(h-yC)+z_vec[2]*tw ]
								v_212 = [nodes[elements[j].nodes[1].number].coord[0][0]+y_vec[0]*(h-yC)-z_vec[0]*tw,
										 nodes[elements[j].nodes[1].number].coord[1][0]+y_vec[1]*(h-yC)-z_vec[1]*tw,
										 nodes[elements[j].nodes[1].number].coord[2][0]+y_vec[2]*(h-yC)-z_vec[2]*tw ]

								lines = [[v_11,v_12],[v_12,v_19],[v_19,v_110],[v_110,v_111],
										 [v_111,v_112],[v_112,v_17],[v_17,v_18],[v_18,v_11],
										 [v_21,v_22],[v_22,v_29],[v_29,v_210],[v_210,v_211],
										 [v_211,v_212],[v_212,v_27],[v_27,v_28],[v_28,v_21],
										 [v_11,v_21],[v_12,v_22],[v_17,v_27],[v_18,v_28],
										 [v_19,v_29],[v_110,v_210],[v_111,v_211],[v_112,v_212]]
								faces = [[v_11,v_12,v_19],[v_19,v_18,v_11],
										 [v_112,v_17,v_110],[v_110,v_111,v_112],
										 [v_29,v_22,v_21],[v_21,v_28,v_29],
										 [v_210,v_27,v_212],[v_212,v_211,v_210],
										 [v_19,v_12,v_22],[v_22,v_29,v_19],
										 [v_11,v_18,v_28],[v_28,v_21,v_11],
										 [v_111,v_110,v_210],[v_210,v_211,v_111],
										 [v_17,v_112,v_212],[v_212,v_27,v_17],
										 [v_11,v_21,v_12],[v_21,v_22,v_12],
										 [v_112,v_111,v_212],[v_212,v_111,v_211],
										 [v_18,v_17,v_27],[v_27,v_28,v_18],
										 [v_110,v_19,v_29],[v_29,v_210,v_110]]

							else:
								pass

							glLineWidth(2.0)
							glColor3f(0.05, 0.1, 0.05)
							for line in range(len(lines)):
								glBegin(GL_LINES)
								glVertex3f(lines[line][0][0],lines[line][0][1],lines[line][0][2])
								glVertex3f(lines[line][1][0],lines[line][1][1],lines[line][1][2])
								glEnd()

							glColor3f(0.2, 0.4, 0.2)
							for face in range(len(faces)):
								glBegin(GL_TRIANGLES)
								glVertex3f(faces[face][0][0],faces[face][0][1],faces[face][0][2])
								glVertex3f(faces[face][1][0],faces[face][1][1],faces[face][1][2])
								glVertex3f(faces[face][2][0],faces[face][2][1],faces[face][2][2])
								glEnd()

			glEndList()


		else:

			if self.results[newResult].solutions[solution].type == 'Static':

				self.displayLists[solution][result][subresult]['nodes'] = glGenLists(1)
				self.displayLists[solution][result][subresult]['wireframe'] = glGenLists(1)
				self.displayLists[solution][result][subresult]['shaded'] = glGenLists(1)
				
				# displacement, nodepoints only
				glNewList(self.displayLists[solution][result][subresult]['nodes'], GL_COMPILE)

				scale_factor = self.scale_factor
				displacements = mesh.nodes

				glPointSize(5.0)
				glBegin(GL_POINTS)
				glColor3f(0.0, 0.3, 0.0)
				for i in displacements:
					glVertex3f(nodes[i].coord[0][0] + scale_factor*(displacements[i].solutions[solution]['displacement'][0]), 
							   nodes[i].coord[1][0] + scale_factor*(displacements[i].solutions[solution]['displacement'][1]),
							   nodes[i].coord[2][0] + scale_factor*(displacements[i].solutions[solution]['displacement'][2]))
				glEnd()
				glEndList()

				# wireframe mode, model with displacement, lines only
				glNewList(self.displayLists[solution][result][subresult]['wireframe'], GL_COMPILE)

				glLineWidth(3.0)
				for j in elements:
					glColor3f(0.0, 0.3, 0.0)
					nodelines = []
					if elements[j].type == 'ROD2N2D':
						nodelines = [[0,1]]
						glColor3f(0.0, 0.0, 1.0)
					elif elements[j].type == 'ROD2N':
						nodelines = [[0,1]]
						glColor3f(0.0, 0.0, 1.0)
					elif elements[j].type == 'BEAM2N2D':
						nodelines = [[0,1]]
						glColor3f(0.0, 0.0, 1.0)
					elif elements[j].type == 'BEAM2N':
						nodelines = [[0,1]]
						glColor3f(0.0, 0.0, 1.0)
					elif elements[j].type == 'TRI3N':
						nodelines = [[0,1], [1,2], [2,0]]
					elif elements[j].type == 'TRI6N':
						nodelines = [[0,3], [3,1], [1,4], [4,2], [2,5], [5,0]]
					elif elements[j].type == 'QUAD4N':
						nodelines = [[0,1], [1,2], [2,3], [0,3]]
					elif elements[j].type == 'QUAD8N':
						nodelines = [[0,1], [1,2], [2,3], [3,4], [4,5], [5,6], [6,7], [7,0]]
					elif elements[j].type == 'TET4N':
						nodelines = [[0,1], [1,2], [0,2], [0,3], [1,3], [2,3]]
					elif elements[j].type == 'TET10N':
						nodelines = [[0,4], [1,4], [1,5], [2,5], [0,6], [2,6], [0,7], [3,7], [1,8], [3,8], [2,9], [3,9]]
					elif elements[j].type == 'HEX8N':
						nodelines = [[0,1], [1,2], [2,3], [0,3], [0,4], [1,5], [2,6], [3,7], [4,5], [5,6], [6,7], [4,7]]
					elif elements[j].type == 'HEX20N':
						nodelines = [[ 0, 8], [ 8, 1], [ 1, 9], [ 9, 2], [ 2,10], [10, 3], [ 3,11], [11, 0], 
									 [ 0,12], [12, 4], [ 1,13], [13, 5], [ 2,14], [14, 6], [ 3,15], [15, 7],
									 [ 4,16], [16, 5], [ 5,17], [17, 6], [ 6,18], [18, 7], [ 7,19], [19, 4]]
					else:
						pass

					for k in range(len(nodelines)):
						glBegin(GL_LINES)
						glVertex3f(nodes[elements[j].nodes[nodelines[k][0]].number].coord[0][0] + 
									scale_factor*(displacements[elements[j].nodes[nodelines[k][0]].number].solutions[solution]['displacement'][0]),
								   nodes[elements[j].nodes[nodelines[k][0]].number].coord[1][0] +
									scale_factor*(displacements[elements[j].nodes[nodelines[k][0]].number].solutions[solution]['displacement'][1]),
								   nodes[elements[j].nodes[nodelines[k][0]].number].coord[2][0] +
									scale_factor*(displacements[elements[j].nodes[nodelines[k][0]].number].solutions[solution]['displacement'][2]))
						glVertex3f(nodes[elements[j].nodes[nodelines[k][1]].number].coord[0][0] +
									scale_factor*(displacements[elements[j].nodes[nodelines[k][1]].number].solutions[solution]['displacement'][0]),
								   nodes[elements[j].nodes[nodelines[k][1]].number].coord[1][0] +
									scale_factor*(displacements[elements[j].nodes[nodelines[k][1]].number].solutions[solution]['displacement'][1]),
								   nodes[elements[j].nodes[nodelines[k][1]].number].coord[2][0] +
									scale_factor*(displacements[elements[j].nodes[nodelines[k][1]].number].solutions[solution]['displacement'][2]))
						glEnd()
						
					if result == 'elementforce':
						if elements[j].type in ['BEAM2N2D', 'BEAM2N']:
							# Draw bending or shear diagram
							disp_max = 0.
							disp_min = 0.
							for i in elements:
								if 'elementforce' not in elements[i].solutions[solution]:
									pass
								elif elements[i].type not in ['BEAM2N', 'BEAM2N2D']:
									pass
								elif subresult == 'FY':
									if elements[i].solutions[solution]['elementforce'][1] >= disp_max:
										disp_max = elements[i].solutions[solution]['elementforce'][1]
									if elements[i].solutions[solution]['elementforce'][6] >= disp_max:
										disp_max = elements[i].solutions[solution]['elementforce'][6]
								elif subresult == 'FZ':
									if elements[i].solutions[solution]['elementforce'][2] >= disp_max:
										disp_max = elements[i].solutions[solution]['elementforce'][2]
									if elements[i].solutions[solution]['elementforce'][7] >= disp_max:
										disp_max = elements[i].solutions[solution]['elementforce'][7]
								elif subresult == 'MX':
									if elements[i].solutions[solution]['elementforce'][3] >= disp_max:
										disp_max = elements[i].solutions[solution]['elementforce'][3]
									if elements[i].solutions[solution]['elementforce'][8] >= disp_max:
										disp_max = elements[i].solutions[solution]['elementforce'][8]
								elif subresult == 'MY':
									if elements[i].solutions[solution]['elementforce'][4] >= disp_max:
										disp_max = elements[i].solutions[solution]['elementforce'][4]
									if elements[i].solutions[solution]['elementforce'][9] >= disp_max:
										disp_max = elements[i].solutions[solution]['elementforce'][9]
								elif subresult == 'MZ':
									if elements[i].solutions[solution]['elementforce'][5] >= disp_max:
										disp_max = elements[i].solutions[solution]['elementforce'][5]
									if elements[i].solutions[solution]['elementforce'][10] >= disp_max:
										disp_max = elements[i].solutions[solution]['elementforce'][10]
								else:
									pass

							scale = max([abs(disp_min), abs(disp_max)])
							if scale == 0.:
								scale = 1.e-9
							n1 = [nodes[elements[j].nodes[0].number].coord[0][0] +
									scale_factor*(displacements[elements[j].nodes[0].number].solutions[solution]['displacement'][0]),
								  nodes[elements[j].nodes[0].number].coord[1][0] +
									scale_factor*(displacements[elements[j].nodes[0].number].solutions[solution]['displacement'][1]),
								  nodes[elements[j].nodes[0].number].coord[2][0] +
									scale_factor*(displacements[elements[j].nodes[0].number].solutions[solution]['displacement'][2])]
							n2 = [nodes[elements[j].nodes[1].number].coord[0][0] +
									scale_factor*(displacements[elements[j].nodes[0].number].solutions[solution]['displacement'][0]),
								  nodes[elements[j].nodes[1].number].coord[1][0] +
									scale_factor*(displacements[elements[j].nodes[0].number].solutions[solution]['displacement'][1]),
								  nodes[elements[j].nodes[1].number].coord[2][0] +
									scale_factor*(displacements[elements[j].nodes[0].number].solutions[solution]['displacement'][2])]
							if subresult in ['FY', 'FZ']:
								glColor4f(0.8, 0.4, 0.1, 0.7)
								if subresult == 'FY':
									shear_n1 = elements[j].solutions[solution]['elementforce'][1]
									shear_n2 = elements[j].solutions[solution]['elementforce'][6]
									vector = 'y-vec'
								else:
									shear_n1 = elements[j].solutions[solution]['elementforce'][2]
									shear_n2 = elements[j].solutions[solution]['elementforce'][7]
									vector = 'z-vec'
								crossing_zero = False
								ratio = 0.5
								if(shear_n1<0 and shear_n2>0):
									shear_n1 = -abs(shear_n1)
									shear_n2 = -abs(shear_n2)
								elif(shear_n1>0 and shear_n2<0):
									shear_n1 = abs(shear_n1)
									shear_n2 = abs(shear_n2)
								elif(shear_n1<0 and shear_n2<0):
									shear_n1 = -abs(shear_n1)
									shear_n2 = abs(shear_n2)
									crossing_zero = True
									ratio = shear_n1/shear_n2
								elif(shear_n1>0 and shear_n2>0):
									shear_n1 = abs(shear_n1)
									shear_n2 = -abs(shear_n2)
									crossing_zero = True
									ratio = shear_n1/shear_n2
								elif(shear_n1>0 and shear_n2==0):
									shear_n1 = abs(shear_n1)
								elif(shear_n1<0 and shear_n2==0):
									shear_n1 = -abs(shear_n1)
								elif(shear_n1==0 and shear_n2>0):
									shear_n2 = -abs(shear_n2)
								elif(shear_n1==0 and shear_n2<0):
									shear_n2 = abs(shear_n2)
								else:
									pass
								if crossing_zero:
									cross_at = [0.,0.,0.]
									cross_at[0] = n1[0] - (n2[0]-n1[0])*ratio/(1.-ratio)
									cross_at[1] = n1[1] - (n2[1]-n1[1])*ratio/(1.-ratio)
									cross_at[2] = n1[2] - (n2[2]-n1[2])*ratio/(1.-ratio)
									# triangle 1
									glBegin(GL_TRIANGLES)
									glVertex3f( n1[0], n1[1], n1[2] )
									glVertex3f( cross_at[0], cross_at[1], cross_at[2] )
									glVertex3f( n1[0] +	elements[j].orientation[vector][0]*(shear_n1/scale)*self.scaleShearBendDiagram,
											    n1[1] + elements[j].orientation[vector][1]*(shear_n1/scale)*self.scaleShearBendDiagram,
											    n1[2] + elements[j].orientation[vector][2]*(shear_n1/scale)*self.scaleShearBendDiagram )
									glEnd()
									# triangle 2
									glBegin(GL_TRIANGLES)
									glVertex3f( n1[0], n1[1], n1[2] )
									glVertex3f( n1[0] +	elements[j].orientation[vector][0]*(shear_n1/scale)*self.scaleShearBendDiagram,
											    n1[1] + elements[j].orientation[vector][1]*(shear_n1/scale)*self.scaleShearBendDiagram,
											    n1[2] + elements[j].orientation[vector][2]*(shear_n1/scale)*self.scaleShearBendDiagram )
									glVertex3f(cross_at[0], cross_at[1], cross_at[2])
									glEnd()
									# triangle 3
									glBegin(GL_TRIANGLES)
									glVertex3f(cross_at[0], cross_at[1], cross_at[2])
									glVertex3f( n2[0], n2[1], n2[2] )
									glVertex3f( n2[0] +	elements[j].orientation[vector][0]*(shear_n2/scale)*self.scaleShearBendDiagram,
											    n2[1] + elements[j].orientation[vector][1]*(shear_n2/scale)*self.scaleShearBendDiagram,
											    n2[2] + elements[j].orientation[vector][2]*(shear_n2/scale)*self.scaleShearBendDiagram )
									glEnd()
									# triangle 4
									glBegin(GL_TRIANGLES)
									glVertex3f(cross_at[0], cross_at[1], cross_at[2])
									glVertex3f( n2[0] +	elements[j].orientation[vector][0]*(shear_n2/scale)*self.scaleShearBendDiagram,
											    n2[1] + elements[j].orientation[vector][1]*(shear_n2/scale)*self.scaleShearBendDiagram,
											    n2[2] + elements[j].orientation[vector][2]*(shear_n2/scale)*self.scaleShearBendDiagram )
									glVertex3f( n2[0], n2[1], n2[2] )
									glEnd()
								else:
									# triangle 1
									glBegin(GL_TRIANGLES)
									glVertex3f( n1[0], n1[1], n1[2] )
									glVertex3f( n2[0], n2[1], n2[2] )
									glVertex3f( n1[0] +	elements[j].orientation[vector][0]*(shear_n1/scale)*self.scaleShearBendDiagram,
											    n1[1] + elements[j].orientation[vector][1]*(shear_n1/scale)*self.scaleShearBendDiagram,
											    n1[2] + elements[j].orientation[vector][2]*(shear_n1/scale)*self.scaleShearBendDiagram )
									glEnd()
									# triangle 2
									glBegin(GL_TRIANGLES)
									glVertex3f( n1[0], n1[1], n1[2] )
									glVertex3f( n1[0] +	elements[j].orientation[vector][0]*(shear_n1/scale)*self.scaleShearBendDiagram,
											    n1[1] + elements[j].orientation[vector][1]*(shear_n1/scale)*self.scaleShearBendDiagram,
											    n1[2] + elements[j].orientation[vector][2]*(shear_n1/scale)*self.scaleShearBendDiagram )
									glVertex3f( n2[0], n2[1], n2[2] )
									glEnd()
									# triangle 3
									glBegin(GL_TRIANGLES)
									glVertex3f( n1[0] +	elements[j].orientation[vector][0]*(shear_n1/scale)*self.scaleShearBendDiagram,
											    n1[1] + elements[j].orientation[vector][1]*(shear_n1/scale)*self.scaleShearBendDiagram,
											    n1[2] + elements[j].orientation[vector][2]*(shear_n1/scale)*self.scaleShearBendDiagram )
									glVertex3f( n2[0], n2[1], n2[2] )
									glVertex3f( n2[0] +	elements[j].orientation[vector][0]*(shear_n2/scale)*self.scaleShearBendDiagram,
											    n2[1] + elements[j].orientation[vector][1]*(shear_n2/scale)*self.scaleShearBendDiagram,
											    n2[2] + elements[j].orientation[vector][2]*(shear_n2/scale)*self.scaleShearBendDiagram )
									glEnd()
									# triangle 4
									glBegin(GL_TRIANGLES)
									glVertex3f( n1[0] +	elements[j].orientation[vector][0]*(shear_n1/scale)*self.scaleShearBendDiagram,
											    n1[1] + elements[j].orientation[vector][1]*(shear_n1/scale)*self.scaleShearBendDiagram,
											    n1[2] + elements[j].orientation[vector][2]*(shear_n1/scale)*self.scaleShearBendDiagram )
									glVertex3f( n2[0] +	elements[j].orientation[vector][0]*(shear_n2/scale)*self.scaleShearBendDiagram,
											    n2[1] + elements[j].orientation[vector][1]*(shear_n2/scale)*self.scaleShearBendDiagram,
											    n2[2] + elements[j].orientation[vector][2]*(shear_n2/scale)*self.scaleShearBendDiagram )
									glVertex3f( n2[0], n2[1], n2[2] )
									glEnd()
							elif subresult in ['MX', 'MY', 'MZ']:
								glColor4f(0.5, 0.1, 0.5, 0.7)
								if subresult == 'MX':
									bend_n1 = elements[j].solutions[solution]['elementforce'][3]
									bend_n2 = elements[j].solutions[solution]['elementforce'][8]
									vector = 'y-vec'
								elif subresult == 'MY':
									bend_n1 = elements[j].solutions[solution]['elementforce'][4]
									bend_n2 = elements[j].solutions[solution]['elementforce'][9]
									vector = 'z-vec'
								else:
									bend_n1 = elements[j].solutions[solution]['elementforce'][5]
									bend_n2 = elements[j].solutions[solution]['elementforce'][10]
									vector = 'y-vec'
								crossing_zero = False
								ratio = 0.5
								if(bend_n1<0 and bend_n2>0):
									bend_n1 = -abs(bend_n1)
									bend_n2 = -abs(bend_n2)
								elif(bend_n1<0 and bend_n2<0):
									bend_n1 = -abs(bend_n1)
									bend_n2 = abs(bend_n2)
									crossing_zero = True
									ratio = bend_n1/bend_n2
								elif(bend_n1>0 and bend_n2>0):
									bend_n1 = abs(bend_n1)
									bend_n2 = -abs(bend_n2)
									crossing_zero = True
									ratio = bend_n1/bend_n2
								elif(bend_n1>0 and bend_n2<0):
									bend_n1 = abs(bend_n1)
									bend_n2 = abs(bend_n2)
								elif(bend_n1>0 and bend_n2==0):
									bend_n1 = abs(bend_n1)
								elif(bend_n1<0 and bend_n2==0):
									bend_n1 = -abs(bend_n1)
								elif(bend_n1==0 and bend_n2>0):
									bend_n2 = -abs(bend_n2)
								elif(bend_n1==0 and bend_n2<0):
									bend_n2 = abs(bend_n2)
								else:
									pass
								if crossing_zero:
									cross_at = [0.,0.,0.]
									cross_at[0] = n1[0] - (n2[0]-n1[0])*ratio/(1.-ratio)
									cross_at[1] = n1[1] - (n2[1]-n1[1])*ratio/(1.-ratio)
									cross_at[2] = n1[2] - (n2[2]-n1[2])*ratio/(1.-ratio)
									# triangle 1
									glBegin(GL_TRIANGLES)
									glVertex3f( n1[0], n1[1], n1[2] )
									glVertex3f( cross_at[0], cross_at[1], cross_at[2] )
									glVertex3f( n1[0] +	elements[j].orientation[vector][0]*(bend_n1/scale)*self.scaleShearBendDiagram,
											    n1[1] + elements[j].orientation[vector][1]*(bend_n1/scale)*self.scaleShearBendDiagram,
											    n1[2] + elements[j].orientation[vector][2]*(bend_n1/scale)*self.scaleShearBendDiagram )
									glEnd()
									# triangle 2
									glBegin(GL_TRIANGLES)
									glVertex3f( n1[0], n1[1], n1[2] )
									glVertex3f( n1[0] +	elements[j].orientation[vector][0]*(bend_n1/scale)*self.scaleShearBendDiagram,
											    n1[1] + elements[j].orientation[vector][1]*(bend_n1/scale)*self.scaleShearBendDiagram,
											    n1[2] + elements[j].orientation[vector][2]*(bend_n1/scale)*self.scaleShearBendDiagram )
									glVertex3f(cross_at[0], cross_at[1], cross_at[2])
									glEnd()
									# triangle 3
									glBegin(GL_TRIANGLES)
									glVertex3f(cross_at[0], cross_at[1], cross_at[2])
									glVertex3f( n2[0], n2[1], n2[2] )
									glVertex3f( n2[0] +	elements[j].orientation[vector][0]*(bend_n2/scale)*self.scaleShearBendDiagram,
											    n2[1] + elements[j].orientation[vector][1]*(bend_n2/scale)*self.scaleShearBendDiagram,
											    n2[2] + elements[j].orientation[vector][2]*(bend_n2/scale)*self.scaleShearBendDiagram )
									glEnd()
									# triangle 4
									glBegin(GL_TRIANGLES)
									glVertex3f(cross_at[0], cross_at[1], cross_at[2])
									glVertex3f( n2[0] +	elements[j].orientation[vector][0]*(bend_n2/scale)*self.scaleShearBendDiagram,
											    n2[1] + elements[j].orientation[vector][1]*(bend_n2/scale)*self.scaleShearBendDiagram,
											    n2[2] + elements[j].orientation[vector][2]*(bend_n2/scale)*self.scaleShearBendDiagram )
									glVertex3f( n2[0], n2[1], n2[2] )
									glEnd()
								else:
									# triangle 1
									glBegin(GL_TRIANGLES)
									glVertex3f( n1[0], n1[1], n1[2] )
									glVertex3f( n2[0], n2[1], n2[2] )
									glVertex3f( n1[0] +	elements[j].orientation[vector][0]*(bend_n1/scale)*self.scaleShearBendDiagram,
											    n1[1] + elements[j].orientation[vector][1]*(bend_n1/scale)*self.scaleShearBendDiagram,
											    n1[2] + elements[j].orientation[vector][2]*(bend_n1/scale)*self.scaleShearBendDiagram )
									glEnd()
									# triangle 2
									glBegin(GL_TRIANGLES)
									glVertex3f( n1[0], n1[1], n1[2] )
									glVertex3f( n1[0] +	elements[j].orientation[vector][0]*(bend_n1/scale)*self.scaleShearBendDiagram,
											    n1[1] + elements[j].orientation[vector][1]*(bend_n1/scale)*self.scaleShearBendDiagram,
											    n1[2] + elements[j].orientation[vector][2]*(bend_n1/scale)*self.scaleShearBendDiagram )
									glVertex3f( n2[0], n2[1], n2[2] )
									glEnd()
									# triangle 3
									glBegin(GL_TRIANGLES)
									glVertex3f( n1[0] +	elements[j].orientation[vector][0]*(bend_n1/scale)*self.scaleShearBendDiagram,
											    n1[1] + elements[j].orientation[vector][1]*(bend_n1/scale)*self.scaleShearBendDiagram,
											    n1[2] + elements[j].orientation[vector][2]*(bend_n1/scale)*self.scaleShearBendDiagram )
									glVertex3f( n2[0], n2[1], n2[2] )
									glVertex3f( n2[0] +	elements[j].orientation[vector][0]*(bend_n2/scale)*self.scaleShearBendDiagram,
											    n2[1] + elements[j].orientation[vector][1]*(bend_n2/scale)*self.scaleShearBendDiagram,
											    n2[2] + elements[j].orientation[vector][2]*(bend_n2/scale)*self.scaleShearBendDiagram )
									glEnd()
									# triangle 4
									glBegin(GL_TRIANGLES)
									glVertex3f( n1[0] +	elements[j].orientation[vector][0]*(bend_n1/scale)*self.scaleShearBendDiagram,
											    n1[1] + elements[j].orientation[vector][1]*(bend_n1/scale)*self.scaleShearBendDiagram,
											    n1[2] + elements[j].orientation[vector][2]*(bend_n1/scale)*self.scaleShearBendDiagram )
									glVertex3f( n2[0] +	elements[j].orientation[vector][0]*(bend_n2/scale)*self.scaleShearBendDiagram,
											    n2[1] + elements[j].orientation[vector][1]*(bend_n2/scale)*self.scaleShearBendDiagram,
											    n2[2] + elements[j].orientation[vector][2]*(bend_n2/scale)*self.scaleShearBendDiagram )
									glVertex3f( n2[0], n2[1], n2[2] )
									glEnd()
					
				glEndList()


				if result == 'displacement':

					# shaded mode, model with displacements, contoured elements to show values
					disp_max = 0.
					disp_min = 0.
					for i in nodes:
						if subresult == 'magnitude':
							if nodes[i].solutions[solution]['displacement'][6] >= disp_max:
								disp_max = nodes[i].solutions[solution]['displacement'][6]
							if nodes[i].solutions[solution]['displacement'][6] <= disp_min:
								disp_min = nodes[i].solutions[solution]['displacement'][6]
							self.displayLists[solution][result][subresult]['info'] = 'Max %.4E' % (disp_max)
						elif subresult == 'x-dir':
							if nodes[i].solutions[solution]['displacement'][0] >= disp_max:
								disp_max = nodes[i].solutions[solution]['displacement'][0]
							if nodes[i].solutions[solution]['displacement'][0] <= disp_min:
								disp_min = nodes[i].solutions[solution]['displacement'][0]
							self.displayLists[solution][result][subresult]['info'] = 'Max %.4E   Min %.4E' % (disp_max, disp_min)
						elif subresult == 'y-dir':
							if nodes[i].solutions[solution]['displacement'][1] >= disp_max:
								disp_max = nodes[i].solutions[solution]['displacement'][1]
							if nodes[i].solutions[solution]['displacement'][1] <= disp_min:
								disp_min = nodes[i].solutions[solution]['displacement'][1]
							self.displayLists[solution][result][subresult]['info'] = 'Max %.4E   Min %.4E' % (disp_max, disp_min)
						elif subresult == 'z-dir':
							if nodes[i].solutions[solution]['displacement'][2] >= disp_max:
								disp_max = nodes[i].solutions[solution]['displacement'][2]
							if nodes[i].solutions[solution]['displacement'][2] <= disp_min:
								disp_min = nodes[i].solutions[solution]['displacement'][2]
							self.displayLists[solution][result][subresult]['info'] = 'Max %.4E   Min %.4E' % (disp_max, disp_min)
						else:
							pass

					self.displayLists[solution][result][subresult]['max_val'] = disp_max
					self.displayLists[solution][result][subresult]['min_val'] = disp_min

					glNewList(self.displayLists[solution][result][subresult]['shaded'], GL_COMPILE)

					disp_mag_values = [ disp_min,
										disp_min+(disp_max-disp_min)*1./12.,
										disp_min+(disp_max-disp_min)*2./12.,
										disp_min+(disp_max-disp_min)*3./12.,
										disp_min+(disp_max-disp_min)*4./12.,
										disp_min+(disp_max-disp_min)*5./12.,
										disp_min+(disp_max-disp_min)*6./12.,
										disp_min+(disp_max-disp_min)*7./12.,
										disp_min+(disp_max-disp_min)*8./12.,
										disp_min+(disp_max-disp_min)*9./12.,
										disp_min+(disp_max-disp_min)*10./12.,
										disp_min+(disp_max-disp_min)*11./12.,
										disp_max ]
					disp_colors = [ (  0.0,   0.0,   1.0), # blue
									(  0.0, 0.333,   1.0),  
									(  0.0, 0.666,   1.0),  
									(  0.0,   1.0,   1.0),  
									(  0.0,   1.0, 0.666),  
									(  0.0,   1.0, 0.333),
									(  0.0,   1.0,   0.0), # green
									(0.333,   1.0,   0.0),  
									(0.666,   1.0,   0.0),  
									(  1.0,   1.0,   0.0),  
									(  1.0, 0.666,   0.0),  
									(  1.0, 0.333,   0.0),
									(  1.0,   0.0,   0.0) ] # red
					disp_color = disp_colors[0]

					for j in elements:
						facenodes = []
						nodelines = []
						if elements[j].type == 'ROD2N2D':
#							glLineWidth(8.0)
							nodelines = [[0,1]]
						elif elements[j].type == 'ROD2N':
#							glLineWidth(8.0)
							nodelines = [[0,1]]
						elif elements[j].type == 'BEAM2N2D':
#							glLineWidth(8.0)
							nodelines = [[0,1]]
						elif elements[j].type == 'BEAM2N':
#							glLineWidth(8.0)
							nodelines = [[0,1]]
						elif elements[j].type == 'TRI3N':
							facenodes = [[0,1,2]]
						elif elements[j].type == 'TRI6N':
							facenodes = [[0,3,5], [3,1,4], [4,2,5], [5,3,4]]
						elif elements[j].type == 'QUAD4N':
							facenodes = [[0,1,3], [1,2,3]]
						elif elements[j].type == 'QUAD8N':
							facenodes = [[0,1,7], [1,2,3], [3,4,5], [5,6,7], [1,3,7], [5,7,3]]
						elif elements[j].type == 'TET4N':
							facenodes = [[0,1,3], [1,2,3], [2,0,3], [0,2,1]]
						elif elements[j].type == 'TET10N':
							facenodes = [[0,4,7], [7,4,8], [8,4,1], [7,8,3], [1,5,8], [8,5,9], [9,3,8], [5,2,9],
										 [2,6,9], [9,6,7], [6,0,7], [9,7,3], [5,6,2], [4,0,6], [6,5,4], [4,5,1]]
						elif elements[j].type == 'HEX8N':
							facenodes = [[2,1,0], [0,3,2], [3,7,2], [2,7,6], [7,3,0], [0,4,7], [5,6,7], [7,4,5],
										 [1,2,6], [1,6,5], [1,4,0], [5,4,1]]
						elif elements[j].type == 'HEX20N':
							facenodes = [[ 0, 8,12], [ 8, 1,13], [13, 5,16], [16, 4,12], [ 8,13,12], [12,13,16],
										 [ 2,10,14], [10, 3,15], [15, 7,18], [18, 6,14], [15,14,10], [18,14,15],
										 [ 1, 9,13], [ 9, 2,14], [14, 6,17], [17, 5,13], [13, 9,14], [13,14,17],
										 [ 3,11,15], [15,19, 7], [19,12, 4], [12,11, 0], [12,15,11], [12,19,15],
										 [ 9, 1, 8], [ 2, 9,10], [ 3,10,11], [ 0,11, 8], [ 9, 8,10], [10, 8,11],
										 [ 5,17,16], [17, 6,18], [18, 7,19], [19, 4,16], [16,17,18], [18,19,16]]
						else:
							pass

						for l in range(len(nodelines)):
							glBegin(GL_LINES)
							for k in range(len(disp_mag_values)):
								if subresult == 'magnitude' and (displacements[elements[j].nodes[nodelines[l][0]].number].solutions[solution] \
																										['displacement'][6] > disp_mag_values[k]):
										pass
								elif subresult == 'x-dir' and (displacements[elements[j].nodes[nodelines[l][0]].number].solutions[solution] \
																										['displacement'][0] > disp_mag_values[k]):
										pass
								elif subresult == 'y-dir' and (displacements[elements[j].nodes[nodelines[l][0]].number].solutions[solution] \
																										['displacement'][1] > disp_mag_values[k]):
										pass
								elif subresult == 'z-dir' and (displacements[elements[j].nodes[nodelines[l][0]].number].solutions[solution] \
																										['displacement'][2] > disp_mag_values[k]):
										pass
								else:
									disp_color = disp_colors[k]
									break
							node1_color = deepcopy(disp_color)
							glColor3f(disp_color[0], disp_color[1], disp_color[2])
							glVertex3f(nodes[elements[j].nodes[nodelines[l][0]].number].coord[0][0] + 
										scale_factor*(displacements[elements[j].nodes[nodelines[l][0]].number].solutions[solution]['displacement'][0]),
									   nodes[elements[j].nodes[nodelines[l][0]].number].coord[1][0] +
										scale_factor*(displacements[elements[j].nodes[nodelines[l][0]].number].solutions[solution]['displacement'][1]),
									   nodes[elements[j].nodes[nodelines[l][0]].number].coord[2][0] +
										scale_factor*(displacements[elements[j].nodes[nodelines[l][0]].number].solutions[solution]['displacement'][2]))
							for k in range(len(disp_mag_values)):
								if subresult == 'magnitude' and (displacements[elements[j].nodes[nodelines[l][1]].number].solutions[solution] \
																										['displacement'][6] > disp_mag_values[k]):
										pass
								elif subresult == 'x-dir' and (displacements[elements[j].nodes[nodelines[l][1]].number].solutions[solution] \
																										['displacement'][0] > disp_mag_values[k]):
										pass
								elif subresult == 'y-dir' and (displacements[elements[j].nodes[nodelines[l][1]].number].solutions[solution] \
																										['displacement'][1] > disp_mag_values[k]):
										pass
								elif subresult == 'z-dir' and (displacements[elements[j].nodes[nodelines[l][1]].number].solutions[solution] \
																										['displacement'][2] > disp_mag_values[k]):
										pass
								else:
									disp_color = disp_colors[k]
									break
							node2_color = deepcopy(disp_color)
							glColor3f(disp_color[0], disp_color[1], disp_color[2])
							glVertex3f(nodes[elements[j].nodes[nodelines[l][1]].number].coord[0][0] + 
										scale_factor*(displacements[elements[j].nodes[nodelines[l][1]].number].solutions[solution]['displacement'][0]),
									   nodes[elements[j].nodes[nodelines[l][1]].number].coord[1][0] +
										scale_factor*(displacements[elements[j].nodes[nodelines[l][1]].number].solutions[solution]['displacement'][1]),
									   nodes[elements[j].nodes[nodelines[l][1]].number].coord[2][0] +
										scale_factor*(displacements[elements[j].nodes[nodelines[l][1]].number].solutions[solution]['displacement'][2]))
							glEnd()

						for l in range(len(facenodes)):
							glBegin(GL_TRIANGLES)
							for k in range(len(disp_mag_values)):
								if subresult == 'magnitude' and (displacements[elements[j].nodes[facenodes[l][0]].number].solutions[solution] \
																										['displacement'][6] > disp_mag_values[k]):
										pass
								elif subresult == 'x-dir' and (displacements[elements[j].nodes[facenodes[l][0]].number].solutions[solution] \
																										['displacement'][0] > disp_mag_values[k]):
										pass
								elif subresult == 'y-dir' and (displacements[elements[j].nodes[facenodes[l][0]].number].solutions[solution] \
																										['displacement'][1] > disp_mag_values[k]):
										pass
								elif subresult == 'z-dir' and (displacements[elements[j].nodes[facenodes[l][0]].number].solutions[solution] \
																										['displacement'][2] > disp_mag_values[k]):
										pass
								else:
									disp_color = disp_colors[k]
									break
							glColor3f(disp_color[0], disp_color[1], disp_color[2])
							glVertex3f(nodes[elements[j].nodes[facenodes[l][0]].number].coord[0][0] + 
										scale_factor*(displacements[elements[j].nodes[facenodes[l][0]].number].solutions[solution]['displacement'][0]),
									   nodes[elements[j].nodes[facenodes[l][0]].number].coord[1][0] +
										scale_factor*(displacements[elements[j].nodes[facenodes[l][0]].number].solutions[solution]['displacement'][1]),
									   nodes[elements[j].nodes[facenodes[l][0]].number].coord[2][0] +
										scale_factor*(displacements[elements[j].nodes[facenodes[l][0]].number].solutions[solution]['displacement'][2]))
							for k in range(len(disp_mag_values)):
								if subresult == 'magnitude' and (displacements[elements[j].nodes[facenodes[l][1]].number].solutions[solution] \
																										['displacement'][6] > disp_mag_values[k]):
										pass
								elif subresult == 'x-dir' and (displacements[elements[j].nodes[facenodes[l][1]].number].solutions[solution] \
																										['displacement'][0] > disp_mag_values[k]):
										pass
								elif subresult == 'y-dir' and (displacements[elements[j].nodes[facenodes[l][1]].number].solutions[solution] \
																										['displacement'][1] > disp_mag_values[k]):
										pass
								elif subresult == 'z-dir' and (displacements[elements[j].nodes[facenodes[l][1]].number].solutions[solution] \
																										['displacement'][2] > disp_mag_values[k]):
										pass
								else:
									disp_color = disp_colors[k]
									break
							glColor3f(disp_color[0], disp_color[1], disp_color[2])
							glVertex3f(nodes[elements[j].nodes[facenodes[l][1]].number].coord[0][0] + 
										scale_factor*(displacements[elements[j].nodes[facenodes[l][1]].number].solutions[solution]['displacement'][0]),
									   nodes[elements[j].nodes[facenodes[l][1]].number].coord[1][0] +
										scale_factor*(displacements[elements[j].nodes[facenodes[l][1]].number].solutions[solution]['displacement'][1]),
									   nodes[elements[j].nodes[facenodes[l][1]].number].coord[2][0] +
										scale_factor*(displacements[elements[j].nodes[facenodes[l][1]].number].solutions[solution]['displacement'][2]))
							for k in range(len(disp_mag_values)):
								if subresult == 'magnitude' and (displacements[elements[j].nodes[facenodes[l][2]].number].solutions[solution] \
																										['displacement'][6] > disp_mag_values[k]):
										pass
								elif subresult == 'x-dir' and (displacements[elements[j].nodes[facenodes[l][2]].number].solutions[solution] \
																										['displacement'][0] > disp_mag_values[k]):
										pass
								elif subresult == 'y-dir' and (displacements[elements[j].nodes[facenodes[l][2]].number].solutions[solution] \
																										['displacement'][1] > disp_mag_values[k]):
										pass
								elif subresult == 'z-dir' and (displacements[elements[j].nodes[facenodes[l][2]].number].solutions[solution] \
																										['displacement'][2] > disp_mag_values[k]):
										pass
								else:
									disp_color = disp_colors[k]
									break
							glColor3f(disp_color[0], disp_color[1], disp_color[2])
							glVertex3f(nodes[elements[j].nodes[facenodes[l][2]].number].coord[0][0] + 
										scale_factor*(displacements[elements[j].nodes[facenodes[l][2]].number].solutions[solution]['displacement'][0]),
									   nodes[elements[j].nodes[facenodes[l][2]].number].coord[1][0] +
										scale_factor*(displacements[elements[j].nodes[facenodes[l][2]].number].solutions[solution]['displacement'][1]),
									   nodes[elements[j].nodes[facenodes[l][2]].number].coord[2][0] +
										scale_factor*(displacements[elements[j].nodes[facenodes[l][2]].number].solutions[solution]['displacement'][2]))
							glEnd()
							
							

						if elements[j].type in ['BEAM2N2D', 'BEAM2N', 'ROD2N2D', 'ROD2N']:
						
							if hasattr(elements[j],'crossSection'):
								if hasattr(elements[j],'orientation'):
									node1_coord = [nodes[elements[j].nodes[0].number].coord[0][0] + 
													scale_factor*(displacements[elements[j].nodes[0].number].solutions[solution]['displacement'][0]),
												   nodes[elements[j].nodes[0].number].coord[1][0] +
													scale_factor*(displacements[elements[j].nodes[0].number].solutions[solution]['displacement'][1]),
												   nodes[elements[j].nodes[0].number].coord[2][0] +
													scale_factor*(displacements[elements[j].nodes[0].number].solutions[solution]['displacement'][2])]
									node1_rotation = [scale_factor*(displacements[elements[j].nodes[0].number].solutions[solution]['displacement'][3]),
													  scale_factor*(displacements[elements[j].nodes[0].number].solutions[solution]['displacement'][4]),
													  scale_factor*(displacements[elements[j].nodes[0].number].solutions[solution]['displacement'][5])]
									node2_coord = [nodes[elements[j].nodes[1].number].coord[0][0] +
													scale_factor*(displacements[elements[j].nodes[1].number].solutions[solution]['displacement'][0]),
												   nodes[elements[j].nodes[1].number].coord[1][0] +
													scale_factor*(displacements[elements[j].nodes[1].number].solutions[solution]['displacement'][1]),
												   nodes[elements[j].nodes[1].number].coord[2][0] +
													scale_factor*(displacements[elements[j].nodes[1].number].solutions[solution]['displacement'][2])]
									node2_rotation = [scale_factor*(displacements[elements[j].nodes[1].number].solutions[solution]['displacement'][3]),
													  scale_factor*(displacements[elements[j].nodes[1].number].solutions[solution]['displacement'][4]),
													  scale_factor*(displacements[elements[j].nodes[1].number].solutions[solution]['displacement'][5])]
									faces = []
									lines = []
									x_vec = elements[j].orientation['x-vec']
									y_vec = elements[j].orientation['y-vec']
									z_vec = elements[j].orientation['z-vec']

									if elements[j].crossSection['Type'] == 'Rectangle':

										w  = elements[j].crossSection['width, w']
										h  = elements[j].crossSection['height, h']
										iw = elements[j].crossSection['inner width, iw']
										ih = elements[j].crossSection['inner height, ih']
										w  = w/2.
										h  = h/2.
										iw = iw/2.
										ih = ih/2.
										v_11 = [[node1_coord[0]-y_vec[0]*h-z_vec[0]*w,
												 node1_coord[1]-y_vec[1]*h-z_vec[1]*w,
												 node1_coord[2]-y_vec[2]*h-z_vec[2]*w ], node1_color]
										v_12 = [[node1_coord[0]-y_vec[0]*h+z_vec[0]*w,
												 node1_coord[1]-y_vec[1]*h+z_vec[1]*w,
												 node1_coord[2]-y_vec[2]*h+z_vec[2]*w ], node1_color]
										v_13 = [[node1_coord[0]+y_vec[0]*h+z_vec[0]*w,
												 node1_coord[1]+y_vec[1]*h+z_vec[1]*w,
												 node1_coord[2]+y_vec[2]*h+z_vec[2]*w ], node1_color]
										v_14 = [[node1_coord[0]+y_vec[0]*h-z_vec[0]*w,
												 node1_coord[1]+y_vec[1]*h-z_vec[1]*w,
												 node1_coord[2]+y_vec[2]*h-z_vec[2]*w ], node1_color]
										v_21 = [[node2_coord[0]-y_vec[0]*h-z_vec[0]*w,
												 node2_coord[1]-y_vec[1]*h-z_vec[1]*w,
												 node2_coord[2]-y_vec[2]*h-z_vec[2]*w ], node2_color]
										v_22 = [[node2_coord[0]-y_vec[0]*h+z_vec[0]*w,
												 node2_coord[1]-y_vec[1]*h+z_vec[1]*w,
												 node2_coord[2]-y_vec[2]*h+z_vec[2]*w ], node2_color]
										v_23 = [[node2_coord[0]+y_vec[0]*h+z_vec[0]*w,
												 node2_coord[1]+y_vec[1]*h+z_vec[1]*w,
												 node2_coord[2]+y_vec[2]*h+z_vec[2]*w ], node2_color]
										v_24 = [[node2_coord[0]+y_vec[0]*h-z_vec[0]*w,
												 node2_coord[1]+y_vec[1]*h-z_vec[1]*w,
												 node2_coord[2]+y_vec[2]*h-z_vec[2]*w ], node2_color]
										v_11[0] = rotatePointAboutAxis(v_11[0],node1_coord,[node1_coord[0]+1,node1_coord[1],node1_coord[2]],node1_rotation[0])
										v_11[0] = rotatePointAboutAxis(v_11[0],node1_coord,[node1_coord[0],node1_coord[1]+1,node1_coord[2]],node1_rotation[1])
										v_11[0] = rotatePointAboutAxis(v_11[0],node1_coord,[node1_coord[0],node1_coord[1],node1_coord[2]+1],node1_rotation[2])
										v_12[0] = rotatePointAboutAxis(v_12[0],node1_coord,[node1_coord[0]+1,node1_coord[1],node1_coord[2]],node1_rotation[0])
										v_12[0] = rotatePointAboutAxis(v_12[0],node1_coord,[node1_coord[0],node1_coord[1]+1,node1_coord[2]],node1_rotation[1])
										v_12[0] = rotatePointAboutAxis(v_12[0],node1_coord,[node1_coord[0],node1_coord[1],node1_coord[2]+1],node1_rotation[2])
										v_13[0] = rotatePointAboutAxis(v_13[0],node1_coord,[node1_coord[0]+1,node1_coord[1],node1_coord[2]],node1_rotation[0])
										v_13[0] = rotatePointAboutAxis(v_13[0],node1_coord,[node1_coord[0],node1_coord[1]+1,node1_coord[2]],node1_rotation[1])
										v_13[0] = rotatePointAboutAxis(v_13[0],node1_coord,[node1_coord[0],node1_coord[1],node1_coord[2]+1],node1_rotation[2])
										v_14[0] = rotatePointAboutAxis(v_14[0],node1_coord,[node1_coord[0]+1,node1_coord[1],node1_coord[2]],node1_rotation[0])
										v_14[0] = rotatePointAboutAxis(v_14[0],node1_coord,[node1_coord[0],node1_coord[1]+1,node1_coord[2]],node1_rotation[1])
										v_14[0] = rotatePointAboutAxis(v_14[0],node1_coord,[node1_coord[0],node1_coord[1],node1_coord[2]+1],node1_rotation[2])
										v_21[0] = rotatePointAboutAxis(v_21[0],node2_coord,[node2_coord[0]+1,node2_coord[1],node2_coord[2]],node2_rotation[0])
										v_21[0] = rotatePointAboutAxis(v_21[0],node2_coord,[node2_coord[0],node2_coord[1]+1,node2_coord[2]],node2_rotation[1])
										v_21[0] = rotatePointAboutAxis(v_21[0],node2_coord,[node2_coord[0],node2_coord[1],node2_coord[2]+1],node2_rotation[2])
										v_22[0] = rotatePointAboutAxis(v_22[0],node2_coord,[node2_coord[0]+1,node2_coord[1],node2_coord[2]],node2_rotation[0])
										v_22[0] = rotatePointAboutAxis(v_22[0],node2_coord,[node2_coord[0],node2_coord[1]+1,node2_coord[2]],node2_rotation[1])
										v_22[0] = rotatePointAboutAxis(v_22[0],node2_coord,[node2_coord[0],node2_coord[1],node2_coord[2]+1],node2_rotation[2])
										v_23[0] = rotatePointAboutAxis(v_23[0],node2_coord,[node2_coord[0]+1,node2_coord[1],node2_coord[2]],node2_rotation[0])
										v_23[0] = rotatePointAboutAxis(v_23[0],node2_coord,[node2_coord[0],node2_coord[1]+1,node2_coord[2]],node2_rotation[1])
										v_23[0] = rotatePointAboutAxis(v_23[0],node2_coord,[node2_coord[0],node2_coord[1],node2_coord[2]+1],node2_rotation[2])
										v_24[0] = rotatePointAboutAxis(v_24[0],node2_coord,[node2_coord[0]+1,node2_coord[1],node2_coord[2]],node2_rotation[0])
										v_24[0] = rotatePointAboutAxis(v_24[0],node2_coord,[node2_coord[0],node2_coord[1]+1,node2_coord[2]],node2_rotation[1])
										v_24[0] = rotatePointAboutAxis(v_24[0],node2_coord,[node2_coord[0],node2_coord[1],node2_coord[2]+1],node2_rotation[2])
										if iw != 0. or ih != 0.:
											v_15 = [[node1_coord[0]-y_vec[0]*ih-z_vec[0]*iw,
													 node1_coord[1]-y_vec[1]*ih-z_vec[1]*iw,
													 node1_coord[2]-y_vec[2]*ih-z_vec[2]*iw ], node1_color]
											v_16 = [[node1_coord[0]-y_vec[0]*ih+z_vec[0]*iw,
													 node1_coord[1]-y_vec[1]*ih+z_vec[1]*iw,
													 node1_coord[2]-y_vec[2]*ih+z_vec[2]*iw ], node1_color]
											v_17 = [[node1_coord[0]+y_vec[0]*ih+z_vec[0]*iw,
													 node1_coord[1]+y_vec[1]*ih+z_vec[1]*iw,
													 node1_coord[2]+y_vec[2]*ih+z_vec[2]*iw ], node1_color]
											v_18 = [[node1_coord[0]+y_vec[0]*ih-z_vec[0]*iw,
													 node1_coord[1]+y_vec[1]*ih-z_vec[1]*iw,
													 node1_coord[2]+y_vec[2]*ih-z_vec[2]*iw ], node1_color]
											v_25 = [[node2_coord[0]-y_vec[0]*ih-z_vec[0]*iw,
													 node2_coord[1]-y_vec[1]*ih-z_vec[1]*iw,
													 node2_coord[2]-y_vec[2]*ih-z_vec[2]*iw ], node2_color]
											v_26 = [[node2_coord[0]-y_vec[0]*ih+z_vec[0]*iw,
													 node2_coord[1]-y_vec[1]*ih+z_vec[1]*iw,
													 node2_coord[2]-y_vec[2]*ih+z_vec[2]*iw ], node2_color]
											v_27 = [[node2_coord[0]+y_vec[0]*ih+z_vec[0]*iw,
													 node2_coord[1]+y_vec[1]*ih+z_vec[1]*iw,
													 node2_coord[2]+y_vec[2]*ih+z_vec[2]*iw ], node2_color]
											v_28 = [[node2_coord[0]+y_vec[0]*ih-z_vec[0]*iw,
													 node2_coord[1]+y_vec[1]*ih-z_vec[1]*iw,
													 node2_coord[2]+y_vec[2]*ih-z_vec[2]*iw ], node2_color]
											v_15[0] = rotatePointAboutAxis(v_15[0],node1_coord,[node1_coord[0]+1,node1_coord[1],node1_coord[2]],node1_rotation[0])
											v_15[0] = rotatePointAboutAxis(v_15[0],node1_coord,[node1_coord[0],node1_coord[1]+1,node1_coord[2]],node1_rotation[1])
											v_15[0] = rotatePointAboutAxis(v_15[0],node1_coord,[node1_coord[0],node1_coord[1],node1_coord[2]+1],node1_rotation[2])
											v_16[0] = rotatePointAboutAxis(v_16[0],node1_coord,[node1_coord[0]+1,node1_coord[1],node1_coord[2]],node1_rotation[0])
											v_16[0] = rotatePointAboutAxis(v_16[0],node1_coord,[node1_coord[0],node1_coord[1]+1,node1_coord[2]],node1_rotation[1])
											v_16[0] = rotatePointAboutAxis(v_16[0],node1_coord,[node1_coord[0],node1_coord[1],node1_coord[2]+1],node1_rotation[2])
											v_17[0] = rotatePointAboutAxis(v_17[0],node1_coord,[node1_coord[0]+1,node1_coord[1],node1_coord[2]],node1_rotation[0])
											v_17[0] = rotatePointAboutAxis(v_17[0],node1_coord,[node1_coord[0],node1_coord[1]+1,node1_coord[2]],node1_rotation[1])
											v_17[0] = rotatePointAboutAxis(v_17[0],node1_coord,[node1_coord[0],node1_coord[1],node1_coord[2]+1],node1_rotation[2])
											v_18[0] = rotatePointAboutAxis(v_18[0],node1_coord,[node1_coord[0]+1,node1_coord[1],node1_coord[2]],node1_rotation[0])
											v_18[0] = rotatePointAboutAxis(v_18[0],node1_coord,[node1_coord[0],node1_coord[1]+1,node1_coord[2]],node1_rotation[1])
											v_18[0] = rotatePointAboutAxis(v_18[0],node1_coord,[node1_coord[0],node1_coord[1],node1_coord[2]+1],node1_rotation[2])
											v_25[0] = rotatePointAboutAxis(v_25[0],node2_coord,[node2_coord[0]+1,node2_coord[1],node2_coord[2]],node2_rotation[0])
											v_25[0] = rotatePointAboutAxis(v_25[0],node2_coord,[node2_coord[0],node2_coord[1]+1,node2_coord[2]],node2_rotation[1])
											v_25[0] = rotatePointAboutAxis(v_25[0],node2_coord,[node2_coord[0],node2_coord[1],node2_coord[2]+1],node2_rotation[2])
											v_26[0] = rotatePointAboutAxis(v_26[0],node2_coord,[node2_coord[0]+1,node2_coord[1],node2_coord[2]],node2_rotation[0])
											v_26[0] = rotatePointAboutAxis(v_26[0],node2_coord,[node2_coord[0],node2_coord[1]+1,node2_coord[2]],node2_rotation[1])
											v_26[0] = rotatePointAboutAxis(v_26[0],node2_coord,[node2_coord[0],node2_coord[1],node2_coord[2]+1],node2_rotation[2])
											v_27[0] = rotatePointAboutAxis(v_27[0],node2_coord,[node2_coord[0]+1,node2_coord[1],node2_coord[2]],node2_rotation[0])
											v_27[0] = rotatePointAboutAxis(v_27[0],node2_coord,[node2_coord[0],node2_coord[1]+1,node2_coord[2]],node2_rotation[1])
											v_27[0] = rotatePointAboutAxis(v_27[0],node2_coord,[node2_coord[0],node2_coord[1],node2_coord[2]+1],node2_rotation[2])
											v_28[0] = rotatePointAboutAxis(v_28[0],node2_coord,[node2_coord[0]+1,node2_coord[1],node2_coord[2]],node2_rotation[0])
											v_28[0] = rotatePointAboutAxis(v_28[0],node2_coord,[node2_coord[0],node2_coord[1]+1,node2_coord[2]],node2_rotation[1])
											v_28[0] = rotatePointAboutAxis(v_28[0],node2_coord,[node2_coord[0],node2_coord[1],node2_coord[2]+1],node2_rotation[2])

										lines = [[v_11,v_12],[v_12,v_13],[v_13,v_14],[v_14,v_11],
												 [v_21,v_22],[v_22,v_23],[v_23,v_24],[v_24,v_21],
												 [v_11,v_21],[v_12,v_22],[v_13,v_23],[v_14,v_24]]
										faces = [[v_13,v_12,v_22],[v_22,v_23,v_13],
												 [v_14,v_13,v_23],[v_23,v_24,v_14],
												 [v_11,v_14,v_24],[v_24,v_21,v_11],
												 [v_12,v_11,v_21],[v_21,v_22,v_12]]

										if iw == 0. or ih == 0.:
											faces += [[v_11,v_12,v_13],[v_13,v_14,v_11],
													  [v_21,v_24,v_23],[v_23,v_22,v_21]]
										else:
											lines += [[v_15,v_16],[v_16,v_17],[v_17,v_18],[v_18,v_15],
													  [v_25,v_26],[v_26,v_27],[v_27,v_28],[v_28,v_25],
													  [v_15,v_25],[v_16,v_26],[v_17,v_27],[v_18,v_28]]
											faces += [[v_15,v_11,v_12],[v_12,v_16,v_15],
													  [v_16,v_12,v_13],[v_13,v_17,v_16],
													  [v_17,v_13,v_14],[v_14,v_18,v_17],
													  [v_18,v_14,v_11],[v_11,v_15,v_18],
													  [v_26,v_22,v_21],[v_21,v_25,v_26],
													  [v_22,v_26,v_23],[v_26,v_27,v_23],
													  [v_23,v_27,v_24],[v_27,v_28,v_24],
													  [v_24,v_28,v_21],[v_25,v_21,v_28],
													  [v_17,v_27,v_16],[v_27,v_26,v_16],
													  [v_18,v_28,v_17],[v_28,v_27,v_17],
													  [v_15,v_25,v_18],[v_25,v_28,v_18],
													  [v_25,v_15,v_26],[v_15,v_16,v_26]]

									elif elements[j].crossSection['Type'] == 'Circle':

										r  = elements[j].crossSection['radius, r']
										ir  = elements[j].crossSection['inner radius, ir']
										vertices1 = []
										vertices2 = []
										pnts = 24
										for v in range(pnts):
											d = pnts/(v+1)
											vc = np.cos(2*np.pi/d)
											vs = np.sin(2*np.pi/d)
											vertices1.append([[node1_coord[0]+vs*y_vec[0]*r+vc*z_vec[0]*r,
															   node1_coord[1]+vs*y_vec[1]*r+vc*z_vec[1]*r,
															   node1_coord[2]+vs*y_vec[2]*r+vc*z_vec[2]*r ], node1_color])
											vertices1[v][0] = rotatePointAboutAxis(vertices1[v][0],node1_coord, \
																[node1_coord[0]+1,node1_coord[1],node1_coord[2]],node1_rotation[0])
											vertices1[v][0] = rotatePointAboutAxis(vertices1[v][0],node1_coord, \
																[node1_coord[0],node1_coord[1]+1,node1_coord[2]],node1_rotation[1])
											vertices1[v][0] = rotatePointAboutAxis(vertices1[v][0],node1_coord, \
																[node1_coord[0],node1_coord[1],node1_coord[2]+1],node1_rotation[2])
											vertices2.append([[node2_coord[0]+vs*y_vec[0]*r+vc*z_vec[0]*r,
															   node2_coord[1]+vs*y_vec[1]*r+vc*z_vec[1]*r,
															   node2_coord[2]+vs*y_vec[2]*r+vc*z_vec[2]*r ], node2_color])
											vertices2[v][0] = rotatePointAboutAxis(vertices2[v][0],node2_coord, \
																[node2_coord[0]+1,node2_coord[1],node2_coord[2]],node2_rotation[0])
											vertices2[v][0] = rotatePointAboutAxis(vertices2[v][0],node2_coord, \
																[node2_coord[0],node2_coord[1]+1,node2_coord[2]],node2_rotation[1])
											vertices2[v][0] = rotatePointAboutAxis(vertices2[v][0],node2_coord, \
																[node2_coord[0],node2_coord[1],node2_coord[2]+1],node2_rotation[2])
										if ir != 0.:
											ivertices1 = []
											ivertices2 = []
											for v in range(pnts):
												d = pnts/(v+1)
												vc = np.cos(2*np.pi/d)
												vs = np.sin(2*np.pi/d)
												ivertices1.append([[node1_coord[0]+vs*y_vec[0]*ir+vc*z_vec[0]*ir,
																    node1_coord[1]+vs*y_vec[1]*ir+vc*z_vec[1]*ir,
																    node1_coord[2]+vs*y_vec[2]*ir+vc*z_vec[2]*ir ], node1_color])
												ivertices1[v][0] = rotatePointAboutAxis(ivertices1[v][0],node1_coord, \
																[node1_coord[0]+1,node1_coord[1],node1_coord[2]],node1_rotation[0])
												ivertices1[v][0] = rotatePointAboutAxis(ivertices1[v][0],node1_coord, \
																[node1_coord[0],node1_coord[1]+1,node1_coord[2]],node1_rotation[1])
												ivertices1[v][0] = rotatePointAboutAxis(ivertices1[v][0],node1_coord, \
																[node1_coord[0],node1_coord[1],node1_coord[2]+1],node1_rotation[2])
												ivertices2.append([[node2_coord[0]+vs*y_vec[0]*ir+vc*z_vec[0]*ir,
																    node2_coord[1]+vs*y_vec[1]*ir+vc*z_vec[1]*ir,
																    node2_coord[2]+vs*y_vec[2]*ir+vc*z_vec[2]*ir ], node2_color])
												ivertices2[v][0] = rotatePointAboutAxis(ivertices2[v][0],node2_coord, \
																[node2_coord[0]+1,node2_coord[1],node2_coord[2]],node2_rotation[0])
												ivertices2[v][0] = rotatePointAboutAxis(ivertices2[v][0],node2_coord, \
																[node2_coord[0],node2_coord[1]+1,node2_coord[2]],node2_rotation[1])
												ivertices2[v][0] = rotatePointAboutAxis(ivertices2[v][0],node2_coord, \
																[node2_coord[0],node2_coord[1],node2_coord[2]+1],node2_rotation[2])

										lines = []
										faces = []
										for v in range(pnts):
											lines.append([vertices1[v-1],vertices1[v]])
											lines.append([vertices2[v-1],vertices2[v]])
										lines.append([vertices1[0],vertices2[0]])

										if ir != 0.:
											for v in range(pnts):
												lines.append([ivertices1[v-1],ivertices1[v]])
												lines.append([ivertices2[v-1],ivertices2[v]])
											lines.append([ivertices1[0],ivertices2[0]])
											for v in range(pnts-1):
												faces.append([ivertices1[v],vertices1[v],vertices1[v+1]])
												faces.append([vertices1[v+1],ivertices1[v+1],ivertices1[v]])
												faces.append([ivertices2[v],vertices2[v+1],vertices2[v]])
												faces.append([vertices2[v+1],ivertices2[v],ivertices2[v+1]])
												faces.append([vertices1[v],vertices2[v],vertices2[v+1]])
												faces.append([vertices2[v+1],vertices1[v+1],vertices1[v]])
												faces.append([ivertices1[v],ivertices1[v+1],ivertices2[v]])
												faces.append([ivertices1[v+1],ivertices2[v+1],ivertices2[v]])
											faces.append([ivertices1[-1],vertices1[-1],vertices1[0]])
											faces.append([vertices1[0],ivertices1[0],ivertices1[-1]])
											faces.append([ivertices2[-1],vertices2[0],vertices2[-1]])
											faces.append([vertices2[0],ivertices2[-1],ivertices2[0]])
											faces.append([vertices1[-1],vertices2[-1],vertices2[0]])
											faces.append([vertices2[0],vertices1[0],vertices1[-1]])
											faces.append([ivertices1[-1],ivertices1[0],ivertices2[-1]])
											faces.append([ivertices1[0],ivertices2[0],ivertices2[-1]])
													
										else:
											vertices1.append([[node1_coord[0],
															   node1_coord[1],
															   node1_coord[2] ], node1_color])
											vertices1[-1][0] = rotatePointAboutAxis(vertices1[-1][0],node1_coord, \
																[node1_coord[0]+1,node1_coord[1],node1_coord[2]],node1_rotation[0])
											vertices1[-1][0] = rotatePointAboutAxis(vertices1[-1][0],node1_coord, \
																[node1_coord[0],node1_coord[1]+1,node1_coord[2]],node1_rotation[1])
											vertices1[-1][0] = rotatePointAboutAxis(vertices1[-1][0],node1_coord, \
																[node1_coord[0],node1_coord[1],node1_coord[2]+1],node1_rotation[2])
											vertices2.append([[node2_coord[0],
															   node2_coord[1],
															   node2_coord[2] ], node2_color])
											vertices2[-1][0] = rotatePointAboutAxis(vertices2[-1][0],node2_coord, \
																[node2_coord[0]+1,node2_coord[1],node2_coord[2]],node2_rotation[0])
											vertices2[-1][0] = rotatePointAboutAxis(vertices2[-1][0],node2_coord, \
																[node2_coord[0],node2_coord[1]+1,node2_coord[2]],node2_rotation[1])
											vertices2[-1][0] = rotatePointAboutAxis(vertices2[-1][0],node2_coord, \
																[node2_coord[0],node2_coord[1],node2_coord[2]+1],node2_rotation[2])
											for v in range(pnts):
												faces.append([vertices1[-1],vertices1[v],vertices1[v+1]])
												faces.append([vertices2[-1],vertices2[v+1],vertices2[v]])
												faces.append([vertices1[v],vertices2[v],vertices2[v+1]])
												faces.append([vertices2[v+1],vertices1[v+1],vertices1[v]])
											faces.append([vertices1[-1],vertices1[-2],vertices1[0]])
											faces.append([vertices2[-1],vertices2[0],vertices2[-2]])
											faces.append([vertices1[-2],vertices2[-2],vertices2[0]])
											faces.append([vertices2[0],vertices1[0],vertices1[-2]])

									elif elements[j].crossSection['Type'] == 'L-Beam':

										bw = elements[j].crossSection['bottom width, bw']
										bt = elements[j].crossSection['bottom thickness, bt']
										st = elements[j].crossSection['side thickness, st']
										h  = elements[j].crossSection['height, h']
										A1  = st*(h-bt)
										A2  = bt*bw
										A   = A1+A2
										yC1 = (h/2.)+bt
										yC2 = bt/2.
										zC1 = st/2.
										zC2 = bw/2.
										if A != 0.:
											yC = (A1*yC1+A2*yC2)/A
											zC = (A1*zC1+A2*zC2)/A
										else:
											yC = 0.
											zC = 0.
										v_11  = [[node1_coord[0]-y_vec[0]*yC-z_vec[0]*zC,
												  node1_coord[1]-y_vec[1]*yC-z_vec[1]*zC,
												  node1_coord[2]-y_vec[2]*yC-z_vec[2]*zC ], node1_color]
										v_12  = [[node1_coord[0]-y_vec[0]*yC+z_vec[0]*(bw-zC),
												  node1_coord[1]-y_vec[1]*yC+z_vec[1]*(bw-zC),
												  node1_coord[2]-y_vec[2]*yC+z_vec[2]*(bw-zC) ], node1_color]
										v_13  = [[node1_coord[0]-y_vec[0]*(yC-bt)+z_vec[0]*(bw-zC),
												  node1_coord[1]-y_vec[1]*(yC-bt)+z_vec[1]*(bw-zC),
												  node1_coord[2]-y_vec[2]*(yC-bt)+z_vec[2]*(bw-zC) ], node1_color]
										v_14  = [[node1_coord[0]-y_vec[0]*(yC-bt)-z_vec[0]*(zC-st),
												  node1_coord[1]-y_vec[1]*(yC-bt)-z_vec[1]*(zC-st),
												  node1_coord[2]-y_vec[2]*(yC-bt)-z_vec[2]*(zC-st) ], node1_color]
										v_15  = [[node1_coord[0]+y_vec[0]*(h-yC)-z_vec[0]*(zC-st),
												  node1_coord[1]+y_vec[1]*(h-yC)-z_vec[1]*(zC-st),
												  node1_coord[2]+y_vec[2]*(h-yC)-z_vec[2]*(zC-st) ], node1_color]
										v_16  = [[node1_coord[0]+y_vec[0]*(h-yC)-z_vec[0]*zC,
												  node1_coord[1]+y_vec[1]*(h-yC)-z_vec[1]*zC,
												  node1_coord[2]+y_vec[2]*(h-yC)-z_vec[2]*zC ], node1_color]
										v_21  = [[node2_coord[0]-y_vec[0]*yC-z_vec[0]*zC,
												  node2_coord[1]-y_vec[1]*yC-z_vec[1]*zC,
												  node2_coord[2]-y_vec[2]*yC-z_vec[2]*zC ], node2_color]
										v_22  = [[node2_coord[0]-y_vec[0]*yC+z_vec[0]*(bw-zC),
												  node2_coord[1]-y_vec[1]*yC+z_vec[1]*(bw-zC),
												  node2_coord[2]-y_vec[2]*yC+z_vec[2]*(bw-zC) ], node2_color]
										v_23  = [[node2_coord[0]-y_vec[0]*(yC-bt)+z_vec[0]*(bw-zC),
												  node2_coord[1]-y_vec[1]*(yC-bt)+z_vec[1]*(bw-zC),
												  node2_coord[2]-y_vec[2]*(yC-bt)+z_vec[2]*(bw-zC) ], node2_color]
										v_24  = [[node2_coord[0]-y_vec[0]*(yC-bt)-z_vec[0]*(zC-st),
												  node2_coord[1]-y_vec[1]*(yC-bt)-z_vec[1]*(zC-st),
												  node2_coord[2]-y_vec[2]*(yC-bt)-z_vec[2]*(zC-st) ], node2_color]
										v_25  = [[node2_coord[0]+y_vec[0]*(h-yC)-z_vec[0]*(zC-st),
												  node2_coord[1]+y_vec[1]*(h-yC)-z_vec[1]*(zC-st),
												  node2_coord[2]+y_vec[2]*(h-yC)-z_vec[2]*(zC-st) ], node2_color]
										v_26  = [[node2_coord[0]+y_vec[0]*(h-yC)-z_vec[0]*zC,
												  node2_coord[1]+y_vec[1]*(h-yC)-z_vec[1]*zC,
												  node2_coord[2]+y_vec[2]*(h-yC)-z_vec[2]*zC ], node2_color]
										v_11[0] = rotatePointAboutAxis(v_11[0],node1_coord,[node1_coord[0]+1,node1_coord[1],node1_coord[2]],node1_rotation[0])
										v_11[0] = rotatePointAboutAxis(v_11[0],node1_coord,[node1_coord[0],node1_coord[1]+1,node1_coord[2]],node1_rotation[1])
										v_11[0] = rotatePointAboutAxis(v_11[0],node1_coord,[node1_coord[0],node1_coord[1],node1_coord[2]+1],node1_rotation[2])
										v_12[0] = rotatePointAboutAxis(v_12[0],node1_coord,[node1_coord[0]+1,node1_coord[1],node1_coord[2]],node1_rotation[0])
										v_12[0] = rotatePointAboutAxis(v_12[0],node1_coord,[node1_coord[0],node1_coord[1]+1,node1_coord[2]],node1_rotation[1])
										v_12[0] = rotatePointAboutAxis(v_12[0],node1_coord,[node1_coord[0],node1_coord[1],node1_coord[2]+1],node1_rotation[2])
										v_13[0] = rotatePointAboutAxis(v_13[0],node1_coord,[node1_coord[0]+1,node1_coord[1],node1_coord[2]],node1_rotation[0])
										v_13[0] = rotatePointAboutAxis(v_13[0],node1_coord,[node1_coord[0],node1_coord[1]+1,node1_coord[2]],node1_rotation[1])
										v_13[0] = rotatePointAboutAxis(v_13[0],node1_coord,[node1_coord[0],node1_coord[1],node1_coord[2]+1],node1_rotation[2])
										v_14[0] = rotatePointAboutAxis(v_14[0],node1_coord,[node1_coord[0]+1,node1_coord[1],node1_coord[2]],node1_rotation[0])
										v_14[0] = rotatePointAboutAxis(v_14[0],node1_coord,[node1_coord[0],node1_coord[1]+1,node1_coord[2]],node1_rotation[1])
										v_14[0] = rotatePointAboutAxis(v_14[0],node1_coord,[node1_coord[0],node1_coord[1],node1_coord[2]+1],node1_rotation[2])
										v_15[0] = rotatePointAboutAxis(v_15[0],node1_coord,[node1_coord[0]+1,node1_coord[1],node1_coord[2]],node1_rotation[0])
										v_15[0] = rotatePointAboutAxis(v_15[0],node1_coord,[node1_coord[0],node1_coord[1]+1,node1_coord[2]],node1_rotation[1])
										v_15[0] = rotatePointAboutAxis(v_15[0],node1_coord,[node1_coord[0],node1_coord[1],node1_coord[2]+1],node1_rotation[2])
										v_16[0] = rotatePointAboutAxis(v_16[0],node1_coord,[node1_coord[0]+1,node1_coord[1],node1_coord[2]],node1_rotation[0])
										v_16[0] = rotatePointAboutAxis(v_16[0],node1_coord,[node1_coord[0],node1_coord[1]+1,node1_coord[2]],node1_rotation[1])
										v_16[0] = rotatePointAboutAxis(v_16[0],node1_coord,[node1_coord[0],node1_coord[1],node1_coord[2]+1],node1_rotation[2])
										v_21[0] = rotatePointAboutAxis(v_21[0],node2_coord,[node2_coord[0]+1,node2_coord[1],node2_coord[2]],node2_rotation[0])
										v_21[0] = rotatePointAboutAxis(v_21[0],node2_coord,[node2_coord[0],node2_coord[1]+1,node2_coord[2]],node2_rotation[1])
										v_21[0] = rotatePointAboutAxis(v_21[0],node2_coord,[node2_coord[0],node2_coord[1],node2_coord[2]+1],node2_rotation[2])
										v_22[0] = rotatePointAboutAxis(v_22[0],node2_coord,[node2_coord[0]+1,node2_coord[1],node2_coord[2]],node2_rotation[0])
										v_22[0] = rotatePointAboutAxis(v_22[0],node2_coord,[node2_coord[0],node2_coord[1]+1,node2_coord[2]],node2_rotation[1])
										v_22[0] = rotatePointAboutAxis(v_22[0],node2_coord,[node2_coord[0],node2_coord[1],node2_coord[2]+1],node2_rotation[2])
										v_23[0] = rotatePointAboutAxis(v_23[0],node2_coord,[node2_coord[0]+1,node2_coord[1],node2_coord[2]],node2_rotation[0])
										v_23[0] = rotatePointAboutAxis(v_23[0],node2_coord,[node2_coord[0],node2_coord[1]+1,node2_coord[2]],node2_rotation[1])
										v_23[0] = rotatePointAboutAxis(v_23[0],node2_coord,[node2_coord[0],node2_coord[1],node2_coord[2]+1],node2_rotation[2])
										v_24[0] = rotatePointAboutAxis(v_24[0],node2_coord,[node2_coord[0]+1,node2_coord[1],node2_coord[2]],node2_rotation[0])
										v_24[0] = rotatePointAboutAxis(v_24[0],node2_coord,[node2_coord[0],node2_coord[1]+1,node2_coord[2]],node2_rotation[1])
										v_24[0] = rotatePointAboutAxis(v_24[0],node2_coord,[node2_coord[0],node2_coord[1],node2_coord[2]+1],node2_rotation[2])
										v_25[0] = rotatePointAboutAxis(v_25[0],node2_coord,[node2_coord[0]+1,node2_coord[1],node2_coord[2]],node2_rotation[0])
										v_25[0] = rotatePointAboutAxis(v_25[0],node2_coord,[node2_coord[0],node2_coord[1]+1,node2_coord[2]],node2_rotation[1])
										v_25[0] = rotatePointAboutAxis(v_25[0],node2_coord,[node2_coord[0],node2_coord[1],node2_coord[2]+1],node2_rotation[2])
										v_26[0] = rotatePointAboutAxis(v_26[0],node2_coord,[node2_coord[0]+1,node2_coord[1],node2_coord[2]],node2_rotation[0])
										v_26[0] = rotatePointAboutAxis(v_26[0],node2_coord,[node2_coord[0],node2_coord[1]+1,node2_coord[2]],node2_rotation[1])
										v_26[0] = rotatePointAboutAxis(v_26[0],node2_coord,[node2_coord[0],node2_coord[1],node2_coord[2]+1],node2_rotation[2])

										lines = [[v_11,v_12],[v_12,v_13],[v_13,v_14],[v_14,v_15],[v_15,v_16],[v_16,v_11],
												 [v_21,v_22],[v_22,v_23],[v_23,v_24],[v_24,v_25],[v_25,v_26],[v_26,v_21],
												 [v_11,v_21],[v_12,v_22],[v_13,v_23],[v_14,v_24],[v_15,v_25],[v_16,v_26]]
										faces = [[v_11,v_12,v_13],[v_13,v_14,v_11],
												 [v_11,v_14,v_16],[v_16,v_14,v_15],
												 [v_23,v_22,v_21],[v_21,v_24,v_23],
												 [v_24,v_21,v_26],[v_24,v_26,v_25],
												 [v_11,v_21,v_12],[v_12,v_21,v_22],
												 [v_11,v_16,v_26],[v_26,v_21,v_11],
												 [v_16,v_15,v_26],[v_26,v_15,v_25],
												 [v_13,v_12,v_22],[v_22,v_23,v_13],
												 [v_14,v_13,v_24],[v_24,v_13,v_23],
												 [v_14,v_24,v_25],[v_25,v_15,v_14]]

									elif elements[j].crossSection['Type'] == 'I-Beam':
										tw = elements[j].crossSection['top width, tw']
										tt = elements[j].crossSection['top thickness, tt']
										mt = elements[j].crossSection['middle thickness, mt']
										bw = elements[j].crossSection['bottom width, bw']
										bt = elements[j].crossSection['bottom thickness, bt']
										h  = elements[j].crossSection['height, h']
										tw = tw/2.
										tt = tt
										mt = mt/2.
										bw = bw/2.
										bt = bt
										h  = h/2.
										v_11  = [[node1_coord[0]-y_vec[0]*h-z_vec[0]*bw,
												  node1_coord[1]-y_vec[1]*h-z_vec[1]*bw,
												  node1_coord[2]-y_vec[2]*h-z_vec[2]*bw ], node1_color]
										v_12  = [[node1_coord[0]-y_vec[0]*h+z_vec[0]*bw,
												  node1_coord[1]-y_vec[1]*h+z_vec[1]*bw,
												  node1_coord[2]-y_vec[2]*h+z_vec[2]*bw ], node1_color]
										v_13  = [[node1_coord[0]-y_vec[0]*(h-bt)+z_vec[0]*bw,
												  node1_coord[1]-y_vec[1]*(h-bt)+z_vec[1]*bw,
												  node1_coord[2]-y_vec[2]*(h-bt)+z_vec[2]*bw ], node1_color]
										v_14  = [[node1_coord[0]-y_vec[0]*(h-bt)+z_vec[0]*mt,
												  node1_coord[1]-y_vec[1]*(h-bt)+z_vec[1]*mt,
												  node1_coord[2]-y_vec[2]*(h-bt)+z_vec[2]*mt ], node1_color]
										v_15  = [[node1_coord[0]-y_vec[0]*(h-bt)-z_vec[0]*mt,
												  node1_coord[1]-y_vec[1]*(h-bt)-z_vec[1]*mt,
												  node1_coord[2]-y_vec[2]*(h-bt)-z_vec[2]*mt ], node1_color]
										v_16  = [[node1_coord[0]-y_vec[0]*(h-bt)-z_vec[0]*bw,
												  node1_coord[1]-y_vec[1]*(h-bt)-z_vec[1]*bw,
												  node1_coord[2]-y_vec[2]*(h-bt)-z_vec[2]*bw ], node1_color]
										v_17  = [[node1_coord[0]+y_vec[0]*(h-tt)-z_vec[0]*tw,
												  node1_coord[1]+y_vec[1]*(h-tt)-z_vec[1]*tw,
												  node1_coord[2]+y_vec[2]*(h-tt)-z_vec[2]*tw ], node1_color]
										v_18  = [[node1_coord[0]+y_vec[0]*(h-tt)-z_vec[0]*mt,
												  node1_coord[1]+y_vec[1]*(h-tt)-z_vec[1]*mt,
												  node1_coord[2]+y_vec[2]*(h-tt)-z_vec[2]*mt ], node1_color]
										v_19  = [[node1_coord[0]+y_vec[0]*(h-tt)+z_vec[0]*mt,
												  node1_coord[1]+y_vec[1]*(h-tt)+z_vec[1]*mt,
												  node1_coord[2]+y_vec[2]*(h-tt)+z_vec[2]*mt ], node1_color]
										v_110 = [[node1_coord[0]+y_vec[0]*(h-tt)+z_vec[0]*tw,
												  node1_coord[1]+y_vec[1]*(h-tt)+z_vec[1]*tw,
												  node1_coord[2]+y_vec[2]*(h-tt)+z_vec[2]*tw ], node1_color]
										v_111 = [[node1_coord[0]+y_vec[0]*h+z_vec[0]*tw,
												  node1_coord[1]+y_vec[1]*h+z_vec[1]*tw,
												  node1_coord[2]+y_vec[2]*h+z_vec[2]*tw ], node1_color]
										v_112 = [[node1_coord[0]+y_vec[0]*h-z_vec[0]*tw,
												  node1_coord[1]+y_vec[1]*h-z_vec[1]*tw,
												  node1_coord[2]+y_vec[2]*h-z_vec[2]*tw ], node1_color]
										v_21  = [[node2_coord[0]-y_vec[0]*h-z_vec[0]*bw,
												  node2_coord[1]-y_vec[1]*h-z_vec[1]*bw,
												  node2_coord[2]-y_vec[2]*h-z_vec[2]*bw ], node2_color]
										v_22  = [[node2_coord[0]-y_vec[0]*h+z_vec[0]*bw,
												  node2_coord[1]-y_vec[1]*h+z_vec[1]*bw,
												  node2_coord[2]-y_vec[2]*h+z_vec[2]*bw ], node2_color]
										v_23  = [[node2_coord[0]-y_vec[0]*(h-bt)+z_vec[0]*bw,
												  node2_coord[1]-y_vec[1]*(h-bt)+z_vec[1]*bw,
												  node2_coord[2]-y_vec[2]*(h-bt)+z_vec[2]*bw ], node2_color]
										v_24  = [[node2_coord[0]-y_vec[0]*(h-bt)+z_vec[0]*mt,
												  node2_coord[1]-y_vec[1]*(h-bt)+z_vec[1]*mt,
												  node2_coord[2]-y_vec[2]*(h-bt)+z_vec[2]*mt ], node2_color]
										v_25  = [[node2_coord[0]-y_vec[0]*(h-bt)-z_vec[0]*mt,
												  node2_coord[1]-y_vec[1]*(h-bt)-z_vec[1]*mt,
												  node2_coord[2]-y_vec[2]*(h-bt)-z_vec[2]*mt ], node2_color]
										v_26  = [[node2_coord[0]-y_vec[0]*(h-bt)-z_vec[0]*bw,
												  node2_coord[1]-y_vec[1]*(h-bt)-z_vec[1]*bw,
												  node2_coord[2]-y_vec[2]*(h-bt)-z_vec[2]*bw ], node2_color]
										v_27  = [[node2_coord[0]+y_vec[0]*(h-tt)-z_vec[0]*tw,
												  node2_coord[1]+y_vec[1]*(h-tt)-z_vec[1]*tw,
												  node2_coord[2]+y_vec[2]*(h-tt)-z_vec[2]*tw ], node2_color]
										v_28  = [[node2_coord[0]+y_vec[0]*(h-tt)-z_vec[0]*mt,
												  node2_coord[1]+y_vec[1]*(h-tt)-z_vec[1]*mt,
												  node2_coord[2]+y_vec[2]*(h-tt)-z_vec[2]*mt ], node2_color]
										v_29  = [[node2_coord[0]+y_vec[0]*(h-tt)+z_vec[0]*mt,
												  node2_coord[1]+y_vec[1]*(h-tt)+z_vec[1]*mt,
												  node2_coord[2]+y_vec[2]*(h-tt)+z_vec[2]*mt ], node2_color]
										v_210 = [[node2_coord[0]+y_vec[0]*(h-tt)+z_vec[0]*tw,
												  node2_coord[1]+y_vec[1]*(h-tt)+z_vec[1]*tw,
												  node2_coord[2]+y_vec[2]*(h-tt)+z_vec[2]*tw ], node2_color]
										v_211 = [[node2_coord[0]+y_vec[0]*h+z_vec[0]*tw,
												  node2_coord[1]+y_vec[1]*h+z_vec[1]*tw,
												  node2_coord[2]+y_vec[2]*h+z_vec[2]*tw ], node2_color]
										v_212 = [[node2_coord[0]+y_vec[0]*h-z_vec[0]*tw,
												  node2_coord[1]+y_vec[1]*h-z_vec[1]*tw,
												  node2_coord[2]+y_vec[2]*h-z_vec[2]*tw ], node2_color]
										v_11[0] = rotatePointAboutAxis(v_11[0],node1_coord,[node1_coord[0]+1,node1_coord[1],node1_coord[2]],node1_rotation[0])
										v_11[0] = rotatePointAboutAxis(v_11[0],node1_coord,[node1_coord[0],node1_coord[1]+1,node1_coord[2]],node1_rotation[1])
										v_11[0] = rotatePointAboutAxis(v_11[0],node1_coord,[node1_coord[0],node1_coord[1],node1_coord[2]+1],node1_rotation[2])
										v_12[0] = rotatePointAboutAxis(v_12[0],node1_coord,[node1_coord[0]+1,node1_coord[1],node1_coord[2]],node1_rotation[0])
										v_12[0] = rotatePointAboutAxis(v_12[0],node1_coord,[node1_coord[0],node1_coord[1]+1,node1_coord[2]],node1_rotation[1])
										v_12[0] = rotatePointAboutAxis(v_12[0],node1_coord,[node1_coord[0],node1_coord[1],node1_coord[2]+1],node1_rotation[2])
										v_13[0] = rotatePointAboutAxis(v_13[0],node1_coord,[node1_coord[0]+1,node1_coord[1],node1_coord[2]],node1_rotation[0])
										v_13[0] = rotatePointAboutAxis(v_13[0],node1_coord,[node1_coord[0],node1_coord[1]+1,node1_coord[2]],node1_rotation[1])
										v_13[0] = rotatePointAboutAxis(v_13[0],node1_coord,[node1_coord[0],node1_coord[1],node1_coord[2]+1],node1_rotation[2])
										v_14[0] = rotatePointAboutAxis(v_14[0],node1_coord,[node1_coord[0]+1,node1_coord[1],node1_coord[2]],node1_rotation[0])
										v_14[0] = rotatePointAboutAxis(v_14[0],node1_coord,[node1_coord[0],node1_coord[1]+1,node1_coord[2]],node1_rotation[1])
										v_14[0] = rotatePointAboutAxis(v_14[0],node1_coord,[node1_coord[0],node1_coord[1],node1_coord[2]+1],node1_rotation[2])
										v_15[0] = rotatePointAboutAxis(v_15[0],node1_coord,[node1_coord[0]+1,node1_coord[1],node1_coord[2]],node1_rotation[0])
										v_15[0] = rotatePointAboutAxis(v_15[0],node1_coord,[node1_coord[0],node1_coord[1]+1,node1_coord[2]],node1_rotation[1])
										v_15[0] = rotatePointAboutAxis(v_15[0],node1_coord,[node1_coord[0],node1_coord[1],node1_coord[2]+1],node1_rotation[2])
										v_16[0] = rotatePointAboutAxis(v_16[0],node1_coord,[node1_coord[0]+1,node1_coord[1],node1_coord[2]],node1_rotation[0])
										v_16[0] = rotatePointAboutAxis(v_16[0],node1_coord,[node1_coord[0],node1_coord[1]+1,node1_coord[2]],node1_rotation[1])
										v_16[0] = rotatePointAboutAxis(v_16[0],node1_coord,[node1_coord[0],node1_coord[1],node1_coord[2]+1],node1_rotation[2])
										v_17[0] = rotatePointAboutAxis(v_17[0],node1_coord,[node1_coord[0]+1,node1_coord[1],node1_coord[2]],node1_rotation[0])
										v_17[0] = rotatePointAboutAxis(v_17[0],node1_coord,[node1_coord[0],node1_coord[1]+1,node1_coord[2]],node1_rotation[1])
										v_17[0] = rotatePointAboutAxis(v_17[0],node1_coord,[node1_coord[0],node1_coord[1],node1_coord[2]+1],node1_rotation[2])
										v_18[0] = rotatePointAboutAxis(v_18[0],node1_coord,[node1_coord[0]+1,node1_coord[1],node1_coord[2]],node1_rotation[0])
										v_18[0] = rotatePointAboutAxis(v_18[0],node1_coord,[node1_coord[0],node1_coord[1]+1,node1_coord[2]],node1_rotation[1])
										v_18[0] = rotatePointAboutAxis(v_18[0],node1_coord,[node1_coord[0],node1_coord[1],node1_coord[2]+1],node1_rotation[2])
										v_19[0] = rotatePointAboutAxis(v_19[0],node1_coord,[node1_coord[0]+1,node1_coord[1],node1_coord[2]],node1_rotation[0])
										v_19[0] = rotatePointAboutAxis(v_19[0],node1_coord,[node1_coord[0],node1_coord[1]+1,node1_coord[2]],node1_rotation[1])
										v_19[0] = rotatePointAboutAxis(v_19[0],node1_coord,[node1_coord[0],node1_coord[1],node1_coord[2]+1],node1_rotation[2])
										v_110[0] = rotatePointAboutAxis(v_110[0],node1_coord,[node1_coord[0]+1,node1_coord[1],node1_coord[2]],node1_rotation[0])
										v_110[0] = rotatePointAboutAxis(v_110[0],node1_coord,[node1_coord[0],node1_coord[1]+1,node1_coord[2]],node1_rotation[1])
										v_110[0] = rotatePointAboutAxis(v_110[0],node1_coord,[node1_coord[0],node1_coord[1],node1_coord[2]+1],node1_rotation[2])
										v_111[0] = rotatePointAboutAxis(v_111[0],node1_coord,[node1_coord[0]+1,node1_coord[1],node1_coord[2]],node1_rotation[0])
										v_111[0] = rotatePointAboutAxis(v_111[0],node1_coord,[node1_coord[0],node1_coord[1]+1,node1_coord[2]],node1_rotation[1])
										v_111[0] = rotatePointAboutAxis(v_111[0],node1_coord,[node1_coord[0],node1_coord[1],node1_coord[2]+1],node1_rotation[2])
										v_112[0] = rotatePointAboutAxis(v_112[0],node1_coord,[node1_coord[0]+1,node1_coord[1],node1_coord[2]],node1_rotation[0])
										v_112[0] = rotatePointAboutAxis(v_112[0],node1_coord,[node1_coord[0],node1_coord[1]+1,node1_coord[2]],node1_rotation[1])
										v_112[0] = rotatePointAboutAxis(v_112[0],node1_coord,[node1_coord[0],node1_coord[1],node1_coord[2]+1],node1_rotation[2])
										v_21[0] = rotatePointAboutAxis(v_21[0],node2_coord,[node2_coord[0]+1,node2_coord[1],node2_coord[2]],node2_rotation[0])
										v_21[0] = rotatePointAboutAxis(v_21[0],node2_coord,[node2_coord[0],node2_coord[1]+1,node2_coord[2]],node2_rotation[1])
										v_21[0] = rotatePointAboutAxis(v_21[0],node2_coord,[node2_coord[0],node2_coord[1],node2_coord[2]+1],node2_rotation[2])
										v_22[0] = rotatePointAboutAxis(v_22[0],node2_coord,[node2_coord[0]+1,node2_coord[1],node2_coord[2]],node2_rotation[0])
										v_22[0] = rotatePointAboutAxis(v_22[0],node2_coord,[node2_coord[0],node2_coord[1]+1,node2_coord[2]],node2_rotation[1])
										v_22[0] = rotatePointAboutAxis(v_22[0],node2_coord,[node2_coord[0],node2_coord[1],node2_coord[2]+1],node2_rotation[2])
										v_23[0] = rotatePointAboutAxis(v_23[0],node2_coord,[node2_coord[0]+1,node2_coord[1],node2_coord[2]],node2_rotation[0])
										v_23[0] = rotatePointAboutAxis(v_23[0],node2_coord,[node2_coord[0],node2_coord[1]+1,node2_coord[2]],node2_rotation[1])
										v_23[0] = rotatePointAboutAxis(v_23[0],node2_coord,[node2_coord[0],node2_coord[1],node2_coord[2]+1],node2_rotation[2])
										v_24[0] = rotatePointAboutAxis(v_24[0],node2_coord,[node2_coord[0]+1,node2_coord[1],node2_coord[2]],node2_rotation[0])
										v_24[0] = rotatePointAboutAxis(v_24[0],node2_coord,[node2_coord[0],node2_coord[1]+1,node2_coord[2]],node2_rotation[1])
										v_24[0] = rotatePointAboutAxis(v_24[0],node2_coord,[node2_coord[0],node2_coord[1],node2_coord[2]+1],node2_rotation[2])
										v_25[0] = rotatePointAboutAxis(v_25[0],node2_coord,[node2_coord[0]+1,node2_coord[1],node2_coord[2]],node2_rotation[0])
										v_25[0] = rotatePointAboutAxis(v_25[0],node2_coord,[node2_coord[0],node2_coord[1]+1,node2_coord[2]],node2_rotation[1])
										v_25[0] = rotatePointAboutAxis(v_25[0],node2_coord,[node2_coord[0],node2_coord[1],node2_coord[2]+1],node2_rotation[2])
										v_26[0] = rotatePointAboutAxis(v_26[0],node2_coord,[node2_coord[0]+1,node2_coord[1],node2_coord[2]],node2_rotation[0])
										v_26[0] = rotatePointAboutAxis(v_26[0],node2_coord,[node2_coord[0],node2_coord[1]+1,node2_coord[2]],node2_rotation[1])
										v_26[0] = rotatePointAboutAxis(v_26[0],node2_coord,[node2_coord[0],node2_coord[1],node2_coord[2]+1],node2_rotation[2])
										v_27[0] = rotatePointAboutAxis(v_27[0],node2_coord,[node2_coord[0]+1,node2_coord[1],node2_coord[2]],node2_rotation[0])
										v_27[0] = rotatePointAboutAxis(v_27[0],node2_coord,[node2_coord[0],node2_coord[1]+1,node2_coord[2]],node2_rotation[1])
										v_27[0] = rotatePointAboutAxis(v_27[0],node2_coord,[node2_coord[0],node2_coord[1],node2_coord[2]+1],node2_rotation[2])
										v_28[0] = rotatePointAboutAxis(v_28[0],node2_coord,[node2_coord[0]+1,node2_coord[1],node2_coord[2]],node2_rotation[0])
										v_28[0] = rotatePointAboutAxis(v_28[0],node2_coord,[node2_coord[0],node2_coord[1]+1,node2_coord[2]],node2_rotation[1])
										v_28[0] = rotatePointAboutAxis(v_28[0],node2_coord,[node2_coord[0],node2_coord[1],node2_coord[2]+1],node2_rotation[2])
										v_29[0] = rotatePointAboutAxis(v_29[0],node2_coord,[node2_coord[0]+1,node2_coord[1],node2_coord[2]],node2_rotation[0])
										v_29[0] = rotatePointAboutAxis(v_29[0],node2_coord,[node2_coord[0],node2_coord[1]+1,node2_coord[2]],node2_rotation[1])
										v_29[0] = rotatePointAboutAxis(v_29[0],node2_coord,[node2_coord[0],node2_coord[1],node2_coord[2]+1],node2_rotation[2])
										v_210[0] = rotatePointAboutAxis(v_210[0],node2_coord,[node2_coord[0]+1,node2_coord[1],node2_coord[2]],node2_rotation[0])
										v_210[0] = rotatePointAboutAxis(v_210[0],node2_coord,[node2_coord[0],node2_coord[1]+1,node2_coord[2]],node2_rotation[1])
										v_210[0] = rotatePointAboutAxis(v_210[0],node2_coord,[node2_coord[0],node2_coord[1],node2_coord[2]+1],node2_rotation[2])
										v_211[0] = rotatePointAboutAxis(v_211[0],node2_coord,[node2_coord[0]+1,node2_coord[1],node2_coord[2]],node2_rotation[0])
										v_211[0] = rotatePointAboutAxis(v_211[0],node2_coord,[node2_coord[0],node2_coord[1]+1,node2_coord[2]],node2_rotation[1])
										v_211[0] = rotatePointAboutAxis(v_211[0],node2_coord,[node2_coord[0],node2_coord[1],node2_coord[2]+1],node2_rotation[2])
										v_212[0] = rotatePointAboutAxis(v_212[0],node2_coord,[node2_coord[0]+1,node2_coord[1],node2_coord[2]],node2_rotation[0])
										v_212[0] = rotatePointAboutAxis(v_212[0],node2_coord,[node2_coord[0],node2_coord[1]+1,node2_coord[2]],node2_rotation[1])
										v_212[0] = rotatePointAboutAxis(v_212[0],node2_coord,[node2_coord[0],node2_coord[1],node2_coord[2]+1],node2_rotation[2])

										lines = [[v_11,v_12],[v_12,v_13],[v_13,v_14],[v_14,v_19],
												 [v_19,v_110],[v_110,v_111],[v_111,v_112],[v_112,v_17],
												 [v_17,v_18],[v_18,v_15],[v_15,v_16],[v_16,v_11],
												 [v_21,v_22],[v_22,v_23],[v_23,v_24],[v_24,v_29],
												 [v_29,v_210],[v_210,v_211],[v_211,v_212],[v_212,v_27],
												 [v_27,v_28],[v_28,v_25],[v_25,v_26],[v_26,v_21],
												 [v_11,v_21],[v_12,v_22],[v_13,v_23],[v_14,v_24],
												 [v_15,v_25],[v_16,v_26],[v_17,v_27],[v_18,v_28],
												 [v_19,v_29],[v_110,v_210],[v_111,v_211],[v_112,v_212]]
										faces = [[v_11,v_12,v_13],[v_13,v_16,v_11],
												 [v_15,v_14,v_19],[v_19,v_18,v_15],
												 [v_112,v_17,v_110],[v_110,v_111,v_112],
												 [v_23,v_22,v_21],[v_21,v_26,v_23],
												 [v_29,v_24,v_25],[v_25,v_28,v_29],
												 [v_210,v_27,v_212],[v_212,v_211,v_210],
												 [v_19,v_14,v_24],[v_24,v_29,v_19],
												 [v_15,v_18,v_28],[v_28,v_25,v_15],
												 [v_13,v_12,v_22],[v_22,v_23,v_13],
												 [v_11,v_16,v_26],[v_26,v_21,v_11],
												 [v_111,v_110,v_210],[v_210,v_211,v_111],
												 [v_17,v_112,v_212],[v_212,v_27,v_17],
												 [v_11,v_21,v_12],[v_21,v_22,v_12],
												 [v_112,v_111,v_212],[v_212,v_111,v_211],
												 [v_14,v_13,v_24],[v_24,v_13,v_23],
												 [v_16,v_15,v_26],[v_26,v_15,v_25],
												 [v_18,v_17,v_27],[v_27,v_28,v_18],
												 [v_110,v_19,v_29],[v_29,v_210,v_110]]

									elif elements[j].crossSection['Type'] == 'C-Beam':
										tw = elements[j].crossSection['top width, tw']
										tt = elements[j].crossSection['top thickness, tt']
										mt = elements[j].crossSection['middle thickness, mt']
										bw = elements[j].crossSection['bottom width, bw']
										bt = elements[j].crossSection['bottom thickness, bt']
										h  = elements[j].crossSection['height, h']
										A1  = tt*tw
										A2  = mt*(h-tt-bt)
										A3  = bt*bw
										A   = A1+A2+A3
										zC1 = tw/2.
										zC2 = mt/2.
										zC3 = bw/2.
										yC1 = h-(tt/2.)
										yC2 = (h-tt)/2.
										yC3 = bt/2.
										if A != 0.:
											zC = (A1*zC1+A2*zC2+A3*zC3)/A
											yC = (A1*yC1+A2*yC2+A3*yC3)/A
										else:
											zC = 0.
											yC = 0.
										v_11  = [[node1_coord[0]-y_vec[0]*yC-z_vec[0]*zC,
												  node1_coord[1]-y_vec[1]*yC-z_vec[1]*zC,
												  node1_coord[2]-y_vec[2]*yC-z_vec[2]*zC ], node1_color]
										v_12  = [[node1_coord[0]-y_vec[0]*yC+z_vec[0]*(bw-zC),
												  node1_coord[1]-y_vec[1]*yC+z_vec[1]*(bw-zC),
												  node1_coord[2]-y_vec[2]*yC+z_vec[2]*(bw-zC) ], node1_color]
										v_13  = [[node1_coord[0]-y_vec[0]*(yC-bt)+z_vec[0]*(bw-zC),
												  node1_coord[1]-y_vec[1]*(yC-bt)+z_vec[1]*(bw-zC),
												  node1_coord[2]-y_vec[2]*(yC-bt)+z_vec[2]*(bw-zC) ], node1_color]
										v_14  = [[node1_coord[0]-y_vec[0]*(yC-bt)-z_vec[0]*(zC-mt),
												  node1_coord[1]-y_vec[1]*(yC-bt)-z_vec[1]*(zC-mt),
												  node1_coord[2]-y_vec[2]*(yC-bt)-z_vec[2]*(zC-mt) ], node1_color]
										v_15  = [[node1_coord[0]+y_vec[0]*(h-yC-tt)-z_vec[0]*(zC-mt),
												  node1_coord[1]+y_vec[1]*(h-yC-tt)-z_vec[1]*(zC-mt),
												  node1_coord[2]+y_vec[2]*(h-yC-tt)-z_vec[2]*(zC-mt) ], node1_color]
										v_16  = [[node1_coord[0]+y_vec[0]*(h-yC-tt)+z_vec[0]*(tw-zC),
												  node1_coord[1]+y_vec[1]*(h-yC-tt)+z_vec[1]*(tw-zC),
												  node1_coord[2]+y_vec[2]*(h-yC-tt)+z_vec[2]*(tw-zC) ], node1_color]
										v_17  = [[node1_coord[0]+y_vec[0]*(h-yC)+z_vec[0]*(tw-zC),
												  node1_coord[1]+y_vec[1]*(h-yC)+z_vec[1]*(tw-zC),
												  node1_coord[2]+y_vec[2]*(h-yC)+z_vec[2]*(tw-zC) ], node1_color]
										v_18  = [[node1_coord[0]+y_vec[0]*(h-yC)-z_vec[0]*zC,
												  node1_coord[1]+y_vec[1]*(h-yC)-z_vec[1]*zC,
												  node1_coord[2]+y_vec[2]*(h-yC)-z_vec[2]*zC ], node1_color]
										v_21  = [[node2_coord[0]-y_vec[0]*yC-z_vec[0]*zC,
												  node2_coord[1]-y_vec[1]*yC-z_vec[1]*zC,
												  node2_coord[2]-y_vec[2]*yC-z_vec[2]*zC ], node2_color]
										v_22  = [[node2_coord[0]-y_vec[0]*yC+z_vec[0]*(bw-zC),
												  node2_coord[1]-y_vec[1]*yC+z_vec[1]*(bw-zC),
												  node2_coord[2]-y_vec[2]*yC+z_vec[2]*(bw-zC) ], node2_color]
										v_23  = [[node2_coord[0]-y_vec[0]*(yC-bt)+z_vec[0]*(bw-zC),
												  node2_coord[1]-y_vec[1]*(yC-bt)+z_vec[1]*(bw-zC),
												  node2_coord[2]-y_vec[2]*(yC-bt)+z_vec[2]*(bw-zC) ], node2_color]
										v_24  = [[node2_coord[0]-y_vec[0]*(yC-bt)-z_vec[0]*(zC-mt),
												  node2_coord[1]-y_vec[1]*(yC-bt)-z_vec[1]*(zC-mt),
												  node2_coord[2]-y_vec[2]*(yC-bt)-z_vec[2]*(zC-mt) ], node2_color]
										v_25  = [[node2_coord[0]+y_vec[0]*(h-yC-tt)-z_vec[0]*(zC-mt),
												  node2_coord[1]+y_vec[1]*(h-yC-tt)-z_vec[1]*(zC-mt),
												  node2_coord[2]+y_vec[2]*(h-yC-tt)-z_vec[2]*(zC-mt) ], node2_color]
										v_26  = [[node2_coord[0]+y_vec[0]*(h-yC-tt)+z_vec[0]*(tw-zC),
												  node2_coord[1]+y_vec[1]*(h-yC-tt)+z_vec[1]*(tw-zC),
												  node2_coord[2]+y_vec[2]*(h-yC-tt)+z_vec[2]*(tw-zC) ], node2_color]
										v_27  = [[node2_coord[0]+y_vec[0]*(h-yC)+z_vec[0]*(tw-zC),
												  node2_coord[1]+y_vec[1]*(h-yC)+z_vec[1]*(tw-zC),
												  node2_coord[2]+y_vec[2]*(h-yC)+z_vec[2]*(tw-zC) ], node2_color]
										v_28  = [[node2_coord[0]+y_vec[0]*(h-yC)-z_vec[0]*zC,
												  node2_coord[1]+y_vec[1]*(h-yC)-z_vec[1]*zC,
												  node2_coord[2]+y_vec[2]*(h-yC)-z_vec[2]*zC ], node2_color]
										v_11[0] = rotatePointAboutAxis(v_11[0],node1_coord,[node1_coord[0]+1,node1_coord[1],node1_coord[2]],node1_rotation[0])
										v_11[0] = rotatePointAboutAxis(v_11[0],node1_coord,[node1_coord[0],node1_coord[1]+1,node1_coord[2]],node1_rotation[1])
										v_11[0] = rotatePointAboutAxis(v_11[0],node1_coord,[node1_coord[0],node1_coord[1],node1_coord[2]+1],node1_rotation[2])
										v_12[0] = rotatePointAboutAxis(v_12[0],node1_coord,[node1_coord[0]+1,node1_coord[1],node1_coord[2]],node1_rotation[0])
										v_12[0] = rotatePointAboutAxis(v_12[0],node1_coord,[node1_coord[0],node1_coord[1]+1,node1_coord[2]],node1_rotation[1])
										v_12[0] = rotatePointAboutAxis(v_12[0],node1_coord,[node1_coord[0],node1_coord[1],node1_coord[2]+1],node1_rotation[2])
										v_13[0] = rotatePointAboutAxis(v_13[0],node1_coord,[node1_coord[0]+1,node1_coord[1],node1_coord[2]],node1_rotation[0])
										v_13[0] = rotatePointAboutAxis(v_13[0],node1_coord,[node1_coord[0],node1_coord[1]+1,node1_coord[2]],node1_rotation[1])
										v_13[0] = rotatePointAboutAxis(v_13[0],node1_coord,[node1_coord[0],node1_coord[1],node1_coord[2]+1],node1_rotation[2])
										v_14[0] = rotatePointAboutAxis(v_14[0],node1_coord,[node1_coord[0]+1,node1_coord[1],node1_coord[2]],node1_rotation[0])
										v_14[0] = rotatePointAboutAxis(v_14[0],node1_coord,[node1_coord[0],node1_coord[1]+1,node1_coord[2]],node1_rotation[1])
										v_14[0] = rotatePointAboutAxis(v_14[0],node1_coord,[node1_coord[0],node1_coord[1],node1_coord[2]+1],node1_rotation[2])
										v_15[0] = rotatePointAboutAxis(v_15[0],node1_coord,[node1_coord[0]+1,node1_coord[1],node1_coord[2]],node1_rotation[0])
										v_15[0] = rotatePointAboutAxis(v_15[0],node1_coord,[node1_coord[0],node1_coord[1]+1,node1_coord[2]],node1_rotation[1])
										v_15[0] = rotatePointAboutAxis(v_15[0],node1_coord,[node1_coord[0],node1_coord[1],node1_coord[2]+1],node1_rotation[2])
										v_16[0] = rotatePointAboutAxis(v_16[0],node1_coord,[node1_coord[0]+1,node1_coord[1],node1_coord[2]],node1_rotation[0])
										v_16[0] = rotatePointAboutAxis(v_16[0],node1_coord,[node1_coord[0],node1_coord[1]+1,node1_coord[2]],node1_rotation[1])
										v_16[0] = rotatePointAboutAxis(v_16[0],node1_coord,[node1_coord[0],node1_coord[1],node1_coord[2]+1],node1_rotation[2])
										v_17[0] = rotatePointAboutAxis(v_17[0],node1_coord,[node1_coord[0]+1,node1_coord[1],node1_coord[2]],node1_rotation[0])
										v_17[0] = rotatePointAboutAxis(v_17[0],node1_coord,[node1_coord[0],node1_coord[1]+1,node1_coord[2]],node1_rotation[1])
										v_17[0] = rotatePointAboutAxis(v_17[0],node1_coord,[node1_coord[0],node1_coord[1],node1_coord[2]+1],node1_rotation[2])
										v_18[0] = rotatePointAboutAxis(v_18[0],node1_coord,[node1_coord[0]+1,node1_coord[1],node1_coord[2]],node1_rotation[0])
										v_18[0] = rotatePointAboutAxis(v_18[0],node1_coord,[node1_coord[0],node1_coord[1]+1,node1_coord[2]],node1_rotation[1])
										v_18[0] = rotatePointAboutAxis(v_18[0],node1_coord,[node1_coord[0],node1_coord[1],node1_coord[2]+1],node1_rotation[2])
										v_21[0] = rotatePointAboutAxis(v_21[0],node2_coord,[node2_coord[0]+1,node2_coord[1],node2_coord[2]],node2_rotation[0])
										v_21[0] = rotatePointAboutAxis(v_21[0],node2_coord,[node2_coord[0],node2_coord[1]+1,node2_coord[2]],node2_rotation[1])
										v_21[0] = rotatePointAboutAxis(v_21[0],node2_coord,[node2_coord[0],node2_coord[1],node2_coord[2]+1],node2_rotation[2])
										v_22[0] = rotatePointAboutAxis(v_22[0],node2_coord,[node2_coord[0]+1,node2_coord[1],node2_coord[2]],node2_rotation[0])
										v_22[0] = rotatePointAboutAxis(v_22[0],node2_coord,[node2_coord[0],node2_coord[1]+1,node2_coord[2]],node2_rotation[1])
										v_22[0] = rotatePointAboutAxis(v_22[0],node2_coord,[node2_coord[0],node2_coord[1],node2_coord[2]+1],node2_rotation[2])
										v_23[0] = rotatePointAboutAxis(v_23[0],node2_coord,[node2_coord[0]+1,node2_coord[1],node2_coord[2]],node2_rotation[0])
										v_23[0] = rotatePointAboutAxis(v_23[0],node2_coord,[node2_coord[0],node2_coord[1]+1,node2_coord[2]],node2_rotation[1])
										v_23[0] = rotatePointAboutAxis(v_23[0],node2_coord,[node2_coord[0],node2_coord[1],node2_coord[2]+1],node2_rotation[2])
										v_24[0] = rotatePointAboutAxis(v_24[0],node2_coord,[node2_coord[0]+1,node2_coord[1],node2_coord[2]],node2_rotation[0])
										v_24[0] = rotatePointAboutAxis(v_24[0],node2_coord,[node2_coord[0],node2_coord[1]+1,node2_coord[2]],node2_rotation[1])
										v_24[0] = rotatePointAboutAxis(v_24[0],node2_coord,[node2_coord[0],node2_coord[1],node2_coord[2]+1],node2_rotation[2])
										v_25[0] = rotatePointAboutAxis(v_25[0],node2_coord,[node2_coord[0]+1,node2_coord[1],node2_coord[2]],node2_rotation[0])
										v_25[0] = rotatePointAboutAxis(v_25[0],node2_coord,[node2_coord[0],node2_coord[1]+1,node2_coord[2]],node2_rotation[1])
										v_25[0] = rotatePointAboutAxis(v_25[0],node2_coord,[node2_coord[0],node2_coord[1],node2_coord[2]+1],node2_rotation[2])
										v_26[0] = rotatePointAboutAxis(v_26[0],node2_coord,[node2_coord[0]+1,node2_coord[1],node2_coord[2]],node2_rotation[0])
										v_26[0] = rotatePointAboutAxis(v_26[0],node2_coord,[node2_coord[0],node2_coord[1]+1,node2_coord[2]],node2_rotation[1])
										v_26[0] = rotatePointAboutAxis(v_26[0],node2_coord,[node2_coord[0],node2_coord[1],node2_coord[2]+1],node2_rotation[2])
										v_27[0] = rotatePointAboutAxis(v_27[0],node2_coord,[node2_coord[0]+1,node2_coord[1],node2_coord[2]],node2_rotation[0])
										v_27[0] = rotatePointAboutAxis(v_27[0],node2_coord,[node2_coord[0],node2_coord[1]+1,node2_coord[2]],node2_rotation[1])
										v_27[0] = rotatePointAboutAxis(v_27[0],node2_coord,[node2_coord[0],node2_coord[1],node2_coord[2]+1],node2_rotation[2])
										v_28[0] = rotatePointAboutAxis(v_28[0],node2_coord,[node2_coord[0]+1,node2_coord[1],node2_coord[2]],node2_rotation[0])
										v_28[0] = rotatePointAboutAxis(v_28[0],node2_coord,[node2_coord[0],node2_coord[1]+1,node2_coord[2]],node2_rotation[1])
										v_28[0] = rotatePointAboutAxis(v_28[0],node2_coord,[node2_coord[0],node2_coord[1],node2_coord[2]+1],node2_rotation[2])

										lines = [[v_11,v_12],[v_12,v_13],[v_13,v_14],[v_14,v_15],
												 [v_15,v_16],[v_16,v_17],[v_17,v_18],[v_18,v_11],
												 [v_21,v_22],[v_22,v_23],[v_23,v_24],[v_24,v_25],
												 [v_25,v_26],[v_26,v_27],[v_27,v_28],[v_28,v_21],
												 [v_11,v_21],[v_12,v_22],[v_13,v_23],[v_14,v_24],
												 [v_15,v_25],[v_16,v_26],[v_17,v_27],[v_18,v_28]]
										faces = [[v_11,v_12,v_13],[v_13,v_14,v_11],
												 [v_11,v_14,v_18],[v_18,v_14,v_15],
												 [v_15,v_16,v_17],[v_17,v_18,v_15],
												 [v_23,v_22,v_21],[v_21,v_24,v_23],
												 [v_24,v_21,v_28],[v_24,v_28,v_25],
												 [v_26,v_25,v_27],[v_28,v_27,v_25],
												 [v_11,v_21,v_12],[v_12,v_21,v_22],
												 [v_11,v_18,v_28],[v_28,v_21,v_11],
												 [v_18,v_17,v_28],[v_28,v_17,v_27],
												 [v_16,v_26,v_27],[v_27,v_17,v_16],
												 [v_16,v_15,v_25],[v_25,v_26,v_16],
												 [v_14,v_24,v_25],[v_25,v_15,v_14],
												 [v_13,v_24,v_14],[v_24,v_13,v_23],
												 [v_13,v_12,v_22],[v_22,v_23,v_13]]

									elif elements[j].crossSection['Type'] == 'T-Beam':
										tw = elements[j].crossSection['top width, tw']
										tt = elements[j].crossSection['top thickness, tt']
										mt = elements[j].crossSection['middle thickness, mt']
										h  = elements[j].crossSection['height, h']
										A1  = mt*(h-tt)
										A2  = tt*tw
										A   = A1+A2
										yC1 = h-(tt/2.)
										yC2 = (h-tt)/2.
										if A != 0.:
											yC = (A1*yC1+A2*yC2)/A
										else:
											yC = 0.
										tw = tw/2.
										tt = tt
										mt = mt/2.
										v_11  = [[node1_coord[0]-y_vec[0]*yC-z_vec[0]*mt,
												  node1_coord[1]-y_vec[1]*yC-z_vec[1]*mt,
												  node1_coord[2]-y_vec[2]*yC-z_vec[2]*mt ], node1_color]
										v_12  = [[node1_coord[0]-y_vec[0]*yC+z_vec[0]*mt,
												  node1_coord[1]-y_vec[1]*yC+z_vec[1]*mt,
												  node1_coord[2]-y_vec[2]*yC+z_vec[2]*mt ], node1_color]
										v_17  = [[node1_coord[0]+y_vec[0]*(h-yC-tt)-z_vec[0]*tw,
												  node1_coord[1]+y_vec[1]*(h-yC-tt)-z_vec[1]*tw,
												  node1_coord[2]+y_vec[2]*(h-yC-tt)-z_vec[2]*tw ], node1_color]
										v_18  = [[node1_coord[0]+y_vec[0]*(h-yC-tt)-z_vec[0]*mt,
												  node1_coord[1]+y_vec[1]*(h-yC-tt)-z_vec[1]*mt,
												  node1_coord[2]+y_vec[2]*(h-yC-tt)-z_vec[2]*mt ], node1_color]
										v_19  = [[node1_coord[0]+y_vec[0]*(h-yC-tt)+z_vec[0]*mt,
												  node1_coord[1]+y_vec[1]*(h-yC-tt)+z_vec[1]*mt,
												  node1_coord[2]+y_vec[2]*(h-yC-tt)+z_vec[2]*mt ], node1_color]
										v_110 = [[node1_coord[0]+y_vec[0]*(h-yC-tt)+z_vec[0]*tw,
												  node1_coord[1]+y_vec[1]*(h-yC-tt)+z_vec[1]*tw,
												  node1_coord[2]+y_vec[2]*(h-yC-tt)+z_vec[2]*tw ], node1_color]
										v_111 = [[node1_coord[0]+y_vec[0]*(h-yC)+z_vec[0]*tw,
												  node1_coord[1]+y_vec[1]*(h-yC)+z_vec[1]*tw,
												  node1_coord[2]+y_vec[2]*(h-yC)+z_vec[2]*tw ], node1_color]
										v_112 = [[node1_coord[0]+y_vec[0]*(h-yC)-z_vec[0]*tw,
												  node1_coord[1]+y_vec[1]*(h-yC)-z_vec[1]*tw,
												  node1_coord[2]+y_vec[2]*(h-yC)-z_vec[2]*tw ], node2_color]
										v_21  = [[node2_coord[0]-y_vec[0]*yC-z_vec[0]*mt,
												  node2_coord[1]-y_vec[1]*yC-z_vec[1]*mt,
												  node2_coord[2]-y_vec[2]*yC-z_vec[2]*mt ], node2_color]
										v_22  = [[node2_coord[0]-y_vec[0]*yC+z_vec[0]*mt,
												  node2_coord[1]-y_vec[1]*yC+z_vec[1]*mt,
												  node2_coord[2]-y_vec[2]*yC+z_vec[2]*mt ], node2_color]
										v_27  = [[node2_coord[0]+y_vec[0]*(h-yC-tt)-z_vec[0]*tw,
												  node2_coord[1]+y_vec[1]*(h-yC-tt)-z_vec[1]*tw,
												  node2_coord[2]+y_vec[2]*(h-yC-tt)-z_vec[2]*tw ], node2_color]
										v_28  = [[node2_coord[0]+y_vec[0]*(h-yC-tt)-z_vec[0]*mt,
												  node2_coord[1]+y_vec[1]*(h-yC-tt)-z_vec[1]*mt,
												  node2_coord[2]+y_vec[2]*(h-yC-tt)-z_vec[2]*mt ], node2_color]
										v_29  = [[node2_coord[0]+y_vec[0]*(h-yC-tt)+z_vec[0]*mt,
												  node2_coord[1]+y_vec[1]*(h-yC-tt)+z_vec[1]*mt,
												  node2_coord[2]+y_vec[2]*(h-yC-tt)+z_vec[2]*mt ], node2_color]
										v_210 = [[node2_coord[0]+y_vec[0]*(h-yC-tt)+z_vec[0]*tw,
												  node2_coord[1]+y_vec[1]*(h-yC-tt)+z_vec[1]*tw,
												  node2_coord[2]+y_vec[2]*(h-yC-tt)+z_vec[2]*tw ], node2_color]
										v_211 = [[node2_coord[0]+y_vec[0]*(h-yC)+z_vec[0]*tw,
												  node2_coord[1]+y_vec[1]*(h-yC)+z_vec[1]*tw,
												  node2_coord[2]+y_vec[2]*(h-yC)+z_vec[2]*tw ], node2_color]
										v_212 = [[node2_coord[0]+y_vec[0]*(h-yC)-z_vec[0]*tw,
												  node2_coord[1]+y_vec[1]*(h-yC)-z_vec[1]*tw,
												  node2_coord[2]+y_vec[2]*(h-yC)-z_vec[2]*tw ], node2_color]
										v_11[0] = rotatePointAboutAxis(v_11[0],node1_coord,[node1_coord[0]+1,node1_coord[1],node1_coord[2]],node1_rotation[0])
										v_11[0] = rotatePointAboutAxis(v_11[0],node1_coord,[node1_coord[0],node1_coord[1]+1,node1_coord[2]],node1_rotation[1])
										v_11[0] = rotatePointAboutAxis(v_11[0],node1_coord,[node1_coord[0],node1_coord[1],node1_coord[2]+1],node1_rotation[2])
										v_12[0] = rotatePointAboutAxis(v_12[0],node1_coord,[node1_coord[0]+1,node1_coord[1],node1_coord[2]],node1_rotation[0])
										v_12[0] = rotatePointAboutAxis(v_12[0],node1_coord,[node1_coord[0],node1_coord[1]+1,node1_coord[2]],node1_rotation[1])
										v_12[0] = rotatePointAboutAxis(v_12[0],node1_coord,[node1_coord[0],node1_coord[1],node1_coord[2]+1],node1_rotation[2])
										v_17[0] = rotatePointAboutAxis(v_17[0],node1_coord,[node1_coord[0]+1,node1_coord[1],node1_coord[2]],node1_rotation[0])
										v_17[0] = rotatePointAboutAxis(v_17[0],node1_coord,[node1_coord[0],node1_coord[1]+1,node1_coord[2]],node1_rotation[1])
										v_17[0] = rotatePointAboutAxis(v_17[0],node1_coord,[node1_coord[0],node1_coord[1],node1_coord[2]+1],node1_rotation[2])
										v_18[0] = rotatePointAboutAxis(v_18[0],node1_coord,[node1_coord[0]+1,node1_coord[1],node1_coord[2]],node1_rotation[0])
										v_18[0] = rotatePointAboutAxis(v_18[0],node1_coord,[node1_coord[0],node1_coord[1]+1,node1_coord[2]],node1_rotation[1])
										v_18[0] = rotatePointAboutAxis(v_18[0],node1_coord,[node1_coord[0],node1_coord[1],node1_coord[2]+1],node1_rotation[2])
										v_19[0] = rotatePointAboutAxis(v_19[0],node1_coord,[node1_coord[0]+1,node1_coord[1],node1_coord[2]],node1_rotation[0])
										v_19[0] = rotatePointAboutAxis(v_19[0],node1_coord,[node1_coord[0],node1_coord[1]+1,node1_coord[2]],node1_rotation[1])
										v_19[0] = rotatePointAboutAxis(v_19[0],node1_coord,[node1_coord[0],node1_coord[1],node1_coord[2]+1],node1_rotation[2])
										v_110[0] = rotatePointAboutAxis(v_110[0],node1_coord,[node1_coord[0]+1,node1_coord[1],node1_coord[2]],node1_rotation[0])
										v_110[0] = rotatePointAboutAxis(v_110[0],node1_coord,[node1_coord[0],node1_coord[1]+1,node1_coord[2]],node1_rotation[1])
										v_110[0] = rotatePointAboutAxis(v_110[0],node1_coord,[node1_coord[0],node1_coord[1],node1_coord[2]+1],node1_rotation[2])
										v_111[0] = rotatePointAboutAxis(v_111[0],node1_coord,[node1_coord[0]+1,node1_coord[1],node1_coord[2]],node1_rotation[0])
										v_111[0] = rotatePointAboutAxis(v_111[0],node1_coord,[node1_coord[0],node1_coord[1]+1,node1_coord[2]],node1_rotation[1])
										v_111[0] = rotatePointAboutAxis(v_111[0],node1_coord,[node1_coord[0],node1_coord[1],node1_coord[2]+1],node1_rotation[2])
										v_112[0] = rotatePointAboutAxis(v_112[0],node1_coord,[node1_coord[0]+1,node1_coord[1],node1_coord[2]],node1_rotation[0])
										v_112[0] = rotatePointAboutAxis(v_112[0],node1_coord,[node1_coord[0],node1_coord[1]+1,node1_coord[2]],node1_rotation[1])
										v_112[0] = rotatePointAboutAxis(v_112[0],node1_coord,[node1_coord[0],node1_coord[1],node1_coord[2]+1],node1_rotation[2])
										v_21[0] = rotatePointAboutAxis(v_21[0],node2_coord,[node2_coord[0]+1,node2_coord[1],node2_coord[2]],node2_rotation[0])
										v_21[0] = rotatePointAboutAxis(v_21[0],node2_coord,[node2_coord[0],node2_coord[1]+1,node2_coord[2]],node2_rotation[1])
										v_21[0] = rotatePointAboutAxis(v_21[0],node2_coord,[node2_coord[0],node2_coord[1],node2_coord[2]+1],node2_rotation[2])
										v_22[0] = rotatePointAboutAxis(v_22[0],node2_coord,[node2_coord[0]+1,node2_coord[1],node2_coord[2]],node2_rotation[0])
										v_22[0] = rotatePointAboutAxis(v_22[0],node2_coord,[node2_coord[0],node2_coord[1]+1,node2_coord[2]],node2_rotation[1])
										v_22[0] = rotatePointAboutAxis(v_22[0],node2_coord,[node2_coord[0],node2_coord[1],node2_coord[2]+1],node2_rotation[2])
										v_27[0] = rotatePointAboutAxis(v_27[0],node2_coord,[node2_coord[0]+1,node2_coord[1],node2_coord[2]],node2_rotation[0])
										v_27[0] = rotatePointAboutAxis(v_27[0],node2_coord,[node2_coord[0],node2_coord[1]+1,node2_coord[2]],node2_rotation[1])
										v_27[0] = rotatePointAboutAxis(v_27[0],node2_coord,[node2_coord[0],node2_coord[1],node2_coord[2]+1],node2_rotation[2])
										v_28[0] = rotatePointAboutAxis(v_28[0],node2_coord,[node2_coord[0]+1,node2_coord[1],node2_coord[2]],node2_rotation[0])
										v_28[0] = rotatePointAboutAxis(v_28[0],node2_coord,[node2_coord[0],node2_coord[1]+1,node2_coord[2]],node2_rotation[1])
										v_28[0] = rotatePointAboutAxis(v_28[0],node2_coord,[node2_coord[0],node2_coord[1],node2_coord[2]+1],node2_rotation[2])
										v_29[0] = rotatePointAboutAxis(v_29[0],node2_coord,[node2_coord[0]+1,node2_coord[1],node2_coord[2]],node2_rotation[0])
										v_29[0] = rotatePointAboutAxis(v_29[0],node2_coord,[node2_coord[0],node2_coord[1]+1,node2_coord[2]],node2_rotation[1])
										v_29[0] = rotatePointAboutAxis(v_29[0],node2_coord,[node2_coord[0],node2_coord[1],node2_coord[2]+1],node2_rotation[2])
										v_210[0] = rotatePointAboutAxis(v_210[0],node2_coord,[node2_coord[0]+1,node2_coord[1],node2_coord[2]],node2_rotation[0])
										v_210[0] = rotatePointAboutAxis(v_210[0],node2_coord,[node2_coord[0],node2_coord[1]+1,node2_coord[2]],node2_rotation[1])
										v_210[0] = rotatePointAboutAxis(v_210[0],node2_coord,[node2_coord[0],node2_coord[1],node2_coord[2]+1],node2_rotation[2])
										v_211[0] = rotatePointAboutAxis(v_211[0],node2_coord,[node2_coord[0]+1,node2_coord[1],node2_coord[2]],node2_rotation[0])
										v_211[0] = rotatePointAboutAxis(v_211[0],node2_coord,[node2_coord[0],node2_coord[1]+1,node2_coord[2]],node2_rotation[1])
										v_211[0] = rotatePointAboutAxis(v_211[0],node2_coord,[node2_coord[0],node2_coord[1],node2_coord[2]+1],node2_rotation[2])
										v_212[0] = rotatePointAboutAxis(v_212[0],node2_coord,[node2_coord[0]+1,node2_coord[1],node2_coord[2]],node2_rotation[0])
										v_212[0] = rotatePointAboutAxis(v_212[0],node2_coord,[node2_coord[0],node2_coord[1]+1,node2_coord[2]],node2_rotation[1])
										v_212[0] = rotatePointAboutAxis(v_212[0],node2_coord,[node2_coord[0],node2_coord[1],node2_coord[2]+1],node2_rotation[2])

										lines = [[v_11,v_12],[v_12,v_19],[v_19,v_110],[v_110,v_111],
												 [v_111,v_112],[v_112,v_17],[v_17,v_18],[v_18,v_11],
												 [v_21,v_22],[v_22,v_29],[v_29,v_210],[v_210,v_211],
												 [v_211,v_212],[v_212,v_27],[v_27,v_28],[v_28,v_21],
												 [v_11,v_21],[v_12,v_22],[v_17,v_27],[v_18,v_28],
												 [v_19,v_29],[v_110,v_210],[v_111,v_211],[v_112,v_212]]
										faces = [[v_11,v_12,v_19],[v_19,v_18,v_11],
												 [v_112,v_17,v_110],[v_110,v_111,v_112],
												 [v_29,v_22,v_21],[v_21,v_28,v_29],
												 [v_210,v_27,v_212],[v_212,v_211,v_210],
												 [v_19,v_12,v_22],[v_22,v_29,v_19],
												 [v_11,v_18,v_28],[v_28,v_21,v_11],
												 [v_111,v_110,v_210],[v_210,v_211,v_111],
												 [v_17,v_112,v_212],[v_212,v_27,v_17],
												 [v_11,v_21,v_12],[v_21,v_22,v_12],
												 [v_112,v_111,v_212],[v_212,v_111,v_211],
												 [v_18,v_17,v_27],[v_27,v_28,v_18],
												 [v_110,v_19,v_29],[v_29,v_210,v_110]]

									else:
										pass

									glLineWidth(2.0)
									glColor3f(0.05, 0.1, 0.05)
									for line in range(len(lines)):
										glBegin(GL_LINES)
										glVertex3f(lines[line][0][0][0],lines[line][0][0][1],lines[line][0][0][2])
										glVertex3f(lines[line][1][0][0],lines[line][1][0][1],lines[line][1][0][2])
										glEnd()

									for face in range(len(faces)):
										glBegin(GL_TRIANGLES)
										glColor3f(faces[face][0][1][0],faces[face][0][1][1],faces[face][0][1][2])
										glVertex3f(faces[face][0][0][0],faces[face][0][0][1],faces[face][0][0][2])
										glColor3f(faces[face][1][1][0],faces[face][1][1][1],faces[face][1][1][2])
										glVertex3f(faces[face][1][0][0],faces[face][1][0][1],faces[face][1][0][2])
										glColor3f(faces[face][2][1][0],faces[face][2][1][1],faces[face][2][1][2])
										glVertex3f(faces[face][2][0][0],faces[face][2][0][1],faces[face][2][0][2])
										glEnd()
						
					glEndList()

				elif result == 'nodeforce':

					# shaded mode, model force vectors at nodes, contoured to show values
					disp_max = 0.
					disp_min = 0.
					for i in nodes:
						if subresult == 'Force':
							if 'nodeforce' not in nodes[i].solutions[solution]:
								pass
							elif nodes[i].solutions[solution]['nodeforce'][6] >= disp_max:
								disp_max = nodes[i].solutions[solution]['nodeforce'][6]
							else:
								pass
						else:
							if 'nodeforce' not in nodes[i].solutions[solution]:
								pass
							else:
								moment_magn = np.sqrt((nodes[i].solutions[solution]['nodeforce'][3])**2 + \
													  (nodes[i].solutions[solution]['nodeforce'][4])**2 + \
													  (nodes[i].solutions[solution]['nodeforce'][5])**2)
								if moment_magn >= disp_max:
									disp_max = moment_magn
								else:
									pass
					self.displayLists[solution][result][subresult]['info'] = 'Max %.4E' % (disp_max)

					self.displayLists[solution][result][subresult]['max_val'] = disp_max
					self.displayLists[solution][result][subresult]['min_val'] = disp_min

					glNewList(self.displayLists[solution][result][subresult]['shaded'], GL_COMPILE)

					disp_mag_values = [ disp_min,
										disp_min+(disp_max-disp_min)*1./12.,
										disp_min+(disp_max-disp_min)*2./12.,
										disp_min+(disp_max-disp_min)*3./12.,
										disp_min+(disp_max-disp_min)*4./12.,
										disp_min+(disp_max-disp_min)*5./12.,
										disp_min+(disp_max-disp_min)*6./12.,
										disp_min+(disp_max-disp_min)*7./12.,
										disp_min+(disp_max-disp_min)*8./12.,
										disp_min+(disp_max-disp_min)*9./12.,
										disp_min+(disp_max-disp_min)*10./12.,
										disp_min+(disp_max-disp_min)*11./12.,
										disp_max ]
					disp_colors = [ (  0.0,   0.0,   1.0), # blue
									(  0.0, 0.333,   1.0),  
									(  0.0, 0.666,   1.0),  
									(  0.0,   1.0,   1.0),  
									(  0.0,   1.0, 0.666),  
									(  0.0,   1.0, 0.333),
									(  0.0,   1.0,   0.0), # green
									(0.333,   1.0,   0.0),  
									(0.666,   1.0,   0.0),  
									(  1.0,   1.0,   0.0),  
									(  1.0, 0.666,   0.0),  
									(  1.0, 0.333,   0.0),
									(  1.0,   0.0,   0.0) ] # red
					disp_color = disp_colors[0]

					glLineWidth(9.0)
					for j in nodes:
						if subresult == 'Force':
							for k in range(len(disp_mag_values)):
								if 'nodeforce' not in nodes[j].solutions[solution]:
									disp_color = (0.1, 0.1, 0.1)
								elif nodes[j].solutions[solution]['nodeforce'][6] > disp_mag_values[k]:
									pass
								else:
									disp_color = disp_colors[k]
									break
							if 'nodeforce' not in nodes[j].solutions[solution]:
								pass
							else:
								glColor3f(disp_color[0], disp_color[1], disp_color[2])

								if nodes[j].solutions[solution]['nodeforce'][6] < 1.e-7:
									pass
								else:
									glBegin(GL_LINES)
									glVertex3f(nodes[j].coord[0][0] + scale_factor*displacements[nodes[j].number].solutions[solution]['displacement'][0],
											   nodes[j].coord[1][0] + scale_factor*displacements[nodes[j].number].solutions[solution]['displacement'][1], 
											   nodes[j].coord[2][0] + scale_factor*displacements[nodes[j].number].solutions[solution]['displacement'][2])
									x = nodes[j].solutions[solution]['nodeforce'][0]/disp_max
									y = nodes[j].solutions[solution]['nodeforce'][1]/disp_max
									z = nodes[j].solutions[solution]['nodeforce'][2]/disp_max
									max_xyz = max(abs(x),abs(y),abs(z))
									if max_xyz == 0.:
										max_xyz = 0.1
									x = -x/max_xyz
									y = -y/max_xyz
									z = -z/max_xyz
									glVertex3f(nodes[j].coord[0][0] + scale_factor*displacements[nodes[j].number].solutions[solution]['displacement'][0] \
												-x*0.1*mesh.viewRadius, 
											   nodes[j].coord[1][0] + scale_factor*displacements[nodes[j].number].solutions[solution]['displacement'][1] \
												-y*0.1*mesh.viewRadius, 
											   nodes[j].coord[2][0] + scale_factor*displacements[nodes[j].number].solutions[solution]['displacement'][2] \
												-z*0.1*mesh.viewRadius)
									glEnd()
									angle = np.pi/4
									if (x == 0) and (y == 0):
										x_arrow = x*np.cos(angle) - z*np.sin(angle)
										y_arrow = y
										z_arrow = x*np.sin(angle) + z*np.cos(angle)
									else:
										x_arrow = x*np.cos(angle) - y*np.sin(angle)
										y_arrow = x*np.sin(angle) + y*np.cos(angle)
										z_arrow = z
									glBegin(GL_LINES)
									glVertex3f(nodes[j].coord[0][0] + scale_factor*displacements[nodes[j].number].solutions[solution]['displacement'][0] \
												-x*0.1*mesh.viewRadius, 
											   nodes[j].coord[1][0] + scale_factor*displacements[nodes[j].number].solutions[solution]['displacement'][1] \
												-y*0.1*mesh.viewRadius, 
											   nodes[j].coord[2][0] + scale_factor*displacements[nodes[j].number].solutions[solution]['displacement'][2] \
												-z*0.1*mesh.viewRadius)
									glVertex3f(nodes[j].coord[0][0] + scale_factor*displacements[nodes[j].number].solutions[solution]['displacement'][0] \
												-x*0.1*mesh.viewRadius + x_arrow*0.02*mesh.viewRadius, 
											   nodes[j].coord[1][0] + scale_factor*displacements[nodes[j].number].solutions[solution]['displacement'][1] \
												-y*0.1*mesh.viewRadius + y_arrow*0.02*mesh.viewRadius, 
											   nodes[j].coord[2][0] + scale_factor*displacements[nodes[j].number].solutions[solution]['displacement'][2] \
												-z*0.1*mesh.viewRadius + z_arrow*0.02*mesh.viewRadius)
									glEnd()
									angle = -np.pi/4
									if (x == 0) and (y == 0):
										x_arrow = x*np.cos(angle) - z*np.sin(angle)
										y_arrow = y
										z_arrow = x*np.sin(angle) + z*np.cos(angle)
									else:
										x_arrow = x*np.cos(angle) - y*np.sin(angle)
										y_arrow = x*np.sin(angle) + y*np.cos(angle)
										z_arrow = z
									glBegin(GL_LINES)
									glVertex3f(nodes[j].coord[0][0] + scale_factor*displacements[nodes[j].number].solutions[solution]['displacement'][0] \
												-x*0.1*mesh.viewRadius, 
											   nodes[j].coord[1][0] + scale_factor*displacements[nodes[j].number].solutions[solution]['displacement'][1] \
												-y*0.1*mesh.viewRadius, 
											   nodes[j].coord[2][0] + scale_factor*displacements[nodes[j].number].solutions[solution]['displacement'][2] \
												-z*0.1*mesh.viewRadius)
									glVertex3f(nodes[j].coord[0][0] + scale_factor*displacements[nodes[j].number].solutions[solution]['displacement'][0] \
												-x*0.1*mesh.viewRadius + x_arrow*0.02*mesh.viewRadius, 
											   nodes[j].coord[1][0] + scale_factor*displacements[nodes[j].number].solutions[solution]['displacement'][1] \
												-y*0.1*mesh.viewRadius + y_arrow*0.02*mesh.viewRadius, 
											   nodes[j].coord[2][0] + scale_factor*displacements[nodes[j].number].solutions[solution]['displacement'][2] \
												-z*0.1*mesh.viewRadius + z_arrow*0.02*mesh.viewRadius)
									glEnd()

						else:
							for k in range(len(disp_mag_values)):
								if 'nodeforce' not in nodes[j].solutions[solution]:
									disp_color = (0.1, 0.1, 0.1)
								else:
									moment_magn = np.sqrt((nodes[j].solutions[solution]['nodeforce'][3])**2 + \
														  (nodes[j].solutions[solution]['nodeforce'][4])**2 + \
														  (nodes[j].solutions[solution]['nodeforce'][5])**2)
									if moment_magn > disp_mag_values[k]:
										pass
									else:
										disp_color = disp_colors[k]
										break

							if 'nodeforce' not in nodes[j].solutions[solution]:
								pass
							else:
								origin = [ nodes[j].coord[0][0] + scale_factor*displacements[nodes[j].number].solutions[solution]['displacement'][0],
										   nodes[j].coord[1][0] + scale_factor*displacements[nodes[j].number].solutions[solution]['displacement'][1], 
										   nodes[j].coord[2][0] + scale_factor*displacements[nodes[j].number].solutions[solution]['displacement'][2] ]
								moment_magn = np.sqrt((nodes[j].solutions[solution]['nodeforce'][3])**2 + \
													  (nodes[j].solutions[solution]['nodeforce'][4])**2 + \
													  (nodes[j].solutions[solution]['nodeforce'][5])**2)
								if moment_magn < 1.e-7:
									pass
								else:
									mx = nodes[j].solutions[solution]['nodeforce'][3]
									my = nodes[j].solutions[solution]['nodeforce'][4]
									mz = nodes[j].solutions[solution]['nodeforce'][5]

									if abs(mx) < 0.001 and abs(my) > 0.001:
										n1_offset = np.array([origin[0]-1, origin[1], origin[2]])
										n2_offset = np.array([origin[0]+mx-1, origin[1]+my, origin[2]+mz])
									else:
										n1_offset = np.array([origin[0], origin[1]+1, origin[2]])
										n2_offset = np.array([origin[0]+mx, origin[1]+my+1, origin[2]+mz])
									mv = np.array([mx, my, mz])
									xu = mv/moment_magn
									n_offset = n1_offset + 0.5*(n2_offset-n1_offset)
									ov = n_offset - np.array([origin[0],origin[1],origin[2]])
									yv = ov - np.dot(ov,xu)*xu
									mag = sqrt(yv[0]**2 + yv[1]**2 + yv[2]**2)
									if mag == 0.:
										yu = yv
									else:
										yu = yv/mag
									zu = np.cross(xu, yu)

									scale = 0.05*mesh.viewRadius
									vertices = []
									arrow = []
									for v in range(18):
										d = 24/(v+1)
										vc = np.cos(2*np.pi/d)
										vs = np.sin(2*np.pi/d)
										vertices.append([ origin[0]+vs*yu[0]*scale+vc*zu[0]*scale,
														  origin[1]+vs*yu[1]*scale+vc*zu[1]*scale,
														  origin[2]+vs*yu[2]*scale+vc*zu[2]*scale ])
										if v == 1:
											arrow.append([ origin[0]+vs*yu[0]*1.3*scale+vc*zu[0]*1.3*scale,
														   origin[1]+vs*yu[1]*1.3*scale+vc*zu[1]*1.3*scale,
														   origin[2]+vs*yu[2]*1.3*scale+vc*zu[2]*1.3*scale ])
											arrow.append([ origin[0]+vs*yu[0]*0.7*scale+vc*zu[0]*0.7*scale,
														   origin[1]+vs*yu[1]*0.7*scale+vc*zu[1]*0.7*scale,
														   origin[2]+vs*yu[2]*0.7*scale+vc*zu[2]*0.7*scale ])
									glColor3f(disp_color[0], disp_color[1], disp_color[2])
									for v in range(17):
										glBegin(GL_LINES)
										glVertex3f(vertices[v][0],vertices[v][1],vertices[v][2])
										glVertex3f(vertices[v+1][0],vertices[v+1][1],vertices[v+1][2])
										glEnd()
									glBegin(GL_LINES)
									glVertex3f(vertices[0][0],vertices[0][1],vertices[0][2])
									glVertex3f(arrow[0][0],arrow[0][1],arrow[0][2])
									glEnd()
									glBegin(GL_LINES)
									glVertex3f(vertices[0][0],vertices[0][1],vertices[0][2])
									glVertex3f(arrow[1][0],arrow[1][1],arrow[1][2])
									glEnd()
					glEndList()

				elif result == 'elementforce':

					disp_max = 0.
					disp_min = 0.
					for i in elements:
						if 'elementforce' not in elements[i].solutions[solution]:
							pass
						elif elements[i].type not in ['ROD2N', 'ROD2N2D', 'BEAM2N', 'BEAM2N2D']:
							pass
						elif subresult == 'FX':
							if elements[i].solutions[solution]['elementforce'][0] >= disp_max:
								disp_max = elements[i].solutions[solution]['elementforce'][0]
							if elements[i].solutions[solution]['elementforce'][0] <= disp_min:
								disp_min = elements[i].solutions[solution]['elementforce'][0]
						elif subresult == 'FY':
							if elements[i].solutions[solution]['elementforce'][1] >= disp_max:
								disp_max = elements[i].solutions[solution]['elementforce'][1]
							if elements[i].solutions[solution]['elementforce'][6] >= disp_max:
								disp_max = elements[i].solutions[solution]['elementforce'][6]
						elif subresult == 'FZ':
							if elements[i].solutions[solution]['elementforce'][2] >= disp_max:
								disp_max = elements[i].solutions[solution]['elementforce'][2]
							if elements[i].solutions[solution]['elementforce'][7] >= disp_max:
								disp_max = elements[i].solutions[solution]['elementforce'][7]
						elif subresult == 'MX':
							if elements[i].solutions[solution]['elementforce'][3] >= disp_max:
								disp_max = elements[i].solutions[solution]['elementforce'][3]
							if elements[i].solutions[solution]['elementforce'][8] >= disp_max:
								disp_max = elements[i].solutions[solution]['elementforce'][8]
						elif subresult == 'MY':
							if elements[i].solutions[solution]['elementforce'][4] >= disp_max:
								disp_max = elements[i].solutions[solution]['elementforce'][4]
							if elements[i].solutions[solution]['elementforce'][9] >= disp_max:
								disp_max = elements[i].solutions[solution]['elementforce'][9]
						elif subresult == 'MZ':
							if elements[i].solutions[solution]['elementforce'][5] >= disp_max:
								disp_max = elements[i].solutions[solution]['elementforce'][5]
							if elements[i].solutions[solution]['elementforce'][10] >= disp_max:
								disp_max = elements[i].solutions[solution]['elementforce'][10]
						else:
							pass
					self.displayLists[solution][result][subresult]['info'] = 'Max %.4E' % (disp_max)

					self.displayLists[solution][result][subresult]['max_val'] = disp_max
					self.displayLists[solution][result][subresult]['min_val'] = disp_min

					glNewList(self.displayLists[solution][result][subresult]['shaded'], GL_COMPILE)

					disp_mag_values = [ disp_min,
										disp_min+(disp_max-disp_min)*1./12.,
										disp_min+(disp_max-disp_min)*2./12.,
										disp_min+(disp_max-disp_min)*3./12.,
										disp_min+(disp_max-disp_min)*4./12.,
										disp_min+(disp_max-disp_min)*5./12.,
										disp_min+(disp_max-disp_min)*6./12.,
										disp_min+(disp_max-disp_min)*7./12.,
										disp_min+(disp_max-disp_min)*8./12.,
										disp_min+(disp_max-disp_min)*9./12.,
										disp_min+(disp_max-disp_min)*10./12.,
										disp_min+(disp_max-disp_min)*11./12.,
										disp_max ]
					disp_colors = [ (  0.0,   0.0,   1.0), # blue
									(  0.0, 0.333,   1.0),  
									(  0.0, 0.666,   1.0),  
									(  0.0,   1.0,   1.0),  
									(  0.0,   1.0, 0.666),  
									(  0.0,   1.0, 0.333),
									(  0.0,   1.0,   0.0), # green
									(0.333,   1.0,   0.0),  
									(0.666,   1.0,   0.0),  
									(  1.0,   1.0,   0.0),  
									(  1.0, 0.666,   0.0),  
									(  1.0, 0.333,   0.0),
									(  1.0,   0.0,   0.0) ] # red
					disp_color = disp_colors[0]

					glLineWidth(9.0)
					for j in elements:
						for k in range(len(disp_mag_values)):
							if 'elementforce' not in elements[j].solutions[solution]:
								disp_color = (0.1, 0.1, 0.1)
							elif (subresult == 'FX') and \
									(elements[j].solutions[solution]['elementforce'][0] > disp_mag_values[k]):
								pass
							else:
								disp_color = disp_colors[k]
								break
						node1_color = deepcopy(disp_color)
						glBegin(GL_LINES)
						glColor3f(disp_color[0], disp_color[1], disp_color[2])
						glVertex3f(nodes[elements[j].nodes[0].number].coord[0][0] + 
									scale_factor*(displacements[elements[j].nodes[0].number].solutions[solution]['displacement'][0]),
								   nodes[elements[j].nodes[0].number].coord[1][0] +
									scale_factor*(displacements[elements[j].nodes[0].number].solutions[solution]['displacement'][1]),
								   nodes[elements[j].nodes[0].number].coord[2][0] +
									scale_factor*(displacements[elements[j].nodes[0].number].solutions[solution]['displacement'][2]))
						for k in range(len(disp_mag_values)):
							if 'elementforce' not in elements[j].solutions[solution]:
								disp_color = (0.1, 0.1, 0.1)
							elif (subresult == 'FX') and \
									(elements[j].solutions[solution]['elementforce'][0] > disp_mag_values[k]):
								pass
							else:
								disp_color = disp_colors[k]
								break
						node2_color = deepcopy(disp_color)
						glColor3f(disp_color[0], disp_color[1], disp_color[2])
						glVertex3f(nodes[elements[j].nodes[1].number].coord[0][0] +
									scale_factor*(displacements[elements[j].nodes[1].number].solutions[solution]['displacement'][0]),
								   nodes[elements[j].nodes[1].number].coord[1][0] +
									scale_factor*(displacements[elements[j].nodes[1].number].solutions[solution]['displacement'][1]),
								   nodes[elements[j].nodes[1].number].coord[2][0] +
									scale_factor*(displacements[elements[j].nodes[1].number].solutions[solution]['displacement'][2]))
						glEnd()

						if elements[j].type in ['BEAM2N2D', 'BEAM2N', 'ROD2N2D', 'ROD2N']:
							if hasattr(elements[j],'crossSection'):
								if hasattr(elements[j],'orientation'):
									node1_coord = [nodes[elements[j].nodes[0].number].coord[0][0] + 
													scale_factor*(displacements[elements[j].nodes[0].number].solutions[solution]['displacement'][0]),
												   nodes[elements[j].nodes[0].number].coord[1][0] +
													scale_factor*(displacements[elements[j].nodes[0].number].solutions[solution]['displacement'][1]),
												   nodes[elements[j].nodes[0].number].coord[2][0] +
													scale_factor*(displacements[elements[j].nodes[0].number].solutions[solution]['displacement'][2])]
									node1_rotation = [scale_factor*(displacements[elements[j].nodes[0].number].solutions[solution]['displacement'][3]),
													  scale_factor*(displacements[elements[j].nodes[0].number].solutions[solution]['displacement'][4]),
													  scale_factor*(displacements[elements[j].nodes[0].number].solutions[solution]['displacement'][5])]
									node2_coord = [nodes[elements[j].nodes[1].number].coord[0][0] +
													scale_factor*(displacements[elements[j].nodes[1].number].solutions[solution]['displacement'][0]),
												   nodes[elements[j].nodes[1].number].coord[1][0] +
													scale_factor*(displacements[elements[j].nodes[1].number].solutions[solution]['displacement'][1]),
												   nodes[elements[j].nodes[1].number].coord[2][0] +
													scale_factor*(displacements[elements[j].nodes[1].number].solutions[solution]['displacement'][2])]
									node2_rotation = [scale_factor*(displacements[elements[j].nodes[1].number].solutions[solution]['displacement'][3]),
													  scale_factor*(displacements[elements[j].nodes[1].number].solutions[solution]['displacement'][4]),
													  scale_factor*(displacements[elements[j].nodes[1].number].solutions[solution]['displacement'][5])]

									faces = []
									lines = []
									x_vec = elements[j].orientation['x-vec']
									y_vec = elements[j].orientation['y-vec']
									z_vec = elements[j].orientation['z-vec']

									if elements[j].crossSection['Type'] == 'Rectangle':

										w  = elements[j].crossSection['width, w']
										h  = elements[j].crossSection['height, h']
										iw = elements[j].crossSection['inner width, iw']
										ih = elements[j].crossSection['inner height, ih']
										w  = w/2.
										h  = h/2.
										iw = iw/2.
										ih = ih/2.
										v_11 = [[node1_coord[0]-y_vec[0]*h-z_vec[0]*w,
												 node1_coord[1]-y_vec[1]*h-z_vec[1]*w,
												 node1_coord[2]-y_vec[2]*h-z_vec[2]*w ], node1_color]
										v_12 = [[node1_coord[0]-y_vec[0]*h+z_vec[0]*w,
												 node1_coord[1]-y_vec[1]*h+z_vec[1]*w,
												 node1_coord[2]-y_vec[2]*h+z_vec[2]*w ], node1_color]
										v_13 = [[node1_coord[0]+y_vec[0]*h+z_vec[0]*w,
												 node1_coord[1]+y_vec[1]*h+z_vec[1]*w,
												 node1_coord[2]+y_vec[2]*h+z_vec[2]*w ], node1_color]
										v_14 = [[node1_coord[0]+y_vec[0]*h-z_vec[0]*w,
												 node1_coord[1]+y_vec[1]*h-z_vec[1]*w,
												 node1_coord[2]+y_vec[2]*h-z_vec[2]*w ], node1_color]
										v_21 = [[node2_coord[0]-y_vec[0]*h-z_vec[0]*w,
												 node2_coord[1]-y_vec[1]*h-z_vec[1]*w,
												 node2_coord[2]-y_vec[2]*h-z_vec[2]*w ], node2_color]
										v_22 = [[node2_coord[0]-y_vec[0]*h+z_vec[0]*w,
												 node2_coord[1]-y_vec[1]*h+z_vec[1]*w,
												 node2_coord[2]-y_vec[2]*h+z_vec[2]*w ], node2_color]
										v_23 = [[node2_coord[0]+y_vec[0]*h+z_vec[0]*w,
												 node2_coord[1]+y_vec[1]*h+z_vec[1]*w,
												 node2_coord[2]+y_vec[2]*h+z_vec[2]*w ], node2_color]
										v_24 = [[node2_coord[0]+y_vec[0]*h-z_vec[0]*w,
												 node2_coord[1]+y_vec[1]*h-z_vec[1]*w,
												 node2_coord[2]+y_vec[2]*h-z_vec[2]*w ], node2_color]
										v_11[0] = rotatePointAboutAxis(v_11[0],node1_coord,[node1_coord[0]+1,node1_coord[1],node1_coord[2]],node1_rotation[0])
										v_11[0] = rotatePointAboutAxis(v_11[0],node1_coord,[node1_coord[0],node1_coord[1]+1,node1_coord[2]],node1_rotation[1])
										v_11[0] = rotatePointAboutAxis(v_11[0],node1_coord,[node1_coord[0],node1_coord[1],node1_coord[2]+1],node1_rotation[2])
										v_12[0] = rotatePointAboutAxis(v_12[0],node1_coord,[node1_coord[0]+1,node1_coord[1],node1_coord[2]],node1_rotation[0])
										v_12[0] = rotatePointAboutAxis(v_12[0],node1_coord,[node1_coord[0],node1_coord[1]+1,node1_coord[2]],node1_rotation[1])
										v_12[0] = rotatePointAboutAxis(v_12[0],node1_coord,[node1_coord[0],node1_coord[1],node1_coord[2]+1],node1_rotation[2])
										v_13[0] = rotatePointAboutAxis(v_13[0],node1_coord,[node1_coord[0]+1,node1_coord[1],node1_coord[2]],node1_rotation[0])
										v_13[0] = rotatePointAboutAxis(v_13[0],node1_coord,[node1_coord[0],node1_coord[1]+1,node1_coord[2]],node1_rotation[1])
										v_13[0] = rotatePointAboutAxis(v_13[0],node1_coord,[node1_coord[0],node1_coord[1],node1_coord[2]+1],node1_rotation[2])
										v_14[0] = rotatePointAboutAxis(v_14[0],node1_coord,[node1_coord[0]+1,node1_coord[1],node1_coord[2]],node1_rotation[0])
										v_14[0] = rotatePointAboutAxis(v_14[0],node1_coord,[node1_coord[0],node1_coord[1]+1,node1_coord[2]],node1_rotation[1])
										v_14[0] = rotatePointAboutAxis(v_14[0],node1_coord,[node1_coord[0],node1_coord[1],node1_coord[2]+1],node1_rotation[2])
										v_21[0] = rotatePointAboutAxis(v_21[0],node2_coord,[node2_coord[0]+1,node2_coord[1],node2_coord[2]],node2_rotation[0])
										v_21[0] = rotatePointAboutAxis(v_21[0],node2_coord,[node2_coord[0],node2_coord[1]+1,node2_coord[2]],node2_rotation[1])
										v_21[0] = rotatePointAboutAxis(v_21[0],node2_coord,[node2_coord[0],node2_coord[1],node2_coord[2]+1],node2_rotation[2])
										v_22[0] = rotatePointAboutAxis(v_22[0],node2_coord,[node2_coord[0]+1,node2_coord[1],node2_coord[2]],node2_rotation[0])
										v_22[0] = rotatePointAboutAxis(v_22[0],node2_coord,[node2_coord[0],node2_coord[1]+1,node2_coord[2]],node2_rotation[1])
										v_22[0] = rotatePointAboutAxis(v_22[0],node2_coord,[node2_coord[0],node2_coord[1],node2_coord[2]+1],node2_rotation[2])
										v_23[0] = rotatePointAboutAxis(v_23[0],node2_coord,[node2_coord[0]+1,node2_coord[1],node2_coord[2]],node2_rotation[0])
										v_23[0] = rotatePointAboutAxis(v_23[0],node2_coord,[node2_coord[0],node2_coord[1]+1,node2_coord[2]],node2_rotation[1])
										v_23[0] = rotatePointAboutAxis(v_23[0],node2_coord,[node2_coord[0],node2_coord[1],node2_coord[2]+1],node2_rotation[2])
										v_24[0] = rotatePointAboutAxis(v_24[0],node2_coord,[node2_coord[0]+1,node2_coord[1],node2_coord[2]],node2_rotation[0])
										v_24[0] = rotatePointAboutAxis(v_24[0],node2_coord,[node2_coord[0],node2_coord[1]+1,node2_coord[2]],node2_rotation[1])
										v_24[0] = rotatePointAboutAxis(v_24[0],node2_coord,[node2_coord[0],node2_coord[1],node2_coord[2]+1],node2_rotation[2])
										if iw != 0. or ih != 0.:
											v_15 = [[node1_coord[0]-y_vec[0]*ih-z_vec[0]*iw,
													 node1_coord[1]-y_vec[1]*ih-z_vec[1]*iw,
													 node1_coord[2]-y_vec[2]*ih-z_vec[2]*iw ], node1_color]
											v_16 = [[node1_coord[0]-y_vec[0]*ih+z_vec[0]*iw,
													 node1_coord[1]-y_vec[1]*ih+z_vec[1]*iw,
													 node1_coord[2]-y_vec[2]*ih+z_vec[2]*iw ], node1_color]
											v_17 = [[node1_coord[0]+y_vec[0]*ih+z_vec[0]*iw,
													 node1_coord[1]+y_vec[1]*ih+z_vec[1]*iw,
													 node1_coord[2]+y_vec[2]*ih+z_vec[2]*iw ], node1_color]
											v_18 = [[node1_coord[0]+y_vec[0]*ih-z_vec[0]*iw,
													 node1_coord[1]+y_vec[1]*ih-z_vec[1]*iw,
													 node1_coord[2]+y_vec[2]*ih-z_vec[2]*iw ], node1_color]
											v_25 = [[node2_coord[0]-y_vec[0]*ih-z_vec[0]*iw,
													 node2_coord[1]-y_vec[1]*ih-z_vec[1]*iw,
													 node2_coord[2]-y_vec[2]*ih-z_vec[2]*iw ], node2_color]
											v_26 = [[node2_coord[0]-y_vec[0]*ih+z_vec[0]*iw,
													 node2_coord[1]-y_vec[1]*ih+z_vec[1]*iw,
													 node2_coord[2]-y_vec[2]*ih+z_vec[2]*iw ], node2_color]
											v_27 = [[node2_coord[0]+y_vec[0]*ih+z_vec[0]*iw,
													 node2_coord[1]+y_vec[1]*ih+z_vec[1]*iw,
													 node2_coord[2]+y_vec[2]*ih+z_vec[2]*iw ], node2_color]
											v_28 = [[node2_coord[0]+y_vec[0]*ih-z_vec[0]*iw,
													 node2_coord[1]+y_vec[1]*ih-z_vec[1]*iw,
													 node2_coord[2]+y_vec[2]*ih-z_vec[2]*iw ], node2_color]
											v_15[0] = rotatePointAboutAxis(v_15[0],node1_coord,[node1_coord[0]+1,node1_coord[1],node1_coord[2]],node1_rotation[0])
											v_15[0] = rotatePointAboutAxis(v_15[0],node1_coord,[node1_coord[0],node1_coord[1]+1,node1_coord[2]],node1_rotation[1])
											v_15[0] = rotatePointAboutAxis(v_15[0],node1_coord,[node1_coord[0],node1_coord[1],node1_coord[2]+1],node1_rotation[2])
											v_16[0] = rotatePointAboutAxis(v_16[0],node1_coord,[node1_coord[0]+1,node1_coord[1],node1_coord[2]],node1_rotation[0])
											v_16[0] = rotatePointAboutAxis(v_16[0],node1_coord,[node1_coord[0],node1_coord[1]+1,node1_coord[2]],node1_rotation[1])
											v_16[0] = rotatePointAboutAxis(v_16[0],node1_coord,[node1_coord[0],node1_coord[1],node1_coord[2]+1],node1_rotation[2])
											v_17[0] = rotatePointAboutAxis(v_17[0],node1_coord,[node1_coord[0]+1,node1_coord[1],node1_coord[2]],node1_rotation[0])
											v_17[0] = rotatePointAboutAxis(v_17[0],node1_coord,[node1_coord[0],node1_coord[1]+1,node1_coord[2]],node1_rotation[1])
											v_17[0] = rotatePointAboutAxis(v_17[0],node1_coord,[node1_coord[0],node1_coord[1],node1_coord[2]+1],node1_rotation[2])
											v_18[0] = rotatePointAboutAxis(v_18[0],node1_coord,[node1_coord[0]+1,node1_coord[1],node1_coord[2]],node1_rotation[0])
											v_18[0] = rotatePointAboutAxis(v_18[0],node1_coord,[node1_coord[0],node1_coord[1]+1,node1_coord[2]],node1_rotation[1])
											v_18[0] = rotatePointAboutAxis(v_18[0],node1_coord,[node1_coord[0],node1_coord[1],node1_coord[2]+1],node1_rotation[2])
											v_25[0] = rotatePointAboutAxis(v_25[0],node2_coord,[node2_coord[0]+1,node2_coord[1],node2_coord[2]],node2_rotation[0])
											v_25[0] = rotatePointAboutAxis(v_25[0],node2_coord,[node2_coord[0],node2_coord[1]+1,node2_coord[2]],node2_rotation[1])
											v_25[0] = rotatePointAboutAxis(v_25[0],node2_coord,[node2_coord[0],node2_coord[1],node2_coord[2]+1],node2_rotation[2])
											v_26[0] = rotatePointAboutAxis(v_26[0],node2_coord,[node2_coord[0]+1,node2_coord[1],node2_coord[2]],node2_rotation[0])
											v_26[0] = rotatePointAboutAxis(v_26[0],node2_coord,[node2_coord[0],node2_coord[1]+1,node2_coord[2]],node2_rotation[1])
											v_26[0] = rotatePointAboutAxis(v_26[0],node2_coord,[node2_coord[0],node2_coord[1],node2_coord[2]+1],node2_rotation[2])
											v_27[0] = rotatePointAboutAxis(v_27[0],node2_coord,[node2_coord[0]+1,node2_coord[1],node2_coord[2]],node2_rotation[0])
											v_27[0] = rotatePointAboutAxis(v_27[0],node2_coord,[node2_coord[0],node2_coord[1]+1,node2_coord[2]],node2_rotation[1])
											v_27[0] = rotatePointAboutAxis(v_27[0],node2_coord,[node2_coord[0],node2_coord[1],node2_coord[2]+1],node2_rotation[2])
											v_28[0] = rotatePointAboutAxis(v_28[0],node2_coord,[node2_coord[0]+1,node2_coord[1],node2_coord[2]],node2_rotation[0])
											v_28[0] = rotatePointAboutAxis(v_28[0],node2_coord,[node2_coord[0],node2_coord[1]+1,node2_coord[2]],node2_rotation[1])
											v_28[0] = rotatePointAboutAxis(v_28[0],node2_coord,[node2_coord[0],node2_coord[1],node2_coord[2]+1],node2_rotation[2])

										lines = [[v_11,v_12],[v_12,v_13],[v_13,v_14],[v_14,v_11],
												 [v_21,v_22],[v_22,v_23],[v_23,v_24],[v_24,v_21],
												 [v_11,v_21],[v_12,v_22],[v_13,v_23],[v_14,v_24]]
										faces = [[v_13,v_12,v_22],[v_22,v_23,v_13],
												 [v_14,v_13,v_23],[v_23,v_24,v_14],
												 [v_11,v_14,v_24],[v_24,v_21,v_11],
												 [v_12,v_11,v_21],[v_21,v_22,v_12]]

										if iw == 0. or ih == 0.:
											faces += [[v_11,v_12,v_13],[v_13,v_14,v_11],
													  [v_21,v_24,v_23],[v_23,v_22,v_21]]
										else:
											lines += [[v_15,v_16],[v_16,v_17],[v_17,v_18],[v_18,v_15],
													  [v_25,v_26],[v_26,v_27],[v_27,v_28],[v_28,v_25],
													  [v_15,v_25],[v_16,v_26],[v_17,v_27],[v_18,v_28]]
											faces += [[v_15,v_11,v_12],[v_12,v_16,v_15],
													  [v_16,v_12,v_13],[v_13,v_17,v_16],
													  [v_17,v_13,v_14],[v_14,v_18,v_17],
													  [v_18,v_14,v_11],[v_11,v_15,v_18],
													  [v_26,v_22,v_21],[v_21,v_25,v_26],
													  [v_22,v_26,v_23],[v_26,v_27,v_23],
													  [v_23,v_27,v_24],[v_27,v_28,v_24],
													  [v_24,v_28,v_21],[v_25,v_21,v_28],
													  [v_17,v_27,v_16],[v_27,v_26,v_16],
													  [v_18,v_28,v_17],[v_28,v_27,v_17],
													  [v_15,v_25,v_18],[v_25,v_28,v_18],
													  [v_25,v_15,v_26],[v_15,v_16,v_26]]

									elif elements[j].crossSection['Type'] == 'Circle':

										r  = elements[j].crossSection['radius, r']
										ir  = elements[j].crossSection['inner radius, ir']
										vertices1 = []
										vertices2 = []
										pnts = 24
										for v in range(pnts):
											d = pnts/(v+1)
											vc = np.cos(2*np.pi/d)
											vs = np.sin(2*np.pi/d)
											vertices1.append([[node1_coord[0]+vs*y_vec[0]*r+vc*z_vec[0]*r,
															   node1_coord[1]+vs*y_vec[1]*r+vc*z_vec[1]*r,
															   node1_coord[2]+vs*y_vec[2]*r+vc*z_vec[2]*r ], node1_color])
											vertices1[v][0] = rotatePointAboutAxis(vertices1[v][0],node1_coord, \
																[node1_coord[0]+1,node1_coord[1],node1_coord[2]],node1_rotation[0])
											vertices1[v][0] = rotatePointAboutAxis(vertices1[v][0],node1_coord, \
																[node1_coord[0],node1_coord[1]+1,node1_coord[2]],node1_rotation[1])
											vertices1[v][0] = rotatePointAboutAxis(vertices1[v][0],node1_coord, \
																[node1_coord[0],node1_coord[1],node1_coord[2]+1],node1_rotation[2])
											vertices2.append([[node2_coord[0]+vs*y_vec[0]*r+vc*z_vec[0]*r,
															   node2_coord[1]+vs*y_vec[1]*r+vc*z_vec[1]*r,
															   node2_coord[2]+vs*y_vec[2]*r+vc*z_vec[2]*r ], node2_color])
											vertices2[v][0] = rotatePointAboutAxis(vertices2[v][0],node2_coord, \
																[node2_coord[0]+1,node2_coord[1],node2_coord[2]],node2_rotation[0])
											vertices2[v][0] = rotatePointAboutAxis(vertices2[v][0],node2_coord, \
																[node2_coord[0],node2_coord[1]+1,node2_coord[2]],node2_rotation[1])
											vertices2[v][0] = rotatePointAboutAxis(vertices2[v][0],node2_coord, \
																[node2_coord[0],node2_coord[1],node2_coord[2]+1],node2_rotation[2])
										if ir != 0.:
											ivertices1 = []
											ivertices2 = []
											for v in range(pnts):
												d = pnts/(v+1)
												vc = np.cos(2*np.pi/d)
												vs = np.sin(2*np.pi/d)
												ivertices1.append([[node1_coord[0]+vs*y_vec[0]*ir+vc*z_vec[0]*ir,
																    node1_coord[1]+vs*y_vec[1]*ir+vc*z_vec[1]*ir,
																    node1_coord[2]+vs*y_vec[2]*ir+vc*z_vec[2]*ir ], node1_color])
												ivertices1[v][0] = rotatePointAboutAxis(ivertices1[v][0],node1_coord, \
																[node1_coord[0]+1,node1_coord[1],node1_coord[2]],node1_rotation[0])
												ivertices1[v][0] = rotatePointAboutAxis(ivertices1[v][0],node1_coord, \
																[node1_coord[0],node1_coord[1]+1,node1_coord[2]],node1_rotation[1])
												ivertices1[v][0] = rotatePointAboutAxis(ivertices1[v][0],node1_coord, \
																[node1_coord[0],node1_coord[1],node1_coord[2]+1],node1_rotation[2])
												ivertices2.append([[node2_coord[0]+vs*y_vec[0]*ir+vc*z_vec[0]*ir,
																    node2_coord[1]+vs*y_vec[1]*ir+vc*z_vec[1]*ir,
																    node2_coord[2]+vs*y_vec[2]*ir+vc*z_vec[2]*ir ], node2_color])
												ivertices2[v][0] = rotatePointAboutAxis(ivertices2[v][0],node2_coord, \
																[node2_coord[0]+1,node2_coord[1],node2_coord[2]],node2_rotation[0])
												ivertices2[v][0] = rotatePointAboutAxis(ivertices2[v][0],node2_coord, \
																[node2_coord[0],node2_coord[1]+1,node2_coord[2]],node2_rotation[1])
												ivertices2[v][0] = rotatePointAboutAxis(ivertices2[v][0],node2_coord, \
																[node2_coord[0],node2_coord[1],node2_coord[2]+1],node2_rotation[2])

										lines = []
										faces = []
										for v in range(pnts):
											lines.append([vertices1[v-1],vertices1[v]])
											lines.append([vertices2[v-1],vertices2[v]])
										lines.append([vertices1[0],vertices2[0]])

										if ir != 0.:
											for v in range(pnts):
												lines.append([ivertices1[v-1],ivertices1[v]])
												lines.append([ivertices2[v-1],ivertices2[v]])
											lines.append([ivertices1[0],ivertices2[0]])
											for v in range(pnts-1):
												faces.append([ivertices1[v],vertices1[v],vertices1[v+1]])
												faces.append([vertices1[v+1],ivertices1[v+1],ivertices1[v]])
												faces.append([ivertices2[v],vertices2[v+1],vertices2[v]])
												faces.append([vertices2[v+1],ivertices2[v],ivertices2[v+1]])
												faces.append([vertices1[v],vertices2[v],vertices2[v+1]])
												faces.append([vertices2[v+1],vertices1[v+1],vertices1[v]])
												faces.append([ivertices1[v],ivertices1[v+1],ivertices2[v]])
												faces.append([ivertices1[v+1],ivertices2[v+1],ivertices2[v]])
											faces.append([ivertices1[-1],vertices1[-1],vertices1[0]])
											faces.append([vertices1[0],ivertices1[0],ivertices1[-1]])
											faces.append([ivertices2[-1],vertices2[0],vertices2[-1]])
											faces.append([vertices2[0],ivertices2[-1],ivertices2[0]])
											faces.append([vertices1[-1],vertices2[-1],vertices2[0]])
											faces.append([vertices2[0],vertices1[0],vertices1[-1]])
											faces.append([ivertices1[-1],ivertices1[0],ivertices2[-1]])
											faces.append([ivertices1[0],ivertices2[0],ivertices2[-1]])
													
										else:
											vertices1.append([[node1_coord[0],
															   node1_coord[1],
															   node1_coord[2] ], node1_color])
											vertices1[-1][0] = rotatePointAboutAxis(vertices1[-1][0],node1_coord, \
																[node1_coord[0]+1,node1_coord[1],node1_coord[2]],node1_rotation[0])
											vertices1[-1][0] = rotatePointAboutAxis(vertices1[-1][0],node1_coord, \
																[node1_coord[0],node1_coord[1]+1,node1_coord[2]],node1_rotation[1])
											vertices1[-1][0] = rotatePointAboutAxis(vertices1[-1][0],node1_coord, \
																[node1_coord[0],node1_coord[1],node1_coord[2]+1],node1_rotation[2])
											vertices2.append([[node2_coord[0],
															   node2_coord[1],
															   node2_coord[2] ], node2_color])
											vertices2[-1][0] = rotatePointAboutAxis(vertices2[-1][0],node2_coord, \
																[node2_coord[0]+1,node2_coord[1],node2_coord[2]],node2_rotation[0])
											vertices2[-1][0] = rotatePointAboutAxis(vertices2[-1][0],node2_coord, \
																[node2_coord[0],node2_coord[1]+1,node2_coord[2]],node2_rotation[1])
											vertices2[-1][0] = rotatePointAboutAxis(vertices2[-1][0],node2_coord, \
																[node2_coord[0],node2_coord[1],node2_coord[2]+1],node2_rotation[2])
											for v in range(pnts):
												faces.append([vertices1[-1],vertices1[v],vertices1[v+1]])
												faces.append([vertices2[-1],vertices2[v+1],vertices2[v]])
												faces.append([vertices1[v],vertices2[v],vertices2[v+1]])
												faces.append([vertices2[v+1],vertices1[v+1],vertices1[v]])
											faces.append([vertices1[-1],vertices1[-2],vertices1[0]])
											faces.append([vertices2[-1],vertices2[0],vertices2[-2]])
											faces.append([vertices1[-2],vertices2[-2],vertices2[0]])
											faces.append([vertices2[0],vertices1[0],vertices1[-2]])

									elif elements[j].crossSection['Type'] == 'L-Beam':

										bw = elements[j].crossSection['bottom width, bw']
										bt = elements[j].crossSection['bottom thickness, bt']
										st = elements[j].crossSection['side thickness, st']
										h  = elements[j].crossSection['height, h']
										A1  = st*(h-bt)
										A2  = bt*bw
										A   = A1+A2
										yC1 = (h/2.)+bt
										yC2 = bt/2.
										zC1 = st/2.
										zC2 = bw/2.
										if A != 0.:
											yC = (A1*yC1+A2*yC2)/A
											zC = (A1*zC1+A2*zC2)/A
										else:
											yC = 0.
											zC = 0.
										v_11  = [[node1_coord[0]-y_vec[0]*yC-z_vec[0]*zC,
												  node1_coord[1]-y_vec[1]*yC-z_vec[1]*zC,
												  node1_coord[2]-y_vec[2]*yC-z_vec[2]*zC ], node1_color]
										v_12  = [[node1_coord[0]-y_vec[0]*yC+z_vec[0]*(bw-zC),
												  node1_coord[1]-y_vec[1]*yC+z_vec[1]*(bw-zC),
												  node1_coord[2]-y_vec[2]*yC+z_vec[2]*(bw-zC) ], node1_color]
										v_13  = [[node1_coord[0]-y_vec[0]*(yC-bt)+z_vec[0]*(bw-zC),
												  node1_coord[1]-y_vec[1]*(yC-bt)+z_vec[1]*(bw-zC),
												  node1_coord[2]-y_vec[2]*(yC-bt)+z_vec[2]*(bw-zC) ], node1_color]
										v_14  = [[node1_coord[0]-y_vec[0]*(yC-bt)-z_vec[0]*(zC-st),
												  node1_coord[1]-y_vec[1]*(yC-bt)-z_vec[1]*(zC-st),
												  node1_coord[2]-y_vec[2]*(yC-bt)-z_vec[2]*(zC-st) ], node1_color]
										v_15  = [[node1_coord[0]+y_vec[0]*(h-yC)-z_vec[0]*(zC-st),
												  node1_coord[1]+y_vec[1]*(h-yC)-z_vec[1]*(zC-st),
												  node1_coord[2]+y_vec[2]*(h-yC)-z_vec[2]*(zC-st) ], node1_color]
										v_16  = [[node1_coord[0]+y_vec[0]*(h-yC)-z_vec[0]*zC,
												  node1_coord[1]+y_vec[1]*(h-yC)-z_vec[1]*zC,
												  node1_coord[2]+y_vec[2]*(h-yC)-z_vec[2]*zC ], node1_color]
										v_21  = [[node2_coord[0]-y_vec[0]*yC-z_vec[0]*zC,
												  node2_coord[1]-y_vec[1]*yC-z_vec[1]*zC,
												  node2_coord[2]-y_vec[2]*yC-z_vec[2]*zC ], node2_color]
										v_22  = [[node2_coord[0]-y_vec[0]*yC+z_vec[0]*(bw-zC),
												  node2_coord[1]-y_vec[1]*yC+z_vec[1]*(bw-zC),
												  node2_coord[2]-y_vec[2]*yC+z_vec[2]*(bw-zC) ], node2_color]
										v_23  = [[node2_coord[0]-y_vec[0]*(yC-bt)+z_vec[0]*(bw-zC),
												  node2_coord[1]-y_vec[1]*(yC-bt)+z_vec[1]*(bw-zC),
												  node2_coord[2]-y_vec[2]*(yC-bt)+z_vec[2]*(bw-zC) ], node2_color]
										v_24  = [[node2_coord[0]-y_vec[0]*(yC-bt)-z_vec[0]*(zC-st),
												  node2_coord[1]-y_vec[1]*(yC-bt)-z_vec[1]*(zC-st),
												  node2_coord[2]-y_vec[2]*(yC-bt)-z_vec[2]*(zC-st) ], node2_color]
										v_25  = [[node2_coord[0]+y_vec[0]*(h-yC)-z_vec[0]*(zC-st),
												  node2_coord[1]+y_vec[1]*(h-yC)-z_vec[1]*(zC-st),
												  node2_coord[2]+y_vec[2]*(h-yC)-z_vec[2]*(zC-st) ], node2_color]
										v_26  = [[node2_coord[0]+y_vec[0]*(h-yC)-z_vec[0]*zC,
												  node2_coord[1]+y_vec[1]*(h-yC)-z_vec[1]*zC,
												  node2_coord[2]+y_vec[2]*(h-yC)-z_vec[2]*zC ], node2_color]
										v_11[0] = rotatePointAboutAxis(v_11[0],node1_coord,[node1_coord[0]+1,node1_coord[1],node1_coord[2]],node1_rotation[0])
										v_11[0] = rotatePointAboutAxis(v_11[0],node1_coord,[node1_coord[0],node1_coord[1]+1,node1_coord[2]],node1_rotation[1])
										v_11[0] = rotatePointAboutAxis(v_11[0],node1_coord,[node1_coord[0],node1_coord[1],node1_coord[2]+1],node1_rotation[2])
										v_12[0] = rotatePointAboutAxis(v_12[0],node1_coord,[node1_coord[0]+1,node1_coord[1],node1_coord[2]],node1_rotation[0])
										v_12[0] = rotatePointAboutAxis(v_12[0],node1_coord,[node1_coord[0],node1_coord[1]+1,node1_coord[2]],node1_rotation[1])
										v_12[0] = rotatePointAboutAxis(v_12[0],node1_coord,[node1_coord[0],node1_coord[1],node1_coord[2]+1],node1_rotation[2])
										v_13[0] = rotatePointAboutAxis(v_13[0],node1_coord,[node1_coord[0]+1,node1_coord[1],node1_coord[2]],node1_rotation[0])
										v_13[0] = rotatePointAboutAxis(v_13[0],node1_coord,[node1_coord[0],node1_coord[1]+1,node1_coord[2]],node1_rotation[1])
										v_13[0] = rotatePointAboutAxis(v_13[0],node1_coord,[node1_coord[0],node1_coord[1],node1_coord[2]+1],node1_rotation[2])
										v_14[0] = rotatePointAboutAxis(v_14[0],node1_coord,[node1_coord[0]+1,node1_coord[1],node1_coord[2]],node1_rotation[0])
										v_14[0] = rotatePointAboutAxis(v_14[0],node1_coord,[node1_coord[0],node1_coord[1]+1,node1_coord[2]],node1_rotation[1])
										v_14[0] = rotatePointAboutAxis(v_14[0],node1_coord,[node1_coord[0],node1_coord[1],node1_coord[2]+1],node1_rotation[2])
										v_15[0] = rotatePointAboutAxis(v_15[0],node1_coord,[node1_coord[0]+1,node1_coord[1],node1_coord[2]],node1_rotation[0])
										v_15[0] = rotatePointAboutAxis(v_15[0],node1_coord,[node1_coord[0],node1_coord[1]+1,node1_coord[2]],node1_rotation[1])
										v_15[0] = rotatePointAboutAxis(v_15[0],node1_coord,[node1_coord[0],node1_coord[1],node1_coord[2]+1],node1_rotation[2])
										v_16[0] = rotatePointAboutAxis(v_16[0],node1_coord,[node1_coord[0]+1,node1_coord[1],node1_coord[2]],node1_rotation[0])
										v_16[0] = rotatePointAboutAxis(v_16[0],node1_coord,[node1_coord[0],node1_coord[1]+1,node1_coord[2]],node1_rotation[1])
										v_16[0] = rotatePointAboutAxis(v_16[0],node1_coord,[node1_coord[0],node1_coord[1],node1_coord[2]+1],node1_rotation[2])
										v_21[0] = rotatePointAboutAxis(v_21[0],node2_coord,[node2_coord[0]+1,node2_coord[1],node2_coord[2]],node2_rotation[0])
										v_21[0] = rotatePointAboutAxis(v_21[0],node2_coord,[node2_coord[0],node2_coord[1]+1,node2_coord[2]],node2_rotation[1])
										v_21[0] = rotatePointAboutAxis(v_21[0],node2_coord,[node2_coord[0],node2_coord[1],node2_coord[2]+1],node2_rotation[2])
										v_22[0] = rotatePointAboutAxis(v_22[0],node2_coord,[node2_coord[0]+1,node2_coord[1],node2_coord[2]],node2_rotation[0])
										v_22[0] = rotatePointAboutAxis(v_22[0],node2_coord,[node2_coord[0],node2_coord[1]+1,node2_coord[2]],node2_rotation[1])
										v_22[0] = rotatePointAboutAxis(v_22[0],node2_coord,[node2_coord[0],node2_coord[1],node2_coord[2]+1],node2_rotation[2])
										v_23[0] = rotatePointAboutAxis(v_23[0],node2_coord,[node2_coord[0]+1,node2_coord[1],node2_coord[2]],node2_rotation[0])
										v_23[0] = rotatePointAboutAxis(v_23[0],node2_coord,[node2_coord[0],node2_coord[1]+1,node2_coord[2]],node2_rotation[1])
										v_23[0] = rotatePointAboutAxis(v_23[0],node2_coord,[node2_coord[0],node2_coord[1],node2_coord[2]+1],node2_rotation[2])
										v_24[0] = rotatePointAboutAxis(v_24[0],node2_coord,[node2_coord[0]+1,node2_coord[1],node2_coord[2]],node2_rotation[0])
										v_24[0] = rotatePointAboutAxis(v_24[0],node2_coord,[node2_coord[0],node2_coord[1]+1,node2_coord[2]],node2_rotation[1])
										v_24[0] = rotatePointAboutAxis(v_24[0],node2_coord,[node2_coord[0],node2_coord[1],node2_coord[2]+1],node2_rotation[2])
										v_25[0] = rotatePointAboutAxis(v_25[0],node2_coord,[node2_coord[0]+1,node2_coord[1],node2_coord[2]],node2_rotation[0])
										v_25[0] = rotatePointAboutAxis(v_25[0],node2_coord,[node2_coord[0],node2_coord[1]+1,node2_coord[2]],node2_rotation[1])
										v_25[0] = rotatePointAboutAxis(v_25[0],node2_coord,[node2_coord[0],node2_coord[1],node2_coord[2]+1],node2_rotation[2])
										v_26[0] = rotatePointAboutAxis(v_26[0],node2_coord,[node2_coord[0]+1,node2_coord[1],node2_coord[2]],node2_rotation[0])
										v_26[0] = rotatePointAboutAxis(v_26[0],node2_coord,[node2_coord[0],node2_coord[1]+1,node2_coord[2]],node2_rotation[1])
										v_26[0] = rotatePointAboutAxis(v_26[0],node2_coord,[node2_coord[0],node2_coord[1],node2_coord[2]+1],node2_rotation[2])

										lines = [[v_11,v_12],[v_12,v_13],[v_13,v_14],[v_14,v_15],[v_15,v_16],[v_16,v_11],
												 [v_21,v_22],[v_22,v_23],[v_23,v_24],[v_24,v_25],[v_25,v_26],[v_26,v_21],
												 [v_11,v_21],[v_12,v_22],[v_13,v_23],[v_14,v_24],[v_15,v_25],[v_16,v_26]]
										faces = [[v_11,v_12,v_13],[v_13,v_14,v_11],
												 [v_11,v_14,v_16],[v_16,v_14,v_15],
												 [v_23,v_22,v_21],[v_21,v_24,v_23],
												 [v_24,v_21,v_26],[v_24,v_26,v_25],
												 [v_11,v_21,v_12],[v_12,v_21,v_22],
												 [v_11,v_16,v_26],[v_26,v_21,v_11],
												 [v_16,v_15,v_26],[v_26,v_15,v_25],
												 [v_13,v_12,v_22],[v_22,v_23,v_13],
												 [v_14,v_13,v_24],[v_24,v_13,v_23],
												 [v_14,v_24,v_25],[v_25,v_15,v_14]]

									elif elements[j].crossSection['Type'] == 'I-Beam':
										tw = elements[j].crossSection['top width, tw']
										tt = elements[j].crossSection['top thickness, tt']
										mt = elements[j].crossSection['middle thickness, mt']
										bw = elements[j].crossSection['bottom width, bw']
										bt = elements[j].crossSection['bottom thickness, bt']
										h  = elements[j].crossSection['height, h']
										tw = tw/2.
										tt = tt
										mt = mt/2.
										bw = bw/2.
										bt = bt
										h  = h/2.
										v_11  = [[node1_coord[0]-y_vec[0]*h-z_vec[0]*bw,
												  node1_coord[1]-y_vec[1]*h-z_vec[1]*bw,
												  node1_coord[2]-y_vec[2]*h-z_vec[2]*bw ], node1_color]
										v_12  = [[node1_coord[0]-y_vec[0]*h+z_vec[0]*bw,
												  node1_coord[1]-y_vec[1]*h+z_vec[1]*bw,
												  node1_coord[2]-y_vec[2]*h+z_vec[2]*bw ], node1_color]
										v_13  = [[node1_coord[0]-y_vec[0]*(h-bt)+z_vec[0]*bw,
												  node1_coord[1]-y_vec[1]*(h-bt)+z_vec[1]*bw,
												  node1_coord[2]-y_vec[2]*(h-bt)+z_vec[2]*bw ], node1_color]
										v_14  = [[node1_coord[0]-y_vec[0]*(h-bt)+z_vec[0]*mt,
												  node1_coord[1]-y_vec[1]*(h-bt)+z_vec[1]*mt,
												  node1_coord[2]-y_vec[2]*(h-bt)+z_vec[2]*mt ], node1_color]
										v_15  = [[node1_coord[0]-y_vec[0]*(h-bt)-z_vec[0]*mt,
												  node1_coord[1]-y_vec[1]*(h-bt)-z_vec[1]*mt,
												  node1_coord[2]-y_vec[2]*(h-bt)-z_vec[2]*mt ], node1_color]
										v_16  = [[node1_coord[0]-y_vec[0]*(h-bt)-z_vec[0]*bw,
												  node1_coord[1]-y_vec[1]*(h-bt)-z_vec[1]*bw,
												  node1_coord[2]-y_vec[2]*(h-bt)-z_vec[2]*bw ], node1_color]
										v_17  = [[node1_coord[0]+y_vec[0]*(h-tt)-z_vec[0]*tw,
												  node1_coord[1]+y_vec[1]*(h-tt)-z_vec[1]*tw,
												  node1_coord[2]+y_vec[2]*(h-tt)-z_vec[2]*tw ], node1_color]
										v_18  = [[node1_coord[0]+y_vec[0]*(h-tt)-z_vec[0]*mt,
												  node1_coord[1]+y_vec[1]*(h-tt)-z_vec[1]*mt,
												  node1_coord[2]+y_vec[2]*(h-tt)-z_vec[2]*mt ], node1_color]
										v_19  = [[node1_coord[0]+y_vec[0]*(h-tt)+z_vec[0]*mt,
												  node1_coord[1]+y_vec[1]*(h-tt)+z_vec[1]*mt,
												  node1_coord[2]+y_vec[2]*(h-tt)+z_vec[2]*mt ], node1_color]
										v_110 = [[node1_coord[0]+y_vec[0]*(h-tt)+z_vec[0]*tw,
												  node1_coord[1]+y_vec[1]*(h-tt)+z_vec[1]*tw,
												  node1_coord[2]+y_vec[2]*(h-tt)+z_vec[2]*tw ], node1_color]
										v_111 = [[node1_coord[0]+y_vec[0]*h+z_vec[0]*tw,
												  node1_coord[1]+y_vec[1]*h+z_vec[1]*tw,
												  node1_coord[2]+y_vec[2]*h+z_vec[2]*tw ], node1_color]
										v_112 = [[node1_coord[0]+y_vec[0]*h-z_vec[0]*tw,
												  node1_coord[1]+y_vec[1]*h-z_vec[1]*tw,
												  node1_coord[2]+y_vec[2]*h-z_vec[2]*tw ], node1_color]
										v_21  = [[node2_coord[0]-y_vec[0]*h-z_vec[0]*bw,
												  node2_coord[1]-y_vec[1]*h-z_vec[1]*bw,
												  node2_coord[2]-y_vec[2]*h-z_vec[2]*bw ], node2_color]
										v_22  = [[node2_coord[0]-y_vec[0]*h+z_vec[0]*bw,
												  node2_coord[1]-y_vec[1]*h+z_vec[1]*bw,
												  node2_coord[2]-y_vec[2]*h+z_vec[2]*bw ], node2_color]
										v_23  = [[node2_coord[0]-y_vec[0]*(h-bt)+z_vec[0]*bw,
												  node2_coord[1]-y_vec[1]*(h-bt)+z_vec[1]*bw,
												  node2_coord[2]-y_vec[2]*(h-bt)+z_vec[2]*bw ], node2_color]
										v_24  = [[node2_coord[0]-y_vec[0]*(h-bt)+z_vec[0]*mt,
												  node2_coord[1]-y_vec[1]*(h-bt)+z_vec[1]*mt,
												  node2_coord[2]-y_vec[2]*(h-bt)+z_vec[2]*mt ], node2_color]
										v_25  = [[node2_coord[0]-y_vec[0]*(h-bt)-z_vec[0]*mt,
												  node2_coord[1]-y_vec[1]*(h-bt)-z_vec[1]*mt,
												  node2_coord[2]-y_vec[2]*(h-bt)-z_vec[2]*mt ], node2_color]
										v_26  = [[node2_coord[0]-y_vec[0]*(h-bt)-z_vec[0]*bw,
												  node2_coord[1]-y_vec[1]*(h-bt)-z_vec[1]*bw,
												  node2_coord[2]-y_vec[2]*(h-bt)-z_vec[2]*bw ], node2_color]
										v_27  = [[node2_coord[0]+y_vec[0]*(h-tt)-z_vec[0]*tw,
												  node2_coord[1]+y_vec[1]*(h-tt)-z_vec[1]*tw,
												  node2_coord[2]+y_vec[2]*(h-tt)-z_vec[2]*tw ], node2_color]
										v_28  = [[node2_coord[0]+y_vec[0]*(h-tt)-z_vec[0]*mt,
												  node2_coord[1]+y_vec[1]*(h-tt)-z_vec[1]*mt,
												  node2_coord[2]+y_vec[2]*(h-tt)-z_vec[2]*mt ], node2_color]
										v_29  = [[node2_coord[0]+y_vec[0]*(h-tt)+z_vec[0]*mt,
												  node2_coord[1]+y_vec[1]*(h-tt)+z_vec[1]*mt,
												  node2_coord[2]+y_vec[2]*(h-tt)+z_vec[2]*mt ], node2_color]
										v_210 = [[node2_coord[0]+y_vec[0]*(h-tt)+z_vec[0]*tw,
												  node2_coord[1]+y_vec[1]*(h-tt)+z_vec[1]*tw,
												  node2_coord[2]+y_vec[2]*(h-tt)+z_vec[2]*tw ], node2_color]
										v_211 = [[node2_coord[0]+y_vec[0]*h+z_vec[0]*tw,
												  node2_coord[1]+y_vec[1]*h+z_vec[1]*tw,
												  node2_coord[2]+y_vec[2]*h+z_vec[2]*tw ], node2_color]
										v_212 = [[node2_coord[0]+y_vec[0]*h-z_vec[0]*tw,
												  node2_coord[1]+y_vec[1]*h-z_vec[1]*tw,
												  node2_coord[2]+y_vec[2]*h-z_vec[2]*tw ], node2_color]
										v_11[0] = rotatePointAboutAxis(v_11[0],node1_coord,[node1_coord[0]+1,node1_coord[1],node1_coord[2]],node1_rotation[0])
										v_11[0] = rotatePointAboutAxis(v_11[0],node1_coord,[node1_coord[0],node1_coord[1]+1,node1_coord[2]],node1_rotation[1])
										v_11[0] = rotatePointAboutAxis(v_11[0],node1_coord,[node1_coord[0],node1_coord[1],node1_coord[2]+1],node1_rotation[2])
										v_12[0] = rotatePointAboutAxis(v_12[0],node1_coord,[node1_coord[0]+1,node1_coord[1],node1_coord[2]],node1_rotation[0])
										v_12[0] = rotatePointAboutAxis(v_12[0],node1_coord,[node1_coord[0],node1_coord[1]+1,node1_coord[2]],node1_rotation[1])
										v_12[0] = rotatePointAboutAxis(v_12[0],node1_coord,[node1_coord[0],node1_coord[1],node1_coord[2]+1],node1_rotation[2])
										v_13[0] = rotatePointAboutAxis(v_13[0],node1_coord,[node1_coord[0]+1,node1_coord[1],node1_coord[2]],node1_rotation[0])
										v_13[0] = rotatePointAboutAxis(v_13[0],node1_coord,[node1_coord[0],node1_coord[1]+1,node1_coord[2]],node1_rotation[1])
										v_13[0] = rotatePointAboutAxis(v_13[0],node1_coord,[node1_coord[0],node1_coord[1],node1_coord[2]+1],node1_rotation[2])
										v_14[0] = rotatePointAboutAxis(v_14[0],node1_coord,[node1_coord[0]+1,node1_coord[1],node1_coord[2]],node1_rotation[0])
										v_14[0] = rotatePointAboutAxis(v_14[0],node1_coord,[node1_coord[0],node1_coord[1]+1,node1_coord[2]],node1_rotation[1])
										v_14[0] = rotatePointAboutAxis(v_14[0],node1_coord,[node1_coord[0],node1_coord[1],node1_coord[2]+1],node1_rotation[2])
										v_15[0] = rotatePointAboutAxis(v_15[0],node1_coord,[node1_coord[0]+1,node1_coord[1],node1_coord[2]],node1_rotation[0])
										v_15[0] = rotatePointAboutAxis(v_15[0],node1_coord,[node1_coord[0],node1_coord[1]+1,node1_coord[2]],node1_rotation[1])
										v_15[0] = rotatePointAboutAxis(v_15[0],node1_coord,[node1_coord[0],node1_coord[1],node1_coord[2]+1],node1_rotation[2])
										v_16[0] = rotatePointAboutAxis(v_16[0],node1_coord,[node1_coord[0]+1,node1_coord[1],node1_coord[2]],node1_rotation[0])
										v_16[0] = rotatePointAboutAxis(v_16[0],node1_coord,[node1_coord[0],node1_coord[1]+1,node1_coord[2]],node1_rotation[1])
										v_16[0] = rotatePointAboutAxis(v_16[0],node1_coord,[node1_coord[0],node1_coord[1],node1_coord[2]+1],node1_rotation[2])
										v_17[0] = rotatePointAboutAxis(v_17[0],node1_coord,[node1_coord[0]+1,node1_coord[1],node1_coord[2]],node1_rotation[0])
										v_17[0] = rotatePointAboutAxis(v_17[0],node1_coord,[node1_coord[0],node1_coord[1]+1,node1_coord[2]],node1_rotation[1])
										v_17[0] = rotatePointAboutAxis(v_17[0],node1_coord,[node1_coord[0],node1_coord[1],node1_coord[2]+1],node1_rotation[2])
										v_18[0] = rotatePointAboutAxis(v_18[0],node1_coord,[node1_coord[0]+1,node1_coord[1],node1_coord[2]],node1_rotation[0])
										v_18[0] = rotatePointAboutAxis(v_18[0],node1_coord,[node1_coord[0],node1_coord[1]+1,node1_coord[2]],node1_rotation[1])
										v_18[0] = rotatePointAboutAxis(v_18[0],node1_coord,[node1_coord[0],node1_coord[1],node1_coord[2]+1],node1_rotation[2])
										v_19[0] = rotatePointAboutAxis(v_19[0],node1_coord,[node1_coord[0]+1,node1_coord[1],node1_coord[2]],node1_rotation[0])
										v_19[0] = rotatePointAboutAxis(v_19[0],node1_coord,[node1_coord[0],node1_coord[1]+1,node1_coord[2]],node1_rotation[1])
										v_19[0] = rotatePointAboutAxis(v_19[0],node1_coord,[node1_coord[0],node1_coord[1],node1_coord[2]+1],node1_rotation[2])
										v_110[0] = rotatePointAboutAxis(v_110[0],node1_coord,[node1_coord[0]+1,node1_coord[1],node1_coord[2]],node1_rotation[0])
										v_110[0] = rotatePointAboutAxis(v_110[0],node1_coord,[node1_coord[0],node1_coord[1]+1,node1_coord[2]],node1_rotation[1])
										v_110[0] = rotatePointAboutAxis(v_110[0],node1_coord,[node1_coord[0],node1_coord[1],node1_coord[2]+1],node1_rotation[2])
										v_111[0] = rotatePointAboutAxis(v_111[0],node1_coord,[node1_coord[0]+1,node1_coord[1],node1_coord[2]],node1_rotation[0])
										v_111[0] = rotatePointAboutAxis(v_111[0],node1_coord,[node1_coord[0],node1_coord[1]+1,node1_coord[2]],node1_rotation[1])
										v_111[0] = rotatePointAboutAxis(v_111[0],node1_coord,[node1_coord[0],node1_coord[1],node1_coord[2]+1],node1_rotation[2])
										v_112[0] = rotatePointAboutAxis(v_112[0],node1_coord,[node1_coord[0]+1,node1_coord[1],node1_coord[2]],node1_rotation[0])
										v_112[0] = rotatePointAboutAxis(v_112[0],node1_coord,[node1_coord[0],node1_coord[1]+1,node1_coord[2]],node1_rotation[1])
										v_112[0] = rotatePointAboutAxis(v_112[0],node1_coord,[node1_coord[0],node1_coord[1],node1_coord[2]+1],node1_rotation[2])
										v_21[0] = rotatePointAboutAxis(v_21[0],node2_coord,[node2_coord[0]+1,node2_coord[1],node2_coord[2]],node2_rotation[0])
										v_21[0] = rotatePointAboutAxis(v_21[0],node2_coord,[node2_coord[0],node2_coord[1]+1,node2_coord[2]],node2_rotation[1])
										v_21[0] = rotatePointAboutAxis(v_21[0],node2_coord,[node2_coord[0],node2_coord[1],node2_coord[2]+1],node2_rotation[2])
										v_22[0] = rotatePointAboutAxis(v_22[0],node2_coord,[node2_coord[0]+1,node2_coord[1],node2_coord[2]],node2_rotation[0])
										v_22[0] = rotatePointAboutAxis(v_22[0],node2_coord,[node2_coord[0],node2_coord[1]+1,node2_coord[2]],node2_rotation[1])
										v_22[0] = rotatePointAboutAxis(v_22[0],node2_coord,[node2_coord[0],node2_coord[1],node2_coord[2]+1],node2_rotation[2])
										v_23[0] = rotatePointAboutAxis(v_23[0],node2_coord,[node2_coord[0]+1,node2_coord[1],node2_coord[2]],node2_rotation[0])
										v_23[0] = rotatePointAboutAxis(v_23[0],node2_coord,[node2_coord[0],node2_coord[1]+1,node2_coord[2]],node2_rotation[1])
										v_23[0] = rotatePointAboutAxis(v_23[0],node2_coord,[node2_coord[0],node2_coord[1],node2_coord[2]+1],node2_rotation[2])
										v_24[0] = rotatePointAboutAxis(v_24[0],node2_coord,[node2_coord[0]+1,node2_coord[1],node2_coord[2]],node2_rotation[0])
										v_24[0] = rotatePointAboutAxis(v_24[0],node2_coord,[node2_coord[0],node2_coord[1]+1,node2_coord[2]],node2_rotation[1])
										v_24[0] = rotatePointAboutAxis(v_24[0],node2_coord,[node2_coord[0],node2_coord[1],node2_coord[2]+1],node2_rotation[2])
										v_25[0] = rotatePointAboutAxis(v_25[0],node2_coord,[node2_coord[0]+1,node2_coord[1],node2_coord[2]],node2_rotation[0])
										v_25[0] = rotatePointAboutAxis(v_25[0],node2_coord,[node2_coord[0],node2_coord[1]+1,node2_coord[2]],node2_rotation[1])
										v_25[0] = rotatePointAboutAxis(v_25[0],node2_coord,[node2_coord[0],node2_coord[1],node2_coord[2]+1],node2_rotation[2])
										v_26[0] = rotatePointAboutAxis(v_26[0],node2_coord,[node2_coord[0]+1,node2_coord[1],node2_coord[2]],node2_rotation[0])
										v_26[0] = rotatePointAboutAxis(v_26[0],node2_coord,[node2_coord[0],node2_coord[1]+1,node2_coord[2]],node2_rotation[1])
										v_26[0] = rotatePointAboutAxis(v_26[0],node2_coord,[node2_coord[0],node2_coord[1],node2_coord[2]+1],node2_rotation[2])
										v_27[0] = rotatePointAboutAxis(v_27[0],node2_coord,[node2_coord[0]+1,node2_coord[1],node2_coord[2]],node2_rotation[0])
										v_27[0] = rotatePointAboutAxis(v_27[0],node2_coord,[node2_coord[0],node2_coord[1]+1,node2_coord[2]],node2_rotation[1])
										v_27[0] = rotatePointAboutAxis(v_27[0],node2_coord,[node2_coord[0],node2_coord[1],node2_coord[2]+1],node2_rotation[2])
										v_28[0] = rotatePointAboutAxis(v_28[0],node2_coord,[node2_coord[0]+1,node2_coord[1],node2_coord[2]],node2_rotation[0])
										v_28[0] = rotatePointAboutAxis(v_28[0],node2_coord,[node2_coord[0],node2_coord[1]+1,node2_coord[2]],node2_rotation[1])
										v_28[0] = rotatePointAboutAxis(v_28[0],node2_coord,[node2_coord[0],node2_coord[1],node2_coord[2]+1],node2_rotation[2])
										v_29[0] = rotatePointAboutAxis(v_29[0],node2_coord,[node2_coord[0]+1,node2_coord[1],node2_coord[2]],node2_rotation[0])
										v_29[0] = rotatePointAboutAxis(v_29[0],node2_coord,[node2_coord[0],node2_coord[1]+1,node2_coord[2]],node2_rotation[1])
										v_29[0] = rotatePointAboutAxis(v_29[0],node2_coord,[node2_coord[0],node2_coord[1],node2_coord[2]+1],node2_rotation[2])
										v_210[0] = rotatePointAboutAxis(v_210[0],node2_coord,[node2_coord[0]+1,node2_coord[1],node2_coord[2]],node2_rotation[0])
										v_210[0] = rotatePointAboutAxis(v_210[0],node2_coord,[node2_coord[0],node2_coord[1]+1,node2_coord[2]],node2_rotation[1])
										v_210[0] = rotatePointAboutAxis(v_210[0],node2_coord,[node2_coord[0],node2_coord[1],node2_coord[2]+1],node2_rotation[2])
										v_211[0] = rotatePointAboutAxis(v_211[0],node2_coord,[node2_coord[0]+1,node2_coord[1],node2_coord[2]],node2_rotation[0])
										v_211[0] = rotatePointAboutAxis(v_211[0],node2_coord,[node2_coord[0],node2_coord[1]+1,node2_coord[2]],node2_rotation[1])
										v_211[0] = rotatePointAboutAxis(v_211[0],node2_coord,[node2_coord[0],node2_coord[1],node2_coord[2]+1],node2_rotation[2])
										v_212[0] = rotatePointAboutAxis(v_212[0],node2_coord,[node2_coord[0]+1,node2_coord[1],node2_coord[2]],node2_rotation[0])
										v_212[0] = rotatePointAboutAxis(v_212[0],node2_coord,[node2_coord[0],node2_coord[1]+1,node2_coord[2]],node2_rotation[1])
										v_212[0] = rotatePointAboutAxis(v_212[0],node2_coord,[node2_coord[0],node2_coord[1],node2_coord[2]+1],node2_rotation[2])

										lines = [[v_11,v_12],[v_12,v_13],[v_13,v_14],[v_14,v_19],
												 [v_19,v_110],[v_110,v_111],[v_111,v_112],[v_112,v_17],
												 [v_17,v_18],[v_18,v_15],[v_15,v_16],[v_16,v_11],
												 [v_21,v_22],[v_22,v_23],[v_23,v_24],[v_24,v_29],
												 [v_29,v_210],[v_210,v_211],[v_211,v_212],[v_212,v_27],
												 [v_27,v_28],[v_28,v_25],[v_25,v_26],[v_26,v_21],
												 [v_11,v_21],[v_12,v_22],[v_13,v_23],[v_14,v_24],
												 [v_15,v_25],[v_16,v_26],[v_17,v_27],[v_18,v_28],
												 [v_19,v_29],[v_110,v_210],[v_111,v_211],[v_112,v_212]]
										faces = [[v_11,v_12,v_13],[v_13,v_16,v_11],
												 [v_15,v_14,v_19],[v_19,v_18,v_15],
												 [v_112,v_17,v_110],[v_110,v_111,v_112],
												 [v_23,v_22,v_21],[v_21,v_26,v_23],
												 [v_29,v_24,v_25],[v_25,v_28,v_29],
												 [v_210,v_27,v_212],[v_212,v_211,v_210],
												 [v_19,v_14,v_24],[v_24,v_29,v_19],
												 [v_15,v_18,v_28],[v_28,v_25,v_15],
												 [v_13,v_12,v_22],[v_22,v_23,v_13],
												 [v_11,v_16,v_26],[v_26,v_21,v_11],
												 [v_111,v_110,v_210],[v_210,v_211,v_111],
												 [v_17,v_112,v_212],[v_212,v_27,v_17],
												 [v_11,v_21,v_12],[v_21,v_22,v_12],
												 [v_112,v_111,v_212],[v_212,v_111,v_211],
												 [v_14,v_13,v_24],[v_24,v_13,v_23],
												 [v_16,v_15,v_26],[v_26,v_15,v_25],
												 [v_18,v_17,v_27],[v_27,v_28,v_18],
												 [v_110,v_19,v_29],[v_29,v_210,v_110]]

									elif elements[j].crossSection['Type'] == 'C-Beam':
										tw = elements[j].crossSection['top width, tw']
										tt = elements[j].crossSection['top thickness, tt']
										mt = elements[j].crossSection['middle thickness, mt']
										bw = elements[j].crossSection['bottom width, bw']
										bt = elements[j].crossSection['bottom thickness, bt']
										h  = elements[j].crossSection['height, h']
										A1  = tt*tw
										A2  = mt*(h-tt-bt)
										A3  = bt*bw
										A   = A1+A2+A3
										zC1 = tw/2.
										zC2 = mt/2.
										zC3 = bw/2.
										yC1 = h-(tt/2.)
										yC2 = (h-tt)/2.
										yC3 = bt/2.
										if A != 0.:
											zC = (A1*zC1+A2*zC2+A3*zC3)/A
											yC = (A1*yC1+A2*yC2+A3*yC3)/A
										else:
											zC = 0.
											yC = 0.
										v_11  = [[node1_coord[0]-y_vec[0]*yC-z_vec[0]*zC,
												  node1_coord[1]-y_vec[1]*yC-z_vec[1]*zC,
												  node1_coord[2]-y_vec[2]*yC-z_vec[2]*zC ], node1_color]
										v_12  = [[node1_coord[0]-y_vec[0]*yC+z_vec[0]*(bw-zC),
												  node1_coord[1]-y_vec[1]*yC+z_vec[1]*(bw-zC),
												  node1_coord[2]-y_vec[2]*yC+z_vec[2]*(bw-zC) ], node1_color]
										v_13  = [[node1_coord[0]-y_vec[0]*(yC-bt)+z_vec[0]*(bw-zC),
												  node1_coord[1]-y_vec[1]*(yC-bt)+z_vec[1]*(bw-zC),
												  node1_coord[2]-y_vec[2]*(yC-bt)+z_vec[2]*(bw-zC) ], node1_color]
										v_14  = [[node1_coord[0]-y_vec[0]*(yC-bt)-z_vec[0]*(zC-mt),
												  node1_coord[1]-y_vec[1]*(yC-bt)-z_vec[1]*(zC-mt),
												  node1_coord[2]-y_vec[2]*(yC-bt)-z_vec[2]*(zC-mt) ], node1_color]
										v_15  = [[node1_coord[0]+y_vec[0]*(h-yC-tt)-z_vec[0]*(zC-mt),
												  node1_coord[1]+y_vec[1]*(h-yC-tt)-z_vec[1]*(zC-mt),
												  node1_coord[2]+y_vec[2]*(h-yC-tt)-z_vec[2]*(zC-mt) ], node1_color]
										v_16  = [[node1_coord[0]+y_vec[0]*(h-yC-tt)+z_vec[0]*(tw-zC),
												  node1_coord[1]+y_vec[1]*(h-yC-tt)+z_vec[1]*(tw-zC),
												  node1_coord[2]+y_vec[2]*(h-yC-tt)+z_vec[2]*(tw-zC) ], node1_color]
										v_17  = [[node1_coord[0]+y_vec[0]*(h-yC)+z_vec[0]*(tw-zC),
												  node1_coord[1]+y_vec[1]*(h-yC)+z_vec[1]*(tw-zC),
												  node1_coord[2]+y_vec[2]*(h-yC)+z_vec[2]*(tw-zC) ], node1_color]
										v_18  = [[node1_coord[0]+y_vec[0]*(h-yC)-z_vec[0]*zC,
												  node1_coord[1]+y_vec[1]*(h-yC)-z_vec[1]*zC,
												  node1_coord[2]+y_vec[2]*(h-yC)-z_vec[2]*zC ], node1_color]
										v_21  = [[node2_coord[0]-y_vec[0]*yC-z_vec[0]*zC,
												  node2_coord[1]-y_vec[1]*yC-z_vec[1]*zC,
												  node2_coord[2]-y_vec[2]*yC-z_vec[2]*zC ], node2_color]
										v_22  = [[node2_coord[0]-y_vec[0]*yC+z_vec[0]*(bw-zC),
												  node2_coord[1]-y_vec[1]*yC+z_vec[1]*(bw-zC),
												  node2_coord[2]-y_vec[2]*yC+z_vec[2]*(bw-zC) ], node2_color]
										v_23  = [[node2_coord[0]-y_vec[0]*(yC-bt)+z_vec[0]*(bw-zC),
												  node2_coord[1]-y_vec[1]*(yC-bt)+z_vec[1]*(bw-zC),
												  node2_coord[2]-y_vec[2]*(yC-bt)+z_vec[2]*(bw-zC) ], node2_color]
										v_24  = [[node2_coord[0]-y_vec[0]*(yC-bt)-z_vec[0]*(zC-mt),
												  node2_coord[1]-y_vec[1]*(yC-bt)-z_vec[1]*(zC-mt),
												  node2_coord[2]-y_vec[2]*(yC-bt)-z_vec[2]*(zC-mt) ], node2_color]
										v_25  = [[node2_coord[0]+y_vec[0]*(h-yC-tt)-z_vec[0]*(zC-mt),
												  node2_coord[1]+y_vec[1]*(h-yC-tt)-z_vec[1]*(zC-mt),
												  node2_coord[2]+y_vec[2]*(h-yC-tt)-z_vec[2]*(zC-mt) ], node2_color]
										v_26  = [[node2_coord[0]+y_vec[0]*(h-yC-tt)+z_vec[0]*(tw-zC),
												  node2_coord[1]+y_vec[1]*(h-yC-tt)+z_vec[1]*(tw-zC),
												  node2_coord[2]+y_vec[2]*(h-yC-tt)+z_vec[2]*(tw-zC) ], node2_color]
										v_27  = [[node2_coord[0]+y_vec[0]*(h-yC)+z_vec[0]*(tw-zC),
												  node2_coord[1]+y_vec[1]*(h-yC)+z_vec[1]*(tw-zC),
												  node2_coord[2]+y_vec[2]*(h-yC)+z_vec[2]*(tw-zC) ], node2_color]
										v_28  = [[node2_coord[0]+y_vec[0]*(h-yC)-z_vec[0]*zC,
												  node2_coord[1]+y_vec[1]*(h-yC)-z_vec[1]*zC,
												  node2_coord[2]+y_vec[2]*(h-yC)-z_vec[2]*zC ], node2_color]
										v_11[0] = rotatePointAboutAxis(v_11[0],node1_coord,[node1_coord[0]+1,node1_coord[1],node1_coord[2]],node1_rotation[0])
										v_11[0] = rotatePointAboutAxis(v_11[0],node1_coord,[node1_coord[0],node1_coord[1]+1,node1_coord[2]],node1_rotation[1])
										v_11[0] = rotatePointAboutAxis(v_11[0],node1_coord,[node1_coord[0],node1_coord[1],node1_coord[2]+1],node1_rotation[2])
										v_12[0] = rotatePointAboutAxis(v_12[0],node1_coord,[node1_coord[0]+1,node1_coord[1],node1_coord[2]],node1_rotation[0])
										v_12[0] = rotatePointAboutAxis(v_12[0],node1_coord,[node1_coord[0],node1_coord[1]+1,node1_coord[2]],node1_rotation[1])
										v_12[0] = rotatePointAboutAxis(v_12[0],node1_coord,[node1_coord[0],node1_coord[1],node1_coord[2]+1],node1_rotation[2])
										v_13[0] = rotatePointAboutAxis(v_13[0],node1_coord,[node1_coord[0]+1,node1_coord[1],node1_coord[2]],node1_rotation[0])
										v_13[0] = rotatePointAboutAxis(v_13[0],node1_coord,[node1_coord[0],node1_coord[1]+1,node1_coord[2]],node1_rotation[1])
										v_13[0] = rotatePointAboutAxis(v_13[0],node1_coord,[node1_coord[0],node1_coord[1],node1_coord[2]+1],node1_rotation[2])
										v_14[0] = rotatePointAboutAxis(v_14[0],node1_coord,[node1_coord[0]+1,node1_coord[1],node1_coord[2]],node1_rotation[0])
										v_14[0] = rotatePointAboutAxis(v_14[0],node1_coord,[node1_coord[0],node1_coord[1]+1,node1_coord[2]],node1_rotation[1])
										v_14[0] = rotatePointAboutAxis(v_14[0],node1_coord,[node1_coord[0],node1_coord[1],node1_coord[2]+1],node1_rotation[2])
										v_15[0] = rotatePointAboutAxis(v_15[0],node1_coord,[node1_coord[0]+1,node1_coord[1],node1_coord[2]],node1_rotation[0])
										v_15[0] = rotatePointAboutAxis(v_15[0],node1_coord,[node1_coord[0],node1_coord[1]+1,node1_coord[2]],node1_rotation[1])
										v_15[0] = rotatePointAboutAxis(v_15[0],node1_coord,[node1_coord[0],node1_coord[1],node1_coord[2]+1],node1_rotation[2])
										v_16[0] = rotatePointAboutAxis(v_16[0],node1_coord,[node1_coord[0]+1,node1_coord[1],node1_coord[2]],node1_rotation[0])
										v_16[0] = rotatePointAboutAxis(v_16[0],node1_coord,[node1_coord[0],node1_coord[1]+1,node1_coord[2]],node1_rotation[1])
										v_16[0] = rotatePointAboutAxis(v_16[0],node1_coord,[node1_coord[0],node1_coord[1],node1_coord[2]+1],node1_rotation[2])
										v_17[0] = rotatePointAboutAxis(v_17[0],node1_coord,[node1_coord[0]+1,node1_coord[1],node1_coord[2]],node1_rotation[0])
										v_17[0] = rotatePointAboutAxis(v_17[0],node1_coord,[node1_coord[0],node1_coord[1]+1,node1_coord[2]],node1_rotation[1])
										v_17[0] = rotatePointAboutAxis(v_17[0],node1_coord,[node1_coord[0],node1_coord[1],node1_coord[2]+1],node1_rotation[2])
										v_18[0] = rotatePointAboutAxis(v_18[0],node1_coord,[node1_coord[0]+1,node1_coord[1],node1_coord[2]],node1_rotation[0])
										v_18[0] = rotatePointAboutAxis(v_18[0],node1_coord,[node1_coord[0],node1_coord[1]+1,node1_coord[2]],node1_rotation[1])
										v_18[0] = rotatePointAboutAxis(v_18[0],node1_coord,[node1_coord[0],node1_coord[1],node1_coord[2]+1],node1_rotation[2])
										v_21[0] = rotatePointAboutAxis(v_21[0],node2_coord,[node2_coord[0]+1,node2_coord[1],node2_coord[2]],node2_rotation[0])
										v_21[0] = rotatePointAboutAxis(v_21[0],node2_coord,[node2_coord[0],node2_coord[1]+1,node2_coord[2]],node2_rotation[1])
										v_21[0] = rotatePointAboutAxis(v_21[0],node2_coord,[node2_coord[0],node2_coord[1],node2_coord[2]+1],node2_rotation[2])
										v_22[0] = rotatePointAboutAxis(v_22[0],node2_coord,[node2_coord[0]+1,node2_coord[1],node2_coord[2]],node2_rotation[0])
										v_22[0] = rotatePointAboutAxis(v_22[0],node2_coord,[node2_coord[0],node2_coord[1]+1,node2_coord[2]],node2_rotation[1])
										v_22[0] = rotatePointAboutAxis(v_22[0],node2_coord,[node2_coord[0],node2_coord[1],node2_coord[2]+1],node2_rotation[2])
										v_23[0] = rotatePointAboutAxis(v_23[0],node2_coord,[node2_coord[0]+1,node2_coord[1],node2_coord[2]],node2_rotation[0])
										v_23[0] = rotatePointAboutAxis(v_23[0],node2_coord,[node2_coord[0],node2_coord[1]+1,node2_coord[2]],node2_rotation[1])
										v_23[0] = rotatePointAboutAxis(v_23[0],node2_coord,[node2_coord[0],node2_coord[1],node2_coord[2]+1],node2_rotation[2])
										v_24[0] = rotatePointAboutAxis(v_24[0],node2_coord,[node2_coord[0]+1,node2_coord[1],node2_coord[2]],node2_rotation[0])
										v_24[0] = rotatePointAboutAxis(v_24[0],node2_coord,[node2_coord[0],node2_coord[1]+1,node2_coord[2]],node2_rotation[1])
										v_24[0] = rotatePointAboutAxis(v_24[0],node2_coord,[node2_coord[0],node2_coord[1],node2_coord[2]+1],node2_rotation[2])
										v_25[0] = rotatePointAboutAxis(v_25[0],node2_coord,[node2_coord[0]+1,node2_coord[1],node2_coord[2]],node2_rotation[0])
										v_25[0] = rotatePointAboutAxis(v_25[0],node2_coord,[node2_coord[0],node2_coord[1]+1,node2_coord[2]],node2_rotation[1])
										v_25[0] = rotatePointAboutAxis(v_25[0],node2_coord,[node2_coord[0],node2_coord[1],node2_coord[2]+1],node2_rotation[2])
										v_26[0] = rotatePointAboutAxis(v_26[0],node2_coord,[node2_coord[0]+1,node2_coord[1],node2_coord[2]],node2_rotation[0])
										v_26[0] = rotatePointAboutAxis(v_26[0],node2_coord,[node2_coord[0],node2_coord[1]+1,node2_coord[2]],node2_rotation[1])
										v_26[0] = rotatePointAboutAxis(v_26[0],node2_coord,[node2_coord[0],node2_coord[1],node2_coord[2]+1],node2_rotation[2])
										v_27[0] = rotatePointAboutAxis(v_27[0],node2_coord,[node2_coord[0]+1,node2_coord[1],node2_coord[2]],node2_rotation[0])
										v_27[0] = rotatePointAboutAxis(v_27[0],node2_coord,[node2_coord[0],node2_coord[1]+1,node2_coord[2]],node2_rotation[1])
										v_27[0] = rotatePointAboutAxis(v_27[0],node2_coord,[node2_coord[0],node2_coord[1],node2_coord[2]+1],node2_rotation[2])
										v_28[0] = rotatePointAboutAxis(v_28[0],node2_coord,[node2_coord[0]+1,node2_coord[1],node2_coord[2]],node2_rotation[0])
										v_28[0] = rotatePointAboutAxis(v_28[0],node2_coord,[node2_coord[0],node2_coord[1]+1,node2_coord[2]],node2_rotation[1])
										v_28[0] = rotatePointAboutAxis(v_28[0],node2_coord,[node2_coord[0],node2_coord[1],node2_coord[2]+1],node2_rotation[2])

										lines = [[v_11,v_12],[v_12,v_13],[v_13,v_14],[v_14,v_15],
												 [v_15,v_16],[v_16,v_17],[v_17,v_18],[v_18,v_11],
												 [v_21,v_22],[v_22,v_23],[v_23,v_24],[v_24,v_25],
												 [v_25,v_26],[v_26,v_27],[v_27,v_28],[v_28,v_21],
												 [v_11,v_21],[v_12,v_22],[v_13,v_23],[v_14,v_24],
												 [v_15,v_25],[v_16,v_26],[v_17,v_27],[v_18,v_28]]
										faces = [[v_11,v_12,v_13],[v_13,v_14,v_11],
												 [v_11,v_14,v_18],[v_18,v_14,v_15],
												 [v_15,v_16,v_17],[v_17,v_18,v_15],
												 [v_23,v_22,v_21],[v_21,v_24,v_23],
												 [v_24,v_21,v_28],[v_24,v_28,v_25],
												 [v_26,v_25,v_27],[v_28,v_27,v_25],
												 [v_11,v_21,v_12],[v_12,v_21,v_22],
												 [v_11,v_18,v_28],[v_28,v_21,v_11],
												 [v_18,v_17,v_28],[v_28,v_17,v_27],
												 [v_16,v_26,v_27],[v_27,v_17,v_16],
												 [v_16,v_15,v_25],[v_25,v_26,v_16],
												 [v_14,v_24,v_25],[v_25,v_15,v_14],
												 [v_13,v_24,v_14],[v_24,v_13,v_23],
												 [v_13,v_12,v_22],[v_22,v_23,v_13]]

									elif elements[j].crossSection['Type'] == 'T-Beam':
										tw = elements[j].crossSection['top width, tw']
										tt = elements[j].crossSection['top thickness, tt']
										mt = elements[j].crossSection['middle thickness, mt']
										h  = elements[j].crossSection['height, h']
										A1  = mt*(h-tt)
										A2  = tt*tw
										A   = A1+A2
										yC1 = h-(tt/2.)
										yC2 = (h-tt)/2.
										if A != 0.:
											yC = (A1*yC1+A2*yC2)/A
										else:
											yC = 0.
										tw = tw/2.
										tt = tt
										mt = mt/2.
										v_11  = [[node1_coord[0]-y_vec[0]*yC-z_vec[0]*mt,
												  node1_coord[1]-y_vec[1]*yC-z_vec[1]*mt,
												  node1_coord[2]-y_vec[2]*yC-z_vec[2]*mt ], node1_color]
										v_12  = [[node1_coord[0]-y_vec[0]*yC+z_vec[0]*mt,
												  node1_coord[1]-y_vec[1]*yC+z_vec[1]*mt,
												  node1_coord[2]-y_vec[2]*yC+z_vec[2]*mt ], node1_color]
										v_17  = [[node1_coord[0]+y_vec[0]*(h-yC-tt)-z_vec[0]*tw,
												  node1_coord[1]+y_vec[1]*(h-yC-tt)-z_vec[1]*tw,
												  node1_coord[2]+y_vec[2]*(h-yC-tt)-z_vec[2]*tw ], node1_color]
										v_18  = [[node1_coord[0]+y_vec[0]*(h-yC-tt)-z_vec[0]*mt,
												  node1_coord[1]+y_vec[1]*(h-yC-tt)-z_vec[1]*mt,
												  node1_coord[2]+y_vec[2]*(h-yC-tt)-z_vec[2]*mt ], node1_color]
										v_19  = [[node1_coord[0]+y_vec[0]*(h-yC-tt)+z_vec[0]*mt,
												  node1_coord[1]+y_vec[1]*(h-yC-tt)+z_vec[1]*mt,
												  node1_coord[2]+y_vec[2]*(h-yC-tt)+z_vec[2]*mt ], node1_color]
										v_110 = [[node1_coord[0]+y_vec[0]*(h-yC-tt)+z_vec[0]*tw,
												  node1_coord[1]+y_vec[1]*(h-yC-tt)+z_vec[1]*tw,
												  node1_coord[2]+y_vec[2]*(h-yC-tt)+z_vec[2]*tw ], node1_color]
										v_111 = [[node1_coord[0]+y_vec[0]*(h-yC)+z_vec[0]*tw,
												  node1_coord[1]+y_vec[1]*(h-yC)+z_vec[1]*tw,
												  node1_coord[2]+y_vec[2]*(h-yC)+z_vec[2]*tw ], node1_color]
										v_112 = [[node1_coord[0]+y_vec[0]*(h-yC)-z_vec[0]*tw,
												  node1_coord[1]+y_vec[1]*(h-yC)-z_vec[1]*tw,
												  node1_coord[2]+y_vec[2]*(h-yC)-z_vec[2]*tw ], node2_color]
										v_21  = [[node2_coord[0]-y_vec[0]*yC-z_vec[0]*mt,
												  node2_coord[1]-y_vec[1]*yC-z_vec[1]*mt,
												  node2_coord[2]-y_vec[2]*yC-z_vec[2]*mt ], node2_color]
										v_22  = [[node2_coord[0]-y_vec[0]*yC+z_vec[0]*mt,
												  node2_coord[1]-y_vec[1]*yC+z_vec[1]*mt,
												  node2_coord[2]-y_vec[2]*yC+z_vec[2]*mt ], node2_color]
										v_27  = [[node2_coord[0]+y_vec[0]*(h-yC-tt)-z_vec[0]*tw,
												  node2_coord[1]+y_vec[1]*(h-yC-tt)-z_vec[1]*tw,
												  node2_coord[2]+y_vec[2]*(h-yC-tt)-z_vec[2]*tw ], node2_color]
										v_28  = [[node2_coord[0]+y_vec[0]*(h-yC-tt)-z_vec[0]*mt,
												  node2_coord[1]+y_vec[1]*(h-yC-tt)-z_vec[1]*mt,
												  node2_coord[2]+y_vec[2]*(h-yC-tt)-z_vec[2]*mt ], node2_color]
										v_29  = [[node2_coord[0]+y_vec[0]*(h-yC-tt)+z_vec[0]*mt,
												  node2_coord[1]+y_vec[1]*(h-yC-tt)+z_vec[1]*mt,
												  node2_coord[2]+y_vec[2]*(h-yC-tt)+z_vec[2]*mt ], node2_color]
										v_210 = [[node2_coord[0]+y_vec[0]*(h-yC-tt)+z_vec[0]*tw,
												  node2_coord[1]+y_vec[1]*(h-yC-tt)+z_vec[1]*tw,
												  node2_coord[2]+y_vec[2]*(h-yC-tt)+z_vec[2]*tw ], node2_color]
										v_211 = [[node2_coord[0]+y_vec[0]*(h-yC)+z_vec[0]*tw,
												  node2_coord[1]+y_vec[1]*(h-yC)+z_vec[1]*tw,
												  node2_coord[2]+y_vec[2]*(h-yC)+z_vec[2]*tw ], node2_color]
										v_212 = [[node2_coord[0]+y_vec[0]*(h-yC)-z_vec[0]*tw,
												  node2_coord[1]+y_vec[1]*(h-yC)-z_vec[1]*tw,
												  node2_coord[2]+y_vec[2]*(h-yC)-z_vec[2]*tw ], node2_color]
										v_11[0] = rotatePointAboutAxis(v_11[0],node1_coord,[node1_coord[0]+1,node1_coord[1],node1_coord[2]],node1_rotation[0])
										v_11[0] = rotatePointAboutAxis(v_11[0],node1_coord,[node1_coord[0],node1_coord[1]+1,node1_coord[2]],node1_rotation[1])
										v_11[0] = rotatePointAboutAxis(v_11[0],node1_coord,[node1_coord[0],node1_coord[1],node1_coord[2]+1],node1_rotation[2])
										v_12[0] = rotatePointAboutAxis(v_12[0],node1_coord,[node1_coord[0]+1,node1_coord[1],node1_coord[2]],node1_rotation[0])
										v_12[0] = rotatePointAboutAxis(v_12[0],node1_coord,[node1_coord[0],node1_coord[1]+1,node1_coord[2]],node1_rotation[1])
										v_12[0] = rotatePointAboutAxis(v_12[0],node1_coord,[node1_coord[0],node1_coord[1],node1_coord[2]+1],node1_rotation[2])
										v_17[0] = rotatePointAboutAxis(v_17[0],node1_coord,[node1_coord[0]+1,node1_coord[1],node1_coord[2]],node1_rotation[0])
										v_17[0] = rotatePointAboutAxis(v_17[0],node1_coord,[node1_coord[0],node1_coord[1]+1,node1_coord[2]],node1_rotation[1])
										v_17[0] = rotatePointAboutAxis(v_17[0],node1_coord,[node1_coord[0],node1_coord[1],node1_coord[2]+1],node1_rotation[2])
										v_18[0] = rotatePointAboutAxis(v_18[0],node1_coord,[node1_coord[0]+1,node1_coord[1],node1_coord[2]],node1_rotation[0])
										v_18[0] = rotatePointAboutAxis(v_18[0],node1_coord,[node1_coord[0],node1_coord[1]+1,node1_coord[2]],node1_rotation[1])
										v_18[0] = rotatePointAboutAxis(v_18[0],node1_coord,[node1_coord[0],node1_coord[1],node1_coord[2]+1],node1_rotation[2])
										v_19[0] = rotatePointAboutAxis(v_19[0],node1_coord,[node1_coord[0]+1,node1_coord[1],node1_coord[2]],node1_rotation[0])
										v_19[0] = rotatePointAboutAxis(v_19[0],node1_coord,[node1_coord[0],node1_coord[1]+1,node1_coord[2]],node1_rotation[1])
										v_19[0] = rotatePointAboutAxis(v_19[0],node1_coord,[node1_coord[0],node1_coord[1],node1_coord[2]+1],node1_rotation[2])
										v_110[0] = rotatePointAboutAxis(v_110[0],node1_coord,[node1_coord[0]+1,node1_coord[1],node1_coord[2]],node1_rotation[0])
										v_110[0] = rotatePointAboutAxis(v_110[0],node1_coord,[node1_coord[0],node1_coord[1]+1,node1_coord[2]],node1_rotation[1])
										v_110[0] = rotatePointAboutAxis(v_110[0],node1_coord,[node1_coord[0],node1_coord[1],node1_coord[2]+1],node1_rotation[2])
										v_111[0] = rotatePointAboutAxis(v_111[0],node1_coord,[node1_coord[0]+1,node1_coord[1],node1_coord[2]],node1_rotation[0])
										v_111[0] = rotatePointAboutAxis(v_111[0],node1_coord,[node1_coord[0],node1_coord[1]+1,node1_coord[2]],node1_rotation[1])
										v_111[0] = rotatePointAboutAxis(v_111[0],node1_coord,[node1_coord[0],node1_coord[1],node1_coord[2]+1],node1_rotation[2])
										v_112[0] = rotatePointAboutAxis(v_112[0],node1_coord,[node1_coord[0]+1,node1_coord[1],node1_coord[2]],node1_rotation[0])
										v_112[0] = rotatePointAboutAxis(v_112[0],node1_coord,[node1_coord[0],node1_coord[1]+1,node1_coord[2]],node1_rotation[1])
										v_112[0] = rotatePointAboutAxis(v_112[0],node1_coord,[node1_coord[0],node1_coord[1],node1_coord[2]+1],node1_rotation[2])
										v_21[0] = rotatePointAboutAxis(v_21[0],node2_coord,[node2_coord[0]+1,node2_coord[1],node2_coord[2]],node2_rotation[0])
										v_21[0] = rotatePointAboutAxis(v_21[0],node2_coord,[node2_coord[0],node2_coord[1]+1,node2_coord[2]],node2_rotation[1])
										v_21[0] = rotatePointAboutAxis(v_21[0],node2_coord,[node2_coord[0],node2_coord[1],node2_coord[2]+1],node2_rotation[2])
										v_22[0] = rotatePointAboutAxis(v_22[0],node2_coord,[node2_coord[0]+1,node2_coord[1],node2_coord[2]],node2_rotation[0])
										v_22[0] = rotatePointAboutAxis(v_22[0],node2_coord,[node2_coord[0],node2_coord[1]+1,node2_coord[2]],node2_rotation[1])
										v_22[0] = rotatePointAboutAxis(v_22[0],node2_coord,[node2_coord[0],node2_coord[1],node2_coord[2]+1],node2_rotation[2])
										v_27[0] = rotatePointAboutAxis(v_27[0],node2_coord,[node2_coord[0]+1,node2_coord[1],node2_coord[2]],node2_rotation[0])
										v_27[0] = rotatePointAboutAxis(v_27[0],node2_coord,[node2_coord[0],node2_coord[1]+1,node2_coord[2]],node2_rotation[1])
										v_27[0] = rotatePointAboutAxis(v_27[0],node2_coord,[node2_coord[0],node2_coord[1],node2_coord[2]+1],node2_rotation[2])
										v_28[0] = rotatePointAboutAxis(v_28[0],node2_coord,[node2_coord[0]+1,node2_coord[1],node2_coord[2]],node2_rotation[0])
										v_28[0] = rotatePointAboutAxis(v_28[0],node2_coord,[node2_coord[0],node2_coord[1]+1,node2_coord[2]],node2_rotation[1])
										v_28[0] = rotatePointAboutAxis(v_28[0],node2_coord,[node2_coord[0],node2_coord[1],node2_coord[2]+1],node2_rotation[2])
										v_29[0] = rotatePointAboutAxis(v_29[0],node2_coord,[node2_coord[0]+1,node2_coord[1],node2_coord[2]],node2_rotation[0])
										v_29[0] = rotatePointAboutAxis(v_29[0],node2_coord,[node2_coord[0],node2_coord[1]+1,node2_coord[2]],node2_rotation[1])
										v_29[0] = rotatePointAboutAxis(v_29[0],node2_coord,[node2_coord[0],node2_coord[1],node2_coord[2]+1],node2_rotation[2])
										v_210[0] = rotatePointAboutAxis(v_210[0],node2_coord,[node2_coord[0]+1,node2_coord[1],node2_coord[2]],node2_rotation[0])
										v_210[0] = rotatePointAboutAxis(v_210[0],node2_coord,[node2_coord[0],node2_coord[1]+1,node2_coord[2]],node2_rotation[1])
										v_210[0] = rotatePointAboutAxis(v_210[0],node2_coord,[node2_coord[0],node2_coord[1],node2_coord[2]+1],node2_rotation[2])
										v_211[0] = rotatePointAboutAxis(v_211[0],node2_coord,[node2_coord[0]+1,node2_coord[1],node2_coord[2]],node2_rotation[0])
										v_211[0] = rotatePointAboutAxis(v_211[0],node2_coord,[node2_coord[0],node2_coord[1]+1,node2_coord[2]],node2_rotation[1])
										v_211[0] = rotatePointAboutAxis(v_211[0],node2_coord,[node2_coord[0],node2_coord[1],node2_coord[2]+1],node2_rotation[2])
										v_212[0] = rotatePointAboutAxis(v_212[0],node2_coord,[node2_coord[0]+1,node2_coord[1],node2_coord[2]],node2_rotation[0])
										v_212[0] = rotatePointAboutAxis(v_212[0],node2_coord,[node2_coord[0],node2_coord[1]+1,node2_coord[2]],node2_rotation[1])
										v_212[0] = rotatePointAboutAxis(v_212[0],node2_coord,[node2_coord[0],node2_coord[1],node2_coord[2]+1],node2_rotation[2])

										lines = [[v_11,v_12],[v_12,v_19],[v_19,v_110],[v_110,v_111],
												 [v_111,v_112],[v_112,v_17],[v_17,v_18],[v_18,v_11],
												 [v_21,v_22],[v_22,v_29],[v_29,v_210],[v_210,v_211],
												 [v_211,v_212],[v_212,v_27],[v_27,v_28],[v_28,v_21],
												 [v_11,v_21],[v_12,v_22],[v_17,v_27],[v_18,v_28],
												 [v_19,v_29],[v_110,v_210],[v_111,v_211],[v_112,v_212]]
										faces = [[v_11,v_12,v_19],[v_19,v_18,v_11],
												 [v_112,v_17,v_110],[v_110,v_111,v_112],
												 [v_29,v_22,v_21],[v_21,v_28,v_29],
												 [v_210,v_27,v_212],[v_212,v_211,v_210],
												 [v_19,v_12,v_22],[v_22,v_29,v_19],
												 [v_11,v_18,v_28],[v_28,v_21,v_11],
												 [v_111,v_110,v_210],[v_210,v_211,v_111],
												 [v_17,v_112,v_212],[v_212,v_27,v_17],
												 [v_11,v_21,v_12],[v_21,v_22,v_12],
												 [v_112,v_111,v_212],[v_212,v_111,v_211],
												 [v_18,v_17,v_27],[v_27,v_28,v_18],
												 [v_110,v_19,v_29],[v_29,v_210,v_110]]

									else:
										pass

									glLineWidth(2.0)
									glColor3f(0.05, 0.1, 0.05)
									for line in range(len(lines)):
										glBegin(GL_LINES)
										glVertex3f(lines[line][0][0][0],lines[line][0][0][1],lines[line][0][0][2])
										glVertex3f(lines[line][1][0][0],lines[line][1][0][1],lines[line][1][0][2])
										glEnd()

									for face in range(len(faces)):
										glBegin(GL_TRIANGLES)
										glColor3f(faces[face][0][1][0],faces[face][0][1][1],faces[face][0][1][2])
										glVertex3f(faces[face][0][0][0],faces[face][0][0][1],faces[face][0][0][2])
										glColor3f(faces[face][1][1][0],faces[face][1][1][1],faces[face][1][1][2])
										glVertex3f(faces[face][1][0][0],faces[face][1][0][1],faces[face][1][0][2])
										glColor3f(faces[face][2][1][0],faces[face][2][1][1],faces[face][2][1][2])
										glVertex3f(faces[face][2][0][0],faces[face][2][0][1],faces[face][2][0][2])
										glEnd()

					glEndList()

				elif result == 'stress':

					disp_max = 0.
					disp_min = 0.
					for i in elements:
						for j in range(len(elements[i].nodes)):
							if subresult == 'VonMises':
								if solution not in elements[i].solutions:
									pass
								elif result not in elements[i].solutions[solution]:
									pass
								else:
									if elements[i].solutions[solution]['stress']['nodal'][j+1]['VonMises'] >= disp_max:
										disp_max = elements[i].solutions[solution]['stress']['nodal'][j+1]['VonMises']
									if elements[i].solutions[solution]['stress']['nodal'][j+1]['VonMises'] <= disp_min:
										disp_min = elements[i].solutions[solution]['stress']['nodal'][j+1]['VonMises']
								self.displayLists[solution][result][subresult]['info'] = 'Max %.4E' % (disp_max)
							elif subresult == 'MaxPrinc':
								if solution not in elements[i].solutions:
									pass
								elif result not in elements[i].solutions[solution]:
									pass
								else:
									if elements[i].solutions[solution]['stress']['nodal'][j+1]['MaxPrinc'] >= disp_max:
										disp_max = elements[i].solutions[solution]['stress']['nodal'][j+1]['MaxPrinc']
									if elements[i].solutions[solution]['stress']['nodal'][j+1]['MaxPrinc'] <= disp_min:
										disp_min = elements[i].solutions[solution]['stress']['nodal'][j+1]['MaxPrinc']
								self.displayLists[solution][result][subresult]['info'] = 'Max %.4E' % (disp_max)
							elif subresult == 'MinPrinc':
								if solution not in elements[i].solutions:
									pass
								elif result not in elements[i].solutions[solution]:
									pass
								else:
									if elements[i].solutions[solution]['stress']['nodal'][j+1]['MinPrinc'] >= disp_max:
										disp_max = elements[i].solutions[solution]['stress']['nodal'][j+1]['MinPrinc']
									if elements[i].solutions[solution]['stress']['nodal'][j+1]['MinPrinc'] <= disp_min:
										disp_min = elements[i].solutions[solution]['stress']['nodal'][j+1]['MinPrinc']
								self.displayLists[solution][result][subresult]['info'] = 'Max %.4E' % (disp_max)
							elif subresult == 'MaxShear':
								if solution not in elements[i].solutions:
									pass
								elif result not in elements[i].solutions[solution]:
									pass
								else:
									if elements[i].solutions[solution]['stress']['nodal'][j+1]['MaxShear'] >= disp_max:
										disp_max = elements[i].solutions[solution]['stress']['nodal'][j+1]['MaxShear']
									if elements[i].solutions[solution]['stress']['nodal'][j+1]['MaxShear'] <= disp_min:
										disp_min = elements[i].solutions[solution]['stress']['nodal'][j+1]['MaxShear']
								self.displayLists[solution][result][subresult]['info'] = 'Max %.4E' % (disp_max)

					self.displayLists[solution][result][subresult]['max_val'] = disp_max
					self.displayLists[solution][result][subresult]['min_val'] = disp_min

					glNewList(self.displayLists[solution][result][subresult]['shaded'], GL_COMPILE)

					disp_mag_values = [ disp_min,
										disp_min+(disp_max-disp_min)*1./12.,
										disp_min+(disp_max-disp_min)*2./12.,
										disp_min+(disp_max-disp_min)*3./12.,
										disp_min+(disp_max-disp_min)*4./12.,
										disp_min+(disp_max-disp_min)*5./12.,
										disp_min+(disp_max-disp_min)*6./12.,
										disp_min+(disp_max-disp_min)*7./12.,
										disp_min+(disp_max-disp_min)*8./12.,
										disp_min+(disp_max-disp_min)*9./12.,
										disp_min+(disp_max-disp_min)*10./12.,
										disp_min+(disp_max-disp_min)*11./12.,
										disp_max ]
					disp_colors = [ (  0.0,   0.0,   1.0), # blue
									(  0.0, 0.333,   1.0),  
									(  0.0, 0.666,   1.0),  
									(  0.0,   1.0,   1.0),  
									(  0.0,   1.0, 0.666),  
									(  0.0,   1.0, 0.333),
									(  0.0,   1.0,   0.0), # green
									(0.333,   1.0,   0.0),  
									(0.666,   1.0,   0.0),  
									(  1.0,   1.0,   0.0),  
									(  1.0, 0.666,   0.0),  
									(  1.0, 0.333,   0.0),
									(  1.0,   0.0,   0.0) ] # red
					disp_color = disp_colors[0]

					for j in elements:
						facenodes = []
						if elements[j].type == 'ROD2N2D':
							facenodes = [[]]
						elif elements[j].type == 'ROD2N':
							facenodes = [[]]
						elif elements[j].type == 'BEAM2N2D':
							facenodes = [[]]
						elif elements[j].type == 'BEAM2N':
							facenodes = [[]]
						elif elements[j].type == 'TRI3N':
							facenodes = [[0,1,2]]
						elif elements[j].type == 'TRI6N':
							facenodes = [[0,3,5], [3,1,4], [4,2,5], [5,3,4]]
						elif elements[j].type == 'QUAD4N':
							facenodes = [[0,1,3], [1,2,3]]
						elif elements[j].type == 'QUAD8N':
							facenodes = [[0,1,8], [1,2,8], [2,3,8], [3,4,8], [4,5,8], [5,6,8], [6,7,8], [7,0,8]]
						elif elements[j].type == 'TET4N':
							facenodes = [[0,1,3], [1,2,3], [2,0,3], [0,2,1]]
						elif elements[j].type == 'TET10N':
							facenodes = [[0,4,7], [7,4,8], [8,4,1], [7,8,3], [1,5,8], [8,5,9], [9,3,8], [5,2,9],
										 [2,6,9], [9,6,7], [6,0,7], [9,7,3], [5,6,2], [4,0,6], [6,5,4], [4,5,1]]
						elif elements[j].type == 'HEX8N':
							facenodes = [[2,1,0], [0,3,2], [3,7,2], [2,7,6], [7,3,0], [0,4,7], [5,6,7], [7,4,5],
										 [1,2,6], [1,6,5], [1,4,0], [5,4,1]]
						elif elements[j].type == 'HEX20N':
							facenodes = [[ 0, 8,22], [ 8, 1,22], [ 1,13,22], [13, 5,22], [ 5,16,22], [16, 4,22], [ 4,12,22], [12, 0,22],
										 [ 1, 9,23], [ 9, 2,23], [ 2,14,23], [14, 6,23], [ 6,17,23], [17, 5,23], [ 5,13,23], [13, 1,23],
										 [ 2,10,24], [10, 3,24], [ 3,15,24], [15, 7,24], [ 7,18,24], [18, 6,24], [ 6,14,24], [14, 2,24],
										 [ 3,11,25], [11, 0,25], [ 0,12,25], [12, 4,25], [ 4,19,25], [19, 7,25], [ 7,15,25], [15, 3,25],
										 [ 0,11,20], [11, 3,20], [ 3,10,20], [10, 2,20], [ 2, 9,20], [ 9, 1,20], [ 1, 8,20], [ 8, 0,20],
										 [ 4,16,21], [16, 5,21], [ 5,17,21], [17, 6,21], [ 6,18,21], [18, 7,21], [ 7,19,21], [19, 4,21]]
						else:
							pass

						for l in range(len(facenodes)):
							if elements[j].type in ['ROD2N2D', 'ROD2N', 'BEAM2N2D', 'BEAM2N']:
								break
							glBegin(GL_TRIANGLES)
							for k in range(len(disp_mag_values)):
								if solution not in elements[j].solutions:
									disp_color = (0.1, 0.1, 0.1)
								elif result not in elements[j].solutions[solution]:
									disp_color = (0.1, 0.1, 0.1)
								elif subresult == 'VonMises' and ( \
										elements[j].solutions[solution]['stress']['nodal'][facenodes[l][0]+1]['VonMises'] > disp_mag_values[k]):
										pass
								elif subresult == 'MaxPrinc' and ( \
										elements[j].solutions[solution]['stress']['nodal'][facenodes[l][0]+1]['MaxPrinc'] > disp_mag_values[k]):
										pass
								elif subresult == 'MinPrinc' and ( \
										elements[j].solutions[solution]['stress']['nodal'][facenodes[l][0]+1]['MinPrinc'] > disp_mag_values[k]):
										pass
								elif subresult == 'MaxShear' and ( \
										elements[j].solutions[solution]['stress']['nodal'][facenodes[l][0]+1]['MaxShear'] > disp_mag_values[k]):
										pass
								else:
									disp_color = disp_colors[k]
									break
							glColor3f(disp_color[0], disp_color[1], disp_color[2])
							glVertex3f(nodes[elements[j].nodes[facenodes[l][0]].number].coord[0][0] + 
										scale_factor*(displacements[elements[j].nodes[facenodes[l][0]].number].solutions[solution]['displacement'][0]),
									   nodes[elements[j].nodes[facenodes[l][0]].number].coord[1][0] +
										scale_factor*(displacements[elements[j].nodes[facenodes[l][0]].number].solutions[solution]['displacement'][1]),
									   nodes[elements[j].nodes[facenodes[l][0]].number].coord[2][0] +
										scale_factor*(displacements[elements[j].nodes[facenodes[l][0]].number].solutions[solution]['displacement'][2]))
							for k in range(len(disp_mag_values)):
								if solution not in elements[j].solutions:
									disp_color = (0.1, 0.1, 0.1)
								elif result not in elements[j].solutions[solution]:
									disp_color = (0.1, 0.1, 0.1)
								elif subresult == 'VonMises' and ( \
										elements[j].solutions[solution]['stress']['nodal'][facenodes[l][1]+1]['VonMises'] > disp_mag_values[k]):
										pass
								elif subresult == 'MaxPrinc' and ( \
										elements[j].solutions[solution]['stress']['nodal'][facenodes[l][1]+1]['MaxPrinc'] > disp_mag_values[k]):
										pass
								elif subresult == 'MinPrinc' and ( \
										elements[j].solutions[solution]['stress']['nodal'][facenodes[l][1]+1]['MinPrinc'] > disp_mag_values[k]):
										pass
								elif subresult == 'MaxShear' and ( \
										elements[j].solutions[solution]['stress']['nodal'][facenodes[l][1]+1]['MaxShear'] > disp_mag_values[k]):
										pass
								else:
									disp_color = disp_colors[k]
									break
							glColor3f(disp_color[0], disp_color[1], disp_color[2])
							glVertex3f(nodes[elements[j].nodes[facenodes[l][1]].number].coord[0][0] + 
										scale_factor*(displacements[elements[j].nodes[facenodes[l][1]].number].solutions[solution]['displacement'][0]),
									   nodes[elements[j].nodes[facenodes[l][1]].number].coord[1][0] +
										scale_factor*(displacements[elements[j].nodes[facenodes[l][1]].number].solutions[solution]['displacement'][1]),
									   nodes[elements[j].nodes[facenodes[l][1]].number].coord[2][0] +
										scale_factor*(displacements[elements[j].nodes[facenodes[l][1]].number].solutions[solution]['displacement'][2]))
							for k in range(len(disp_mag_values)):
								if solution not in elements[j].solutions:
									disp_color = (0.1, 0.1, 0.1)
								elif result not in elements[j].solutions[solution]:
									disp_color = (0.1, 0.1, 0.1)
								elif subresult == 'VonMises' and ( \
										elements[j].solutions[solution]['stress']['nodal'][facenodes[l][2]+1]['VonMises'] > disp_mag_values[k]):
										pass
								elif subresult == 'MaxPrinc' and ( \
										elements[j].solutions[solution]['stress']['nodal'][facenodes[l][2]+1]['MaxPrinc'] > disp_mag_values[k]):
										pass
								elif subresult == 'MinPrinc' and ( \
										elements[j].solutions[solution]['stress']['nodal'][facenodes[l][2]+1]['MinPrinc'] > disp_mag_values[k]):
										pass
								elif subresult == 'MaxShear' and ( \
										elements[j].solutions[solution]['stress']['nodal'][facenodes[l][2]+1]['MaxShear'] > disp_mag_values[k]):
										pass
								else:
									disp_color = disp_colors[k]
									break
							glColor3f(disp_color[0], disp_color[1], disp_color[2])
							if (elements[j].type == 'QUAD8N') and (facenodes[l][2] == 8):
								glVertex3f( (nodes[elements[j].nodes[0].number].coord[0][0] + nodes[elements[j].nodes[4].number].coord[0][0])/2. + \
											scale_factor*( (displacements[elements[j].nodes[0].number].solutions[solution]['displacement'][0] + \
															displacements[elements[j].nodes[4].number].solutions[solution]['displacement'][0])/2.),
										    (nodes[elements[j].nodes[0].number].coord[1][0] + nodes[elements[j].nodes[4].number].coord[1][0])/2. + \
											scale_factor*( (displacements[elements[j].nodes[0].number].solutions[solution]['displacement'][1] + \
															displacements[elements[j].nodes[4].number].solutions[solution]['displacement'][1])/2.),
										    (nodes[elements[j].nodes[0].number].coord[2][0] + nodes[elements[j].nodes[4].number].coord[2][0])/2. + \
											scale_factor*( (displacements[elements[j].nodes[0].number].solutions[solution]['displacement'][2] + \
															displacements[elements[j].nodes[4].number].solutions[solution]['displacement'][2])/2.) )
							elif (elements[j].type == 'HEX20N') and (facenodes[l][2] in [20,21,22,23,24,25]):
								node_a = 1
								node_b = 2
								if facenodes[l][2] == 20:
									node_a = 0
									node_b = 2
								elif facenodes[l][2] == 21:
									node_a = 4
									node_b = 6
								elif facenodes[l][2] == 22:
									node_a = 0
									node_b = 5
								elif facenodes[l][2] == 23:
									node_a = 1
									node_b = 6
								elif facenodes[l][2] == 24:
									node_a = 2
									node_b = 7
								elif facenodes[l][2] == 25:
									node_a = 3
									node_b = 4
								else:
									pass
								glVertex3f( (nodes[elements[j].nodes[node_a].number].coord[0][0] + nodes[elements[j].nodes[node_b].number].coord[0][0])/2. + \
											scale_factor*( (displacements[elements[j].nodes[0].number].solutions[solution]['displacement'][0] + \
															displacements[elements[j].nodes[4].number].solutions[solution]['displacement'][0])/2.),
										    (nodes[elements[j].nodes[node_a].number].coord[1][0] + nodes[elements[j].nodes[node_b].number].coord[1][0])/2. + \
											scale_factor*( (displacements[elements[j].nodes[0].number].solutions[solution]['displacement'][1] + \
															displacements[elements[j].nodes[4].number].solutions[solution]['displacement'][1])/2.),
										    (nodes[elements[j].nodes[node_a].number].coord[2][0] + nodes[elements[j].nodes[node_b].number].coord[2][0])/2. + \
											scale_factor*( (displacements[elements[j].nodes[0].number].solutions[solution]['displacement'][2] + \
															displacements[elements[j].nodes[4].number].solutions[solution]['displacement'][2])/2.) )
							else:
								glVertex3f(nodes[elements[j].nodes[facenodes[l][2]].number].coord[0][0] + 
											scale_factor*(displacements[elements[j].nodes[facenodes[l][2]].number].solutions[solution]['displacement'][0]),
										   nodes[elements[j].nodes[facenodes[l][2]].number].coord[1][0] +
											scale_factor*(displacements[elements[j].nodes[facenodes[l][2]].number].solutions[solution]['displacement'][1]),
										   nodes[elements[j].nodes[facenodes[l][2]].number].coord[2][0] +
											scale_factor*(displacements[elements[j].nodes[facenodes[l][2]].number].solutions[solution]['displacement'][2]))
							glEnd()
					glEndList()

					self.displayLists[solution][result][subresult]['average'] = glGenLists(1)

					disp_max = 0.
					disp_min = 0.
					for i in elements:
						for j in range(len(elements[i].nodes)):
							if subresult == 'VonMises':
								if solution not in elements[i].solutions:
									pass
								elif result not in elements[i].solutions[solution]:
									pass
								else:
									if nodes[elements[i].nodes[j].number].solutions[solution]['avg_stress']['VonMises'] >= disp_max:
										disp_max = nodes[elements[i].nodes[j].number].solutions[solution]['avg_stress']['VonMises']
									if nodes[elements[i].nodes[j].number].solutions[solution]['avg_stress']['VonMises'] <= disp_min:
										disp_min = nodes[elements[i].nodes[j].number].solutions[solution]['avg_stress']['VonMises']
								self.displayLists[solution][result][subresult]['avg_info'] = 'Max (avg) %.4E' % (disp_max)
							elif subresult == 'MaxPrinc':
								if solution not in elements[i].solutions:
									pass
								elif result not in elements[i].solutions[solution]:
									pass
								else:
									if nodes[elements[i].nodes[j].number].solutions[solution]['avg_stress']['MaxPrinc'] >= disp_max:
										disp_max = nodes[elements[i].nodes[j].number].solutions[solution]['avg_stress']['MaxPrinc']
									if nodes[elements[i].nodes[j].number].solutions[solution]['avg_stress']['MaxPrinc'] <= disp_min:
										disp_min = nodes[elements[i].nodes[j].number].solutions[solution]['avg_stress']['MaxPrinc']
								self.displayLists[solution][result][subresult]['avg_info'] = 'Max (avg) %.4E' % (disp_max)
							elif subresult == 'MinPrinc':
								if solution not in elements[i].solutions:
									pass
								elif result not in elements[i].solutions[solution]:
									pass
								else:
									if nodes[elements[i].nodes[j].number].solutions[solution]['avg_stress']['MinPrinc'] >= disp_max:
										disp_max = nodes[elements[i].nodes[j].number].solutions[solution]['avg_stress']['MinPrinc']
									if nodes[elements[i].nodes[j].number].solutions[solution]['avg_stress']['MinPrinc'] <= disp_min:
										disp_min = nodes[elements[i].nodes[j].number].solutions[solution]['avg_stress']['MinPrinc']
								self.displayLists[solution][result][subresult]['avg_info'] = 'Max (avg) %.4E' % (disp_max)
							elif subresult == 'MaxShear':
								if solution not in elements[i].solutions:
									pass
								elif result not in elements[i].solutions[solution]:
									pass
								else:
									if nodes[elements[i].nodes[j].number].solutions[solution]['avg_stress']['MaxShear'] >= disp_max:
										disp_max = nodes[elements[i].nodes[j].number].solutions[solution]['avg_stress']['MaxShear']
									if nodes[elements[i].nodes[j].number].solutions[solution]['avg_stress']['MaxShear'] <= disp_min:
										disp_min = nodes[elements[i].nodes[j].number].solutions[solution]['avg_stress']['MaxShear']
								self.displayLists[solution][result][subresult]['avg_info'] = 'Max (avg) %.4E' % (disp_max)

					self.displayLists[solution][result][subresult]['avg_max_val'] = disp_max
					self.displayLists[solution][result][subresult]['avg_min_val'] = disp_min

					glNewList(self.displayLists[solution][result][subresult]['average'], GL_COMPILE)

					disp_mag_values = [ disp_min,
										disp_min+(disp_max-disp_min)*1./12.,
										disp_min+(disp_max-disp_min)*2./12.,
										disp_min+(disp_max-disp_min)*3./12.,
										disp_min+(disp_max-disp_min)*4./12.,
										disp_min+(disp_max-disp_min)*5./12.,
										disp_min+(disp_max-disp_min)*6./12.,
										disp_min+(disp_max-disp_min)*7./12.,
										disp_min+(disp_max-disp_min)*8./12.,
										disp_min+(disp_max-disp_min)*9./12.,
										disp_min+(disp_max-disp_min)*10./12.,
										disp_min+(disp_max-disp_min)*11./12.,
										disp_max ]
					disp_colors = [ (  0.0,   0.0,   1.0), # blue
									(  0.0, 0.333,   1.0),  
									(  0.0, 0.666,   1.0),  
									(  0.0,   1.0,   1.0),  
									(  0.0,   1.0, 0.666),  
									(  0.0,   1.0, 0.333),
									(  0.0,   1.0,   0.0), # green
									(0.333,   1.0,   0.0),  
									(0.666,   1.0,   0.0),  
									(  1.0,   1.0,   0.0),  
									(  1.0, 0.666,   0.0),  
									(  1.0, 0.333,   0.0),
									(  1.0,   0.0,   0.0) ] # red
					disp_color = disp_colors[0]

					for j in elements:
						facenodes = []
						if elements[j].type == 'ROD2N2D':
							facenodes = [[]]
						elif elements[j].type == 'ROD2N':
							facenodes = [[]]
						elif elements[j].type == 'BEAM2N2D':
							facenodes = [[]]
						elif elements[j].type == 'BEAM2N':
							facenodes = [[]]
						elif elements[j].type == 'TRI3N':
							facenodes = [[0,1,2]]
						elif elements[j].type == 'TRI6N':
							facenodes = [[0,3,5], [3,1,4], [4,2,5], [5,3,4]]
						elif elements[j].type == 'QUAD4N':
							facenodes = [[0,1,3], [1,2,3]]
						elif elements[j].type == 'QUAD8N':
							facenodes = [[0,1,8], [1,2,8], [2,3,8], [3,4,8], [4,5,8], [5,6,8], [6,7,8], [7,0,8]]
						elif elements[j].type == 'TET4N':
							facenodes = [[0,1,3], [1,2,3], [2,0,3], [0,2,1]]
						elif elements[j].type == 'TET10N':
							facenodes = [[0,4,7], [7,4,8], [8,4,1], [7,8,3], [1,5,8], [8,5,9], [9,3,8], [5,2,9],
										 [2,6,9], [9,6,7], [6,0,7], [9,7,3], [5,6,2], [4,0,6], [6,5,4], [4,5,1]]
						elif elements[j].type == 'HEX8N':
							facenodes = [[2,1,0], [0,3,2], [3,7,2], [2,7,6], [7,3,0], [0,4,7], [5,6,7], [7,4,5],
										 [1,2,6], [1,6,5], [1,4,0], [5,4,1]]
						elif elements[j].type == 'HEX20N':
							facenodes = [[ 0, 8,22], [ 8, 1,22], [ 1,13,22], [13, 5,22], [ 5,16,22], [16, 4,22], [ 4,12,22], [12, 0,22],
										 [ 1, 9,23], [ 9, 2,23], [ 2,14,23], [14, 6,23], [ 6,17,23], [17, 5,23], [ 5,13,23], [13, 1,23],
										 [ 2,10,24], [10, 3,24], [ 3,15,24], [15, 7,24], [ 7,18,24], [18, 6,24], [ 6,14,24], [14, 2,24],
										 [ 3,11,25], [11, 0,25], [ 0,12,25], [12, 4,25], [ 4,19,25], [19, 7,25], [ 7,15,25], [15, 3,25],
										 [ 0,11,20], [11, 3,20], [ 3,10,20], [10, 2,20], [ 2, 9,20], [ 9, 1,20], [ 1, 8,20], [ 8, 0,20],
										 [ 4,16,21], [16, 5,21], [ 5,17,21], [17, 6,21], [ 6,18,21], [18, 7,21], [ 7,19,21], [19, 4,21]]
						else:
							pass

						for l in range(len(facenodes)):
							if elements[j].type in ['ROD2N2D', 'ROD2N', 'BEAM2N2D', 'BEAM2N']:
								break
							glBegin(GL_TRIANGLES)
							for k in range(len(disp_mag_values)):
								if solution not in elements[j].solutions:
									disp_color = (0.1, 0.1, 0.1)
								elif subresult == 'VonMises' and ( \
										nodes[elements[j].nodes[facenodes[l][0]].number].solutions[solution]['avg_stress']['VonMises'] > disp_mag_values[k]):
										pass
								elif subresult == 'MaxPrinc' and ( \
										nodes[elements[j].nodes[facenodes[l][0]].number].solutions[solution]['avg_stress']['MaxPrinc'] > disp_mag_values[k]):
										pass
								elif subresult == 'MinPrinc' and ( \
										nodes[elements[j].nodes[facenodes[l][0]].number].solutions[solution]['avg_stress']['MinPrinc'] > disp_mag_values[k]):
										pass
								elif subresult == 'MaxShear' and ( \
										nodes[elements[j].nodes[facenodes[l][0]].number].solutions[solution]['avg_stress']['MaxShear'] > disp_mag_values[k]):
										pass
								else:
									disp_color = disp_colors[k]
									break
							glColor3f(disp_color[0], disp_color[1], disp_color[2])
							glVertex3f(nodes[elements[j].nodes[facenodes[l][0]].number].coord[0][0] + 
										scale_factor*(displacements[elements[j].nodes[facenodes[l][0]].number].solutions[solution]['displacement'][0]),
									   nodes[elements[j].nodes[facenodes[l][0]].number].coord[1][0] +
										scale_factor*(displacements[elements[j].nodes[facenodes[l][0]].number].solutions[solution]['displacement'][1]),
									   nodes[elements[j].nodes[facenodes[l][0]].number].coord[2][0] +
										scale_factor*(displacements[elements[j].nodes[facenodes[l][0]].number].solutions[solution]['displacement'][2]))
							for k in range(len(disp_mag_values)):
								if solution not in elements[j].solutions:
									disp_color = (0.1, 0.1, 0.1)
								elif subresult == 'VonMises' and ( \
										nodes[elements[j].nodes[facenodes[l][1]].number].solutions[solution]['avg_stress']['VonMises'] > disp_mag_values[k]):
										pass
								elif subresult == 'MaxPrinc' and ( \
										nodes[elements[j].nodes[facenodes[l][1]].number].solutions[solution]['avg_stress']['MaxPrinc'] > disp_mag_values[k]):
										pass
								elif subresult == 'MinPrinc' and ( \
										nodes[elements[j].nodes[facenodes[l][1]].number].solutions[solution]['avg_stress']['MinPrinc'] > disp_mag_values[k]):
										pass
								elif subresult == 'MaxShear' and ( \
										nodes[elements[j].nodes[facenodes[l][1]].number].solutions[solution]['avg_stress']['MaxShear'] > disp_mag_values[k]):
										pass
								else:
									disp_color = disp_colors[k]
									break
							glColor3f(disp_color[0], disp_color[1], disp_color[2])
							glVertex3f(nodes[elements[j].nodes[facenodes[l][1]].number].coord[0][0] + 
										scale_factor*(displacements[elements[j].nodes[facenodes[l][1]].number].solutions[solution]['displacement'][0]),
									   nodes[elements[j].nodes[facenodes[l][1]].number].coord[1][0] +
										scale_factor*(displacements[elements[j].nodes[facenodes[l][1]].number].solutions[solution]['displacement'][1]),
									   nodes[elements[j].nodes[facenodes[l][1]].number].coord[2][0] +
										scale_factor*(displacements[elements[j].nodes[facenodes[l][1]].number].solutions[solution]['displacement'][2]))
							for k in range(len(disp_mag_values)):
								if ((elements[j].type == 'QUAD8N') and (facenodes[l][2] == 8)) or \
									((elements[j].type == 'HEX20N') and (facenodes[l][2] in [20,21,22,23,24,25])):
									if solution not in elements[j].solutions:
										disp_color = (0.1, 0.1, 0.1)
									elif subresult == 'VonMises' and ( \
											elements[j].solutions[solution]['stress']['nodal'][facenodes[l][2]+1]['VonMises'] > disp_mag_values[k]):
											pass
									elif subresult == 'MaxPrinc' and ( \
											elements[j].solutions[solution]['stress']['nodal'][facenodes[l][2]+1]['MaxPrinc'] > disp_mag_values[k]):
											pass
									elif subresult == 'MinPrinc' and ( \
											elements[j].solutions[solution]['stress']['nodal'][facenodes[l][2]+1]['MinPrinc'] > disp_mag_values[k]):
											pass
									elif subresult == 'MaxShear' and ( \
											elements[j].solutions[solution]['stress']['nodal'][facenodes[l][2]+1]['MaxShear'] > disp_mag_values[k]):
											pass
									else:
										disp_color = disp_colors[k]
										break
								else:
									if solution not in elements[j].solutions:
										disp_color = (0.1, 0.1, 0.1)
									elif subresult == 'VonMises' and ( \
											nodes[elements[j].nodes[facenodes[l][2]].number].solutions[solution]['avg_stress']['VonMises'] > disp_mag_values[k]):
											pass
									elif subresult == 'MaxPrinc' and ( \
											nodes[elements[j].nodes[facenodes[l][2]].number].solutions[solution]['avg_stress']['MaxPrinc'] > disp_mag_values[k]):
											pass
									elif subresult == 'MinPrinc' and ( \
											nodes[elements[j].nodes[facenodes[l][2]].number].solutions[solution]['avg_stress']['MinPrinc'] > disp_mag_values[k]):
											pass
									elif subresult == 'MaxShear' and ( \
											nodes[elements[j].nodes[facenodes[l][2]].number].solutions[solution]['avg_stress']['MaxShear'] > disp_mag_values[k]):
											pass
									else:
										disp_color = disp_colors[k]
										break
							glColor3f(disp_color[0], disp_color[1], disp_color[2])
							if (elements[j].type == 'QUAD8N') and (facenodes[l][2] == 8):
								glVertex3f( (nodes[elements[j].nodes[0].number].coord[0][0] + nodes[elements[j].nodes[4].number].coord[0][0])/2. + \
											scale_factor*( (displacements[elements[j].nodes[0].number].solutions[solution]['displacement'][0] + \
															displacements[elements[j].nodes[4].number].solutions[solution]['displacement'][0])/2.),
										    (nodes[elements[j].nodes[0].number].coord[1][0] + nodes[elements[j].nodes[4].number].coord[1][0])/2. + \
											scale_factor*( (displacements[elements[j].nodes[0].number].solutions[solution]['displacement'][1] + \
															displacements[elements[j].nodes[4].number].solutions[solution]['displacement'][1])/2.),
										    (nodes[elements[j].nodes[0].number].coord[2][0] + nodes[elements[j].nodes[4].number].coord[2][0])/2. + \
											scale_factor*( (displacements[elements[j].nodes[0].number].solutions[solution]['displacement'][2] + \
															displacements[elements[j].nodes[4].number].solutions[solution]['displacement'][2])/2.) )
							elif (elements[j].type == 'HEX20N') and (facenodes[l][2] in [20,21,22,23,24,25]):
								node_a = 1
								node_b = 2
								if facenodes[l][2] == 20:
									node_a = 0
									node_b = 2
								elif facenodes[l][2] == 21:
									node_a = 4
									node_b = 6
								elif facenodes[l][2] == 22:
									node_a = 0
									node_b = 5
								elif facenodes[l][2] == 23:
									node_a = 1
									node_b = 6
								elif facenodes[l][2] == 24:
									node_a = 2
									node_b = 7
								elif facenodes[l][2] == 25:
									node_a = 3
									node_b = 4
								else:
									pass
								glVertex3f( (nodes[elements[j].nodes[node_a].number].coord[0][0] + nodes[elements[j].nodes[node_b].number].coord[0][0])/2. + \
											scale_factor*( (displacements[elements[j].nodes[0].number].solutions[solution]['displacement'][0] + \
															displacements[elements[j].nodes[4].number].solutions[solution]['displacement'][0])/2.),
										    (nodes[elements[j].nodes[node_a].number].coord[1][0] + nodes[elements[j].nodes[node_b].number].coord[1][0])/2. + \
											scale_factor*( (displacements[elements[j].nodes[0].number].solutions[solution]['displacement'][1] + \
															displacements[elements[j].nodes[4].number].solutions[solution]['displacement'][1])/2.),
										    (nodes[elements[j].nodes[node_a].number].coord[2][0] + nodes[elements[j].nodes[node_b].number].coord[2][0])/2. + \
											scale_factor*( (displacements[elements[j].nodes[0].number].solutions[solution]['displacement'][2] + \
															displacements[elements[j].nodes[4].number].solutions[solution]['displacement'][2])/2.) )
							else:
								glVertex3f(nodes[elements[j].nodes[facenodes[l][2]].number].coord[0][0] + 
											scale_factor*(displacements[elements[j].nodes[facenodes[l][2]].number].solutions[solution]['displacement'][0]),
										   nodes[elements[j].nodes[facenodes[l][2]].number].coord[1][0] +
											scale_factor*(displacements[elements[j].nodes[facenodes[l][2]].number].solutions[solution]['displacement'][1]),
										   nodes[elements[j].nodes[facenodes[l][2]].number].coord[2][0] +
											scale_factor*(displacements[elements[j].nodes[facenodes[l][2]].number].solutions[solution]['displacement'][2]))
							glEnd()
					glEndList()

				elif result == 'strain':

					disp_max = 0.
					disp_min = 0.
					for i in elements:
						for j in range(len(elements[i].nodes)):
							if subresult == 'VonMises':
								if solution not in elements[i].solutions:
									pass
								elif result not in elements[i].solutions[solution]:
									pass
								else:
									if elements[i].solutions[solution]['strain']['nodal'][j+1]['VonMises'] >= disp_max:
										disp_max = elements[i].solutions[solution]['strain']['nodal'][j+1]['VonMises']
									if elements[i].solutions[solution]['strain']['nodal'][j+1]['VonMises'] <= disp_min:
										disp_min = elements[i].solutions[solution]['strain']['nodal'][j+1]['VonMises']
								self.displayLists[solution][result][subresult]['info'] = 'Max %.4E' % (disp_max)
							elif subresult == 'MaxPrinc':
								if solution not in elements[i].solutions:
									pass
								elif result not in elements[i].solutions[solution]:
									pass
								else:
									if elements[i].solutions[solution]['strain']['nodal'][j+1]['MaxPrinc'] >= disp_max:
										disp_max = elements[i].solutions[solution]['strain']['nodal'][j+1]['MaxPrinc']
									if elements[i].solutions[solution]['strain']['nodal'][j+1]['MaxPrinc'] <= disp_min:
										disp_min = elements[i].solutions[solution]['strain']['nodal'][j+1]['MaxPrinc']
								self.displayLists[solution][result][subresult]['info'] = 'Max %.4E' % (disp_max)
							elif subresult == 'MinPrinc':
								if solution not in elements[i].solutions:
									pass
								elif result not in elements[i].solutions[solution]:
									pass
								else:
									if elements[i].solutions[solution]['strain']['nodal'][j+1]['MinPrinc'] >= disp_max:
										disp_max = elements[i].solutions[solution]['strain']['nodal'][j+1]['MinPrinc']
									if elements[i].solutions[solution]['strain']['nodal'][j+1]['MinPrinc'] <= disp_min:
										disp_min = elements[i].solutions[solution]['strain']['nodal'][j+1]['MinPrinc']
								self.displayLists[solution][result][subresult]['info'] = 'Max %.4E' % (disp_max)
							elif subresult == 'MaxShear':
								if solution not in elements[i].solutions:
									pass
								elif result not in elements[i].solutions[solution]:
									pass
								else:
									if elements[i].solutions[solution]['strain']['nodal'][j+1]['MaxShear'] >= disp_max:
										disp_max = elements[i].solutions[solution]['strain']['nodal'][j+1]['MaxShear']
									if elements[i].solutions[solution]['strain']['nodal'][j+1]['MaxShear'] <= disp_min:
										disp_min = elements[i].solutions[solution]['strain']['nodal'][j+1]['MaxShear']
								self.displayLists[solution][result][subresult]['info'] = 'Max %.4E' % (disp_max)

					self.displayLists[solution][result][subresult]['max_val'] = disp_max
					self.displayLists[solution][result][subresult]['min_val'] = disp_min

					glNewList(self.displayLists[solution][result][subresult]['shaded'], GL_COMPILE)

					disp_mag_values = [ disp_min,
										disp_min+(disp_max-disp_min)*1./12.,
										disp_min+(disp_max-disp_min)*2./12.,
										disp_min+(disp_max-disp_min)*3./12.,
										disp_min+(disp_max-disp_min)*4./12.,
										disp_min+(disp_max-disp_min)*5./12.,
										disp_min+(disp_max-disp_min)*6./12.,
										disp_min+(disp_max-disp_min)*7./12.,
										disp_min+(disp_max-disp_min)*8./12.,
										disp_min+(disp_max-disp_min)*9./12.,
										disp_min+(disp_max-disp_min)*10./12.,
										disp_min+(disp_max-disp_min)*11./12.,
										disp_max ]
					disp_colors = [ (  0.0,   0.0,   1.0), # blue
									(  0.0, 0.333,   1.0),  
									(  0.0, 0.666,   1.0),  
									(  0.0,   1.0,   1.0),  
									(  0.0,   1.0, 0.666),  
									(  0.0,   1.0, 0.333),
									(  0.0,   1.0,   0.0), # green
									(0.333,   1.0,   0.0),  
									(0.666,   1.0,   0.0),  
									(  1.0,   1.0,   0.0),  
									(  1.0, 0.666,   0.0),  
									(  1.0, 0.333,   0.0),
									(  1.0,   0.0,   0.0) ] # red
					disp_color = disp_colors[0]

					for j in elements:
						facenodes = []
						if elements[j].type == 'ROD2N2D':
							facenodes = [[]]
						elif elements[j].type == 'ROD2N':
							facenodes = [[]]
						elif elements[j].type == 'BEAM2N2D':
							facenodes = [[]]
						elif elements[j].type == 'BEAM2N':
							facenodes = [[]]
						elif elements[j].type == 'TRI3N':
							facenodes = [[0,1,2]]
						elif elements[j].type == 'TRI6N':
							facenodes = [[0,3,5], [3,1,4], [4,2,5], [5,3,4]]
						elif elements[j].type == 'QUAD4N':
							facenodes = [[0,1,3], [1,2,3]]
						elif elements[j].type == 'QUAD8N':
							facenodes = [[0,1,8], [1,2,8], [2,3,8], [3,4,8], [4,5,8], [5,6,8], [6,7,8], [7,0,8]]
						elif elements[j].type == 'TET4N':
							facenodes = [[0,1,3], [1,2,3], [2,0,3], [0,2,1]]
						elif elements[j].type == 'TET10N':
							facenodes = [[0,4,7], [7,4,8], [8,4,1], [7,8,3], [1,5,8], [8,5,9], [9,3,8], [5,2,9],
										 [2,6,9], [9,6,7], [6,0,7], [9,7,3], [5,6,2], [4,0,6], [6,5,4], [4,5,1]]
						elif elements[j].type == 'HEX8N':
							facenodes = [[2,1,0], [0,3,2], [3,7,2], [2,7,6], [7,3,0], [0,4,7], [5,6,7], [7,4,5],
										 [1,2,6], [1,6,5], [1,4,0], [5,4,1]]
						elif elements[j].type == 'HEX20N':
							facenodes = [[ 0, 8,22], [ 8, 1,22], [ 1,13,22], [13, 5,22], [ 5,16,22], [16, 4,22], [ 4,12,22], [12, 0,22],
										 [ 1, 9,23], [ 9, 2,23], [ 2,14,23], [14, 6,23], [ 6,17,23], [17, 5,23], [ 5,13,23], [13, 1,23],
										 [ 2,10,24], [10, 3,24], [ 3,15,24], [15, 7,24], [ 7,18,24], [18, 6,24], [ 6,14,24], [14, 2,24],
										 [ 3,11,25], [11, 0,25], [ 0,12,25], [12, 4,25], [ 4,19,25], [19, 7,25], [ 7,15,25], [15, 3,25],
										 [ 0,11,20], [11, 3,20], [ 3,10,20], [10, 2,20], [ 2, 9,20], [ 9, 1,20], [ 1, 8,20], [ 8, 0,20],
										 [ 4,16,21], [16, 5,21], [ 5,17,21], [17, 6,21], [ 6,18,21], [18, 7,21], [ 7,19,21], [19, 4,21]]
						else:
							pass

						for l in range(len(facenodes)):
							if elements[j].type in ['ROD2N2D', 'ROD2N', 'BEAM2N2D', 'BEAM2N']:
								break
							glBegin(GL_TRIANGLES)
							for k in range(len(disp_mag_values)):
								if solution not in elements[j].solutions:
									disp_color = (0.1, 0.1, 0.1)
								elif result not in elements[j].solutions[solution]:
									disp_color = (0.1, 0.1, 0.1)
								elif subresult == 'VonMises' and ( \
										elements[j].solutions[solution]['strain']['nodal'][facenodes[l][0]+1]['VonMises'] > disp_mag_values[k]):
										pass
								elif subresult == 'MaxPrinc' and ( \
										elements[j].solutions[solution]['strain']['nodal'][facenodes[l][0]+1]['MaxPrinc'] > disp_mag_values[k]):
										pass
								elif subresult == 'MinPrinc' and ( \
										elements[j].solutions[solution]['strain']['nodal'][facenodes[l][0]+1]['MinPrinc'] > disp_mag_values[k]):
										pass
								elif subresult == 'MaxShear' and ( \
										elements[j].solutions[solution]['strain']['nodal'][facenodes[l][0]+1]['MaxShear'] > disp_mag_values[k]):
										pass
								else:
									disp_color = disp_colors[k]
									break
							glColor3f(disp_color[0], disp_color[1], disp_color[2])
							glVertex3f(nodes[elements[j].nodes[facenodes[l][0]].number].coord[0][0] + 
										scale_factor*(displacements[elements[j].nodes[facenodes[l][0]].number].solutions[solution]['displacement'][0]),
									   nodes[elements[j].nodes[facenodes[l][0]].number].coord[1][0] +
										scale_factor*(displacements[elements[j].nodes[facenodes[l][0]].number].solutions[solution]['displacement'][1]),
									   nodes[elements[j].nodes[facenodes[l][0]].number].coord[2][0] +
										scale_factor*(displacements[elements[j].nodes[facenodes[l][0]].number].solutions[solution]['displacement'][2]))
							for k in range(len(disp_mag_values)):
								if solution not in elements[j].solutions:
									disp_color = (0.1, 0.1, 0.1)
								elif result not in elements[j].solutions[solution]:
									disp_color = (0.1, 0.1, 0.1)
								elif subresult == 'VonMises' and ( \
										elements[j].solutions[solution]['strain']['nodal'][facenodes[l][1]+1]['VonMises'] > disp_mag_values[k]):
										pass
								elif subresult == 'MaxPrinc' and ( \
										elements[j].solutions[solution]['strain']['nodal'][facenodes[l][1]+1]['MaxPrinc'] > disp_mag_values[k]):
										pass
								elif subresult == 'MinPrinc' and ( \
										elements[j].solutions[solution]['strain']['nodal'][facenodes[l][1]+1]['MinPrinc'] > disp_mag_values[k]):
										pass
								elif subresult == 'MaxShear' and ( \
										elements[j].solutions[solution]['strain']['nodal'][facenodes[l][1]+1]['MaxShear'] > disp_mag_values[k]):
										pass
								else:
									disp_color = disp_colors[k]
									break
							glColor3f(disp_color[0], disp_color[1], disp_color[2])
							glVertex3f(nodes[elements[j].nodes[facenodes[l][1]].number].coord[0][0] + 
										scale_factor*(displacements[elements[j].nodes[facenodes[l][1]].number].solutions[solution]['displacement'][0]),
									   nodes[elements[j].nodes[facenodes[l][1]].number].coord[1][0] +
										scale_factor*(displacements[elements[j].nodes[facenodes[l][1]].number].solutions[solution]['displacement'][1]),
									   nodes[elements[j].nodes[facenodes[l][1]].number].coord[2][0] +
										scale_factor*(displacements[elements[j].nodes[facenodes[l][1]].number].solutions[solution]['displacement'][2]))
							for k in range(len(disp_mag_values)):
								if solution not in elements[j].solutions:
									disp_color = (0.1, 0.1, 0.1)
								elif result not in elements[j].solutions[solution]:
									disp_color = (0.1, 0.1, 0.1)
								elif subresult == 'VonMises' and ( \
										elements[j].solutions[solution]['strain']['nodal'][facenodes[l][2]+1]['VonMises'] > disp_mag_values[k]):
										pass
								elif subresult == 'MaxPrinc' and ( \
										elements[j].solutions[solution]['strain']['nodal'][facenodes[l][2]+1]['MaxPrinc'] > disp_mag_values[k]):
										pass
								elif subresult == 'MinPrinc' and ( \
										elements[j].solutions[solution]['strain']['nodal'][facenodes[l][2]+1]['MinPrinc'] > disp_mag_values[k]):
										pass
								elif subresult == 'MaxShear' and ( \
										elements[j].solutions[solution]['strain']['nodal'][facenodes[l][2]+1]['MaxShear'] > disp_mag_values[k]):
										pass
								else:
									disp_color = disp_colors[k]
									break
							glColor3f(disp_color[0], disp_color[1], disp_color[2])
							if (elements[j].type == 'QUAD8N') and (facenodes[l][2] == 8):
								glVertex3f( (nodes[elements[j].nodes[0].number].coord[0][0] + nodes[elements[j].nodes[4].number].coord[0][0])/2. + \
											scale_factor*( (displacements[elements[j].nodes[0].number].solutions[solution]['displacement'][0] + \
															displacements[elements[j].nodes[4].number].solutions[solution]['displacement'][0])/2.),
										    (nodes[elements[j].nodes[0].number].coord[1][0] + nodes[elements[j].nodes[4].number].coord[1][0])/2. + \
											scale_factor*( (displacements[elements[j].nodes[0].number].solutions[solution]['displacement'][1] + \
															displacements[elements[j].nodes[4].number].solutions[solution]['displacement'][1])/2.),
										    (nodes[elements[j].nodes[0].number].coord[2][0] + nodes[elements[j].nodes[4].number].coord[2][0])/2. + \
											scale_factor*( (displacements[elements[j].nodes[0].number].solutions[solution]['displacement'][2] + \
															displacements[elements[j].nodes[4].number].solutions[solution]['displacement'][2])/2.) )
							elif (elements[j].type == 'HEX20N') and (facenodes[l][2] in [20,21,22,23,24,25]):
								node_a = 1
								node_b = 2
								if facenodes[l][2] == 20:
									node_a = 0
									node_b = 2
								elif facenodes[l][2] == 21:
									node_a = 4
									node_b = 6
								elif facenodes[l][2] == 22:
									node_a = 0
									node_b = 5
								elif facenodes[l][2] == 23:
									node_a = 1
									node_b = 6
								elif facenodes[l][2] == 24:
									node_a = 2
									node_b = 7
								elif facenodes[l][2] == 25:
									node_a = 3
									node_b = 4
								else:
									pass
								glVertex3f( (nodes[elements[j].nodes[node_a].number].coord[0][0] + nodes[elements[j].nodes[node_b].number].coord[0][0])/2. + \
											scale_factor*( (displacements[elements[j].nodes[0].number].solutions[solution]['displacement'][0] + \
															displacements[elements[j].nodes[4].number].solutions[solution]['displacement'][0])/2.),
										    (nodes[elements[j].nodes[node_a].number].coord[1][0] + nodes[elements[j].nodes[node_b].number].coord[1][0])/2. + \
											scale_factor*( (displacements[elements[j].nodes[0].number].solutions[solution]['displacement'][1] + \
															displacements[elements[j].nodes[4].number].solutions[solution]['displacement'][1])/2.),
										    (nodes[elements[j].nodes[node_a].number].coord[2][0] + nodes[elements[j].nodes[node_b].number].coord[2][0])/2. + \
											scale_factor*( (displacements[elements[j].nodes[0].number].solutions[solution]['displacement'][2] + \
															displacements[elements[j].nodes[4].number].solutions[solution]['displacement'][2])/2.) )
							else:
								glVertex3f(nodes[elements[j].nodes[facenodes[l][2]].number].coord[0][0] + 
											scale_factor*(displacements[elements[j].nodes[facenodes[l][2]].number].solutions[solution]['displacement'][0]),
										   nodes[elements[j].nodes[facenodes[l][2]].number].coord[1][0] +
											scale_factor*(displacements[elements[j].nodes[facenodes[l][2]].number].solutions[solution]['displacement'][1]),
										   nodes[elements[j].nodes[facenodes[l][2]].number].coord[2][0] +
											scale_factor*(displacements[elements[j].nodes[facenodes[l][2]].number].solutions[solution]['displacement'][2]))
							glEnd()
					glEndList()

					self.displayLists[solution][result][subresult]['average'] = glGenLists(1)

					disp_max = 0.
					disp_min = 0.
					for i in elements:
						for j in range(len(elements[i].nodes)):
							if subresult == 'VonMises':
								if solution not in elements[i].solutions:
									pass
								elif result not in elements[i].solutions[solution]:
									pass
								else:
									if nodes[elements[i].nodes[j].number].solutions[solution]['avg_strain']['VonMises'] >= disp_max:
										disp_max = nodes[elements[i].nodes[j].number].solutions[solution]['avg_strain']['VonMises']
									if nodes[elements[i].nodes[j].number].solutions[solution]['avg_strain']['VonMises'] <= disp_min:
										disp_min = nodes[elements[i].nodes[j].number].solutions[solution]['avg_strain']['VonMises']
								self.displayLists[solution][result][subresult]['avg_info'] = 'Max (avg) %.4E' % (disp_max)
							elif subresult == 'MaxPrinc':
								if solution not in elements[i].solutions:
									pass
								elif result not in elements[i].solutions[solution]:
									pass
								else:
									if nodes[elements[i].nodes[j].number].solutions[solution]['avg_strain']['MaxPrinc'] >= disp_max:
										disp_max = nodes[elements[i].nodes[j].number].solutions[solution]['avg_strain']['MaxPrinc']
									if nodes[elements[i].nodes[j].number].solutions[solution]['avg_strain']['MaxPrinc'] <= disp_min:
										disp_min = nodes[elements[i].nodes[j].number].solutions[solution]['avg_strain']
								self.displayLists[solution][result][subresult]['avg_info'] = 'Max (avg) %.4E' % (disp_max)
							elif subresult == 'MinPrinc':
								if solution not in elements[i].solutions:
									pass
								elif result not in elements[i].solutions[solution]:
									pass
								else:
									if nodes[elements[i].nodes[j].number].solutions[solution]['avg_strain']['MinPrinc'] >= disp_max:
										disp_max = nodes[elements[i].nodes[j].number].solutions[solution]['avg_strain']['MinPrinc']
									if nodes[elements[i].nodes[j].number].solutions[solution]['avg_strain']['MinPrinc'] <= disp_min:
										disp_min = nodes[elements[i].nodes[j].number].solutions[solution]['avg_strain']['MinPrinc']
								self.displayLists[solution][result][subresult]['avg_info'] = 'Max (avg) %.4E' % (disp_max)
							elif subresult == 'MaxShear':
								if solution not in elements[i].solutions:
									pass
								elif result not in elements[i].solutions[solution]:
									pass
								else:
									if nodes[elements[i].nodes[j].number].solutions[solution]['avg_strain']['MaxShear'] >= disp_max:
										disp_max = nodes[elements[i].nodes[j].number].solutions[solution]['avg_strain']['MaxShear']
									if nodes[elements[i].nodes[j].number].solutions[solution]['avg_strain']['MaxShear'] <= disp_min:
										disp_min = nodes[elements[i].nodes[j].number].solutions[solution]['avg_strain']['MaxShear']
								self.displayLists[solution][result][subresult]['avg_info'] = 'Max (avg) %.4E' % (disp_max)

					self.displayLists[solution][result][subresult]['avg_max_val'] = disp_max
					self.displayLists[solution][result][subresult]['avg_min_val'] = disp_min

					glNewList(self.displayLists[solution][result][subresult]['average'], GL_COMPILE)

					disp_mag_values = [ disp_min,
										disp_min+(disp_max-disp_min)*1./12.,
										disp_min+(disp_max-disp_min)*2./12.,
										disp_min+(disp_max-disp_min)*3./12.,
										disp_min+(disp_max-disp_min)*4./12.,
										disp_min+(disp_max-disp_min)*5./12.,
										disp_min+(disp_max-disp_min)*6./12.,
										disp_min+(disp_max-disp_min)*7./12.,
										disp_min+(disp_max-disp_min)*8./12.,
										disp_min+(disp_max-disp_min)*9./12.,
										disp_min+(disp_max-disp_min)*10./12.,
										disp_min+(disp_max-disp_min)*11./12.,
										disp_max ]
					disp_colors = [ (  0.0,   0.0,   1.0), # blue
									(  0.0, 0.333,   1.0),  
									(  0.0, 0.666,   1.0),  
									(  0.0,   1.0,   1.0),  
									(  0.0,   1.0, 0.666),  
									(  0.0,   1.0, 0.333),
									(  0.0,   1.0,   0.0), # green
									(0.333,   1.0,   0.0),  
									(0.666,   1.0,   0.0),  
									(  1.0,   1.0,   0.0),  
									(  1.0, 0.666,   0.0),  
									(  1.0, 0.333,   0.0),
									(  1.0,   0.0,   0.0) ] # red
					disp_color = disp_colors[0]

					for j in elements:
						facenodes = []
						if elements[j].type == 'ROD2N2D':
							facenodes = [[]]
						elif elements[j].type == 'ROD2N':
							facenodes = [[]]
						elif elements[j].type == 'BEAM2N2D':
							facenodes = [[]]
						elif elements[j].type == 'BEAM2N':
							facenodes = [[]]
						elif elements[j].type == 'TRI3N':
							facenodes = [[0,1,2]]
						elif elements[j].type == 'TRI6N':
							facenodes = [[0,3,5], [3,1,4], [4,2,5], [5,3,4]]
						elif elements[j].type == 'QUAD4N':
							facenodes = [[0,1,3], [1,2,3]]
						elif elements[j].type == 'QUAD8N':
							facenodes = [[0,1,8], [1,2,8], [2,3,8], [3,4,8], [4,5,8], [5,6,8], [6,7,8], [7,0,8]]
						elif elements[j].type == 'TET4N':
							facenodes = [[0,1,3], [1,2,3], [2,0,3], [0,2,1]]
						elif elements[j].type == 'TET10N':
							facenodes = [[0,4,7], [7,4,8], [8,4,1], [7,8,3], [1,5,8], [8,5,9], [9,3,8], [5,2,9],
										 [2,6,9], [9,6,7], [6,0,7], [9,7,3], [5,6,2], [4,0,6], [6,5,4], [4,5,1]]
						elif elements[j].type == 'HEX8N':
							facenodes = [[2,1,0], [0,3,2], [3,7,2], [2,7,6], [7,3,0], [0,4,7], [5,6,7], [7,4,5],
										 [1,2,6], [1,6,5], [1,4,0], [5,4,1]]
						elif elements[j].type == 'HEX20N':
							facenodes = [[ 0, 8,22], [ 8, 1,22], [ 1,13,22], [13, 5,22], [ 5,16,22], [16, 4,22], [ 4,12,22], [12, 0,22],
										 [ 1, 9,23], [ 9, 2,23], [ 2,14,23], [14, 6,23], [ 6,17,23], [17, 5,23], [ 5,13,23], [13, 1,23],
										 [ 2,10,24], [10, 3,24], [ 3,15,24], [15, 7,24], [ 7,18,24], [18, 6,24], [ 6,14,24], [14, 2,24],
										 [ 3,11,25], [11, 0,25], [ 0,12,25], [12, 4,25], [ 4,19,25], [19, 7,25], [ 7,15,25], [15, 3,25],
										 [ 0,11,20], [11, 3,20], [ 3,10,20], [10, 2,20], [ 2, 9,20], [ 9, 1,20], [ 1, 8,20], [ 8, 0,20],
										 [ 4,16,21], [16, 5,21], [ 5,17,21], [17, 6,21], [ 6,18,21], [18, 7,21], [ 7,19,21], [19, 4,21]]
						else:
							pass

						for l in range(len(facenodes)):
							if elements[j].type in ['ROD2N2D', 'ROD2N', 'BEAM2N2D', 'BEAM2N']:
								break
							glBegin(GL_TRIANGLES)
							for k in range(len(disp_mag_values)):
								if solution not in elements[j].solutions:
									disp_color = (0.1, 0.1, 0.1)
								elif subresult == 'VonMises' and ( \
										nodes[elements[j].nodes[facenodes[l][0]].number].solutions[solution]['avg_strain']['VonMises'] > disp_mag_values[k]):
										pass
								elif subresult == 'MaxPrinc' and ( \
										nodes[elements[j].nodes[facenodes[l][0]].number].solutions[solution]['avg_strain']['MaxPrinc'] > disp_mag_values[k]):
										pass
								elif subresult == 'MinPrinc' and ( \
										nodes[elements[j].nodes[facenodes[l][0]].number].solutions[solution]['avg_strain']['MinPrinc'] > disp_mag_values[k]):
										pass
								elif subresult == 'MaxShear' and ( \
										nodes[elements[j].nodes[facenodes[l][0]].number].solutions[solution]['avg_strain']['MaxShear'] > disp_mag_values[k]):
										pass
								else:
									disp_color = disp_colors[k]
									break
							glColor3f(disp_color[0], disp_color[1], disp_color[2])
							glVertex3f(nodes[elements[j].nodes[facenodes[l][0]].number].coord[0][0] + 
										scale_factor*(displacements[elements[j].nodes[facenodes[l][0]].number].solutions[solution]['displacement'][0]),
									   nodes[elements[j].nodes[facenodes[l][0]].number].coord[1][0] +
										scale_factor*(displacements[elements[j].nodes[facenodes[l][0]].number].solutions[solution]['displacement'][1]),
									   nodes[elements[j].nodes[facenodes[l][0]].number].coord[2][0] +
										scale_factor*(displacements[elements[j].nodes[facenodes[l][0]].number].solutions[solution]['displacement'][2]))
							for k in range(len(disp_mag_values)):
								if solution not in elements[j].solutions:
									disp_color = (0.1, 0.1, 0.1)
								elif subresult == 'VonMises' and ( \
										nodes[elements[j].nodes[facenodes[l][1]].number].solutions[solution]['avg_strain']['VonMises'] > disp_mag_values[k]):
										pass
								elif subresult == 'MaxPrinc' and ( \
										nodes[elements[j].nodes[facenodes[l][1]].number].solutions[solution]['avg_strain']['MaxPrinc'] > disp_mag_values[k]):
										pass
								elif subresult == 'MinPrinc' and ( \
										nodes[elements[j].nodes[facenodes[l][1]].number].solutions[solution]['avg_strain']['MinPrinc'] > disp_mag_values[k]):
										pass
								elif subresult == 'MaxShear' and ( \
										nodes[elements[j].nodes[facenodes[l][1]].number].solutions[solution]['avg_strain']['MaxShear'] > disp_mag_values[k]):
										pass
								else:
									disp_color = disp_colors[k]
									break
							glColor3f(disp_color[0], disp_color[1], disp_color[2])
							glVertex3f(nodes[elements[j].nodes[facenodes[l][1]].number].coord[0][0] + 
										scale_factor*(displacements[elements[j].nodes[facenodes[l][1]].number].solutions[solution]['displacement'][0]),
									   nodes[elements[j].nodes[facenodes[l][1]].number].coord[1][0] +
										scale_factor*(displacements[elements[j].nodes[facenodes[l][1]].number].solutions[solution]['displacement'][1]),
									   nodes[elements[j].nodes[facenodes[l][1]].number].coord[2][0] +
										scale_factor*(displacements[elements[j].nodes[facenodes[l][1]].number].solutions[solution]['displacement'][2]))
							for k in range(len(disp_mag_values)):
								if ((elements[j].type == 'QUAD8N') and (facenodes[l][2] == 8)) or \
									((elements[j].type == 'HEX20N') and (facenodes[l][2] in [20,21,22,23,24,25])):
									if solution not in elements[j].solutions:
										disp_color = (0.1, 0.1, 0.1)
									elif subresult == 'VonMises' and ( \
											elements[j].solutions[solution]['strain']['nodal'][facenodes[l][2]+1]['VonMises'] > disp_mag_values[k]):
											pass
									elif subresult == 'MaxPrinc' and ( \
											elements[j].solutions[solution]['strain']['nodal'][facenodes[l][2]+1]['MaxPrinc'] > disp_mag_values[k]):
											pass
									elif subresult == 'MinPrinc' and ( \
											elements[j].solutions[solution]['strain']['nodal'][facenodes[l][2]+1]['MinPrinc'] > disp_mag_values[k]):
											pass
									elif subresult == 'MaxShear' and ( \
											elements[j].solutions[solution]['strain']['nodal'][facenodes[l][2]+1]['MaxShear'] > disp_mag_values[k]):
											pass
									else:
										disp_color = disp_colors[k]
										break
								else:
									if solution not in elements[j].solutions:
										disp_color = (0.1, 0.1, 0.1)
									elif subresult == 'VonMises' and ( \
											nodes[elements[j].nodes[facenodes[l][2]].number].solutions[solution]['avg_strain']['VonMises'] > disp_mag_values[k]):
											pass
									elif subresult == 'MaxPrinc' and ( \
											nodes[elements[j].nodes[facenodes[l][2]].number].solutions[solution]['avg_strain']['MaxPrinc'] > disp_mag_values[k]):
											pass
									elif subresult == 'MinPrinc' and ( \
											nodes[elements[j].nodes[facenodes[l][2]].number].solutions[solution]['avg_strain']['MinPrinc'] > disp_mag_values[k]):
											pass
									elif subresult == 'MaxShear' and ( \
											nodes[elements[j].nodes[facenodes[l][2]].number].solutions[solution]['avg_strain']['MaxShear'] > disp_mag_values[k]):
											pass
									else:
										disp_color = disp_colors[k]
										break
							glColor3f(disp_color[0], disp_color[1], disp_color[2])
							if (elements[j].type == 'QUAD8N') and (facenodes[l][2] == 8):
								glVertex3f( (nodes[elements[j].nodes[0].number].coord[0][0] + nodes[elements[j].nodes[4].number].coord[0][0])/2. + \
											scale_factor*( (displacements[elements[j].nodes[0].number].solutions[solution]['displacement'][0] + \
															displacements[elements[j].nodes[4].number].solutions[solution]['displacement'][0])/2.),
										    (nodes[elements[j].nodes[0].number].coord[1][0] + nodes[elements[j].nodes[4].number].coord[1][0])/2. + \
											scale_factor*( (displacements[elements[j].nodes[0].number].solutions[solution]['displacement'][1] + \
															displacements[elements[j].nodes[4].number].solutions[solution]['displacement'][1])/2.),
										    (nodes[elements[j].nodes[0].number].coord[2][0] + nodes[elements[j].nodes[4].number].coord[2][0])/2. + \
											scale_factor*( (displacements[elements[j].nodes[0].number].solutions[solution]['displacement'][2] + \
															displacements[elements[j].nodes[4].number].solutions[solution]['displacement'][2])/2.) )
							elif (elements[j].type == 'HEX20N') and (facenodes[l][2] in [20,21,22,23,24,25]):
								node_a = 1
								node_b = 2
								if facenodes[l][2] == 20:
									node_a = 0
									node_b = 2
								elif facenodes[l][2] == 21:
									node_a = 4
									node_b = 6
								elif facenodes[l][2] == 22:
									node_a = 0
									node_b = 5
								elif facenodes[l][2] == 23:
									node_a = 1
									node_b = 6
								elif facenodes[l][2] == 24:
									node_a = 2
									node_b = 7
								elif facenodes[l][2] == 25:
									node_a = 3
									node_b = 4
								else:
									pass
								glVertex3f( (nodes[elements[j].nodes[node_a].number].coord[0][0] + nodes[elements[j].nodes[node_b].number].coord[0][0])/2. + \
											scale_factor*( (displacements[elements[j].nodes[0].number].solutions[solution]['displacement'][0] + \
															displacements[elements[j].nodes[4].number].solutions[solution]['displacement'][0])/2.),
										    (nodes[elements[j].nodes[node_a].number].coord[1][0] + nodes[elements[j].nodes[node_b].number].coord[1][0])/2. + \
											scale_factor*( (displacements[elements[j].nodes[0].number].solutions[solution]['displacement'][1] + \
															displacements[elements[j].nodes[4].number].solutions[solution]['displacement'][1])/2.),
										    (nodes[elements[j].nodes[node_a].number].coord[2][0] + nodes[elements[j].nodes[node_b].number].coord[2][0])/2. + \
											scale_factor*( (displacements[elements[j].nodes[0].number].solutions[solution]['displacement'][2] + \
															displacements[elements[j].nodes[4].number].solutions[solution]['displacement'][2])/2.) )
							else:
								glVertex3f(nodes[elements[j].nodes[facenodes[l][2]].number].coord[0][0] + 
											scale_factor*(displacements[elements[j].nodes[facenodes[l][2]].number].solutions[solution]['displacement'][0]),
										   nodes[elements[j].nodes[facenodes[l][2]].number].coord[1][0] +
											scale_factor*(displacements[elements[j].nodes[facenodes[l][2]].number].solutions[solution]['displacement'][1]),
										   nodes[elements[j].nodes[facenodes[l][2]].number].coord[2][0] +
											scale_factor*(displacements[elements[j].nodes[facenodes[l][2]].number].solutions[solution]['displacement'][2]))
							glEnd()
					glEndList()

				else:
					pass


			elif self.results[newResult].solutions[solution].type == 'Eigenmodes':

				if result == 'modeshapes':
						mode = int(subresult[4:])-1
						vect_max = 0.
						eigenvector = []
						is3D = self.results[newResult].solutions[solution].mesh.is3D
						for DOF in range(mesh.nDOFs):
							if abs(self.results[newResult].solutions[solution].eigenvectors[DOF,mode]) > vect_max:
								vect_max = abs(self.results[newResult].solutions[solution].eigenvectors[DOF,mode])
						for DOF in range(mesh.nDOFs):
							eigenvector.append(self.results[newResult].solutions[solution].eigenvectors[DOF,mode]/vect_max)

						self.displayLists[solution][result][subresult] = \
														{'info': '%.4E Hertz' % (self.results[newResult].solutions[solution].eigenfrequencies[mode])}

						for frame in range(13):
							self.displayLists[solution][result][subresult][frame] = {}
							self.displayLists[solution][result][subresult][frame]['nodes'] = glGenLists(1)
							self.displayLists[solution][result][subresult][frame]['wireframe'] = glGenLists(1)
							self.displayLists[solution][result][subresult][frame]['shaded'] = glGenLists(1)

							move = (frame-6)*0.1*self.scale_factor
							# nodes modelled with displacement
							glNewList(self.displayLists[solution][result][subresult][frame]['nodes'], GL_COMPILE)

							glPointSize(5.0)
							glBegin(GL_POINTS)
							glColor3f(0.0, 0.2, 0.0)
							if is3D:
								for i in nodes:
									glVertex3f(nodes[i].coord[0][0] + move*eigenvector[mesh.NFMT[nodes[i].number]], 
											   nodes[i].coord[1][0] + move*eigenvector[mesh.NFMT[nodes[i].number]+1],
											   nodes[i].coord[2][0] + move*eigenvector[mesh.NFMT[nodes[i].number]+2])
							else:
								for i in nodes:
									glVertex3f(nodes[i].coord[0][0] + move*eigenvector[mesh.NFMT[nodes[i].number]], 
											   nodes[i].coord[1][0] + move*eigenvector[mesh.NFMT[nodes[i].number]+1],
											   0.)
							glEnd()
							glEndList()

							# wireframe mode, model with displacement, lines only
							glNewList(self.displayLists[solution][result][subresult][frame]['wireframe'], GL_COMPILE)

							glLineWidth(3.0)
							for j in elements:
								nodelines = []
								if elements[j].type == 'ROD2N2D':
									nodelines = [[0,1]]
								if elements[j].type == 'ROD2N':
									nodelines = [[0,1]]
								if elements[j].type == 'BEAM2N2D':
									nodelines = [[0,1]]
								if elements[j].type == 'BEAM2N':
									nodelines = [[0,1]]
								if elements[j].type == 'TRI3N':
									nodelines = [[0,1], [1,2], [2,0]]
								if elements[j].type == 'TRI6N':
									nodelines = [[0,3], [3,1], [1,4], [4,2], [2,5], [5,0]]
								if elements[j].type == 'QUAD4N':
									nodelines = [[0,1], [1,2], [2,3], [0,3]]
								if elements[j].type == 'QUAD8N':
									nodelines = [[0,1], [1,2], [2,3], [3,4], [4,5], [5,6], [6,7], [7,0]]
								if elements[j].type == 'TET4N':
									nodelines = [[0,1], [1,2], [0,2], [0,3], [1,3], [2,3]]
								if elements[j].type == 'TET10N':
									nodelines = [[0,4], [1,4], [1,5], [2,5], [0,6], [2,6], [0,7], [3,7], [1,8], [3,8], [2,9], [3,9]]
								if elements[j].type == 'HEX8N':
									nodelines = [[0,1], [1,2], [2,3], [0,3], [0,4], [1,5], [2,6], [3,7], [4,5], [5,6], [6,7], [4,7]]
								if elements[j].type == 'HEX20N':
									nodelines = [[ 0, 8], [ 8, 1], [ 1, 9], [ 9, 2], [ 2,10], [10, 3], [ 3,11], [11, 0], 
												 [ 0,12], [12, 4], [ 1,13], [13, 5], [ 2,14], [14, 6], [ 3,15], [15, 7],
												 [ 4,16], [16, 5], [ 5,17], [17, 6], [ 6,18], [18, 7], [ 7,19], [19, 4]]

								if is3D:
									for k in range(len(nodelines)):
										glBegin(GL_LINES)
										glColor3f(0.0, 0.2, 0.0)
										glVertex3f(nodes[elements[j].nodes[nodelines[k][0]].number].coord[0][0] + 
													move*eigenvector[mesh.NFMT[nodes[elements[j].nodes[nodelines[k][0]].number].number]],
												   nodes[elements[j].nodes[nodelines[k][0]].number].coord[1][0] +
													move*eigenvector[mesh.NFMT[nodes[elements[j].nodes[nodelines[k][0]].number].number]+1],
												   nodes[elements[j].nodes[nodelines[k][0]].number].coord[2][0] +
													move*eigenvector[mesh.NFMT[nodes[elements[j].nodes[nodelines[k][0]].number].number]+2])
										glVertex3f(nodes[elements[j].nodes[nodelines[k][1]].number].coord[0][0] +
													move*eigenvector[mesh.NFMT[nodes[elements[j].nodes[nodelines[k][1]].number].number]],
												   nodes[elements[j].nodes[nodelines[k][1]].number].coord[1][0] +
													move*eigenvector[mesh.NFMT[nodes[elements[j].nodes[nodelines[k][1]].number].number]+1],
												   nodes[elements[j].nodes[nodelines[k][1]].number].coord[2][0] +
													move*eigenvector[mesh.NFMT[nodes[elements[j].nodes[nodelines[k][1]].number].number]+2])
										glEnd()
								else:
									for k in range(len(nodelines)):
										glBegin(GL_LINES)
										glColor3f(0.0, 0.2, 0.0)
										glVertex3f(nodes[elements[j].nodes[nodelines[k][0]].number].coord[0][0] + 
													move*eigenvector[mesh.NFMT[nodes[elements[j].nodes[nodelines[k][0]].number].number]],
												   nodes[elements[j].nodes[nodelines[k][0]].number].coord[1][0] +
													move*eigenvector[mesh.NFMT[nodes[elements[j].nodes[nodelines[k][0]].number].number]+1], 0.)
										glVertex3f(nodes[elements[j].nodes[nodelines[k][1]].number].coord[0][0] +
													move*eigenvector[mesh.NFMT[nodes[elements[j].nodes[nodelines[k][1]].number].number]],
												   nodes[elements[j].nodes[nodelines[k][1]].number].coord[1][0] +
													move*eigenvector[mesh.NFMT[nodes[elements[j].nodes[nodelines[k][1]].number].number]+1], 0.)
										glEnd()

							glEndList()

							# shaded mode, model with displacement, green elements
							glNewList(self.displayLists[solution][result][subresult][frame]['shaded'], GL_COMPILE)

							for j in elements:
								facenodes = []
								if elements[j].type == 'TRI3N':
									facenodes = [[0,1,2]]
								if elements[j].type == 'TRI6N':
									facenodes = [[0,3,5], [3,1,4], [4,2,5], [5,3,4]]
								if elements[j].type == 'QUAD4N':
									facenodes = [[0,1,3], [1,2,3]]
								if elements[j].type == 'QUAD8N':
									facenodes = [[0,1,7], [1,2,3], [3,4,5], [5,6,7], [1,3,7], [5,7,3]]
								if elements[j].type == 'TET4N':
									facenodes = [[0,1,3], [1,2,3], [2,0,3], [0,2,1]]
								if elements[j].type == 'TET10N':
									facenodes = [[0,4,7], [7,4,8], [8,4,1], [7,8,3], [1,5,8], [8,5,9], [9,3,8], [5,2,9],
												 [2,6,9], [9,6,7], [6,0,7], [9,7,3], [5,6,2], [4,0,6], [6,5,4], [4,5,1]]
								if elements[j].type == 'HEX8N':
									facenodes = [[2,1,0], [0,3,2], [3,7,2], [2,7,6], [7,3,0], [0,4,7], [5,6,7], [7,4,5],
												 [1,2,6], [1,6,5], [1,4,0], [5,4,1]]
								if elements[j].type == 'HEX20N':
									facenodes = [[ 0, 8,12], [ 8, 1,13], [13, 5,16], [16, 4,12], [ 8,13,12], [12,13,16],
												 [ 2,10,14], [10, 3,15], [15, 7,18], [18, 6,14], [15,14,10], [18,14,15],
												 [ 1, 9,13], [ 9, 2,14], [14, 6,17], [17, 5,13], [13, 9,14], [13,14,17],
												 [ 3,11,15], [15,19, 7], [19,12, 4], [12,11, 0], [12,15,11], [12,19,15],
												 [ 9, 1, 8], [ 2, 9,10], [ 3,10,11], [ 0,11, 8], [ 9, 8,10], [10, 8,11],
												 [ 5,17,16], [17, 6,18], [18, 7,19], [19, 4,16], [16,17,18], [18,19,16]]

								if is3D:
									for l in range(len(facenodes)):
										glBegin(GL_TRIANGLES)

										glColor3f(0.0, 0.7, 0.0)
										glVertex3f(nodes[elements[j].nodes[facenodes[l][0]].number].coord[0][0] + 
													move*eigenvector[mesh.NFMT[elements[j].nodes[facenodes[l][0]].number]],
												   nodes[elements[j].nodes[facenodes[l][0]].number].coord[1][0] +
													move*eigenvector[mesh.NFMT[elements[j].nodes[facenodes[l][0]].number]+1],
												   nodes[elements[j].nodes[facenodes[l][0]].number].coord[2][0] +
													move*eigenvector[mesh.NFMT[elements[j].nodes[facenodes[l][0]].number]+2])

										glVertex3f(nodes[elements[j].nodes[facenodes[l][1]].number].coord[0][0] + 
													move*eigenvector[mesh.NFMT[elements[j].nodes[facenodes[l][1]].number]],
												   nodes[elements[j].nodes[facenodes[l][1]].number].coord[1][0] +
													move*eigenvector[mesh.NFMT[elements[j].nodes[facenodes[l][1]].number]+1],
												   nodes[elements[j].nodes[facenodes[l][1]].number].coord[2][0] +
													move*eigenvector[mesh.NFMT[elements[j].nodes[facenodes[l][1]].number]+2])

										glVertex3f(nodes[elements[j].nodes[facenodes[l][2]].number].coord[0][0] + 
													move*eigenvector[mesh.NFMT[elements[j].nodes[facenodes[l][2]].number]],
												   nodes[elements[j].nodes[facenodes[l][2]].number].coord[1][0] +
													move*eigenvector[mesh.NFMT[elements[j].nodes[facenodes[l][2]].number]+1],
												   nodes[elements[j].nodes[facenodes[l][2]].number].coord[2][0] +
													move*eigenvector[mesh.NFMT[elements[j].nodes[facenodes[l][2]].number]+2])
										glEnd()
								else:
									for l in range(len(facenodes)):
										glBegin(GL_TRIANGLES)

										glColor3f(0.0, 0.7, 0.0)
										glVertex3f(nodes[elements[j].nodes[facenodes[l][0]].number].coord[0][0] + 
													move*eigenvector[mesh.NFMT[elements[j].nodes[facenodes[l][0]].number]],
												   nodes[elements[j].nodes[facenodes[l][0]].number].coord[1][0] +
													move*eigenvector[mesh.NFMT[elements[j].nodes[facenodes[l][0]].number]+1], 0.)

										glVertex3f(nodes[elements[j].nodes[facenodes[l][1]].number].coord[0][0] + 
													move*eigenvector[mesh.NFMT[elements[j].nodes[facenodes[l][1]].number]],
												   nodes[elements[j].nodes[facenodes[l][1]].number].coord[1][0] +
													move*eigenvector[mesh.NFMT[elements[j].nodes[facenodes[l][1]].number]+1], 0.)

										glVertex3f(nodes[elements[j].nodes[facenodes[l][2]].number].coord[0][0] + 
													move*eigenvector[mesh.NFMT[elements[j].nodes[facenodes[l][2]].number]],
												   nodes[elements[j].nodes[facenodes[l][2]].number].coord[1][0] +
													move*eigenvector[mesh.NFMT[elements[j].nodes[facenodes[l][2]].number]+1], 0.)
										glEnd()


								if elements[j].type in ['BEAM2N2D', 'BEAM2N', 'ROD2N2D', 'ROD2N']:
									if hasattr(elements[j],'crossSection'):
										if hasattr(elements[j],'orientation'):
											if elements[j].type in ['BEAM2N2D', 'BEAM2N']:
												node1_coord = [nodes[elements[j].nodes[0].number].coord[0][0] + 
																move*eigenvector[mesh.NFMT[elements[j].nodes[0].number]],
															   nodes[elements[j].nodes[0].number].coord[1][0] +
																move*eigenvector[mesh.NFMT[elements[j].nodes[0].number]+1], 0.]
												node2_coord = [nodes[elements[j].nodes[1].number].coord[0][0] + 
																move*eigenvector[mesh.NFMT[elements[j].nodes[1].number]],
															   nodes[elements[j].nodes[1].number].coord[1][0] +
																move*eigenvector[mesh.NFMT[elements[j].nodes[1].number]+1], 0.]
												if is3D:
													node1_coord[2] = nodes[elements[j].nodes[0].number].coord[2][0] + \
																	  move*eigenvector[mesh.NFMT[elements[j].nodes[0].number]+2]
													node1_rotation = [move*eigenvector[mesh.NFMT[elements[j].nodes[0].number]+3],
																	  move*eigenvector[mesh.NFMT[elements[j].nodes[0].number]+4],
																	  move*eigenvector[mesh.NFMT[elements[j].nodes[0].number]+5]]
													node2_coord[2] = nodes[elements[j].nodes[1].number].coord[2][0] + \
																	  move*eigenvector[mesh.NFMT[elements[j].nodes[1].number]+2]
													node2_rotation = [move*eigenvector[mesh.NFMT[elements[j].nodes[1].number]+3],
																	  move*eigenvector[mesh.NFMT[elements[j].nodes[1].number]+4],
																	  move*eigenvector[mesh.NFMT[elements[j].nodes[1].number]+5]]
												else:
													node1_rotation = [0., 0., move*eigenvector[mesh.NFMT[elements[j].nodes[0].number]+2]]
													node2_rotation = [0., 0., move*eigenvector[mesh.NFMT[elements[j].nodes[1].number]+2]]
											else:
												node1_coord = [nodes[elements[j].nodes[0].number].coord[0][0] + 
																move*eigenvector[mesh.NFMT[elements[j].nodes[0].number]],
															   nodes[elements[j].nodes[0].number].coord[1][0] +
																move*eigenvector[mesh.NFMT[elements[j].nodes[0].number]+1], 0.]
												node2_coord = [nodes[elements[j].nodes[1].number].coord[0][0] + 
																move*eigenvector[mesh.NFMT[elements[j].nodes[1].number]],
															   nodes[elements[j].nodes[1].number].coord[1][0] +
																move*eigenvector[mesh.NFMT[elements[j].nodes[1].number]+1], 0.]
												if is3D:
													node1_coord[2] = nodes[elements[j].nodes[0].number].coord[2][0] + \
																	  move*eigenvector[mesh.NFMT[elements[j].nodes[0].number]+2]
													node1_rotation = [0.,0.,0.]
													node2_coord[2] = nodes[elements[j].nodes[1].number].coord[2][0] + \
																	  move*eigenvector[mesh.NFMT[elements[j].nodes[1].number]+2]
													node2_rotation = [0.,0.,0.]
												else:
													node1_rotation = [0., 0., 0.]
													node2_rotation = [0., 0., 0.]
												
											faces = []
											lines = []
											x_vec = elements[j].orientation['x-vec']
											y_vec = elements[j].orientation['y-vec']
											z_vec = elements[j].orientation['z-vec']

											if elements[j].crossSection['Type'] == 'Rectangle':

												w  = elements[j].crossSection['width, w']
												h  = elements[j].crossSection['height, h']
												iw = elements[j].crossSection['inner width, iw']
												ih = elements[j].crossSection['inner height, ih']
												w  = w/2.
												h  = h/2.
												iw = iw/2.
												ih = ih/2.
												v_11 = [node1_coord[0]-y_vec[0]*h-z_vec[0]*w,
														node1_coord[1]-y_vec[1]*h-z_vec[1]*w,
														node1_coord[2]-y_vec[2]*h-z_vec[2]*w ]
												v_12 = [node1_coord[0]-y_vec[0]*h+z_vec[0]*w,
														node1_coord[1]-y_vec[1]*h+z_vec[1]*w,
														node1_coord[2]-y_vec[2]*h+z_vec[2]*w ]
												v_13 = [node1_coord[0]+y_vec[0]*h+z_vec[0]*w,
														node1_coord[1]+y_vec[1]*h+z_vec[1]*w,
														node1_coord[2]+y_vec[2]*h+z_vec[2]*w ]
												v_14 = [node1_coord[0]+y_vec[0]*h-z_vec[0]*w,
														node1_coord[1]+y_vec[1]*h-z_vec[1]*w,
														node1_coord[2]+y_vec[2]*h-z_vec[2]*w ]
												v_21 = [node2_coord[0]-y_vec[0]*h-z_vec[0]*w,
														node2_coord[1]-y_vec[1]*h-z_vec[1]*w,
														node2_coord[2]-y_vec[2]*h-z_vec[2]*w ]
												v_22 = [node2_coord[0]-y_vec[0]*h+z_vec[0]*w,
														node2_coord[1]-y_vec[1]*h+z_vec[1]*w,
														node2_coord[2]-y_vec[2]*h+z_vec[2]*w ]
												v_23 = [node2_coord[0]+y_vec[0]*h+z_vec[0]*w,
														node2_coord[1]+y_vec[1]*h+z_vec[1]*w,
														node2_coord[2]+y_vec[2]*h+z_vec[2]*w ]
												v_24 = [node2_coord[0]+y_vec[0]*h-z_vec[0]*w,
														node2_coord[1]+y_vec[1]*h-z_vec[1]*w,
														node2_coord[2]+y_vec[2]*h-z_vec[2]*w ]
												v_11 = rotatePointAboutAxis(v_11,node1_coord,[node1_coord[0]+1,node1_coord[1],node1_coord[2]],node1_rotation[0])
												v_11 = rotatePointAboutAxis(v_11,node1_coord,[node1_coord[0],node1_coord[1]+1,node1_coord[2]],node1_rotation[1])
												v_11 = rotatePointAboutAxis(v_11,node1_coord,[node1_coord[0],node1_coord[1],node1_coord[2]+1],node1_rotation[2])
												v_12 = rotatePointAboutAxis(v_12,node1_coord,[node1_coord[0]+1,node1_coord[1],node1_coord[2]],node1_rotation[0])
												v_12 = rotatePointAboutAxis(v_12,node1_coord,[node1_coord[0],node1_coord[1]+1,node1_coord[2]],node1_rotation[1])
												v_12 = rotatePointAboutAxis(v_12,node1_coord,[node1_coord[0],node1_coord[1],node1_coord[2]+1],node1_rotation[2])
												v_13 = rotatePointAboutAxis(v_13,node1_coord,[node1_coord[0]+1,node1_coord[1],node1_coord[2]],node1_rotation[0])
												v_13 = rotatePointAboutAxis(v_13,node1_coord,[node1_coord[0],node1_coord[1]+1,node1_coord[2]],node1_rotation[1])
												v_13 = rotatePointAboutAxis(v_13,node1_coord,[node1_coord[0],node1_coord[1],node1_coord[2]+1],node1_rotation[2])
												v_14 = rotatePointAboutAxis(v_14,node1_coord,[node1_coord[0]+1,node1_coord[1],node1_coord[2]],node1_rotation[0])
												v_14 = rotatePointAboutAxis(v_14,node1_coord,[node1_coord[0],node1_coord[1]+1,node1_coord[2]],node1_rotation[1])
												v_14 = rotatePointAboutAxis(v_14,node1_coord,[node1_coord[0],node1_coord[1],node1_coord[2]+1],node1_rotation[2])
												v_21 = rotatePointAboutAxis(v_21,node2_coord,[node2_coord[0]+1,node2_coord[1],node2_coord[2]],node2_rotation[0])
												v_21 = rotatePointAboutAxis(v_21,node2_coord,[node2_coord[0],node2_coord[1]+1,node2_coord[2]],node2_rotation[1])
												v_21 = rotatePointAboutAxis(v_21,node2_coord,[node2_coord[0],node2_coord[1],node2_coord[2]+1],node2_rotation[2])
												v_22 = rotatePointAboutAxis(v_22,node2_coord,[node2_coord[0]+1,node2_coord[1],node2_coord[2]],node2_rotation[0])
												v_22 = rotatePointAboutAxis(v_22,node2_coord,[node2_coord[0],node2_coord[1]+1,node2_coord[2]],node2_rotation[1])
												v_22 = rotatePointAboutAxis(v_22,node2_coord,[node2_coord[0],node2_coord[1],node2_coord[2]+1],node2_rotation[2])
												v_23 = rotatePointAboutAxis(v_23,node2_coord,[node2_coord[0]+1,node2_coord[1],node2_coord[2]],node2_rotation[0])
												v_23 = rotatePointAboutAxis(v_23,node2_coord,[node2_coord[0],node2_coord[1]+1,node2_coord[2]],node2_rotation[1])
												v_23 = rotatePointAboutAxis(v_23,node2_coord,[node2_coord[0],node2_coord[1],node2_coord[2]+1],node2_rotation[2])
												v_24 = rotatePointAboutAxis(v_24,node2_coord,[node2_coord[0]+1,node2_coord[1],node2_coord[2]],node2_rotation[0])
												v_24 = rotatePointAboutAxis(v_24,node2_coord,[node2_coord[0],node2_coord[1]+1,node2_coord[2]],node2_rotation[1])
												v_24 = rotatePointAboutAxis(v_24,node2_coord,[node2_coord[0],node2_coord[1],node2_coord[2]+1],node2_rotation[2])
												if iw != 0. or ih != 0.:
													v_15 = [node1_coord[0]-y_vec[0]*ih-z_vec[0]*iw,
															node1_coord[1]-y_vec[1]*ih-z_vec[1]*iw,
															node1_coord[2]-y_vec[2]*ih-z_vec[2]*iw ]
													v_16 = [node1_coord[0]-y_vec[0]*ih+z_vec[0]*iw,
															node1_coord[1]-y_vec[1]*ih+z_vec[1]*iw,
															node1_coord[2]-y_vec[2]*ih+z_vec[2]*iw ]
													v_17 = [node1_coord[0]+y_vec[0]*ih+z_vec[0]*iw,
															node1_coord[1]+y_vec[1]*ih+z_vec[1]*iw,
															node1_coord[2]+y_vec[2]*ih+z_vec[2]*iw ]
													v_18 = [node1_coord[0]+y_vec[0]*ih-z_vec[0]*iw,
															node1_coord[1]+y_vec[1]*ih-z_vec[1]*iw,
															node1_coord[2]+y_vec[2]*ih-z_vec[2]*iw ]
													v_25 = [node2_coord[0]-y_vec[0]*ih-z_vec[0]*iw,
															node2_coord[1]-y_vec[1]*ih-z_vec[1]*iw,
															node2_coord[2]-y_vec[2]*ih-z_vec[2]*iw ]
													v_26 = [node2_coord[0]-y_vec[0]*ih+z_vec[0]*iw,
															node2_coord[1]-y_vec[1]*ih+z_vec[1]*iw,
															node2_coord[2]-y_vec[2]*ih+z_vec[2]*iw ]
													v_27 = [node2_coord[0]+y_vec[0]*ih+z_vec[0]*iw,
															node2_coord[1]+y_vec[1]*ih+z_vec[1]*iw,
															node2_coord[2]+y_vec[2]*ih+z_vec[2]*iw ]
													v_28 = [node2_coord[0]+y_vec[0]*ih-z_vec[0]*iw,
															node2_coord[1]+y_vec[1]*ih-z_vec[1]*iw,
															node2_coord[2]+y_vec[2]*ih-z_vec[2]*iw ]
													v_15 = rotatePointAboutAxis(v_15,node1_coord,[node1_coord[0]+1,node1_coord[1],node1_coord[2]],node1_rotation[0])
													v_15 = rotatePointAboutAxis(v_15,node1_coord,[node1_coord[0],node1_coord[1]+1,node1_coord[2]],node1_rotation[1])
													v_15 = rotatePointAboutAxis(v_15,node1_coord,[node1_coord[0],node1_coord[1],node1_coord[2]+1],node1_rotation[2])
													v_16 = rotatePointAboutAxis(v_16,node1_coord,[node1_coord[0]+1,node1_coord[1],node1_coord[2]],node1_rotation[0])
													v_16 = rotatePointAboutAxis(v_16,node1_coord,[node1_coord[0],node1_coord[1]+1,node1_coord[2]],node1_rotation[1])
													v_16 = rotatePointAboutAxis(v_16,node1_coord,[node1_coord[0],node1_coord[1],node1_coord[2]+1],node1_rotation[2])
													v_17 = rotatePointAboutAxis(v_17,node1_coord,[node1_coord[0]+1,node1_coord[1],node1_coord[2]],node1_rotation[0])
													v_17 = rotatePointAboutAxis(v_17,node1_coord,[node1_coord[0],node1_coord[1]+1,node1_coord[2]],node1_rotation[1])
													v_17 = rotatePointAboutAxis(v_17,node1_coord,[node1_coord[0],node1_coord[1],node1_coord[2]+1],node1_rotation[2])
													v_18 = rotatePointAboutAxis(v_18,node1_coord,[node1_coord[0]+1,node1_coord[1],node1_coord[2]],node1_rotation[0])
													v_18 = rotatePointAboutAxis(v_18,node1_coord,[node1_coord[0],node1_coord[1]+1,node1_coord[2]],node1_rotation[1])
													v_18 = rotatePointAboutAxis(v_18,node1_coord,[node1_coord[0],node1_coord[1],node1_coord[2]+1],node1_rotation[2])
													v_25 = rotatePointAboutAxis(v_25,node2_coord,[node2_coord[0]+1,node2_coord[1],node2_coord[2]],node2_rotation[0])
													v_25 = rotatePointAboutAxis(v_25,node2_coord,[node2_coord[0],node2_coord[1]+1,node2_coord[2]],node2_rotation[1])
													v_25 = rotatePointAboutAxis(v_25,node2_coord,[node2_coord[0],node2_coord[1],node2_coord[2]+1],node2_rotation[2])
													v_26 = rotatePointAboutAxis(v_26,node2_coord,[node2_coord[0]+1,node2_coord[1],node2_coord[2]],node2_rotation[0])
													v_26 = rotatePointAboutAxis(v_26,node2_coord,[node2_coord[0],node2_coord[1]+1,node2_coord[2]],node2_rotation[1])
													v_26 = rotatePointAboutAxis(v_26,node2_coord,[node2_coord[0],node2_coord[1],node2_coord[2]+1],node2_rotation[2])
													v_27 = rotatePointAboutAxis(v_27,node2_coord,[node2_coord[0]+1,node2_coord[1],node2_coord[2]],node2_rotation[0])
													v_27 = rotatePointAboutAxis(v_27,node2_coord,[node2_coord[0],node2_coord[1]+1,node2_coord[2]],node2_rotation[1])
													v_27 = rotatePointAboutAxis(v_27,node2_coord,[node2_coord[0],node2_coord[1],node2_coord[2]+1],node2_rotation[2])
													v_28 = rotatePointAboutAxis(v_28,node2_coord,[node2_coord[0]+1,node2_coord[1],node2_coord[2]],node2_rotation[0])
													v_28 = rotatePointAboutAxis(v_28,node2_coord,[node2_coord[0],node2_coord[1]+1,node2_coord[2]],node2_rotation[1])
													v_28 = rotatePointAboutAxis(v_28,node2_coord,[node2_coord[0],node2_coord[1],node2_coord[2]+1],node2_rotation[2])

												lines = [[v_11,v_12],[v_12,v_13],[v_13,v_14],[v_14,v_11],
														 [v_21,v_22],[v_22,v_23],[v_23,v_24],[v_24,v_21],
														 [v_11,v_21],[v_12,v_22],[v_13,v_23],[v_14,v_24]]
												faces = [[v_13,v_12,v_22],[v_22,v_23,v_13],
														 [v_14,v_13,v_23],[v_23,v_24,v_14],
														 [v_11,v_14,v_24],[v_24,v_21,v_11],
														 [v_12,v_11,v_21],[v_21,v_22,v_12]]

												if iw == 0. or ih == 0.:
													faces += [[v_11,v_12,v_13],[v_13,v_14,v_11],
															  [v_21,v_24,v_23],[v_23,v_22,v_21]]
												else:
													lines += [[v_15,v_16],[v_16,v_17],[v_17,v_18],[v_18,v_15],
															  [v_25,v_26],[v_26,v_27],[v_27,v_28],[v_28,v_25],
															  [v_15,v_25],[v_16,v_26],[v_17,v_27],[v_18,v_28]]
													faces += [[v_15,v_11,v_12],[v_12,v_16,v_15],
															  [v_16,v_12,v_13],[v_13,v_17,v_16],
															  [v_17,v_13,v_14],[v_14,v_18,v_17],
															  [v_18,v_14,v_11],[v_11,v_15,v_18],
															  [v_26,v_22,v_21],[v_21,v_25,v_26],
															  [v_22,v_26,v_23],[v_26,v_27,v_23],
															  [v_23,v_27,v_24],[v_27,v_28,v_24],
															  [v_24,v_28,v_21],[v_25,v_21,v_28],
															  [v_17,v_27,v_16],[v_27,v_26,v_16],
															  [v_18,v_28,v_17],[v_28,v_27,v_17],
															  [v_15,v_25,v_18],[v_25,v_28,v_18],
															  [v_25,v_15,v_26],[v_15,v_16,v_26]]

											elif elements[j].crossSection['Type'] == 'Circle':

												r  = elements[j].crossSection['radius, r']
												ir  = elements[j].crossSection['inner radius, ir']
												vertices1 = []
												vertices2 = []
												pnts = 24
												for v in range(pnts):
													d = pnts/(v+1)
													vc = np.cos(2*np.pi/d)
													vs = np.sin(2*np.pi/d)
													vertices1.append([node1_coord[0]+vs*y_vec[0]*r+vc*z_vec[0]*r,
																	  node1_coord[1]+vs*y_vec[1]*r+vc*z_vec[1]*r,
																	  node1_coord[2]+vs*y_vec[2]*r+vc*z_vec[2]*r ])
													vertices1[v] = rotatePointAboutAxis(vertices1[v],node1_coord, \
																		[node1_coord[0]+1,node1_coord[1],node1_coord[2]],node1_rotation[0])
													vertices1[v] = rotatePointAboutAxis(vertices1[v],node1_coord, \
																		[node1_coord[0],node1_coord[1]+1,node1_coord[2]],node1_rotation[1])
													vertices1[v] = rotatePointAboutAxis(vertices1[v],node1_coord, \
																		[node1_coord[0],node1_coord[1],node1_coord[2]+1],node1_rotation[2])
													vertices2.append([node2_coord[0]+vs*y_vec[0]*r+vc*z_vec[0]*r,
																	  node2_coord[1]+vs*y_vec[1]*r+vc*z_vec[1]*r,
																	  node2_coord[2]+vs*y_vec[2]*r+vc*z_vec[2]*r ])
													vertices2[v] = rotatePointAboutAxis(vertices2[v],node2_coord, \
																		[node2_coord[0]+1,node2_coord[1],node2_coord[2]],node2_rotation[0])
													vertices2[v] = rotatePointAboutAxis(vertices2[v],node2_coord, \
																		[node2_coord[0],node2_coord[1]+1,node2_coord[2]],node2_rotation[1])
													vertices2[v] = rotatePointAboutAxis(vertices2[v],node2_coord, \
																		[node2_coord[0],node2_coord[1],node2_coord[2]+1],node2_rotation[2])
												if ir != 0.:
													ivertices1 = []
													ivertices2 = []
													for v in range(pnts):
														d = pnts/(v+1)
														vc = np.cos(2*np.pi/d)
														vs = np.sin(2*np.pi/d)
														ivertices1.append([node1_coord[0]+vs*y_vec[0]*ir+vc*z_vec[0]*ir,
																		   node1_coord[1]+vs*y_vec[1]*ir+vc*z_vec[1]*ir,
																		   node1_coord[2]+vs*y_vec[2]*ir+vc*z_vec[2]*ir ])
														ivertices1[v] = rotatePointAboutAxis(ivertices1[v],node1_coord, \
																		[node1_coord[0]+1,node1_coord[1],node1_coord[2]],node1_rotation[0])
														ivertices1[v] = rotatePointAboutAxis(ivertices1[v],node1_coord, \
																		[node1_coord[0],node1_coord[1]+1,node1_coord[2]],node1_rotation[1])
														ivertices1[v] = rotatePointAboutAxis(ivertices1[v],node1_coord, \
																		[node1_coord[0],node1_coord[1],node1_coord[2]+1],node1_rotation[2])
														ivertices2.append([node2_coord[0]+vs*y_vec[0]*ir+vc*z_vec[0]*ir,
																		   node2_coord[1]+vs*y_vec[1]*ir+vc*z_vec[1]*ir,
																		   node2_coord[2]+vs*y_vec[2]*ir+vc*z_vec[2]*ir ])
														ivertices2[v] = rotatePointAboutAxis(ivertices2[v],node2_coord, \
																		[node2_coord[0]+1,node2_coord[1],node2_coord[2]],node2_rotation[0])
														ivertices2[v] = rotatePointAboutAxis(ivertices2[v],node2_coord, \
																		[node2_coord[0],node2_coord[1]+1,node2_coord[2]],node2_rotation[1])
														ivertices2[v] = rotatePointAboutAxis(ivertices2[v],node2_coord, \
																		[node2_coord[0],node2_coord[1],node2_coord[2]+1],node2_rotation[2])

												lines = []
												faces = []
												for v in range(pnts):
													lines.append([vertices1[v-1],vertices1[v]])
													lines.append([vertices2[v-1],vertices2[v]])
												lines.append([vertices1[0],vertices2[0]])

												if ir != 0.:
													for v in range(pnts):
														lines.append([ivertices1[v-1],ivertices1[v]])
														lines.append([ivertices2[v-1],ivertices2[v]])
													lines.append([ivertices1[0],ivertices2[0]])
													for v in range(pnts-1):
														faces.append([ivertices1[v],vertices1[v],vertices1[v+1]])
														faces.append([vertices1[v+1],ivertices1[v+1],ivertices1[v]])
														faces.append([ivertices2[v],vertices2[v+1],vertices2[v]])
														faces.append([vertices2[v+1],ivertices2[v],ivertices2[v+1]])
														faces.append([vertices1[v],vertices2[v],vertices2[v+1]])
														faces.append([vertices2[v+1],vertices1[v+1],vertices1[v]])
														faces.append([ivertices1[v],ivertices1[v+1],ivertices2[v]])
														faces.append([ivertices1[v+1],ivertices2[v+1],ivertices2[v]])
													faces.append([ivertices1[-1],vertices1[-1],vertices1[0]])
													faces.append([vertices1[0],ivertices1[0],ivertices1[-1]])
													faces.append([ivertices2[-1],vertices2[0],vertices2[-1]])
													faces.append([vertices2[0],ivertices2[-1],ivertices2[0]])
													faces.append([vertices1[-1],vertices2[-1],vertices2[0]])
													faces.append([vertices2[0],vertices1[0],vertices1[-1]])
													faces.append([ivertices1[-1],ivertices1[0],ivertices2[-1]])
													faces.append([ivertices1[0],ivertices2[0],ivertices2[-1]])
													
												else:
													vertices1.append([node1_coord[0],
																	  node1_coord[1],
																	  node1_coord[2] ])
													vertices1[-1] = rotatePointAboutAxis(vertices1[-1],node1_coord, \
																		[node1_coord[0]+1,node1_coord[1],node1_coord[2]],node1_rotation[0])
													vertices1[-1] = rotatePointAboutAxis(vertices1[-1],node1_coord, \
																		[node1_coord[0],node1_coord[1]+1,node1_coord[2]],node1_rotation[1])
													vertices1[-1] = rotatePointAboutAxis(vertices1[-1],node1_coord, \
																		[node1_coord[0],node1_coord[1],node1_coord[2]+1],node1_rotation[2])
													vertices2.append([node2_coord[0],
																	  node2_coord[1],
																	  node2_coord[2] ])
													vertices2[-1] = rotatePointAboutAxis(vertices2[-1],node2_coord, \
																		[node2_coord[0]+1,node2_coord[1],node2_coord[2]],node2_rotation[0])
													vertices2[-1] = rotatePointAboutAxis(vertices2[-1],node2_coord, \
																		[node2_coord[0],node2_coord[1]+1,node2_coord[2]],node2_rotation[1])
													vertices2[-1] = rotatePointAboutAxis(vertices2[-1],node2_coord, \
																		[node2_coord[0],node2_coord[1],node2_coord[2]+1],node2_rotation[2])
													for v in range(pnts):
														faces.append([vertices1[-1],vertices1[v],vertices1[v+1]])
														faces.append([vertices2[-1],vertices2[v+1],vertices2[v]])
														faces.append([vertices1[v],vertices2[v],vertices2[v+1]])
														faces.append([vertices2[v+1],vertices1[v+1],vertices1[v]])
													faces.append([vertices1[-1],vertices1[-2],vertices1[0]])
													faces.append([vertices2[-1],vertices2[0],vertices2[-2]])
													faces.append([vertices1[-2],vertices2[-2],vertices2[0]])
													faces.append([vertices2[0],vertices1[0],vertices1[-2]])

											elif elements[j].crossSection['Type'] == 'L-Beam':

												bw = elements[j].crossSection['bottom width, bw']
												bt = elements[j].crossSection['bottom thickness, bt']
												st = elements[j].crossSection['side thickness, st']
												h  = elements[j].crossSection['height, h']
												A1  = st*(h-bt)
												A2  = bt*bw
												A   = A1+A2
												yC1 = (h/2.)+bt
												yC2 = bt/2.
												zC1 = st/2.
												zC2 = bw/2.
												if A != 0.:
													yC = (A1*yC1+A2*yC2)/A
													zC = (A1*zC1+A2*zC2)/A
												else:
													yC = 0.
													zC = 0.
												v_11  = [node1_coord[0]-y_vec[0]*yC-z_vec[0]*zC,
														 node1_coord[1]-y_vec[1]*yC-z_vec[1]*zC,
														 node1_coord[2]-y_vec[2]*yC-z_vec[2]*zC ]
												v_12  = [node1_coord[0]-y_vec[0]*yC+z_vec[0]*(bw-zC),
														 node1_coord[1]-y_vec[1]*yC+z_vec[1]*(bw-zC),
														 node1_coord[2]-y_vec[2]*yC+z_vec[2]*(bw-zC) ]
												v_13  = [node1_coord[0]-y_vec[0]*(yC-bt)+z_vec[0]*(bw-zC),
														 node1_coord[1]-y_vec[1]*(yC-bt)+z_vec[1]*(bw-zC),
														 node1_coord[2]-y_vec[2]*(yC-bt)+z_vec[2]*(bw-zC) ]
												v_14  = [node1_coord[0]-y_vec[0]*(yC-bt)-z_vec[0]*(zC-st),
														 node1_coord[1]-y_vec[1]*(yC-bt)-z_vec[1]*(zC-st),
														 node1_coord[2]-y_vec[2]*(yC-bt)-z_vec[2]*(zC-st) ]
												v_15  = [node1_coord[0]+y_vec[0]*(h-yC)-z_vec[0]*(zC-st),
														 node1_coord[1]+y_vec[1]*(h-yC)-z_vec[1]*(zC-st),
														 node1_coord[2]+y_vec[2]*(h-yC)-z_vec[2]*(zC-st) ]
												v_16  = [node1_coord[0]+y_vec[0]*(h-yC)-z_vec[0]*zC,
														 node1_coord[1]+y_vec[1]*(h-yC)-z_vec[1]*zC,
														 node1_coord[2]+y_vec[2]*(h-yC)-z_vec[2]*zC ]
												v_21  = [node2_coord[0]-y_vec[0]*yC-z_vec[0]*zC,
														 node2_coord[1]-y_vec[1]*yC-z_vec[1]*zC,
														 node2_coord[2]-y_vec[2]*yC-z_vec[2]*zC ]
												v_22  = [node2_coord[0]-y_vec[0]*yC+z_vec[0]*(bw-zC),
														 node2_coord[1]-y_vec[1]*yC+z_vec[1]*(bw-zC),
														 node2_coord[2]-y_vec[2]*yC+z_vec[2]*(bw-zC) ]
												v_23  = [node2_coord[0]-y_vec[0]*(yC-bt)+z_vec[0]*(bw-zC),
														 node2_coord[1]-y_vec[1]*(yC-bt)+z_vec[1]*(bw-zC),
														 node2_coord[2]-y_vec[2]*(yC-bt)+z_vec[2]*(bw-zC) ]
												v_24  = [node2_coord[0]-y_vec[0]*(yC-bt)-z_vec[0]*(zC-st),
														 node2_coord[1]-y_vec[1]*(yC-bt)-z_vec[1]*(zC-st),
														 node2_coord[2]-y_vec[2]*(yC-bt)-z_vec[2]*(zC-st) ]
												v_25  = [node2_coord[0]+y_vec[0]*(h-yC)-z_vec[0]*(zC-st),
														 node2_coord[1]+y_vec[1]*(h-yC)-z_vec[1]*(zC-st),
														 node2_coord[2]+y_vec[2]*(h-yC)-z_vec[2]*(zC-st) ]
												v_26  = [node2_coord[0]+y_vec[0]*(h-yC)-z_vec[0]*zC,
														 node2_coord[1]+y_vec[1]*(h-yC)-z_vec[1]*zC,
														 node2_coord[2]+y_vec[2]*(h-yC)-z_vec[2]*zC ]
												v_11 = rotatePointAboutAxis(v_11,node1_coord,[node1_coord[0]+1,node1_coord[1],node1_coord[2]],node1_rotation[0])
												v_11 = rotatePointAboutAxis(v_11,node1_coord,[node1_coord[0],node1_coord[1]+1,node1_coord[2]],node1_rotation[1])
												v_11 = rotatePointAboutAxis(v_11,node1_coord,[node1_coord[0],node1_coord[1],node1_coord[2]+1],node1_rotation[2])
												v_12 = rotatePointAboutAxis(v_12,node1_coord,[node1_coord[0]+1,node1_coord[1],node1_coord[2]],node1_rotation[0])
												v_12 = rotatePointAboutAxis(v_12,node1_coord,[node1_coord[0],node1_coord[1]+1,node1_coord[2]],node1_rotation[1])
												v_12 = rotatePointAboutAxis(v_12,node1_coord,[node1_coord[0],node1_coord[1],node1_coord[2]+1],node1_rotation[2])
												v_13 = rotatePointAboutAxis(v_13,node1_coord,[node1_coord[0]+1,node1_coord[1],node1_coord[2]],node1_rotation[0])
												v_13 = rotatePointAboutAxis(v_13,node1_coord,[node1_coord[0],node1_coord[1]+1,node1_coord[2]],node1_rotation[1])
												v_13 = rotatePointAboutAxis(v_13,node1_coord,[node1_coord[0],node1_coord[1],node1_coord[2]+1],node1_rotation[2])
												v_14 = rotatePointAboutAxis(v_14,node1_coord,[node1_coord[0]+1,node1_coord[1],node1_coord[2]],node1_rotation[0])
												v_14 = rotatePointAboutAxis(v_14,node1_coord,[node1_coord[0],node1_coord[1]+1,node1_coord[2]],node1_rotation[1])
												v_14 = rotatePointAboutAxis(v_14,node1_coord,[node1_coord[0],node1_coord[1],node1_coord[2]+1],node1_rotation[2])
												v_15 = rotatePointAboutAxis(v_15,node1_coord,[node1_coord[0]+1,node1_coord[1],node1_coord[2]],node1_rotation[0])
												v_15 = rotatePointAboutAxis(v_15,node1_coord,[node1_coord[0],node1_coord[1]+1,node1_coord[2]],node1_rotation[1])
												v_15 = rotatePointAboutAxis(v_15,node1_coord,[node1_coord[0],node1_coord[1],node1_coord[2]+1],node1_rotation[2])
												v_16 = rotatePointAboutAxis(v_16,node1_coord,[node1_coord[0]+1,node1_coord[1],node1_coord[2]],node1_rotation[0])
												v_16 = rotatePointAboutAxis(v_16,node1_coord,[node1_coord[0],node1_coord[1]+1,node1_coord[2]],node1_rotation[1])
												v_16 = rotatePointAboutAxis(v_16,node1_coord,[node1_coord[0],node1_coord[1],node1_coord[2]+1],node1_rotation[2])
												v_21 = rotatePointAboutAxis(v_21,node2_coord,[node2_coord[0]+1,node2_coord[1],node2_coord[2]],node2_rotation[0])
												v_21 = rotatePointAboutAxis(v_21,node2_coord,[node2_coord[0],node2_coord[1]+1,node2_coord[2]],node2_rotation[1])
												v_21 = rotatePointAboutAxis(v_21,node2_coord,[node2_coord[0],node2_coord[1],node2_coord[2]+1],node2_rotation[2])
												v_22 = rotatePointAboutAxis(v_22,node2_coord,[node2_coord[0]+1,node2_coord[1],node2_coord[2]],node2_rotation[0])
												v_22 = rotatePointAboutAxis(v_22,node2_coord,[node2_coord[0],node2_coord[1]+1,node2_coord[2]],node2_rotation[1])
												v_22 = rotatePointAboutAxis(v_22,node2_coord,[node2_coord[0],node2_coord[1],node2_coord[2]+1],node2_rotation[2])
												v_23 = rotatePointAboutAxis(v_23,node2_coord,[node2_coord[0]+1,node2_coord[1],node2_coord[2]],node2_rotation[0])
												v_23 = rotatePointAboutAxis(v_23,node2_coord,[node2_coord[0],node2_coord[1]+1,node2_coord[2]],node2_rotation[1])
												v_23 = rotatePointAboutAxis(v_23,node2_coord,[node2_coord[0],node2_coord[1],node2_coord[2]+1],node2_rotation[2])
												v_24 = rotatePointAboutAxis(v_24,node2_coord,[node2_coord[0]+1,node2_coord[1],node2_coord[2]],node2_rotation[0])
												v_24 = rotatePointAboutAxis(v_24,node2_coord,[node2_coord[0],node2_coord[1]+1,node2_coord[2]],node2_rotation[1])
												v_24 = rotatePointAboutAxis(v_24,node2_coord,[node2_coord[0],node2_coord[1],node2_coord[2]+1],node2_rotation[2])
												v_25 = rotatePointAboutAxis(v_25,node2_coord,[node2_coord[0]+1,node2_coord[1],node2_coord[2]],node2_rotation[0])
												v_25 = rotatePointAboutAxis(v_25,node2_coord,[node2_coord[0],node2_coord[1]+1,node2_coord[2]],node2_rotation[1])
												v_25 = rotatePointAboutAxis(v_25,node2_coord,[node2_coord[0],node2_coord[1],node2_coord[2]+1],node2_rotation[2])
												v_26 = rotatePointAboutAxis(v_26,node2_coord,[node2_coord[0]+1,node2_coord[1],node2_coord[2]],node2_rotation[0])
												v_26 = rotatePointAboutAxis(v_26,node2_coord,[node2_coord[0],node2_coord[1]+1,node2_coord[2]],node2_rotation[1])
												v_26 = rotatePointAboutAxis(v_26,node2_coord,[node2_coord[0],node2_coord[1],node2_coord[2]+1],node2_rotation[2])

												lines = [[v_11,v_12],[v_12,v_13],[v_13,v_14],[v_14,v_15],[v_15,v_16],[v_16,v_11],
														 [v_21,v_22],[v_22,v_23],[v_23,v_24],[v_24,v_25],[v_25,v_26],[v_26,v_21],
														 [v_11,v_21],[v_12,v_22],[v_13,v_23],[v_14,v_24],[v_15,v_25],[v_16,v_26]]
												faces = [[v_11,v_12,v_13],[v_13,v_14,v_11],
														 [v_11,v_14,v_16],[v_16,v_14,v_15],
														 [v_23,v_22,v_21],[v_21,v_24,v_23],
														 [v_24,v_21,v_26],[v_24,v_26,v_25],
														 [v_11,v_21,v_12],[v_12,v_21,v_22],
														 [v_11,v_16,v_26],[v_26,v_21,v_11],
														 [v_16,v_15,v_26],[v_26,v_15,v_25],
														 [v_13,v_12,v_22],[v_22,v_23,v_13],
														 [v_14,v_13,v_24],[v_24,v_13,v_23],
														 [v_14,v_24,v_25],[v_25,v_15,v_14]]

											elif elements[j].crossSection['Type'] == 'I-Beam':
												tw = elements[j].crossSection['top width, tw']
												tt = elements[j].crossSection['top thickness, tt']
												mt = elements[j].crossSection['middle thickness, mt']
												bw = elements[j].crossSection['bottom width, bw']
												bt = elements[j].crossSection['bottom thickness, bt']
												h  = elements[j].crossSection['height, h']
												tw = tw/2.
												tt = tt
												mt = mt/2.
												bw = bw/2.
												bt = bt
												h  = h/2.
												v_11  = [node1_coord[0]-y_vec[0]*h-z_vec[0]*bw,
														 node1_coord[1]-y_vec[1]*h-z_vec[1]*bw,
														 node1_coord[2]-y_vec[2]*h-z_vec[2]*bw ]
												v_12  = [node1_coord[0]-y_vec[0]*h+z_vec[0]*bw,
														 node1_coord[1]-y_vec[1]*h+z_vec[1]*bw,
														 node1_coord[2]-y_vec[2]*h+z_vec[2]*bw ]
												v_13  = [node1_coord[0]-y_vec[0]*(h-bt)+z_vec[0]*bw,
														 node1_coord[1]-y_vec[1]*(h-bt)+z_vec[1]*bw,
														 node1_coord[2]-y_vec[2]*(h-bt)+z_vec[2]*bw ]
												v_14  = [node1_coord[0]-y_vec[0]*(h-bt)+z_vec[0]*mt,
														 node1_coord[1]-y_vec[1]*(h-bt)+z_vec[1]*mt,
														 node1_coord[2]-y_vec[2]*(h-bt)+z_vec[2]*mt ]
												v_15  = [node1_coord[0]-y_vec[0]*(h-bt)-z_vec[0]*mt,
														 node1_coord[1]-y_vec[1]*(h-bt)-z_vec[1]*mt,
														 node1_coord[2]-y_vec[2]*(h-bt)-z_vec[2]*mt ]
												v_16  = [node1_coord[0]-y_vec[0]*(h-bt)-z_vec[0]*bw,
														 node1_coord[1]-y_vec[1]*(h-bt)-z_vec[1]*bw,
														 node1_coord[2]-y_vec[2]*(h-bt)-z_vec[2]*bw ]
												v_17  = [node1_coord[0]+y_vec[0]*(h-tt)-z_vec[0]*tw,
														 node1_coord[1]+y_vec[1]*(h-tt)-z_vec[1]*tw,
														 node1_coord[2]+y_vec[2]*(h-tt)-z_vec[2]*tw ]
												v_18  = [node1_coord[0]+y_vec[0]*(h-tt)-z_vec[0]*mt,
														 node1_coord[1]+y_vec[1]*(h-tt)-z_vec[1]*mt,
														 node1_coord[2]+y_vec[2]*(h-tt)-z_vec[2]*mt ]
												v_19  = [node1_coord[0]+y_vec[0]*(h-tt)+z_vec[0]*mt,
														 node1_coord[1]+y_vec[1]*(h-tt)+z_vec[1]*mt,
														 node1_coord[2]+y_vec[2]*(h-tt)+z_vec[2]*mt ]
												v_110 = [node1_coord[0]+y_vec[0]*(h-tt)+z_vec[0]*tw,
														 node1_coord[1]+y_vec[1]*(h-tt)+z_vec[1]*tw,
														 node1_coord[2]+y_vec[2]*(h-tt)+z_vec[2]*tw ]
												v_111 = [node1_coord[0]+y_vec[0]*h+z_vec[0]*tw,
														 node1_coord[1]+y_vec[1]*h+z_vec[1]*tw,
														 node1_coord[2]+y_vec[2]*h+z_vec[2]*tw ]
												v_112 = [node1_coord[0]+y_vec[0]*h-z_vec[0]*tw,
														 node1_coord[1]+y_vec[1]*h-z_vec[1]*tw,
														 node1_coord[2]+y_vec[2]*h-z_vec[2]*tw ]
												v_21  = [node2_coord[0]-y_vec[0]*h-z_vec[0]*bw,
														 node2_coord[1]-y_vec[1]*h-z_vec[1]*bw,
														 node2_coord[2]-y_vec[2]*h-z_vec[2]*bw ]
												v_22  = [node2_coord[0]-y_vec[0]*h+z_vec[0]*bw,
														 node2_coord[1]-y_vec[1]*h+z_vec[1]*bw,
														 node2_coord[2]-y_vec[2]*h+z_vec[2]*bw ]
												v_23  = [node2_coord[0]-y_vec[0]*(h-bt)+z_vec[0]*bw,
														 node2_coord[1]-y_vec[1]*(h-bt)+z_vec[1]*bw,
														 node2_coord[2]-y_vec[2]*(h-bt)+z_vec[2]*bw ]
												v_24  = [node2_coord[0]-y_vec[0]*(h-bt)+z_vec[0]*mt,
														 node2_coord[1]-y_vec[1]*(h-bt)+z_vec[1]*mt,
														 node2_coord[2]-y_vec[2]*(h-bt)+z_vec[2]*mt ]
												v_25  = [node2_coord[0]-y_vec[0]*(h-bt)-z_vec[0]*mt,
														 node2_coord[1]-y_vec[1]*(h-bt)-z_vec[1]*mt,
														 node2_coord[2]-y_vec[2]*(h-bt)-z_vec[2]*mt ]
												v_26  = [node2_coord[0]-y_vec[0]*(h-bt)-z_vec[0]*bw,
														 node2_coord[1]-y_vec[1]*(h-bt)-z_vec[1]*bw,
														 node2_coord[2]-y_vec[2]*(h-bt)-z_vec[2]*bw ]
												v_27  = [node2_coord[0]+y_vec[0]*(h-tt)-z_vec[0]*tw,
														 node2_coord[1]+y_vec[1]*(h-tt)-z_vec[1]*tw,
														 node2_coord[2]+y_vec[2]*(h-tt)-z_vec[2]*tw ]
												v_28  = [node2_coord[0]+y_vec[0]*(h-tt)-z_vec[0]*mt,
														 node2_coord[1]+y_vec[1]*(h-tt)-z_vec[1]*mt,
														 node2_coord[2]+y_vec[2]*(h-tt)-z_vec[2]*mt ]
												v_29  = [node2_coord[0]+y_vec[0]*(h-tt)+z_vec[0]*mt,
														 node2_coord[1]+y_vec[1]*(h-tt)+z_vec[1]*mt,
														 node2_coord[2]+y_vec[2]*(h-tt)+z_vec[2]*mt ]
												v_210 = [node2_coord[0]+y_vec[0]*(h-tt)+z_vec[0]*tw,
														 node2_coord[1]+y_vec[1]*(h-tt)+z_vec[1]*tw,
														 node2_coord[2]+y_vec[2]*(h-tt)+z_vec[2]*tw ]
												v_211 = [node2_coord[0]+y_vec[0]*h+z_vec[0]*tw,
														 node2_coord[1]+y_vec[1]*h+z_vec[1]*tw,
														 node2_coord[2]+y_vec[2]*h+z_vec[2]*tw ]
												v_212 = [node2_coord[0]+y_vec[0]*h-z_vec[0]*tw,
														 node2_coord[1]+y_vec[1]*h-z_vec[1]*tw,
														 node2_coord[2]+y_vec[2]*h-z_vec[2]*tw ]
												v_11 = rotatePointAboutAxis(v_11,node1_coord,[node1_coord[0]+1,node1_coord[1],node1_coord[2]],node1_rotation[0])
												v_11 = rotatePointAboutAxis(v_11,node1_coord,[node1_coord[0],node1_coord[1]+1,node1_coord[2]],node1_rotation[1])
												v_11 = rotatePointAboutAxis(v_11,node1_coord,[node1_coord[0],node1_coord[1],node1_coord[2]+1],node1_rotation[2])
												v_12 = rotatePointAboutAxis(v_12,node1_coord,[node1_coord[0]+1,node1_coord[1],node1_coord[2]],node1_rotation[0])
												v_12 = rotatePointAboutAxis(v_12,node1_coord,[node1_coord[0],node1_coord[1]+1,node1_coord[2]],node1_rotation[1])
												v_12 = rotatePointAboutAxis(v_12,node1_coord,[node1_coord[0],node1_coord[1],node1_coord[2]+1],node1_rotation[2])
												v_13 = rotatePointAboutAxis(v_13,node1_coord,[node1_coord[0]+1,node1_coord[1],node1_coord[2]],node1_rotation[0])
												v_13 = rotatePointAboutAxis(v_13,node1_coord,[node1_coord[0],node1_coord[1]+1,node1_coord[2]],node1_rotation[1])
												v_13 = rotatePointAboutAxis(v_13,node1_coord,[node1_coord[0],node1_coord[1],node1_coord[2]+1],node1_rotation[2])
												v_14 = rotatePointAboutAxis(v_14,node1_coord,[node1_coord[0]+1,node1_coord[1],node1_coord[2]],node1_rotation[0])
												v_14 = rotatePointAboutAxis(v_14,node1_coord,[node1_coord[0],node1_coord[1]+1,node1_coord[2]],node1_rotation[1])
												v_14 = rotatePointAboutAxis(v_14,node1_coord,[node1_coord[0],node1_coord[1],node1_coord[2]+1],node1_rotation[2])
												v_15 = rotatePointAboutAxis(v_15,node1_coord,[node1_coord[0]+1,node1_coord[1],node1_coord[2]],node1_rotation[0])
												v_15 = rotatePointAboutAxis(v_15,node1_coord,[node1_coord[0],node1_coord[1]+1,node1_coord[2]],node1_rotation[1])
												v_15 = rotatePointAboutAxis(v_15,node1_coord,[node1_coord[0],node1_coord[1],node1_coord[2]+1],node1_rotation[2])
												v_16 = rotatePointAboutAxis(v_16,node1_coord,[node1_coord[0]+1,node1_coord[1],node1_coord[2]],node1_rotation[0])
												v_16 = rotatePointAboutAxis(v_16,node1_coord,[node1_coord[0],node1_coord[1]+1,node1_coord[2]],node1_rotation[1])
												v_16 = rotatePointAboutAxis(v_16,node1_coord,[node1_coord[0],node1_coord[1],node1_coord[2]+1],node1_rotation[2])
												v_17 = rotatePointAboutAxis(v_17,node1_coord,[node1_coord[0]+1,node1_coord[1],node1_coord[2]],node1_rotation[0])
												v_17 = rotatePointAboutAxis(v_17,node1_coord,[node1_coord[0],node1_coord[1]+1,node1_coord[2]],node1_rotation[1])
												v_17 = rotatePointAboutAxis(v_17,node1_coord,[node1_coord[0],node1_coord[1],node1_coord[2]+1],node1_rotation[2])
												v_18 = rotatePointAboutAxis(v_18,node1_coord,[node1_coord[0]+1,node1_coord[1],node1_coord[2]],node1_rotation[0])
												v_18 = rotatePointAboutAxis(v_18,node1_coord,[node1_coord[0],node1_coord[1]+1,node1_coord[2]],node1_rotation[1])
												v_18 = rotatePointAboutAxis(v_18,node1_coord,[node1_coord[0],node1_coord[1],node1_coord[2]+1],node1_rotation[2])
												v_19 = rotatePointAboutAxis(v_19,node1_coord,[node1_coord[0]+1,node1_coord[1],node1_coord[2]],node1_rotation[0])
												v_19 = rotatePointAboutAxis(v_19,node1_coord,[node1_coord[0],node1_coord[1]+1,node1_coord[2]],node1_rotation[1])
												v_19 = rotatePointAboutAxis(v_19,node1_coord,[node1_coord[0],node1_coord[1],node1_coord[2]+1],node1_rotation[2])
												v_110 = rotatePointAboutAxis(v_110,node1_coord,[node1_coord[0]+1,node1_coord[1],node1_coord[2]],node1_rotation[0])
												v_110 = rotatePointAboutAxis(v_110,node1_coord,[node1_coord[0],node1_coord[1]+1,node1_coord[2]],node1_rotation[1])
												v_110 = rotatePointAboutAxis(v_110,node1_coord,[node1_coord[0],node1_coord[1],node1_coord[2]+1],node1_rotation[2])
												v_111 = rotatePointAboutAxis(v_111,node1_coord,[node1_coord[0]+1,node1_coord[1],node1_coord[2]],node1_rotation[0])
												v_111 = rotatePointAboutAxis(v_111,node1_coord,[node1_coord[0],node1_coord[1]+1,node1_coord[2]],node1_rotation[1])
												v_111 = rotatePointAboutAxis(v_111,node1_coord,[node1_coord[0],node1_coord[1],node1_coord[2]+1],node1_rotation[2])
												v_112 = rotatePointAboutAxis(v_112,node1_coord,[node1_coord[0]+1,node1_coord[1],node1_coord[2]],node1_rotation[0])
												v_112 = rotatePointAboutAxis(v_112,node1_coord,[node1_coord[0],node1_coord[1]+1,node1_coord[2]],node1_rotation[1])
												v_112 = rotatePointAboutAxis(v_112,node1_coord,[node1_coord[0],node1_coord[1],node1_coord[2]+1],node1_rotation[2])
												v_21 = rotatePointAboutAxis(v_21,node2_coord,[node2_coord[0]+1,node2_coord[1],node2_coord[2]],node2_rotation[0])
												v_21 = rotatePointAboutAxis(v_21,node2_coord,[node2_coord[0],node2_coord[1]+1,node2_coord[2]],node2_rotation[1])
												v_21 = rotatePointAboutAxis(v_21,node2_coord,[node2_coord[0],node2_coord[1],node2_coord[2]+1],node2_rotation[2])
												v_22 = rotatePointAboutAxis(v_22,node2_coord,[node2_coord[0]+1,node2_coord[1],node2_coord[2]],node2_rotation[0])
												v_22 = rotatePointAboutAxis(v_22,node2_coord,[node2_coord[0],node2_coord[1]+1,node2_coord[2]],node2_rotation[1])
												v_22 = rotatePointAboutAxis(v_22,node2_coord,[node2_coord[0],node2_coord[1],node2_coord[2]+1],node2_rotation[2])
												v_23 = rotatePointAboutAxis(v_23,node2_coord,[node2_coord[0]+1,node2_coord[1],node2_coord[2]],node2_rotation[0])
												v_23 = rotatePointAboutAxis(v_23,node2_coord,[node2_coord[0],node2_coord[1]+1,node2_coord[2]],node2_rotation[1])
												v_23 = rotatePointAboutAxis(v_23,node2_coord,[node2_coord[0],node2_coord[1],node2_coord[2]+1],node2_rotation[2])
												v_24 = rotatePointAboutAxis(v_24,node2_coord,[node2_coord[0]+1,node2_coord[1],node2_coord[2]],node2_rotation[0])
												v_24 = rotatePointAboutAxis(v_24,node2_coord,[node2_coord[0],node2_coord[1]+1,node2_coord[2]],node2_rotation[1])
												v_24 = rotatePointAboutAxis(v_24,node2_coord,[node2_coord[0],node2_coord[1],node2_coord[2]+1],node2_rotation[2])
												v_25 = rotatePointAboutAxis(v_25,node2_coord,[node2_coord[0]+1,node2_coord[1],node2_coord[2]],node2_rotation[0])
												v_25 = rotatePointAboutAxis(v_25,node2_coord,[node2_coord[0],node2_coord[1]+1,node2_coord[2]],node2_rotation[1])
												v_25 = rotatePointAboutAxis(v_25,node2_coord,[node2_coord[0],node2_coord[1],node2_coord[2]+1],node2_rotation[2])
												v_26 = rotatePointAboutAxis(v_26,node2_coord,[node2_coord[0]+1,node2_coord[1],node2_coord[2]],node2_rotation[0])
												v_26 = rotatePointAboutAxis(v_26,node2_coord,[node2_coord[0],node2_coord[1]+1,node2_coord[2]],node2_rotation[1])
												v_26 = rotatePointAboutAxis(v_26,node2_coord,[node2_coord[0],node2_coord[1],node2_coord[2]+1],node2_rotation[2])
												v_27 = rotatePointAboutAxis(v_27,node2_coord,[node2_coord[0]+1,node2_coord[1],node2_coord[2]],node2_rotation[0])
												v_27 = rotatePointAboutAxis(v_27,node2_coord,[node2_coord[0],node2_coord[1]+1,node2_coord[2]],node2_rotation[1])
												v_27 = rotatePointAboutAxis(v_27,node2_coord,[node2_coord[0],node2_coord[1],node2_coord[2]+1],node2_rotation[2])
												v_28 = rotatePointAboutAxis(v_28,node2_coord,[node2_coord[0]+1,node2_coord[1],node2_coord[2]],node2_rotation[0])
												v_28 = rotatePointAboutAxis(v_28,node2_coord,[node2_coord[0],node2_coord[1]+1,node2_coord[2]],node2_rotation[1])
												v_28 = rotatePointAboutAxis(v_28,node2_coord,[node2_coord[0],node2_coord[1],node2_coord[2]+1],node2_rotation[2])
												v_29 = rotatePointAboutAxis(v_29,node2_coord,[node2_coord[0]+1,node2_coord[1],node2_coord[2]],node2_rotation[0])
												v_29 = rotatePointAboutAxis(v_29,node2_coord,[node2_coord[0],node2_coord[1]+1,node2_coord[2]],node2_rotation[1])
												v_29 = rotatePointAboutAxis(v_29,node2_coord,[node2_coord[0],node2_coord[1],node2_coord[2]+1],node2_rotation[2])
												v_210 = rotatePointAboutAxis(v_210,node2_coord,[node2_coord[0]+1,node2_coord[1],node2_coord[2]],node2_rotation[0])
												v_210 = rotatePointAboutAxis(v_210,node2_coord,[node2_coord[0],node2_coord[1]+1,node2_coord[2]],node2_rotation[1])
												v_210 = rotatePointAboutAxis(v_210,node2_coord,[node2_coord[0],node2_coord[1],node2_coord[2]+1],node2_rotation[2])
												v_211 = rotatePointAboutAxis(v_211,node2_coord,[node2_coord[0]+1,node2_coord[1],node2_coord[2]],node2_rotation[0])
												v_211 = rotatePointAboutAxis(v_211,node2_coord,[node2_coord[0],node2_coord[1]+1,node2_coord[2]],node2_rotation[1])
												v_211 = rotatePointAboutAxis(v_211,node2_coord,[node2_coord[0],node2_coord[1],node2_coord[2]+1],node2_rotation[2])
												v_212 = rotatePointAboutAxis(v_212,node2_coord,[node2_coord[0]+1,node2_coord[1],node2_coord[2]],node2_rotation[0])
												v_212 = rotatePointAboutAxis(v_212,node2_coord,[node2_coord[0],node2_coord[1]+1,node2_coord[2]],node2_rotation[1])
												v_212 = rotatePointAboutAxis(v_212,node2_coord,[node2_coord[0],node2_coord[1],node2_coord[2]+1],node2_rotation[2])

												lines = [[v_11,v_12],[v_12,v_13],[v_13,v_14],[v_14,v_19],
														 [v_19,v_110],[v_110,v_111],[v_111,v_112],[v_112,v_17],
														 [v_17,v_18],[v_18,v_15],[v_15,v_16],[v_16,v_11],
														 [v_21,v_22],[v_22,v_23],[v_23,v_24],[v_24,v_29],
														 [v_29,v_210],[v_210,v_211],[v_211,v_212],[v_212,v_27],
														 [v_27,v_28],[v_28,v_25],[v_25,v_26],[v_26,v_21],
														 [v_11,v_21],[v_12,v_22],[v_13,v_23],[v_14,v_24],
														 [v_15,v_25],[v_16,v_26],[v_17,v_27],[v_18,v_28],
														 [v_19,v_29],[v_110,v_210],[v_111,v_211],[v_112,v_212]]
												faces = [[v_11,v_12,v_13],[v_13,v_16,v_11],
														 [v_15,v_14,v_19],[v_19,v_18,v_15],
														 [v_112,v_17,v_110],[v_110,v_111,v_112],
														 [v_23,v_22,v_21],[v_21,v_26,v_23],
														 [v_29,v_24,v_25],[v_25,v_28,v_29],
														 [v_210,v_27,v_212],[v_212,v_211,v_210],
														 [v_19,v_14,v_24],[v_24,v_29,v_19],
														 [v_15,v_18,v_28],[v_28,v_25,v_15],
														 [v_13,v_12,v_22],[v_22,v_23,v_13],
														 [v_11,v_16,v_26],[v_26,v_21,v_11],
														 [v_111,v_110,v_210],[v_210,v_211,v_111],
														 [v_17,v_112,v_212],[v_212,v_27,v_17],
														 [v_11,v_21,v_12],[v_21,v_22,v_12],
														 [v_112,v_111,v_212],[v_212,v_111,v_211],
														 [v_14,v_13,v_24],[v_24,v_13,v_23],
														 [v_16,v_15,v_26],[v_26,v_15,v_25],
														 [v_18,v_17,v_27],[v_27,v_28,v_18],
														 [v_110,v_19,v_29],[v_29,v_210,v_110]]

											elif elements[j].crossSection['Type'] == 'C-Beam':
												tw = elements[j].crossSection['top width, tw']
												tt = elements[j].crossSection['top thickness, tt']
												mt = elements[j].crossSection['middle thickness, mt']
												bw = elements[j].crossSection['bottom width, bw']
												bt = elements[j].crossSection['bottom thickness, bt']
												h  = elements[j].crossSection['height, h']
												A1  = tt*tw
												A2  = mt*(h-tt-bt)
												A3  = bt*bw
												A   = A1+A2+A3
												zC1 = tw/2.
												zC2 = mt/2.
												zC3 = bw/2.
												yC1 = h-(tt/2.)
												yC2 = (h-tt)/2.
												yC3 = bt/2.
												if A != 0.:
													zC = (A1*zC1+A2*zC2+A3*zC3)/A
													yC = (A1*yC1+A2*yC2+A3*yC3)/A
												else:
													zC = 0.
													yC = 0.
												v_11  = [node1_coord[0]-y_vec[0]*yC-z_vec[0]*zC,
														 node1_coord[1]-y_vec[1]*yC-z_vec[1]*zC,
														 node1_coord[2]-y_vec[2]*yC-z_vec[2]*zC ]
												v_12  = [node1_coord[0]-y_vec[0]*yC+z_vec[0]*(bw-zC),
														 node1_coord[1]-y_vec[1]*yC+z_vec[1]*(bw-zC),
														 node1_coord[2]-y_vec[2]*yC+z_vec[2]*(bw-zC) ]
												v_13  = [node1_coord[0]-y_vec[0]*(yC-bt)+z_vec[0]*(bw-zC),
														 node1_coord[1]-y_vec[1]*(yC-bt)+z_vec[1]*(bw-zC),
														 node1_coord[2]-y_vec[2]*(yC-bt)+z_vec[2]*(bw-zC) ]
												v_14  = [node1_coord[0]-y_vec[0]*(yC-bt)-z_vec[0]*(zC-mt),
														 node1_coord[1]-y_vec[1]*(yC-bt)-z_vec[1]*(zC-mt),
														 node1_coord[2]-y_vec[2]*(yC-bt)-z_vec[2]*(zC-mt) ]
												v_15  = [node1_coord[0]+y_vec[0]*(h-yC-tt)-z_vec[0]*(zC-mt),
														 node1_coord[1]+y_vec[1]*(h-yC-tt)-z_vec[1]*(zC-mt),
														 node1_coord[2]+y_vec[2]*(h-yC-tt)-z_vec[2]*(zC-mt) ]
												v_16  = [node1_coord[0]+y_vec[0]*(h-yC-tt)+z_vec[0]*(tw-zC),
														 node1_coord[1]+y_vec[1]*(h-yC-tt)+z_vec[1]*(tw-zC),
														 node1_coord[2]+y_vec[2]*(h-yC-tt)+z_vec[2]*(tw-zC) ]
												v_17  = [node1_coord[0]+y_vec[0]*(h-yC)+z_vec[0]*(tw-zC),
														 node1_coord[1]+y_vec[1]*(h-yC)+z_vec[1]*(tw-zC),
														 node1_coord[2]+y_vec[2]*(h-yC)+z_vec[2]*(tw-zC) ]
												v_18  = [node1_coord[0]+y_vec[0]*(h-yC)-z_vec[0]*zC,
														 node1_coord[1]+y_vec[1]*(h-yC)-z_vec[1]*zC,
														 node1_coord[2]+y_vec[2]*(h-yC)-z_vec[2]*zC ]
												v_21  = [node2_coord[0]-y_vec[0]*yC-z_vec[0]*zC,
														 node2_coord[1]-y_vec[1]*yC-z_vec[1]*zC,
														 node2_coord[2]-y_vec[2]*yC-z_vec[2]*zC ]
												v_22  = [node2_coord[0]-y_vec[0]*yC+z_vec[0]*(bw-zC),
														 node2_coord[1]-y_vec[1]*yC+z_vec[1]*(bw-zC),
														 node2_coord[2]-y_vec[2]*yC+z_vec[2]*(bw-zC) ]
												v_23  = [node2_coord[0]-y_vec[0]*(yC-bt)+z_vec[0]*(bw-zC),
														 node2_coord[1]-y_vec[1]*(yC-bt)+z_vec[1]*(bw-zC),
														 node2_coord[2]-y_vec[2]*(yC-bt)+z_vec[2]*(bw-zC) ]
												v_24  = [node2_coord[0]-y_vec[0]*(yC-bt)-z_vec[0]*(zC-mt),
														 node2_coord[1]-y_vec[1]*(yC-bt)-z_vec[1]*(zC-mt),
														 node2_coord[2]-y_vec[2]*(yC-bt)-z_vec[2]*(zC-mt) ]
												v_25  = [node2_coord[0]+y_vec[0]*(h-yC-tt)-z_vec[0]*(zC-mt),
														 node2_coord[1]+y_vec[1]*(h-yC-tt)-z_vec[1]*(zC-mt),
														 node2_coord[2]+y_vec[2]*(h-yC-tt)-z_vec[2]*(zC-mt) ]
												v_26  = [node2_coord[0]+y_vec[0]*(h-yC-tt)+z_vec[0]*(tw-zC),
														 node2_coord[1]+y_vec[1]*(h-yC-tt)+z_vec[1]*(tw-zC),
														 node2_coord[2]+y_vec[2]*(h-yC-tt)+z_vec[2]*(tw-zC) ]
												v_27  = [node2_coord[0]+y_vec[0]*(h-yC)+z_vec[0]*(tw-zC),
														 node2_coord[1]+y_vec[1]*(h-yC)+z_vec[1]*(tw-zC),
														 node2_coord[2]+y_vec[2]*(h-yC)+z_vec[2]*(tw-zC) ]
												v_28  = [node2_coord[0]+y_vec[0]*(h-yC)-z_vec[0]*zC,
														 node2_coord[1]+y_vec[1]*(h-yC)-z_vec[1]*zC,
														 node2_coord[2]+y_vec[2]*(h-yC)-z_vec[2]*zC ]
												v_11 = rotatePointAboutAxis(v_11,node1_coord,[node1_coord[0]+1,node1_coord[1],node1_coord[2]],node1_rotation[0])
												v_11 = rotatePointAboutAxis(v_11,node1_coord,[node1_coord[0],node1_coord[1]+1,node1_coord[2]],node1_rotation[1])
												v_11 = rotatePointAboutAxis(v_11,node1_coord,[node1_coord[0],node1_coord[1],node1_coord[2]+1],node1_rotation[2])
												v_12 = rotatePointAboutAxis(v_12,node1_coord,[node1_coord[0]+1,node1_coord[1],node1_coord[2]],node1_rotation[0])
												v_12 = rotatePointAboutAxis(v_12,node1_coord,[node1_coord[0],node1_coord[1]+1,node1_coord[2]],node1_rotation[1])
												v_12 = rotatePointAboutAxis(v_12,node1_coord,[node1_coord[0],node1_coord[1],node1_coord[2]+1],node1_rotation[2])
												v_13 = rotatePointAboutAxis(v_13,node1_coord,[node1_coord[0]+1,node1_coord[1],node1_coord[2]],node1_rotation[0])
												v_13 = rotatePointAboutAxis(v_13,node1_coord,[node1_coord[0],node1_coord[1]+1,node1_coord[2]],node1_rotation[1])
												v_13 = rotatePointAboutAxis(v_13,node1_coord,[node1_coord[0],node1_coord[1],node1_coord[2]+1],node1_rotation[2])
												v_14 = rotatePointAboutAxis(v_14,node1_coord,[node1_coord[0]+1,node1_coord[1],node1_coord[2]],node1_rotation[0])
												v_14 = rotatePointAboutAxis(v_14,node1_coord,[node1_coord[0],node1_coord[1]+1,node1_coord[2]],node1_rotation[1])
												v_14 = rotatePointAboutAxis(v_14,node1_coord,[node1_coord[0],node1_coord[1],node1_coord[2]+1],node1_rotation[2])
												v_15 = rotatePointAboutAxis(v_15,node1_coord,[node1_coord[0]+1,node1_coord[1],node1_coord[2]],node1_rotation[0])
												v_15 = rotatePointAboutAxis(v_15,node1_coord,[node1_coord[0],node1_coord[1]+1,node1_coord[2]],node1_rotation[1])
												v_15 = rotatePointAboutAxis(v_15,node1_coord,[node1_coord[0],node1_coord[1],node1_coord[2]+1],node1_rotation[2])
												v_16 = rotatePointAboutAxis(v_16,node1_coord,[node1_coord[0]+1,node1_coord[1],node1_coord[2]],node1_rotation[0])
												v_16 = rotatePointAboutAxis(v_16,node1_coord,[node1_coord[0],node1_coord[1]+1,node1_coord[2]],node1_rotation[1])
												v_16 = rotatePointAboutAxis(v_16,node1_coord,[node1_coord[0],node1_coord[1],node1_coord[2]+1],node1_rotation[2])
												v_17 = rotatePointAboutAxis(v_17,node1_coord,[node1_coord[0]+1,node1_coord[1],node1_coord[2]],node1_rotation[0])
												v_17 = rotatePointAboutAxis(v_17,node1_coord,[node1_coord[0],node1_coord[1]+1,node1_coord[2]],node1_rotation[1])
												v_17 = rotatePointAboutAxis(v_17,node1_coord,[node1_coord[0],node1_coord[1],node1_coord[2]+1],node1_rotation[2])
												v_18 = rotatePointAboutAxis(v_18,node1_coord,[node1_coord[0]+1,node1_coord[1],node1_coord[2]],node1_rotation[0])
												v_18 = rotatePointAboutAxis(v_18,node1_coord,[node1_coord[0],node1_coord[1]+1,node1_coord[2]],node1_rotation[1])
												v_18 = rotatePointAboutAxis(v_18,node1_coord,[node1_coord[0],node1_coord[1],node1_coord[2]+1],node1_rotation[2])
												v_21 = rotatePointAboutAxis(v_21,node2_coord,[node2_coord[0]+1,node2_coord[1],node2_coord[2]],node2_rotation[0])
												v_21 = rotatePointAboutAxis(v_21,node2_coord,[node2_coord[0],node2_coord[1]+1,node2_coord[2]],node2_rotation[1])
												v_21 = rotatePointAboutAxis(v_21,node2_coord,[node2_coord[0],node2_coord[1],node2_coord[2]+1],node2_rotation[2])
												v_22 = rotatePointAboutAxis(v_22,node2_coord,[node2_coord[0]+1,node2_coord[1],node2_coord[2]],node2_rotation[0])
												v_22 = rotatePointAboutAxis(v_22,node2_coord,[node2_coord[0],node2_coord[1]+1,node2_coord[2]],node2_rotation[1])
												v_22 = rotatePointAboutAxis(v_22,node2_coord,[node2_coord[0],node2_coord[1],node2_coord[2]+1],node2_rotation[2])
												v_23 = rotatePointAboutAxis(v_23,node2_coord,[node2_coord[0]+1,node2_coord[1],node2_coord[2]],node2_rotation[0])
												v_23 = rotatePointAboutAxis(v_23,node2_coord,[node2_coord[0],node2_coord[1]+1,node2_coord[2]],node2_rotation[1])
												v_23 = rotatePointAboutAxis(v_23,node2_coord,[node2_coord[0],node2_coord[1],node2_coord[2]+1],node2_rotation[2])
												v_24 = rotatePointAboutAxis(v_24,node2_coord,[node2_coord[0]+1,node2_coord[1],node2_coord[2]],node2_rotation[0])
												v_24 = rotatePointAboutAxis(v_24,node2_coord,[node2_coord[0],node2_coord[1]+1,node2_coord[2]],node2_rotation[1])
												v_24 = rotatePointAboutAxis(v_24,node2_coord,[node2_coord[0],node2_coord[1],node2_coord[2]+1],node2_rotation[2])
												v_25 = rotatePointAboutAxis(v_25,node2_coord,[node2_coord[0]+1,node2_coord[1],node2_coord[2]],node2_rotation[0])
												v_25 = rotatePointAboutAxis(v_25,node2_coord,[node2_coord[0],node2_coord[1]+1,node2_coord[2]],node2_rotation[1])
												v_25 = rotatePointAboutAxis(v_25,node2_coord,[node2_coord[0],node2_coord[1],node2_coord[2]+1],node2_rotation[2])
												v_26 = rotatePointAboutAxis(v_26,node2_coord,[node2_coord[0]+1,node2_coord[1],node2_coord[2]],node2_rotation[0])
												v_26 = rotatePointAboutAxis(v_26,node2_coord,[node2_coord[0],node2_coord[1]+1,node2_coord[2]],node2_rotation[1])
												v_26 = rotatePointAboutAxis(v_26,node2_coord,[node2_coord[0],node2_coord[1],node2_coord[2]+1],node2_rotation[2])
												v_27 = rotatePointAboutAxis(v_27,node2_coord,[node2_coord[0]+1,node2_coord[1],node2_coord[2]],node2_rotation[0])
												v_27 = rotatePointAboutAxis(v_27,node2_coord,[node2_coord[0],node2_coord[1]+1,node2_coord[2]],node2_rotation[1])
												v_27 = rotatePointAboutAxis(v_27,node2_coord,[node2_coord[0],node2_coord[1],node2_coord[2]+1],node2_rotation[2])
												v_28 = rotatePointAboutAxis(v_28,node2_coord,[node2_coord[0]+1,node2_coord[1],node2_coord[2]],node2_rotation[0])
												v_28 = rotatePointAboutAxis(v_28,node2_coord,[node2_coord[0],node2_coord[1]+1,node2_coord[2]],node2_rotation[1])
												v_28 = rotatePointAboutAxis(v_28,node2_coord,[node2_coord[0],node2_coord[1],node2_coord[2]+1],node2_rotation[2])
												
												lines = [[v_11,v_12],[v_12,v_13],[v_13,v_14],[v_14,v_15],
														 [v_15,v_16],[v_16,v_17],[v_17,v_18],[v_18,v_11],
														 [v_21,v_22],[v_22,v_23],[v_23,v_24],[v_24,v_25],
														 [v_25,v_26],[v_26,v_27],[v_27,v_28],[v_28,v_21],
														 [v_11,v_21],[v_12,v_22],[v_13,v_23],[v_14,v_24],
														 [v_15,v_25],[v_16,v_26],[v_17,v_27],[v_18,v_28]]
												faces = [[v_11,v_12,v_13],[v_13,v_14,v_11],
														 [v_11,v_14,v_18],[v_18,v_14,v_15],
														 [v_15,v_16,v_17],[v_17,v_18,v_15],
														 [v_23,v_22,v_21],[v_21,v_24,v_23],
														 [v_24,v_21,v_28],[v_24,v_28,v_25],
														 [v_26,v_25,v_27],[v_28,v_27,v_25],
														 [v_11,v_21,v_12],[v_12,v_21,v_22],
														 [v_11,v_18,v_28],[v_28,v_21,v_11],
														 [v_18,v_17,v_28],[v_28,v_17,v_27],
														 [v_16,v_26,v_27],[v_27,v_17,v_16],
														 [v_16,v_15,v_25],[v_25,v_26,v_16],
														 [v_14,v_24,v_25],[v_25,v_15,v_14],
														 [v_13,v_24,v_14],[v_24,v_13,v_23],
														 [v_13,v_12,v_22],[v_22,v_23,v_13]]

											elif elements[j].crossSection['Type'] == 'T-Beam':
												tw = elements[j].crossSection['top width, tw']
												tt = elements[j].crossSection['top thickness, tt']
												mt = elements[j].crossSection['middle thickness, mt']
												h  = elements[j].crossSection['height, h']
												A1  = mt*(h-tt)
												A2  = tt*tw
												A   = A1+A2
												yC1 = h-(tt/2.)
												yC2 = (h-tt)/2.
												if A != 0.:
													yC = (A1*yC1+A2*yC2)/A
												else:
													yC = 0.
												tw = tw/2.
												tt = tt
												mt = mt/2.
												v_11  = [node1_coord[0]-y_vec[0]*yC-z_vec[0]*mt,
														 node1_coord[1]-y_vec[1]*yC-z_vec[1]*mt,
														 node1_coord[2]-y_vec[2]*yC-z_vec[2]*mt ]
												v_12  = [node1_coord[0]-y_vec[0]*yC+z_vec[0]*mt,
														 node1_coord[1]-y_vec[1]*yC+z_vec[1]*mt,
														 node1_coord[2]-y_vec[2]*yC+z_vec[2]*mt ]
												v_17  = [node1_coord[0]+y_vec[0]*(h-yC-tt)-z_vec[0]*tw,
														 node1_coord[1]+y_vec[1]*(h-yC-tt)-z_vec[1]*tw,
														 node1_coord[2]+y_vec[2]*(h-yC-tt)-z_vec[2]*tw ]
												v_18  = [node1_coord[0]+y_vec[0]*(h-yC-tt)-z_vec[0]*mt,
														 node1_coord[1]+y_vec[1]*(h-yC-tt)-z_vec[1]*mt,
														 node1_coord[2]+y_vec[2]*(h-yC-tt)-z_vec[2]*mt ]
												v_19  = [node1_coord[0]+y_vec[0]*(h-yC-tt)+z_vec[0]*mt,
														 node1_coord[1]+y_vec[1]*(h-yC-tt)+z_vec[1]*mt,
														 node1_coord[2]+y_vec[2]*(h-yC-tt)+z_vec[2]*mt ]
												v_110 = [node1_coord[0]+y_vec[0]*(h-yC-tt)+z_vec[0]*tw,
														 node1_coord[1]+y_vec[1]*(h-yC-tt)+z_vec[1]*tw,
														 node1_coord[2]+y_vec[2]*(h-yC-tt)+z_vec[2]*tw ]
												v_111 = [node1_coord[0]+y_vec[0]*(h-yC)+z_vec[0]*tw,
														 node1_coord[1]+y_vec[1]*(h-yC)+z_vec[1]*tw,
														 node1_coord[2]+y_vec[2]*(h-yC)+z_vec[2]*tw ]
												v_112 = [node1_coord[0]+y_vec[0]*(h-yC)-z_vec[0]*tw,
														 node1_coord[1]+y_vec[1]*(h-yC)-z_vec[1]*tw,
														 node1_coord[2]+y_vec[2]*(h-yC)-z_vec[2]*tw ]
												v_21  = [node2_coord[0]-y_vec[0]*yC-z_vec[0]*mt,
														 node2_coord[1]-y_vec[1]*yC-z_vec[1]*mt,
														 node2_coord[2]-y_vec[2]*yC-z_vec[2]*mt ]
												v_22  = [node2_coord[0]-y_vec[0]*yC+z_vec[0]*mt,
														 node2_coord[1]-y_vec[1]*yC+z_vec[1]*mt,
														 node2_coord[2]-y_vec[2]*yC+z_vec[2]*mt ]
												v_27  = [node2_coord[0]+y_vec[0]*(h-yC-tt)-z_vec[0]*tw,
														 node2_coord[1]+y_vec[1]*(h-yC-tt)-z_vec[1]*tw,
														 node2_coord[2]+y_vec[2]*(h-yC-tt)-z_vec[2]*tw ]
												v_28  = [node2_coord[0]+y_vec[0]*(h-yC-tt)-z_vec[0]*mt,
														 node2_coord[1]+y_vec[1]*(h-yC-tt)-z_vec[1]*mt,
														 node2_coord[2]+y_vec[2]*(h-yC-tt)-z_vec[2]*mt ]
												v_29  = [node2_coord[0]+y_vec[0]*(h-yC-tt)+z_vec[0]*mt,
														 node2_coord[1]+y_vec[1]*(h-yC-tt)+z_vec[1]*mt,
														 node2_coord[2]+y_vec[2]*(h-yC-tt)+z_vec[2]*mt ]
												v_210 = [node2_coord[0]+y_vec[0]*(h-yC-tt)+z_vec[0]*tw,
														 node2_coord[1]+y_vec[1]*(h-yC-tt)+z_vec[1]*tw,
														 node2_coord[2]+y_vec[2]*(h-yC-tt)+z_vec[2]*tw ]
												v_211 = [node2_coord[0]+y_vec[0]*(h-yC)+z_vec[0]*tw,
														 node2_coord[1]+y_vec[1]*(h-yC)+z_vec[1]*tw,
														 node2_coord[2]+y_vec[2]*(h-yC)+z_vec[2]*tw ]
												v_212 = [node2_coord[0]+y_vec[0]*(h-yC)-z_vec[0]*tw,
														 node2_coord[1]+y_vec[1]*(h-yC)-z_vec[1]*tw,
														 node2_coord[2]+y_vec[2]*(h-yC)-z_vec[2]*tw ]
												v_11 = rotatePointAboutAxis(v_11,node1_coord,[node1_coord[0]+1,node1_coord[1],node1_coord[2]],node1_rotation[0])
												v_11 = rotatePointAboutAxis(v_11,node1_coord,[node1_coord[0],node1_coord[1]+1,node1_coord[2]],node1_rotation[1])
												v_11 = rotatePointAboutAxis(v_11,node1_coord,[node1_coord[0],node1_coord[1],node1_coord[2]+1],node1_rotation[2])
												v_12 = rotatePointAboutAxis(v_12,node1_coord,[node1_coord[0]+1,node1_coord[1],node1_coord[2]],node1_rotation[0])
												v_12 = rotatePointAboutAxis(v_12,node1_coord,[node1_coord[0],node1_coord[1]+1,node1_coord[2]],node1_rotation[1])
												v_12 = rotatePointAboutAxis(v_12,node1_coord,[node1_coord[0],node1_coord[1],node1_coord[2]+1],node1_rotation[2])
												v_17 = rotatePointAboutAxis(v_17,node1_coord,[node1_coord[0]+1,node1_coord[1],node1_coord[2]],node1_rotation[0])
												v_17 = rotatePointAboutAxis(v_17,node1_coord,[node1_coord[0],node1_coord[1]+1,node1_coord[2]],node1_rotation[1])
												v_17 = rotatePointAboutAxis(v_17,node1_coord,[node1_coord[0],node1_coord[1],node1_coord[2]+1],node1_rotation[2])
												v_18 = rotatePointAboutAxis(v_18,node1_coord,[node1_coord[0]+1,node1_coord[1],node1_coord[2]],node1_rotation[0])
												v_18 = rotatePointAboutAxis(v_18,node1_coord,[node1_coord[0],node1_coord[1]+1,node1_coord[2]],node1_rotation[1])
												v_18 = rotatePointAboutAxis(v_18,node1_coord,[node1_coord[0],node1_coord[1],node1_coord[2]+1],node1_rotation[2])
												v_19 = rotatePointAboutAxis(v_19,node1_coord,[node1_coord[0]+1,node1_coord[1],node1_coord[2]],node1_rotation[0])
												v_19 = rotatePointAboutAxis(v_19,node1_coord,[node1_coord[0],node1_coord[1]+1,node1_coord[2]],node1_rotation[1])
												v_19 = rotatePointAboutAxis(v_19,node1_coord,[node1_coord[0],node1_coord[1],node1_coord[2]+1],node1_rotation[2])
												v_110 = rotatePointAboutAxis(v_110,node1_coord,[node1_coord[0]+1,node1_coord[1],node1_coord[2]],node1_rotation[0])
												v_110 = rotatePointAboutAxis(v_110,node1_coord,[node1_coord[0],node1_coord[1]+1,node1_coord[2]],node1_rotation[1])
												v_110 = rotatePointAboutAxis(v_110,node1_coord,[node1_coord[0],node1_coord[1],node1_coord[2]+1],node1_rotation[2])
												v_111 = rotatePointAboutAxis(v_111,node1_coord,[node1_coord[0]+1,node1_coord[1],node1_coord[2]],node1_rotation[0])
												v_111 = rotatePointAboutAxis(v_111,node1_coord,[node1_coord[0],node1_coord[1]+1,node1_coord[2]],node1_rotation[1])
												v_111 = rotatePointAboutAxis(v_111,node1_coord,[node1_coord[0],node1_coord[1],node1_coord[2]+1],node1_rotation[2])
												v_112 = rotatePointAboutAxis(v_112,node1_coord,[node1_coord[0]+1,node1_coord[1],node1_coord[2]],node1_rotation[0])
												v_112 = rotatePointAboutAxis(v_112,node1_coord,[node1_coord[0],node1_coord[1]+1,node1_coord[2]],node1_rotation[1])
												v_112 = rotatePointAboutAxis(v_112,node1_coord,[node1_coord[0],node1_coord[1],node1_coord[2]+1],node1_rotation[2])
												v_21 = rotatePointAboutAxis(v_21,node2_coord,[node2_coord[0]+1,node2_coord[1],node2_coord[2]],node2_rotation[0])
												v_21 = rotatePointAboutAxis(v_21,node2_coord,[node2_coord[0],node2_coord[1]+1,node2_coord[2]],node2_rotation[1])
												v_21 = rotatePointAboutAxis(v_21,node2_coord,[node2_coord[0],node2_coord[1],node2_coord[2]+1],node2_rotation[2])
												v_22 = rotatePointAboutAxis(v_22,node2_coord,[node2_coord[0]+1,node2_coord[1],node2_coord[2]],node2_rotation[0])
												v_22 = rotatePointAboutAxis(v_22,node2_coord,[node2_coord[0],node2_coord[1]+1,node2_coord[2]],node2_rotation[1])
												v_22 = rotatePointAboutAxis(v_22,node2_coord,[node2_coord[0],node2_coord[1],node2_coord[2]+1],node2_rotation[2])
												v_27 = rotatePointAboutAxis(v_27,node2_coord,[node2_coord[0]+1,node2_coord[1],node2_coord[2]],node2_rotation[0])
												v_27 = rotatePointAboutAxis(v_27,node2_coord,[node2_coord[0],node2_coord[1]+1,node2_coord[2]],node2_rotation[1])
												v_27 = rotatePointAboutAxis(v_27,node2_coord,[node2_coord[0],node2_coord[1],node2_coord[2]+1],node2_rotation[2])
												v_28 = rotatePointAboutAxis(v_28,node2_coord,[node2_coord[0]+1,node2_coord[1],node2_coord[2]],node2_rotation[0])
												v_28 = rotatePointAboutAxis(v_28,node2_coord,[node2_coord[0],node2_coord[1]+1,node2_coord[2]],node2_rotation[1])
												v_28 = rotatePointAboutAxis(v_28,node2_coord,[node2_coord[0],node2_coord[1],node2_coord[2]+1],node2_rotation[2])
												v_29 = rotatePointAboutAxis(v_29,node2_coord,[node2_coord[0]+1,node2_coord[1],node2_coord[2]],node2_rotation[0])
												v_29 = rotatePointAboutAxis(v_29,node2_coord,[node2_coord[0],node2_coord[1]+1,node2_coord[2]],node2_rotation[1])
												v_29 = rotatePointAboutAxis(v_29,node2_coord,[node2_coord[0],node2_coord[1],node2_coord[2]+1],node2_rotation[2])
												v_210 = rotatePointAboutAxis(v_210,node2_coord,[node2_coord[0]+1,node2_coord[1],node2_coord[2]],node2_rotation[0])
												v_210 = rotatePointAboutAxis(v_210,node2_coord,[node2_coord[0],node2_coord[1]+1,node2_coord[2]],node2_rotation[1])
												v_210 = rotatePointAboutAxis(v_210,node2_coord,[node2_coord[0],node2_coord[1],node2_coord[2]+1],node2_rotation[2])
												v_211 = rotatePointAboutAxis(v_211,node2_coord,[node2_coord[0]+1,node2_coord[1],node2_coord[2]],node2_rotation[0])
												v_211 = rotatePointAboutAxis(v_211,node2_coord,[node2_coord[0],node2_coord[1]+1,node2_coord[2]],node2_rotation[1])
												v_211 = rotatePointAboutAxis(v_211,node2_coord,[node2_coord[0],node2_coord[1],node2_coord[2]+1],node2_rotation[2])
												v_212 = rotatePointAboutAxis(v_212,node2_coord,[node2_coord[0]+1,node2_coord[1],node2_coord[2]],node2_rotation[0])
												v_212 = rotatePointAboutAxis(v_212,node2_coord,[node2_coord[0],node2_coord[1]+1,node2_coord[2]],node2_rotation[1])
												v_212 = rotatePointAboutAxis(v_212,node2_coord,[node2_coord[0],node2_coord[1],node2_coord[2]+1],node2_rotation[2])

												lines = [[v_11,v_12],[v_12,v_19],[v_19,v_110],[v_110,v_111],
														 [v_111,v_112],[v_112,v_17],[v_17,v_18],[v_18,v_11],
														 [v_21,v_22],[v_22,v_29],[v_29,v_210],[v_210,v_211],
														 [v_211,v_212],[v_212,v_27],[v_27,v_28],[v_28,v_21],
														 [v_11,v_21],[v_12,v_22],[v_17,v_27],[v_18,v_28],
														 [v_19,v_29],[v_110,v_210],[v_111,v_211],[v_112,v_212]]
												faces = [[v_11,v_12,v_19],[v_19,v_18,v_11],
														 [v_112,v_17,v_110],[v_110,v_111,v_112],
														 [v_29,v_22,v_21],[v_21,v_28,v_29],
														 [v_210,v_27,v_212],[v_212,v_211,v_210],
														 [v_19,v_12,v_22],[v_22,v_29,v_19],
														 [v_11,v_18,v_28],[v_28,v_21,v_11],
														 [v_111,v_110,v_210],[v_210,v_211,v_111],
														 [v_17,v_112,v_212],[v_212,v_27,v_17],
														 [v_11,v_21,v_12],[v_21,v_22,v_12],
														 [v_112,v_111,v_212],[v_212,v_111,v_211],
														 [v_18,v_17,v_27],[v_27,v_28,v_18],
														 [v_110,v_19,v_29],[v_29,v_210,v_110]]

											else:
												pass

											glLineWidth(2.0)
											glColor3f(0.0, 0.2, 0.0)
											for line in range(len(lines)):
												glBegin(GL_LINES)
												glVertex3f(lines[line][0][0],lines[line][0][1],lines[line][0][2])
												glVertex3f(lines[line][1][0],lines[line][1][1],lines[line][1][2])
												glEnd()

											glColor3f(0.0, 0.7, 0.0)
											for face in range(len(faces)):
												glBegin(GL_TRIANGLES)
												glVertex3f(faces[face][0][0],faces[face][0][1],faces[face][0][2])
												glVertex3f(faces[face][1][0],faces[face][1][1],faces[face][1][2])
												glVertex3f(faces[face][2][0],faces[face][2][1],faces[face][2][2])
												glEnd()


							glEndList()

				elif result == 'strainenergy':
					pass

			elif self.results[newResult].solutions[solution].type == 'ModalDynamic':

				self.displayLists[solution][result][subresult]['nodes'] = mesh.displayLists['nodes']
				self.displayLists[solution][result][subresult]['wireframe'] = mesh.displayLists['wireframe']
				self.displayLists[solution][result][subresult]['shaded'] = mesh.displayLists['shaded']
				self.displayLists[solution][result][subresult]['info'] = subresult


			elif self.results[newResult].solutions[solution].type == 'StaticPlastic':
				pass

			else:
				pass




if __name__ == '__main__':

    app = QtWidgets.QApplication(['viewFEM - Finite Element Viewer'])
    window = UserInterface()
    window.show()
    app.exec_()



