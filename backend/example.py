"""An example script for frontend to get an idea of how it works."""
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
backend.add_cam_pose([[0, -10, 0], [np.pi / 2, 0, 0]])
backend.add_cam_pose([[0, -20, 0], [np.pi / 2, 0, 0]])
backend.set_res([1920, 1080])

# Start the render
backend.render()
