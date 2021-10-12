#! /usr/bin/env python3
#
#
#	meshFEM.py
#  ------------
#
#	This is the meshFEM module. It takes input from the
#	user inside the viewer to generate elements in a very
#	basic way. Not meant to mesh complex geometry from
#	an external CAD-program, but rather give the user a
#	chance to build simplistic models for quick and dirty
#	FE-models.
#	


import sys
from PyQt5 import QtGui, QtCore, QtWidgets

sys.path.insert(1, '../Objects')

from nodes import *
from elements import *





class MakeElements(QtWidgets.QWidget):
	'''
Create new element(s) as specified by
user in dialog box.
'''
	window_closed = QtCore.pyqtSignal()

	def __init__(self, new_elements):
		super(MakeElements, self).__init__()
		self.setWindowTitle('Make Element(s)')

		self.new_elements = new_elements
		self.element_type = 'BEAM2N'

		self.element_types = {'BEAM2N2D': QtGui.QPixmap('../Icons/pix_rod2_beam2.png'),
							  'ROD2N2D' : QtGui.QPixmap('../Icons/pix_rod2_beam2.png'),
							  'BEAM2N'  : QtGui.QPixmap('../Icons/pix_rod2_beam2.png'),
							  'ROD2N'   : QtGui.QPixmap('../Icons/pix_rod2_beam2.png'),
#							  'TRI3N'   : QtGui.QPixmap('../Icons/pix_tri3.png'),
#							  'TRI6N'   : QtGui.QPixmap('../Icons/pix_tri6.png'),
							  'QUAD4N'  : QtGui.QPixmap('../Icons/pix_quad4.png'),
#							  'QUAD8N'  : QtGui.QPixmap('../Icons/pix_quad8.png'),
#							  'TET4N'   : QtGui.QPixmap('../Icons/pix_tet4.png'),
#							  'TET10N'  : QtGui.QPixmap('../Icons/pix_tet10.png'),
							  'HEX8N'   : QtGui.QPixmap('../Icons/pix_hex8.png')}#,
#							  'HEX20N'  : QtGui.QPixmap('../Icons/pix_hex20.png')}

		# Initialize the labels
		self.labels = [ QtWidgets.QLabel('Element size'), 
						QtWidgets.QLabel('Node 1 (optional)'), 
						QtWidgets.QLabel('Node 2 (optional)'),
						QtWidgets.QLabel('Element type'),
						QtWidgets.QLabel('element_pix') ]
		self.labels[4].setPixmap(self.element_types['BEAM2N2D'])

		# Initialize the selection box
		self.selection_box = QtWidgets.QComboBox()
		self.selection_box.addItems(list(self.element_types.keys()))
		self.selection_box.currentIndexChanged[str].connect(self.boxChoiceChanged)

		# Initialize the input textboxes
		self.line_edits = [ QtWidgets.QLineEdit(),
							QtWidgets.QLineEdit(),
							QtWidgets.QLineEdit() ]
		for line in range(len(self.line_edits)):
			self.line_edits[line].setMaxLength(40)
		self.line_edits[0].setPlaceholderText('1.')

		# Initialize the pushbuttons
		button_ok = QtWidgets.QPushButton('OK', self)
		button_ok.clicked.connect(self.returnInput)
		button_ok.clicked.connect(self.close)

		button_cancel = QtWidgets.QPushButton('Cancel', self)
		button_cancel.clicked.connect(self.close)

		# Put all the labels, selection boxes, textboxes
		# and buttons into the layout of the dialog box
		layout1 = QtWidgets.QVBoxLayout()
		layout2 = QtWidgets.QHBoxLayout()
		layout3 = QtWidgets.QVBoxLayout()
		layout4 = QtWidgets.QVBoxLayout()
		layout5 = QtWidgets.QHBoxLayout()

		layout1.setContentsMargins(20,20,20,20)
		layout1.setSpacing(20)

		layout3.addWidget(self.labels[3])
		layout3.addWidget(self.labels[0])
		layout3.addWidget(self.labels[1])
		layout3.addWidget(self.labels[2])

		layout4.addWidget(self.selection_box)
		layout4.addWidget(self.line_edits[0])
		layout4.addWidget(self.line_edits[1])
		layout4.addWidget(self.line_edits[2])

		layout2.addLayout(layout3)
		layout2.addLayout(layout4)
		layout2.addWidget(self.labels[4])

		layout5.addWidget(button_cancel)
		layout5.addWidget(button_ok)
        
		layout1.addLayout(layout2)
		layout1.addLayout(layout5)

		self.setLayout(layout1)
		self.center()


	def closeEvent(self, event):
		'''
	Signals to the main window that the selectionWidget
	has been closed so the main window will know it should
	refresh now
	'''
		self.window_closed.emit()
		event.accept()


	def center(self):
		'''
	Center Window on the Current Screen,
	with Multi-Monitor support
	'''
		self.showNormal()
		window_geometry = self.frameGeometry()
		mousepointer_position = QtWidgets.QApplication.desktop().cursor().pos()
		screen = QtWidgets.QApplication.desktop().screenNumber(mousepointer_position)
		centerPoint = QtWidgets.QApplication.desktop().screenGeometry(screen).center()
		window_geometry.moveCenter(centerPoint)
		return bool(not self.move(window_geometry.topLeft()))


	def boxChoiceChanged(self, index):
		'''
	Change the element depicted so it
	corresponds to the one selected.
	'''
		self.labels[4].setPixmap(self.element_types[str(index)])
		self.element_type = str(index)


	def returnInput(self):
		'''
	Set the values of self.new_elements
	to be returned.
	'''
		self.new_elements['Element type'] = self.element_type
		if str(self.line_edits[0].text()) == '':
			self.new_elements['Element size'] = str(self.line_edits[0].placeholderText())
		else:
			self.new_elements['Element size'] = str(self.line_edits[0].text())
		self.new_elements['Node 1'] = str(self.line_edits[1].text())
		self.new_elements['Node 2'] = str(self.line_edits[2].text())





class ExtrudeElements(QtWidgets.QWidget):
	'''
Create new element(s) as specified by
user in dialog box.
'''
	window_closed = QtCore.pyqtSignal()

	def __init__(self, selected_elements, element_type, extrude_elements):
		super(ExtrudeElements, self).__init__()
		self.setWindowTitle('Extrude Element(s)')

		self.element_type = element_type
		self.selected_elements = selected_elements
		self.extrude_elements = extrude_elements
		self.extrusion_scenarios = ['straight', 'angled']
		self.extrude_elements['Extrude scenario'] = 'straight'
		self.extrusion_scenario = { '1D straight': QtGui.QPixmap('../Icons/pix_1D_extrusion_str.png'),
									'1D angled':   QtGui.QPixmap('../Icons/pix_1D_extrusion_ang.png'),
									'2D straight': QtGui.QPixmap('../Icons/pix_2D_extrusion_str.png'),
									'2D str.many': QtGui.QPixmap('../Icons/pix_2D_extrusion_str_many.png'),
									'2D angled':   QtGui.QPixmap('../Icons/pix_2D_extrusion_ang.png'),
									'2D ang.many': QtGui.QPixmap('../Icons/pix_2D_extrusion_ang_many.png'),
									'3D straight': QtGui.QPixmap('../Icons/pix_3D_extrusion_str.png'),
									'3D str.many': QtGui.QPixmap('../Icons/pix_3D_extrusion_str_many.png'),
									'3D angled':   QtGui.QPixmap('../Icons/pix_3D_extrusion_ang.png'),
									'3D ang.many': QtGui.QPixmap('../Icons/pix_3D_extrusion_ang_many.png') }

		# Initialize the labels
		self.labels = [ QtWidgets.QLabel('Extrude scenario'),
						QtWidgets.QLabel('Extrude direction [x,y,z]'), 
						QtWidgets.QLabel('Extrude number'), 
						QtWidgets.QLabel('Extrude angle'),
						QtWidgets.QLabel('Extrude angle axis'),
						QtWidgets.QLabel('Extrude angle radius'),
						QtWidgets.QLabel('element_pix') ]
		if self.element_type in ['ROD2N2D', 'ROD2N', 'BEAM2N2D', 'BEAM2N']:
			self.labels[6].setPixmap(self.extrusion_scenario['1D straight'])
		elif self.element_type in ['TRI3N', 'TRI6N', 'QUAD4N', 'QUAD8N']:
			if len(self.selected_elements) != 1:
				self.labels[6].setPixmap(self.extrusion_scenario['2D str.many'])
			else:
				self.labels[6].setPixmap(self.extrusion_scenario['2D straight'])
		elif self.element_type in ['HEX8N', 'HEX20N', 'TET4N', 'TET10N']:
			if len(self.selected_elements) != 1:
				self.labels[6].setPixmap(self.extrusion_scenario['3D str.many'])
			else:
				self.labels[6].setPixmap(self.extrusion_scenario['3D straight'])
		else:
			print('\n\tUNKNOWN ELEMENT TYPE', self.element_type)

		# Initialize the selection box
		self.selection_box = QtWidgets.QComboBox()
		self.selection_box.addItems(self.extrusion_scenarios)
		self.selection_box.currentIndexChanged[str].connect(self.boxChoiceChanged)

		# Initialize the input textboxes
		self.line_edits = [ QtWidgets.QLineEdit(),
							QtWidgets.QLineEdit(),
							QtWidgets.QLineEdit(),
							QtWidgets.QLineEdit(),
							QtWidgets.QLineEdit() ]
		for line in range(len(self.line_edits)):
			self.line_edits[line].setMaxLength(40)
		self.line_edits[0].setPlaceholderText('1,0,0')
		self.line_edits[1].setPlaceholderText('5')
		self.line_edits[2].setPlaceholderText('0')
		self.line_edits[2].setEnabled(False)
		self.line_edits[3].setPlaceholderText('0,0,1')
		self.line_edits[3].setEnabled(False)
		self.line_edits[4].setPlaceholderText('10')
		self.line_edits[4].setEnabled(False)

		# Initialize the pushbuttons
		button_ok = QtWidgets.QPushButton('OK', self)
		button_ok.clicked.connect(self.returnInput)
		button_ok.clicked.connect(self.close)

		button_cancel = QtWidgets.QPushButton('Cancel', self)
		button_cancel.clicked.connect(self.close)

		# Put all the labels, selection boxes, textboxes
		# and buttons into the layout of the dialog box
		layout1 = QtWidgets.QVBoxLayout()
		layout2 = QtWidgets.QHBoxLayout()
		layout3 = QtWidgets.QVBoxLayout()
		layout4 = QtWidgets.QVBoxLayout()
		layout5 = QtWidgets.QHBoxLayout()

		layout1.setContentsMargins(20,20,20,20)
		layout1.setSpacing(20)

		layout3.addWidget(self.labels[0])
		layout3.addWidget(self.labels[1])
		layout3.addWidget(self.labels[2])
		layout3.addWidget(self.labels[3])
		layout3.addWidget(self.labels[4])
		layout3.addWidget(self.labels[5])

		layout4.addWidget(self.selection_box)
		layout4.addWidget(self.line_edits[0])
		layout4.addWidget(self.line_edits[1])
		layout4.addWidget(self.line_edits[2])
		layout4.addWidget(self.line_edits[3])
		layout4.addWidget(self.line_edits[4])

		layout2.addLayout(layout3)
		layout2.addLayout(layout4)
		layout2.addWidget(self.labels[6])

		layout5.addWidget(button_cancel)
		layout5.addWidget(button_ok)
        
		layout1.addLayout(layout2)
		layout1.addLayout(layout5)

		self.setLayout(layout1)
		self.center()


	def closeEvent(self, event):
		'''
	Signals to the main window that the selectionWidget
	has been closed so the main window will know it should
	refresh now
	'''
		self.window_closed.emit()
		event.accept()


	def center(self):
		'''
	Center Window on the Current Screen,
	with Multi-Monitor support
	'''
		self.showNormal()
		window_geometry = self.frameGeometry()
		mousepointer_position = QtWidgets.QApplication.desktop().cursor().pos()
		screen = QtWidgets.QApplication.desktop().screenNumber(mousepointer_position)
		centerPoint = QtWidgets.QApplication.desktop().screenGeometry(screen).center()
		window_geometry.moveCenter(centerPoint)
		return bool(not self.move(window_geometry.topLeft()))


	def boxChoiceChanged(self, index):
		'''
	Change the element depicted so it
	corresponds to the one selected.
	'''
		self.extrude_elements['Extrude scenario'] = str(index)
		if str(index) == 'straight':
			self.line_edits[2].setEnabled(False)
			self.line_edits[3].setEnabled(False)
			self.line_edits[4].setEnabled(False)
		else:
			self.line_edits[2].setEnabled(True)
			self.line_edits[3].setEnabled(True)
			self.line_edits[4].setEnabled(True)
		if self.element_type in ['ROD2N2D', 'ROD2N', 'BEAM2N2D', 'BEAM2N']:
			if self.extrude_elements['Extrude scenario'] == 'straight':
				self.labels[6].setPixmap(self.extrusion_scenario['1D straight'])
			else:
				self.labels[6].setPixmap(self.extrusion_scenario['1D angled'])
		elif self.element_type in ['TRI3N', 'TRI6N', 'QUAD4N', 'QUAD8N']:
			if len(self.selected_elements) != 1:
				if self.extrude_elements['Extrude scenario'] == 'straight':
					self.labels[6].setPixmap(self.extrusion_scenario['2D str.many'])
				else:
					self.labels[6].setPixmap(self.extrusion_scenario['2D ang.many'])
			else:
				if self.extrude_elements['Extrude scenario'] == 'straight':
					self.labels[6].setPixmap(self.extrusion_scenario['2D straight'])
				else:
					self.labels[6].setPixmap(self.extrusion_scenario['2D angled'])
		elif self.element_type in ['HEX8N', 'HEX20N', 'TET4N', 'TET10N']:
			if len(self.selected_elements) != 1:
				if self.extrude_elements['Extrude scenario'] == 'straight':
					self.labels[6].setPixmap(self.extrusion_scenario['3D str.many'])
				else:
					self.labels[6].setPixmap(self.extrusion_scenario['3D ang.many'])
			else:
				if self.extrude_elements['Extrude scenario'] == 'straight':
					self.labels[6].setPixmap(self.extrusion_scenario['3D straight'])
				else:
					self.labels[6].setPixmap(self.extrusion_scenario['3D angled'])
		else:
			print('\n\tUNKNOWN ELEMENT TYPE')



	def returnInput(self):
		'''
	Set the values of self.extrude_elements
	to be returned.
	'''
		self.extrude_elements['Element type'] = self.element_type
		if str(self.line_edits[0].text()) == '':
			self.extrude_elements['Extrude direction'] = str(self.line_edits[0].placeholderText())
		else:
			self.extrude_elements['Extrude direction'] = str(self.line_edits[0].text())
		if str(self.line_edits[1].text()) == '':
			self.extrude_elements['Extrude number'] = str(self.line_edits[1].placeholderText())
		else:
			self.extrude_elements['Extrude number'] = str(self.line_edits[1].text())
		if str(self.line_edits[2].text()) == '':
			self.extrude_elements['Extrude angle'] = str(self.line_edits[2].placeholderText())
		else:
			self.extrude_elements['Extrude angle'] = str(self.line_edits[2].text())
		if str(self.line_edits[3].text()) == '':
			self.extrude_elements['Extrude angle axis'] = str(self.line_edits[3].placeholderText())
		else:
			self.extrude_elements['Extrude angle axis'] = str(self.line_edits[3].text())
		if str(self.line_edits[4].text()) == '':
			self.extrude_elements['Extrude angle radius'] = str(self.line_edits[4].placeholderText())
		else:
			self.extrude_elements['Extrude angle radius'] = str(self.line_edits[4].text())






