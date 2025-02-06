"""The main backend file which deals with rendering."""

# import blenderproc as bproc
import numpy as np
import random
import json
import os

# initialise config - will hold the config ready for export
config = { 
    "pivot": {},
}

# remove linter wanrings that bproc is undefined (it's undefined due to vsc not running using blender's python interpreter)
# pyright: reportUndefinedVariable=false

# check if this is the blender environment
try:
    bproc
except NameError:
    is_blender_environment = False
else:
    is_blender_environment = True

class Backend():
    """The main backend class which deals with setting up paramaters for the renderer."""
    def __init__(self, json_filepath=None):
        """Initialise the backend by setting up bproc.

        :param json_filepath: Filepath to a JSON configuration file.
        """
        

        if (is_blender_environment):
            bproc.init()
        
        self.initialise_cfg() # initialise config

        new_seed = random.randint(1000000, 999999999) # set config seed to a random 7 digit number
        self.set_seed(new_seed)

        if (json_filepath is not None):
            # load json objects into self
            temp = None
            with open(json_filepath, "r") as import_file:
                temp = json.load(import_file)

            # call funcitons to set up scene
            poses = temp.get("camera_poses", False)
            if (poses):
                for pose in poses:
                    self.add_cam_pose(pose)
            if ("background_color" in temp):
                self.set_bg_color(temp["background_color"])
            if ("render_res" in temp):
                self.set_res(temp["render_res"])

            if ("objects" in temp):
                for obj in temp["objects"]:
                    o = None
                    if ("filename" in obj):
                        o = self.RenderObject(filepath = obj["filename"])
                    else:
                        o = self.RenderObject(primative = obj["primative"])
                

                    o.set_loc(obj["pos"])
                    o.set_rotation(obj["rot"])
                    o.set_scale(obj["sca"])

            if ("light_sources" in temp):
                for light in temp["light_sources"]:
                    l = self.RenderLight(light["type"], light["name"])

                    l.set_loc(light["pos"])
                    l.set_rotation(light["rot"])
                    l.set_energy(light["energy"])
                    l.set_color(light["color"])

            if ("pivot" in temp):
                config["pivot"] = temp["pivot"].copy()

            if ("random" in temp):
                config["random"] = temp["random"].copy()

            if ("render" in temp):
                config["render"] = temp["render"].copy()
            if ("seed" in temp):
                self.set_seed(temp["seed"])
            if ("render_folder" in temp):
                config["render_folder"] = temp["render_folder"]

    def set_render_output_folder(self, path):
        config["render_folder"] = path


    def add_cam_pose(self, pose):
        """Adds a position of a camera to the scene for rendering.
        
        :param pose: a list containing position and rotation config details. Position in index 0 and rotation in index 1."""
        if (is_blender_environment):
            cam_pose = bproc.math.build_transformation_mat(pose[0], pose[1])
            bproc.camera.add_camera_pose(cam_pose)

        config.setdefault("camera_poses", [])
        config["camera_poses"].append(pose)

    def initialise_cfg(self):
        config.clear() # reset config due to new initialisation
        config["pivot"] = {
            "point": [0, 0, 0],
            "dis": 0
        }
        config["random"] = {
            "pivot": [],
            "environment": [],
            "pos": [],
            "sca": []
        }
        config["render"] = {
            "renders": 1,
            "degree": [1,1,1]
        }
        config["render_folder"] = ""

        config["render_res"] = [256,256]

    def set_pivot_point(self, point):
        """ Sets a custom pivotpoint in the scene for rendering.
        
        :param point: a list containing [X,Y,Z]"""
        config["pivot"]["point"] = point
        
    def set_pivot_distance(self, dis):
        """ Sets a custom distance for the pivotpoint in the scene for rendering.
        
        :param dis: a float value determining the distance"""
        config["pivot"]["dis"] = dis

    def set_seed(self,seed):
        """ Sets a custom seed for generating random when adding camera poses.
        
        :param seed: int value indicating random seed"""
        config["seed"] = seed

    def set_renders(self, n):
        """ Sets amount renders generated.
        
        :param n: int amount of renders"""
        config["render"]["renders"] = n

    def set_angles(self, angles):
        """ Sets camera angle change per render in the config.
        
        :param angles: a list containing x z and y angle change"""
        config["render"]["degree"] = angles

    def toggle_random_pivot_x(self):
        """Toggles value for if pivot x coordinate is randomised"""
        if "x" in config["random"]["pivot"]:
            config["random"]["pivot"].remove("x")
        else:
            config["random"]["pivot"].append("x")

    def toggle_random_pivot_z(self):
        """Toggles value for if pivot z coordinate is randomised"""
        if "z" in config["random"]["pivot"]:
            config["random"]["pivot"].remove("z")
        else:
            config["random"]["pivot"].append("z")

    def toggle_random_pivot_y(self):
        """Toggles value for if pivot y coordinate is randomised"""
        if "y" in config["random"]["pivot"]:
            config["random"]["pivot"].remove("y")
        else:
            config["random"]["pivot"].append("y")

    def toggle_random_environment_angle(self):
        """Toggles value for if the angle is randomised during render"""
        if "angle" in config["random"]["environment"]:
            config["random"]["environment"].remove("angle")
        else:
            config["random"]["environment"].append("angle")

    def toggle_random_environment_background(self):
        """Toggles value for if background colour is randomised during render"""
        if "background" in config["random"]["environment"]:
            config["random"]["environment"].remove("background")
        else:
            config["random"]["environment"].append("background")

    def toggle_random_coord_x(self,selected_index):
        if "x" in config["random"]["pos"]:
            config["random"]["pos"].remove("x")
        else:
            config["random"]["pos"].append("x")
        self.add_object_properties(selected_index)

    def toggle_random_coord_y(self,selected_index):
        if "y" in config["random"]["pos"]:
            config["random"]["pos"].remove("y")
        else:
            config["random"]["pos"].append("y")
        self.add_object_properties(selected_index)

    def toggle_random_coord_z(self,selected_index):
        if "z" in config["random"]["pos"]:
            config["random"]["pos"].remove("z")
        else:
            config["random"]["pos"].append("z")
        self.add_object_properties(selected_index)


    def toggle_random_width(self,selected_index):
        if "width" in config["random"]["sca"]:
            config["random"]["sca"].remove("width")
        else:
            config["random"]["sca"].append("width")
        self.add_object_properties(selected_index)
        


    def toggle_random_height(self,selected_index):
        if "height" in config["random"]["sca"]:
            config["random"]["sca"].remove("height")
        else:
            config["random"]["sca"].append("height")
        self.add_object_properties(selected_index)

    def toggle_random_length(self,selected_index):
        if "length" in config["random"]["sca"]:
            config["random"]["sca"].remove("length")
        else:
            config["random"]["sca"].append("length")
        self.add_object_properties(selected_index)
  
    def is_config_objects_empty(self):
        if config.get("objects") == None:
            return True
        
        for obj in config.get("objects"):
            if obj != None:
                return False
            
        return True
        
    def get_config(self):
        return config
        
    def set_res(self, resolution):
        """Set the resolution of the output images. Will effect total render time.

        :param resolution: A list [x, y] with the height and width of the resolution in pixels.
        """
        if (is_blender_environment):
            bproc.camera.set_resolution(resolution[0], resolution[1])

        config["render_res"] = resolution

    def set_bg_color(self, color, strength=1):
        """Sets the world background color for rendering. Note: RBG values are between 0-1, diving by 255 gives the appropriate values. 
        
        :param color: a list containing RGB values for the color of the background.
        :param strength: strength of the background color, set to 1 by default."""
        if (is_blender_environment):
            bproc.renderer.set_world_background([color[0]/255, color[1]/255, color[2]/255], strength)

        config["background_color"] = color


    def calculate_position(self, angle, distance):
        """Calulates position of camera based on the angle of camera and distance from pivot point
        
        :param angle: a list containing the camera angle
        :param distance: distance from pivot point

        :return param position: list containing x,z,y position values for camera"""

        r = np.sin(angle[0]) * distance

        x_position = r * np.sin( angle[2] )    #calculate x and y positions based on y angle
        z_position = -1 * r * np.cos( angle[2] )

        y_position = np.cos(angle[0]) * distance #caluclate y angle based on x positions

        position = [x_position, z_position, y_position]
        return position

    
    def add_camera_poses(self):
        """Add camera poses to generate render from"""

        randoms = config["random"] #Read values from config

        pivot_distance = config["pivot"]["dis"]
        pivot_point = config["pivot"]["point"]

        degree_change = config["render"]["degree"]

        number_of_renders = config["render"]["renders"]

        starting_x_angle = np.pi / 2 #No place in UI to set starting camera angle 
        starting_z_angle = 0
        starting_y_angle = 0

        current_x_angle = starting_x_angle
        current_z_angle = starting_z_angle
        current_y_angle = starting_y_angle

        

        for i in range(number_of_renders): #Reads config and randomised parts of render meant to be rendered
            
            if "background" in randoms["environment"]:
                self.set_bg_color( [ random.randint(1,255) , random.randint(1,255) , random.randint(1,255) ] )
            else:
                pass

            camera_rotation = [current_x_angle,current_z_angle,current_y_angle]
            position = self.calculate_position(camera_rotation, pivot_distance)

            if "x" in randoms["pivot"]:
               position[0] += random.randint(0,10)
            else:
                position[0] += pivot_point[0]

            if "z" in randoms["pivot"]:
               position[1] += random.randint(0,10)
            else:
                position[1] += pivot_point[1]
            
            if "y" in randoms["pivot"]:
               position[2] += random.randint(0,10)
            else:
                position[2] += pivot_point[2] 

            self.add_cam_pose([position, camera_rotation])

            if "angle" in randoms["environment"]:
                current_x_angle += np.deg2rad( random.randint(0,359) )
                current_z_angle += np.deg2rad( random.randint(0,359) )
                current_y_angle += np.deg2rad( random.randint(0,359) )
            else:
                current_x_angle += degree_change[0]
                current_z_angle += degree_change[1]
                current_y_angle += degree_change[2]

    def remove_camera_poses(self):
        """Remove camera poses that have been used to generate renders"""

        config["camera_poses"] = []
   

    def add_object_properties(self,selected_index):
        #IF ANYONE WANTS ASSIGN VALUES TO RANDOM RANGE I JUST PUT PLACEHOLDER VALUES
        obj = config["objects"][selected_index]

        # Get randomization settings from the config
        randoms = config["random"]
        random_object_pos = randoms["pos"]
        random_object_scale = randoms["sca"]

        # Copy current position and scale values
        position = obj["pos"].copy()
        scale = obj["sca"].copy()
            #Position propertis
        if "x" in random_object_pos:
            position[0] = random.uniform(1, 10) # random range of x coords - 1-10
            print(f"Randomized Object X: {scale[0]}")
            
        if "y" in random_object_pos:
            position[2] = random.uniform(1, 10)
            print(f"Randomized Object y: {position[2]}")


        if "z" in random_object_pos:
            position[1] = random.uniform(1, 10)
            print(f"Randomized Object Z: {position[1]}")


            #Scale properties
        if "width" in random_object_scale:
            self.random_object_width = random.uniform(1,5)
            scale[0] = self.random_object_width # random range of width - 1-100
            print(f"Randomized Width: {scale[0]}")

            
        if "height" in random_object_scale:
            scale[1] = random.uniform(1, 5)
            print(f"Randomized Height: {scale[1]}")


        if "length" in random_object_scale:
            scale[2] = random.uniform(1, 5)
            print(f"Randomized Length: {scale[2]}")

                    
        obj["pos"] = position
        obj["sca"] = scale
        obj = config["objects"][selected_index]


    def render(self, headless = False):
        """Renders the scene and saves to file in the output folder."""
        self.add_camera_poses()
        

        with open("backend\\temp_export.json", "w") as export_file:
            json.dump(config, export_file)

        # Create a temporary file for the blender environment and call it
        path = os.path.abspath(os.getcwd()) + "\\backend"
        file_contents = ""

        with open(path + "\\backend.py", "r") as this_file:
            file_contents = this_file.read()

        with open(path + "\\_temp.py", "w") as to_run:
            path = path.replace("\\", "\\\\")
            to_run.write("import blenderproc as bproc\n" + file_contents + f"""Backend("{path}\\\\temp_export.json")._render()""")

        os.system("blenderproc run backend/_temp.py")
        if (not headless):
            for i in range(config["render"]["renders"]):
                os.system("blenderproc vis hdf5 output/"+str(i)+".hdf5")
        os.remove("backend/_temp.py")
        os.remove("backend/temp_export.json")

        self.remove_camera_poses()
        
    def _render(self):
        """Internal function for rendering. Don't call this normally, it's called for rendering internally."""
        data = bproc.renderer.render()
        if config["render_folder"] == "":
            bproc.writer.write_hdf5("output/", data)
        else:
            bproc.writer.write_hdf5(config["render_folder"], data)

    def export(self, path, filename="export.json"):
        """Exports the current scene setup to a JSON file.
        
        :param filename: The filename of the exported config, defaults to export.json."
        """
        config["render_folder"] = ""
        file_path = path + "/" + filename
        with open(file_path, "w") as export_file:
            json.dump(config, export_file, indent = 2)

    class RenderObject():
        """An object to be rendered."""
        
        def __init__(self, filepath=None, primative=None):
            """Initialise a render object.

            :param filepath: Filepath to an object file.
            :param primative: Create object primatively, choose from one of ["CUBE", "CYLINDER", "CONE", "PLANE", "SPHERE", "MONKEY"].
            """
            self.object_pos = len(config.setdefault("objects", []))
            config["objects"].append({})
                        
            if (filepath is not None):
                if (is_blender_environment):
                    self.object = bproc.loader.load_blend(filepath) if filepath.endswith(".blend") else bproc.loader.load_obj(filepath)
                config["objects"][self.object_pos] = {
                    "filename": filepath,
                    "pos": [0, 0, 0],
                    "rot": [0, 0, 0],
                    "sca": [1, 1, 1]
                }
                return

            if (primative is not None):
                if (is_blender_environment):
                    self.object = bproc.object.create_primitive(primative)
                config["objects"][self.object_pos] = {
                    "primative": primative,
                    "pos": [0, 0, 0],
                    "rot": [0, 0, 0],
                    "sca": [1, 1, 1]
                }
                return

            raise TypeError('No filepath or primative argument given.')

        def __str__(self):
            return f"Object {self.object_pos + 1}"

        def set_loc(self, location):
            """Set the location of an object in the scene.
            
            :param location: A list containing [x,z,y] where x,z,y is an integer or float. This determines the coordinates of the object's location.
            """
            if (is_blender_environment):
                self.object.set_location(location)
            
            config["objects"][self.object_pos]["pos"] = location

        def set_scale(self, scale):
            """Set the scale of an object in the scene.
            
            :param scale: A list containing [x,z,y] where x,z,y is an integer or float. This determines the scaling of each axis.
            """
            if (is_blender_environment):
                self.object.set_scale(scale)
            config["objects"][self.object_pos]["sca"] = scale

        def set_rotation(self, euler_rotation):
            """Set the rotation of an object in the scene.
            
            :param euler_rotation: A list containing [x,y,z] - (pitch,yaw,roll) values for the euler rotation to be applied to the object.
            """
            if (is_blender_environment):
                self.object.set_rotation_euler(euler_rotation)

            config["objects"][self.object_pos]["rot"] = euler_rotation

        def remove_object(self):
            """Remove the object from the scene"""

            config["objects"][self.object_pos] = None


        #! TODO: Think of and implement more object manipulation methods

    class RenderLight():
        """Render a light source."""

        def __init__(self, light_type = "POINT", name = "light"):
            """Initialise a light source in the scene.
            
            :param light_type: The type of light, can be one of [POINT, SUN, SPOT, AREA].
            :param name: The name of the new light, can be used for keeping track of different light sources.
            """
            if (is_blender_environment):
                self.light = bproc.types.Light(light_type, name)

            self.light_pos = len(config.setdefault("light_sources", []))
            config["light_sources"].append({
                "type": light_type,
                "name": name,
                "pos": [0, 0, 0],
                "rot": [0, 0, 0],
                "energy": 10,
                "color": [255, 255, 255],
                "radius": 0
            })

        def set_type(self, type):
            #print(config)
            if (is_blender_environment):
                self.light.set_type(type)

            config["light_sources"][self.light_pos]["type"] = type

        def set_radius(self, radius):
            #print(radius)
            if (is_blender_environment):
                self.light.set_radius(radius)

            config["light_sources"][self.light_pos]["radius"] = radius


        def set_loc(self, location):
            """Set the location of a light source in the scene.
            
            :param location: A list containing [x,z,y] where x,z,y is an integer or float. This determines the coordinates of the light's location.
            """
            #print("location changed")
            if (is_blender_environment):
                self.light.set_location(location)

            config["light_sources"][self.light_pos]["pos"] = location

        def set_rotation(self, rotation):
            """Set the rotation of the light in the scene.

            :param rotation: A list [x,z,y] with values for the rotation to be applied to the light.
            """
            #print("angle changed")
            rotRad = []
            for x in rotation:
                rotRad.append(np.deg2rad(int(x)))


            if (is_blender_environment):
                self.light.set_rotation_euler(rotRad)

            config["light_sources"][self.light_pos]["rot"] = rotation

        def set_energy(self, energy):
            """Sets the energy of the light.
            
            :param energy: The energy to set it as. Interpreted as watts.
            """
            #print("energy changed")
            if (is_blender_environment):
                self.light.set_energy(energy)

            config["light_sources"][self.light_pos]["energy"] = energy


        def hex_to_rgba(self, hex_value: str):
            """ Converts the given hex string to rgba color values.

            :param hex_value: The hex string, describing rgb.
            :return: The rgba color, in form of a list. Values between 0 and 1.

            THIS HAS BEEN BORROWED PERMENETLY FROM THE BPROC SOURCE CODE!
            I COULDN'T FIGURE OUT HOW TO CALL IT
            SOMEONE FIX IF YOU WANT TO
            OR WE REFERENCE
            :SHRUG:
            """
            return [x / 255 for x in bytes.fromhex(hex_value[-6:])]

        def set_color(self, color):
            """Sets the color of the light using the RGB colour space.
            
            :param color: A list [r,g,b] containing the values of the red, green and blue attributes from 0 to 255 inclusive.
            """
            print(color)
            colour = self.hex_to_rgba(color)
            #print(colour)
            if (is_blender_environment):
                self.light.set_color(colour)

            config["light_sources"][self.light_pos]["color"] = color