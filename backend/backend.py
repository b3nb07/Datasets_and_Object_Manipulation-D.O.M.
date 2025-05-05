"""The main backend file which deals with rendering."""

# import blenderproc as bproc
from copy import deepcopy
import sys, random, json, os, shutil, subprocess, multiprocessing
import numpy as np


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

        if not is_blender_environment:
            with open('interaction_log.txt','w') as file:
                file.write('Program initialised\n')
        
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
                    if obj == None: continue
                    o = None
                    if ("filename" in obj):
                        o = self.RenderObject(filepath = obj["filename"])
                    else:
                        o = self.RenderObject(primative = obj["primative"])

                    o.set_loc(obj["pos"])
                    o.set_rotation(obj["rot"])
                    o.set_scale(obj["sca"])

            if ("light_sources" in temp and temp["light_sources"].get("type")):
                # for now there is only one light which can be on the scene
                l = self.RenderLight(temp["light_sources"]["type"], temp["light_sources"]["name"])

                l.set_loc(temp["light_sources"]["pos"])
                l.set_rotation(temp["light_sources"]["rot"])
                l.set_energy(temp["light_sources"]["energy"])
                l.set_color(temp["light_sources"]["color"])

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

        Backend.update_log(f'Render output folder changed to: {path}\n')


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
            "mode": "set",
            "objects": {},
            "pivot": [],
            "environment": [],
            "pos": [],
            "sca": []
        }
        config["render"] = {
            "renders": 1,
            "degree": [0,0,0]
        }

        config["render_folder"] = "output/"
        
        path = config["render_folder"] 
        if (not os.path.exists(path)):
            try:
                os.mkdir("output/") 
            except:
                pass

        config["render_res"] = (256,256)

    def set_pivot_point(self, point):
        """ Sets a custom pivotpoint in the scene for rendering.
        
        :param point: a list containing [X,Y,Z]"""
        config["pivot"]["point"] = point

        Backend.update_log(f'Pivot point changed to: {point}\n')
        
    def set_pivot_distance(self, dis):
        """ Sets a custom distance for the pivotpoint in the scene for rendering.
        
        :param dis: a float value determining the distance"""
        config["pivot"]["dis"] = dis

        Backend.update_log(f'Pivot distance changed to: {dis}\n')

    def set_seed(self,seed):
        """ Sets a custom seed for generating random when adding camera poses.
        
        :param seed: int value indicating random seed"""
        config["seed"] = seed
        random.seed(seed)

        Backend.update_log(f'Seed changed to: {seed}\n')

    def set_renders(self, n):
        """ Sets amount renders generated.
        
        :param n: int amount of renders"""
        config["render"]["renders"] = n

        Backend.update_log(f'Number of renders changed to: {n}\n')
   
    def set_angles(self, angles):
        """ Sets camera angle change per render in the config.
        
        :param angles: a list containing x y and z angle change"""
        config["render"]["degree"] = angles

    def toggle_random_mode(self, mode):
        """
        Toggles the random mode in config.

        Args:
            mode (str): The new mode to set for random operations. 

        Returns:
            None
        """
        config["random"]["mode"] = str(mode)
        Backend.update_log(f'Random mode set to {mode}\n')
        
    def update_random_attribute(self, index, category, field, state, lower, upper):        
        # cfg error handling:
        config["random"].setdefault("objects", {})
        config["random"]["objects"].setdefault(index, {})
        config["random"]["objects"][index].setdefault(category, {})

        # if still ticked
        if state:            
            # add field to config with bounds
            try:
                config["random"]["objects"][index][category][field] = [float(lower), float(upper)]
            except:
                config["random"]["objects"][index][category][field] = [0,0]
            # try apply this change
            if (config["random"]["mode"] == "set"):
                self.apply_specific_random_limit(index, category, field)
        else:
            # check this logic again
            # remove field from config if it exists
            if field in config["random"]["objects"][index][category]:
                del config["random"]["objects"][index][category][field]
        
    
    def apply_specific_random_limit(self, index, category, field):
        """Applies the specific limits"""
        try:
            lower_bound = float(config["random"]["objects"][index][category][field][0])
            upper_bound = float(config["random"]["objects"][index][category][field][1])
            
            random_value = random.uniform(lower_bound, upper_bound)
            self.update_appropriate_cfg(index, category, field, random_value)
        except:
            pass
    
    # this should be called for when its generating PER render
    def apply_all_random_limits(self):
        """Applies the limits at the per render mode"""
        try:
            for obj_index, categories in config["random"]["objects"].items():
                for category, attributes in categories.items():  # Iterate over categories (e.g., 'render', 'pivot')
                    for attr, bounds in attributes.items():  # Iterate over attributes within each category
                        try:
                            # Extract lower and upper bounds for random generation
                            lower_bound = float(bounds[0])
                            upper_bound = float(bounds[1])

                            # Generate a random value within bounds
                            random_value = random.uniform(lower_bound, upper_bound)
                            
                            # apply this field
                            self.apply_specific_random_limit(obj_index, category, attr)
                        except Exception as e:
                            print(f"Error processing attribute '{attr}' for Object {obj_index}: {e}")
        
            return config
        
        except Exception as e:
            print(f"Error processing config['random']['objects']: {e}")
   
    def update_appropriate_cfg(self, index, category, field, random_value): 
        """
        Updates the config file based on the specific index, category and field.
        
        Args:
            index (int): The objects index of the configuration to update if applicable default is 0.
            category (str): The category of which  configuration to update (object, pivot, render, light).
            field (str): The specific field within the category to update.
            random_value (float): The new value to be applied to the corresponding category and field.
            
        Returns:
            None 
        """
        match category:
            case 'object':
                self.random_update_object_loc(index, field, random_value)
            case 'pivot':
                self.random_update_pivot(field, random_value)
            case 'render':
                self.random_update_render(field, random_value)
            case 'light':
                self.random_update_light(field, random_value)
                
            case _:
                raise ValueError(f"Unrecognized category: {category}")

    def random_update_render(self, field, random_value):
        """
        Updates the render section in the config based on the specific field.
        
        Args:
            field (str): The specific field within the render config to update (X, Y, Z, Quantity).
            random_value (float): The new value to be applied to the corresponding field.

        Returns:
            dict: The updated render config.

        Notes:
            This function modifies the global config.
        """
        match field:
            case "X":
                config["render"]["degree"][0] = random_value
            case "Y":
                config["render"]["degree"][1] = random_value
            case "Z":
                config["render"]["degree"][2] = random_value
            
            case "Quantity":
                config["render"]["renders"] = int(np.ceil(random_value))
                
            case _:
                raise ValueError(f"Unrecognized category: {category}")
                
        return config

    def random_update_pivot(self, field, random_value):
        """
        Updates the pivot section in the config based on the specified field.

        Args:
            field (str): The specific field within the pivot config to update.
                        Expected vals: 'X', 'Y', 'Z' (pivot cords) or 'Measurement' (distance).
            random_value (float): The new value to apply to the specified field.

        Returns:
            dict: The updated pivot config.

        Notes:
            This function modifies the global config.
        """        
        match field:
            case "X":
                config["pivot"]["point"][0] = random_value
            case "Y":
                config["pivot"]["point"][1] = random_value
            case "Z":
                config["pivot"]["point"][2] = random_value
            
            case "Measurement":
                config["pivot"]["dis"] = random_value
            
            case _:
                raise ValueError(f"Unrecognized category: {category}")
            
        return config
    
    def random_update_light(self, field, random_value):
        """
        Updates the light source config based on the specified field.

        Args:
            field (str): The specific field within the light source config to update.
                Expected vals: (X, Y, Z, Pitch, Roll, Yaw, Strength, Radius, Colour)
            random_value (float): The new value to be applied to the corresponding field.

        Returns:
            dict: The updated config.
            
        Notes:
            This function modifies the global config.
        """
        match field:
            case "X":
                config["light_sources"]["pos"][0] = random_value
            case "Y":
                config["light_sources"]["pos"][1] = random_value
            case "Z":
                config["light_sources"]["pos"][2] = random_value
                
            case "Roll":
                config["light_sources"]["rot"][0] = random_value
            case "Pitch":
                config["light_sources"]["rot"][1] = random_value
            case "Yaw":
                config["light_sources"]["rot"][2] = random_value 
                
            case "Strength":
                config["light_sources"]["energy"] = random_value
            case "Radius":
                config["light_sources"]["radius"] = random_value
            
            case _:
                raise ValueError(f"Unrecognized field: {field}")
        
        return config

    def random_update_object_loc(self, index, field, random_value):
        match field:
            # assumes pos is xyz
            case "X":
                config["objects"][index]["pos"][0] = random_value
            case "Y":
                config["objects"][index]["pos"][1] = random_value
            case "Z":
                config["objects"][index]["pos"][2] = random_value
            
            # assumes pitch is Y, roll is X and yaw is Z
            case "Roll":
                config["objects"][index]["rot"][0] = random_value
            case "Pitch":
                config["objects"][index]["rot"][1] = random_value
            case "Yaw":
                config["objects"][index]["rot"][2] = random_value
            
            # assumes width is x height is y and length is z and is in form xyz
            case "Width":
                config["objects"][index]["sca"][0] = random_value
            case "Length":
                config["objects"][index]["sca"][1] = random_value
            case "Height":
                config["objects"][index]["sca"][2] = random_value
            
            case _:
                raise ValueError(f"Unrecognized field: {field}")
        return config
    

    def toggle_object(self, object, state):
        if state:
            if object.hidden: 
                object.add_object()
        else:
            if not object.hidden:
                object.remove_object()
    
    def ground_object(self, object, state):
        if state:
            object.grounded = True
            Backend.update_log(f'Object {object} grounded\n')
        else:
            object.grounded = False
            Backend.update_log(f'Object {object} ungrounded\n')
            
  
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

        Backend.update_log(f'Render resolution changed to {resolution}\n')


    def set_bg_color(self, color, strength=1):
        """Sets the world background color for rendering. Note: RBG values are between 0-1, diving by 255 gives the appropriate values. 
        
        :param color: a list containing RGB values for the color of the background.
        :param strength: strength of the background color, set to 1 by default."""
        if (is_blender_environment):
            bproc.renderer.set_world_background([color[0]/255, color[1]/255, color[2]/255], strength)

        config["background_color"] = color

        Backend.update_log(f'Background colour changed to {color}, with strength {strength}')


    def calculate_position(self, angle, distance):
        """Calulates position of camera based on the angle of camera and distance from pivot point
        
        :param angle: a list containing the camera angle
        :param distance: distance from pivot point

        :return param position: list containing x,y,z position values for camera"""

        r = np.sin(angle[0]) * distance

        x_position = r * np.sin( angle[2] )    #calculate x and y positions based on y angle
        y_position = -1 * r * np.cos( angle[2] )

        z_position = np.cos(angle[0]) * distance #calculate z angle based on x positions

        position = [x_position, y_position, z_position]
        return position

    
    def add_camera_poses(self, preview = False):
        """Add camera poses to generate render from"""

        randoms = config["random"] #Read values from config

        pivot_distance = config["pivot"]["dis"]
        pivot_point = config["pivot"]["point"]

        degree_change = config["render"]["degree"]

        number_of_renders = config["render"]["renders"]

        starting_x_angle = np.pi / 2
        starting_y_angle = 0
        starting_z_angle = 0

        current_x_angle = starting_x_angle
        current_y_angle = starting_y_angle
        current_z_angle = starting_z_angle

        if preview:
            number_of_renders = 1

        for i in range(number_of_renders): #Reads config and randomised parts of render meant to be rendered
            
            if "background" in randoms["environment"]:
                self.set_bg_color( [ random.randint(0,255) , random.randint(0,255) , random.randint(0,255) ] )
            else:
                pass

            camera_rotation = [current_x_angle,current_y_angle,current_z_angle]
            position = self.calculate_position(camera_rotation, pivot_distance)

            if "x" in randoms["pivot"]:
               position[0] += random.randint(0,10)
            else:
                position[0] += pivot_point[0]

            if "y" in randoms["pivot"]:
               position[1] += random.randint(0,10)
            else:
                position[1] += pivot_point[1]
            
            if "z" in randoms["pivot"]:
               position[2] += random.randint(0,10)
            else:
                position[2] += pivot_point[2] 

            self.add_cam_pose([position, camera_rotation])

            if preview == True:
                break

            if "angle" in randoms["environment"]:
                current_x_angle += np.deg2rad( random.randint(0,359) )
                current_y_angle += np.deg2rad( random.randint(0,359) )
                current_z_angle += np.deg2rad( random.randint(0,359) )
            else:
                current_x_angle += degree_change[0]
                current_y_angle += degree_change[1]
                current_z_angle += degree_change[2]

    def remove_camera_poses(self):
        """Remove camera poses that have been used to generate renders"""

        config["camera_poses"] = []

    def set_runtime_config(self, run_config):
        self.runtime_config = run_config

    def set_config(self, new_config):
        config = new_config

    def render(self, objects, headless = False, preview = False, viewport_temp = False):
        """Renders the scene and saves to file in the output folder."""

        if not viewport_temp: Backend.update_log(f'Rendering Started\n')
        else: Backend.update_log(f'Viewport Preview Render Started\n')


        self.add_camera_poses(viewport_temp)


        with open("backend/temp_export.json", "w") as export_file:
            json.dump(self.runtime_config, export_file)

        # Create a temporary file for the blender environment and call it
        path = os.path.abspath(os.getcwd()) + "/backend"
        if (sys.platform == 'win32'):
            path = path.replace("\\", "/")
        file_contents = ""

        with open(path + "/backend.py", "r") as this_file:
            file_contents = this_file.read()

        with open(path + "/_temp.py", "w") as to_run:
            to_run.write("import blenderproc as bproc\n" + file_contents + f"""Backend("{path}/temp_export.json")._render({viewport_temp})""")

        os.system("blenderproc run backend/_temp.py")

        highest = self.get_highest_in_dir()
        num = highest - config["render"]["renders"] + 1

        if (viewport_temp):
            os.system("blenderproc vis hdf5 viewport_temp/0.hdf5 --save viewport_temp")
        elif (not headless and preview):
            os.system("blenderproc vis hdf5 output/0.hdf5")
        elif (not headless):
            images = []
            for i in range(config["render"]["renders"]):
                hdf5_file = f"{config['render_folder']}/{i + num}.hdf5"
                if (i > 10): break
                image = multiprocessing.Process(target=subprocess.run, args=(["blenderproc", "vis", "hdf5", hdf5_file],))
                images.append(image)
                image.start()

        self.remove_camera_poses()

        '''for i in range(len(objects.items)):
            obj.properties = origObjects[i]'''

        try:
            os.remove("backend/temp_export.json")
            os.remove("backend/_temp.py")
        except:
            ...
        
    def _render(self, viewport_temp):
        """Internal function for rendering. Don't call this normally, it's called for rendering internally."""
        if (viewport_temp):
            # Turn off everything to make it fast
            bproc.renderer.set_denoiser(None)

            bproc.python.types.MeshObjectUtility.create_with_empty_mesh('emptyObject')

            bproc.writer.write_hdf5("viewport_temp/", bproc.renderer.render())
            return
        
        bproc.python.types.MeshObjectUtility.create_with_empty_mesh('emptyObject')
        data = bproc.renderer.render()
        if (config["render_folder"] == ""):
            bproc.writer.write_hdf5("output/", data, append_to_existing_output = True)
        else:
            bproc.writer.write_hdf5(config["render_folder"], data, append_to_existing_output = True)

    def get_highest_in_dir(self):
        highest = -1
        for file in os.listdir(config["render_folder"]):
            if file.endswith(".hdf5"):
                num = ""
                for x in file:
                    if x == ".":
                        break
                    else:
                        num = num + x
                try:
                    if int(num) > highest:
                        highest = int(num)
                except:
                    pass
        return 0 if highest == -1 else highest
    
    def export_interaction(self, path, filename="interaction_log.txt"):
        """Exports the current interaction log.
        
        :param filename: The filename of the exported config, defaults to export.json."
        """
        file_path = path + "/" + filename
        shutil.copyfile(filename, file_path)

        Backend.update_log(f'Interaction exported\n')

    def export(self, path, filename="export.json"):
        """Exports the current scene setup to a JSON file.
        
        :param filename: The filename of the exported config, defaults to export.json."
        """
        file_path = path + "/" + filename
        with open(file_path, "w") as export_file:
            json.dump(config, export_file, indent = 2)

        Backend.update_log(f'Settings exported\n')

    @staticmethod
    def update_log(interaction):

        if not is_blender_environment:

            try:

                with open('interaction_log.txt','r+') as file:
                    contents = file.read().split('\n')
                    if len(contents) == 0:
                        pass
                    elif len(contents) == 1:
                        if contents[-1] != interaction.rstrip('\n'):
                            file.write(interaction)
                    elif contents[-2] != interaction.rstrip('\n'):
                        file.write(interaction)

            except:
                print("Error updating log")


    class RenderObject():
        """An object to be rendered."""
        
        def __init__(self, filepath=None, primative=None):
            """Initialise a render object.
            :param filepath: Filepath to an object file.
            :param primative: Create object primatively, choose from one of ["CUBE", "CYLINDER", "CONE", "PLANE", "SPHERE", "MONKEY"].
            """
            self.object_pos = len(config.setdefault("objects", []))
            self.properties = None
            self.hidden = False
            self.grounded = False
            config["objects"].append({})

            Backend.update_log(f'{self.__str__()} object added\n')
                        
            if (filepath is not None):
                if (is_blender_environment):
                    # handle the objects list
                    loaded_objects = bproc.loader.load_blend(filepath) if filepath.endswith(".blend") else bproc.loader.load_obj(filepath)
                    self.object = loaded_objects[0] if isinstance(loaded_objects, list) else loaded_objects
                
                self.properties = {
                    "filename": filepath,
                    "pos": [0, 0, 0],
                    "rot": [0, 0, 0],
                    "sca": [1, 1, 1]
                }
                config["objects"][self.object_pos] = self.properties
                return

            if (primative is not None):
                if (is_blender_environment):
                    self.object = bproc.object.create_primitive(primative)

                self.properties = {
                    "primative": primative,
                    "pos": [0, 0, 0],
                    "rot": [0, 0, 0],
                    "sca": [1, 1, 1]
                }
                config["objects"][self.object_pos] = self.properties
                return

            raise TypeError('No filepath or primative argument given.')

        def __str__(self):
            return f"Object {self.object_pos + 1}"

        def set_loc(self, location):
            """Set the location of an object in the scene.
            
            :param location: A list containing [x,y,z] where x,y,z is an integer or float. This determines the coordinates of the object's location.
            """
            if (is_blender_environment):
                self.object.set_location(location)
            
            config["objects"][self.object_pos]["pos"] = location

            Backend.update_log(f'Location of {self.__str__()} changed to {location}\n')

        def set_scale(self, scale):
            """Set the scale of an object in the scene.
            
            :param scale: A list containing [x,y,z] where x,y,z is an integer or float. This determines the scaling of each axis.
            """
            if (is_blender_environment):
                self.object.set_scale(scale)
            config["objects"][self.object_pos]["sca"] = scale

            Backend.update_log(f'Scale of {self.__str__()} changed to {scale}\n')

        def set_rotation(self, euler_rotation):
            """Set the rotation of an object in the scene.
            
            :param euler_rotation: A list containing [x,y,z] - (roll,yaw,pitch) values for the euler rotation to be applied to the object.
            """
            if (is_blender_environment):
                self.object.set_rotation_euler(euler_rotation)

            config["objects"][self.object_pos]["rot"] = euler_rotation

            Backend.update_log(f'Rotation of {self.__str__()} changed to {euler_rotation}\n')

        def remove_object(self):
            """Remove the object from the scene"""

            config["objects"][self.object_pos] = None
            self.hidden = True

            Backend.update_log(f'{self.__str__()} object removed from the scene\n')
        
        def add_object(self):
            """Add the object to the scene"""

            config["objects"][self.object_pos] = self.properties
            self.hidden = False

            Backend.update_log(f'{self.__str__()} object added to the scene\n')


    class RenderLight():
        """Render a light source."""

        def __init__(self, light_type = "POINT", name = "light"):
            """Initialise a light source in the scene.
            
            :param light_type: The type of light, can be one of [POINT, SUN, SPOT, AREA].
            :param name: The name of the new light, can be used for keeping track of different light sources.
            """
            if (is_blender_environment):
                self.light = bproc.types.Light(light_type, name)

            self.light_pos = len(config.setdefault("light_sources", {}))

            Backend.update_log(f'{self.__str__()} light source added\n')

            config["light_sources"] = {
                "type": light_type,
                "name": name,
                "pos": [0, 0, 0],
                "rot": [0, 0, 0],
                "energy": 0,
                "color": [255, 255, 255],
                "radius": 0
            }

        def __str__(self):
            return f"Light Source {self.light_pos + 1}"

        def set_type(self, type):
            if (is_blender_environment):
                self.light.set_type(type)

            config["light_sources"]["type"] = type

            Backend.update_log(f'Type of {self.__str__()} changed to {type}\n')

        def set_radius(self, radius):
            if (is_blender_environment):
                self.light.set_radius(radius)

            config["light_sources"]["radius"] = radius

            Backend.update_log(f'Radius of {self.__str__()} changed to {radius}\n')

        def set_loc(self, location):
            """Set the location of a light source in the scene.
            
            :param location: A list containing [x,y,z] where x,y,z is an integer or float. This determines the coordinates of the light's location.
            """
            if (is_blender_environment):
                self.light.set_location(location)

            config["light_sources"]["pos"] = location

            Backend.update_log(f'Location of {self.__str__()} changed to {location}\n')

        def set_rotation(self, rotation):
            """Set the rotation of the light in the scene.

            :param rotation: A list [x,y,z] with values for the rotation to be applied to the light.
            """
            rotRad = []
            for x in rotation:
                rotRad.append(np.deg2rad(int(x)))


            if (is_blender_environment):
                self.light.set_rotation_euler(rotRad)

            config["light_sources"]["rot"] = rotation

            Backend.update_log(f'Rotation of {self.__str__()} changed to {rotation}\n')

        def set_energy(self, energy):
            """Sets the energy of the light.
            
            :param energy: The energy to set it as. Interpreted as watts.
            """
            if (is_blender_environment):
                self.light.set_energy(energy)

            config["light_sources"]["energy"] = energy

            Backend.update_log(f'Energy of {self.__str__()} changed to {energy}\n')


        def hex_to_rgba(self, hex_value: str):
            """ Converts the given hex string to rgba color values.

            :param hex_value: The hex string, describing rgb.
            :return: The rgba color, in form of a list. Values between 0 and 1.

            """
            try:
                return [x / 255 for x in bytes.fromhex(hex_value[-6:])]
            except:
                return [255, 255, 255]

        def set_color(self, color):
            """Sets the color of the light using the RGB colour space.
            
            :param color: A list [r,g,b] containing the values of the red, green and blue attributes from 0 to 255 inclusive.
            """
            colour = self.hex_to_rgba(color)
            if (is_blender_environment):
                self.light.set_color(colour)

            config["light_sources"]["color"] = color

            Backend.update_log(f'Colour of {self.__str__()} changed to {color}\n')
# Empty line required
