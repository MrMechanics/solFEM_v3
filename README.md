# solFEM_v3
A small open source Finite Element program with very basic mesh generation, solver and viewer.



Installation:
-------------

Python3 with the following modules must be installed for the program to work:
- numpy
- scipy
- pyqt5
- pyopengl
- matplotlib

With the above mentioned python modules installed, copy the solFEM_v3 folder to any location, 
open a terminal window and navigate to ../solFEM_v3/work_directory. The program can then be
started from the terminal by running the script 'program.py'.

In windows 10:
..\solFEM_v3\work_directory> py program.py

In Ubuntu:
..\solFEM_v3\work_directory> python3 program.py



Tutorials:
----------

- Written documentation accessed from inside the program -- NEEDS MAJOR UPGRADE!
- Youtube video tutorials -- HOPEFULLY COMING SOON!
- Case files that can be used to see working examples (..\solFEM_v3\Example Mesh Files) -- MORE EXAMPLE MESHES COMING!




Disclaimer:
-----------

This program is meant as a barebones FEM program for quick and dirty calculations.
The code will have many bugs, and should only be used for educational purposes and
as a tool for engineers who wish to dig into FEM code build more intuition for how
the finite element method works.

PS! It is generally not recommended to build big models with many parts, as the
program can crash abruptly which might lose you all your work and cause a lot of
frustration. It is possible to save your work in *.mdl files, but they are not a
very robust format, so it is safest to save your work in *.sol files.


Have fun!
