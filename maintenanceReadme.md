Database and object manipulation

### Goals and scope

### Overview:
The project is to develop a program that can upload 3D object/s int a space allowing a specified
pivot point. Then rotating around the pivot point if the object at the angle at regular intervals.
Thus creating a dataset for “Predictive change”.

### Scope:
● Software must be portable across all systems (dockerised)
● 3D environment to place 3D objects
● Must have tutorial objects
● Must have base shapes (Cube, Sphere, Triangle)
● Must allow n amount of objects (where n ∈ N+)
● Must allow random object spawns and orientations
○ All randomness must be seeded
● Must allow custom pivot points for camera rotation
● Allow 3D object transformation:
○ To the X, Y, Z axis coordinates
○ To the Length, Breadth, Height transformations
○ To allow reflection
○ To rotation
● Allow camera to be manually rotated
○ Allow automated custom rotations to create exportable datasets (degree of
rotation between images)
● Import/export modifications to a json file
○ Must be able to read all majour 3D file types
○ Must integrate with blender
● Must have a simplified menu and advanced options
○ Allow custom environments / void

### Boundaries:
● All files will be localised
● No security concerns as everything is local
● Desktop program - No website / App / Web Interface
● Must be portable across all systems (MacOS, Windows)
● Tutorials will cover basic functions / User Manual
● Readme file includes instructions on how to use software

### Installation

### Requirments
To run this software the prerequisite installs are:
    Python - https://www.python.org/
    pyqt5 - https://pypi.org/project/PyQt5/
    blenderproc - https://github.com/DLR-RM/BlenderProc
    numpy - https://numpy.org/install/

Commands: 

pip install pyqt5
pip install blenderproc
pip install numpy
