"""An example script for frontend to get an idea of how it works."""

#! When we have the JSON file format ready I will make everything automatic when backend.render() is called but this is the workaround for now
import os
if (__name__ == "__main__"):
    path = os.path.abspath(os.getcwd()) + "\\backend"
    file_contents = ""
    # modify this file to append location of backend file for blender's environment
    with open(path + "\\example.py", "r") as this_file:
        file_contents = this_file.read()

    file_contents = file_contents[917:]

    with open(path + "\\_temp.py", "w") as to_run:
        path = path.replace("\\", "\\\\")
        to_run.write(f"""import blenderproc as bproc
from sys import path
path.append("{path}")       
""" + file_contents)

    os.system("blenderproc run backend/_temp.py")
    os.system("blenderproc vis hdf5 output/0.hdf5")
    os.remove("backend/_temp.py")
    exit()

#! Ignore the stuff that's above, it's just the workaround for now. Run like it's a normal python file
from backend import Backend
import numpy as np

# Initialise backend
backend = Backend()

# Initialise a render object in the backend
monkey1 = backend.RenderObject(primative = "MONKEY")
monkey1.set_loc([-2, 0, 0])

monkey2 = backend.RenderObject(primative = "MONKEY")
monkey2.set_loc([2, 0, 0])

# Initialise a light object and set its location, energy and colour
light = backend.RenderLight()
light.set_loc([5, -10, 0])
light.set_energy(5)
light.set_color([255, 0, 0])

# Set the camera position and change output resolution to 1080p
backend.set_cam_pose([[0, -10, 0], [np.pi / 2, 0, 0]])
backend.set_res([1920, 1080])

# Start the render
backend.render()
