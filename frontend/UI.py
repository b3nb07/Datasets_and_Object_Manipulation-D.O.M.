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

# Initialise backend
backend = Backend()

class ComboBoxState(QObject):
    """
    ComboBoxState is a child of QObject, used to handle and maintain the shared box states
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
        print(f'items in combo box have been updated: {items}')
        self.items_updated.emit(items)  # Emit signal for item updates

    def add_item(self, item):
        self.items.append(item)
        self.items_updated.emit(self.items)
        print(f'ComboBox Item added {item}')

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
    Clas to Add all pages into a tabwizard
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
        State = Backend.is_config_objects_empty(self)
        for i in range(4):
            self.tabwizard.setTabEnabled(i, State)

        
class Page1(Page):
    """
    Page 1: Objects
    """
    def __init__(self, parent=None):
        Obj_list = ["Object 1", "Object 2", "Object 3"]
        """
        Initialise "Page n"

        Args:
            parent
            n
            Object_pos_title
            XObj_pos
            XObj_pos_input_field
            X_button_minus
            X_button_plus

            YObj_pos
            YObj_pos_input_field
            Y_button_minus
            Y_button_plus

            ZObj_pos
            ZObj_pos_input_field
            Z_button_minus
            Z_button_plus

            Object_pos_title
            Width_Obj_pos
            Width_Obj_pos_input_field
            W_slider

            Height_Obj_pos
            Height_Obj_pos_input_field
            H_slider

            Length_Obj_pos
            Length_Obj_pos_input_field
            L_slider

            combo_box
            Obj_list

        Methods:

        """
        super().__init__(parent)

        self.Object_pos_title = QLabel(f"{Obj_list[0]} Co-ords", self)

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
        
        # textChanged callbacks that updates backend
        self.XObj_pos_input_field.textChanged.connect(lambda: self.update_object_pos())
        self.YObj_pos_input_field.textChanged.connect(lambda: self.update_object_pos())
        self.ZObj_pos_input_field.textChanged.connect(lambda: self.update_object_pos())
        
        self.X_button_plus.clicked.connect(lambda: self.Plus_click(self.XObj_pos_input_field))
        self.X_button_minus.clicked.connect(lambda: self.Minus_click(self.XObj_pos_input_field))
        
        self.Y_button_plus.clicked.connect(lambda: self.Plus_click(self.YObj_pos_input_field))
        self.Y_button_minus.clicked.connect(lambda: self.Minus_click(self.YObj_pos_input_field))
        
        self.Z_button_plus.clicked.connect(lambda: self.Plus_click(self.ZObj_pos_input_field))
        self.Z_button_minus.clicked.connect(lambda: self.Minus_click(self.ZObj_pos_input_field))
        
        ##########################################################
        self.Object_scale_title = QLabel(f"{Obj_list[0]} Scale", self)

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

        # textChanged callbacks that updates backend
        self.Width_Obj_pos_input_field.textChanged.connect(lambda: self.update_object_scale())
        self.Height_Obj_pos_input_field.textChanged.connect(lambda: self.update_object_scale())
        self.Length_Obj_pos_input_field.textChanged.connect(lambda: self.update_object_scale())

        ########################################

        self.W_slider.valueChanged.connect(lambda val: self.Slider_Update(val, self.Width_Obj_pos_input_field))
        self.H_slider.valueChanged.connect(lambda val: self.Slider_Update(val, self.Height_Obj_pos_input_field))
        self.L_slider.valueChanged.connect(lambda val: self.Slider_Update(val, self.Length_Obj_pos_input_field))
        
        ########################################

        self.Object_rotation_title = QLabel(f"{Obj_list[0]} Rotation", self)

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

        #########################################
        
        self.X_Rotation.valueChanged.connect(lambda val: self.Slider_Update(val, self.X_Rotation_input_field))
        self.Y_Rotation.valueChanged.connect(lambda val: self.Slider_Update(val, self.Y_Rotation_input_field))
        self.Z_Rotation.valueChanged.connect(lambda val: self.Slider_Update(val, self.Z_Rotation_input_field))
        
        #########################################

        # create initial combo_box
        self.combo_box = QComboBox(self)
    
        # connecting shared state updates to combo box
        shared_state.items_updated.connect(self.update_combo_box_items)
        shared_state.selection_changed.connect(self.combo_box.setCurrentIndex)

        # initialise items
        self.update_combo_box_items(shared_state.items)
        shared_state.update_items(items=[])
        shared_state.update_selected(0)
    
    def update_combo_box_items(self, items):
        self.combo_box.clear()
        self.combo_box.addItems(map(lambda o: str(o), items))
    
    
    # TODO: THIS SHOULD BE SELECTED AND CALLED WHEN SWITCHING BETWEEN OBJECT TABS. IT SHOULD INITIALISE ALL ATTRIBUTES.
    def on_object_selected(self):
        # get the selected object's position (index)
        selected_object_pos = self.object_list_combo.currentIndex()
        print(selected_object_pos)

        # find the corresponding object from the backend
        selected_object = shared_state.items[selcted_object_pos]
        # insert the selected object's properties
        self.XObj_pos_input_field.setText(str(selected_object["pos"][0]))
        self.YObj_pos_input_field.setText(str(selected_object["pos"][1]))
        self.ZObj_pos_input_field.setText(str(selected_object["pos"][2]))
    
    def update_object_pos(self):
        """ method to update a targetted object's position """
        try: 
            x = float(self.XObj_pos_input_field.text() or 0)
            z = float(self.ZObj_pos_input_field.text() or 0)
            y = float(self.YObj_pos_input_field.text() or 0)
                
            location = [x,z,y]
            print(f"UPDATE_OBJECT_POS -> {location}") #DEBUG
            
            # get the selected object's position from the combo box
            selected_object_index = self.combo_box.currentIndex()
            #call backend function
            
            #DEBUG
            # obj = backend.RenderObject(primative = "MONKEY")
            # obj.update_object_location(location)            
            obj = shared_state.items[selected_object_index]
            print(obj)
            obj.set_loc(location)
        except:
            QMessageBox.warning(self, "Error Updating Pos", "X, Y or Z value is invalid")
    
    def update_object_scale(self):
        """ method to update a targetted object's scale """
        try: 
            width = float(self.Width_Obj_pos_input_field.text() or 0)
            height = float(self.Height_Obj_pos_input_field.text() or 0)
            length = float(self.Length_Obj_pos_input_field.text() or 0)
            
            scale = [width,height,length]
            print(f"UPDATE_OBJECT_SCALE -> {scale}") #DEBUG
            
            # get the selected object's position from the combo box
            selected_object_index = self.combo_box.currentIndex()
            obj = shared_state.items[selected_object_index]
            print(obj)
            obj.set_scale(scale)
        except:
            QMessageBox.warning(self, "Error Updating Scale", "Width, Height or Length value is invalid")
    
    
    def Plus_click(self, field):
        try:
            val = float(field.text()) + 1
            field.setText(str(val))
        except:
            field.setText(str(0.0))
        
        
    def Minus_click(self, field):
        try:
            val = float(field.text()) - 1
            field.setText(str(val))
        except:
            field.setText(str(0.0))
            
    def Slider_Update(self, val, field):
        field.setText(str(val))
        
    def update_label(self):
        AllItems = [self.combo_box.itemText(i) for i in range(self.combo_box.count())]
        n = self.combo_box.currentIndex()
        Title = AllItems[n]
        self.Object_pos_title.setText(f"{Title} Co-ords")
        self.Object_scale_title.setText(f"{Title} Scale")
        self.Object_rotation_title.setText(f"{Title} Rotation")


    def resizeEvent(self, event):
        """
        Handles window resize event
        #each page needs it own re-size event whoda thunk that

        #On re sizing all elements in the program should be re-adjusted to fit

        Args:
            event # re-size
            Object_pos_title # Label for object position
            XObj_pos # Label for x position
            XObj_pos_input_field # Input field for x position
            X_button_minus # Button addition for x position
            X_button_plus # Button sdubtraction for x position

            YObj_pos # Label for y position
            YObj_pos_input_field # Input field for y position
            Y_button_minus # Button addition for y position
            Y_button_plus # Button sdubtraction for y position

            ZObj_pos # Label for z position
            ZObj_pos_input_field # Input field for z position
            Z_button_minus # Button addition for z position
            Z_button_plus # Button sdubtraction for z position

            Object_scale_title # Label for object position
            Width_Obj_pos  # Label for width scale
            Width_Obj_pos_input_field # Input field for width scale
            W_slider # Slider for width scale

            Height_Obj_pos # Label for Height scale
            Height_Obj_pos_input_field # Input field for Height scale
            H_slider # Slider for Height scale

            Length_Obj_pos # Label for Length scale
            Length_Obj_pos_input_field # Input field for Length scale
            L_slider # Slider for Length scale

            combo_box # Dropdown menu for Object select
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
    Page 2:
    """
    def __init__(self, parent=None):
        """
        Initialise "Page n"

        Args:

            
        Methods:

        """
        super().__init__(parent)
        
        # Pivot Point Coords Section
        self.Pivot_Point_subtitle = QLabel("Pivot Point", self)

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


        #Angle Change Section

        self.Position_layout = QVBoxLayout()
        self.Angle_Change_title = QLabel(f"Angle Change Between Images", self)

        self.Degrees_Pivot = QLabel("Degrees:", self)
        self.Degrees_Pivot_input_field = QLineEdit(parent=self)
        self.Degrees_Pivot_input_field.setText("0")
        
        self.Degrees_Slider = QtWidgets.QSlider(self)
        self.Degrees_Slider.setOrientation(QtCore.Qt.Horizontal)
        self.Degrees_Slider.setRange(0, 360)
        
        self.Distance_Pivot = QLabel("Distance:", self)
        self.Distance_Pivot_input_field = QLineEdit(parent=self)
        self.Distance_Pivot_input_field.setText("0")
        
        self.Distance_Slider = QtWidgets.QSlider(self)
        self.Distance_Slider.setOrientation(QtCore.Qt.Horizontal)
        self.Distance_Slider.setRange(0, 100)
        
        #################
        self.Degrees_Slider.valueChanged.connect(lambda val: self.Slider_Update(val, self.Degrees_Pivot_input_field))
        self.Distance_Slider.valueChanged.connect(lambda val: self.Slider_Update(val, self.Distance_Pivot_input_field))
        #################
        
        self.Num_Rotations = QLabel("Rotations:", self)
        self.Num_Rotations_input_field = QLineEdit(parent=self)
        self.Num_Rotations_input_field.setText("0")
        self.Num_Rotations_minus = QPushButton('-', self)
        self.Num_rotations_plus = QPushButton('+', self)
        
        ###################
        self.Num_rotations_plus.clicked.connect(lambda: self.Plus_click(self.Num_Rotations_input_field))
        self.Num_Rotations_minus.clicked.connect(lambda: self.Minus_click(self.Num_Rotations_input_field))
        ###################

        self.combo_box = QComboBox(self)
        Pivot_list = ["Custom", "Object 1", "Object 2"]
        self.combo_box.addItems(Pivot_list)
    
    
    def Plus_click(self, field):
        try:
            val = float(field.text()) + 1
            field.setText(str(val))
        except:
            field.setText(str(0.0))
        
        
    def Minus_click(self, field):
        try:
            val = float(field.text()) - 1
            field.setText(str(val))
        except:
            field.setText(str(0.0))
            
    def Slider_Update(self, val, field):
        field.setText(str(val))

    def resizeEvent(self, event):
        
        # Title Position
        self.Pivot_Point_subtitle.setGeometry(int(self.width() * 0.025), int(self.height() * 0.01), 100, 30)

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

        # Angle Change Section
        self.Angle_Change_title.setGeometry(int(self.width() * 0.30), int(self.height() * 0.01), 150, 30)

        # Degrees
        self.Degrees_Pivot.setGeometry(int(self.width() * 0.30), int(self.height() * 0.275), 50, 30)
        self.Degrees_Pivot_input_field.setGeometry(int(self.width() * 0.40), int(self.height() * 0.275), int(self.width() * 0.1), 20)
        self.Degrees_Slider.setGeometry(QtCore.QRect(int(self.width() * 0.53), int(self.height() * 0.275), int(self.width() * 0.2), 16))
        
        # Distacne
        self.Distance_Pivot.setGeometry(int(self.width() * 0.30), int(self.height() * 0.5), 75, 30)
        self.Distance_Pivot_input_field.setGeometry(int(self.width() * 0.40), int(self.height() * 0.5), int(self.width() * 0.1), 20)
        self.Distance_Slider.setGeometry(QtCore.QRect(int(self.width() * 0.53), int(self.height() * 0.5), int(self.width() * 0.2), 16))

        # Rotations
        self.Num_Rotations.setGeometry(int(self.width() * 0.30), int(self.height() * 0.75), 80, 30)
        self.Num_Rotations_input_field.setGeometry(int(self.width() * 0.40), int(self.height() * 0.75), int(self.width() * 0.1), 20)
        self.Num_Rotations_minus.setGeometry(int(self.width() * 0.53), int(self.height() * 0.75), 25, 20)
        self.Num_rotations_plus.setGeometry(int(self.width() * 0.56), int(self.height() * 0.75), 25, 20)

        #Pivot Selction
        self.combo_box.setGeometry(self.width()-self.combo_box.width(), 0, self.combo_box.width(), self.combo_box.height())


        super().resizeEvent(event)  # Call the parent class's resizeEvent


class Page3(Page):
    """
    Page 3:
    """
    def __init__(self, parent=None):
        """
        Initialise "Page n"

        Args:
            parent
            
        Methods:

        """

        super().__init__(parent)

        #First Section
        self.Set_All_Random_Button = QCheckBox("Set all Random", self)
        self.Set_All_Random_Button.setLayoutDirection(Qt.LayoutDirection.RightToLeft)

        self.Set_All_Random_Button.setGeometry(0, 0, 125, 30)

        #Second Section
        self.ObjectDimensions_Label = QLabel(f"Object x Dimension", self)
        self.ObjectDimensions_Label.setGeometry(150, 10, 125, 20)

        self.Width_Button = QCheckBox("Width ", self)
        self.Width_Button.setLayoutDirection(Qt.LayoutDirection.RightToLeft)
        self.Width_Button.setGeometry(150, 30, 65, 20)

        self.Height_Button = QCheckBox("Height", self)
        self.Height_Button.setLayoutDirection(Qt.LayoutDirection.RightToLeft)
        self.Height_Button.setGeometry(150, 50, 65, 20)

        self.Length = QCheckBox("Length", self)
        self.Length.setLayoutDirection(Qt.LayoutDirection.RightToLeft)
        self.Length.setGeometry(150, 70, 65, 20)

        #Third Section
        self.combo_box = QComboBox(self)
        Obj_list = ["Object 1", "Object 2", "Object 3"]
        self.combo_box.addItems(Obj_list)
        self.combo_box.setGeometry(275, 10, 100, 20)

        self.X_Button = QCheckBox("X", self)
        self.X_Button.setLayoutDirection(Qt.LayoutDirection.RightToLeft)
        self.X_Button.setGeometry(275, 30, 30, 20)

        self.Y_Button = QCheckBox("Y", self)
        self.Y_Button.setLayoutDirection(Qt.LayoutDirection.RightToLeft)
        self.Y_Button.setGeometry(315, 30, 30, 20)

        self.Z = QCheckBox("Z", self)
        self.Z.setLayoutDirection(Qt.LayoutDirection.RightToLeft)
        self.Z.setGeometry(350, 30, 30, 20)

        self.PivotPoint_Label = QLabel(f"Pivot Point Co-ords:", self)
        self.PivotPoint_Label.setGeometry(275, 50, 120, 20)

        self.X_Button = QCheckBox("X", self)
        self.X_Button.setLayoutDirection(Qt.LayoutDirection.RightToLeft)
        self.X_Button.setGeometry(275, 70, 30, 20)

        self.Y_Button = QCheckBox("Y", self)
        self.Y_Button.setLayoutDirection(Qt.LayoutDirection.RightToLeft)
        self.Y_Button.setGeometry(315, 70, 30, 20)

        self.Z_Button = QCheckBox("Z", self)
        self.Z_Button.setLayoutDirection(Qt.LayoutDirection.RightToLeft)
        self.Z_Button.setGeometry(350, 70, 30, 20)

        #Fourth Section
        self.Reflect_Label = QLabel(f"Reflect:", self)
        self.Reflect_Label.setGeometry(450, 10, 150, 20)

        self.Reflect_Button = QCheckBox("", self)
        self.Reflect_Button.setGeometry(560, 10, 150, 20)

        self.AutoRotationAngle_Label = QLabel(f"Auto Rotation Angle:", self)
        self.AutoRotationAngle_Label.setGeometry(450, 30, 150, 20)

        self.AutoRotationAngle_Button = QCheckBox("", self)
        self.AutoRotationAngle_Button.setGeometry(560, 30, 150, 20)

        self.ImportObjects_Label = QLabel(f"Import Objects:", self)
        self.ImportObjects_Label.setGeometry(450, 50, 150, 20)

        self.ImportObjects_Button = QCheckBox("", self)
        self.ImportObjects_Button.setGeometry(560, 50, 150, 20)

        self.ImportEnvironment_Label = QLabel(f"Import Environment:", self)
        self.ImportEnvironment_Label.setGeometry(450, 70, 150, 20)

        self.ImportEnvironment_Button = QCheckBox("", self)
        self.ImportEnvironment_Button.setGeometry(560, 70, 150, 20)

        #Section 5
        
        self.RandomSettingSeed_Label = QLabel(f"Random Setting Seed", self)
        self.RandomSettingSeed_Label.setGeometry(self.width()-self.RandomSettingSeed_Label.width(), 10, 125, 20)
        self.RandomSeed_Label = QLabel(f"<Random Seed>", self)

    def resizeEvent(self, event):
        if self.RandomSeed_Label.width() > 125:
            x = self.RandomSeed_Label.width()
        else:
            x = 125
        self.RandomSettingSeed_Label.setGeometry(self.width()-self.RandomSettingSeed_Label.width(), 10, x, 20)
        self.RandomSeed_Label.setGeometry(self.width()-self.RandomSeed_Label.width(), 30, self.RandomSeed_Label.width(), 20)

class Page4(Page):
    """
    Page 4: Render
    """
    def __init__(self, parent=None):
        """
        Initialize Page 4
        """
        super().__init__(parent)



        # Number of Renders input fields
        self.Number_of_renders_title = QLabel("Number of Renders", self)
        self.Number_of_renders_input_field = QLineEdit(parent=self)
        self.Number_of_renders_minus = QPushButton('-', self)
        self.Number_of_renders_plus = QPushButton('+', self)

        self.Degree_Change_title = QLabel("Degrees of Change", self)

        # X Degree
        self.X_Degree_Label = QLabel("X:", self)
        self.X_Degree_input_field = QLineEdit(parent=self)
        self.X_Degree_slider = QtWidgets.QSlider(self)
        self.X_Degree_slider.setOrientation(QtCore.Qt.Horizontal)

        # Y Degree
        self.Y_Degree_Label = QLabel("Y:", self)
        self.Y_Degree_input_field = QLineEdit(parent=self)
        self.Y_Degree_slider = QtWidgets.QSlider(self)
        self.Y_Degree_slider.setOrientation(QtCore.Qt.Horizontal)

        # Z Degree
        self.Z_Degree_Label = QLabel("Z:", self)
        self.Z_Degree_input_field = QLineEdit(parent=self)
        self.Z_Degree_slider = QtWidgets.QSlider(self)
        self.Z_Degree_slider.setOrientation(QtCore.Qt.Horizontal)

        #Generate Renders Button
        self.GenerateRenders_Button = QPushButton('Generate Renders', self)

    def resizeEvent(self, event):

        # Number of Renders Title Position
        self.Number_of_renders_title.setGeometry(int(self.width() * 0.025), int(self.height() * 0.01), 100, 30)

        # Number of renders
        self.Number_of_renders_input_field.setGeometry(int(self.width() * 0.025), int(self.height() * 0.25), int(self.width() * 0.1), 20)
        self.Number_of_renders_minus.setGeometry(int(self.width() * 0.14), int(self.height() * 0.25), 25, 20)
        self.Number_of_renders_plus.setGeometry(int(self.width() * 0.17), int(self.height() * 0.25), 25, 20)

        # Degree Change title position
        self.Degree_Change_title.setGeometry(int(self.width() * 0.25), int(self.height() * 0.01), 100, 30)

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



        super().resizeEvent(event)  # Call the parent class's resizeEvent

class Page5(Page):
    """
    Page 5:
    """
    def __init__(self, path ,parent=None):
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
                path = QFileDialog.getOpenFileName(self, 'Open file', 'c:\\',"3D Model (*.blend *.stl *.obj)")[0]
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
                path = QFileDialog.getOpenFileName(self, 'Open file', 'c:\\',"Settings (*.json)")[0]
                if (path == ""): return
                backend = Backend(json_filepath = path)
            except Exception:
                QMessageBox.warning(self, "Error when reading JSON", "The selected file is corrupt or invalid.")

        self.ImportSettings_Button = QPushButton('Import Settings', self)
        self.ImportSettings_Button.setGeometry(600, 10, 125, 50)
        self.ImportSettings_Button.clicked.connect(Get_Settings_Filepath)

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

        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        self.layout = QVBoxLayout()

        # Nav bar

        # margins need to be removed to match enviroment
        self.navbar = Widget()
        self.layout.addWidget(self.navbar)
        
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

if __name__ == "__main__":
    
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()

    def Get_Object_Filepath(self):
        try:
            path = QFileDialog.getOpenFileName(self, 'Open file', 'c:\\',"3D Model (*.blend *.stl *.obj)")[0]
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

    sys.exit(app.exec_())