# solFEM_v3
A small open source Finite Element program with basic mesh generation, solver and viewer.

![alt text](https://github.com/MrMechanics/solFEM_v3/blob/main/Splash/elements.png?raw=true)

Description:
------------

This program is meant as a barebones FEM program for quick and dirty calculations.
Kind of like how you have a calculator easily accessible on your desktop, there
should be a free open source FEM program which you can start up on your computer
and quickly find the stiffness of a simple structure.

It is also meant as a resource for students or engineers who wish to dig into FEM 
code and build more intuition for how the finite element method works. Maybe even 
use parts of this code as a base for their own FEM code.

PS! This program is primarily meant to be used on relatively small FEM solutions
(100 000 DOFs takes more than 2 minutes to solve), because it uses
scipy.sparse.linalg solvers, which only solves matrix equations using one CPU.
No parallel computing.

Also it is generally not recommended to build big models with many parts, as the
program can sometimes crash abruptly which might lose you all your work and cause 
some frustration. It is possible to save your work in .mdl files, but they are 
not a very robust format. Therefore if you need to save a solution for later, it 
is always safest to save your work in .sol files.

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


