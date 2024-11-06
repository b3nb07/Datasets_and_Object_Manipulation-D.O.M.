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
        self.tabwizard.addPage(
          Page2(), "Pivot Point")
        self.tabwizard.addPage(Page3(), "Generate Random")
        self.tabwizard.addPage(Page4(), "Render")
        self.tabwizard.addPage(Page5(), "Import and Export")

class Page1(Page):
    """
    Page 1: Objects
    """
    def __init__(self, parent=None):
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
        n=1

        self.Object_pos_title = QLabel(f"Object {n} Co-ords", self)

        self.XObj_pos = QLabel("X:", self)
        self.XObj_pos_input_field = QLineEdit(parent=self)
        self.X_button_minus = QPushButton('-', self)
        self.X_button_plus = QPushButton('+', self)

        self.YObj_pos = QLabel("Y:", self)

        self.YObj_pos_input_field = QLineEdit(parent=self)

        self.Y_button_minus = QPushButton('-', self)
        self.Y_button_plus = QPushButton('+', self)
        
        self.ZObj_pos = QLabel("Z:", self)

        self.ZObj_pos_input_field = QLineEdit(parent=self)

        self.Z_button_minus = QPushButton('-', self)
        self.Z_button_plus = QPushButton('+', self)

        ##########################################################
        self.Object_scale_title = QLabel(f"Object {n} Scale", self)

        self.Width_Obj_pos = QLabel("Width:", self)
        self.Width_Obj_pos_input_field = QLineEdit(parent=self)
        
        self.W_slider = QtWidgets.QSlider(self)
        self.W_slider.setOrientation(QtCore.Qt.Horizontal)

        self.Height_Obj_pos = QLabel("Height:", self)
        self.Height_Obj_pos_input_field = QLineEdit(parent=self)

        self.H_slider = QtWidgets.QSlider(self)
        self.H_slider.setOrientation(QtCore.Qt.Horizontal)
        
        self.Length_Obj_pos = QLabel("Length:", self)
        self.Length_Obj_pos_input_field = QLineEdit(parent=self)

        self.L_slider = QtWidgets.QSlider(self)
        self.L_slider.setOrientation(QtCore.Qt.Horizontal)

        ########################################

        self.Object_rotation_title = QLabel(f"Object {n} Rotation", self)

        self.X_Rotation_Label = QLabel("Roll:", self)
        self.X_Rotation_input_field = QLineEdit(parent=self)
        
        self.X_Rotation = QtWidgets.QSlider(self)
        self.X_Rotation.setOrientation(QtCore.Qt.Horizontal)

        self.Y_Rotation_Label = QLabel("Pitch:", self)
        self.Y_Rotation_input_field = QLineEdit(parent=self)
        
        self.Y_Rotation = QtWidgets.QSlider(self)
        self.Y_Rotation.setOrientation(QtCore.Qt.Horizontal)

        self.Z_Rotation_Label = QLabel("Yaw:", self)
        self.Z_Rotation_input_field = QLineEdit(parent=self)
        
        self.Z_Rotation = QtWidgets.QSlider(self)
        self.Z_Rotation.setOrientation(QtCore.Qt.Horizontal)


        #########################################

        self.combo_box = QComboBox(self)
        Obj_list = ["Object 1", "Object 2", "Object 3"]
        self.combo_box.addItems(Obj_list)


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
    Page 2: Pivot Point
    """
    def __init__(self, parent=None):
        """
        Initialise "Page n"
        Handles pivot point controls

        Args:
        parent
        Pivot_Point_subtitle
        XPivot_pos
        XPivot_point_input_field
        XPivot_button_minus
        XPivot_button_plus
        YPivot_pos
        YPivot_point_input_field
        YPivot_button_minus
        YPivot_button_plus
        ZPivot_pos
        ZPivot_point_input_field
        ZPivot_button_minus
        ZPivot_button_plus
        Angle_Change_title
        Degrees_Pivot
        Degrees_Pivot_input_field
        Degrees_Slider
        Num_Rotations
        Num_Rotations_input_field
        Num_Rotations_minus
        Num_rotations_plus
        combo_box
        Pivot_list

        Methods:


        """
        super().__init__(parent)

        # Pivot Point Coords Section
        self.Pivot_Point_subtitle = QLabel("Pivot Point", self)

        # X Pivot Point Controls
        self.XPivot_pos = QLabel("X:", self)
        self.XPivot_point_input_field = QLineEdit(parent=self)
        self.XPivot_button_minus = QPushButton('-', self)
        self.XPivot_button_plus = QPushButton('+', self)
        self.XPivot_button_minus.clicked.connect(lambda: self.plus_minus(self.XPivot_point_input_field, -1))
        self.XPivot_button_plus.clicked.connect(lambda: self.plus_minus(self.XPivot_point_input_field, 1))
        self.XPivot_point_input_field.setText("0")

        # Y Pivot Point Controls
        self.YPivot_pos = QLabel("Y:", self)
        self.YPivot_point_input_field = QLineEdit(parent=self)
        self.YPivot_button_minus = QPushButton('-', self)
        self.YPivot_button_plus = QPushButton('+', self)
        self.YPivot_button_minus.clicked.connect(lambda: self.plus_minus(self.YPivot_point_input_field, -1))
        self.YPivot_button_plus.clicked.connect(lambda: self.plus_minus(self.YPivot_point_input_field, 1))
        self.YPivot_point_input_field.setText("0")

        # Z Pivot Point Controls
        self.ZPivot_pos = QLabel("Z:", self)
        self.ZPivot_point_input_field = QLineEdit(parent=self)
        self.ZPivot_button_minus = QPushButton('-', self)
        self.ZPivot_button_plus = QPushButton('+', self)
        self.ZPivot_button_minus.clicked.connect(lambda: self.plus_minus(self.ZPivot_point_input_field, -1))
        self.ZPivot_button_plus.clicked.connect(lambda: self.plus_minus(self.ZPivot_point_input_field, 1))
        self.ZPivot_point_input_field.setText("0")

        # Angle Change Section
        self.Angle_Change_title = QLabel(f"Angle Change Between Images", self)

        self.Degrees_Pivot = QLabel("Degrees:", self)
        self.Degrees_Pivot_input_field = QLineEdit(parent=self)
        
        self.Degrees_Slider = QtWidgets.QSlider(self)
        self.Degrees_Slider.setOrientation(QtCore.Qt.Horizontal)

        self.Num_Rotations = QLabel("Rotations:", self)
        self.Num_Rotations_input_field = QLineEdit(parent=self)
        self.Num_Rotations_minus = QPushButton('-', self)
        self.Num_rotations_plus = QPushButton('+', self)
        self.Num_Rotations_minus.clicked.connect(lambda: self.plus_minus(self.Num_Rotations_input_field, -1))
        self.Num_rotations_plus.clicked.connect(lambda: self.plus_minus(self.Num_Rotations_input_field, 1))
        self.Num_Rotations_input_field.setText("0")

        self.combo_box = QComboBox(self)
        Pivot_list = ["Custom", "Object 1", "Object 2"]
        self.combo_box.addItems(Pivot_list)

    def plus_minus(self, input_field, value_change):
        """
        Adds functionality to the + and - boxes

        """
        input_value = int(input_field.text())
        new_input_value = input_value + value_change
        if new_input_value >= 0:  
            input_field.setText(str(new_input_value))
    



    def resizeEvent(self, event):


        """""
        handles Resizing of window 

        Args:

        Pivot_Point_subtitle
        
        XPivot_pos 
        XPivot_point_input_field
        XPivot_button_minus
        XPivot_button_plus

        YPivot_pos 
        YPivot_point_input_field
        YPivot_button_minus
        YPivot_button_plus
        
        XPivot_pos 
        XPivot_point_input_field
        XPivot_button_minus
        XPivot_button_plus
                

        ZPivot_pos 
        ZPivot_point_input_field
        ZPivot_button_minus
        ZPivot_button_plus
        
        Angle_Change_title

        Degrees_Pivot
        Degrees_Pivot_input_field
        Degrees_Slider
        Num_Rotations
        Num_Rotations_input_field
        Num_Rotations_minus
        Num_Rotations_plus


        """""
        
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
        self.Degrees_Pivot.setGeometry(int(self.width() * 0.30), int(self.height() * 0.30), 50, 30)
        self.Degrees_Pivot_input_field.setGeometry(int(self.width() * 0.40), int(self.height() * 0.35), int(self.width() * 0.1), 20)
        self.Degrees_Slider.setGeometry(QtCore.QRect(int(self.width() * 0.53), int(self.height() * 0.35), int(self.width() * 0.2), 16))

        # Rotations
        self.Num_Rotations.setGeometry(int(self.width() * 0.30), int(self.height() * 0.60), 80, 30)
        self.Num_Rotations_input_field.setGeometry(int(self.width() * 0.40), int(self.height() * 0.65), int(self.width() * 0.1), 20)
        self.Num_Rotations_minus.setGeometry(int(self.width() * 0.53), int(self.height() * 0.65), 25, 20)
        self.Num_rotations_plus.setGeometry(int(self.width() * 0.56), int(self.height() * 0.65), 25, 20)

        #Pivot Selction
        self.combo_box.setGeometry(self.width()-self.combo_box.width(), 0, self.combo_box.width(), self.combo_box.height())


        super().resizeEvent(event)  # Call the parent class's resizeEvent

class Page3(Page):
    """
    Page 3: Generate Random
    """
    def __init__(self, parent=None):
        """
        Initialise "Page n"

        Args:
            parent
            Set_All_Random_Button
            ObjectDimensions_Label
            Width_Button
            Height_Button
            Length
            combo_box
            Obj_list
            X_Button
            Y_Button
            Z
            PivotPoint_Label
            X_Button
            Y_Button
            Z_Button
            Reflect_Label
            Reflect_Button
            AutoRotationAngle_Label
            AutoRotationAngle_Button
            ImportObjects_Label
            ImportObjects_Button
            ImportEnvironment_Label
            ImportEnvironment_Button
            RandomSettingSeed_Label
            RandomSeed_Label
            
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
        self.X_Button.setGeometry(215, 50, 30, 20)

        self.Y_Button = QCheckBox("Y", self)
        self.Y_Button.setLayoutDirection(Qt.LayoutDirection.RightToLeft)
        self.Y_Button.setGeometry(315, 50, 30, 20)

        self.Z_Button = QCheckBox("Z", self)
        self.Z_Button.setLayoutDirection(Qt.LayoutDirection.RightToLeft)
        self.Z_Button.setGeometry(250, 50, 30, 20)

        self.PivotPoint_Label = QLabel(f"Pivot Point Co-ords:", self)
        self.PivotPoint_Label.setGeometry(275, 50, 120, 20)

        self.X_Button2 = QCheckBox("X", self)
        self.X_Button2.setLayoutDirection(Qt.LayoutDirection.RightToLeft)
        self.X_Button2.setGeometry(275, 70, 30, 20)

        self.Y_Button2 = QCheckBox("Y", self)
        self.Y_Button2.setLayoutDirection(Qt.LayoutDirection.RightToLeft)
        self.Y_Button2.setGeometry(315, 70, 30, 20)

        self.Z_Button2 = QCheckBox("Z", self)
        self.Z_Button2.setLayoutDirection(Qt.LayoutDirection.RightToLeft)
        self.Z_Button2.setGeometry(350, 70, 30, 20)

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
        window_width = self.width()
        window_height = self.height()
        
        # First Section
        self.Set_All_Random_Button.setGeometry(int(window_width * 0.01), int(window_height * 0.02), int(window_width * 0.2), 30)
        
        # Second Section
        self.ObjectDimensions_Label.setGeometry(int(window_width * 0.25), int(window_height * 0.02), int(window_width * 0.2), 20)
        
        self.Width_Button.setGeometry(int(window_width * 0.17), int(window_height * 0.3), int(window_width * 0.15), 20)
        self.Height_Button.setGeometry(int(window_width * 0.24), int(window_height * 0.3), int(window_width * 0.15), 20)
        self.Length.setGeometry(int(window_width * 0.31), int(window_height * 0.3), int(window_width * 0.15), 20)
        
        # Third Section
        self.combo_box.setGeometry(int(window_width * 0.375), int(window_height * 0.02), int(window_width * 0.15), 20)
        
        self.X_Button.setGeometry(int(window_width * 0.2875), int(window_height * 0.6), 30, 20)
        self.Y_Button.setGeometry(int(window_width * 0.3575), int(window_height * 0.60), 30, 20)
        self.Z_Button.setGeometry(int(window_width * 0.4275), int(window_height * 0.60), 30, 20)
        
        self.PivotPoint_Label.setGeometry(int(window_width * 0.55), int(window_height * 0.02), int(window_width * 0.2), 20)
        
        self.X_Button2.setGeometry(int(window_width * 0.525), int(window_height * 0.2), 30, 20)
        self.Y_Button2.setGeometry(int(window_width * 0.575), int(window_height * 0.2), 30, 20)
        self.Z_Button2.setGeometry(int(window_width * 0.625), int(window_height * 0.2), 30, 20)
        
        # Fourth Section
        self.Reflect_Label.setGeometry(int(window_width * 0.7), int(window_height * 0.1), int(window_width * 0.2), 20)
        self.Reflect_Button.setGeometry(int(window_width * 0.83), int(window_height * 0.1), 30, 20)
        
        self.AutoRotationAngle_Label.setGeometry(int(window_width * 0.7), int(window_height * 0.3), int(window_width * 0.2), 20)
        self.AutoRotationAngle_Button.setGeometry(int(window_width * 0.83), int(window_height * 0.3), 30, 20)
        
        self.ImportObjects_Label.setGeometry(int(window_width * 0.7), int(window_height * 0.5), int(window_width * 0.2), 20)
        self.ImportObjects_Button.setGeometry(int(window_width * 0.83), int(window_height * 0.5), 30, 20)
        
        self.ImportEnvironment_Label.setGeometry(int(window_width * 0.7), int(window_height * 0.7), int(window_width * 0.2), 20)
        self.ImportEnvironment_Button.setGeometry(int(window_width * 0.83), int(window_height * 0.7), 30, 20)
        
        # Fifth Section
        x = max(self.RandomSeed_Label.width(), 125)  # Minimum width for RandomSettingSeed_Label
        self.RandomSettingSeed_Label.setGeometry(window_width - x - 10, int(window_height * 0.02), x, 20)
        self.RandomSeed_Label.setGeometry(window_width - self.RandomSeed_Label.width() - 10, int(window_height * 0.2), self.RandomSeed_Label.width(), 20)


class Page4(Page):
    """
    Page 4: Render
    """
    def __init__(self, parent=None):
        """
        Initialize Page 4
        """
        super().__init__(parent)
        
        #def GenerateRenders():

        #backend.render
        #backend.RenderObject.setloc()
        #backend.RenderObject.setscale()
        #backend.RenderObject.setrotation()




        #Generate Renders Button
        self.GenerateRenders_Button = QPushButton('Generate Renders', self)
        self.GenerateRenders_Button.clicked.connect(self.generateRandom)
        self.GenerateRenders_Button.setGeometry(0, 10, 125, 50)

        




        # Number of Renders input fields
        self.Number_of_renders_title = QLabel("Number of Renders", self)
        self.Number_of_renders_input_field = QLineEdit(parent=self)
        self.Number_of_renders_input_field.setText("1")

        self.Number_of_renders_minus = QPushButton('-', self)
        self.Number_of_renders_plus = QPushButton('+', self)

        self.Number_of_renders_minus.clicked.connect(self.decrease_count)
        self.Number_of_renders_plus.clicked.connect(self.increase_count)




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
    
    def increase_count(self):
        number_of_renders_value = int(self.Number_of_renders_input_field.text())
        self.Number_of_renders_input_field.setText(str(number_of_renders_value + 1))

    def decrease_count(self):
        number_of_renders_value = int(self.Number_of_renders_input_field.text())
        if number_of_renders_value > 1:  # Prevent negative values if needed
            self.Number_of_renders_input_field.setText(str(number_of_renders_value - 1))

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





    def add_camera_poses_linear(self):
        number_of_renders = int(self.Number_of_renders_input_field.text())

        x_degree_change = int(self.X_Degree_input_field.text())
        z_degree_change = int(self.Z_Degree_input_field.text())
        y_degree_change = int(self.Y_Degree_input_field.text())

    def add_camera_poses_random():
        pass


    def generateRandom(self):
        #validate
        number_of_renders = int(self.Number_of_renders_input_field.text())

        if number_of_renders <1:
            QMessageBox.warning(self, "Error when starting render", "Invalid value for number of renders.")
            return
        
        #add cameras
        
        #for now all cameras are linear

        self.add_camera_poses_linear()
        


        
        #backend.render()



class Page5(Page):
    """
    Page 5:
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
        def Get_Object_Filepath():
            try:
                path = QFileDialog.getOpenFileName(self, 'Open file', 'c:\\',"3D Model (*.blend *.stl *.obj)")[0]
                if (path == ""): return
                backend.RenderObject(filepath = path)
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
            backend.RenderObject(primative = Tutorial_Box.clickedButton().text().upper())

        self.TutorialObjects_Button = QPushButton('Tutorial Objects', self)
        self.TutorialObjects_Button.setGeometry(150, 10, 125, 50)
        self.TutorialObjects_Button.clicked.connect(Tutorial_Object)

        #Third Section --> LEFT FOR NOW
        self.BrowseFiles_Button = QPushButton('Generate Data Set', self)
        self.BrowseFiles_Button.setGeometry(300, 10, 125, 50)

        #Fourth Section
        self.GenerateDataSet_Button = QPushButton('Export Settings', self)
        self.GenerateDataSet_Button.setGeometry(450, 10, 125, 50)
        self.GenerateDataSet_Button.clicked.connect(lambda: backend.export())

        #Fifth Section
        def Get_Settings_Filepath():
            try:
                path = QFileDialog.getOpenFileName(self, 'Open file', 'c:\\',"Settings (*.json)")[0]
                if (path == ""): return
                backend = Backend(json_filepath = path)
            except Exception:
                QMessageBox.warning(self, "Error when reading JSON", "The selected file is corrupt or invalid.")
    
        self.ExportSettings_Button = QPushButton('Import Settings', self)
        self.ExportSettings_Button.setGeometry(600, 10, 125, 50)
        self.ExportSettings_Button.clicked.connect(Get_Settings_Filepath)

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
        print(f"{self.width()}, {self.height()}") # get screen height
        navbar_height = 150
        self.navbar.setFixedHeight(navbar_height) # emviroment
        super().resizeEvent(event)  # handle resize event

if __name__ == "__main__":
    
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
