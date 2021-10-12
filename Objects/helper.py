#! /usr/bin/env python3
#
#
#	helper.py
#  --------------
#
#	This is the helper module. It creates a help window
#	object used to show instructions on topics requested
#	by the user.
#


import sys
from PyQt5 import QtGui, QtCore, QtWidgets





class HelpScreen(QtWidgets.QWidget):
	'''
Class for making a window that shows instructions
on topics specified by user.
'''
	def __init__(self, topic):
		super(HelpScreen, self).__init__()
		self.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint)
		self.setWindowTitle(topic)

		layout = QtWidgets.QVBoxLayout()
		lbl = QtWidgets.QLabel('<font color=Black size=12><b> Unknown Help request: '+topic+' </b></font>')
		size = QtWidgets.QDesktopWidget().screenGeometry().height()-100
		if topic == 'camera':
			pix = QtGui.QPixmap('../Instructions/camera_controls.png')
			lbl.setPixmap(pix.scaledToHeight(size))
		elif topic == 'selection':
			pix = QtGui.QPixmap('../Instructions/selection_controls.png')
			lbl.setPixmap(pix.scaledToHeight(size))
		elif topic == 'meshes':
			pix = QtGui.QPixmap('../Instructions/mesh_creation.png')
			lbl.setPixmap(pix.scaledToHeight(size))
		elif topic == 'materials':
			pix = QtGui.QPixmap('../Instructions/materials.png')
			lbl.setPixmap(pix.scaledToHeight(size))
		elif topic == 'sections':
			pix = QtGui.QPixmap('../Instructions/sections.png')
			lbl.setPixmap(pix.scaledToHeight(size))
		elif topic == 'solutions':
			pix = QtGui.QPixmap('../Instructions/solutions.png')
			lbl.setPixmap(pix.scaledToHeight(size))
		elif topic == 'boundaries':
			pix = QtGui.QPixmap('../Instructions/boundary_conditions.png')
			lbl.setPixmap(pix.scaledToHeight(size))
		elif topic == 'constraints':
			pix = QtGui.QPixmap('../Instructions/multipoint_constraints.png')
			lbl.setPixmap(pix.scaledToHeight(size))
		elif topic == 'loads':
			pix = QtGui.QPixmap('../Instructions/loads.png')
			lbl.setPixmap(pix.scaledToHeight(size))
		elif topic == 'solver':
			pix = QtGui.QPixmap('../Instructions/solver.png')
			lbl.setPixmap(pix.scaledToHeight(size))
		elif topic == 'results':
			pix = QtGui.QPixmap('../Instructions/results.png')
			lbl.setPixmap(pix.scaledToHeight(size))
		else:
			print('\tUnknown help request:', topic)
		layout.addWidget(lbl)

		self.setLayout(layout)
		self.center()
		self.show()

	def center(self):
		self.showNormal()
		window_geometry = self.frameGeometry()
#		self.resize(QtWidgets.QDesktopWidget().screenGeometry().width() // 1.3,
#					QtWidgets.QDesktopWidget().screenGeometry().height() // 1.5)
		mousepointer_position = QtWidgets.QApplication.desktop().cursor().pos()
		screen = QtWidgets.QApplication.desktop().screenNumber(mousepointer_position)
		centerPoint = QtWidgets.QApplication.desktop().screenGeometry(screen).center()
		window_geometry.moveCenter(centerPoint)
		return bool(not self.move(window_geometry.topLeft()))









