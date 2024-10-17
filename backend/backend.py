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

    def set_cam_pose(self):
        # TODO: Ilya
        raise NotImplementedError()

    def set_bg_colour(self):
        # TODO: Ilya
        raise NotImplementedError()

    def render(self):
        # TODO: Ilya
        raise NotImplementedError()

    class RenderObject():
        """An object to be rendered."""

        def __init__(self, filepath=None):
            """Initialise a render object.

            :param filepath: Filepath to an object file.
            """
            self.object = bproc.loader.load_blend(filepath) if filepath.endswith(".blend") else bproc.loader.load_obj(filepath)

        def set_loc(self):
            # TODO: Miller
            raise NotImplementedError()

        def set_scale(self):
            # TODO: Miller
            raise NotImplementedError()

        def set_rotation(self):
            # TODO: Miller
            raise NotImplementedError()

        #! TODO: Think of and implement more object manipulation methods

    class RenderLight(bproc.types.Light):
        """Render a light source."""

        def __init__(self, light_type = "POINT", name = "light"):
            super().__init__(light_type, name)
            raise NotImplementedError()

