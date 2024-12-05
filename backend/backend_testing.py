import random, backend, unittest

"""
Structure of my unit testing with unit tests
1: Config
1.1. Initilisation testing of the config file.
1.2. Ensure the config file updates with backend functions.

2: Objects
2.1: Insert an objecct/objects
2.2: Edit the lights attributes

3: Lighting
3.1: Insert a light/lights
3.2: Edit the lights attributes

4. Test Sequence Method - Allows which functions to be auto tested.



Please keep in mind during testing we used agile methods to make sure the correct things have been altered and our code functions
I guess more tests have never hurt anyone except my sanity :)
"""

class BackendUnitTests(unittest.TestCase):
    def __init__(self) -> None:
        """ Initialise backend class and some general/testing helpers """
        super().__init__()
        self.backend = backend.Backend()
        self.get_cfg = self.backend.get_config()
        
    def initial_config(self) -> None:
        """ Method used to test the initialisation of the config """
        cfg = self.get_cfg # retrieve config from backend and do some tests
        
        # test pivot values
        self.assertEqual(cfg['pivot']['point'], [0,0,0])
        self.assertEqual(cfg['pivot']['dis'], 0)
        
        # test 'random' values
        self.assertEqual(cfg['random']['pivot'], [])
        self.assertEqual(cfg['random']['environment'], [])
        self.assertEqual(cfg['random']['pos'], [])
        self.assertEqual(cfg['random']['sca'], [])

        # test render values
        self.assertEqual(cfg['render']['renders'], 1)
        self.assertEqual(cfg['render']['degree'], [1,1,1])

        # test objects is empty
        self.assertEqual(self.backend.is_config_objects_empty(), True)

        
    def pivot_update(self):
        """ Method to update the pivot point and ensure it is updated """
        cfg = self.get_cfg
        cfg['pivot']['point'] = [0,0,0] # initilises the pivot point to 0,0,0
        
        # sets new pivotpoint to random x,y,z
        x, y, z = random.uniform(-100, 100), random.uniform(-100, 100), random.uniform(-100, 100)
        self.backend.set_pivot_point([x,y,z])
        self.assertNotEqual(cfg['pivot']['point'], [0,0,0]) # ensures its not the initialised value
        self.assertEqual(cfg['pivot']['point'], [x,y,z]) # ensures its equal to random value
        
    def pivot_distance(self):
        """ Method to update the pivot distance and ensure it is updated """
        cfg = self.get_cfg
        cfg['pivot']['dis'] = 0 # initilises the pivot point to 0,0,0
        
        # sets new pivot distance to a random float
        dis = random.uniform(-1000, 1000)
        self.backend.set_pivot_distance(dis)
        self.assertNotEqual(cfg['pivot']['dis'], 0) # ensures its not the initialised value
        self.assertEqual(cfg['pivot']['dis'], dis) # ensures its equal to random value
       
    def update_seed(self):
        """ Method to update the seed and ensure it is updated """
        cfg = self.get_cfg
        cfg['seed']= 1234567 # initilises seed to 1234567
        
        # sets new seed value to a random integer
        seed = random.randint(1000000, 999999999)
        self.backend.set_seed(seed)
        self.assertNotEqual(cfg['seed'], 1234567) # ensures its not the initialised value
        self.assertEqual(cfg['seed'], seed) # ensures its equal to random value
        
    def render_amount(self):
        """ Method to update the number of renders and ensure it is updated """
        cfg = self.get_cfg
        cfg['render']['renders']= 1 # initilises n to 1
        
        # sets new seed value to a random integer
        n = random.randint(2, 10)
        self.backend.set_renders(n)
        self.assertNotEqual(cfg['render']['renders'], 1) # ensures its not the initialised value
        self.assertEqual(cfg['render']['renders'], n) # ensures its equal to random value
        
    def set_angles(self):
        """ Method to update the camera angle change per render and ensure it is updated """
        cfg = self.get_cfg
        cfg['render']['degree']= [1,1,1] # initilises to [1,1,1]
        
        # sets new seed value to a random integer
        angles = [random.randint(2, 10),random.randint(2, 10),random.randint(2, 10)]
        self.backend.set_angles(angles)
        self.assertNotEqual(cfg['render']['degree'], [1,1,1]) # ensures its not the initialised value
        self.assertEqual(cfg['render']['degree'], angles) # ensures its equal to random value

    def toggle_piv_x(self):
        """ Method to toggle the randomising of x pivot value and ensure it is updated """
        cfg = self.get_cfg
        cfg['random']['pivot']= [] # initilises to empty list
        
        self.backend.toggle_random_pivot_x()
        self.assertNotEqual(cfg['random']['pivot'], []) # ensures its not the initialised value
        self.assertEqual(cfg['random']['pivot'], ['x']) # ensures its equal to toggled value
        
        # toggle it again
        self.backend.toggle_random_pivot_x()
        self.assertEqual(cfg['random']['pivot'], [])
        
    def toggle_piv_y(self):
        """ Method to toggle the randomising of y pivot value and ensure it is updated """
        cfg = self.get_cfg
        cfg['random']['pivot']= [] # initilises to empty list
        
        self.backend.toggle_random_pivot_y()
        self.assertNotEqual(cfg['random']['pivot'], []) # ensures its not the initialised value
        self.assertEqual(cfg['random']['pivot'], ['y']) # ensures its equal to toggled value
        
        # toggle it again
        self.backend.toggle_random_pivot_y()
        self.assertEqual(cfg['random']['pivot'], [])
        
    def toggle_piv_z(self):
        """ Method to toggle the randomising of z pivot value and ensure it is updated """
        cfg = self.get_cfg
        cfg['random']['pivot']= [] # initilises to empty list
        
        self.backend.toggle_random_pivot_z()
        self.assertNotEqual(cfg['random']['pivot'], []) # ensures its not the initialised value
        self.assertEqual(cfg['random']['pivot'], ['z']) # ensures its equal to toggled value
        
        # toggle it again
        self.backend.toggle_random_pivot_z()
        self.assertEqual(cfg['random']['pivot'], [])

    def toggle_env_angle(self):
        """ Method to toggle the randomising of the environment angle and ensure it is updated """
        cfg = self.get_cfg
        cfg['random']['environment']= [] # initilises to empty list
        
        self.backend.toggle_random_environment_angle()
        self.assertNotEqual(cfg['random']['environment'], []) # ensures its not the initialised value
        self.assertEqual(cfg['random']['environment'], ['angle']) # ensures its equal to toggled value
        
        # toggle it again
        self.backend.toggle_random_environment_angle()
        self.assertEqual(cfg['random']['environment'], [])

    def toggle_env_bg(self):
        """ Method to toggle the randomising of the environment background and ensure it is updated """
        cfg = self.get_cfg
        cfg['random']['environment']= [] # initilises to empty list
        
        self.backend.toggle_random_environment_background()
        self.assertNotEqual(cfg['random']['environment'], []) # ensures its not the initialised value
        self.assertEqual(cfg['random']['environment'], ['background']) # ensures its equal to toggled value
        
        # toggle it again
        self.backend.toggle_random_environment_background()
        self.assertEqual(cfg['random']['environment'], [])
        
    def change_res(self):
        """ Method to update the render resolution and ensure it is updated """
        cfg = self.get_cfg
        
        self.assertEqual(cfg['render_res'], [256, 256]) # ensures its equal to initial value
        self.backend.set_res([2560, 1440])
        self.assertEqual(cfg['render_res'], [2560, 1440]) # ensures its equal to updated value
        
    def toggle_obj_x(self):
        """ Method to toggle the randomising of the objects x position and ensure it is updated """
        self.obj = self.backend.RenderObject(primative = "MONKEY")

        cfg = self.get_cfg
        cfg['random']['pos']= [] # initilises to empty list
        
        self.backend.toggle_random_coord_x(0)
        self.assertNotEqual(cfg['random']['pos'], []) # ensures its not the initialised value
        self.assertEqual(cfg['random']['pos'], ['x']) # ensures its equal to toggled value
        
        # toggle it again
        self.backend.toggle_random_coord_x(0)
        self.assertEqual(cfg['random']['pos'], [])

        self.obj.remove_object()
        
    def toggle_obj_y(self):
        """ Method to toggle the randomising of the objects y position and ensure it is updated """
        self.obj = self.backend.RenderObject(primative = "MONKEY")

        cfg = self.get_cfg
        cfg['random']['pos']= [] # initilises to empty list
        
        self.backend.toggle_random_coord_y(0)
        self.assertNotEqual(cfg['random']['pos'], []) # ensures its not the initialised value
        self.assertEqual(cfg['random']['pos'], ['y']) # ensures its equal to toggled value
        
        # toggle it again
        self.backend.toggle_random_coord_y(0)
        self.assertEqual(cfg['random']['pos'], [])

        self.obj.remove_object()
    
    def toggle_obj_z(self):
        """ Method to toggle the randomising of the objects z position and ensure it is updated """
        self.obj = self.backend.RenderObject(primative = "MONKEY")

        cfg = self.get_cfg
        cfg['random']['pos']= [] # initilises to empty list
        
        self.backend.toggle_random_coord_z(0)
        self.assertNotEqual(cfg['random']['pos'], []) # ensures its not the initialised value
        self.assertEqual(cfg['random']['pos'], ['z']) # ensures its equal to toggled value
        
        # toggle it again
        self.backend.toggle_random_coord_z(0)
        self.assertEqual(cfg['random']['pos'], [])

        self.obj.remove_object()
        
    def render_obj(self):
        """ Method to import a primitive object and shows config updates"""
        cfg = self.get_cfg
        self.assertEqual(self.backend.is_config_objects_empty(), True) # no objects should be in cfg
        self.backend.RenderObject(primative="MONKEY")
        self.assertEqual(self.backend.is_config_objects_empty(), False) # object should be in cfg
    
        self.backend.RenderObject(primative="CUBE")
        self.backend.RenderObject(primative="MONKEY")
        # 3 objects should now be contained in objects config
        self.assertEqual(len(cfg['objects']), 3)
        
    def edit_obj(self):
        """ Method to import a primitive object and changes its properties """
        # reinitialising the config
        cfg = self.get_cfg
        self.backend.initialise_cfg()

        # render a primative object
        obj = self.backend.RenderObject(primative="MONKEY")
        
        # ==================== Location Testing ====================
        # test this obj is where it should be initialised
        self.assertEqual(cfg['objects'][0]['pos'], [0,0,0])
        # generate a random location and apply this to the objects location
        random_loc = [random.uniform(-100,100), random.uniform(-100,100), random.uniform(-100,100)]
        obj.set_loc(random_loc)
        self.assertNotEqual(cfg['objects'][0]['pos'], [0,0,0]) # obj no longer at initial pos
        self.assertEqual(cfg['objects'][0]['pos'], random_loc) # obj now at random pos
        
        # ==================== Scale Testing ====================
        # test this obj is where it should be initialised
        self.assertEqual(cfg['objects'][0]['sca'], [1,1,1])
        # generate a random scale and apply this to the object
        random_sca = [random.uniform(-100,100), random.uniform(-100,100), random.uniform(-100,100)]
        obj.set_scale(random_sca)
        self.assertNotEqual(cfg['objects'][0]['sca'], [1,1,1]) # obj no longer initial scale
        self.assertEqual(cfg['objects'][0]['sca'], random_sca) # obj now random scale
        
        # ==================== Rotation Testing ====================
        # test the obj rptatopm is what it should be at initilisation
        self.assertEqual(cfg['objects'][0]['rot'], [0,0,0])
        # generate a random scale and apply this to the object
        random_rot = [random.uniform(0.1,1.9), random.uniform(0.1,1.9), random.uniform(0.1,1.9)]
        obj.set_rotation(random_rot)
        self.assertNotEqual(cfg['objects'][0]['rot'], [0,0,0]) # obj no longer initial scale
        self.assertEqual(cfg['objects'][0]['rot'], random_rot) # obj now random scale

    def render_lights(self):
        """ Method to render lights and prove config updates"""
        cfg = self.get_cfg
        self.backend.initialise_cfg()

        light_1 = self.backend.RenderLight()
        light_2 = self.backend.RenderLight()
        
        # ==================== Multiple Light Testing ====================
        self.assertEqual(len(cfg['light_sources']), 2) # 2 lights should be currently rendered
        light_3 = self.backend.RenderLight()
        self.assertEqual(len(cfg['light_sources']), 3) # 3 lights should be currently rendered

        # ==================== Light location Testing ====================
        # test this light is where it should be initialised
        self.assertEqual(cfg['light_sources'][0]['pos'], [0,0,0])
        # generate a random location and apply this to the first light object
        random_loc = [random.uniform(1,10), random.uniform(-1,-10), random.uniform(1,10)]
        light_1.set_loc(random_loc)
        self.assertNotEqual(cfg['light_sources'][0]['pos'], [0,0,0]) # light no longer at initial pos
        self.assertEqual(cfg['light_sources'][0]['pos'], random_loc) # light now at random pos
        
        # ==================== Light Energy Testing ====================
        # test the light energy is what it should be initialised at
        self.assertEqual(cfg['light_sources'][1]['energy'], 10)
        # generate a random energy integer and apply this to the second light object
        random_en = random.randint(1,9)
        light_2.set_energy(random_en)
        self.assertNotEqual(cfg['light_sources'][1]['energy'], 10) # light no longer original energy
        self.assertEqual(cfg['light_sources'][1]['energy'], random_en) # light now at random energy
        
        # ==================== Light Colour Testing ====================
        # generate a random rgb and apply this to set a light to a specific rgb
        rgb = [random.randint(0,255), random.randint(0,255), random.randint(0,255)]
        light_3.set_color(rgb)
        self.assertEqual(cfg['light_sources'][2]['color'], rgb) # light now at random energy
        
        # ==================== Light Rotation Testing ====================
        # test the light rotation is what it should be at initilisation
        self.assertEqual(cfg['light_sources'][0]['rot'], [0,0,0])
        # generate a random rotation and apply this to the light
        random_rot = [random.uniform(0.1,1.9), random.uniform(0.1,1.9), random.uniform(0.1,1.9)]
        light_1.set_rotation(random_rot)
        self.assertNotEqual(cfg['light_sources'][0]['rot'], [0,0,0]) # light rotation no longer initial value
        self.assertEqual(cfg['light_sources'][0]['rot'], random_rot) # light rotation now random value


def test_sequence(test):
    """ Method to be called to carry out a sequence of the testing. Comment out any lines you dont want to test """
    # more config orientated testing
    test.initial_config()
    test.pivot_update()
    test.pivot_distance()
    test.update_seed()
    test.render_amount()
    test.set_angles()
    test.toggle_piv_x()
    test.toggle_piv_y()
    test.toggle_piv_z()
    test.toggle_env_angle()
    test.toggle_env_bg()
    test.change_res()

    # object specific testing
    test.render_obj()
    test.edit_obj()
    test.toggle_obj_x()
    test.toggle_obj_y()
    test.toggle_obj_z()
    
    # light specific testing (I just put it all in one)
    test.render_lights()
    print("All tests passed, no errors occured")
    
    
        
if __name__ == '__main__':
    tester = BackendUnitTests()
    test_sequence(tester)