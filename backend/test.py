# Will need to change these things to get values from frontend UI
# run with blenderproc run backend/test.py
# visualise with blenderproc vis hdf5 output/0.hdf5

import blenderproc as bproc
import numpy as np

bproc.init()

# Create a simple object:
obj = bproc.object.create_primitive("MONKEY")

# Create a point light next to it
light = bproc.types.Light()
light.set_location([6, -9, 0])
light.set_energy(500)

# Set the camera to be in front of the object
cam_pose = bproc.math.build_transformation_mat([0, -5, 0], [np.pi / 2, 0, 0])
bproc.camera.add_camera_pose(cam_pose)

# Render the scene
data = bproc.renderer.render()

# Write the rendering into an hdf5 file
bproc.writer.write_hdf5("output/", data)
