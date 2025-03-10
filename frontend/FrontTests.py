import random
import time

def Tab_Checker(window, shared_state, backend):
    TestPrint("---NavBar Check")
    Tab_names = ["Object", "Pivot Point", "Render", "Lighting", "Random", "Import/Export", "Settings"]
    Tab_state = [False, False, False, False, False, True, True]
    NavBar = window.layout().itemAtPosition(0, 0).widget()
    for i in range(NavBar.count()):
        TestPrint(f"Tab {Tab_names[i]}:", Tab_names[i] == NavBar.tabText(i))
        TestPrint(f"Expected {Tab_state[i]}:", Tab_state[i] == NavBar.isTabEnabled(i))
        
def ObjectLoad(window, shared_state, ObjectTab, backend):
    NavBar = window.layout().itemAtPosition(0, 0).widget()
    NavBar.setTabEnabled(0, True)
    TestPrint("---Object Load Check")
    
    obj = backend.RenderObject("bugatti.obj")
    shared_state.add_item(obj, "bugatti_1")
    
    ObjectTab.Object_detect(ObjectTab, NavBar)
    for i in range(NavBar.count()):
        TestPrint(f"Expected True:", True == NavBar.isTabEnabled(i))
        
def Render(window, tab_widget, ObjectTab):
    TestPrint("---Render")
    Enviroment = window.layout().itemAtPosition(1, 3).widget().styleSheet()
    Initial = "background-position: center;background-repeat: no-repeat;background-image: url(viewport_temp/loading.png);"
    TestPrint(f"Expected {Initial}:", Initial == Enviroment)
    
    #TestPrint(f"Expected {Initial}:", Initial != Enviroment)
    
    
        
def ObjectTabTests(window, tab_widget, shared_state, ObjectTab, backend):
    TestPrint("---Object Tab Check")
    Page = tab_widget.widget(0).layout()
    
    ButtonFields = [[1, 1], [2, 1], [3, 1]]
    Rotation_Fields = [[1, 5], [2, 5], [3, 5]]
    Scale_Fields = [[1, 8], [2, 8], [3, 8]]
    
    for i in range(len(ButtonFields)):
        TestPrint("---Object Tab Button Check")
        Field = Page.itemAtPosition(ButtonFields[i][0], ButtonFields[i][1]).widget()
        MinusButton = Page.itemAtPosition(ButtonFields[i][0], ButtonFields[i][1]+1).widget()
        PlusButton = Page.itemAtPosition(ButtonFields[i][0], ButtonFields[i][1]+2).widget()
        
        #Error Checking on MinusButton
        Field.setText("OYJ")
        MinusButton.click()
        TestPrint(f"Expected 0.0:", Field.text() == "0.0")
        
        #Error Checking on PlusButton
        Field.setText("OYJ")
        PlusButton.click()
        TestPrint(f"Expected 0.0:", Field.text() == "0.0")
        
        #Checking Buttons Alter values
        MinusButton.click()
        TestPrint(f"Expected -1.0:", Field.text() == "-1.0")
        PlusButton.click()
        TestPrint(f"Expected 0.0:", Field.text() == "0.0")
        
    TestPrint("---Object Rotation Slider Check")
    for i in range(len(Rotation_Fields)):
        Field = Page.itemAtPosition(Rotation_Fields[i][0], Rotation_Fields[i][1]).widget()
        Slider = Page.itemAtPosition(Rotation_Fields[i][0], Rotation_Fields[i][1]+1).widget()
        
        #Error Checking on Slider
        Field.setText("OYJ")
        ObjectTab.Slider_Update_Scale(ObjectTab, 10, Field)
        TestPrint(f"Expected 0.0:", Field.text() == "0.0")
    
    TestPrint("---Object Scale Slider Check")
    for i in range(len(Scale_Fields)):
        Field = Page.itemAtPosition(Scale_Fields[i][0], Scale_Fields[i][1]).widget()
        Slider = Page.itemAtPosition(Scale_Fields[i][0], Scale_Fields[i][1]+1).widget()
        
        #Error Checking on Slider
        Field.setText("OYJ")
        ObjectTab.Slider_Update_Scale(ObjectTab, 10, Field)
        TestPrint(f"Expected 0.0:", Field.text() == "0.0")
        
    
    
    
    
            
def Tests(window, tab_widget, shared_state, ObjectTab, backend):
    Tab_Checker(window, shared_state, backend)
    ObjectLoad(window, shared_state, ObjectTab, backend)
    Render(window, tab_widget, ObjectTab)
    ObjectTabTests(window, tab_widget, shared_state, ObjectTab, backend)
    
def TestPrint(String, Valid=None):
    PASS =  '\033[32m'
    OKBLUE = '\033[94m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    if Valid == None:
        print(f"{OKBLUE}{String}{ENDC}")
    elif Valid:
        print(f"{PASS}{String} Valid{ENDC}")
    else:
        print(f"{FAIL}{String} Invalid{ENDC}")