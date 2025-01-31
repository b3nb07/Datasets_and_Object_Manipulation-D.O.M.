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

class TabDialog(QWidget):
    def __init__(self, parent: QWidget = None):
        super().__init__(parent)
        self.setWindowTitle("Datasets and Object Modeling")
        """stream = QtCore.QFile("Style\DarkMode.qss")
        stream.open(QtCore.QIODevice.ReadOnly)
        self.setStyleSheet(QtCore.QTextStream(stream).readAll())"""

        tab_widget = QTabWidget()
        tab_widget.addTab(ObjectTab(self), "Object")
        tab_widget.addTab(PivotTab(self), "Pivot Point")
        tab_widget.addTab(Random(self), "Random")
        tab_widget.addTab(Render(self), "Render")
        tab_widget.addTab(Port(self, tab_widget), "Import/Export")

        tab_widget.setTabEnabled(0, False)
        tab_widget.setTabEnabled(1, False)
        tab_widget.setTabEnabled(2, False)
        tab_widget.setTabEnabled(3, False)


        tab_widget.setFixedHeight(200)
        # enviroment
        environment = QWidget()
        environment.setStyleSheet("background-color: black;")
        self.setMinimumSize(920, 700) # minimum size of program

        main_layout = QVBoxLayout()
        main_layout.addWidget(tab_widget)
        main_layout.addWidget(environment)
        self.setLayout(main_layout)


class ObjectTab(QWidget):
    def __init__(self, parent: QWidget):
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
        ####################################################################
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

        ############################################################

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

        ####################################################

        main_layout = QGridLayout()
        main_layout.addWidget(self.Object_pos_title, 0, 0)

        main_layout.addWidget(self.XObj_pos, 1, 0)
        main_layout.addWidget(self.XObj_pos_input_field, 1, 1)
        main_layout.addWidget(self.X_button_minus, 1, 2)
        main_layout.addWidget(self.X_button_plus, 1, 3)

        main_layout.addWidget(self.YObj_pos, 2, 0)
        main_layout.addWidget(self.YObj_pos_input_field, 2, 1)
        main_layout.addWidget(self.Y_button_minus, 2, 2)
        main_layout.addWidget(self.Y_button_plus, 2, 3)

        main_layout.addWidget(self.ZObj_pos, 3, 0)
        main_layout.addWidget(self.ZObj_pos_input_field, 3, 1)
        main_layout.addWidget(self.Z_button_minus, 3, 2)
        main_layout.addWidget(self.Z_button_plus, 3, 3)
        #############################################################

        main_layout.addWidget(self.Object_rotation_title, 0, 4)

        main_layout.addWidget(self.X_Rotation_Label, 1, 4)
        main_layout.addWidget(self.X_Rotation_input_field, 1, 5)
        main_layout.addWidget(self.X_Rotation, 1, 6)

        main_layout.addWidget(self.Y_Rotation_Label, 2, 4)
        main_layout.addWidget(self.Y_Rotation_input_field, 2, 5)
        main_layout.addWidget(self.Y_Rotation, 2, 6)

        main_layout.addWidget(self.Z_Rotation_Label, 3, 4)
        main_layout.addWidget(self.Z_Rotation_input_field, 3, 5)
        main_layout.addWidget(self.Z_Rotation, 3, 6)

        ##################################################################

        main_layout.addWidget(self.Object_scale_title, 0, 7)

        main_layout.addWidget(self.Width_Obj_pos, 1, 7)
        main_layout.addWidget(self.Width_Obj_pos_input_field, 1, 8)
        main_layout.addWidget(self.W_slider, 1, 9)

        main_layout.addWidget(self.Height_Obj_pos, 2, 7)
        main_layout.addWidget(self.Height_Obj_pos_input_field, 2, 8)
        main_layout.addWidget(self.H_slider, 2, 9)

        main_layout.addWidget(self.Length_Obj_pos, 3, 7)
        main_layout.addWidget(self.Length_Obj_pos_input_field, 3, 8)
        main_layout.addWidget(self.L_slider, 3, 9)

        main_layout.addWidget(self.combo_box, 0, 9)
        self.setLayout(main_layout)

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


class PivotTab(QWidget):
    def __init__(self, parent: QWidget):
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

        #################
        main_layout = QGridLayout()

        main_layout.addWidget(self.Pivot_Point_Check, 0, 0)

        main_layout.addWidget(self.XPivot_pos, 1, 0)
        main_layout.addWidget(self.XPivot_point_input_field, 1, 1)
        main_layout.addWidget(self.XPivot_button_minus, 1, 2)
        main_layout.addWidget(self.XPivot_button_plus, 1, 3)

        main_layout.addWidget(self.YPivot_pos, 2, 0)
        main_layout.addWidget(self.YPivot_point_input_field, 2, 1)
        main_layout.addWidget(self.YPivot_button_minus, 2, 2)
        main_layout.addWidget(self.YPivot_button_plus, 2, 3)

        main_layout.addWidget(self.ZPivot_pos, 3, 0)
        main_layout.addWidget(self.ZPivot_point_input_field, 3, 1)
        main_layout.addWidget(self.ZPivot_button_minus, 3, 2)
        main_layout.addWidget(self.ZPivot_button_plus, 3, 3)

        main_layout.addWidget(self.Distance_Pivot, 4, 0)
        main_layout.addWidget(self.Distance_Pivot_input_field, 4, 1)
        main_layout.addWidget(self.Distance_Slider, 4, 2)

        main_layout.addWidget(self.combo_box, 0, 4)

        self.setLayout(main_layout)



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

class Random(QWidget):
    def __init__(self, parent: QWidget):
        super().__init__(parent)

        # First Section
        self.Set_All_Random_Button = QCheckBox("Set all Random", self)
        self.Set_All_Random_Button.stateChanged.connect(self.set_all_random)

        # Second Section
        self.ObjectDimensions_Label = QLabel(f"Object Dimensions", self)
        
        self.Width_Button = QCheckBox("Width", self)
        self.Width_Button.toggled.connect(self.on_width_toggle)


        #if checked then change value of width text 

        self.Height_Button = QCheckBox("Height", self)
        self.Height_Button.toggled.connect(self.on_height_toggle)
        self.Length_Button = QCheckBox("Length", self)
        self.Length_Button.toggled.connect(self.on_length_toggle)



        #Third Section
        self.Object_Coords_Label = QLabel(f"Object x Co-ords:", self)

        self.X_Button = QCheckBox("X", self)
        self.X_Button.toggled.connect(self.on_x_toggle)


        self.Y_Button = QCheckBox("Y", self)
        self.Y_Button.toggled.connect(self.on_y_toggle)


        self.Z_Button = QCheckBox("Z", self)
        self.Z_Button.toggled.connect(self.on_z_toggle)


        self.PivotPoint_Label = QLabel(f"Pivot Point Co-ords:", self)

        self.X_Button2 = QCheckBox("X", self)
        self.X_Button2.stateChanged.connect(backend.toggle_random_pivot_x)

        self.Y_Button2 = QCheckBox("Y", self)
        self.Y_Button2.stateChanged.connect(backend.toggle_random_pivot_y)

        self.Z_Button2 = QCheckBox("Z", self)
        self.Z_Button2.stateChanged.connect(backend.toggle_random_pivot_z)

        #Fourth Section
        self.AutoRotationAngle_Label = QLabel(f"Auto Rotation Angle:", self)
        

        self.AutoRotationAngle_Button = QCheckBox("", self)
        self.AutoRotationAngle_Button.stateChanged.connect(backend.toggle_random_environment_angle)

        self.ImportEnvironment_Label = QLabel(f"Import Environment:", self)

        self.ImportEnvironment_Button = QCheckBox("", self)
        self.ImportEnvironment_Button.stateChanged.connect(backend.toggle_random_environment_background)

        #Section 5
        
        self.RandomSettingSeed_Label = QLabel(f"Random  Seed", self)
        self.RandomSeed_Label = QLabel(f"<Random Seed>", self)
        self.RandomSeed_Label.setText(str(backend.get_config()["seed"]))


        #Third Section
        self.object_toggle_states = {}
        self.combo_box = QComboBox(self)
        #self.combo_box.addItems()
        
        shared_state.items_updated.connect(self.update_combo_box_items)
        shared_state.selection_changed.connect(self.combo_box.setCurrentIndex)
        self.combo_box.activated.connect(lambda: self.object_selected())

        self.update_combo_box_items(shared_state.items)
        shared_state.update_items(items=[]) 
        shared_state.update_selected(0)    

        main_layout = QGridLayout()
        
        main_layout.addWidget(self.Set_All_Random_Button, 0, 0)
        main_layout.addWidget(self.ObjectDimensions_Label, 0, 1)

        main_layout.addWidget(self.Width_Button, 1, 1)
        main_layout.addWidget(self.Height_Button, 2, 1)
        main_layout.addWidget(self.Length_Button, 3, 1)

        main_layout.addWidget(self.Object_Coords_Label, 0, 2)

        main_layout.addWidget(self.X_Button, 1, 2)
        main_layout.addWidget(self.Y_Button, 2, 2)
        main_layout.addWidget(self.Z_Button, 3, 2)

        main_layout.addWidget(self.PivotPoint_Label, 0, 3)

        main_layout.addWidget(self.X_Button2, 1, 3)
        main_layout.addWidget(self.Y_Button2, 2, 3)
        main_layout.addWidget(self.Z_Button2, 3, 3)

        main_layout.addWidget(self.AutoRotationAngle_Label, 0, 4)
        main_layout.addWidget(self.AutoRotationAngle_Button, 1, 4)

        main_layout.addWidget(self.ImportEnvironment_Label, 0, 5)
        main_layout.addWidget(self.ImportEnvironment_Button, 1, 5)

        main_layout.addWidget(self.RandomSettingSeed_Label, 0, 6)
        main_layout.addWidget(self.RandomSeed_Label, 1, 6)

        main_layout.addWidget(self.combo_box, 0, 7)

        self.setLayout(main_layout)

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


class Render(QWidget):
    def __init__(self, parent: QWidget):
        super().__init__(parent)

        self.GenerateRenders_Button = QPushButton('Generate Renders', self)
        self.GenerateRenders_Button.clicked.connect(self.generate_render)
        


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

        main_layout = QGridLayout()

        main_layout.addWidget(self.Number_of_renders_title, 0, 0)

        main_layout.addWidget(self.Number_of_renders_input_field, 1, 0)
        main_layout.addWidget(self.Number_of_renders_minus, 1, 1)
        main_layout.addWidget(self.Number_of_renders_plus, 1, 2)

        main_layout.addWidget(self.Degree_Change_title, 0, 3)

        main_layout.addWidget(self.X_Degree_Label, 0, 4)
        main_layout.addWidget(self.X_Degree_input_field, 1, 4)
        main_layout.addWidget(self.X_Degree_slider, 2, 4)

        main_layout.addWidget(self.Y_Degree_Label, 0, 5)
        main_layout.addWidget(self.Y_Degree_input_field, 1, 5)
        main_layout.addWidget(self.Y_Degree_slider, 2, 5)

        main_layout.addWidget(self.Z_Degree_Label, 0, 6)
        main_layout.addWidget(self.Z_Degree_input_field, 1, 6)
        main_layout.addWidget(self.Z_Degree_slider, 2, 6)

        main_layout.addWidget(self.GenerateRenders_Button, 0, 7)

        self.setLayout(main_layout)



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


class Port(QWidget):
    def __init__(self, parent: QWidget, tab_widget: QTabWidget):
        super().__init__(parent)
        


        #First Section
        def Get_Object_Filepath():
            try:
                path = QFileDialog.getOpenFileName(self, 'Open file', 'c:\\',"3D Model (*.blend *.stl *.obj)")[0]
                if (path == ""): return
                # add the object to the shared state
                shared_state.add_item(backend.RenderObject(filepath = path))
                
                Object_detect(tab_widget)

            except Exception:
                QMessageBox.warning(self, "Error when reading model", "The selected file is corrupt or invalid.")

        self.Import_Object_Button = QPushButton("Import Object", self)
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
    
            Object_detect(tab_widget)

        self.TutorialObjects_Button = QPushButton('Tutorial Objects', self)
        self.TutorialObjects_Button.clicked.connect(Tutorial_Object)

        #Third Section --> LEFT FOR NOW
        self.BrowseFiles_Button = QPushButton('Generate Data Set', self)

        def Export_Settings():
            try:
                export_path = QFileDialog.getExistingDirectory(self, "Select Folder")

                if (export_path == "" or export_path == None):
                    pass
                else:
                    backend.export(export_path)

            except:
                ErrorBox = QMessageBox()
                ErrorBox.setText("There was an error selecting folder, please try again.")

        #Fourth Section
        self.ExportSettings_Button = QPushButton('Export Settings', self)
        self.ExportSettings_Button.clicked.connect(lambda: backend.export())

        #Fifth Section
        def Get_Settings_Filepath():
            try:
                path = QFileDialog.getOpenFileName(self, 'Open file', 'c:\\',"Settings (*.json)")[0]
                if (path == ""): return
                backend = Backend(json_filepath = path)
                for i in range(4):
                    self.path.tabwizard.widget(i).update_ui_by_config()
            except Exception:
                QMessageBox.warning(self, "Error when reading JSON", "The selected file is corrupt or invalid.")

        self.ImportSettings_Button = QPushButton('Import Settings', self)
        self.ImportSettings_Button.clicked.connect(Get_Settings_Filepath)

        def delete_object(tab_widget):
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
                Object_detect(tab_widget)
                QMessageBox.warning(self, "Warning", "You have deleted all of the objects, object manipulation tabs have been disabled.")
    
        #Sixth section
        self.Delete_Object_Button = QPushButton('Delete Object', self)

        self.Delete_Object_Button.clicked.connect(lambda: delete_object(tab_widget))

        def Object_detect(tab_widget):
            State = not Backend.is_config_objects_empty(tab_widget)
            for i in range(4):
                tab_widget.setTabEnabled(i, State)

        main_layout = QGridLayout()

        main_layout.addWidget(self.TutorialObjects_Button, 0, 0)
        main_layout.addWidget(self.Import_Object_Button, 0, 1)
        main_layout.addWidget(self.ExportSettings_Button, 0, 2)
        main_layout.addWidget(self.ImportSettings_Button, 0, 3)
        main_layout.addWidget(self.Delete_Object_Button, 0, 4)
        main_layout.addWidget(self.BrowseFiles_Button, 0, 5)

        self.setLayout(main_layout)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    tab_dialog = TabDialog()
    tab_dialog.show()

    sys.exit(app.exec())