import random


def Tab_Checker(window, shared_state, backend):
    Tab_names = ["Object", "Pivot Point", "Generate Random", "Render", "Import and Export"]
    for i in range(window.navbar.tabwizard.count()):
        print(f"{Tab_names[i]}: {'Correct' if Tab_names[i] == window.navbar.tabwizard.tabText(i) else 'Incorrect'}")
        

def Page_1_Section_1_Checker(window, shared_state, Page1, backend):
    print("\n Page_1_Section_1_Checker")
    """Tests if all functions in page 1 section 1 work, Input field is detectable and can be incremented and decremented"""
    ####
    obj = backend.RenderObject(primative = "Monkey")
    shared_state.add_item(obj)
    ####
    Path = window.navbar.tabwizard.findChild(Page1)
    
    window.navbar.tabwizard.setTabEnabled(0, True)
    window.navbar.tabwizard.setCurrentIndex(0)
    
    sections = [[Path.XObj_pos_input_field, Path.X_button_plus, Path.X_button_minus], [Path.YObj_pos_input_field, Path.Y_button_plus, Path.Y_button_minus], [Path.ZObj_pos_input_field, Path.Z_button_plus, Path.Z_button_minus]]
    for Sections in sections:
            print(f"Expected 0, {'Correct' if Sections[0].text() == str(0) else 'Incorrect'}")
            
            val = random.randint(1,99)
            val = f"{float(val)}"
            Sections[0].setText(str(val))
            print(f"Expected {val}, {'Correct' if Sections[0].text() == val else 'Incorrect'}")
            
            Sections[1].click()
            val = f"{float(val) + 1}"
            print(f"Expected {val} , {'Correct' if Sections[0].text() == val else 'Incorrect'}")
            
            Sections[2].click()
            val = f"{float(val) - 1}"
            print(f"Expected {val}, {'Correct' if Sections[0].text() == val else 'Incorrect'}")
        
        
        
def Page_1_Section_2_Checker(window, shared_state, Page1, backend):
    print("\n Page_1_Section_2_Checker")
    ####
    obj = backend.RenderObject(primative = "Monkey")
    shared_state.add_item(obj)
    ####
    Path = window.navbar.tabwizard.findChild(Page1)
    
    window.navbar.tabwizard.setTabEnabled(0, True)
    window.navbar.tabwizard.setCurrentIndex(0)
    sections = [[Path.Width_Obj_pos_input_field, Path.W_slider], [Path.Length_Obj_pos_input_field, Path.L_slider], [Path.Height_Obj_pos_input_field, Path.H_slider]]
   
   
    for Sections in sections:
            val = random.randint(1,99)
            Sections[0].setText(str(val))
            Sections[0].editingFinished.emit()
            print(f"Expected {val}, {'Correct' if Sections[1].value() == int(val) else 'Incorrect'}") 
            
            val = random.randint(1,99)
            Sections[1].setSliderPosition(int(val))
            Sections[1].sliderMoved.emit(val)
            print(f"Expected {Sections[0].text()}, {'Correct' if Sections[0].text() == str(Sections[1].value()) else 'Incorrect'}")
            
def Page_1_Section_3_Checker(window, shared_state, Page1, backend):
    print("\n Page_1_Section_3_Checker")
    ####
    Path = window.navbar.tabwizard.findChild(Page1)

    window.navbar.tabwizard.setTabEnabled(0, True)
    window.navbar.tabwizard.setCurrentIndex(0)
    sections = [[Path.X_Rotation_input_field, Path.X_Rotation], [Path.Y_Rotation_input_field, Path.Y_Rotation], [Path.Z_Rotation_input_field, Path.Z_Rotation]]
   
    for Sections in sections:
            val = random.randint(1,359)
            Sections[0].setText(str(val))
            Sections[0].editingFinished.emit()
            print(f"Expected {val}, {'Correct' if Sections[1].value() == int(val) else 'Incorrect'}") 
            
            val = random.randint(1,359)
            Sections[1].setSliderPosition(int(val))
            Sections[1].sliderMoved.emit(val)
            print(f"Expected {Sections[0].text()}, {'Correct' if Sections[0].text() == str(Sections[1].value()) else 'Incorrect'}")
    
def Page_2_Section_1_Checker(window, shared_state, Page2, backend):
    print("\n Page_2_Section_1_Checker")
    """Tests if all functions in page 2 section 1 work, Input field is detectable and can be incremented and decremented"""
    ####
    ####
    Path = window.navbar.tabwizard.findChild(Page2)
    
    window.navbar.tabwizard.setTabEnabled(1, True)
    window.navbar.tabwizard.setCurrentIndex(1)
    
    sections = [[Path.XPivot_point_input_field, Path.XPivot_button_plus, Path.XPivot_button_minus], [Path.YPivot_point_input_field, Path.YPivot_button_plus, Path.YPivot_button_minus], [Path.ZPivot_point_input_field, Path.ZPivot_button_plus, Path.ZPivot_button_minus]]
    for Sections in sections:
            print(f"Expected 0.0, {'Correct' if Sections[0].text() == str(0.0) else 'Incorrect'}")
            
            val = random.randint(-100,100)
            val = f"{float(val)}"
            Sections[0].setText(str(val))
            print(f"Expected {val}, {'Correct' if Sections[0].text() == val else 'Incorrect'}")
            
            Sections[1].click()
            val = f"{float(val) + 1}"
            print(f"Expected {val} , {'Correct' if Sections[0].text() == val else 'Incorrect'}")
            
            Sections[2].click()
            val = f"{float(val) - 1}"
            print(f"Expected {val}, {'Correct' if Sections[0].text() == val else 'Incorrect'}")
            
def Page_2_Section_2_Checker(window, shared_state, Page2, backend):
    print("\n Page_2_Section_2_Checker")
    ####
    ####
    Path = window.navbar.tabwizard.findChild(Page2)
    
    window.navbar.tabwizard.setTabEnabled(1, True)
    window.navbar.tabwizard.setCurrentIndex(1)
    sections = [[Path.Distance_Pivot_input_field, Path.Distance_Slider]]
   
   
    for Sections in sections:
            val = random.randint(1,100)
            Sections[0].setText(str(val))
            Sections[0].editingFinished.emit()
            print(f"Expected {val}, {'Correct' if int(Sections[1].value()) == int(val) else 'Incorrect'}") 
            
            val = random.randint(1,100)
            Sections[1].setSliderPosition(int(val))
            Sections[1].sliderMoved.emit(val)
            print(f"Expected {Sections[0].text()}, {'Correct' if Sections[0].text() == str(Sections[1].value()) else 'Incorrect'}")
            
def Page_2_Section_3_Checker(window, shared_state, Page2, backend):
    print("\n Page_2_Section_3_Checker")
    ####
    ####
    Path = window.navbar.tabwizard.findChild(Page2)
    
    window.navbar.tabwizard.setTabEnabled(1, True)
    window.navbar.tabwizard.setCurrentIndex(1)
            
    Path.combo_box.activated.emit(1)
    
    sections = [Path.XPivot_point_input_field, Path.YPivot_point_input_field, Path.ZPivot_point_input_field]
    for Section in sections:
        print(f"Field {Section}: {'Disabled Correct' if not Section.isEnabled() else 'Enabled Incorrect'}")
        
    Path.Pivot_Point_Check.setChecked(True)
    
    sections = [Path.XPivot_point_input_field, Path.YPivot_point_input_field, Path.ZPivot_point_input_field]
    for Section in sections:
        print(f"Field {Section}: {'Enabled Correct' if Section.isEnabled() else 'Disabled Incorrect'}")
        
def Page_3_Section_Checker(window, shared_state, Page3, backend):
    print("\n Page_3_Section_Checker")
    ####
    ####
    Path = window.navbar.tabwizard.findChild(Page3)
    
    window.navbar.tabwizard.setTabEnabled(2, True)
    window.navbar.tabwizard.setCurrentIndex(2)
    
    Path.Set_All_Random_Button.setChecked(True)
    
    All_Checks = [Path.Width_Button, Path.Height_Button, Path.Length_Button, Path.X_Button, Path.Y_Button, Path.Z_Button,
                  Path.X_Button2, Path.Y_Button2, Path.Z_Button2, Path.AutoRotationAngle_Button, Path.ImportEnvironment_Button]

    
    for check in All_Checks:
        print(f"{'Field is Checked: Correct' if check.isChecked() else 'Field is not Checked: Incorrect'}")
        
def Page_4_Section_1_Checker(window, shared_state, Page4, backend):
    print("\n Page_4_Section_1_Checker")
    ####
    ####
    Path = window.navbar.tabwizard.findChild(Page4)
    
    window.navbar.tabwizard.setTabEnabled(3, True)
    window.navbar.tabwizard.setCurrentIndex(3)
    
    sections = [[Path.Number_of_renders_input_field, Path.Number_of_renders_plus, Path.Number_of_renders_minus]]
    for Sections in sections:
            print(f"Expected 1, {'Correct' if Sections[0].text() == str(1) else 'Incorrect'}")
            
            val = random.randint(2,359)
            val = f"{int(val)}"
            Sections[0].setText(str(val))
            Sections[0].editingFinished.emit()
            print(f"Expected {val}, {'Correct' if Sections[0].text() == val else 'Incorrect'}")
            Sections[1].click()
            val = int(val) + 1
            print(f"Expected {val} , {'Correct' if Sections[0].text() == str(val) else 'Incorrect'}")
            Sections[2].click()
            val = int(val) - 1
            print(f"Expected {val} , {'Correct' if Sections[0].text() == str(val) else 'Incorrect'}")
        
def Page_4_Section_2_Checker(window, shared_state, Page4, backend):
    print("\n Page_4_Section_2_Checker")
    ####
    ####
    Path = window.navbar.tabwizard.findChild(Page4)
    window.navbar.tabwizard.setTabEnabled(3, True)
    window.navbar.tabwizard.setCurrentIndex(3)
    sections = [[Path.X_Degree_input_field, Path.X_Degree_slider], [Path.Y_Degree_input_field, Path.Y_Degree_slider], [Path.Z_Degree_input_field, Path.Z_Degree_slider]]
   
    for Sections in sections:
            val = random.randint(2,359)
            Sections[0].setText(str(val))
            Sections[0].editingFinished.emit()
            print(f"Expected {val}, {'Correct' if Sections[0].text() == str(val) else 'Incorrect'}") 
            
            val = random.randint(2,359)
            Sections[1].setSliderPosition(int(val))
            Sections[1].sliderMoved.emit(val)
            print(f"Expected {Sections[0].text()}, {'Correct' if Sections[0].text() == str(Sections[1].value()) else 'Incorrect'}")
            
def Illegal_Field_checker(window, shared_state, Page1, Page2, Page3, Page4, Page5, backend):
    Path = window.navbar.tabwizard.findChild(Page1)
    
    window.navbar.tabwizard.setTabEnabled(0, True)
    window.navbar.tabwizard.setCurrentIndex(0)
    val = "A"
    
    sections = [Path.XObj_pos_input_field, Path.YObj_pos_input_field, Path.ZObj_pos_input_field,
                Path.Width_Obj_pos_input_field, Path.Length_Obj_pos_input_field, Path.Height_Obj_pos_input_field,
                Path.X_Rotation_input_field, Path.Y_Rotation_input_field, Path.Z_Rotation_input_field]
    
    for Sections in sections:
        Sections.setText(str(val))
        
        
    window.navbar.tabwizard.setTabEnabled(1, True)
    window.navbar.tabwizard.setCurrentIndex(1)
        
    Path = window.navbar.tabwizard.findChild(Page2)
    sections = [Path.XPivot_point_input_field, Path.YPivot_point_input_field, Path.ZPivot_point_input_field,
                Path.Distance_Pivot_input_field,
                Path.XPivot_point_input_field, Path.YPivot_point_input_field, Path.ZPivot_point_input_field]
    
    for Sections in sections:
        Sections.setText(str(val))
        
    window.navbar.tabwizard.setTabEnabled(2, True)
    window.navbar.tabwizard.setCurrentIndex(2)
    
    Path = window.navbar.tabwizard.findChild(Page4)
    sections = [Path.Number_of_renders_input_field,
                Path.X_Degree_input_field, Path.Y_Degree_input_field,  Path.Z_Degree_input_field]
    
    window.navbar.tabwizard.setTabEnabled(3, True)
    window.navbar.tabwizard.setCurrentIndex(3)
    
    for Sections in sections:
        Sections.setText(str(val))

        
def Tests(window, shared_state, Page1, Page2, Page3, Page4, Page5, backend):
    print("Tab_Checker")
    Tab_Checker(window, shared_state, backend)
    
    print("Page_1")
    Page_1_Section_1_Checker(window, shared_state, Page1, backend)
    Page_1_Section_2_Checker(window, shared_state, Page1, backend)
    Page_1_Section_3_Checker(window, shared_state, Page1, backend)
    
    print("Page_2")
    Page_2_Section_1_Checker(window, shared_state, Page2, backend)
    Page_2_Section_2_Checker(window, shared_state, Page2, backend)
    Page_2_Section_3_Checker(window, shared_state, Page2, backend)
    
    print("Page_3")
    Page_3_Section_Checker(window, shared_state, Page3, backend)
    
    print("Page_4")
    Page_4_Section_1_Checker(window, shared_state, Page4, backend)
    Page_4_Section_2_Checker(window, shared_state, Page4, backend)
    
    Illegal_Field_checker(window, shared_state, Page1, Page2, Page3, Page4, Page5, backend)