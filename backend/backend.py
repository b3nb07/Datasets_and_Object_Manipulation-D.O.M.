"""The main backend file which deals with rendering."""

import blenderproc as bproc
import numpy as np

class Backend():
    """The main backend class which deals with setting up paramaters for the renderer."""
    def __init__(self, json=None):
        # TODO: Ethan
        """Initialise the backend by setting up bproc

        :param json: Filepath to a JSON configuration file.
        """
        raise NotImplementedError()

    def set_cam_pose(self, pose):
        """Sets the position of the camera in the scene for rendering
        
        :param pose: a list containing position and rotation config details. Position in index 0 and rotation in index 1"""
        cam_pose = bproc.math.build_transformation_mat(pose[0], pose[1])
        

    def set_bg_colour(self, colour, strength=1):
        """Sets the world background colour for rendering. Note: RBG values are between 0-1, diving by 255 gives the appropriate values
        
        :param colour: a list containing RGB values for the colour of the background
        :param strength: strength of the background colour, set to 1 by default"""

        bproc.renderer.set_world_background([colour[0]/255, colour[1]/255, colour[2]/255], strength)


    def render(self):
        """Renders the scene and saves to file in the output folder"""

        data = bproc.renderer.render()

        bproc.writer.write_hdf5("output/", data)


    class RenderObject():
        """An object to be rendered."""

        def __init__(self, filepath=None):
            """Initialise a render object.

            :param filepath: Filepath to an object file.
            """
            self.object = bproc.loader.load_blend(filepath) if filepath.endswith(".blend") else bproc.loader.load_obj(filepath)

        def set_loc(self, location):
            """Set the location of an object in the scene.
            
            :param location: A list containing [x,z,y] where x,z,y is an integer or float. This determines the coordinates of the objects location.
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

    class RenderLight(bproc.types.Light):
        """Render a light source."""

        def __init__(self, light_type = "POINT", name = "light"):
            super().__init__(light_type, name)
            raise NotImplementedError()

