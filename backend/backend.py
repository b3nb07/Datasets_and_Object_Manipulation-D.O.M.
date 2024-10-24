"""The main backend file which deals with rendering."""

import blenderproc as bproc
import numpy as np

class Backend():
    """The main backend class which deals with setting up paramaters for the renderer."""
    def __init__(self, json=None):
        """Initialise the backend by setting up bproc.

        :param json: Filepath to a JSON configuration file.
        """
        bproc.init()
        #TODO: Create a format for the JSON

    def set_cam_pose(self, pose):
        """Sets the position of the camera in the scene for rendering.
        
        :param pose: a list containing position and rotation config details. Position in index 0 and rotation in index 1."""
        cam_pose = bproc.math.build_transformation_mat(pose[0], pose[1])
        bproc.camera.add_camera_pose(cam_pose)
        
    def set_res(self, resolution):
        """Set the resolution of the output images. Will effect total render time.

        :param resolution: A list [x, y] with the height and width of the resolution in pixels.
        """
        bproc.camera.set_resolution(resolution[0], resolution[1])

    def set_bg_color(self, color, strength=1):
        """Sets the world background color for rendering. Note: RBG values are between 0-1, diving by 255 gives the appropriate values. 
        
        :param color: a list containing RGB values for the color of the background.
        :param strength: strength of the background color, set to 1 by default."""

        bproc.renderer.set_world_background([color[0]/255, color[1]/255, color[2]/255], strength)


    def render(self):
        """Renders the scene and saves to file in the output folder."""

        data = bproc.renderer.render()

        bproc.writer.write_hdf5("output/", data)


    class RenderObject():
        """An object to be rendered."""

        def __init__(self, filepath=None, primative=None):
            """Initialise a render object.

            :param filepath: Filepath to an object file.
            :param primative: Create object primatively, choose from one of ["CUBE", "CYLINDER", "CONE", "PLANE", "SPHERE", "MONKEY"].
            """
            if (filepath is not None):
                self.object = bproc.loader.load_blend(filepath) if filepath.endswith(".blend") else bproc.loader.load_obj(filepath)
                return

            if (primative is not None):
                self.object = bproc.object.create_primitive(primative)
                return

            raise TypeError('No filepath or primative argument given.')

        def set_loc(self, location):
            """Set the location of an object in the scene.
            
            :param location: A list containing [x,z,y] where x,z,y is an integer or float. This determines the coordinates of the object's location.
            """
            self.object.set_location(location)

        def set_scale(self, scale):
            """Set the scale of an object in the scene.
            
            :param scale: A list containing [x,z,y] where x,z,y is an integer or float. This determines the scaling of each axis.
            """
            self.object.set_scale(scale)

        def set_rotation(self, euler_rotation):
            """Set the rotation of an object in the scene.
            
            :param euler_rotation: A list containing [x,z,y] values for the euler rotation to be applied to the object.
            """
            self.object.set_rotation_euler(euler_rotation)

        #! TODO: Think of and implement more object manipulation methods

    class RenderLight():
        """Render a light source."""

        def __init__(self, light_type = "POINT", name = "light"):
            """Initialise a light source in the scene.
            
            :param light_type: The type of light, can be one of [POINT, SUN, SPOT, AREA].
            :param name: The name of the new light, can be used for keeping track of different light sources.
            """
            self.light = bproc.types.Light(light_type, name)

        def set_loc(self, location):
            """Set the location of a light source in the scene.
            
            :param location: A list containing [x,z,y] where x,z,y is an integer or float. This determines the coordinates of the light's location.
            """
            self.light.set_location(location)

        def set_rotation(self, rotation):
            """Set the rotation of the light in the scene.

            :param euler_rotation: A list [x,z,y] with values for the rotation to be applied to the light.
            """
            self.light.set_rotation_euler(rotation)

        def set_energy(self, energy):
            """Sets the energy of the light.
            
            :param energy: The energy to set it as. Interpreted as watts.
            """
            self.light.set_energy(energy)

        def set_color(self, color):
            """Sets the color of the light using the RGB colour space.
            
            :param color: A list [r,g,b] containing the values of the red, green and blue attributes from 0 to 255 inclusive.
            """
            self.light.set_color(color)

