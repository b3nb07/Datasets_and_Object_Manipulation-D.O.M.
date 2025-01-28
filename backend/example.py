"""An example script for frontend to get an idea of how it works."""
from backend import Backend
import numpy as np
from time import time

N_RENDERS = 100

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

# Start the benchmark
start_time = time()
for _ in range(N_RENDERS):
    backend.add_cam_pose([[0, -10, 0], [np.pi / 2, 0, 0]])

backend.render(headless = True)

print(f"Time taken for {N_RENDERS} renders was: {time() - start_time:.2f}s")