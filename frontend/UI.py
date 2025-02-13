"""Importing"""

from functools import cached_property
import sys
from PyQt5 import QtCore, QtWidgets

import os
import PyQt5
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
        self.itemNames = []
        self.selected = None

    def update_items(self, items):
        self.items = items
        self.items_updated.emit(items)  # Emit signal for item updates

    def add_item(self, item, Name):
        self.items.append(item)
        self.itemNames.append(Name)
        self.items_updated.emit(self.items)

    def remove_item(self, item):
        self.items.remove(item)
        self.items_updated.emit(self.items)

    def remove_item(self, item):
        pos = self.items.index(item)
        self.items.remove(item)
        self.itemNames.remove(self.itemNames[pos])
        self.items_updated.emit(self.items)

    def update_selected(self, index):
        self.selected_index = index
        # maybe delete
        self.selection_changed.emit(index)


class RenderThread(QThread):
    finished = pyqtSignal()
    progress = pyqtSignal(str)

    def run(self):
        self.progress.emit("Rendering...")
        backend.render(headless = False)
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

# creates this shared state
shared_state = ComboBoxState()

class TabDialog(QWidget):
    def __init__(self, parent: QWidget = None):
        super().__init__(parent)
        self.setWindowTitle("Datasets and Object Modeling")
        
        tab_widget = QTabWidget()

        # Add all other tabs first
        tab_widget.addTab(ObjectTab(self, tab_widget), "Object")
        tab_widget.addTab(PivotTab(self), "Pivot Point")
        tab_widget.addTab(Render(self), "Render")
        tab_widget.addTab(Lighting(self), "Lighting")
 
        Temp_index = tab_widget.addTab(QWidget(), "Random")
        tab_widget.addTab(Port(self, tab_widget), "Import/Export")
        tab_widget.addTab(Settings(self, tab_widget), "Settings")
        


        random_tab = RandomTabDialog(self, tab_widget)
        tab_widget.removeTab(Temp_index)
        tab_widget.insertTab(Temp_index, random_tab, "Random")

        
        #tab_widget.widget(0).layout().itemAtPosition(1, 1).widget().setEnabled(False)

        tab_widget.setTabEnabled(0, False)
        tab_widget.setTabEnabled(1, False)
        tab_widget.setTabEnabled(2, False)
        tab_widget.setTabEnabled(3, False)
        tab_widget.setTabEnabled(4, False)

        tab_widget.setFixedHeight(200)
        
        # enviroment
        environment = QWidget()
        environment.setStyleSheet("background-color: black;")
        
        ObjectsStatusBar = QScrollArea()
        ObjectsStatusBar.setStyleSheet("background-color: white;")
        ObjectsStatusBar.setMaximumWidth(175)
        
        ObjectsStatusBar.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        ObjectsStatusBar.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

        
        content_widget = QWidget()
        ObjectsStatusBar.setWidget(content_widget)
        ObjectsStatusBar.setWidgetResizable(True)
        
        ObjLayout = QVBoxLayout(content_widget)
        
        for i in range(1, 51):
            Button = QPushButton(f"Object {i}")
            ObjLayout.addWidget(Button)

        self.setMinimumSize(1350, 700) # minimum size of program
        main_layout = QGridLayout()
        main_layout.addWidget(tab_widget, 0, 0, 1, 8)
        
        main_layout.addWidget(ObjectsStatusBar, 1, 0, 1, 2)
        main_layout.addWidget(environment, 1, 1, 1, 7)  
        self.setLayout(main_layout)


class ObjectTab(QWidget):
    def __init__(self, parent: QWidget, tab_widget: QTabWidget):
        super().__init__(parent)

        self.Object_pos_title = QLabel(f"Co-ords", self)

        self.XObj_pos = QLabel("X:", self)
        self.XObj_pos_input_field = QLineEdit(parent=self)
        self.XObj_pos_input_field.setText("0.0")
        self.X_button_minus = QPushButton('-', self)
        self.X_button_plus = QPushButton('+', self)
        
        self.Object_pos_title.setToolTip('Changes the objects Position') 

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
        self.Object_scale_title = QLabel(f"Scale", self)
        
        self.Object_scale_title.setToolTip('Changes the objects scale')

        self.Width_Obj_pos = QLabel("Width:", self)
        self.Width_Obj_pos_input_field = QLineEdit(parent=self)
        
        self.Width_Obj_pos_input_field.setText("1.0")
        
        self.W_slider = QtWidgets.QSlider(self)
        self.W_slider.setRange(-100, 100)
        self.W_slider.setPageStep(0)
        self.W_slider.setOrientation(QtCore.Qt.Horizontal)

        self.Height_Obj_pos = QLabel("Height:", self)
        self.Height_Obj_pos_input_field = QLineEdit(parent=self)
        self.Height_Obj_pos_input_field.setText("1.0")

        self.H_slider = QtWidgets.QSlider(self)
        self.H_slider.setRange(-100, 100)
        self.H_slider.setPageStep(0)
        self.H_slider.setOrientation(QtCore.Qt.Horizontal)
        
        self.Length_Obj_pos = QLabel("Length:", self)
        self.Length_Obj_pos_input_field = QLineEdit(parent=self)
        self.Length_Obj_pos_input_field.setText("1.0")

        self.L_slider = QtWidgets.QSlider(self)
        self.L_slider.setRange(-100, 100)
        self.L_slider.setPageStep(0)
        self.L_slider.setOrientation(QtCore.Qt.Horizontal)
        
        #########################################

        self.Object_rotation_title = QLabel(f"Rotation", self)
        
        self.Object_rotation_title.setToolTip('Changes the objects rotation')

        self.X_Rotation_Label = QLabel("Roll:", self)
        self.X_Rotation_input_field = QLineEdit(parent=self)
        self.X_Rotation_input_field.setText("0.0")
        
        self.X_Rotation = QtWidgets.QSlider(self)
        self.X_Rotation.setPageStep(0)
        self.X_Rotation.setOrientation(QtCore.Qt.Horizontal)
        self.X_Rotation.setRange(0, 360)
        
        self.Y_Rotation_Label = QLabel("Pitch:", self)
        self.Y_Rotation_input_field = QLineEdit(parent=self)
        self.Y_Rotation_input_field.setText("0.0")
        
        self.Y_Rotation = QtWidgets.QSlider(self)
        self.Y_Rotation.setPageStep(0)
        self.Y_Rotation.setOrientation(QtCore.Qt.Horizontal)
        self.Y_Rotation.setRange(0, 360)

        self.Z_Rotation_Label = QLabel("Yaw:", self)
        self.Z_Rotation_input_field = QLineEdit(parent=self)
        self.Z_Rotation_input_field.setText("0.0")
        
        self.Z_Rotation = QtWidgets.QSlider(self)
        self.Z_Rotation.setPageStep(0)
        self.Z_Rotation.setOrientation(QtCore.Qt.Horizontal)
        self.Z_Rotation.setRange(0, 360)

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
    
        def delete_object(tab_widget):
            to_delete = QMessageBox()
            to_delete.setText("Please select an object to remove from below")

            if (not shared_state.items):
                return QMessageBox.warning(self, "Warning", "There are no objects to delete.")

            for obj in shared_state.items:
                to_delete.addButton(str(obj), QMessageBox.ActionRole)
            
            to_delete.addButton("Cancel", QMessageBox.ActionRole)

            to_delete.exec()
            choice = str(to_delete.clickedButton().text())

            if choice != "Cancel":
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

        self.Delete_Object_Button = QPushButton('Delete Object', self)
        self.Delete_Object_Button.clicked.connect(lambda: delete_object(tab_widget))

        # create initial combo_box
        self.combo_box = QComboBox(self)
        # connecting shared state updates to combo box
        shared_state.items_updated.connect(lambda: self.update_combo_box_items(shared_state.itemNames))
        shared_state.selection_changed.connect(self.combo_box.setCurrentIndex)
        self.combo_box.currentIndexChanged.connect(self.on_object_selected)

        # initialise items
        shared_state.update_items(items=[])
        shared_state.update_selected(0)
        
        self.combo_box.setToolTip('Changes the object selected')

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

        main_layout.addWidget(self.Import_Object_Button, 4, 9)
        main_layout.addWidget(self.TutorialObjects_Button, 4, 8)
        main_layout.addWidget(self.Delete_Object_Button, 5, 9)

        self.setLayout(main_layout)

        def Object_detect(tab_widget):
            State = not Backend.is_config_objects_empty(tab_widget)
            for i in range(4):
                tab_widget.setTabEnabled(i, State)

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

        self.Width_Obj_pos_input_field.textEdited.connect(lambda: self.Update_slider(self.W_slider, self.Width_Obj_pos_input_field.text()))
        self.Height_Obj_pos_input_field.textEdited.connect(lambda: self.Update_slider(self.H_slider, self.Height_Obj_pos_input_field.text()))
        self.Length_Obj_pos_input_field.textEdited.connect(lambda: self.Update_slider(self.L_slider, self.Length_Obj_pos_input_field.text()))

        # editingFinished callbacks that updates backend
        self.Width_Obj_pos_input_field.editingFinished.connect(self.update_object_scale)
        self.Height_Obj_pos_input_field.editingFinished.connect(self.update_object_scale)
        self.Length_Obj_pos_input_field.editingFinished.connect(self.update_object_scale)

        ########################################
        
        self.W_slider.sliderMoved.connect(lambda val: self.Slider_Update(val, self.Width_Obj_pos_input_field))
        self.H_slider.sliderMoved.connect(lambda val: self.Slider_Update(val, self.Height_Obj_pos_input_field))
        self.L_slider.sliderMoved.connect(lambda val: self.Slider_Update(val, self.Length_Obj_pos_input_field))

        self.W_slider.sliderReleased.connect(self.update_object_scale)
        self.H_slider.sliderReleased.connect(self.update_object_scale)
        self.L_slider.sliderReleased.connect(self.update_object_scale)

        #########################################
  
        self.X_Rotation_input_field.textEdited.connect(lambda: self.Update_slider(self.X_Rotation, self.X_Rotation_input_field.text()))
        self.Y_Rotation_input_field.textEdited.connect(lambda: self.Update_slider(self.Y_Rotation, self.Y_Rotation_input_field.text()))
        self.Z_Rotation_input_field.textEdited.connect(lambda: self.Update_slider(self.Z_Rotation, self.Z_Rotation_input_field.text()))
        
        # editingFinished callbacks that updates backend
        self.X_Rotation_input_field.editingFinished.connect(self.update_object_rotation)
        self.Y_Rotation_input_field.editingFinished.connect(self.update_object_rotation)
        self.Z_Rotation_input_field.editingFinished.connect(self.update_object_rotation)
        
        self.X_Rotation.sliderMoved.connect(lambda val: self.Slider_Update(val, self.X_Rotation_input_field))
        self.Y_Rotation.sliderMoved.connect(lambda val: self.Slider_Update(val, self.Y_Rotation_input_field))
        self.Z_Rotation.sliderMoved.connect(lambda val: self.Slider_Update(val, self.Z_Rotation_input_field))

        self.X_Rotation.sliderReleased.connect(self.update_object_rotation)
        self.Y_Rotation.sliderReleased.connect(self.update_object_rotation)
        self.Z_Rotation.sliderReleased.connect(self.update_object_rotation)
        
        #########################################

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
            shared_state.itemNames[selected_object_index]
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
            shared_state.itemNames[selected_object_index]
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
            shared_state.itemNames[selected_object_index]
            obj = shared_state.items[selected_object_index]
            #print(obj)
            obj.set_rotation(rotation)
        except:
            print("Error Updating Rotation, X, Y or Z value is invalid")
    
    
    def Plus_click(self, field):
        if field.isEnabled():
            """Updates field value"""
            try:
                val = float(field.text()) + 1
                field.setText(str(val))
                field.editingFinished.emit()
            except:
                field.setText(str(0.0))
                field.editingFinished.emit()
        
        
    def Minus_click(self, field):
        if field.isEnabled():
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
        if field.isEnabled():
            if field.text() == '':
                field.setText('0')
            if float(field.text()) > val or float(field.text()) + 0.5 < val:
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

        self.Pivot_Point_Check.setToolTip('Custom pivot point values')
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
        
        self.Distance_Pivot.setToolTip('Changes Distance from camrea to object')
        
        self.Distance_Slider = QtWidgets.QSlider(self)
        self.Distance_Slider.setPageStep(0)
        self.Distance_Slider.setOrientation(QtCore.Qt.Horizontal)
        self.Distance_Slider.setRange(0, 100)

        self.Distance_Pivot_input_field.textEdited.connect(lambda: self.Update_slider(self.Distance_Slider, self.Distance_Pivot_input_field.text()))
        self.Distance_Pivot_input_field.editingFinished.connect(self.update_distance)
        self.Distance_Pivot_input_field.setText("10")
        self.Distance_Slider.setValue(10)
        #################
        self.Distance_Slider.sliderMoved.connect(lambda val: self.Slider_Update(val, self.Distance_Pivot_input_field))
        self.Distance_Slider.sliderReleased.connect(self.update_distance)
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
        shared_state.items_updated.connect(lambda: self.update_combo_box_items(shared_state.itemNames))
        shared_state.selection_changed.connect(self.combo_box.setCurrentIndex)
        self.combo_box.activated.connect(lambda: self.Object_pivot_selected(self.Pivot_Point_Check, [self.XPivot_point_input_field, self.YPivot_point_input_field, self.ZPivot_point_input_field], [self.XPivot_button_minus, self.XPivot_button_plus, self.YPivot_button_minus, self.YPivot_button_plus,self.ZPivot_button_plus, self.ZPivot_button_minus]))
        
        # initialise items
        self.update_combo_box_items(shared_state.itemNames)
        shared_state.update_items(items=[])
        shared_state.update_selected(0)
        
        self.combo_box.setToolTip('Changes the object selected')

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

        main_layout.addWidget(self.Distance_Pivot, 1, 4)
        main_layout.addWidget(self.Distance_Pivot_input_field, 1, 5)
        main_layout.addWidget(self.Distance_Slider, 1, 6)

        main_layout.addWidget(self.combo_box, 0, 7)

        self.setLayout(main_layout)



    def update_ui_by_config(self):
        """ Method that updates attributes in text field when the object index is change from combo box. """

        cfg = backend.get_config()
        
        self.Distance_Pivot_input_field.setText(str(cfg["pivot"]["dis"]))
        self.XPivot_point_input_field.setText(str(cfg["pivot"]["point"][0]))
        self.YPivot_point_input_field.setText(str(cfg["pivot"]["point"][1]))
        self.ZPivot_point_input_field.setText(str(cfg["pivot"]["point"][2]))
        self.Pivot_Point_Check.setChecked(True)
        self.combo_box.setCurrentIndex(-1)
        if cfg["objects"] != []:
            self.combo_box.setCurrentIndex(0)

        self.Update_slider(self.Distance_Slider, self.Distance_Pivot_input_field.text())
        
        
    def Update_slider(self, slider, val):
        try:
            slider.setValue(int(round(float(val), 0)))
        except Exception as e:
            try:
                slider.setValue(0)
            except:
                print("Error", e)
            
    def Slider_Update(self, val, field):
        """Set Field value to slider value"""
        if field.isEnabled():
            if field.text() == '':
                field.setText('0')
            if float(field.text()) > val or float(field.text()) + 0.5 < val:
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
        if field.isEnabled():
            try:
                val = float(field.text()) + 1
                field.setText(str(val))
                field.editingFinished.emit()
            except:
                field.setText(str(0.0))
                field.editingFinished.emit()
        
        
    def Minus_click(self, field):
        """Updates Field value"""
        if field.isEnabled():
            try:
                val = float(field.text()) - 1
                field.setText(str(val))
                field.editingFinished.emit()
            except:
                field.setText(str(0.0))
                field.editingFinished.emit()

class RandomTabDialog(QWidget):
    def __init__(self, parent: QWidget, ParentTab: QTabWidget):
        super().__init__(parent)

        tab_widget = QTabWidget()
        tab_widget.addTab(RandomDefault(self, tab_widget), "Base")
        tab_widget.addTab(RandomObject(self, ParentTab), "Object")
        tab_widget.addTab(RandomPivot(self, ParentTab), "Pivot Point")
        tab_widget.addTab(RandomRender(self, ParentTab), "Render")
        tab_widget.addTab(RandomLight(self, ParentTab), "Light")
        

        main_layout = QVBoxLayout()
        main_layout.addWidget(tab_widget)
        self.setLayout(main_layout)

class RandomDefault(QWidget):
    def __init__(self, parent: QWidget, tab_widget: QTabWidget):
        super().__init__(parent)

        main_layout = QGridLayout()
        Field = QCheckBox("Set ALL RANDOM", self)
        Field.setToolTip('Sets all elements on all pages to random') 

        SetSetCheck = QCheckBox("Set per SET")
        SetSetCheck.setToolTip('Each selected field is randomly generated and its value is maintained throughout the entire set generation.') 
        SetFrameCheck = QCheckBox("Set per FRAME")
        SetFrameCheck.setToolTip('Each selected field is randomly generated and its value is changed for each frame.') 
        RandomSeed = QLineEdit("", self)
        RandomSeed.setText(str(backend.get_config()["seed"]))
        RandomSeed.setMaximumWidth(200)
        
        main_layout.addWidget(Field, 0, 0)
        main_layout.addWidget(SetSetCheck, 1, 0)
        main_layout.addWidget(SetFrameCheck, 2, 0)
        SetSetCheck.toggled.connect(lambda: self.SetSETChecks(main_layout))
        SetFrameCheck.toggled.connect(lambda: self.SetFRAMEChecks(main_layout))
        SetSetCheck.setChecked(True)
        main_layout.addWidget(RandomSeed, 3, 0)
        main_layout.setAlignment(Qt.AlignTop | Qt.AlignRight)
        
        Field.toggled.connect(lambda state: self.checkUpdate(tab_widget, state))
        RandomSeed.editingFinished.connect(lambda: self.SeedEdit(RandomSeed))
        
        self.setLayout(main_layout)


    def SetSETChecks(self, Layout):
        if Layout.itemAtPosition(1, 0).widget().isChecked():
            Layout.itemAtPosition(2, 0).widget().setChecked(False)
        self.notXOR(Layout)
    
    def SetFRAMEChecks(self, Layout):
        if Layout.itemAtPosition(2, 0).widget().isChecked():
            Layout.itemAtPosition(1, 0).widget().setChecked(False)
        self.notXOR(Layout)

    def notXOR(self, Layout):
        if (not Layout.itemAtPosition(1, 0).widget().isChecked()) == (not Layout.itemAtPosition(2, 0).widget().isChecked()):
            Layout.itemAtPosition(1, 0).widget().setChecked(True)
        
    def checkUpdate(self, tab_widget, State):
        """Method to update all Random checkboxes"""
        """
        Tab navbar -> Page -> QgridLayout -> Widget(Y position, X position) -> QCheckBox -> State
        tab_widget -> tab_widget.widget(i) -> widget.layout() -> widget.layout().itemAtPosition(position[1], position[0]) -> widget.layout().itemAtPosition(position[1], position[0]).widget() -> widget.layout().itemAtPosition(position[1], position[0]).widget().setChecked(State)
        """
        for i in range(1, tab_widget.count()):
            widget = tab_widget.widget(i)
            for Field, position in widget.CheckBoxes.items():
                widget.layout().itemAtPosition(position[1], position[0]).widget().setChecked(State)
                
    def SeedEdit(self, field):
        """Updates field value"""
        try:
            val = int(field.text())
            field.setText(str(val))
        except ValueError:
            field.setText(str(backend.get_config()["seed"]))
            field.setToolTip('Random seed') 
                            
class RandomObject(QWidget):
    def __init__(self, parent: QWidget, ParentTab: QTabWidget):
        super().__init__(parent)

        self.CheckBoxes = {}
        self.LowerBounds = {}
        self.UpperBounds = {}

        main_layout = QGridLayout()
        
        # create initial combo_box
        self.combo_box = QComboBox(self)
        # connecting shared state updates to combo box
        shared_state.items_updated.connect(lambda: self.update_combo_box_items(shared_state.itemNames))
        shared_state.selection_changed.connect(self.combo_box.setCurrentIndex)
        #self.combo_box.currentIndexChanged.connect(self.on_object_selected)

        # initialise items
        self.update_combo_box_items(shared_state.itemNames)
        shared_state.update_items(items=[])
        shared_state.update_selected(0)
        
        main_layout.addWidget(self.combo_box, 0, 10)
        
        main_layout.addWidget(QCheckBox("Set all random", self), 1, 10)
        main_layout.itemAtPosition(1, 10).widget().toggled.connect(lambda:
             self.set_all_random(main_layout, main_layout.itemAtPosition(1, 10).widget().isChecked()))
        
        main_layout.addWidget(QLabel("Co-ords:", self), 0, 0)
        self.gen_field("X", main_layout, 0, 1, self.connFields(ParentTab, 1, 1))
        self.gen_field("Y", main_layout, 0, 2, self.connFields(ParentTab, 1, 2))
        self.gen_field("Z", main_layout, 0, 3, self.connFields(ParentTab, 1, 3))

        main_layout.addWidget(QLabel("Rotation", self), 0, 3)
        self.gen_field("Pitch", main_layout, 3, 1, self.connFields(ParentTab, 5, 1))
        self.gen_field("Roll", main_layout, 3, 2, self.connFields(ParentTab, 5, 2))
        self.gen_field("Yaw", main_layout, 3, 3, self.connFields(ParentTab, 5, 3))
        
        main_layout.addWidget(QLabel("Scale", self), 0, 7)
        self.gen_field("Width", main_layout, 6, 1, self.connFields(ParentTab, 8, 1))
        self.gen_field("Height", main_layout, 6, 2, self.connFields(ParentTab, 8, 2))
        self.gen_field("Length", main_layout, 6, 3, self.connFields(ParentTab, 8, 3))
        
        self.setLayout(main_layout)

    def gen_field(self, Fieldname, Layout, X, Y, ConField):
        """Generate a field including checkbox and 2 input fields"""
        Field = QCheckBox(Fieldname, self)
        Field_LowerBound = QLineEdit(parent=self)
        Field_UpperBound = QLineEdit(parent=self)
        
        Field_LowerBound.setToolTip('LowerBound') 
        Field_UpperBound.setToolTip('UpperBound') 

        self.addCheck(Field, Fieldname, Layout, X, Y, ConField)
        self.addLower(Field_LowerBound, Fieldname, Layout, X+1, Y)
        self.addUpper(Field_UpperBound, Fieldname, Layout, X+2, Y)
        Field_LowerBound.editingFinished.connect(lambda: self.validation(Field_LowerBound))
        Field_UpperBound.editingFinished.connect(lambda: self.validation(Field_UpperBound))

        Field.toggled.connect(lambda: self.un_checked(Field.isChecked(), Field_LowerBound, Field_UpperBound))
        self.un_checked(False, Field_LowerBound, Field_UpperBound)
        
    def addCheck(self, Field, Fieldname, Layout, X, Y, ConField):
        """Generate checkbox"""
        Layout.addWidget(Field, Y, X)
        self.CheckBoxes[f"{Layout.itemAtPosition(0, 10).widget().currentText()}{Fieldname}"] = (X, Y)
        Layout.itemAtPosition(Y, X).widget().toggled.connect(lambda: self.setAbled(ConField, Layout.itemAtPosition(Y, X).widget().isChecked()))
        
    def setAbled(self, Field, State):
        """Connect Checkbox to correlating page field"""
        Field.setEnabled(not State)
        
    def connFields(self, ParentTab, X, Y):
        return ParentTab.widget(0).layout().itemAtPosition(Y, X).widget()

    def addLower(self, Field, Fieldname, Layout, X, Y):
        """Generate Lowerbound Field"""
        Layout.addWidget(Field, Y, X)
        self.LowerBounds[f"{Layout.itemAtPosition(0, 10).widget().currentText()}{Fieldname}"] = (X, Y)
        
    def addUpper(self, Field, Fieldname, Layout, X, Y):
        """Generate Upperbound Field"""
        Layout.addWidget(Field, Y, X)
        self.UpperBounds[f"{Layout.itemAtPosition(0, 10).widget().currentText()}{Fieldname}"] = (X, Y)

    def un_checked(self, State, Field_LowerBound, Field_UpperBound):
        "Sets field to checkbox status"
        Field_LowerBound.setEnabled(State)
        Field_UpperBound.setEnabled(State)

    def set_all_random(self, main_layout, State):
        """Set all elements on page to active"""
        for keys in self.CheckBoxes.keys():
            main_layout.itemAtPosition(self.CheckBoxes[keys][1], self.CheckBoxes[keys][0]).widget().setChecked(State)

    def validation(self, Field):
        if Field.isEnabled():
            """Updates field value"""
            try:
                val = float(Field.text())
                Field.setText(str(val))
            except:
                Field.setText("")

    def update_combo_box_items(self, items):
        """ Method could be called to update combo_box_items. Maybe Delete. """
        self.combo_box.clear()
        self.combo_box.addItems(map(lambda o: str(o), items))
        
    def on_object_selected(self, selected_object_pos):
        """ Method could be called to update combo_box_items. Maybe Delete. """
        pass

class RandomPivot(QWidget):
    def __init__(self, parent: QWidget, ParentTab: QTabWidget):
        super().__init__(parent)

        self.CheckBoxes = {}
        self.LowerBounds = {}
        self.UpperBounds = {}

        main_layout = QGridLayout()
        
        # create initial combo_box
        self.combo_box = QComboBox(self)
        # connecting shared state updates to combo box
        shared_state.items_updated.connect(lambda: self.update_combo_box_items(shared_state.itemNames))
        shared_state.selection_changed.connect(self.combo_box.setCurrentIndex)
        #self.combo_box.currentIndexChanged.connect(self.on_object_selected)

        # initialise items
        self.update_combo_box_items(shared_state.itemNames)
        shared_state.update_items(items=[])
        shared_state.update_selected(0)

        main_layout.addWidget(self.combo_box, 0, 10)

        main_layout.addWidget(QCheckBox("Set all random", self), 1, 10)
        main_layout.itemAtPosition(1, 10).widget().toggled.connect(lambda:
             self.set_all_random(main_layout, main_layout.itemAtPosition(1, 10).widget().isChecked()))

        main_layout.addWidget(QLabel("Co-ords:", self), 0, 0)
        self.gen_field("X", main_layout, 0, 1, self.connFields(ParentTab, 1, 1))
        self.gen_field("Y", main_layout, 0, 2, self.connFields(ParentTab, 1, 2))
        self.gen_field("Z", main_layout, 0, 3, self.connFields(ParentTab, 1, 3))

        main_layout.addWidget(QLabel("Distnace", self), 0, 3)
        self.gen_field("Measurement", main_layout, 3, 1, self.connFields(ParentTab, 5, 1))
        
        self.setLayout(main_layout)

    def gen_field(self, Fieldname, Layout, X, Y, ConField):
        Field = QCheckBox(Fieldname, self)
        Field_LowerBound = QLineEdit(parent=self)
        Field_UpperBound = QLineEdit(parent=self)
        
        Field_LowerBound.setToolTip('LowerBound') 
        Field_UpperBound.setToolTip('UpperBound') 

        self.addCheck(Field, Fieldname, Layout, X, Y, ConField)
        self.addLower(Field_LowerBound, Fieldname, Layout, X+1, Y)
        self.addUpper(Field_UpperBound, Fieldname, Layout, X+2, Y)
        Field_LowerBound.editingFinished.connect(lambda: self.validation(Field_LowerBound))
        Field_UpperBound.editingFinished.connect(lambda: self.validation(Field_UpperBound))

        Field.toggled.connect(lambda: self.un_checked(Field.isChecked(), Field_LowerBound, Field_UpperBound))
        self.un_checked(False, Field_LowerBound, Field_UpperBound)

    def validation(self, Field):
        if Field.isEnabled():
            """Updates field value"""
            try:
                val = float(Field.text())
                Field.setText(str(val))
            except:
                Field.setText("")
        
    def addCheck(self, Field, Fieldname, Layout, X, Y, ConField):
        Layout.addWidget(Field, Y, X)
        self.CheckBoxes[f"{Layout.itemAtPosition(0, 10).widget().currentText()}{Fieldname}"] = (X, Y)
        Layout.itemAtPosition(Y, X).widget().toggled.connect(lambda: self.setAbled(ConField, Layout.itemAtPosition(Y, X).widget().isChecked()))
        
    def setAbled(self, Field, State):
        """Connect Checkbox to correlating page field"""
        Field.setEnabled(not State)
        
    def connFields(self, ParentTab, X, Y):
        return ParentTab.widget(1).layout().itemAtPosition(Y, X).widget()
    
    def addLower(self, Field, Fieldname, Layout, X, Y):
        Layout.addWidget(Field, Y, X)
        self.LowerBounds[f"{Layout.itemAtPosition(0, 10).widget().currentText()}{Fieldname}"] = (X, Y)
        
    def addUpper(self, Field, Fieldname, Layout, X, Y):
        Layout.addWidget(Field, Y, X)
        self.UpperBounds[f"{Layout.itemAtPosition(0, 10).widget().currentText()}{Fieldname}"] = (X, Y)

    def un_checked(self, State, Field_LowerBound, Field_UpperBound):
        Field_LowerBound.setEnabled(State)
        Field_UpperBound.setEnabled(State)

    def set_all_random(self, main_layout, State):
        for keys in self.CheckBoxes.keys():
            main_layout.itemAtPosition(self.CheckBoxes[keys][1], self.CheckBoxes[keys][0]).widget().setChecked(State)

    def update_combo_box_items(self, items):
        """ Method could be called to update combo_box_items. Maybe Delete. """
        self.combo_box.clear()
        self.combo_box.addItems(map(lambda o: str(o), items))
        
    def on_object_selected(self, selected_object_pos):
        """ Method could be called to update combo_box_items. Maybe Delete. """
        pass

class RandomRender(QWidget):
    def __init__(self, parent: QWidget, ParentTab: QTabWidget):
        super().__init__(parent)

        self.CheckBoxes = {}
        self.LowerBounds = {}
        self.UpperBounds = {}

        main_layout = QGridLayout()
        
        # create initial combo_box
        self.combo_box = QComboBox(self)
        # connecting shared state updates to combo box
        shared_state.items_updated.connect(lambda: self.update_combo_box_items(shared_state.itemNames))
        shared_state.selection_changed.connect(self.combo_box.setCurrentIndex)
        #self.combo_box.currentIndexChanged.connect(self.on_object_selected)

        # initialise items
        self.update_combo_box_items(shared_state.itemNames)
        shared_state.update_items(items=[])
        shared_state.update_selected(0)

        main_layout.addWidget(self.combo_box, 0, 10)
        
        main_layout.addWidget(QCheckBox("Set all random", self), 1, 10)
        main_layout.itemAtPosition(1, 10).widget().toggled.connect(lambda:
             self.set_all_random(main_layout, main_layout.itemAtPosition(1, 10).widget().isChecked()))

        main_layout.addWidget(QLabel("Degrees of Change:", self), 0, 0)
        self.gen_field("X", main_layout, 0, 1, self.connFields(ParentTab, 4, 1))
        self.gen_field("Y", main_layout, 0, 2, self.connFields(ParentTab, 4, 2))
        self.gen_field("Z", main_layout, 0, 3, self.connFields(ParentTab, 4, 3))

        main_layout.addWidget(QLabel("Render", self), 0, 3)
        self.gen_field("Quantity", main_layout, 3, 1, self.connFields(ParentTab, 0, 1))

        self.setLayout(main_layout)

    def gen_field(self, Fieldname, Layout, X, Y, ConField):
        Field = QCheckBox(Fieldname, self)
        Field_LowerBound = QLineEdit(parent=self)
        Field_UpperBound = QLineEdit(parent=self)
        
        Field_LowerBound.setToolTip('LowerBound') 
        Field_UpperBound.setToolTip('UpperBound') 

        self.addCheck(Field, Fieldname, Layout, X, Y, ConField)
        self.addLower(Field_LowerBound, Fieldname, Layout, X+1, Y)
        self.addUpper(Field_UpperBound, Fieldname, Layout, X+2, Y)
        Field_LowerBound.editingFinished.connect(lambda: self.validation(Field_LowerBound))
        Field_UpperBound.editingFinished.connect(lambda: self.validation(Field_UpperBound))

        Field.toggled.connect(lambda: self.un_checked(Field.isChecked(), Field_LowerBound, Field_UpperBound))
        self.un_checked(False, Field_LowerBound, Field_UpperBound)
        
    def addCheck(self, Field, Fieldname, Layout, X, Y, ConField):
        Layout.addWidget(Field, Y, X)
        self.CheckBoxes[f"{Layout.itemAtPosition(0, 10).widget().currentText()}{Fieldname}"] = (X, Y)
        Layout.itemAtPosition(Y, X).widget().toggled.connect(lambda: self.setAbled(ConField, Layout.itemAtPosition(Y, X).widget().isChecked()))
    
    def validation(self, Field):
        if Field.isEnabled():
            """Updates field value"""
            try:
                val = float(Field.text())
                Field.setText(str(val))
            except:
                Field.setText("")

    def setAbled(self, Field, State):
        """Connect Checkbox to correlating page field"""
        Field.setEnabled(not State)
        
    def connFields(self, ParentTab, X, Y):
        return ParentTab.widget(2).layout().itemAtPosition(Y, X).widget()

    def addLower(self, Field, Fieldname, Layout, X, Y):
        Layout.addWidget(Field, Y, X)
        self.LowerBounds[f"{Layout.itemAtPosition(0, 10).widget().currentText()}{Fieldname}"] = (X, Y)
        
    def addUpper(self, Field, Fieldname, Layout, X, Y):
        Layout.addWidget(Field, Y, X)
        self.UpperBounds[f"{Layout.itemAtPosition(0, 10).widget().currentText()}{Fieldname}"] = (X, Y)

    def un_checked(self, State, Field_LowerBound, Field_UpperBound):
        Field_LowerBound.setEnabled(State)
        Field_UpperBound.setEnabled(State)

    def set_all_random(self, main_layout, State):
        for keys in self.CheckBoxes.keys():
            main_layout.itemAtPosition(self.CheckBoxes[keys][1], self.CheckBoxes[keys][0]).widget().setChecked(State)

    def update_combo_box_items(self, items):
        """ Method could be called to update combo_box_items. Maybe Delete. """
        self.combo_box.clear()
        self.combo_box.addItems(map(lambda o: str(o), items))
        
    def on_object_selected(self, selected_object_pos):
        """ Method could be called to update combo_box_items. Maybe Delete. """
        pass


class RandomLight(QWidget):
    def __init__(self, parent: QWidget, ParentTab: QTabWidget):
        super().__init__(parent)

        self.CheckBoxes = {}
        self.LowerBounds = {}
        self.UpperBounds = {}

        main_layout = QGridLayout()
        
        # create initial combo_box
        self.combo_box = QComboBox(self)
        # connecting shared state updates to combo box
        shared_state.items_updated.connect(lambda: self.update_combo_box_items(shared_state.itemNames))
        shared_state.selection_changed.connect(self.combo_box.setCurrentIndex)
        #self.combo_box.currentIndexChanged.connect(self.on_object_selected)

        # initialise items
        self.update_combo_box_items(shared_state.itemNames)
        shared_state.update_items(items=[])
        shared_state.update_selected(0)

        main_layout.addWidget(self.combo_box, 0, 12)
        
        main_layout.addWidget(QCheckBox("Set all random", self), 1, 12)
        main_layout.itemAtPosition(1, 12).widget().toggled.connect(lambda:
             self.set_all_random(main_layout, main_layout.itemAtPosition(1, 12).widget().isChecked()))

        main_layout.addWidget(QLabel("Co-ords:", self), 0, 0)
        self.gen_field("X", main_layout, 0, 1, self.connFields(ParentTab, 5, 1))
        self.gen_field("Y", main_layout, 0, 2, self.connFields(ParentTab, 5, 2))
        self.gen_field("Z", main_layout, 0, 3, self.connFields(ParentTab, 5, 3))

        main_layout.addWidget(QLabel("Angle", self), 0, 3)
        self.gen_field("Pitch", main_layout, 3, 1, self.connFields(ParentTab, 9, 1))
        self.gen_field("Roll", main_layout, 3, 2, self.connFields(ParentTab, 9, 2))
        self.gen_field("Yaw", main_layout, 3, 3, self.connFields(ParentTab, 9, 3))
        
        main_layout.addWidget(QLabel("Angle", self), 0, 7)
        self.gen_field("Strength", main_layout, 6, 1, self.connFields(ParentTab, 1, 0))
        self.gen_field("Radius", main_layout, 6, 2, self.connFields(ParentTab, 1, 2))
        self.gen_field("Colour", main_layout, 6, 3, self.connFields(ParentTab, 2, 1))

        #self.gen_field("BackGround", main_layout, 9, 1)

        #print(main_layout.itemAtPosition(0, 0).widget().setText("Electric boogalo"))
        #how to change values

        self.setLayout(main_layout)
        
    def gen_field(self, Fieldname, Layout, X, Y, ConField):
        Field = QCheckBox(Fieldname, self)
        Field_LowerBound = QLineEdit(parent=self)
        Field_UpperBound = QLineEdit(parent=self)
        
        Field_LowerBound.setToolTip('LowerBound') 
        Field_UpperBound.setToolTip('UpperBound') 

        self.addCheck(Field, Fieldname, Layout, X, Y, ConField)
        self.addLower(Field_LowerBound, Fieldname, Layout, X+1, Y)
        self.addUpper(Field_UpperBound, Fieldname, Layout, X+2, Y)
        Field_LowerBound.editingFinished.connect(lambda: self.validation(Field_LowerBound))
        Field_UpperBound.editingFinished.connect(lambda: self.validation(Field_UpperBound))

        Field.toggled.connect(lambda: self.un_checked(Field.isChecked(), Field_LowerBound, Field_UpperBound))
        self.un_checked(False, Field_LowerBound, Field_UpperBound)

    def addCheck(self, Field, Fieldname, Layout, X, Y, ConField):
        Layout.addWidget(Field, Y, X)
        self.CheckBoxes[f"{Layout.itemAtPosition(0, 12).widget().currentText()}{Fieldname}"] = (X, Y)
        Layout.itemAtPosition(Y, X).widget().toggled.connect(lambda: self.setAbled(ConField, Layout.itemAtPosition(Y, X).widget().isChecked()))
    
    def validation(self, Field):
        if Field.isEnabled():
            """Updates field value"""
            try:
                val = float(Field.text())
                Field.setText(str(val))
            except:
                Field.setText("")

    def setAbled(self, Field, State):
        """Connect Checkbox to correlating page field"""
        Field.setEnabled(not State)
        
    def connFields(self, ParentTab, X, Y):
        return ParentTab.widget(3).layout().itemAtPosition(Y, X).widget()

    def addLower(self, Field, Fieldname, Layout, X, Y):
        Layout.addWidget(Field, Y, X)
        self.LowerBounds[f"{Layout.itemAtPosition(0, 12).widget().currentText()}{Fieldname}"] = (X, Y)
        
    def addUpper(self, Field, Fieldname, Layout, X, Y):
        Layout.addWidget(Field, Y, X)
        self.UpperBounds[f"{Layout.itemAtPosition(0, 12).widget().currentText()}{Fieldname}"] = (X, Y)

    def un_checked(self, State, Field_LowerBound, Field_UpperBound):
        Field_LowerBound.setEnabled(State)
        Field_UpperBound.setEnabled(State)

    def set_all_random(self, main_layout, State):
        for keys in self.CheckBoxes.keys():
            main_layout.itemAtPosition(self.CheckBoxes[keys][1], self.CheckBoxes[keys][0]).widget().setChecked(State)
            
    def update_combo_box_items(self, items):
        """ Method could be called to update combo_box_items. Maybe Delete. """
        self.combo_box.clear()
        self.combo_box.addItems(map(lambda o: str(o), items))
        
    def on_object_selected(self, selected_object_pos):
        """ Method could be called to update combo_box_items. Maybe Delete. """
        pass


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
        self.Degree_Change_title.setToolTip('Changes the degrees changed per Frame')

        # X Degree
        self.X_Degree_Label = QLabel("X:", self)
        self.X_Degree_input_field = QLineEdit(parent=self)
        self.X_Degree_input_field.setText("1")
        self.X_Degree_input_field.editingFinished.connect(self.set_angles)
        self.X_Degree_slider = QtWidgets.QSlider(self)
        self.X_Degree_slider.setPageStep(0)
        self.X_Degree_slider.setOrientation(QtCore.Qt.Horizontal)
        self.X_Degree_slider.setMinimum(1) 
        self.X_Degree_slider.setMaximum(360)

        # Y Degree
        self.Y_Degree_Label = QLabel("Y:", self)
        self.Y_Degree_input_field = QLineEdit(parent=self)
        self.Y_Degree_slider = QtWidgets.QSlider(self)
        self.Y_Degree_input_field.setText("1")
        self.Y_Degree_input_field.editingFinished.connect(self.set_angles)
        self.Y_Degree_slider.setPageStep(0)
        self.Y_Degree_slider.setOrientation(QtCore.Qt.Horizontal)
        self.Y_Degree_slider.setMinimum(1)
        self.Y_Degree_slider.setMaximum(360)

        # Z Degree
        self.Z_Degree_Label = QLabel("Z:", self)
        self.Z_Degree_input_field = QLineEdit(parent=self)
        self.Z_Degree_input_field.setText("1")
        self.Z_Degree_input_field.editingFinished.connect(self.set_angles)
        self.Z_Degree_slider = QtWidgets.QSlider(self)
        self.Z_Degree_slider.setPageStep(0)
        self.Z_Degree_slider.setOrientation(QtCore.Qt.Horizontal)
        self.Z_Degree_slider.setMinimum(1)
        self.Z_Degree_slider.setMaximum(360)

        self.X_Degree_input_field.textEdited.connect(lambda: self.Update_slider(self.X_Degree_slider, self.X_Degree_input_field.text()))
        self.Y_Degree_input_field.textEdited.connect(lambda: self.Update_slider(self.Y_Degree_slider, self.Y_Degree_input_field.text()))
        self.Z_Degree_input_field.textEdited.connect(lambda: self.Update_slider(self.Z_Degree_slider, self.Z_Degree_input_field.text()))

        self.X_Degree_slider.sliderMoved.connect(lambda val: self.Slider_Update(val, self.X_Degree_input_field))
        self.Y_Degree_slider.sliderMoved.connect(lambda val: self.Slider_Update(val, self.Y_Degree_input_field))
        self.Z_Degree_slider.sliderMoved.connect(lambda val: self.Slider_Update(val, self.Z_Degree_input_field))

        self.X_Degree_slider.sliderReleased.connect(self.set_angles)
        self.Y_Degree_slider.sliderReleased.connect(self.set_angles)
        self.Z_Degree_slider.sliderReleased.connect(self.set_angles)

        self.unlimited_render_button = QPushButton("Unlimited Renders", self)
        self.unlimited_render_button.setCheckable(True)
        self.unlimited_render_button.clicked.connect(self.unlimitedrender)
        
        self.unlimited_render_button.setToolTip('Generates Frames until interupted')

        self.rendering = False

        main_layout = QGridLayout()

        main_layout.addWidget(self.Number_of_renders_title, 0, 0)

        main_layout.addWidget(self.Number_of_renders_input_field, 1, 0)
        main_layout.addWidget(self.Number_of_renders_minus, 1, 1)
        main_layout.addWidget(self.Number_of_renders_plus, 1, 2)

        main_layout.addWidget(self.Degree_Change_title, 0, 3)

        main_layout.addWidget(self.X_Degree_Label, 1, 3)
        main_layout.addWidget(self.X_Degree_input_field, 1, 4)
        main_layout.addWidget(self.X_Degree_slider, 1, 5)

        main_layout.addWidget(self.Y_Degree_Label, 2, 3)
        main_layout.addWidget(self.Y_Degree_input_field, 2, 4)
        main_layout.addWidget(self.Y_Degree_slider, 2, 5)

        main_layout.addWidget(self.Z_Degree_Label, 3, 3)
        main_layout.addWidget(self.Z_Degree_input_field, 3, 4)
        main_layout.addWidget(self.Z_Degree_slider, 3, 5)

        main_layout.addWidget(self.unlimited_render_button, 1, 7)

        main_layout.addWidget(self.GenerateRenders_Button, 0, 7)

        self.setLayout(main_layout)
    
    def unlimitedrender(self):
        test = True
        while True:
            if (self.rendering):
                loop = QEventLoop()
                QTimer.singleShot(2000, loop.quit)
                loop.exec()
                continue
            if self.unlimited_render_button.isChecked():
                self.Number_of_renders_input_field.setText("1")
                self.generate_render()
            else:
                test = False

    def update_ui_by_config(self):
        """ Method that updates attributes in text field when the object index is change from combo box. """

        cfg = backend.get_config()

        self.X_Degree_input_field.setText(str(cfg["render"]["degree"][0]))
        self.Y_Degree_input_field.setText(str(cfg["render"]["degree"][2]))
        self.Z_Degree_input_field.setText(str(cfg["render"]["degree"][1]))
        self.Number_of_renders_input_field.setText(str(cfg["render"]["renders"]))

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
            
    def Slider_Update(self, val, field):
        """Set Field value to slider value"""
        if field.isEnabled():
            if field.text() == '':
                field.setText('0')
            if float(field.text()) > val or float(field.text()) + 0.5 < val:
                field.setText(str(val))

    def increase_count(self):
        if self.Number_of_renders_input_field.isEnabled():
            try:
                number_of_renders_value = int(self.Number_of_renders_input_field.text())
                self.Number_of_renders_input_field.setText(str(number_of_renders_value + 1))
            except:
                number_of_renders_value = 0
                self.Number_of_renders_input_field.setText(str(number_of_renders_value))
            self.Number_of_renders_input_field.editingFinished.emit()

    def decrease_count(self):
        if self.Number_of_renders_input_field.isEnabled():
            try:
                number_of_renders_value = int(self.Number_of_renders_input_field.text())
                if number_of_renders_value > 1:  # Prevent negative values if needed
                    self.Number_of_renders_input_field.setText(str(number_of_renders_value - 1))
            except:
                number_of_renders_value = 0
                self.Number_of_renders_input_field.setText(str(number_of_renders_value))
            self.Number_of_renders_input_field.editingFinished.emit()

        
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
        try: 
            backend.set_angles( [float(self.X_Degree_input_field.text()), float(self.Z_Degree_input_field.text()), float(self.Y_Degree_input_field.text())] )
        except:
            print("Error")

class Port(QWidget):
    def __init__(self, parent: QWidget, tab_widget: QTabWidget):
        super().__init__(parent)

        
        class ilyaMessageBox(QMessageBox):
                def __init__(self, text, title):
                    super().__init__()
                    self.setText(text)
                    self.setWindowTitle(title)
                    self.exec()

        #First Section
        def Get_Object_Filepath():
            import_box = QMessageBox()
            import_box.setText("How would you like to import objects?")
            import_box.addButton("Multiple Files", QMessageBox.ActionRole)
            import_box.addButton("Folder", QMessageBox.ActionRole)
            import_box.addButton("Cancel", QMessageBox.RejectRole)
            
            import_box.exec()
            clicked_button = import_box.clickedButton().text()
            
            try:
                if clicked_button == "Multiple Files":
                    paths = QFileDialog.getOpenFileNames(self, 'Open files', 'c:\\', "3D Model (*.blend *.stl *.obj)")[0]
                    if not paths:
                        return
                    
                    for path in paths:
                        obj = backend.RenderObject(filepath=path)
                        shared_state.add_item(obj)

                elif clicked_button == "Entire Folder":
                    folder_path = QFileDialog.getExistingDirectory(self, 'Select Folder', 'c:\\')
                    if not folder_path:
                        return
                    
                    # maybe have a global constant of supported extensions?
                    supported_extensions = ['.blend', '.stl', '.obj']
                    # go through each file in directory
                    for root, _, files in os.walk(folder_path):
                        for file in files:
                            if any(file.lower().endswith(ext) for ext in supported_extensions):
                                full_path = os.path.join(root, file)
                                obj = backend.RenderObject(filepath=full_path)
                                shared_state.add_item(obj)


                Object_detect(tab_widget)

                success_box = ilyaMessageBox("Object imported successfully.", "Success")

            except Exception:
                QMessageBox.warning(self, "Error when reading model", "The selected file is corrupt or invalid.")


            except Exception as e:
                QMessageBox.warning(self, "Error when importing", f"Error: {str(e)}")
                
        self.Import_Object_Button = QPushButton("Import Objects", self)
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
            Name = self.GetName()
            try:
                obj = backend.RenderObject(primative = Tutorial_Box.clickedButton().text().upper())
                shared_state.add_item(obj, Name)

                success_box = ilyaMessageBox("Object imported successfully.", "Success")
                
                
            except:
                error_box = QMessageBox()
                error_box.setWindowTitle("Error")
                error_box.setText("Error loading tutorial object.")
                error_box.exec()

                error_box = ilyaMessageBox("Error loading tutorial object.", "Error")
                
    
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
                    success_box = ilyaMessageBox("Setting exported successfully.", "Success")
                   
            except:
                error_box = ilyaMessageBox("There was an error selecting folder, please try again.", "Error")

        #Fourth Section
        self.ExportSettings_Button = QPushButton('Export Settings', self)
        self.ExportSettings_Button.clicked.connect(Export_Settings)

        #Fifth Section
        def Get_Settings_Filepath(tab_widget):
            try:
                path = QFileDialog.getOpenFileName(self, 'Open file', 'c:\\',"Settings (*.json)")[0]
                if (path == ""): return
                backend = Backend(json_filepath = path)
                for i in range(5):
                    #self.path.tabwizard.widget(i).update_ui_by_config()
                    tab_widget(i).update_ui_by_config()

                success_box = ilyaMessageBox("Setting imported successfully.", "Success")
            except Exception:
                QMessageBox.warning(self, "Error when reading JSON", "The selected file is corrupt or invalid.")


        self.ImportSettings_Button = QPushButton('Import Settings', self)
        self.ImportSettings_Button.clicked.connect(lambda: Get_Settings_Filepath(tab_widget))

        def delete_object(tab_widget):
            to_delete = QMessageBox()
            to_delete.setText("Please select an object to remove from below")

            if (not shared_state.items):
                return QMessageBox.warning(self, "Warning", "There are no objects to delete.")

            for obj in shared_state.items:
                to_delete.addButton(str(obj), QMessageBox.ActionRole)
            
            to_delete.addButton("Cancel", QMessageBox.ActionRole)

            to_delete.exec()

            choice = str(to_delete.clickedButton().text())

            if choice != "Cancel":
                
                obj_index = int(to_delete.clickedButton().text()[-1]) - 1
                obj = shared_state.items[obj_index]
                try:
                    shared_state.remove_item(obj)
                    success_box = ilyaMessageBox("Object successfully deleted", "Success")
                    
                    del backend.get_config()["objects"][obj.object_pos]
                    # shift objects after this one down by one
                    for i in range(obj_index, len(shared_state.items)):
                        obj = shared_state.items[i]
                        obj.object_pos = i
                except:
                    error_box = ilyaMessageBox("Error deleting object", "Error")

                shared_state.items_updated.emit(shared_state.items)
                # The last object was deleted
                if (not shared_state.items):
                    Object_detect(tab_widget)
                    QMessageBox.warning(self, "Warning", "You have deleted all of the objects, object manipulation tabs have been disabled.")
    
        #Sixth section
        self.Delete_Object_Button = QPushButton('Delete Object', self)
        self.Delete_Object_Button.clicked.connect(lambda: delete_object(tab_widget))
        
        
        def select_render_folder():        
            try:
                new_path = QFileDialog.getExistingDirectory(self, "Select Folder")

                if (new_path == "" or new_path == None):
                    pass
                else:
                    backend.set_render_output_folder(new_path)
                    success_box = ilyaMessageBox("Render folder changed", "Success")

            except:
                error_box = ilyaMessageBox("Error deleting object", "Error")

        self.SelectRenderFolder_Button = QPushButton('Change Render Folder', self)
        self.SelectRenderFolder_Button.clicked.connect(select_render_folder)


        def Object_detect(tab_widget):
            State = not Backend.is_config_objects_empty(tab_widget)
            for i in range(5):
                tab_widget.setTabEnabled(i, State)

        main_layout = QGridLayout()

        main_layout.addWidget(self.TutorialObjects_Button, 0, 0)
        main_layout.addWidget(self.Import_Object_Button, 0, 1)
        main_layout.addWidget(self.Delete_Object_Button, 0, 2)
        main_layout.addWidget(self.ExportSettings_Button, 0, 3)
        main_layout.addWidget(self.ImportSettings_Button, 0, 4)
        main_layout.addWidget(self.BrowseFiles_Button, 0, 5)
        main_layout.addWidget(self.SelectRenderFolder_Button, 0, 6)

        self.setLayout(main_layout)
        
    def GetName(self):
        ObjName, State = QtWidgets.QInputDialog.getText(self, 'Input Dialog', "Enter Object Name: ")
        if State and ObjName != "":
            return ObjName
        else:
            return "Object"




class Lighting(QWidget):
    def __init__(self, parent: QWidget):
        super().__init__(parent)

        self.light = backend.RenderLight()

        ###
        self.colour_label = QLabel("Colour:", self)
        self.colour_select_button = QPushButton("Select colour", self)
        self.colour_select_button.clicked.connect(self.getColour)
        self.colour_label.setToolTip('Object lighting Colour')

        self.lighting_colour = QLineEdit(self) #f789886 & bullshit
        self.lighting_colour.textEdited.connect(lambda: self.update_colour_example_text(self.lighting_colour.text()))
        self.colour_example = QLabel(self)
        self.lighting_colour.setText("#000000")
        ###


        ###
        self.lighting_strength_label = QLabel("Strength: ", self)
        self.lighting_strength_label.setToolTip('Strength of lighting element')
        self.lighting_strength_input_field = QLineEdit(self)
        self.lighting_strength_input_field.setText("1")
        self.lighting_strength_input_field.textEdited.connect(lambda: self.Update_slider(self.strength_slider, self.lighting_strength_input_field.text()))

        self.strength_slider = QSlider(self)
        self.strength_slider.setRange(0,100)
        self.strength_slider.setOrientation(QtCore.Qt.Horizontal)
        self.strength_slider.sliderMoved.connect(lambda val: self.set_strength(val, self.lighting_strength_input_field))
        ###
        
        ###
        self.radius_label = QLabel("Radius", self)
        self.radius_label.setToolTip('Radius of lighting element')
        self.radius_input_field = QLineEdit(self)
        self.radius_input_field.setText("0")
        self.radius_input_field.textChanged.connect(lambda: self.set_radius_from_field(self.radius_input_field))
        self.radius_button_minus = QPushButton("-", self)
        #self.radius_button_minus.clicked.connect(lambda: self.Minus_click(self.radius_input_field))
        #set_radius
        self.radius_button_minus.clicked.connect(lambda: self.set_radius("Minus", self.radius_input_field))

        self.radius_button_plus = QPushButton("+", self)
        #self.radius_button_plus.clicked.connect(lambda: self.Plus_click(self.radius_input_field))
        self.radius_button_plus.clicked.connect(lambda: self.set_radius("Plus", self.radius_input_field))



        ###


        self.light_coords_label = QLabel("Lighting Co-ords:", self)
        self.light_coords_label.setToolTip('Co-ords of lighting element')
        ###
        self.Xlight_coords_label = QLabel("X:", self)
        self.Xlight_coords_input_field = QLineEdit(self)
        self.Xlight_coords_input_field.setText("0")
        self.Xlight_coords_input_field.textChanged.connect(self.set_loc_from_field)

        self.Xlight_coords_button_plus = QPushButton("+", self)
        self.Xlight_coords_button_plus.clicked.connect(lambda: self.set_loc("Plus", self.Xlight_coords_input_field))

        self.Xlight_coords_button_minus = QPushButton("-", self)
        self.Xlight_coords_button_minus.clicked.connect(lambda: self.set_loc("Minus", self.Xlight_coords_input_field))
        ###


        ###
        self.Ylight_coords_label = QLabel("Y:", self)
        self.Ylight_coords_input_field = QLineEdit(self)
        self.Ylight_coords_input_field.setText("0")
        self.Ylight_coords_input_field.textChanged.connect(self.set_loc_from_field)

        self.Ylight_coords_button_plus = QPushButton("+", self)
        self.Ylight_coords_button_plus.clicked.connect(lambda: self.set_loc("Plus", self.Ylight_coords_input_field))

        self.Ylight_coords_button_minus = QPushButton("-", self)
        self.Ylight_coords_button_minus.clicked.connect(lambda: self.set_loc("Minus", self.Ylight_coords_input_field))
        ###

        ###
        self.Zlight_coords_label = QLabel("Z:", self)
        self.Zlight_coords_input_field = QLineEdit(self)
        self.Zlight_coords_input_field.setText("0")
        self.Zlight_coords_input_field.textChanged.connect(self.set_loc_from_field)

        self.Zlight_coords_button_plus = QPushButton("+", self)
        self.Zlight_coords_button_plus.clicked.connect(lambda: self.set_loc("Plus", self.Zlight_coords_input_field))
        
        self.Zlight_coords_button_minus = QPushButton("-", self)
        self.Zlight_coords_button_minus.clicked.connect(lambda: self.set_loc("Minus", self.Zlight_coords_input_field))
        ###

        self.light_angle_label = QLabel("Lighting Angle:", self)
        self.light_angle_label.setToolTip('Angle of lighting element')
        ###
        self.Xlight_angle_label = QLabel("X:", self)
        self.Xlight_angle_input_field = QLineEdit(self)
        self.Xlight_angle_input_field.setText("0")
        self.Xlight_angle_input_field.textEdited.connect(lambda: self.set_rotation_from_field(self.Xlight_angle_slider, self.Xlight_angle_input_field.text()))


        self.Xlight_angle_slider = QSlider(self)
        self.Xlight_angle_slider.setRange(0,100)
        self.Xlight_angle_slider.setOrientation(QtCore.Qt.Horizontal)
        self.Xlight_angle_slider.sliderMoved.connect(lambda val: self.set_rotation(val, self.Xlight_angle_input_field))


        ###
        self.Ylight_angle_label = QLabel("Y:", self)
        self.Ylight_angle_input_field = QLineEdit(self)
        self.Ylight_angle_input_field.setText("0")
        self.Ylight_angle_input_field.textEdited.connect(lambda: self.set_rotation_from_field(self.Ylight_angle_slider, self.Ylight_angle_input_field.text()))

        self.Ylight_angle_slider = QSlider(self)
        self.Ylight_angle_slider.setRange(0,100)
        self.Ylight_angle_slider.setOrientation(QtCore.Qt.Horizontal)
        self.Ylight_angle_slider.sliderMoved.connect(lambda val: self.set_rotation(val, self.Ylight_angle_input_field))
        ###
        self.Zlight_angle_label = QLabel("Z:", self)
        self.Zlight_angle_input_field = QLineEdit(self)
        self.Zlight_angle_input_field.setText("0")
        self.Zlight_angle_input_field.textEdited.connect(lambda: self.set_rotation_from_field(self.Zlight_angle_slider, self.Zlight_angle_input_field.text()))

        self.Zlight_angle_slider = QSlider(self)
        self.Zlight_angle_slider.setRange(0,100)
        self.Zlight_angle_slider.setOrientation(QtCore.Qt.Horizontal)
        self.Zlight_angle_slider.sliderMoved.connect(lambda val: self.set_rotation(val, self.Zlight_angle_input_field))
       
        self.light_type_label = QLabel("Type: ", self)
        self.light_type_combobox = QComboBox(self)
        self.light_type_combobox.addItems(["POINT", "SUN", "SPOT", "AREA"])
        self.light_type_combobox.currentIndexChanged.connect(self.change_type)
        self.light_type_label.setToolTip('Type of lighting element')


        main_layout = QGridLayout()

        main_layout.addWidget(self.lighting_strength_label, 0, 0)
        main_layout.addWidget(self.lighting_strength_input_field, 0, 1)
        main_layout.addWidget(self.strength_slider, 0, 2)

        
        
        main_layout.addWidget(self.light_coords_label, 0, 4)    

        main_layout.addWidget(self.light_type_label, 3, 0)
        main_layout.addWidget(self.light_type_combobox, 3, 1)  


        main_layout.addWidget(self.Xlight_coords_label, 1, 4)
        main_layout.addWidget(self.Xlight_coords_input_field, 1, 5)
        main_layout.addWidget(self.Xlight_coords_button_plus, 1, 7)
        main_layout.addWidget(self.Xlight_coords_button_minus, 1, 6)

        main_layout.addWidget(self.Ylight_coords_label, 2, 4)
        main_layout.addWidget(self.Ylight_coords_input_field, 2, 5)
        main_layout.addWidget(self.Ylight_coords_button_plus, 2, 7)
        main_layout.addWidget(self.Ylight_coords_button_minus, 2, 6)

        main_layout.addWidget(self.Zlight_coords_label, 3, 4)
        main_layout.addWidget(self.Zlight_coords_input_field, 3, 5)
        main_layout.addWidget(self.Zlight_coords_button_plus, 3, 7)
        main_layout.addWidget(self.Zlight_coords_button_minus, 3, 6)


        main_layout.addWidget(self.light_angle_label, 0, 8)      


        main_layout.addWidget(self.Xlight_angle_label, 1, 8)
        main_layout.addWidget(self.Xlight_angle_input_field, 1, 9)
        main_layout.addWidget(self.Xlight_angle_slider, 1, 10)

        main_layout.addWidget(self.Ylight_angle_label, 2, 8)
        main_layout.addWidget(self.Ylight_angle_input_field, 2, 9)
        main_layout.addWidget(self.Ylight_angle_slider, 2, 10)

        main_layout.addWidget(self.Zlight_angle_label, 3, 8)
        main_layout.addWidget(self.Zlight_angle_input_field, 3, 9)
        main_layout.addWidget(self.Zlight_angle_slider, 3, 10)

        main_layout.addWidget(self.colour_select_button, 1, 1)
        main_layout.addWidget(self.lighting_colour, 1, 2)
        main_layout.addWidget(self.colour_example, 1 , 3)
        main_layout.addWidget(self.colour_label, 1, 0)

        main_layout.addWidget(self.radius_label, 2, 0)
        main_layout.addWidget(self.radius_input_field, 2, 1)
        main_layout.addWidget(self.radius_button_minus, 2, 2)
        main_layout.addWidget(self.radius_button_plus, 2, 3)

        self.setLayout(main_layout)


    def change_type(self):
        self.light.set_type(self.light_type_combobox.currentText())


    def set_strength(self, val, field):
        self.Slider_Update(val, field)
        try:
            self.light.set_energy(float(field.text()))
        except:
            pass


    def set_loc(self, direction, field):
        if direction == "Plus":
            self.Plus_click(field)
        elif direction == "Minus":
            self.Minus_click(field)

        x = self.Xlight_coords_input_field.text()
        y = self.Ylight_coords_input_field.text()
        z = self.Zlight_coords_input_field.text()
        try:
            self.light.set_loc([float(x),float(z),float(y)])
        except:
            pass
    
    def set_loc_from_field(self,):

        x = self.Xlight_coords_input_field.text()
        y = self.Ylight_coords_input_field.text()
        z = self.Zlight_coords_input_field.text()
        try:
            self.light.set_loc([float(x),float(z),float(y)])
        except:
            pass
        


    def set_radius(self, direction, field):
        if direction == "Plus":
            self.Plus_click(field)
        elif direction == "Minus":
            self.Minus_click(field)

        self.light.set_radius(field.text())

    def set_radius_from_field(self, field):
        try:
            self.light.set_radius(float(field.text()))
        except:
            pass

    def set_rotation(self, val, field):
        self.Slider_Update(val, field)

        x = self.Xlight_angle_input_field.text()
        y = self.Ylight_angle_input_field.text()
        z = self.Zlight_angle_input_field.text()

        self.light.set_rotation([float(x),float(z),float(y)])
        

    def getColour(self):
        colour = QColorDialog.getColor()

        self.lighting_colour.setText(colour.name())
        self.colour_example.setStyleSheet(("background-color: {c}").format(c = colour.name()))

        try:
            self.light.set_color(colour.name())
        except:
            pass


    def Minus_click(self, field):
        """Updates field value"""
        try:
            val = float(field.text()) - 1
            field.setText(str(val))
            field.editingFinished.emit()
        except:
            field.setText(str(0.0))
            field.editingFinished.emit()
    
    def Plus_click(self, field):
        """Updates field value"""
        try:
            val = float(field.text()) + 1
            field.setText(str(val))
            field.editingFinished.emit()
        except:
            field.setText(str(0.0))
            field.editingFinished.emit()

    def Slider_Update(self, val, field):
        """Set Field value to slider value"""
        if field.text() == '':
            field.setText('0')
        if float(field.text()) > val or float(field.text()) + 0.5 < val:
            field.setText(str(val))
    
    def set_rotation_from_field(self, slider, val):
        try:
            self.Update_slider(slider, val)

            x = self.Xlight_angle_input_field.text()
            y = self.Ylight_angle_input_field.text()
            z = self.Zlight_angle_input_field.text()
            
            self.light.set_rotation([float(x),float(z),float(y)])
        except:
            pass


    def Update_slider(self, slider, val):
        try:
            slider.setValue(int(round(float(val), 0)))
        except Exception as e:
            try:
                slider.setValue(0)
            except:
                print("Error", e)


    def update_colour_example_text(self, colour):
        try:
            if (len(colour) == 6 and colour[0] != "#") or (len(colour) == 7 and colour[0] == "#"): 
                if colour[0] != "#":
                    colour = "#" + colour

                
                self.light.set_color(colour)
                #print("CHANGED BACKEND")
                self.colour_example.setStyleSheet(("background-color: {c}").format(c = colour))
        except:
            pass

    def update_colour_example(self):
        try:
            colour = self.lighting_strength_input_field.text()
            self.lighting_colour.setText(colour.name())
            self.colour_example.setStyleSheet(("background-color: {c}").format(c = colour.name()))
        except:
            pass

class Settings(QWidget):
    def __init__(self, parent: QWidget, tab_widget: QTabWidget):
        super().__init__(parent)
        
        #Button Labels
        main_layout = QGridLayout()
        self.colour_scheme_button = QPushButton('Colour Theme', self)
        self.Help_button = QPushButton('Help', self)
        self.Guides = QPushButton('Guides', self)
        self.Secret_button = QPushButton('Button', self)
        

        #button clicks
        self.colour_scheme_button.clicked.connect(self.Colour_Scheme_Press)
       
        
        #button Layout
        main_layout.addWidget(self.colour_scheme_button)
        main_layout.addWidget(self.Help_button)
        main_layout.addWidget(self.Guides)
        main_layout.addWidget(self.Secret_button)
        self.setLayout(main_layout)

    def Colour_Scheme_Press(self):
        """Opens colour scheme options"""
        colour_box = QMessageBox(self)
        colour_box.setWindowTitle("Select Colour Scheme")
        colour_box.setText("Please select a colour scheme:")

        # Add buttons for different styles
        dark_mode = colour_box.addButton("Dark Mode", QMessageBox.ActionRole)
        light_mode = colour_box.addButton("Light Mode", QMessageBox.ActionRole)
        colourblind1 = colour_box.addButton("Colourblind 1", QMessageBox.ActionRole)
        colourblind2 = colour_box.addButton("Colourblind 2", QMessageBox.ActionRole)
        dyslexic = colour_box.addButton("Dyslexic Friendly", QMessageBox.ActionRole)
        colour_scheme1 = colour_box.addButton("Colour Mode 1", QMessageBox.ActionRole)
        Image_test = colour_box.addButton("Imagetest", QMessageBox.ActionRole)
        # Show the dialog
        colour_box.exec()

        # Apply styles based on button clicked
        if colour_box.clickedButton() == dark_mode:
            self.apply_stylesheet("Dark.qss")
        elif colour_box.clickedButton() == light_mode:
            self.apply_stylesheet("LightMode.qss")
        elif colour_box.clickedButton() == colourblind1:
            self.apply_stylesheet("colourblind1.qss")
        elif colour_box.clickedButton() == colourblind2:
            self.apply_stylesheet("colourblind2.qss")
        elif colour_box.clickedButton() == dyslexic:
            self.apply_stylesheet("Dyslexic.qss")
        elif colour_box.clickedButton() == colour_scheme1:
            self.apply_stylesheet("ColourScheme1.qss")
        elif colour_box.clickedButton() == Image_test:
            self.apply_stylesheet("ImageTest.qss")

    def apply_stylesheet(self, filename):
        "loads styles from style folder"
        qss_path = os.path.join(os.path.dirname(__file__), "..", "Style", filename)
        try:
            with open(qss_path, "r") as file:
                qss = file.read()
                QApplication.instance().setStyleSheet(qss)  # Apply globally
        except FileNotFoundError:
            print(f"Error: {filename} not found!")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    tab_dialog = TabDialog()
    tab_dialog.show()

    sys.exit(app.exec())