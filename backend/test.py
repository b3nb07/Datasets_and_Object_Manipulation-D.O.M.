# Will need to change these things to get values from frontend UI
# run with blenderproc run backend/test.py
# visualise with blenderproc vis hdf5 output/0.hdf5
import blenderproc as bproc
import numpy as np

bproc.init()

def get_uniform_across_a_set_y(r, n, xAngle, yPose=0):
    """ xRotate will be the one to look down / up
    make a new func to get values for this and then call this
    
    """
    pose = []

    degs = 360 / n

    for i in range(n):
        xPose = r * np.sin(    np.deg2rad(i * degs) )
        zPose = -1 * r * np.cos(    np.deg2rad(i * degs) )

    yAngle = np.deg2rad ( i * degs )

    pose.append( [[xPose, zPose, yPose],[xAngle, 0, yAngle]] )

    return pose

def get_x_for_higher_angles(r, xAngle):
    d = np.sin(xAngle) * r
    return d

def get_y_for_higher_angles(r, xAngle):
    a = np.cos(xAngle)
    return a


def get_uniform_pose(r,n):
    xAngleStep = 180 / n
    poses = []
    for i in range(n):
        xAngle = xAngleStep * i

        distanceFromCenterX = get_x_for_higher_angles(r, xAngle)
        distanceFromCenterY = get_y_for_higher_angles(r, xAngle)

        poses = poses, get_uniform_across_a_set_y(distanceFromCenterX, n, xAngle, distanceFromCenterY)
    
    poses = poses[1::]
    return poses
        


poses = get_uniform_pose(10, 8)
print(len(poses))


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
