# Will need to change these things to get values from frontend UI
# run with blenderproc run backend/test.py
# visualise with blenderproc vis hdf5 output/0.hdf5
import blenderproc as bproc
import numpy as np

bproc.init()

def get_uniform_pose(r, n):
    pose = []

    degs = 360 / n

    for i in range(n):
        xp = r * np.sin(    np.deg2rad(i * degs) )
        zp = -1 * r * np.cos(    np.deg2rad(i * degs) )

        angle = np.deg2rad ( i * degs )

        pose.append( [[xp, zp, 0],[np.pi / 2 , 0, angle]] )

    return pose


poses = get_uniform_pose(10, 8)


# You can import multiple objects:
obj = bproc.object.create_primitive("MONKEY")
obj.set_location([-2, 0, 0])

obj2 = bproc.object.create_primitive("MONKEY")
obj2.set_location([2, 0, 0])

# Create a point light next to it
light = bproc.types.Light()
light.set_location([6, -9, 0])
light.set_energy(300)
# light.set_color((255, 0, 0))

# Set the camera to be in front of the object (vectors in [x, z, y])
#cam_pose = bproc.math.build_transformation_mat([0, -10, 0], [np.pi / 2, 0, 0])
#bproc.camera.add_camera_pose(cam_pose)
# change res of render
# bproc.camera.set_resolution(1920, 1080)

for i in poses:
    cam_pose = bproc.math.build_transformation_mat(i[0], i[1])
    bproc.camera.add_camera_pose(cam_pose)
    print(i)



# Render the scene
data = bproc.renderer.render()

# Write the rendering into an hdf5 file
bproc.writer.write_hdf5("output/", data)
