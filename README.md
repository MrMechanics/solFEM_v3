# solFEM_v3
A small open source Finite Element program with basic mesh generation, solver and viewer.

![alt text](https://github.com/MrMechanics/solFEM_v3/blob/main/Splash/elements.png?raw=true)

Description:
------------

This program is meant as a barebones FEM program for quick and dirty calculations.
Kind of like how you have a calculator easily accessible on your desktop, there
should be a free open source FEM program which you can start up on your computer
and quickly find the stiffness of a simple structure.

The code is written in python primarily to be easy to read, so it also is meant to
be a resource for students or engineers who wish to dig into FEM code and build more 
intuition for how the finite element method works. Maybe even use parts of this 
code as inspiration for their own FEM code.

PS! This program should be used on relatively small FEM solutions (100 000 DOFs 
takes more than 2 minutes to solve on a fast computer with lots of RAM, while 
20 000 DOFs can take several minutes on a 10 year old laptop), because it uses 
scipy.sparse.linalg, which only solves matrix equations using one CPU. No parallel 
computing. It can run larger models also (unless you run out of RAM), but that
will take a long time.

Also it is recommended to save your work regularly while you build your solutions.
This creates .mdl files which can be loaded from your last save if the program
should crash. There is no undo-button. If you want to save your mesh in a more 
robust format, you can export it directly into a .sol file (text format).

Have fun!

![alt text](https://github.com/MrMechanics/solFEM_v3/blob/main/Splash/program.png?raw=true)

Requirements:
-------------

Python3 with the following modules must be installed for the program to work:
- numpy
- scipy
- matplotlib
- pyopengl
- pyqt5
- pyqt5.qtopengl

With the above mentioned python modules installed, copy the solFEM_v3 folder to any location, 
open a terminal window and navigate to '..\solFEM_v3\work_directory'. The program can then be
started from the terminal by running the script 'program.py'.

In windows 10:
..\solFEM_v3\work_directory> py program.py

In Ubuntu:
..\solFEM_v3\work_directory> python3 program.py



Tutorials:
----------

- Written documentation accessed from inside the program -- READY!
- Youtube video tutorial -- COMING SOON!
- Case files that can be used to see working examples (..\solFEM_v3\Example Mesh Files) -- READY!



Future Work:
------------

- Modal Dynamics solver with base motion is too slow, should not be used on large models
- Modal Effective Mass not calculated correctly
- Non-linear Static Plastic solver


