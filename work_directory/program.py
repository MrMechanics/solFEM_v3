#
#
#	program.py
#  --------------
#
#	Start the module specified by the user
#	Either solFEM or viewFEM
#


import sys
sys.path.insert(1, '../Objects')
sys.path.insert(1, '../Modules')

from solFEM import *
from viewFEM import *




if __name__ == '__main__':


	modSelected = False

	print( '\n\n' )
	while modSelected == False:

		print( '\tWhat module do you wish to use?' )
		print( '\t-----------------------------\n' )
		print( '\tsolFEM  - FE-solver			[s]' )
		print( '\tviewFEM - FE-viewer			[v]' )
		modSelect = input('\n\ts/v: ')


		if modSelect in ['s', 'S']:
			print( '\n\n\t\tsolFEM_v3' )
			print( '\tFinite Element Solver' )
			print( '\t--------------------------\n' )
			print( '\tThis finite element solver takes input solver files (.sol)' )
			print( '\tand generates displacement, stress, strain and more results' )
			print( '\tas requested in the files.' )

			fname = input('\n\n\tsolver-file: ')
			inputobj = InputData(fname)
			if inputobj.input_error == False:
				model = FEModel(inputobj)
			else:
				print( '\n\tSolver aborted because of input error(s).' )
			modSelected = True


		elif modSelect in ['v', 'V']:
			print( '\n\n\t\tviewFEM_v3' )
			print( '\tFinite Element Viewer' )
			print( '\t--------------------------\n' )
			print( '\tThis interactive 3D viewer can be used to set up finite elment' )
			print( '\tmodels for the solFEM_v3 solver. Meshes can be imported or created' ) 
			print( '\tdirectly and solutions with boundary conditions, constraints and' ) 
			print( '\tloads defined and exported to *.sol files.' ) 
			print( '\n\tThe viewer also loads results from the *.out files that are' )
			print( '\tgenerated by solFEM_v3. It can show contour plots of displacements,' )
			print( '\tstresses, strains, element forces and also node forces for static' )
			print( '\tsolutions. Animated eigenmodes are supported for the eigenmode' )
			print( '\tsolutions, and for modal dynamic solutions; acceleration,' )
			print( '\tvelocity and displacement graphs made with matplotlibs pyplot.' )
			print( '\n\t\tViewer controls:' )
			print( '\trotate view     --> CTRL + ALT + left mouse button' )
			print( '\tzoom            --> right mouse button' )
			print( '\tpan view        --> mouse wheel click' )
			print( '\tdrag select     --> left mouse button' )
			print( '\tdrag add select --> left mouse button + SHIFT' )
			print( '\tdrag unselect   --> left mouse button + CTRL\n' )

			app = QtWidgets.QApplication(['viewFEM - Finite Element Viewer'])

			pix = QtGui.QPixmap('../Splash/elements.png')
			lbl = QtWidgets.QLabel('<font color=Black size=12><b> solFEM v.2 </b></font>')
			lbl.setPixmap(pix.scaledToWidth(800))
			lbl.setWindowFlags(QtCore.Qt.SplashScreen | QtCore.Qt.FramelessWindowHint | 
								QtCore.Qt.WindowStaysOnTopHint)
			lbl.show()
			QtCore.QTimer.singleShot(2000,lbl.close)

			window = UserInterface()
			window.show()
			app.exec_()
			modSelected = True


		else:
			print( '\n\tyou must choose s or v. Try again...' )


	print( '\n\n\tProgram closing...\n\n' )


