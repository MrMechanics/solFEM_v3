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


import os, sys
from PyQt5 import QtGui, QtCore, QtWidgets

#sys.path.insert(1, '../Instructions')





class HelpScreen(QtWidgets.QWidget):
	'''
Class for making a window that shows instructions
on topics specified by user.
'''
	def __init__(self, topic):
		super(HelpScreen, self).__init__()
		self.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint)
		self.setWindowTitle(topic)
		self.setWindowIcon(QtGui.QIcon('../Icons/icon_question.png'))

		# initialize pixmap filename
		self.page_number = 1
		self.filename = ''
		if topic == 'camera':
			self.filename = '../Instructions/camera_controls'
		elif topic == 'selection':
			self.filename = '../Instructions/selection_controls'	
		elif topic == 'meshes':
			self.filename = '../Instructions/mesh_controls'
		elif topic == 'materials':
			self.filename = '../Instructions/materials'
		elif topic == 'sections':
			self.filename = '../Instructions/sections'	
		elif topic == 'solutions':
			self.filename = '../Instructions/solutions'	
		elif topic == 'boundaries':
			self.filename = '../Instructions/boundary_conditions'	
		elif topic == 'constraints':
			self.filename = '../Instructions/multipoint_constraints'	
		elif topic == 'loads':
			self.filename = '../Instructions/loads'	
		elif topic == 'solver':
			self.filename = '../Instructions/solver'	
		elif topic == 'results':
			self.filename = '../Instructions/results'
		elif topic == 'tutorial_ROD2N2D':
			self.filename = '../Instructions/tutorial_ROD2N2D'
		elif topic == 'tutorial_ROD2N':
			self.filename = '../Instructions/tutorial_ROD2N'
		elif topic == 'tutorial_BEAM2N2D':
			self.filename = '../Instructions/tutorial_BEAM2N2D'
		elif topic == 'tutorial_BEAM2N':
			self.filename = '../Instructions/tutorial_BEAM2N'
		elif topic == 'tutorial_TRI3N':
			self.filename = '../Instructions/tutorial_TRI3N'
		elif topic == 'tutorial_TRI6N':
			self.filename = '../Instructions/tutorial_TRI6N'
		elif topic == 'tutorial_QUAD4N':
			self.filename = '../Instructions/tutorial_QUAD4N'
		elif topic == 'tutorial_QUAD8N':
			self.filename = '../Instructions/tutorial_QUAD8N'
		elif topic == 'tutorial_TET4N':
			self.filename = '../Instructions/tutorial_TET4N'
		elif topic == 'tutorial_TET10N':
			self.filename = '../Instructions/tutorial_TET10N'
		elif topic == 'tutorial_HEX8N':
			self.filename = '../Instructions/tutorial_HEX8N'
		elif topic == 'tutorial_HEX20N':
			self.filename = '../Instructions/tutorial_HEX20N'
		else:
			print('\tUnknown help request:', topic)
			self.close()
		
		self.lbl = QtWidgets.QLabel('<font color=Black size=12><b> Unknown Help request: '+topic+' </b></font>')
		self.pix_size = QtWidgets.QDesktopWidget().screenGeometry().height()-100
		self.pix_size = 800
		self.pix = QtGui.QPixmap(self.filename+'_'+str(self.page_number)+'.png')
		self.lbl.setPixmap(self.pix.scaledToHeight(self.pix_size))

		# Initialize the pushbuttons
		button_next = QtWidgets.QPushButton('Next -->', self)
		button_next.clicked.connect(self.switchToNext)

		button_previous = QtWidgets.QPushButton('<-- Previous', self)
		button_previous.clicked.connect(self.switchToPrevious)

		button_size = QtCore.QSize(120, 22);
		button_next.setFixedSize(button_size)
		button_previous.setFixedSize(button_size)

		# set up the layout
		layoutM = QtWidgets.QVBoxLayout()
		layout1 = QtWidgets.QVBoxLayout()
		layout2 = QtWidgets.QHBoxLayout()

		layout1.addWidget(self.lbl)
		layout2.addWidget(button_previous)
		layout2.addWidget(button_next)

		layoutM.addLayout(layout1)
		layoutM.addLayout(layout2)

		self.setLayout(layoutM)
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

	def switchToNext(self):
		if os.path.exists(self.filename+'_'+str(self.page_number+1)+'.png'):
			self.page_number += 1
			self.pix = QtGui.QPixmap(self.filename+'_'+str(self.page_number)+'.png')
			self.lbl.setPixmap(self.pix.scaledToHeight(self.pix_size))
		
	def switchToPrevious(self):
		if os.path.exists(self.filename+'_'+str(self.page_number-1)+'.png'):
			self.page_number -= 1
			self.pix = QtGui.QPixmap(self.filename+'_'+str(self.page_number)+'.png')
			self.lbl.setPixmap(self.pix.scaledToHeight(self.pix_size))







