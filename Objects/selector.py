#
#
#	selector.py
#  --------------
#
#	This is the selector module. It defines the InputDialog
#	object used for taking input directly from the user.
#


import sys
from numpy import pi
from PyQt5 import QtGui, QtCore, QtWidgets




class InputDialog(QtWidgets.QWidget):
	'''
Class for making a dialog box taking text input
and choices (selection boxes) from user.
'''
	window_closed = QtCore.pyqtSignal()

	def __init__(self, allInput, title, newVariables):
		super(InputDialog, self).__init__()

		self.setWindowTitle(title)
		self.setWindowIcon(QtGui.QIcon('../Icons/icon_view_result.png'))

		self.inputs = allInput['inputs']
		self.current = allInput['current']
		self.choices = allInput['choices']
		self.inOrder = allInput['inOrder']
		self.newVariables = newVariables

		# Initialize the labels
		self.labels = []
		for label in range(len(self.inOrder)):
			self.labels.append(QtWidgets.QLabel(self.inOrder[label]))
			self.labels[label].setAlignment(QtCore.Qt.AlignCenter)

		# Initialize the selection boxes
		self.select_boxes = {}
		for box in range(len(self.choices[0])):
			self.select_boxes[self.choices[0][box]] = QtWidgets.QComboBox()
			if isinstance(self.choices[1], list):
				self.select_boxes[self.choices[0][box]].addItems(self.choices[1])
				self.setBoxChoiceToCurrent(self.select_boxes[self.choices[0][box]], self.choices[1], self.current[self.choices[0][box]])
				self.select_boxes[self.choices[0][box]].currentIndexChanged[str].connect(self.boxChoiceChanged)
			else:
				if box == 0:
					box1_list = []
					for choice in self.choices[1]:
						box1_list.append(choice)
					self.select_boxes[self.choices[0][box]].addItems(box1_list)
					self.setBoxChoiceToCurrent(self.select_boxes[self.choices[0][box]], box1_list, self.current[self.choices[0][box]])
					self.select_boxes[self.choices[0][box]].currentIndexChanged[str].connect(self.boxChoiceChanged)
				if box == 1:
					box2_list = []
					for choice in self.choices[1][self.current[self.choices[0][0]]]:
						box2_list.append(choice)
					self.select_boxes[self.choices[0][box]].addItems(box2_list)
					self.setBoxChoiceToCurrent(self.select_boxes[self.choices[0][box]], box2_list, self.current[self.choices[0][box]])
					self.select_boxes[self.choices[0][box]].currentIndexChanged[str].connect(self.boxChoiceChanged)
				if box == 2:
					box3_list = self.choices[1][self.current[self.choices[0][0]]][self.current[self.choices[0][1]]]
					self.select_boxes[self.choices[0][box]].addItems(box3_list)
					self.setBoxChoiceToCurrent(self.select_boxes[self.choices[0][box]], box3_list, self.current[self.choices[0][box]])
					self.select_boxes[self.choices[0][box]].currentIndexChanged[str].connect(self.boxChoiceChanged)

		# Initialize the input textboxes
		self.line_edits = {}
		for line in self.inputs:
			self.line_edits[line] = QtWidgets.QLineEdit()
			self.line_edits[line].setMaxLength(40)
			self.line_edits[line].setPlaceholderText(self.inputs[line])

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

		for label in range(len(self.inOrder)):
			layout3.addWidget(self.labels[label])
			if self.inOrder[label] in allInput['inputs']:
				layout4.addWidget(self.line_edits[self.inOrder[label]])
			if self.inOrder[label] in allInput['choices'][0]:
				layout4.addWidget(self.select_boxes[self.inOrder[label]])

		layout2.addLayout(layout3)
		layout2.addLayout(layout4)

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


	def boxChoiceChanged(self, selected):
		'''
	Updates self.current to be what was selected
	by the user in the combobox. Also updates any
	underlying comboboxes which now are linked to
	the new selection with the use of function
	self.setBoxChoiceToCurrent().
	'''
		if isinstance(self.choices[1], list):
			self.current[self.choices[0][0]] = str(selected)
		else:
			if str(selected) in self.choices[1]:
				self.current[self.choices[0][0]] = str(selected)
				box2_list = []
				for choice in self.choices[1][self.current[self.choices[0][0]]]:
					box2_list.append(choice)
				self.select_boxes[self.choices[0][1]].clear()
				self.select_boxes[self.choices[0][1]].addItems(box2_list)
				self.setBoxChoiceToCurrent(self.select_boxes[self.choices[0][1]], box2_list, box2_list[0])
				self.select_boxes[self.choices[0][1]].currentIndexChanged[str].connect(self.boxChoiceChanged)
				if isinstance(self.choices[1][self.current[self.choices[0][0]]], list):
					pass
				else:
					box3_list = self.choices[1][self.current[self.choices[0][0]]][self.current[self.choices[0][1]]]
					self.select_boxes[self.choices[0][2]].clear()
					self.select_boxes[self.choices[0][2]].addItems(box3_list)
					self.setBoxChoiceToCurrent(self.select_boxes[self.choices[0][2]], box3_list, box3_list[0])
					self.select_boxes[self.choices[0][2]].currentIndexChanged[str].connect(self.boxChoiceChanged)
			elif str(selected) in self.choices[1][self.current[self.choices[0][0]]]:
				self.current[self.choices[0][1]] = str(selected)
				if isinstance(self.choices[1][self.current[self.choices[0][0]]], list):
					pass
				else:
					box3_list = self.choices[1][self.current[self.choices[0][0]]][self.current[self.choices[0][1]]]
					self.select_boxes[self.choices[0][2]].clear()
					self.select_boxes[self.choices[0][2]].addItems(box3_list)
					self.setBoxChoiceToCurrent(self.select_boxes[self.choices[0][2]], box3_list, box3_list[0])
					self.select_boxes[self.choices[0][2]].currentIndexChanged[str].connect(self.boxChoiceChanged)
			else:
				if isinstance(self.choices[1][self.current[self.choices[0][0]]], list):
					pass
				else:
					self.current[self.choices[0][2]] = str(selected)


	def setBoxChoiceToCurrent(self, combobox, choices, current):
		'''
	Updates the combobox to be on the current selection
	as specified by variable. This is used to initialize
	the combobox before the user has interacted with it,
	or when the combobox is cleared and a new list of
	items are added to it.
	'''
		init_index = 0
		for i in range(len(choices)):
			if choices[i] == current:
				break
			init_index += 1
		combobox.setCurrentIndex(init_index)


	def returnInput(self):
		'''
	Changes self.inputs to what the user has
	written in the QLineEdit widgets. Alternatively
	if user has not written anything, the placeholder
	text is used.
	'''
		check_input = {}
		for prop in self.inputs:
			check_input[prop] = True
			if str(self.line_edits[prop].text()) == '':
				check_input[prop] = False
		for prop in self.inputs:
			if check_input[prop] == True:
				self.inputs[prop] = str(self.line_edits[prop].text())
			else:
				self.inputs[prop] = str(self.line_edits[prop].placeholderText())
		for prop in self.inputs:
			self.newVariables[prop] = self.inputs[prop]
		for prop in self.current:
			self.newVariables[prop] = self.current[prop]



class InputSolFile(QtWidgets.QWidget):
	'''
Class for making a dialog box letting user
set up the sol-file which will be used in
FE-solver.
'''
	window_closed = QtCore.pyqtSignal()

	def __init__(self,allInput, newVariables):
		super(InputSolFile, self).__init__()

		self.setWindowTitle('New sol-file')
		self.setWindowIcon(QtGui.QIcon('../Icons/icon_new_file.png'))

		self.inputs = allInput['inputs']
		self.current = allInput['current']
		self.choices = allInput['choices']
		self.newVariables = newVariables

		self.boldFont=QtGui.QFont()
		self.boldFont.setBold(True)

		# Initialize the labels
		self.name_label = QtWidgets.QLabel('File name')
		self.name_label.setAlignment(QtCore.Qt.AlignCenter)
		self.name_line = QtWidgets.QLineEdit()
		self.name_line.setMaxLength(48)
		self.name_line.setPlaceholderText(self.inputs['Name'])

		self.solution_label = QtWidgets.QLabel('Solution')
		self.solution_label.setAlignment(QtCore.Qt.AlignCenter)
		self.blank_label = QtWidgets.QLabel('\t---\t---\t---')
		self.blank_label.setAlignment(QtCore.Qt.AlignCenter)

		# Initialize the combobox
		self.solution_box = QtWidgets.QComboBox()
		box_list = []
		for sol in self.choices[1]:
			box_list.append(sol)
		self.solution_box.addItems(box_list)
		self.setBoxChoiceToCurrent(self.solution_box, box_list, self.current['Solution'])
		self.solution_box.currentIndexChanged[str].connect(self.boxChoiceChanged)

		# Initialize the pushbuttons
		self.button_add = QtWidgets.QPushButton('Add...')
		self.button_add.clicked.connect(self.addSolution)

		self.button_ok = QtWidgets.QPushButton('OK', self)
		self.button_ok.clicked.connect(self.returnInput)
		self.button_ok.clicked.connect(self.close)

		self.button_cancel = QtWidgets.QPushButton('Cancel', self)
		self.button_cancel.clicked.connect(self.close)

		# Put all the labels, selection boxes, textboxes,
		# checkbox and buttons into the layout of the dialog box
		self.layout1 = QtWidgets.QVBoxLayout()
		self.layout2 = QtWidgets.QHBoxLayout()
		self.layout3 = QtWidgets.QHBoxLayout()
		self.layout4 = QtWidgets.QHBoxLayout()
		self.layout5 = QtWidgets.QVBoxLayout()
		self.layout6 = QtWidgets.QHBoxLayout()

		self.layout1.setContentsMargins(20,20,20,20)
		self.layout1.setSpacing(20)

		self.layout2.addWidget(self.name_label)
		self.layout2.addWidget(self.name_line)
		self.layout3.addWidget(self.solution_label)
		self.layout3.addWidget(self.solution_box)
		self.layout3.addWidget(self.button_add)
		self.layout4.addWidget(self.blank_label)
	
		self.sol_num = 0
		self.solution_layouts = {}

		self.layout6.addWidget(self.button_cancel)
		self.layout6.addWidget(self.button_ok)
        
		self.layout1.addLayout(self.layout2)
		self.layout1.addLayout(self.layout3)
		self.layout1.addLayout(self.layout4)
		self.layout1.addLayout(self.layout5)
		self.layout1.addLayout(self.layout6)

		self.setLayout(self.layout1)
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


	def addSolution(self):
		'''
	Adds a new solution to the main widget,
	with combobox for the user to select which
	solution they want to add.
	'''
		self.solution_layouts[self.sol_num] = {'layout': QtWidgets.QVBoxLayout(),
											   'sublayout1': QtWidgets.QHBoxLayout(),
											   'sublayout2': QtWidgets.QHBoxLayout(),
											   'sublayout3': QtWidgets.QHBoxLayout(),
											   'sublayout4': QtWidgets.QHBoxLayout(),
											   'sublayout5': QtWidgets.QHBoxLayout(),
											   'sublayout6': QtWidgets.QHBoxLayout(),
											   'sublayout7': QtWidgets.QHBoxLayout(),
											   'sublayout8': QtWidgets.QHBoxLayout(),
											   'sublayout9': QtWidgets.QHBoxLayout(),
											   'sublayout10': QtWidgets.QHBoxLayout(),
											   'sublayout11': QtWidgets.QHBoxLayout(),
											   'sublayout12': QtWidgets.QHBoxLayout(),
											   'sublayout13': QtWidgets.QHBoxLayout(),
											   'solution_label': QtWidgets.QLabel(self.current['Solution'])}

		blank_label = QtWidgets.QLabel('\t---\t---\t---')
		blank_label.setAlignment(QtCore.Qt.AlignCenter)
		node_elem_set_label = QtWidgets.QLabel('Node-/Elementsets')
		node_elem_set_label.setAlignment(QtCore.Qt.AlignLeft)
		num_modeshapes_label = QtWidgets.QLabel('Number of Eigenmodes')
		num_modeshapes_label.setAlignment(QtCore.Qt.AlignLeft)
		plot_label = QtWidgets.QLabel('Plt')
		plot_label.setAlignment(QtCore.Qt.AlignRight)
		plot_label.setFixedWidth(20)
		text_label = QtWidgets.QLabel('Txt')
		text_label.setAlignment(QtCore.Qt.AlignRight)
		text_label.setFixedWidth(20)
		displacement_label = QtWidgets.QLabel('Displacement')
		displacement_label.setAlignment(QtCore.Qt.AlignLeft)
		displacement_label.setFixedWidth(100)
		velocity_label = QtWidgets.QLabel('Velocity')
		velocity_label.setAlignment(QtCore.Qt.AlignLeft)
		velocity_label.setFixedWidth(100)
		acceleration_label = QtWidgets.QLabel('Acceleration')
		acceleration_label.setAlignment(QtCore.Qt.AlignLeft)
		acceleration_label.setFixedWidth(100)
		frf_accel_label = QtWidgets.QLabel('FFT Acceleration')
		frf_accel_label.setAlignment(QtCore.Qt.AlignLeft)
		frf_accel_label.setFixedWidth(100)
		nodeforce_label = QtWidgets.QLabel('Nodeforce')
		nodeforce_label.setAlignment(QtCore.Qt.AlignLeft)
		nodeforce_label.setFixedWidth(100)
		stress_label = QtWidgets.QLabel('Stress')
		stress_label.setAlignment(QtCore.Qt.AlignLeft)
		stress_label.setFixedWidth(100)
		strain_label = QtWidgets.QLabel('Strain')
		strain_label.setAlignment(QtCore.Qt.AlignLeft)
		strain_label.setFixedWidth(100)
		elementforce_label = QtWidgets.QLabel('Elementforce')
		elementforce_label.setAlignment(QtCore.Qt.AlignLeft)
		elementforce_label.setFixedWidth(100)
		modeshapes_label = QtWidgets.QLabel('Modeshapes')
		modeshapes_label.setAlignment(QtCore.Qt.AlignLeft)
		modeshapes_label.setFixedWidth(100)
		dampratio_label = QtWidgets.QLabel('Damping Ratio\n(filename if by freq)')
		dampratio_label.setAlignment(QtCore.Qt.AlignLeft)
		dampratio_label.setFixedWidth(120)
		forcetable_label = QtWidgets.QLabel('Force/Acceleration\n(filename)')
		forcetable_label.setAlignment(QtCore.Qt.AlignLeft)
		forcetable_label.setFixedWidth(120)

		self.solution_layouts[self.sol_num]['solution_label'].setAlignment(QtCore.Qt.AlignCenter)
		self.solution_layouts[self.sol_num]['solution_label'].setFont(self.boldFont)
		self.solution_layouts[self.sol_num]['solution_label'].setFixedWidth(100)
		self.solution_layouts[self.sol_num]['sublayout1'].addWidget(self.solution_layouts[self.sol_num]['solution_label'])
		if 'disp' not in self.choices[1][self.current['Solution']]:
			self.solution_layouts[self.sol_num]['sublayout1'].addWidget(num_modeshapes_label)
		else:
			self.solution_layouts[self.sol_num]['sublayout1'].addWidget(node_elem_set_label)
		self.solution_layouts[self.sol_num]['sublayout1'].addWidget(plot_label)
		self.solution_layouts[self.sol_num]['sublayout1'].addWidget(text_label)
		self.solution_layouts[self.sol_num]['layout'].addLayout(self.solution_layouts[self.sol_num]['sublayout1'])

		self.solution_layouts[self.sol_num]['Results'] = {}
		for result in self.choices[1][self.current['Solution']]:
			if result == 'disp':
				self.solution_layouts[self.sol_num]['Results']['disp'] = {}
				self.solution_layouts[self.sol_num]['Results']['disp']['line_edit'] = QtWidgets.QLineEdit()
				self.solution_layouts[self.sol_num]['Results']['disp']['line_edit'].setMaxLength(12)
				self.solution_layouts[self.sol_num]['Results']['disp']['line_edit'].setPlaceholderText('1')
				self.solution_layouts[self.sol_num]['Results']['disp']['checkbox_plot'] = QtWidgets.QCheckBox()
				self.solution_layouts[self.sol_num]['Results']['disp']['checkbox_plot'].setCheckState(QtCore.Qt.Checked)
				self.solution_layouts[self.sol_num]['Results']['disp']['checkbox_plot'].setEnabled(False)
				self.solution_layouts[self.sol_num]['Results']['disp']['checkbox_text'] = QtWidgets.QCheckBox()
			elif result == 'velc':
				self.solution_layouts[self.sol_num]['Results']['velc'] = {}
				self.solution_layouts[self.sol_num]['Results']['velc']['line_edit'] = QtWidgets.QLineEdit()
				self.solution_layouts[self.sol_num]['Results']['velc']['line_edit'].setMaxLength(12)
				self.solution_layouts[self.sol_num]['Results']['velc']['line_edit'].setPlaceholderText('1')
				self.solution_layouts[self.sol_num]['Results']['velc']['checkbox_plot'] = QtWidgets.QCheckBox()
#				self.solution_layouts[self.sol_num]['Results']['velc']['checkbox_plot'].setCheckState(QtCore.Qt.Checked)
#				self.solution_layouts[self.sol_num]['Results']['velc']['checkbox_plot'].setEnabled(False)
				self.solution_layouts[self.sol_num]['Results']['velc']['checkbox_text'] = QtWidgets.QCheckBox()
			elif result == 'accl':
				self.solution_layouts[self.sol_num]['Results']['accl'] = {}
				self.solution_layouts[self.sol_num]['Results']['accl']['line_edit'] = QtWidgets.QLineEdit()
				self.solution_layouts[self.sol_num]['Results']['accl']['line_edit'].setMaxLength(12)
				self.solution_layouts[self.sol_num]['Results']['accl']['line_edit'].setPlaceholderText('1')
				self.solution_layouts[self.sol_num]['Results']['accl']['checkbox_plot'] = QtWidgets.QCheckBox()
#				self.solution_layouts[self.sol_num]['Results']['accl']['checkbox_plot'].setCheckState(QtCore.Qt.Checked)
#				self.solution_layouts[self.sol_num]['Results']['accl']['checkbox_plot'].setEnabled(False)
				self.solution_layouts[self.sol_num]['Results']['accl']['checkbox_text'] = QtWidgets.QCheckBox()
			elif result == 'frf':
				self.solution_layouts[self.sol_num]['Results']['frf'] = {}
				self.solution_layouts[self.sol_num]['Results']['frf']['line_edit'] = QtWidgets.QLineEdit()
				self.solution_layouts[self.sol_num]['Results']['frf']['line_edit'].setMaxLength(12)
				self.solution_layouts[self.sol_num]['Results']['frf']['line_edit'].setPlaceholderText('1')
				self.solution_layouts[self.sol_num]['Results']['frf']['checkbox_plot'] = QtWidgets.QCheckBox()
#				self.solution_layouts[self.sol_num]['Results']['frf']['checkbox_plot'].setCheckState(QtCore.Qt.Checked)
#				self.solution_layouts[self.sol_num]['Results']['frf']['checkbox_plot'].setEnabled(False)
				self.solution_layouts[self.sol_num]['Results']['frf']['checkbox_text'] = QtWidgets.QCheckBox()
			elif result == 'nodf':
				self.solution_layouts[self.sol_num]['Results']['nodf'] = {}
				self.solution_layouts[self.sol_num]['Results']['nodf']['line_edit'] = QtWidgets.QLineEdit()
				self.solution_layouts[self.sol_num]['Results']['nodf']['line_edit'].setMaxLength(12)
				self.solution_layouts[self.sol_num]['Results']['nodf']['line_edit'].setPlaceholderText('All')
				self.solution_layouts[self.sol_num]['Results']['nodf']['checkbox_plot'] = QtWidgets.QCheckBox()
				self.solution_layouts[self.sol_num]['Results']['nodf']['checkbox_plot'].setCheckState(QtCore.Qt.Checked)
				self.solution_layouts[self.sol_num]['Results']['nodf']['checkbox_text'] = QtWidgets.QCheckBox()
			elif result == 'strs':
				self.solution_layouts[self.sol_num]['Results']['strs'] = {}
				self.solution_layouts[self.sol_num]['Results']['strs']['line_edit'] = QtWidgets.QLineEdit()
				self.solution_layouts[self.sol_num]['Results']['strs']['line_edit'].setMaxLength(12)
				self.solution_layouts[self.sol_num]['Results']['strs']['line_edit'].setPlaceholderText('All')
				self.solution_layouts[self.sol_num]['Results']['strs']['checkbox_plot'] = QtWidgets.QCheckBox()
				self.solution_layouts[self.sol_num]['Results']['strs']['checkbox_plot'].setCheckState(QtCore.Qt.Checked)
				self.solution_layouts[self.sol_num]['Results']['strs']['checkbox_text'] = QtWidgets.QCheckBox()
			elif result == 'strn':
				self.solution_layouts[self.sol_num]['Results']['strn'] = {}
				self.solution_layouts[self.sol_num]['Results']['strn']['line_edit'] = QtWidgets.QLineEdit()
				self.solution_layouts[self.sol_num]['Results']['strn']['line_edit'].setMaxLength(12)
				self.solution_layouts[self.sol_num]['Results']['strn']['line_edit'].setPlaceholderText('All')
				self.solution_layouts[self.sol_num]['Results']['strn']['checkbox_plot'] = QtWidgets.QCheckBox()
				self.solution_layouts[self.sol_num]['Results']['strn']['checkbox_plot'].setCheckState(QtCore.Qt.Checked)
				self.solution_layouts[self.sol_num]['Results']['strn']['checkbox_text'] = QtWidgets.QCheckBox()
			elif result == 'elmf':
				self.solution_layouts[self.sol_num]['Results']['elmf'] = {}
				self.solution_layouts[self.sol_num]['Results']['elmf']['line_edit'] = QtWidgets.QLineEdit()
				self.solution_layouts[self.sol_num]['Results']['elmf']['line_edit'].setMaxLength(12)
				self.solution_layouts[self.sol_num]['Results']['elmf']['line_edit'].setPlaceholderText('All')
				self.solution_layouts[self.sol_num]['Results']['elmf']['checkbox_plot'] = QtWidgets.QCheckBox()
				self.solution_layouts[self.sol_num]['Results']['elmf']['checkbox_plot'].setCheckState(QtCore.Qt.Checked)
				self.solution_layouts[self.sol_num]['Results']['elmf']['checkbox_text'] = QtWidgets.QCheckBox()
			elif result == 'modes':
				self.solution_layouts[self.sol_num]['Results']['modes'] = {}
				self.solution_layouts[self.sol_num]['Results']['modes']['line_edit'] = QtWidgets.QLineEdit()
				self.solution_layouts[self.sol_num]['Results']['modes']['line_edit'].setMaxLength(12)
				self.solution_layouts[self.sol_num]['Results']['modes']['line_edit'].setPlaceholderText('8')
				self.solution_layouts[self.sol_num]['Results']['modes']['checkbox_plot'] = QtWidgets.QCheckBox()
				self.solution_layouts[self.sol_num]['Results']['modes']['checkbox_plot'].setCheckState(QtCore.Qt.Checked)
				self.solution_layouts[self.sol_num]['Results']['modes']['checkbox_plot'].setEnabled(False)
				self.solution_layouts[self.sol_num]['Results']['modes']['checkbox_text'] = QtWidgets.QCheckBox()
				self.solution_layouts[self.sol_num]['Results']['modes']['checkbox_text'].setCheckState(QtCore.Qt.Checked)
				self.solution_layouts[self.sol_num]['Results']['modes']['checkbox_text'].setEnabled(False)
			elif result == 'dampratio':
				self.solution_layouts[self.sol_num]['Results']['dampratio'] = {}
				self.solution_layouts[self.sol_num]['Results']['dampratio']['line_edit'] = QtWidgets.QLineEdit()
				self.solution_layouts[self.sol_num]['Results']['dampratio']['line_edit'].setMaxLength(48)
				self.solution_layouts[self.sol_num]['Results']['dampratio']['line_edit'].setPlaceholderText('0.02')
				self.solution_layouts[self.sol_num]['Results']['dampratio']['checkbox_plot'] = QtWidgets.QCheckBox()
				self.solution_layouts[self.sol_num]['Results']['dampratio']['checkbox_plot'].setCheckState(QtCore.Qt.Checked)
				self.solution_layouts[self.sol_num]['Results']['dampratio']['checkbox_plot'].setEnabled(False)
				self.solution_layouts[self.sol_num]['Results']['dampratio']['checkbox_text'] = QtWidgets.QCheckBox()
				self.solution_layouts[self.sol_num]['Results']['dampratio']['checkbox_text'].setCheckState(QtCore.Qt.Checked)
				self.solution_layouts[self.sol_num]['Results']['dampratio']['checkbox_text'].setEnabled(False)
			else:
				self.solution_layouts[self.sol_num]['Results']['forcetable'] = {}
				self.solution_layouts[self.sol_num]['Results']['forcetable']['line_edit'] = QtWidgets.QLineEdit()
				self.solution_layouts[self.sol_num]['Results']['forcetable']['line_edit'].setMaxLength(48)
				self.solution_layouts[self.sol_num]['Results']['forcetable']['line_edit'].setPlaceholderText('filename.tab')
				self.solution_layouts[self.sol_num]['Results']['forcetable']['checkbox_plot'] = QtWidgets.QCheckBox()
				self.solution_layouts[self.sol_num]['Results']['forcetable']['checkbox_plot'].setCheckState(QtCore.Qt.Checked)
				self.solution_layouts[self.sol_num]['Results']['forcetable']['checkbox_plot'].setEnabled(False)
				self.solution_layouts[self.sol_num]['Results']['forcetable']['checkbox_text'] = QtWidgets.QCheckBox()
				self.solution_layouts[self.sol_num]['Results']['forcetable']['checkbox_text'].setCheckState(QtCore.Qt.Checked)
				self.solution_layouts[self.sol_num]['Results']['forcetable']['checkbox_text'].setEnabled(False)

		for result in self.solution_layouts[self.sol_num]['Results']:
			if result == 'disp':
				self.solution_layouts[self.sol_num]['sublayout2'].addWidget(displacement_label)
				self.solution_layouts[self.sol_num]['sublayout2'].addWidget(self.solution_layouts[self.sol_num]['Results']['disp']['line_edit'])
				self.solution_layouts[self.sol_num]['sublayout2'].addWidget(self.solution_layouts[self.sol_num]['Results']['disp']['checkbox_plot'])
				self.solution_layouts[self.sol_num]['sublayout2'].addWidget(self.solution_layouts[self.sol_num]['Results']['disp']['checkbox_text'])
				self.solution_layouts[self.sol_num]['layout'].addLayout(self.solution_layouts[self.sol_num]['sublayout2'])
			elif result == 'velc':
				self.solution_layouts[self.sol_num]['sublayout9'].addWidget(velocity_label)
				self.solution_layouts[self.sol_num]['sublayout9'].addWidget(self.solution_layouts[self.sol_num]['Results']['velc']['line_edit'])
				self.solution_layouts[self.sol_num]['sublayout9'].addWidget(self.solution_layouts[self.sol_num]['Results']['velc']['checkbox_plot'])
				self.solution_layouts[self.sol_num]['sublayout9'].addWidget(self.solution_layouts[self.sol_num]['Results']['velc']['checkbox_text'])
				self.solution_layouts[self.sol_num]['layout'].addLayout(self.solution_layouts[self.sol_num]['sublayout9'])
			elif result == 'accl':
				self.solution_layouts[self.sol_num]['sublayout10'].addWidget(acceleration_label)
				self.solution_layouts[self.sol_num]['sublayout10'].addWidget(self.solution_layouts[self.sol_num]['Results']['accl']['line_edit'])
				self.solution_layouts[self.sol_num]['sublayout10'].addWidget(self.solution_layouts[self.sol_num]['Results']['accl']['checkbox_plot'])
				self.solution_layouts[self.sol_num]['sublayout10'].addWidget(self.solution_layouts[self.sol_num]['Results']['accl']['checkbox_text'])
				self.solution_layouts[self.sol_num]['layout'].addLayout(self.solution_layouts[self.sol_num]['sublayout10'])
			elif result == 'frf':
				self.solution_layouts[self.sol_num]['sublayout11'].addWidget(frf_accel_label)
				self.solution_layouts[self.sol_num]['sublayout11'].addWidget(self.solution_layouts[self.sol_num]['Results']['frf']['line_edit'])
				self.solution_layouts[self.sol_num]['sublayout11'].addWidget(self.solution_layouts[self.sol_num]['Results']['frf']['checkbox_plot'])
				self.solution_layouts[self.sol_num]['sublayout11'].addWidget(self.solution_layouts[self.sol_num]['Results']['frf']['checkbox_text'])
				self.solution_layouts[self.sol_num]['layout'].addLayout(self.solution_layouts[self.sol_num]['sublayout11'])
			elif result == 'nodf':
				self.solution_layouts[self.sol_num]['sublayout3'].addWidget(nodeforce_label)
				self.solution_layouts[self.sol_num]['sublayout3'].addWidget(self.solution_layouts[self.sol_num]['Results']['nodf']['line_edit'])
				self.solution_layouts[self.sol_num]['sublayout3'].addWidget(self.solution_layouts[self.sol_num]['Results']['nodf']['checkbox_plot'])
				self.solution_layouts[self.sol_num]['sublayout3'].addWidget(self.solution_layouts[self.sol_num]['Results']['nodf']['checkbox_text'])
				self.solution_layouts[self.sol_num]['layout'].addLayout(self.solution_layouts[self.sol_num]['sublayout3'])
			elif result == 'strs':
				self.solution_layouts[self.sol_num]['sublayout4'].addWidget(stress_label)
				self.solution_layouts[self.sol_num]['sublayout4'].addWidget(self.solution_layouts[self.sol_num]['Results']['strs']['line_edit'])
				self.solution_layouts[self.sol_num]['sublayout4'].addWidget(self.solution_layouts[self.sol_num]['Results']['strs']['checkbox_plot'])
				self.solution_layouts[self.sol_num]['sublayout4'].addWidget(self.solution_layouts[self.sol_num]['Results']['strs']['checkbox_text'])
				self.solution_layouts[self.sol_num]['layout'].addLayout(self.solution_layouts[self.sol_num]['sublayout4'])
			elif result == 'strn':
				self.solution_layouts[self.sol_num]['sublayout5'].addWidget(strain_label)
				self.solution_layouts[self.sol_num]['sublayout5'].addWidget(self.solution_layouts[self.sol_num]['Results']['strn']['line_edit'])
				self.solution_layouts[self.sol_num]['sublayout5'].addWidget(self.solution_layouts[self.sol_num]['Results']['strn']['checkbox_plot'])
				self.solution_layouts[self.sol_num]['sublayout5'].addWidget(self.solution_layouts[self.sol_num]['Results']['strn']['checkbox_text'])
				self.solution_layouts[self.sol_num]['layout'].addLayout(self.solution_layouts[self.sol_num]['sublayout5'])
			elif result == 'elmf':
				self.solution_layouts[self.sol_num]['sublayout6'].addWidget(elementforce_label)
				self.solution_layouts[self.sol_num]['sublayout6'].addWidget(self.solution_layouts[self.sol_num]['Results']['elmf']['line_edit'])
				self.solution_layouts[self.sol_num]['sublayout6'].addWidget(self.solution_layouts[self.sol_num]['Results']['elmf']['checkbox_plot'])
				self.solution_layouts[self.sol_num]['sublayout6'].addWidget(self.solution_layouts[self.sol_num]['Results']['elmf']['checkbox_text'])
				self.solution_layouts[self.sol_num]['layout'].addLayout(self.solution_layouts[self.sol_num]['sublayout6'])
			elif result == 'modes':
				self.solution_layouts[self.sol_num]['sublayout7'].addWidget(modeshapes_label)
				self.solution_layouts[self.sol_num]['sublayout7'].addWidget(self.solution_layouts[self.sol_num]['Results']['modes']['line_edit'])
				self.solution_layouts[self.sol_num]['sublayout7'].addWidget(self.solution_layouts[self.sol_num]['Results']['modes']['checkbox_plot'])
				self.solution_layouts[self.sol_num]['sublayout7'].addWidget(self.solution_layouts[self.sol_num]['Results']['modes']['checkbox_text'])		
				self.solution_layouts[self.sol_num]['layout'].addLayout(self.solution_layouts[self.sol_num]['sublayout7'])
			elif result == 'dampratio':
				self.solution_layouts[self.sol_num]['sublayout12'].addWidget(dampratio_label)
				self.solution_layouts[self.sol_num]['sublayout12'].addWidget(self.solution_layouts[self.sol_num]['Results']['dampratio']['line_edit'])
#				self.solution_layouts[self.sol_num]['sublayout12'].addWidget(self.solution_layouts[self.sol_num]['Results']['dampratio']['checkbox_plot'])
#				self.solution_layouts[self.sol_num]['sublayout12'].addWidget(self.solution_layouts[self.sol_num]['Results']['dampratio']['checkbox_text'])		
				self.solution_layouts[self.sol_num]['layout'].addLayout(self.solution_layouts[self.sol_num]['sublayout12'])
			else:
				self.solution_layouts[self.sol_num]['sublayout13'].addWidget(forcetable_label)
				self.solution_layouts[self.sol_num]['sublayout13'].addWidget(self.solution_layouts[self.sol_num]['Results']['forcetable']['line_edit'])
#				self.solution_layouts[self.sol_num]['sublayout13'].addWidget(self.solution_layouts[self.sol_num]['Results']['forcetable']['checkbox_plot'])
#				self.solution_layouts[self.sol_num]['sublayout13'].addWidget(self.solution_layouts[self.sol_num]['Results']['forcetable']['checkbox_text'])		
				self.solution_layouts[self.sol_num]['layout'].addLayout(self.solution_layouts[self.sol_num]['sublayout13'])

		self.solution_layouts[self.sol_num]['sublayout8'].addWidget(blank_label)
		self.solution_layouts[self.sol_num]['layout'].addLayout(self.solution_layouts[self.sol_num]['sublayout8'])

		self.layout5.addLayout(self.solution_layouts[self.sol_num]['layout'])
		self.sol_num += 1


	def setBoxChoiceToCurrent(self, combobox, choices, current):
		'''
	Updates the combobox to be on the current selection
	as specified by variable. This is used to initialize
	the combobox before the user has interacted with it.
	'''
		init_index = 0
		for i in range(len(choices)):
			if choices[i] == current:
				break
			init_index += 1
		combobox.setCurrentIndex(init_index)


	def boxChoiceChanged(self, selected):
		'''
	Updates self.current to be what was selected
	by the user in the combobox.
	'''
		self.current['Solution'] = str(selected)


	def returnInput(self):
		'''
	Changes self.newVariables to what the user has
	written in the QLineEdit widgets, and chosen in
	the QCombobox() widgets. Alternatively if user
	has not written anything, the placeholder
	text is used.
	'''
		check_input = True
		if str(self.name_line.text()) == '':
			check_input = False
		if check_input == True:
			self.newVariables['Name'] = str(self.name_line.text())
		else:
			self.newVariables['Name'] = str(self.name_line.placeholderText())
		self.newVariables['Solution'] = {}
		for solution in self.solution_layouts:
			self.newVariables['Solution'][str(self.solution_layouts[solution]['solution_label'].text())] = {}
			for subresult in self.solution_layouts[solution]['Results']:
				if str(self.solution_layouts[solution]['Results'][subresult]['line_edit'].text()) == '':
					nodeset_elementset = str(self.solution_layouts[solution]['Results'][subresult]['line_edit'].placeholderText())
				else:
					nodeset_elementset = str(self.solution_layouts[solution]['Results'][subresult]['line_edit'].text())
				if subresult not in ['dampratio', 'forcetable']:
					self.newVariables['Solution'][str(self.solution_layouts[solution]['solution_label'].text())][subresult] = {}
					if self.solution_layouts[solution]['Results'][subresult]['checkbox_plot'].checkState():
						self.newVariables['Solution'][str(self.solution_layouts[solution]['solution_label'].text())][subresult]['plot'] = nodeset_elementset
					if self.solution_layouts[solution]['Results'][subresult]['checkbox_text'].checkState():
						self.newVariables['Solution'][str(self.solution_layouts[solution]['solution_label'].text())][subresult]['text'] = nodeset_elementset
				else:
					self.newVariables['Solution'][str(self.solution_layouts[solution]['solution_label'].text())][subresult] = nodeset_elementset





class ModifyBeamSection(QtWidgets.QWidget):
	'''
Modify (beam) section as specified by user
with cross section parameters which are used
to calculate beam section area and area moment
of inertia.
'''
	window_closed = QtCore.pyqtSignal()

	def __init__(self, modified_section):
		super(ModifyBeamSection, self).__init__()
		self.setWindowTitle('Modify Beam Section')
		self.setWindowIcon(QtGui.QIcon('../Icons/icon_beam_section.png'))

		self.boldFont=QtGui.QFont()
		self.boldFont.setBold(True)		

		self.modified_section = modified_section
		
		self.section_types = {'I-Beam'	 : QtGui.QPixmap('../Icons/pix_xsect_I-beam.png'),
							  'L-Beam'	 : QtGui.QPixmap('../Icons/pix_xsect_L-beam.png'),
							  'T-Beam'	 : QtGui.QPixmap('../Icons/pix_xsect_T-beam.png'),
							  'C-Beam'   : QtGui.QPixmap('../Icons/pix_xsect_C-beam.png'),
							  'Rectangle': QtGui.QPixmap('../Icons/pix_xsect_rectangle.png'),
							  'Circle'	 : QtGui.QPixmap('../Icons/pix_xsect_circle.png')}

		# Initialize the selection boxes
		self.selection_box_sections = QtWidgets.QComboBox()
		self.selection_box_sections.addItems(sorted(self.modified_section.keys()))
#		self.selection_box_sections.currentIndexChanged[str].connect(self.boxChoiceChanged)
		self.selection_box_sections.setFixedWidth(120)
		
		self.selection_box_types = QtWidgets.QComboBox()
		self.selection_box_types.addItems(sorted(self.section_types.keys()))
		self.selection_box_types.currentIndexChanged[str].connect(self.boxChoiceChanged)
		self.selection_box_types.setFixedWidth(120)

		self.section_type = str(self.selection_box_types.currentText())

		# Initialize the labels
		self.labels = {'Select':	[QtWidgets.QLabel('Section name:        '),
									 QtWidgets.QLabel('Section type:        ')],
					   'Rectangle': [QtWidgets.QLabel('inner width, iw:     '),
								 	 QtWidgets.QLabel('inner height, ih:    '),
								 	 QtWidgets.QLabel('width, w:            '),
								 	 QtWidgets.QLabel('height, h:           '),
								 	 QtWidgets.QLabel('      ---            '),
								 	 QtWidgets.QLabel('      ---            ')],
					   'Circle':	[QtWidgets.QLabel('inner radius, ir:    '),
					   				 QtWidgets.QLabel('radius, r:           '),
								 	 QtWidgets.QLabel('      ---            '),
								 	 QtWidgets.QLabel('      ---            '),
								 	 QtWidgets.QLabel('      ---            '),
								 	 QtWidgets.QLabel('      ---            ')],
					   'I-Beam':	[QtWidgets.QLabel('top width, tw:       '),
								 	 QtWidgets.QLabel('top thickness, tt:   '),
								 	 QtWidgets.QLabel('middle thickness, mt:'),
								 	 QtWidgets.QLabel('bottom width, bw:    '),
								 	 QtWidgets.QLabel('bottom thickness, bt:'),
								 	 QtWidgets.QLabel('height, h:           ')],
					   'L-Beam':	[QtWidgets.QLabel('side thickness, st:  '),
								 	 QtWidgets.QLabel('bottom width, bw:    '),
								 	 QtWidgets.QLabel('bottom thickness, bt:'),
								 	 QtWidgets.QLabel('height, h:           '),
								 	 QtWidgets.QLabel('      ---            '),
								 	 QtWidgets.QLabel('      ---            ')],
					   'T-Beam':	[QtWidgets.QLabel('middle thickness, mt:'),
								 	 QtWidgets.QLabel('top width, tw:       '),
								 	 QtWidgets.QLabel('top thickness, tt:   '),
								 	 QtWidgets.QLabel('height, h:           '),
								 	 QtWidgets.QLabel('      ---            '),
								 	 QtWidgets.QLabel('      ---            ')],
					   'C-Beam':	[QtWidgets.QLabel('top width, tw:       '),
								 	 QtWidgets.QLabel('top thickness, tt:   '),
								 	 QtWidgets.QLabel('middle thickness, mt:'),
								 	 QtWidgets.QLabel('bottom width, bw:    '),
								 	 QtWidgets.QLabel('bottom thickness, bt:'),
								 	 QtWidgets.QLabel('height, h:           ')],
					   'Properties':[QtWidgets.QLabel('Area:'), QtWidgets.QLabel('1.'),
								 	 QtWidgets.QLabel('Izz:'),  QtWidgets.QLabel('1.'),
								 	 QtWidgets.QLabel('Iyy:'),  QtWidgets.QLabel('1.')],
					   'Pixmap': 	 QtWidgets.QLabel('section_pixmap')}
		self.labels['Pixmap'].setPixmap(self.section_types[self.section_type])

		for label in range(3):
			self.labels['Properties'][2*label+1].setFont(self.boldFont)
		for label in self.labels:
			if label not in ['Properties','Pixmap','Select']:
				for i in range(len(self.labels[label])):
					self.labels[label][i].setFixedWidth(120)
			if label == 'Select':
				for i in range(len(self.labels[label])):
					self.labels[label][i].setFixedWidth(80)
		
		# Initialize the input textboxes
		self.line_edits = {'Rectangle': [QtWidgets.QLineEdit(),
										 QtWidgets.QLineEdit(),
										 QtWidgets.QLineEdit(),
										 QtWidgets.QLineEdit(),
										 QtWidgets.QLineEdit(),
										 QtWidgets.QLineEdit()],
					   	   'Circle':	[QtWidgets.QLineEdit(),
										 QtWidgets.QLineEdit(),
										 QtWidgets.QLineEdit(),
										 QtWidgets.QLineEdit(),
										 QtWidgets.QLineEdit(),
										 QtWidgets.QLineEdit()],
					   	   'I-Beam':	[QtWidgets.QLineEdit(),
										 QtWidgets.QLineEdit(),
										 QtWidgets.QLineEdit(),
										 QtWidgets.QLineEdit(),
										 QtWidgets.QLineEdit(),
										 QtWidgets.QLineEdit()],
					   	   'L-Beam':	[QtWidgets.QLineEdit(),
										 QtWidgets.QLineEdit(),
										 QtWidgets.QLineEdit(),
										 QtWidgets.QLineEdit(),
										 QtWidgets.QLineEdit(),
										 QtWidgets.QLineEdit()],
					   	   'T-Beam':	[QtWidgets.QLineEdit(),
										 QtWidgets.QLineEdit(),
										 QtWidgets.QLineEdit(),
										 QtWidgets.QLineEdit(),
										 QtWidgets.QLineEdit(),
										 QtWidgets.QLineEdit()],
					   	   'C-Beam':	[QtWidgets.QLineEdit(),
										 QtWidgets.QLineEdit(),
										 QtWidgets.QLineEdit(),
										 QtWidgets.QLineEdit(),
										 QtWidgets.QLineEdit(),
										 QtWidgets.QLineEdit()]}
		for sect in self.line_edits:
			for line in range(len(self.line_edits[sect])):
				if sect in ['I-Beam', 'C-Beam']:
					self.line_edits[sect][line].setMaxLength(20)
					self.line_edits[sect][line].setPlaceholderText('1.')
				elif sect in ['T-Beam', 'L-Beam', 'Rectangle']:
					if line <= 3:
						self.line_edits[sect][line].setMaxLength(20)
						self.line_edits[sect][line].setPlaceholderText('1.')
					else:
						self.line_edits[sect][line].setMaxLength(20)
						self.line_edits[sect][line].setPlaceholderText(' --- ')
						self.line_edits[sect][line].setEnabled(False)
				else:
					if line <= 1:
						self.line_edits[sect][line].setMaxLength(20)
						self.line_edits[sect][line].setPlaceholderText('1.')
					else:
						self.line_edits[sect][line].setMaxLength(20)
						self.line_edits[sect][line].setPlaceholderText(' --- ')
						self.line_edits[sect][line].setEnabled(False)

		for sect in self.line_edits:
			for line in range(len(self.line_edits[sect])):
				self.line_edits[sect][line].textChanged[str].connect(self.lineEditChanged)

		# Initialize the pushbuttons
		button_ok = QtWidgets.QPushButton('OK', self)
		button_ok.clicked.connect(self.returnInput)
		button_ok.clicked.connect(self.close)

		button_cancel = QtWidgets.QPushButton('Cancel', self)
		button_cancel.clicked.connect(self.close)

		# Put all the labels, selection boxes, textboxes
		# and buttons into the layout of the dialog box
		layoutM = QtWidgets.QHBoxLayout()	# Main layout
		layout0 = QtWidgets.QHBoxLayout()	# Pixmap 
		layout1 = QtWidgets.QVBoxLayout()	# Main sublayout
		layout2 = QtWidgets.QVBoxLayout()	# Selection boxes
		layout21 = QtWidgets.QHBoxLayout()	# Label1 and selection box1 
		layout22 = QtWidgets.QHBoxLayout()	# Label2 and selection box2 
		self.layoutS = QtWidgets.QStackedLayout()			# To swap between the different section types
		self.stacked_widgets = {'Rectangle': QtWidgets.QWidget(),
								'Circle':	 QtWidgets.QWidget(),
								'I-Beam':	 QtWidgets.QWidget(),
								'T-Beam':	 QtWidgets.QWidget(),
								'L-Beam':	 QtWidgets.QWidget(),
								'C-Beam':	 QtWidgets.QWidget()}
		layout3 = {'Rectangle': QtWidgets.QVBoxLayout(),	# Input labels and line edits
				   'Circle':	QtWidgets.QVBoxLayout(),
				   'I-Beam':	QtWidgets.QVBoxLayout(),
				   'L-Beam':	QtWidgets.QVBoxLayout(),
				   'C-Beam':	QtWidgets.QVBoxLayout(),
				   'T-Beam':	QtWidgets.QVBoxLayout()}
		layout31 = {'Rectangle':QtWidgets.QVBoxLayout(),	# 1st input
					'Circle':	QtWidgets.QVBoxLayout(),
					'I-Beam':	QtWidgets.QVBoxLayout(),
					'L-Beam':	QtWidgets.QVBoxLayout(),
					'C-Beam':	QtWidgets.QVBoxLayout(),
					'T-Beam':	QtWidgets.QVBoxLayout()}
		layout32 = {'Rectangle':QtWidgets.QVBoxLayout(),	# 2nd input
					'Circle':	QtWidgets.QVBoxLayout(),
					'I-Beam':	QtWidgets.QVBoxLayout(),
					'L-Beam':	QtWidgets.QVBoxLayout(),
					'C-Beam':	QtWidgets.QVBoxLayout(),
					'T-Beam':	QtWidgets.QVBoxLayout()}
		layout33 = {'Rectangle':QtWidgets.QVBoxLayout(),	# 3rd input
					'Circle':	QtWidgets.QVBoxLayout(),
					'I-Beam':	QtWidgets.QVBoxLayout(),
					'L-Beam':	QtWidgets.QVBoxLayout(),
					'C-Beam':	QtWidgets.QVBoxLayout(),
					'T-Beam':	QtWidgets.QVBoxLayout()}
		layout34 = {'Rectangle':QtWidgets.QVBoxLayout(),	# 4th input
					'Circle':	QtWidgets.QVBoxLayout(),
					'I-Beam':	QtWidgets.QVBoxLayout(),
					'L-Beam':	QtWidgets.QVBoxLayout(),
					'C-Beam':	QtWidgets.QVBoxLayout(),
					'T-Beam':	QtWidgets.QVBoxLayout()}
		layout35 = {'Rectangle':QtWidgets.QVBoxLayout(),	# 5th input
					'Circle':	QtWidgets.QVBoxLayout(),
					'I-Beam':	QtWidgets.QVBoxLayout(),
					'L-Beam':	QtWidgets.QVBoxLayout(),
					'C-Beam':	QtWidgets.QVBoxLayout(),
					'T-Beam':	QtWidgets.QVBoxLayout()}
		layout36 = {'Rectangle':QtWidgets.QVBoxLayout(),	# 6th input
					'Circle':	QtWidgets.QVBoxLayout(),
					'I-Beam':	QtWidgets.QVBoxLayout(),
					'L-Beam':	QtWidgets.QVBoxLayout(),
					'C-Beam':	QtWidgets.QVBoxLayout(),
					'T-Beam':	QtWidgets.QVBoxLayout()}
		layout4 = QtWidgets.QVBoxLayout()	# Output labels and buttons
		layout41 = QtWidgets.QHBoxLayout()	# 1st output
		layout42 = QtWidgets.QHBoxLayout()	# 2nd output
		layout43 = QtWidgets.QHBoxLayout()	# 3rd output
		layout44 = QtWidgets.QHBoxLayout()	# Buttons
		

		layoutM.setContentsMargins(20,20,20,20)
		layoutM.setSpacing(20)

		layout0.addWidget(self.labels['Pixmap'])

		layout21.addWidget(self.labels['Select'][0])
		layout21.addWidget(self.selection_box_sections)
		layout22.addWidget(self.labels['Select'][1])
		layout22.addWidget(self.selection_box_types)
		layout2.addLayout(layout21)
		layout2.addLayout(layout22)

		for sect_type in self.section_types:
			layout31[sect_type].addWidget(self.labels[sect_type][0])
			layout31[sect_type].addWidget(self.line_edits[sect_type][0])
			layout32[sect_type].addWidget(self.labels[sect_type][1])
			layout32[sect_type].addWidget(self.line_edits[sect_type][1])
			layout33[sect_type].addWidget(self.labels[sect_type][2])
			layout33[sect_type].addWidget(self.line_edits[sect_type][2])
			layout34[sect_type].addWidget(self.labels[sect_type][3])
			layout34[sect_type].addWidget(self.line_edits[sect_type][3])
			layout35[sect_type].addWidget(self.labels[sect_type][4])
			layout35[sect_type].addWidget(self.line_edits[sect_type][4])
			layout36[sect_type].addWidget(self.labels[sect_type][5])
			layout36[sect_type].addWidget(self.line_edits[sect_type][5])
			layout3[sect_type].addLayout(layout31[sect_type])
			layout3[sect_type].addLayout(layout32[sect_type])
			layout3[sect_type].addLayout(layout33[sect_type])
			layout3[sect_type].addLayout(layout34[sect_type])
			layout3[sect_type].addLayout(layout35[sect_type])
			layout3[sect_type].addLayout(layout36[sect_type])
		self.stacked_index = []
		for sect_type in self.section_types:
			self.stacked_widgets[sect_type].setLayout(layout3[sect_type])
			self.layoutS.addWidget(self.stacked_widgets[sect_type])
			self.stacked_index.append(sect_type)

		layout41.addWidget(self.labels['Properties'][0])
		layout41.addWidget(self.labels['Properties'][1])
		layout42.addWidget(self.labels['Properties'][2])
		layout42.addWidget(self.labels['Properties'][3])
		layout43.addWidget(self.labels['Properties'][4])
		layout43.addWidget(self.labels['Properties'][5])
		layout44.addWidget(button_cancel)
		layout44.addWidget(button_ok)
		layout4.addLayout(layout41)
		layout4.addLayout(layout42)
		layout4.addLayout(layout43)
		layout4.addLayout(layout44)
        
		layout1.addLayout(layout2)
		layout1.addLayout(self.layoutS)
		layout1.addLayout(layout4)
		
		layoutM.addLayout(layout1)
		layoutM.addLayout(layout0)

		self.setLayout(layoutM)
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
		self.labels['Pixmap'].setPixmap(self.section_types[str(index)])
		self.section_type = str(index)
		self.layoutS.setCurrentIndex(self.stacked_index.index(self.section_type))
		self.updateProperties()

		
	def lineEditChanged(self, text):
		'''
	Calls updateProperties() function every
	time new input is entered into the form.
	'''
		self.updateProperties()


	def updateProperties(self):
		'''
	Update the properties (Area, Izz and Iyy)
	to show the correct values based on new input.
	'''
		if self.section_type == 'Rectangle':
			# parameters: iw, ih, w, h
			try:
				if str(self.line_edits['Rectangle'][0].text()) == '':
					iw = float(self.line_edits['Rectangle'][0].placeholderText())
				else:
					iw = float(self.line_edits['Rectangle'][0].text())
				if str(self.line_edits['Rectangle'][1].text()) == '':
					ih = float(self.line_edits['Rectangle'][1].placeholderText())
				else:
					ih = float(self.line_edits['Rectangle'][1].text())
				if str(self.line_edits['Rectangle'][2].text()) == '':
					w = float(self.line_edits['Rectangle'][2].placeholderText())
				else:
					w = float(self.line_edits['Rectangle'][2].text())
				if str(self.line_edits['Rectangle'][3].text()) == '':
					h = float(self.line_edits['Rectangle'][3].placeholderText())
				else:
					h = float(self.line_edits['Rectangle'][3].text())
			except ValueError:
				print('\n\tParameters must be float or int')
				self.labels['Properties'][1].setText(' N/A ')
				self.labels['Properties'][3].setText(' N/A ')
				self.labels['Properties'][5].setText(' N/A ')
			else:
				# Area
				self.labels['Properties'][1].setText(str( w*h-iw*ih ))
				# Izz
				self.labels['Properties'][3].setText(str( (w*(h**3)-iw*(ih**3))/12. ))
				# Iyy
				self.labels['Properties'][5].setText(str( ((w**3)*h-(iw**3)*ih)/12. ))

		elif self.section_type == 'Circle':
			# parameters: ir, r
			try:
				if str(self.line_edits['Circle'][0].text()) == '':
					ir = float(self.line_edits['Circle'][0].placeholderText())
				else:
					ir = float(self.line_edits['Circle'][0].text())
				if str(self.line_edits['Circle'][1].text()) == '':
					r = float(self.line_edits['Circle'][1].placeholderText())
				else:
					r = float(self.line_edits['Circle'][1].text())
			except ValueError:
				print('\n\tParameters must be float or int')
				self.labels['Properties'][1].setText(' N/A ')
				self.labels['Properties'][3].setText(' N/A ')
				self.labels['Properties'][5].setText(' N/A ')
			else:
				# Area
				self.labels['Properties'][1].setText(str( pi*r**2 - pi*ir**2 ))
				# Izz
				self.labels['Properties'][3].setText(str( ((r**4)-(ir**4))*(pi/4.) ))
				# Iyy
				self.labels['Properties'][5].setText(str( ((r**4)-(ir**4))*(pi/4.) ))

		elif self.section_type == 'I-Beam':
			# parameters: tw, tt, mt, bw, bt, h
			try:
				if str(self.line_edits['I-Beam'][0].text()) == '':
					tw = float(self.line_edits['I-Beam'][0].placeholderText())
				else:
					tw = float(self.line_edits['I-Beam'][0].text())
				if str(self.line_edits['I-Beam'][1].text()) == '':
					tt = float(self.line_edits['I-Beam'][1].placeholderText())
				else:
					tt = float(self.line_edits['I-Beam'][1].text())
				if str(self.line_edits['I-Beam'][2].text()) == '':
					mt = float(self.line_edits['I-Beam'][2].placeholderText())
				else:
					mt = float(self.line_edits['I-Beam'][2].text())
				if str(self.line_edits['I-Beam'][3].text()) == '':
					bw = float(self.line_edits['I-Beam'][3].placeholderText())
				else:
					bw = float(self.line_edits['I-Beam'][3].text())
				if str(self.line_edits['I-Beam'][4].text()) == '':
					bt = float(self.line_edits['I-Beam'][4].placeholderText())
				else:
					bt = float(self.line_edits['I-Beam'][4].text())
				if str(self.line_edits['I-Beam'][5].text()) == '':
					h = float(self.line_edits['I-Beam'][5].placeholderText())
				else:
					h = float(self.line_edits['I-Beam'][5].text())
			except ValueError:
				print('\n\tParameters must be float or int')
				self.labels['Properties'][1].setText(' N/A ')
				self.labels['Properties'][3].setText(' N/A ')
				self.labels['Properties'][5].setText(' N/A ')
			else:
				A1  = tt*tw
				A2  = mt*(h-tt-bt)
				A3  = bt*bw
				A   = A1+A2+A3
				yC1 = h-(tt/2.)
				yC2 = (h-tt)/2.
				yC3 = bt/2.
				if A != 0.:
					yC = (A1*yC1+A2*yC2+A3*yC3)/A
				else:
					yC = 0.
				d1  = yC1-yC
				d2  = yC2-yC
				d3  = yC-yC3
				Iz1 = (tw*(tt**3))/12
				Iz2 = (mt*((h-tt-bt)**3))/12
				Iz3 = (bw*(bt**3))/12
				Iy1 = (tt*(tw**3))/12
				Iy2 = ((h-tt-bt)*(mt**3))/12
				Iy3 = (bt*(bw**3))/12
				# Area
				self.labels['Properties'][1].setText(str( A ))
				# Izz
				self.labels['Properties'][3].setText(str( (Iz1 + A1*(d1**2)) + (Iz2 + A2*(d2**2)) + (Iz3 + A3*(d3**2)) ))
				# Iyy
				self.labels['Properties'][5].setText(str( Iy1 + Iy2 + Iy3 ))

		elif self.section_type == 'C-Beam':
			# parameters: tw, tt, mt, bw, bt, h
			try:
				if str(self.line_edits['C-Beam'][0].text()) == '':
					tw = float(self.line_edits['C-Beam'][0].placeholderText())
				else:
					tw = float(self.line_edits['C-Beam'][0].text())
				if str(self.line_edits['C-Beam'][1].text()) == '':
					tt = float(self.line_edits['C-Beam'][1].placeholderText())
				else:
					tt = float(self.line_edits['C-Beam'][1].text())
				if str(self.line_edits['C-Beam'][2].text()) == '':
					mt = float(self.line_edits['C-Beam'][2].placeholderText())
				else:
					mt = float(self.line_edits['C-Beam'][2].text())
				if str(self.line_edits['C-Beam'][3].text()) == '':
					bw = float(self.line_edits['C-Beam'][3].placeholderText())
				else:
					bw = float(self.line_edits['C-Beam'][3].text())
				if str(self.line_edits['C-Beam'][4].text()) == '':
					bt = float(self.line_edits['C-Beam'][4].placeholderText())
				else:
					bt = float(self.line_edits['C-Beam'][4].text())
				if str(self.line_edits['C-Beam'][5].text()) == '':
					h = float(self.line_edits['C-Beam'][5].placeholderText())
				else:
					h = float(self.line_edits['C-Beam'][5].text())
			except ValueError:
				print('\n\tParameters must be float or int')
				self.labels['Properties'][1].setText(' N/A ')
				self.labels['Properties'][3].setText(' N/A ')
				self.labels['Properties'][5].setText(' N/A ')
			else:
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
				dz1  = yC1-yC
				dz2  = yC2-yC
				dz3  = yC-yC3
				dy1  = zC1-zC
				dy2  = zC-zC2
				dy3  = zC3-zC
				Iz1 = (tw*(tt**3))/12
				Iz2 = (mt*((h-tt-bt)**3))/12
				Iz3 = (bw*(bt**3))/12
				Iy1 = (tt*(tw**3))/12
				Iy2 = ((h-tt-bt)*(mt**3))/12
				Iy3 = (bt*(bw**3))/12
				# Area
				self.labels['Properties'][1].setText(str( A ))
				# Izz
				self.labels['Properties'][3].setText(str( (Iz1 + A1*(dz1**2)) + (Iz2 + A2*(dz2**2)) + (Iz3 + A3*(dz3**2)) ))
				# Iyy
				self.labels['Properties'][5].setText(str( (Iy1 + A1*(dy1**2)) + (Iy2 + A2*(dy2**2)) + (Iy3 + A3*(dy3**2)) ))

		elif self.section_type == 'L-Beam':
			# parameters: st, bw, bt, h
			try:
				if str(self.line_edits['L-Beam'][0].text()) == '':
					st = float(self.line_edits['L-Beam'][0].placeholderText())
				else:
					st = float(self.line_edits['L-Beam'][0].text())
				if str(self.line_edits['L-Beam'][1].text()) == '':
					bw = float(self.line_edits['L-Beam'][1].placeholderText())
				else:
					bw = float(self.line_edits['L-Beam'][1].text())
				if str(self.line_edits['L-Beam'][2].text()) == '':
					bt = float(self.line_edits['L-Beam'][2].placeholderText())
				else:
					bt = float(self.line_edits['L-Beam'][2].text())
				if str(self.line_edits['L-Beam'][3].text()) == '':
					h = float(self.line_edits['L-Beam'][3].placeholderText())
				else:
					h = float(self.line_edits['L-Beam'][3].text())
			except ValueError:
				print('\n\tParameters must be float or int')
				self.labels['Properties'][1].setText(' N/A ')
				self.labels['Properties'][3].setText(' N/A ')
				self.labels['Properties'][5].setText(' N/A ')
			else:
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
				dz1 = yC1-yC
				dz2 = yC-yC2
				dy1 = zC-zC1
				dy2 = zC2-zC
				Iz1 = (st*((h-bt)**3))/12
				Iz2 = (bw*(bt**3))/12
				Iy1 = ((h-bt)*(st**3))/12
				Iy2 = (bt*(bw**3))/12
				# Area
				self.labels['Properties'][1].setText(str( A ))
				# Izz
				self.labels['Properties'][3].setText(str( (Iz1 + A1*(dz1**2)) + (Iz2 + A2*(dz2**2)) ))
				# Iyy
				self.labels['Properties'][5].setText(str( (Iy1 + A1*(dy1**2)) + (Iy2 + A2*(dy2**2)) ))

		elif self.section_type == 'T-Beam':
			# parameters: mt, tw, tt, h
			try:
				if str(self.line_edits['T-Beam'][0].text()) == '':
					mt = float(self.line_edits['T-Beam'][0].placeholderText())
				else:
					mt = float(self.line_edits['T-Beam'][0].text())
				if str(self.line_edits['T-Beam'][1].text()) == '':
					tw = float(self.line_edits['T-Beam'][1].placeholderText())
				else:
					tw = float(self.line_edits['T-Beam'][1].text())
				if str(self.line_edits['T-Beam'][2].text()) == '':
					tt = float(self.line_edits['T-Beam'][2].placeholderText())
				else:
					tt = float(self.line_edits['T-Beam'][2].text())
				if str(self.line_edits['T-Beam'][3].text()) == '':
					h = float(self.line_edits['T-Beam'][3].placeholderText())
				else:
					h = float(self.line_edits['T-Beam'][3].text())
			except ValueError:
				print('\n\tParameters must be float or int')
				self.labels['Properties'][1].setText(' N/A ')
				self.labels['Properties'][3].setText(' N/A ')
				self.labels['Properties'][5].setText(' N/A ')
			else:
				A1  = mt*(h-tt)
				A2  = tt*tw
				A   = A1+A2
				yC1 = h-(tt/2.)
				yC2 = (h-tt)/2.
				if A != 0.:
					yC = (A1*yC1+A2*yC2)/A
				else:
					yC = 0.
				d1  = yC1-yC
				d2  = yC-yC2
				Iz1 = (tw*(tt**3))/12
				Iz2 = (mt*((h-tt)**3))/12
				Iy1 = (tt*(tw**3))/12
				Iy2 = ((h-tt)*(mt**3))/12
				# Area
				self.labels['Properties'][1].setText(str( A ))
				# Izz
				self.labels['Properties'][3].setText(str( (Iz1 + A1*(d1**2)) + (Iz2 + A2*(d2**2)) ))
				# Iyy
				self.labels['Properties'][5].setText(str( Iy1 + Iy2 ))

		else:
			pass

		
	def returnInput(self):
		'''
	Set the values of self.modify_section
	to be returned.
	'''
		section = str(self.selection_box_sections.currentText())
		self.modified_section[section]['Area (Rod or Beam)'] = float(self.labels['Properties'][1].text())
		self.modified_section[section]['Izz (Beam)'] = float(self.labels['Properties'][3].text())
		self.modified_section[section]['Iyy (Beam 3D)'] = float(self.labels['Properties'][5].text())
		self.modified_section[section]['Cross section'] = {'Type': self.section_type}
		for m in range(6):
			if str(self.labels[self.section_type][m].text()).strip() != '---':
				if str(self.line_edits[self.section_type][m].text()) == '':
					self.modified_section[section]['Cross section'][str(self.labels[self.section_type][m].text()).strip().replace(':','')] = \
																				float(self.line_edits[self.section_type][m].placeholderText())
				else:
					self.modified_section[section]['Cross section'][str(self.labels[self.section_type][m].text()).strip().replace(':','')] = \
																				float(self.line_edits[self.section_type][m].text())
		print('\n\tSection modified ('+section+'):')
		print('\t', self.modified_section[section])






