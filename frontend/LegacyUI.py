"""Importing"""

from functools import cached_property
import sys
from PyQt5 import QtCore, QtWidgets
from functools import cached_property

from PyQt5.QtWidgets import QApplication, QPushButton, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QTabWidget, QLabel, QLineEdit, QComboBox, QCheckBox
from PyQt5.QtCore import * 
from PyQt5.QtGui import * 
from PyQt5.QtWidgets import *

from sys import path
path.append("backend")
"""Importing"""
from backend import Backend
import numpy as np


""""
    Comment info - 
    Comment at start of class with :""" """" to signify the args,methods within class
    Add comment at start of methods describing their purpose
    Add green comments during parts of code you need to explain

"""



# Initialise backend
backend = Backend()



class ComboBoxState(QObject):

    """"
    ComboBoxState is a child of QObject, used to handle and maintain the shared box states
    Args:


    Methods:
        update_items
        add_item
        remove_item
        Update_selected


    """
    # Defines basic signals for items and selection updates
    items_updated = pyqtSignal(list) # signal to send when items are updated
    selection_changed = pyqtSignal(int)# signal to send when selection changes

    def __init__(self):
        super().__init__()
        self.items = [] # this will store what is in the combobox
        self.selected = None

    def update_items(self, items):
        self.items = items
        self.items_updated.emit(items)  # Emit signal for item updates

    def add_item(self, item):
        self.items.append(item)
        self.items_updated.emit(self.items)

    def remove_item(self, item):
        self.items.remove(item)
        self.items_updated.emit(self.items)

    def remove_item(self, item):
        self.items.remove(item)
        self.items_updated.emit(self.items)

    def update_selected(self, index):
        self.selected_index = index
        # maybe delete
        self.selection_changed.emit(index)

# creates this shared state
shared_state = ComboBoxState()

class Page(QtWidgets.QWidget):
    """
    Navbar page creation class
    """
    completeChanged = QtCore.pyqtSignal()

    def __init__(self, parent=None):
        """
        Intialise page class
        """
        super().__init__(parent)
        lay = QtWidgets.QVBoxLayout(self)
        lay.addWidget(self.container)

    @cached_property
    def container(self):
        return QtWidgets.QWidget()

class TabWizard(QTabWidget):
    """
    creates a tab like widget For the Navbar
    """
    def __init__(self, parent=None):
        super().__init__(parent)

    def addPage(self, page, title):
        """

        """
        if not isinstance(page, Page):
            raise TypeError(f"{page} must be a Page object")
        self.addTab(page, title)

class Widget(QtWidgets.QWidget):
    """
    Class to Add all pages into a tabwizard
    """
    def __init__(self):
        """
        Initialise widget class for Navbar
        """
        super().__init__()

        #nav bar widget adding
        self.tabwizard = TabWizard()
        lay = QVBoxLayout(self)
        lay.addWidget(self.tabwizard)

        #applying stlyes
        self.tabwizard.setStyleSheet(GlobalStyles.style())

        
        #pages
        self.tabwizard.addPage(Page1(), "Object")
        self.tabwizard.addPage(Page2(), "Pivot Point")
        self.tabwizard.addPage(Page3(), "Generate Random")
        self.tabwizard.addPage(Page4(), "Render")
        self.tabwizard.addPage(Page5(self), "Import and Export")
        self.tabwizard.setTabEnabled(0, False)
        self.tabwizard.setTabEnabled(1, False)
        self.tabwizard.setTabEnabled(2, False)
        self.tabwizard.setTabEnabled(3, False)
        
    def Object_detect(self):
        State = not Backend.is_config_objects_empty(self)
        for i in range(4):
            self.tabwizard.setTabEnabled(i, State)

        
class Page1(Page):
    """
    Page 1: Objects
    """
    def __init__(self, parent=None):
        """
        Initialise "Page n"
        
        Methods:
            __init__: Initializes the page with necessary UI components and connections.
            update_combo_box_items: Updates items in the combo box.
            on_object_selected: Changes displayed attributes when a new object is selected.
            Update_slider: Syncs text input to slider position.
            update_object_pos: Updates object position based on input fields.
            update_object_scale: Updates object scale dynamically.
            update_object_rotation: Adjusts object rotation as per input fields.
            Plus_click: Increments input field by 1.
            Minus_click: Decrements input field by 1.
            Slider_Update: Sets input field to slider value.
            update_label: Updates labels for position, scale, and rotation sections.
            resizeEvent: Adjusts component positions on window resize.
        
        """

    def __init__(self, parent=None):
        """
        Initialize Page 1:Object Manipulation UI components and buttons for object interaction
        
        Args:
            parent (QWidget, optional): Parent widget for this page.
        """

        
        super().__init__(parent)

        self.Object_pos_title = QLabel(f"Object 1 Co-ords", self)

        self.XObj_pos = QLabel("X:", self)
        self.XObj_pos_input_field = QLineEdit(parent=self)
        self.XObj_pos_input_field.setText("0.0")
        self.X_button_minus = QPushButton('-', self)
        self.X_button_plus = QPushButton('+', self)

        self.YObj_pos = QLabel("Y:", self)
        self.YObj_pos_input_field = QLineEdit(parent=self)
        self.YObj_pos_input_field.setText("0.0")

        self.Y_button_minus = QPushButton('-', self)
        self.Y_button_plus = QPushButton('+', self)
        
        self.ZObj_pos = QLabel("Z:", self)
        self.ZObj_pos_input_field = QLineEdit(parent=self) 
        self.ZObj_pos_input_field.setText("0.0")

        self.Z_button_minus = QPushButton('-', self)
        self.Z_button_plus = QPushButton('+', self)

        ##########################################################
        
        # editingFinished callbacks that updates backend
        self.XObj_pos_input_field.editingFinished.connect(self.update_object_pos)
        self.YObj_pos_input_field.editingFinished.connect(self.update_object_pos)
        self.ZObj_pos_input_field.editingFinished.connect(self.update_object_pos)
        
        self.X_button_plus.clicked.connect(lambda: self.Plus_click(self.XObj_pos_input_field))
        self.X_button_minus.clicked.connect(lambda: self.Minus_click(self.XObj_pos_input_field))
        
        self.Y_button_plus.clicked.connect(lambda: self.Plus_click(self.YObj_pos_input_field))
        self.Y_button_minus.clicked.connect(lambda: self.Minus_click(self.YObj_pos_input_field))
        
        self.Z_button_plus.clicked.connect(lambda: self.Plus_click(self.ZObj_pos_input_field))
        self.Z_button_minus.clicked.connect(lambda: self.Minus_click(self.ZObj_pos_input_field))
        
        ##########################################################
        self.Object_scale_title = QLabel(f"Object 1 Scale", self)

        self.Width_Obj_pos = QLabel("Width:", self)
        self.Width_Obj_pos_input_field = QLineEdit(parent=self)
        
        self.Width_Obj_pos_input_field.setText("0.0")
        
        self.W_slider = QtWidgets.QSlider(self)
        self.W_slider.setRange(0, 100)
        self.W_slider.setOrientation(QtCore.Qt.Horizontal)

        self.Height_Obj_pos = QLabel("Height:", self)
        self.Height_Obj_pos_input_field = QLineEdit(parent=self)
        self.Height_Obj_pos_input_field.setText("0.0")

        self.H_slider = QtWidgets.QSlider(self)
        self.H_slider.setRange(0, 100)
        self.H_slider.setOrientation(QtCore.Qt.Horizontal)
        
        self.Length_Obj_pos = QLabel("Length:", self)
        self.Length_Obj_pos_input_field = QLineEdit(parent=self)
        self.Length_Obj_pos_input_field.setText("0.0")

        self.L_slider = QtWidgets.QSlider(self)
        self.L_slider.setRange(0, 100)
        self.L_slider.setOrientation(QtCore.Qt.Horizontal)
        
        self.Width_Obj_pos_input_field.editingFinished.connect(lambda: self.Update_slider(self.W_slider, self.Width_Obj_pos_input_field.text()))
        self.Height_Obj_pos_input_field.editingFinished.connect(lambda: self.Update_slider(self.H_slider, self.Height_Obj_pos_input_field.text()))
        self.Length_Obj_pos_input_field.editingFinished.connect(lambda: self.Update_slider(self.L_slider, self.Length_Obj_pos_input_field.text()))

        # editingFinished callbacks that updates backend
        self.Width_Obj_pos_input_field.editingFinished.connect(self.update_object_scale)
        self.Height_Obj_pos_input_field.editingFinished.connect(self.update_object_scale)
        self.Length_Obj_pos_input_field.editingFinished.connect(self.update_object_scale)

        ########################################

        self.W_slider.sliderMoved.connect(lambda val: self.Slider_Update(val, self.Width_Obj_pos_input_field))
        self.H_slider.sliderMoved.connect(lambda val: self.Slider_Update(val, self.Height_Obj_pos_input_field))
        self.L_slider.sliderMoved.connect(lambda val: self.Slider_Update(val, self.Length_Obj_pos_input_field))
        
        ########################################

        self.Object_rotation_title = QLabel(f"Object 1 Rotation", self)

        self.X_Rotation_Label = QLabel("Roll:", self)
        self.X_Rotation_input_field = QLineEdit(parent=self)
        self.X_Rotation_input_field.setText("0.0")
        
        self.X_Rotation = QtWidgets.QSlider(self)
        
        self.X_Rotation.setOrientation(QtCore.Qt.Horizontal)
        self.X_Rotation.setRange(0, 360)
        
        self.Y_Rotation_Label = QLabel("Pitch:", self)
        self.Y_Rotation_input_field = QLineEdit(parent=self)
        self.Y_Rotation_input_field.setText("0.0")
        
        self.Y_Rotation = QtWidgets.QSlider(self)
        self.Y_Rotation.setOrientation(QtCore.Qt.Horizontal)
        self.Y_Rotation.setRange(0, 360)

        self.Z_Rotation_Label = QLabel("Yaw:", self)
        self.Z_Rotation_input_field = QLineEdit(parent=self)
        self.Z_Rotation_input_field.setText("0.0")
        
        self.Z_Rotation = QtWidgets.QSlider(self)
        self.Z_Rotation.setOrientation(QtCore.Qt.Horizontal)
        self.Z_Rotation.setRange(0, 360)
        
        self.X_Rotation_input_field.editingFinished.connect(lambda: self.Update_slider(self.X_Rotation, self.X_Rotation_input_field.text()))
        self.Y_Rotation_input_field.editingFinished.connect(lambda: self.Update_slider(self.Y_Rotation, self.Y_Rotation_input_field.text()))
        self.Z_Rotation_input_field.editingFinished.connect(lambda: self.Update_slider(self.Z_Rotation, self.Z_Rotation_input_field.text()))

        #########################################
        
        # editingFinished callbacks that updates backend
        self.X_Rotation_input_field.editingFinished.connect(self.update_object_rotation)
        self.Y_Rotation_input_field.editingFinished.connect(self.update_object_rotation)
        self.Z_Rotation_input_field.editingFinished.connect(self.update_object_rotation)
        
        self.X_Rotation.sliderMoved.connect(lambda val: self.Slider_Update(val, self.X_Rotation_input_field))
        self.Y_Rotation.sliderMoved.connect(lambda val: self.Slider_Update(val, self.Y_Rotation_input_field))
        self.Z_Rotation.sliderMoved.connect(lambda val: self.Slider_Update(val, self.Z_Rotation_input_field))
        
        #########################################

        # create initial combo_box
        self.combo_box = QComboBox(self)
        # connecting shared state updates to combo box
        shared_state.items_updated.connect(self.update_combo_box_items)
        shared_state.selection_changed.connect(self.combo_box.setCurrentIndex)
        self.combo_box.currentIndexChanged.connect(self.on_object_selected)

        # initialise items
        self.update_combo_box_items(shared_state.items)
        shared_state.update_items(items=[])
        shared_state.update_selected(0)
    
    def update_combo_box_items(self, items):
        """ Method could be called to update combo_box_items. Maybe Delete. """
        self.combo_box.clear()
        self.combo_box.addItems(map(lambda o: str(o), items))
        self.combo_box.activated.connect(self.update_label)

    def update_ui_by_config(self):
        """ Method that updates attributes in text field when the object index is change from combo box. """

        self.on_object_selected(0)
    
    
    def on_object_selected(self, selected_object_pos):
        """ Method that updates attributes in text field when the object index is change from combo box. """
        # find the corresponding object attributes from the backend
        selected_object = backend.get_config()["objects"][selected_object_pos]
        if (selected_object is None): return
        
        # disconnects text fields
        self.XObj_pos_input_field.editingFinished.disconnect(self.update_object_pos)
        self.YObj_pos_input_field.editingFinished.disconnect(self.update_object_pos)
        self.ZObj_pos_input_field.editingFinished.disconnect(self.update_object_pos)
        self.Width_Obj_pos_input_field.editingFinished.disconnect(self.update_object_scale)
        self.Height_Obj_pos_input_field.editingFinished.disconnect(self.update_object_scale)
        self.Length_Obj_pos_input_field.editingFinished.disconnect(self.update_object_scale)
        self.X_Rotation_input_field.editingFinished.disconnect(self.update_object_rotation)
        self.Y_Rotation_input_field.editingFinished.disconnect(self.update_object_rotation)
        self.Z_Rotation_input_field.editingFinished.disconnect(self.update_object_rotation)
        
        # sets the text as object attributes
        self.XObj_pos_input_field.setText(str(selected_object["pos"][0]))
        self.YObj_pos_input_field.setText(str(selected_object["pos"][2]))
        self.ZObj_pos_input_field.setText(str(selected_object["pos"][1]))
        self.Width_Obj_pos_input_field.setText(str(selected_object["sca"][0]))
        self.Height_Obj_pos_input_field.setText(str(selected_object["sca"][1]))
        self.Length_Obj_pos_input_field.setText(str(selected_object["sca"][2]))
        self.X_Rotation_input_field.setText(str(selected_object["rot"][0]))
        self.Y_Rotation_input_field.setText(str(selected_object["rot"][1]))
        self.Z_Rotation_input_field.setText(str(selected_object["rot"][2]))
        
        # reconnects text fields
        self.XObj_pos_input_field.editingFinished.connect(self.update_object_pos)
        self.YObj_pos_input_field.editingFinished.connect(self.update_object_pos)
        self.ZObj_pos_input_field.editingFinished.connect(self.update_object_pos)
        self.Width_Obj_pos_input_field.editingFinished.connect(self.update_object_scale)
        self.Height_Obj_pos_input_field.editingFinished.connect(self.update_object_scale)
        self.Length_Obj_pos_input_field.editingFinished.connect(self.update_object_scale)
        self.X_Rotation_input_field.editingFinished.connect(self.update_object_rotation)
        self.Y_Rotation_input_field.editingFinished.connect(self.update_object_rotation)
        self.Z_Rotation_input_field.editingFinished.connect(self.update_object_rotation)

        self.Update_slider(self.W_slider,self.Width_Obj_pos_input_field.text())
        self.Update_slider(self.H_slider,self.Height_Obj_pos_input_field.text())
        self.Update_slider(self.L_slider,self.Length_Obj_pos_input_field.text())
        self.Update_slider(self.X_Rotation,self.X_Rotation_input_field.text())
        self.Update_slider(self.Y_Rotation,self.Y_Rotation_input_field.text())
        self.Update_slider(self.Z_Rotation,self.Z_Rotation_input_field.text())
        
    
    def Update_slider(self, slider, val):
        try:
            slider.setValue(int(round(float(val), 0)))
        except Exception as e:
            try:
                slider.setValue(0)
            except:
                print("Error", e)

            
    def update_object_pos(self):
        """ Method to dynamically update a targetted object's position """
        try: 
            x = float(self.XObj_pos_input_field.text() or 0)
            z = float(self.ZObj_pos_input_field.text() or 0)
            y = float(self.YObj_pos_input_field.text() or 0)
                
            location = [x,z,y]
            
            # get the selected object's position from the combo box
            selected_object_index = self.combo_box.currentIndex()
            #call backend function   
            obj = shared_state.items[selected_object_index]
            #print(obj)
            obj.set_loc(location)
        except:
            print("Error Updating PosX, Y or Z value is invalid")
    
    def update_object_scale(self):
        """ Method to dynamically update a targetted object's scale """
        try: 
            width = float(self.Width_Obj_pos_input_field.text() or 0)
            height = float(self.Height_Obj_pos_input_field.text() or 0)
            length = float(self.Length_Obj_pos_input_field.text() or 0)
            scale = [width,height,length]
            
            # get the selected object's position from the combo box
            selected_object_index = self.combo_box.currentIndex()
            obj = shared_state.items[selected_object_index]
            #print(obj)
            obj.set_scale(scale)
        except:
            print("Error Updating Scale, Width, Height or Length value is invalid")
    
    def update_object_rotation(self):
        """ Method to dynamically update a targetted object's rotation """
        try: 
            x_rot = float(self.X_Rotation_input_field.text() or 0)
            y_rot = float(self.Y_Rotation_input_field.text() or 0)
            z_rot = float(self.Z_Rotation_input_field.text() or 0)
            
            rotation = [x_rot,y_rot,z_rot]
            
            # get the selected object's position from the combo box
            selected_object_index = self.combo_box.currentIndex()
            obj = shared_state.items[selected_object_index]
            #print(obj)
            obj.set_rotation(rotation)
        except:
            print("Error Updating Rotation, X, Y or Z value is invalid")
    
    
    def Plus_click(self, field):
        """Updates field value"""
        try:
            val = float(field.text()) + 1
            field.setText(str(val))
            field.editingFinished.emit()
        except:
            field.setText(str(0.0))
            field.editingFinished.emit()
        
        
    def Minus_click(self, field):
        """Updates field value"""
        try:
            val = float(field.text()) - 1
            field.setText(str(val))
            field.editingFinished.emit()
        except:
            field.setText(str(0.0))
            field.editingFinished.emit()
            
    def Slider_Update(self, val, field):
        """Set Field value to slider value"""
        field.setText(str(val))
        
    def update_label(self):
        """Updates labels on object change"""
        AllItems = [self.combo_box.itemText(i) for i in range(self.combo_box.count())]
        n = self.combo_box.currentIndex()
        Title = AllItems[n]
        self.Object_pos_title.setText(f"{Title} Co-ords")
        self.Object_scale_title.setText(f"{Title} Scale")
        self.Object_rotation_title.setText(f"{Title} Rotation")


    def resizeEvent(self, event):
    
        """
        Handles window resize event to dynamically change styling
        :
            - Object Position:
                - Object_pos_title: Label for object position.
                - XObj_pos, YObj_pos, ZObj_pos: Labels for X Y Z positions
                - XObj_pos_input_field, YObj_pos_input_field, ZObj_pos_input_field - Input for X Y Z positions.
                - X_button_minus/plus, Y_button_minus/plus, Z_button_minus/plus - Buttons to increase/decrease X Y Z positions.
            
            - Object Scale:
                - Object_scale_title: Label for object scale.
                - Width_Obj_pos, Height_Obj_pos, Length_Obj_pos: Labels for width, 
                height, and length scales.
                - Width_Obj_pos_input_field, Height_Obj_pos_input_field, 
                Length_Obj_pos_input_field: Input fields for width, height, 
                length scales.
                - W_slider, H_slider, L_slider: Sliders for width, height, and length.
            
            - Object Rotation:
                - Object_rotation_title: Label for object rotation.
                - X_Rotation_Label, Y_Rotation_Label, Z_Rotation_Label: Labels for 
                rotation on X, Y, Z axes.
                - X_Rotation_input_field, Y_Rotation_input_field, Z_Rotation_input_field:
                Input fields for rotation on X, Y, Z axes.
                - X_Rotation, Y_Rotation, Z_Rotation: Sliders for rotation on X, Y, Z axes.
            
            - combo_box: Dropdown menu for object selection, anchored to the top-right.
        
          """
    
        self.Object_pos_title.setGeometry(int(self.width()*0.01), int(self.height()*0.01), 200, 30)

        self.XObj_pos.setGeometry(int(self.width()*0.01), int(self.height()*0.25),15, 30)
        self.XObj_pos_input_field.setGeometry(int(self.width()*0.03), int(self.height()*0.25), int(self.width()*0.1), 20)
        
        self.X_button_minus.setGeometry(int(self.width()*0.13), int(self.height()*0.25), int(self.width()*0.025), 20)
        self.X_button_plus.setGeometry(int(self.width()*0.13+int(self.width()*0.025)), int(self.height()*0.25), int(self.width()*0.025), 20)

        self.YObj_pos.setGeometry(int(self.width()*0.01), int(self.height()*0.50),15, 30)
        self.YObj_pos_input_field.setGeometry(int(self.width()*0.03), int(self.height()*0.5), int(self.width()*0.1), 20)

        self.Y_button_minus.setGeometry(int(self.width()*0.13), int(self.height()*0.50), int(self.width()*0.025), 20)
        self.Y_button_plus.setGeometry(int(self.width()*0.13+int(self.width()*0.025)), int(self.height()*0.50), int(self.width()*0.025), 20)

        self.ZObj_pos.setGeometry(int(self.width()*0.01), int(self.height()*0.75),15, 30)
        self.ZObj_pos_input_field.setGeometry(int(self.width()*0.03), int(self.height()*0.75), int(self.width()*0.1), 20)

        self.Z_button_minus.setGeometry(int(self.width()*0.13), int(self.height()*0.75), int(self.width()*0.025), 20)
        self.Z_button_plus.setGeometry(int(self.width()*0.13+int(self.width()*0.025)), int(self.height()*0.75), int(self.width()*0.025), 20)
    

        ##########################################################

        self.Object_scale_title.setGeometry(int(self.width()*0.20), int(self.height()*0.01), 200, 30)

        self.Width_Obj_pos.setGeometry(int(self.width()*0.20), int(self.height()*0.2), 50, 30)
        self.Width_Obj_pos_input_field.setGeometry(int(self.width()*0.25), int(self.height()*0.25), int(self.width()*0.1), 20)
        self.W_slider.setGeometry(QtCore.QRect(int(self.width()*0.38), int(self.height()*0.28), int(self.width()*0.2), 16))

        self.Height_Obj_pos.setGeometry(int(self.width()*0.20), int(self.height()*0.45), 50, 30)
        self.Height_Obj_pos_input_field.setGeometry(int(self.width()*0.25), int(self.height()*0.5), int(self.width()*0.1), 20)
        self.H_slider.setGeometry(QtCore.QRect(int(self.width()*0.38), int(self.height()*0.52), int(self.width()*0.2), 16))

        self.Length_Obj_pos.setGeometry(int(self.width()*0.20), int(self.height()*0.7), 50, 30)
        self.Length_Obj_pos_input_field.setGeometry(int(self.width()*0.25), int(self.height()*0.75), int(self.width()*0.1), 20)
        self.L_slider.setGeometry(QtCore.QRect(int(self.width()*0.38), int(self.height()*0.77), int(self.width()*0.2), 16))

        ################################################################


        self.Object_rotation_title.setGeometry(int(self.width()*0.60), int(self.height()*0.01), 200, 30)
        self.X_Rotation_Label.setGeometry(int(self.width()*0.60), int(self.height()*0.2), 50, 30)
        self.X_Rotation_input_field.setGeometry(int(self.width()*0.65), int(self.height()*0.25), int(self.width()*0.1), 20)
        self.X_Rotation.setGeometry(QtCore.QRect(int(self.width()*0.78), int(self.height()*0.28), int(self.width()*0.2), 16))

        self.Y_Rotation_Label.setGeometry(int(self.width()*0.60), int(self.height()*0.45), 50, 30)
        self.Y_Rotation_input_field.setGeometry(int(self.width()*0.65), int(self.height()*0.5), int(self.width()*0.1), 20)
        self.Y_Rotation.setGeometry(QtCore.QRect(int(self.width()*0.78), int(self.height()*0.52), int(self.width()*0.2), 16))

        self.Z_Rotation_Label.setGeometry(int(self.width()*0.60), int(self.height()*0.7), 50, 30)
        self.Z_Rotation_input_field.setGeometry(int(self.width()*0.65), int(self.height()*0.75), int(self.width()*0.1), 20)
        self.Z_Rotation.setGeometry(QtCore.QRect(int(self.width()*0.78), int(self.height()*0.77), int(self.width()*0.2), 16))

        ###############################################################
        self.combo_box.setGeometry(self.width()-self.combo_box.width(), 0, self.combo_box.width(), self.combo_box.height())

class Page2(Page):
    """
    Page 2: Pivot Point
    """

    def __init__(self, parent=None):
        """
        Initialise "Page n"


        """
        super().__init__(parent)

        # Pivot Point Coords Section
        self.Pivot_Point_Check = QCheckBox("Cutom Pivot Point", self)
        self.Pivot_Point_Check.setLayoutDirection(Qt.LayoutDirection.RightToLeft)
        self.Pivot_Point_Check.setChecked(True)
        self.Pivot_Point_Check.stateChanged.connect(lambda: self.state_changed(self.Pivot_Point_Check, [self.XPivot_point_input_field, self.YPivot_point_input_field, self.ZPivot_point_input_field], [self.XPivot_button_minus, self.XPivot_button_plus, self.YPivot_button_minus, self.YPivot_button_plus,self.ZPivot_button_plus, self.ZPivot_button_minus]))

        # X Pivot Point Controls
        self.XPivot_pos = QLabel("X:", self)
        self.XPivot_point_input_field = QLineEdit(parent=self)
        self.XPivot_point_input_field.setText("0.0")
        self.XPivot_button_minus = QPushButton('-', self)
        self.XPivot_button_plus = QPushButton('+', self)
        
        ###################
        self.XPivot_button_plus.clicked.connect(lambda: self.Plus_click(self.XPivot_point_input_field))
        self.XPivot_button_minus.clicked.connect(lambda: self.Minus_click(self.XPivot_point_input_field))
        ###################

        # Y Pivot Point Controls
        self.YPivot_pos = QLabel("Y:", self)
        self.YPivot_point_input_field = QLineEdit(parent=self)
        self.YPivot_point_input_field.setText("0.0")
        self.YPivot_button_minus = QPushButton('-', self)
        self.YPivot_button_plus = QPushButton('+', self)
        
        ###################
        self.YPivot_button_plus.clicked.connect(lambda: self.Plus_click(self.YPivot_point_input_field))
        self.YPivot_button_minus.clicked.connect(lambda: self.Minus_click(self.YPivot_point_input_field))
        ###################

        # Z Pivot Point Controls
        self.ZPivot_pos = QLabel("Z:", self)
        self.ZPivot_point_input_field = QLineEdit(parent=self)
        self.ZPivot_point_input_field.setText("0.0")
        self.ZPivot_button_minus = QPushButton('-', self)
        self.ZPivot_button_plus = QPushButton('+', self)
        
        ###################
        self.ZPivot_button_plus.clicked.connect(lambda: self.Plus_click(self.ZPivot_point_input_field))
        self.ZPivot_button_minus.clicked.connect(lambda: self.Minus_click(self.ZPivot_point_input_field))
        ###################

        # Angle Change Section        
        self.Distance_Pivot = QLabel("Distance:", self)
        self.Distance_Pivot_input_field = QLineEdit(parent=self)
        self.Distance_Pivot_input_field.setText("0")
        
        self.Distance_Slider = QtWidgets.QSlider(self)
        self.Distance_Slider.setOrientation(QtCore.Qt.Horizontal)
        self.Distance_Slider.setRange(0, 100)

        self.Distance_Pivot_input_field.editingFinished.connect(lambda: self.Update_slider(self.Distance_Slider, self.Distance_Pivot_input_field.text()))
        self.Distance_Pivot_input_field.setText("0")
        
        #################
        self.Distance_Slider.sliderMoved.connect(lambda: self.Slider_Update(self.Distance_Pivot_input_field))
        #################
        
        ################### 
        # editingFinished callbacks that updates backend
        self.XPivot_point_input_field.editingFinished.connect(self.update_pivot)
        self.YPivot_point_input_field.editingFinished.connect(self.update_pivot)
        self.ZPivot_point_input_field.editingFinished.connect(self.update_pivot)

        
        ################
        # create initial combo_box
        self.combo_box = QComboBox(self)
        # connecting shared state updates to combo box
        shared_state.items_updated.connect(self.update_combo_box_items)
        shared_state.selection_changed.connect(self.combo_box.setCurrentIndex)
        self.combo_box.activated.connect(lambda: self.Object_pivot_selected(self.Pivot_Point_Check, [self.XPivot_point_input_field, self.YPivot_point_input_field, self.ZPivot_point_input_field], [self.XPivot_button_minus, self.XPivot_button_plus, self.YPivot_button_minus, self.YPivot_button_plus,self.ZPivot_button_plus, self.ZPivot_button_minus]))
        
        # initialise items
        self.update_combo_box_items(shared_state.items)
        shared_state.update_items(items=[])
        shared_state.update_selected(0)

    def update_ui_by_config(self):
        """ Method that updates attributes in text field when the object index is change from combo box. """

        cfg = backend.get_config()

        # disconnects text fields
        self.Distance_Pivot_input_field.editingFinished.disconnect()
        self.XPivot_point_input_field.editingFinished.disconnect()
        self.YPivot_point_input_field.editingFinished.disconnect()
        self.ZPivot_point_input_field.editingFinished.disconnect()
        self.Pivot_Point_Check.stateChanged.disconnect()
        self.combo_box.activated.disconnect()
        
        self.Distance_Pivot_input_field.setText(str(cfg["pivot"]["dis"]))
        self.XPivot_point_input_field.setText(str(cfg["pivot"]["point"][0]))
        self.YPivot_point_input_field.setText(str(cfg["pivot"]["point"][1]))
        self.ZPivot_point_input_field.setText(str(cfg["pivot"]["point"][2]))
        self.Pivot_Point_Check.setChecked(True)
        self.combo_box.setCurrentIndex(-1)
        if cfg["objects"] != []:
            self.combo_box.setCurrentIndex(0)
            
        # reconnects text fields
        self.Distance_Pivot_input_field.editingFinished.connect(lambda: self.Update_slider(self.Distance_Slider, self.Distance_Pivot_input_field.text()))
        self.XPivot_point_input_field.editingFinished.connect(self.update_pivot)
        self.YPivot_point_input_field.editingFinished.connect(self.update_pivot)
        self.ZPivot_point_input_field.editingFinished.connect(self.update_pivot)
        self.Pivot_Point_Check.stateChanged.connect(lambda: self.state_changed(self.Pivot_Point_Check, [self.XPivot_point_input_field, self.YPivot_point_input_field, self.ZPivot_point_input_field], [self.XPivot_button_minus, self.XPivot_button_plus, self.YPivot_button_minus, self.YPivot_button_plus,self.ZPivot_button_plus, self.ZPivot_button_minus]))
        self.combo_box.activated.connect(lambda: self.Object_pivot_selected(self.Pivot_Point_Check, [self.XPivot_point_input_field, self.YPivot_point_input_field, self.ZPivot_point_input_field], [self.XPivot_button_minus, self.XPivot_button_plus, self.YPivot_button_minus, self.YPivot_button_plus,self.ZPivot_button_plus, self.ZPivot_button_minus]))

        self.Update_slider(self.Distance_Slider, self.Distance_Pivot_input_field.text())
        
        
    def Update_slider(self, slider, val):
        try:
            slider.setValue(int(round(float(val), 0)))
        except Exception as e:
            try:
                slider.setValue(0)
            except:
                print("Error", e)
            
    def Slider_Update(self, field):
        """Sets field value to slider value"""
        val = self.Distance_Slider.value()
        field.setText(str(val))
        
    def Object_pivot_selected(self, Check, Fields, Buttons):
        "Set checkbox and associsated Fields and buttons False"
        Check.setChecked(False)
        self.able_Fields(Fields, Buttons, True)

    def state_changed(self, Pivot_Point_Check, Fields, Buttons):
        "Detects if State of checkbox has changed"
        if Pivot_Point_Check.isChecked():
            self.able_Fields(Fields, Buttons, False)
        else:
            self.able_Fields(Fields, Buttons, True)
    
    def able_Fields(self, Fields, Buttons, State):
        "Sets all fields and buttons specified to Desired state"
        for i in range(len(Fields)):
            Fields[i].setDisabled(State)
            
        for i in range(len(Buttons)):
            Buttons[i].blockSignals(State) 
    
    def update_combo_box_items(self, items):
        """ Method could be called to update combo_box_items. Maybe Delete. """
        self.combo_box.clear()
        self.combo_box.addItems(map(lambda o: str(o), items))
        self.Distance_Pivot_input_field.editingFinished.connect(self.update_distance)
    
    def update_pivot(self):
        """ Method to dynamically update a targetted object's position """
        try: 
            x = float(self.XPivot_point_input_field.text() or 0)
            y = float(self.YPivot_point_input_field.text() or 0)
            z = float(self.ZPivot_point_input_field.text() or 0)
                
            point = [x,y,z]
            backend.set_pivot_point(point)
        except:
            print("Error Updating Pivot, X, Y or Z value is invalid")
            
    def update_distance(self):
        """ Method to dynamically update a targetted object's position """
        try: 
            dis = float(self.Distance_Pivot_input_field.text() or 0)
            backend.set_pivot_distance(dis)
        except:
            print("Error Updating Distance, You entered an invalid input.")
    
    
    def Plus_click(self, field):
        """Updates Field value"""
        try:
            val = float(field.text()) + 1
            field.setText(str(val))
            field.editingFinished.emit()
        except:
            field.setText(str(0.0))
            field.editingFinished.emit()
        
        
    def Minus_click(self, field):
        """Updates Field value"""
        try:
            val = float(field.text()) - 1
            field.setText(str(val))
            field.editingFinished.emit()
        except:
            field.setText(str(0.0))
            field.editingFinished.emit()

    def resizeEvent(self, event):
            
        """
        Handles window resize event

        :
                -Pivot Position
                -   Pivot_point_subtitle
                -   XPivot_pos
                -   XPivot
                -   XPivot_button_minus
                -   XPivot_button_plus
                
                -   YPivot_pos
                -   YPivot_point_input_field
                -   YPivot_button_minus
                -   YPivot_button_plus
            

                -   ZPivot_pos
                -   ZPivot_point_input_field
                -   ZPivot_button_minus
                -   ZPivot_button_plus

            -Degree of Angle Change
                -   Angle_change_title
                -   Degrees_pivot
                -   Degrees_pivot_input_field
                -   Degrees_Slider

            -Number of rotaions
                -   Num_Rotations
                -   Num_Rotations_input_field
                -   Num_Rotations_minus
                -   Num_Rotations_plus
            
        """

        
        # Title Position
        self.Pivot_Point_Check.setGeometry(int(self.width() * 0.01), int(self.height() * 0.00), 120, 30)

        # X Pivot Point
        self.XPivot_pos.setGeometry(int(self.width() * 0.05), int(self.height() * 0.2), 20, 30)
        self.XPivot_point_input_field.setGeometry(int(self.width() * 0.1), int(self.height() * 0.2), int(self.width() * 0.1), 20)
        self.XPivot_button_minus.setGeometry(int(self.width() * 0.22), int(self.height() * 0.2), 25, 20)
        self.XPivot_button_plus.setGeometry(int(self.width() * 0.25), int(self.height() * 0.2), 25, 20)

        # Y Pivot Point
        self.YPivot_pos.setGeometry(int(self.width() * 0.05), int(self.height() * 0.5), 20, 30)
        self.YPivot_point_input_field.setGeometry(int(self.width() * 0.1), int(self.height() * 0.5), int(self.width() * 0.1), 20)
        self.YPivot_button_minus.setGeometry(int(self.width() * 0.22), int(self.height() * 0.5), 25, 20)
        self.YPivot_button_plus.setGeometry(int(self.width() * 0.25), int(self.height() * 0.5), 25, 20)

        # Z Pivot Point
        self.ZPivot_pos.setGeometry(int(self.width() * 0.05), int(self.height() * 0.8), 20, 30)
        self.ZPivot_point_input_field.setGeometry(int(self.width() * 0.1), int(self.height() * 0.8), int(self.width() * 0.1), 20)
        self.ZPivot_button_minus.setGeometry(int(self.width() * 0.22), int(self.height() * 0.8), 25, 20)
        self.ZPivot_button_plus.setGeometry(int(self.width() * 0.25), int(self.height() * 0.8), 25, 20)

        # Degrees
        self.Distance_Pivot.setGeometry(int(self.width() * 0.30), int(self.height() * 0.01), 150, 30)
        self.Distance_Pivot_input_field.setGeometry(int(self.width() * 0.30), int(self.height() * 0.2), int(self.width() * 0.1), 20)
        self.Distance_Slider.setGeometry(QtCore.QRect(int(self.width() * 0.425), int(self.height() * 0.21), int(self.width() * 0.3), 16))
        
        self.combo_box.setGeometry(self.width()-self.combo_box.width(), 0, self.combo_box.width(), self.combo_box.height())

        super().resizeEvent(event)  # Call the parent class's resizeEvent

class Page3(Page):
    """
    Page 3: Generate Random
    """
    def __init__(self, parent=None, ):

        """
        Initialise "Page n"
        
        generate random variables for objects and coords
            
        Args:

        Methods:
            __init__(parent=None) - Initializes the page, setting up all UI components.                
            resizeEvent(event) -  Adjusts component positions on window resize.
            decrease_count() -  Decreases the number of renders.
            set_all_random(state) -  Sets all randomization checkboxes based on the state.

        """

        super().__init__(parent)
        

        

        # First Section
        self.Set_All_Random_Button = QCheckBox("Set all Random", self)
        self.Set_All_Random_Button.setLayoutDirection(Qt.LayoutDirection.RightToLeft)
        self.Set_All_Random_Button.setGeometry(0, 0, 125, 30)
        self.Set_All_Random_Button.stateChanged.connect(self.set_all_random)

        # Second Section
        self.ObjectDimensions_Label = QLabel(f"Object Dimensions", self)
        self.ObjectDimensions_Label.setGeometry(150, 10, 125, 20)
        
        self.Width_Button = QCheckBox("Width", self)
        self.Width_Button.setGeometry(150, 30, 65, 20)
        self.Width_Button.toggled.connect(self.on_width_toggle)


        #if checked then change value of width text 

        self.Height_Button = QCheckBox("Height", self)
        self.Height_Button.setGeometry(150, 50, 65, 20)
        self.Height_Button.toggled.connect(self.on_height_toggle)


        self.Length_Button = QCheckBox("Length", self)
        self.Length_Button.setGeometry(150, 70, 65, 20)
        self.Length_Button.toggled.connect(self.on_length_toggle)



        #Third Section
        self.Object_Coords_Label = QLabel(f"Object x Co-ords:", self)
        self.Object_Coords_Label.setGeometry(275, 10, 100, 20)

        self.X_Button = QCheckBox("X", self)
        self.X_Button.setGeometry(215, 50, 30, 20)
        self.X_Button.toggled.connect(self.on_x_toggle)


        self.Y_Button = QCheckBox("Y", self)
        self.Y_Button.setGeometry(315, 50, 30, 20)
        self.Y_Button.toggled.connect(self.on_y_toggle)


        self.Z_Button = QCheckBox("Z", self)
        self.Z_Button.setGeometry(250, 50, 30, 20)
        self.Z_Button.toggled.connect(self.on_z_toggle)


        self.PivotPoint_Label = QLabel(f"Pivot Point Co-ords:", self)
        self.PivotPoint_Label.setGeometry(275, 50, 120, 20)

        self.X_Button2 = QCheckBox("X", self)
        self.X_Button2.setLayoutDirection(Qt.LayoutDirection.RightToLeft)
        self.X_Button2.setGeometry(275, 70, 30, 20)
        self.X_Button2.stateChanged.connect(backend.toggle_random_pivot_x)

        self.Y_Button2 = QCheckBox("Y", self)
        self.Y_Button2.setLayoutDirection(Qt.LayoutDirection.RightToLeft)
        self.Y_Button2.setGeometry(315, 70, 30, 20)
        self.Y_Button2.stateChanged.connect(backend.toggle_random_pivot_y)

        self.Z_Button2 = QCheckBox("Z", self)
        self.Z_Button2.setLayoutDirection(Qt.LayoutDirection.RightToLeft)
        self.Z_Button2.setGeometry(350, 70, 30, 20)
        self.Z_Button2.stateChanged.connect(backend.toggle_random_pivot_z)

        #Fourth Section
        self.AutoRotationAngle_Label = QLabel(f"Auto Rotation Angle:", self)
        self.AutoRotationAngle_Label.setGeometry(450, 30, 150, 20)
        

        self.AutoRotationAngle_Button = QCheckBox("", self)
        self.AutoRotationAngle_Button.setGeometry(560, 30, 150, 20)
        self.AutoRotationAngle_Button.stateChanged.connect(backend.toggle_random_environment_angle)

        self.ImportEnvironment_Label = QLabel(f"Import Environment:", self)
        self.ImportEnvironment_Label.setGeometry(450, 70, 150, 20)

        self.ImportEnvironment_Button = QCheckBox("", self)
        self.ImportEnvironment_Button.setGeometry(560, 70, 150, 20)
        self.ImportEnvironment_Button.stateChanged.connect(backend.toggle_random_environment_background)

        #Section 5
        
        self.RandomSettingSeed_Label = QLabel(f"Random  Seed", self)
        self.RandomSeed_Label = QLabel(f"<Random Seed>", self)
        self.RandomSeed_Label.setText(str(backend.get_config()["seed"]))


        #Third Section
        self.object_toggle_states = {}
        self.combo_box = QComboBox(self)
        self.combo_box.setGeometry(200, 150, 200, 30)
        #self.combo_box.addItems()
        
        shared_state.items_updated.connect(self.update_combo_box_items)
        shared_state.selection_changed.connect(self.combo_box.setCurrentIndex)
        self.combo_box.activated.connect(lambda: self.object_selected())

        self.update_combo_box_items(shared_state.items)
        shared_state.update_items(items=[]) 
        shared_state.update_selected(0)    

    def update_combo_box_items(self, items):
        """Update the combo box with the latest shared state items."""
        self.combo_box.clear()
        self.combo_box.addItems(map(lambda o: str(o), items))


    def object_selected(self):
        """Handle object selection from the combo box."""
        
        selected_index = self.combo_box.currentIndex()
        self.reset_toggle_states()

        #self.restore_states()

    def reset_toggle_states(self):
        """Reset all toggle states to unchecked state."""        
        self.Width_Button.blockSignals(True)
        self.Height_Button.blockSignals(True)
        self.Length_Button.blockSignals(True)
        self.X_Button.blockSignals(False)
        self.Y_Button.blockSignals(False)
        self.Z_Button.blockSignals(False)

        self.Width_Button.setChecked(False)
        self.Height_Button.setChecked(False)
        self.Length_Button.setChecked(False)
        self.X_Button.setChecked(False)
        self.Y_Button.setChecked(False)
        self.Z_Button.setChecked(False)
        
        self.Width_Button.blockSignals(False)
        self.Height_Button.blockSignals(False)
        self.Length_Button.blockSignals(False)
        self.X_Button.blockSignals(False)
        self.Y_Button.blockSignals(False)
        self.Z_Button.blockSignals(False)

    def on_width_toggle(self):
        selected_index = self.combo_box.currentIndex()
        if selected_index is not None:
            backend.toggle_random_width(selected_index)

    def on_height_toggle(self):
        selected_index = self.combo_box.currentIndex()
        if selected_index is not None:
            backend.toggle_random_height(selected_index)

    def on_length_toggle(self):
        selected_index = self.combo_box.currentIndex()
        if selected_index is not None:
            backend.toggle_random_length(selected_index)

    def on_x_toggle(self):
        selected_index = self.combo_box.currentIndex()
        if selected_index is not None:
            backend.toggle_random_coord_x(selected_index)

    def on_y_toggle(self):
        selected_index = self.combo_box.currentIndex()
        if selected_index is not None:
            backend.toggle_random_coord_y(selected_index)

    def on_z_toggle(self):
        selected_index = self.combo_box.currentIndex()
        if selected_index is not None:
            backend.toggle_random_coord_z(selected_index)




    def resizeEvent(self, event):


        """
        Handles window resize event

        Args:
            - Random Object Dimensions
                -   Object_Dimensions_Label
                -   Width_button
                -   Height_button
                -   Length
            - Random Object Co-ords
                -   X_button
                -   Y_button
                -   Z_button

            - Random Pivot Point Co-ords
                -   PivotPoint_Label
                -   X_Button2
                -   Y_Button2
                -   Z_Button2


            - Random Properties
                -   Reflect_Label
                -   Reflect_Button
                -?
                -?

            - Titles and Text
                -   RandomSettingSeed_Label
                -   RandomSeed_Label
                -   

            """
        window_width = self.width()
        window_height = self.height()
        
        # First Section
        self.Set_All_Random_Button.setGeometry(int(window_width * 0), int(window_height * 0.02), int(window_width * 0.12), 20)
        

        # Second Section
        self.ObjectDimensions_Label.setGeometry(int(window_width * 0.15), int(window_height * 0.02), int(window_width * 0.2), 20)


        self.Width_Button.setGeometry(int(window_width * 0.15), int(window_height * 0.3), int(window_width * 0.15), 20)
        self.Height_Button.setGeometry(int(window_width * 0.22), int(window_height * 0.3), int(window_width * 0.15), 20)
        self.Length_Button.setGeometry(int(window_width * 0.29), int(window_height * 0.3), int(window_width * 0.15), 20)


        # Third Section
        self.combo_box.setGeometry(int(window_width * 0.01), int(window_height * 0.3), int(window_width * 0.12), 20)
        
        self.X_Button.setGeometry(int(window_width * 0.15), int(window_height * 0.6), 30, 20)
        self.Y_Button.setGeometry(int(window_width * 0.22), int(window_height * 0.60), 30, 20)
        self.Z_Button.setGeometry(int(window_width * 0.29), int(window_height * 0.60), 30, 20)
        
        self.PivotPoint_Label.setGeometry(int(window_width * 0.40), int(window_height * 0.02), int(window_width * 0.2), 20)
        self.X_Button2.setGeometry(int(window_width * 0.38), int(window_height * 0.3), 30, 20)
        self.Y_Button2.setGeometry(int(window_width * 0.45), int(window_height * 0.3), 30, 20)
        self.Z_Button2.setGeometry(int(window_width * 0.52), int(window_height * 0.3), 30, 20)
        
        # Fourth Section

        self.AutoRotationAngle_Label.setGeometry(int(window_width * 0.6), int(window_height * 0.3), int(window_width * 0.2), 20)
        self.AutoRotationAngle_Button.setGeometry(int(window_width * 0.73), int(window_height * 0.32), 30, 20)

        self.ImportEnvironment_Label.setGeometry(int(window_width * 0.6), int(window_height * 0.7), int(window_width * 0.2), 20)
        self.ImportEnvironment_Button.setGeometry(int(window_width * 0.73), int(window_height * 0.72), 30, 20)

        # Fifth Section
        x = max(self.RandomSeed_Label.width(), 125)  # Minimum width for RandomSettingSeed_Label
        self.RandomSettingSeed_Label.setGeometry(window_width - x - 10, int(window_height * 0.02), x, 20)
        self.RandomSeed_Label.setGeometry(window_width - self.RandomSeed_Label.width() - 10, int(window_height * 0.2), self.RandomSeed_Label.width(), 20)

    def update_ui_by_config(self):
        """ Method that updates attributes in text field when the object index is change from combo box. """

        cfg = backend.get_config()

        self.RandomSeed_Label.setText(str(cfg["seed"]))
        '''self.Width_Button.setChecked(random_cfg[])
        self.Height_Button.setChecked(is_checked)
        self.Length_Button.setChecked(is_checked)
        self.X_Button.setChecked(is_checked)
        self.Y_Button.setChecked(is_checked)
        self.Z_Button.setChecked(is_checked)
        self.X_Button2.setChecked(is_checked)
        self.Y_Button2.setChecked(is_checked)
        self.Z_Button2.setChecked(is_checked)
        self.AutoRotationAngle_Button.setChecked(is_checked)
        self.ImportEnvironment_Button.setChecked(is_checked)
        self.combo_box.setCurrentIndex(0)'''
    
    def set_all_random(self, state):
        is_checked = state == Qt.Checked
        self.Width_Button.setChecked(is_checked)
        self.Height_Button.setChecked(is_checked)
        self.Length_Button.setChecked(is_checked)
        self.X_Button.setChecked(is_checked)
        self.Y_Button.setChecked(is_checked)
        self.Z_Button.setChecked(is_checked)
        self.X_Button2.setChecked(is_checked)
        self.Y_Button2.setChecked(is_checked)
        self.Z_Button2.setChecked(is_checked)
        self.AutoRotationAngle_Button.setChecked(is_checked)
        self.ImportEnvironment_Button.setChecked(is_checked)

class RenderThread(QThread):
    finished = pyqtSignal()
    progress = pyqtSignal(str)

    def run(self):
        self.progress.emit("Rendering...")
        backend.render(headless = True)
        self.finished.emit()
        
class LoadingScreen(QDialog):
    def __init__(self, text, parent=None):
        super().__init__(parent)


        self.setWindowTitle("Rendering...")
        self.setWindowModality(Qt.NonModal)
        self.setGeometry(250, 250, 250, 200)

        layout = QVBoxLayout()
        self.label = QLabel(text)
        layout.addWidget(self.label)

        self.setLayout(layout)

    def update_text(self, text):
        self.label.setText(text)


class Page4(Page):
    """
    Page 4: Render
        
        Generate Renders

        Args:
            GenerateRenders_Button - QPushButton - Button for Generating Renders
            Number_of_renders_title - QLabel - Title for number of renders
            Number_of_renders_input_field - QLineEdit - Field to input number of renders
            Number_of_renders_minus - QPushButton -  Button to decrease number of renders
            Number_of_renders_plus - QPushButton - Button to increase number of renders
            Degree_Change_title - QLabel: Title for degrees of change section
            X_Degree_Label, Y_Degree_Label, Z_Degree_Label - QLabel -  Text for angles of rotation 
            X_Degree_input_field, Y_Degree_input_field, Z_Degree_input_field - QLineEdit - Fields to input degree values
            X_Degree_slider, Y_Degree_slider, Z_Degree_slider - QSlider - Sliders to adjust rotation angles
            
        Methods:
            __init__(parent=None)
            increase_count() - Increases number of renders for buttons
            decrease_count() - Decreases number of renders for buttons
            update_degree_input(slider, input_field) - Updates degree input
            resizeEvent(event) - handles resize event
        """

    def __init__(self, parent=None):
        """
        Initialize Page 4
        """
        super().__init__(parent)

        self.GenerateRenders_Button = QPushButton('Generate Renders', self)
        self.GenerateRenders_Button.clicked.connect(self.generate_render)
        self.GenerateRenders_Button.setGeometry(0, 10, 125, 50)
        


        # Number of Renders input fields
        self.Number_of_renders_title = QLabel("Number of Renders", self)
        self.Number_of_renders_input_field = QLineEdit(parent=self)
        self.Number_of_renders_input_field.setText("1")
        self.Number_of_renders_input_field.editingFinished.connect(self.set_renders)

        self.Number_of_renders_minus = QPushButton('-', self)
        self.Number_of_renders_plus = QPushButton('+', self)

        self.Number_of_renders_minus.clicked.connect(self.decrease_count)
        self.Number_of_renders_plus.clicked.connect(self.increase_count)




        self.Degree_Change_title = QLabel("Degrees of Change", self)

        # X Degree
        self.X_Degree_Label = QLabel("X:", self)
        self.X_Degree_input_field = QLineEdit(parent=self)
        self.X_Degree_input_field.setText("1")
        self.X_Degree_input_field.editingFinished.connect(self.set_angles)
        self.X_Degree_slider = QtWidgets.QSlider(self)
        self.X_Degree_slider.setOrientation(QtCore.Qt.Horizontal)
        self.X_Degree_slider.setMinimum(1) 
        self.X_Degree_slider.setMaximum(360) 
        self.X_Degree_slider.setTickPosition(QSlider.TicksBelow)
        


        # Y Degree
        self.Y_Degree_Label = QLabel("Y:", self)
        self.Y_Degree_input_field = QLineEdit(parent=self)
        self.Y_Degree_slider = QtWidgets.QSlider(self)
        self.Y_Degree_input_field.setText("1")
        self.Y_Degree_input_field.editingFinished.connect(self.set_angles)
        self.Y_Degree_slider.setOrientation(QtCore.Qt.Horizontal)
        self.Y_Degree_slider.setMinimum(1)
        self.Y_Degree_slider.setMaximum(360)
        self.Y_Degree_slider.setTickPosition(QSlider.TicksBelow)


        # Z Degree
        self.Z_Degree_Label = QLabel("Z:", self)
        self.Z_Degree_input_field = QLineEdit(parent=self)
        self.Z_Degree_input_field.setText("1")
        self.Z_Degree_input_field.editingFinished.connect(self.set_angles)
        self.Z_Degree_slider = QtWidgets.QSlider(self)
        self.Z_Degree_slider.setOrientation(QtCore.Qt.Horizontal)
        self.Z_Degree_slider.setMinimum(1)
        self.Z_Degree_slider.setMaximum(360)
        self.Z_Degree_slider.setTickPosition(QSlider.TicksBelow)


        self.X_Degree_slider.sliderMoved.connect(lambda: self.update_degree_input(self.X_Degree_slider, self.X_Degree_input_field))
        self.Y_Degree_slider.sliderMoved.connect(lambda: self.update_degree_input(self.Y_Degree_slider, self.Y_Degree_input_field))
        self.Z_Degree_slider.sliderMoved.connect(lambda: self.update_degree_input(self.Z_Degree_slider, self.Z_Degree_input_field))


        self.rendering = False

    def update_ui_by_config(self):
        """ Method that updates attributes in text field when the object index is change from combo box. """

        cfg = backend.get_config()

        self.X_Degree_input_field.editingFinished.disconnect()
        self.Y_Degree_input_field.editingFinished.disconnect()
        self.Z_Degree_input_field.editingFinished.disconnect()
        self.Number_of_renders_input_field.editingFinished.disconnect()

        self.X_Degree_input_field.setText(str(cfg["render"]["degree"][0]))
        self.Y_Degree_input_field.setText(str(cfg["render"]["degree"][2]))
        self.Z_Degree_input_field.setText(str(cfg["render"]["degree"][1]))
        self.Number_of_renders_input_field.setText(str(cfg["render"]["renders"]))

        self.X_Degree_input_field.editingFinished.connect(self.set_angles)
        self.Y_Degree_input_field.editingFinished.connect(self.set_angles)
        self.Z_Degree_input_field.editingFinished.connect(self.set_angles)
        self.Number_of_renders_input_field.editingFinished.connect(self.set_renders)

        self.Update_slider(self.X_Degree_slider,self.X_Degree_input_field.text())
        self.Update_slider(self.Y_Degree_slider,self.Y_Degree_input_field.text())
        self.Update_slider(self.Z_Degree_slider,self.Z_Degree_input_field.text())
        
    
    def Update_slider(self, slider, val):
        try:
            slider.setValue(int(round(float(val), 0)))
        except Exception as e:
            try:
                slider.setValue(0)
            except:
                print("Error", e)

    def increase_count(self):
        try:
            number_of_renders_value = int(self.Number_of_renders_input_field.text())
            self.Number_of_renders_input_field.setText(str(number_of_renders_value + 1))
        except:
            number_of_renders_value = 0
            self.Number_of_renders_input_field.setText(str(number_of_renders_value))
        self.Number_of_renders_input_field.editingFinished.emit()

    def decrease_count(self):
        try:
            number_of_renders_value = int(self.Number_of_renders_input_field.text())
            if number_of_renders_value > 1:  # Prevent negative values if needed
                self.Number_of_renders_input_field.setText(str(number_of_renders_value - 1))
        except:
            number_of_renders_value = 0
            self.Number_of_renders_input_field.setText(str(number_of_renders_value))
        self.Number_of_renders_input_field.editingFinished.emit()

    def update_degree_input(self, slider, input_field):
        value = slider.value()
        input_field.setText(str(value))

    def resizeEvent(self, event):

        """
        Handles window resize event

        Args:
            - Number of renders
                -   
                -   
                -   
                -   
            - Degree Change
                -   
                -   
                -   
                -  
                -
                -
                -

            - Generate Button
                -   
                -   
                -   
    


            """


        # Number of Renders Title Position
        self.Number_of_renders_title.setGeometry(int(self.width() * 0.025), int(self.height() * 0.01), 150, 20)

        # Number of renders
        self.Number_of_renders_input_field.setGeometry(int(self.width() * 0.025), int(self.height() * 0.25), int(self.width() * 0.1), 20)
        self.Number_of_renders_minus.setGeometry(int(self.width() * 0.14), int(self.height() * 0.25), 25, 20)
        self.Number_of_renders_plus.setGeometry(int(self.width() * 0.17), int(self.height() * 0.25), 25, 20)

        # Degree Change title position
        self.Degree_Change_title.setGeometry(int(self.width() * 0.25), int(self.height() * 0.01), 150, 20)

        # X Degree
        self.X_Degree_Label.setGeometry(int(self.width() * 0.25), int(self.height() * 0.2), 50, 30)
        self.X_Degree_input_field.setGeometry(int(self.width() * 0.30), int(self.height() * 0.25), int(self.width() * 0.1), 20)
        self.X_Degree_slider.setGeometry(QtCore.QRect(int(self.width() * 0.43), int(self.height() * 0.28), int(self.width() * 0.2), 16))

        # Y Degree
        self.Y_Degree_Label.setGeometry(int(self.width() * 0.25), int(self.height() * 0.45), 50, 30)
        self.Y_Degree_input_field.setGeometry(int(self.width() * 0.30), int(self.height() * 0.5), int(self.width() * 0.1), 20)
        self.Y_Degree_slider.setGeometry(QtCore.QRect(int(self.width() * 0.43), int(self.height() * 0.52), int(self.width() * 0.2), 16))

        # Z Degree
        self.Z_Degree_Label.setGeometry(int(self.width() * 0.25), int(self.height() * 0.7), 50, 30)
        self.Z_Degree_input_field.setGeometry(int(self.width() * 0.30), int(self.height() * 0.75), int(self.width() * 0.1), 20)
        self.Z_Degree_slider.setGeometry(QtCore.QRect(int(self.width() * 0.43), int(self.height() * 0.77), int(self.width() * 0.2), 16))
        
        # Generate Button 
        self.GenerateRenders_Button.setGeometry(self.width()-self.GenerateRenders_Button.width(), 10, self.GenerateRenders_Button.width(), 50)

    
        
    def generate_render(self):
        if not self.rendering:
            self.rendering = True
            self.thread = RenderThread()

            self.thread.progress.connect(self.update_loading)
            self.thread.finished.connect(self.complete_loading)

            self.thread.start()
            self.windowUp()

            self.thread.quit()
        else:
            renderingBox = QMessageBox()
            renderingBox.setText("Already rendering, please wait for current render to finish before starting new render.")
            renderingBox.exec()
        
    
    def windowUp(self):
        self.LoadingBox = LoadingScreen("")
        self.LoadingBox.update_text("")
        

        self.LoadingBox.show()

    def update_loading(self,text):
        self.LoadingBox.update_text(text)
    
    def complete_loading(self):
        self.rendering = False
        self.LoadingBox.update_text("Rendering complete")



    def set_renders(self):
        try: 
            backend.set_renders(int(self.Number_of_renders_input_field.text()))
        except:
            print("Error")
    
    def set_angles(self):
        self.Update_slider(self.X_Degree_slider,self.X_Degree_input_field.text())
        self.Update_slider(self.Y_Degree_slider,self.Y_Degree_input_field.text())
        self.Update_slider(self.Z_Degree_slider,self.Z_Degree_input_field.text())
        try: 
            backend.set_angles( [float(self.X_Degree_input_field.text()), float(self.Z_Degree_input_field.text()), float(self.Y_Degree_input_field.text())] )
        except:
            print("Error")
        



class Page5(Page):
    """
    Page 5:
    """
    def __init__(self, path, parent=None):
        self.path = path
        """
        Initialise "Page n"

        Args:
            parent
            
        Methods:

        """
        super().__init__(parent)

        #First Section
        def Get_Object_Filepath():
            try:
                path = QFileDialog.getOpenFileName(self, 'Open file', 'c:/',"3D Model (*.blend *.stl *.obj)")[0]
                if (path == ""): return
                # add the object to the shared state
                shared_state.add_item(backend.RenderObject(filepath = path))
                
                self.path.Object_detect()
            except Exception:
                QMessageBox.warning(self, "Error when reading model", "The selected file is corrupt or invalid.")

        self.Import_Object_Button = QPushButton("Import Object", self)
        self.Import_Object_Button.setGeometry(0, 10, 125, 50)
        self.Import_Object_Button.clicked.connect(Get_Object_Filepath)

        #Second Section
        def Tutorial_Object():
            Tutorial_Box = QMessageBox()
            Tutorial_Box.setText("Please select a tutorial object from below")
            Tutorial_Box.addButton("Cube", QMessageBox.ActionRole)
            Tutorial_Box.addButton("Cylinder", QMessageBox.ActionRole)
            Tutorial_Box.addButton("Cone", QMessageBox.ActionRole)
            Tutorial_Box.addButton("Plane", QMessageBox.ActionRole)
            Tutorial_Box.addButton("Sphere", QMessageBox.ActionRole)
            Tutorial_Box.addButton("Monkey", QMessageBox.ActionRole)

            Tutorial_Box.exec()
            obj = backend.RenderObject(primative = Tutorial_Box.clickedButton().text().upper())
            shared_state.add_item(obj)
            
            self.path.Object_detect()

        self.TutorialObjects_Button = QPushButton('Tutorial Objects', self)
        self.TutorialObjects_Button.setGeometry(150, 10, 125, 50)
        self.TutorialObjects_Button.clicked.connect(Tutorial_Object)

        #Third Section --> LEFT FOR NOW
        self.BrowseFiles_Button = QPushButton('Generate Data Set', self)
        self.BrowseFiles_Button.setGeometry(300, 10, 125, 50)

        #Fourth Section
        self.ExportSettings_Button = QPushButton('Export Settings', self)
        self.ExportSettings_Button.setGeometry(450, 10, 125, 50)
        self.ExportSettings_Button.clicked.connect(lambda: backend.export())

        #Fifth Section
        def Get_Settings_Filepath():
            try:
                path = QFileDialog.getOpenFileName(self, 'Open file', 'c:/',"Settings (*.json)")[0]
                if (path == ""): return
                backend = Backend(json_filepath = path)
                for i in range(4):
                    self.path.tabwizard.widget(i).update_ui_by_config()
            except Exception:
                QMessageBox.warning(self, "Error when reading JSON", "The selected file is corrupt or invalid.")

        self.ImportSettings_Button = QPushButton('Import Settings', self)
        self.ImportSettings_Button.setGeometry(600, 10, 125, 50)
        self.ImportSettings_Button.clicked.connect(Get_Settings_Filepath)

        def delete_object():
            to_delete = QMessageBox()
            to_delete.setText("Please select an object to remove from below")

            if (not shared_state.items):
                return QMessageBox.warning(self, "Warning", "There are no objects to delete.")

            for obj in shared_state.items:
                to_delete.addButton(str(obj), QMessageBox.ActionRole)

            to_delete.exec()
            obj_index = int(to_delete.clickedButton().text()[-1]) - 1
            obj = shared_state.items[obj_index]
            shared_state.remove_item(obj)
            del backend.get_config()["objects"][obj.object_pos]
            # shift objects after this one down by one
            for i in range(obj_index, len(shared_state.items)):
                obj = shared_state.items[i]
                obj.object_pos = i

            shared_state.items_updated.emit(shared_state.items)
            # The last object was deleted
            if (not shared_state.items):
                self.path.tabwizard.setTabEnabled(0, False)
                self.path.tabwizard.setTabEnabled(1, False)
                self.path.tabwizard.setTabEnabled(2, False)
                self.path.tabwizard.setTabEnabled(3, False)
                QMessageBox.warning(self, "Warning", "You have deleted all of the objects, object manipulation tabs have been disabled.")
    
        #Sixth section
        self.Delete_Object_Button = QPushButton('Delete Object', self)
        self.Delete_Object_Button.setGeometry(750, 10, 125, 50)
        self.Delete_Object_Button.clicked.connect(delete_object)

class MainWindow(QMainWindow):
    """
    Main Window for all the elements
    """
    def __init__(self):
        """
        Initialise all elements of the Program
        """
        super().__init__()


        self.setWindowTitle('CS 3028 Project')
        screen = QApplication.primaryScreen()
        screen_geometry = screen.geometry()
        self.setGeometry(
            screen_geometry.width() // 4,  # x position to center the window
            screen_geometry.height() // 4,  # y position to center the window
            screen_geometry.width() // 2,
            screen_geometry.height() // 2
        )

        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)
        self.layout = QVBoxLayout(central_widget)
        central_widget.setStyleSheet("background-color: #9bc1bc;")
        
        # Nav bar
        # margins need to be removed to match enviroment
        self.navbar = Widget()
        self.layout.addWidget(self.navbar)
        self.navbar.setFixedHeight(int(self.height()*0.2))

        
        ############
        
        #Set image background - dont delete will use later

        #self.navbar.setStyleSheet("""
        #background-image: url(frontend/background.jpg); 
        #background-attachment: fixed;
        #""")

        ############



        # enviroment
        self.environment = QWidget()
        self.layout.addWidget(self.environment)
        self.environment.setStyleSheet("background-color: black;")

        central_widget.setLayout(self.layout)
        self.setMinimumSize(920, 500) # minimum size of program
        self.show()

    def resizeEvent(self, event):
        """
        Handles window resize event

        #On re sizing all elements in the program should be re-adjusted to fit

        Args:
            event
        """
        window_height = self.height() # get screen height
        navbar_height = 150
        self.navbar.setFixedHeight(navbar_height) # emviroment
        super().resizeEvent(event)  # handle resize event


class GlobalStyles:
    """
    Class for global styling
    """


    @staticmethod

    def style():
        return """
        QTabBar::tab { 
            background-color: #D3D3D3; 
            padding: 5px;
            border: 1px solid black;
            border-radius: 3px;
            font-weight: bold;
            min-width: 120px;
        }
        

        QTabBar::tab:selected {
            background-color: #A9A9A9;  
        }
        QTabWidget::pane {
            border: 1px solid black;
        }

        QPushButton {
            background-color: white;
            color: black;
            border: 1px solid black;
            border-radius: 5px;
            font-weight: bold;
        }
        QPushButton:hover {
            background-color: #A9A9A9; 
        }
        QPushButton:checked {
            background-color: #A9A9A9;  
        }
        QLineEdit {
            border: 1px solid black; 
            border-radius: 5px;       
            background-color: white; 
            color: black;            
        }
        QLabel {
            font-weight: bold;
        }
        QCheckBox {
            font-weight: bold;
            background:transparent;

        }
        QWidget {
        background-color:#e6ebe0;
        }
        QSlider {
        background: transparent; 
        }
        
        """



if __name__ == "__main__":
    
    

    app = QApplication(sys.argv)
    # creates this shared state
    # shared_state = ComboBoxState()
    window = MainWindow()
    window.show()

    def Get_Object_Filepath(self):
        try:
            path = QFileDialog.getOpenFileName(self, 'Open file', 'c:/',"3D Model (*.blend *.stl *.obj)")[0]
            if (path == ""): return False
            # add the object to the shared state
            shared_state.add_item(backend.RenderObject(filepath = path))
            
            self.Object_detect()
            return True
        except Exception:
            QMessageBox.warning(self, "Error when reading model", "The selected file is corrupt or invalid.")


    def Tutorial_Object(self):
        Tutorial_Box = QMessageBox()
        Tutorial_Box.setText("Please select a tutorial object from below")
        Tutorial_Box.addButton("Cube", QMessageBox.ActionRole)
        Tutorial_Box.addButton("Cylinder", QMessageBox.ActionRole)
        Tutorial_Box.addButton("Cone", QMessageBox.ActionRole)
        Tutorial_Box.addButton("Plane", QMessageBox.ActionRole)
        Tutorial_Box.addButton("Sphere", QMessageBox.ActionRole)
        Tutorial_Box.addButton("Monkey", QMessageBox.ActionRole)

        Tutorial_Box.exec()
        obj = backend.RenderObject(primative = Tutorial_Box.clickedButton().text().upper())
        shared_state.add_item(obj)

        self.Object_detect()
        return True

    objectSelected = False
    while not objectSelected:
        Initial_Object = QMessageBox()
        Initial_Object.setText("Please select an initial object from below")
        Initial_Object.addButton("Custom Object", QMessageBox.ActionRole)
        Initial_Object.addButton("Tutorial Object", QMessageBox.ActionRole)

        Initial_Object.exec_()
        if Initial_Object.clickedButton().text() == "Custom Object":
            objectSelected = Get_Object_Filepath(window.navbar)
        else:
            objectSelected = Tutorial_Object(window.navbar)
            
    
    #from Front_tests import Tests
    #Tests(window, shared_state, Page1, Page2, Page3, Page4, Page5, backend)
    
    
    
    sys.exit(app.exec_())