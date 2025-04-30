import random

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
    
    obj = backend.RenderObject("bugatti.obj")
    shared_state.add_item(obj, "bugatti_2")
    
    ObjectTab.Object_detect(ObjectTab, NavBar)
    for i in range(NavBar.count()):
        TestPrint(f"Expected True:", True == NavBar.isTabEnabled(i))
        
def Render(window, tab_widget, ObjectTab):
    TestPrint("---Render")
    Enviroment = window.layout().itemAtPosition(1, 3).widget().styleSheet()
    Initial = "background-position: center;background-repeat: no-repeat;background-image: url(viewport_temp/loading.png);"
    TestPrint(f"Expected {Initial}:", Initial == Enviroment)
    
    #TestPrint(f"Expected {Initial}:", Initial != Enviroment)
    
    
        
def ObjectTabTests(tab_widget, shared_state, ObjectTab):
    TestPrint("---Object Tab Check")
    Page = tab_widget.widget(0).layout()
    
    ButtonFields = [[1, 1], [2, 1], [3, 1]]
    Rotation_Fields = [[1, 5], [2, 5], [3, 5]]
    Scale_Fields = [[1, 8], [2, 8], [3, 8]]
    
    for s in range(shared_state.count()):
    
        for i in range(len(ButtonFields)):
            TestPrint(f"{s}---Object Tab Button Check")
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
            
        TestPrint(f"{s}---Object Rotation Slider Check")
        for i in range(len(Rotation_Fields)):
            Field = Page.itemAtPosition(Rotation_Fields[i][0], Rotation_Fields[i][1]).widget()
            Slider = Page.itemAtPosition(Rotation_Fields[i][0], Rotation_Fields[i][1]+1).widget()
            
            #Error Checking on Slider
            Field.setText("OYJ")
            ObjectTab.Slider_Update_Scale(ObjectTab, 0, Field)
            TestPrint(f"Expected 0.0:", Field.text() == "0.0")
            
            #Updates Field Value
            ObjectTab.Slider_Update_Scale(ObjectTab, 5450, Field)
            TestPrint(f"Expected 100:", Field.text() == "100.0")
            
            """#Updates slider position
            ObjectTab.Update_slider(ObjectTab, Slider, 5450)
            TestPrint(f"Expected 100:", Slider.sliderPosition() == "100")"""
            
        
        TestPrint(f"{s}---Object Scale Slider Check")
        for i in range(len(Scale_Fields)):
            Field = Page.itemAtPosition(Scale_Fields[i][0], Scale_Fields[i][1]).widget()
            Slider = Page.itemAtPosition(Scale_Fields[i][0], Scale_Fields[i][1]+1).widget()
            
            #Error Checking on Slider
            Field.setText("OYJ")
            ObjectTab.Slider_Update_Scale(ObjectTab, 10, Field)
            TestPrint(f"Expected 0.0:", Field.text() == "0.0")
            
            ObjectTab.Slider_Update_Scale(ObjectTab, 5450, Field)
            TestPrint(f"Expected 100:", Field.text() == "100.0")
            
            """#Updates slider position
            ObjectTab.Update_slider(ObjectTab, Slider, 5450)
            TestPrint(f"Expected 100:", Slider.sliderPosition() == "100")
            print(Slider.sliderPosition())"""
            
def PivotTabTests(tab_widget, shared_state, PivotTab):
    TestPrint("---Pivot Tab Check")
    Page = tab_widget.widget(1).layout()
    
    ButtonFields = [[1, 1], [2, 1], [3, 1]]
    Distance_Fields = [[1, 5]]
    
    for s in range(shared_state.count()):
    
        for i in range(len(ButtonFields)):
            TestPrint(f"{s}---Pivot Tab Button Check")
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
            
        TestPrint(f"{s}---PivotTab Slider Check")
        for i in range(len(Distance_Fields)):
            Field = Page.itemAtPosition(Distance_Fields[i][0], Distance_Fields[i][1]).widget()
            Slider = Page.itemAtPosition(Distance_Fields[i][0], Distance_Fields[i][1]+1).widget()
            
            #Error Checking on Slider
            Field.setText("OYJ")
            PivotTab.Slider_Update(PivotTab, 10, Field)
            TestPrint(f"Expected 0:", Field.text() == "0")
            
            #Updates slider position
            PivotTab.Update_slider(PivotTab, Slider, 50)
            #Updates Field Value
            PivotTab.Slider_Update(PivotTab, 50, Field)
            TestPrint(f"Expected 50:", Field.text() == "50")

def RenderTabTests(tab_widget, shared_state, RenderTab):
        TestPrint("---Render Tab Check")
        Page = tab_widget.widget(2).layout()

        s = 0

        ButtonFields = [[1, 0]]
        Slider_Fields = [[1, 4], [2, 4], [3, 4]]
    
        for i in range(len(ButtonFields)):
            TestPrint(f"{s}---Render Tab Button Check")
            Field = Page.itemAtPosition(ButtonFields[i][0], ButtonFields[i][1]).widget()
            MinusButton = Page.itemAtPosition(ButtonFields[i][0], ButtonFields[i][1]+1).widget()
            PlusButton = Page.itemAtPosition(ButtonFields[i][0], ButtonFields[i][1]+2).widget()

            #Error Checking on MinusButton
            Field.setText("OYJ")
            MinusButton.click()
            TestPrint(f"Expected 1:", Field.text() == "1")
            
            #Error Checking on PlusButton
            Field.setText("OYJ")
            PlusButton.click()
            TestPrint(f"Expected 1:", Field.text() == "1")
            
            #Checking Buttons Alter values
            Field.setText("10")
            MinusButton.click()
            TestPrint(f"Expected 9:", Field.text() == "9")
            PlusButton.click()
            TestPrint(f"Expected 10:", Field.text() == "10")

        TestPrint(f"{s}---Render Tab Slider Check")
        for i in range(len(Slider_Fields)):
            Field = Page.itemAtPosition(Slider_Fields[i][0], Slider_Fields[i][1]).widget()
            Slider = Page.itemAtPosition(Slider_Fields[i][0], Slider_Fields[i][1]+1).widget()
            
            #Error Checking on Slider
            Field.setText("OYJ")
            RenderTab.Slider_Update(RenderTab, 10, Field)
            TestPrint(f"Expected 0.0:", Field.text() == "0.0")
            
            #Updates Field Value
            RenderTab.Slider_Update(RenderTab, 50, Field)
            TestPrint(f"Expected 50:", Field.text() == "50")

def LightingTabTests(tab_widget, shared_state, LightingTab):
        TestPrint("---Lighting Tab Check")
        Page = tab_widget.widget(3).layout()

        ButtonFields = [[2, 1], [1, 5], [2, 5], [3, 5]]
        Slider_Fields = [[0, 1], [1, 9], [2, 9], [3, 9]]

        s = 0

        TestPrint(f"{s}---Lighting Tab Button Check")
        for Position in ButtonFields:
            Field = Page.itemAtPosition(Position[0], Position[1]).widget()
            MinusButton = Page.itemAtPosition(Position[0], Position[1]+1).widget()
            PlusButton = Page.itemAtPosition(Position[0], Position[1]+2).widget()
            
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
            
        TestPrint(f"{s}---Lighting Tab Slider Check")
        for Position in Slider_Fields:
            Field = Page.itemAtPosition(Position[0], Position[1]).widget()
            Slider = Page.itemAtPosition(Position[0], Position[1]+1).widget()
            
            #Error Checking on Slider
            Field.setText("OYJ")
            LightingTab.Slider_Update(LightingTab, 10, Field)
            TestPrint(f"Expected 0.0:", Field.text() == "0.0")
            
            #Updates Field Value
            LightingTab.Slider_Update(LightingTab, 50, Field)
            TestPrint(f"Expected 50:", Field.text() == "50")

def RandomDefaultTabTests(tab_widget):
    TestPrint("---Random Default Tab Check")
    Page = tab_widget.widget(0)
    PageLayout = Page.layout()

    #XOR CHECKING
    TestPrint("XOR CheckBox Testing")
    PageLayout.itemAtPosition(1, 0).widget().setChecked(True)
    TestPrint("Check 1 not Check 2:", not PageLayout.itemAtPosition(2, 0).widget().isChecked())

    PageLayout.itemAtPosition(2, 0).widget().setChecked(True)
    TestPrint("Check 2 not Check 1:", not PageLayout.itemAtPosition(1, 0).widget().isChecked())

    PageLayout.itemAtPosition(0, 0).widget().setChecked(True)

def RandomTabPageTests(tab_widget, PagePos):
    Pages = ["Default", "Object", "Pivot", "Render", "Lighting"]
    CheckBoxPos = 12 if PagePos == 4 else 10 
    TestPrint(f"---Random {Pages[PagePos]} Tab Check")
    Page = tab_widget.widget(PagePos)
    PageLayout = Page.layout()

    TestPrint("---All Enabled")
    for keys in Page.CheckBoxes.keys():
        x, y = Page.CheckBoxes[keys]
        TestPrint("Expected True:", PageLayout.itemAtPosition(1, x).widget().isChecked())
        PageLayout.itemAtPosition(1, CheckBoxPos).widget().setChecked(False)

    for keys in Page.CheckBoxes.keys():
        x, y = Page.CheckBoxes[keys]
        TestPrint("---Checkbox False: Field Disabled")
        if not PageLayout.itemAtPosition(y, x).widget().isChecked():
            TestPrint("Expected False:", not PageLayout.itemAtPosition(y, x+1).widget().isEnabled())
            TestPrint("Expected False:", not PageLayout.itemAtPosition(y, x+2).widget().isEnabled())

        PageLayout.itemAtPosition(y, x).widget().setChecked(True)

        TestPrint("---Checkbox True: Field Enabled")
        if PageLayout.itemAtPosition(y, x).widget().isChecked():
            TestPrint("Expected True:", PageLayout.itemAtPosition(y, x+1).widget().isEnabled())
            TestPrint("Expected True:", PageLayout.itemAtPosition(y, x+2).widget().isEnabled())

        TestPrint("---Illegal Value")
        PageLayout.itemAtPosition(y, x+1).widget().setText("OYJ")
        PageLayout.itemAtPosition(y, x+1).widget().editingFinished.emit()
        TestPrint("Expected 0:", PageLayout.itemAtPosition(y, x+1).widget().text() == "0")
        TestPrint("Expected 0:", PageLayout.itemAtPosition(y, x+2).widget().text() == "0")

        TestPrint("---LowerBound Value > UpperBound Value")
        PageLayout.itemAtPosition(y, x+1).widget().setText("1")
        PageLayout.itemAtPosition(y, x+2).widget().setText("0")
        PageLayout.itemAtPosition(y, x+1).widget().editingFinished.emit()
        TestPrint("Expected -inf:", PageLayout.itemAtPosition(y, x+1).widget().text() == "-inf")

        TestPrint("---UpperBound Value < LowerBound Value")
        PageLayout.itemAtPosition(y, x+1).widget().setText("1")
        PageLayout.itemAtPosition(y, x+2).widget().setText("0")
        PageLayout.itemAtPosition(y, x+2).widget().editingFinished.emit()
        TestPrint("Expected -inf:", PageLayout.itemAtPosition(y, x+1).widget().text() == "-inf")

    PageLayout.itemAtPosition(1, CheckBoxPos).widget().setChecked(True)
    PageLayout.itemAtPosition(1, CheckBoxPos).widget().setChecked(False)
    TestPrint("---AllPage Checkbox False: Field Disabled")
    for keys in Page.CheckBoxes.keys():
        x, y = Page.CheckBoxes[keys]
        TestPrint("Expected False:", not PageLayout.itemAtPosition(y, x+1).widget().isEnabled())
        TestPrint("Expected False:", not PageLayout.itemAtPosition(y, x+2).widget().isEnabled())

#Invoked on line 991
def RandomTabTests(tab_widget):
    TestPrint("---Random Tab Check")
    RandomDefaultTabTests(tab_widget)
    RandomTabPageTests(tab_widget, 1)
    RandomTabPageTests(tab_widget, 2)
    RandomTabPageTests(tab_widget, 3)
    RandomTabPageTests(tab_widget, 4)

#Invoked on line 213
def Tests(window, tab_widget, shared_state, ObjectTab, PivotTab, RenderTab, LightingTab, backend):
    Tab_Checker(window, shared_state, backend)
    ObjectLoad(window, shared_state, ObjectTab, backend)
    Render(window, tab_widget, ObjectTab)
    ObjectTabTests(tab_widget, shared_state, ObjectTab)
    PivotTabTests(tab_widget, shared_state, PivotTab)
    RenderTabTests(tab_widget, shared_state, RenderTab)
    LightingTabTests(tab_widget, shared_state, LightingTab)
