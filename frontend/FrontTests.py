import random

def Tab_Checker(window, shared_state, Port, backend):
    print("NavBar Check")
    Tab_names = ["Object", "Pivot Point", "Render", "Lighting", "Random", "Import/Export", "Settings"]
    Tab_state = [False, False, False, False, False, True, True]
    NavBar = window.layout().itemAtPosition(0, 0).widget()
    for i in range(NavBar.count()):
        print(f"Tab {Tab_names[i]}: {'Valid' if Tab_names[i] == NavBar.tabText(i) else 'InValid'}, ")
        print(f"Expected {Tab_state[i]}: {'Valid' if Tab_state[i] == NavBar.isTabEnabled(i) else 'InValid'}")
        
def ObjectsTab_Check(window, shared_state, ObjectTab, backend):
    NavBar = window.layout().itemAtPosition(0, 0).widget()
    NavBar.setTabEnabled(0, True)
    print("ObjectTab Check")
    
    
    obj = backend.RenderObject("bugatti.obj")
    shared_state.add_item(obj, "bugatti_1")    
    
    print(ObjectTab.layout())
            
def Tests(window, shared_state, ObjectTab, PivotTab, Render, RandomTabDialog, RandomDefault, RandomLight, RandomObject, RandomPivot, RandomRender, Lighting, Port, Settings, backend):
    Tab_Checker(window, shared_state, Port, backend)
    ObjectsTab_Check(window, shared_state, ObjectTab, backend)