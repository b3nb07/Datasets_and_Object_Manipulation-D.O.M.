"""Importing"""

from functools import cached_property
import sys
from PyQt5 import QtCore, QtWidgets
from functools import cached_property
from PyQt5.QtCore import QSettings
from TranslationManager import translator
import json
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
from re import search as regex
from time import time

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
        # Add items to list of objects in list and display name
        self.items.append(item)
        self.itemNames.append(Name)
        self.items_updated.emit(self.items)

    def remove_item(self, item):
        # remove items to list of objects in list and display name
        self.items.remove(item)
        self.items_updated.emit(self.items)

    def remove_item(self, item):
        # Add items to list of objects in list and display name
        pos = self.items.index(item)
        self.items.remove(item)
        self.itemNames.remove(self.itemNames[pos])
        self.items_updated.emit(self.items)

    def update_selected(self, index):
        #Update current object selected
        self.selected_index = index
        # maybe delete
        self.selection_changed.emit(index)
        
    def count(self):
        #Amount of items
        return len(self.items)


class ViewportThread(QThread):
    def __init__(self, size):
        super().__init__()
        self.size = (size.width() * 0.85, size.height() * 0.7)

    finished = pyqtSignal()

    def run(self):
        old_res = backend.get_config().get("render_res")
        backend.set_res((int(self.size[0] / 4), int(self.size[1] / 4)))
        backend.render(shared_state, viewport_temp = True)
        backend.set_res(old_res)
        self.finished.emit()

class RenderThreadPreview(QThread):
    finished = pyqtSignal()
    progress = pyqtSignal(str)

    def run(self):
        self.progress.emit("Rendering...")
        backend.render(shared_state, headless = False, preview = True)
        self.finished.emit()
    

class RenderThread(QThread):
    finished = pyqtSignal()
    progress = pyqtSignal(str)

    def run(self):
        self.progress.emit("Rendering...")
        backend.render(shared_state, headless = False)
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

class ilyaStorageBox:
    def __init__(self, thread, config):
        self.thread = thread
        self.config = config



# creates this shared state
shared_state = ComboBoxState()
class TabDialog(QWidget):
    def __init__(self, parent: QWidget = None):
        super().__init__(parent)
        self.setWindowTitle("Datasets and Object Modeling")
        
        #Object side par to display current objects loaded in and allow for removal from current render without deletion
        ObjectsStatusBar = QScrollArea()
        ObjectsStatusBar.setMaximumWidth(175)

        ObjectsStatusBar.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        
        content_widget = QWidget()
        ObjLayout = QVBoxLayout(content_widget)
        ObjLayout.setAlignment(Qt.AlignTop)
        ObjectsStatusBar.setWidget(content_widget)
        ObjectsStatusBar.setWidgetResizable(True)
        
        self.tab_widget = QTabWidget()
        # NAVBAR: Add all other tabs first
        self.tab_widget.addTab(ObjectTab(self, self.tab_widget, ObjLayout), "Object")
        self.tab_widget.addTab(PivotTab(self), "Pivot Point")
        self.tab_widget.addTab(Render(self), "Render")
        self.tab_widget.addTab(Lighting(self), "Lighting")
 
        Temp_index = self.tab_widget.addTab(QWidget(), "Random")
        self.tab_widget.addTab(Port(self, self.tab_widget, ObjLayout), "Import/Export")
        self.tab_widget.addTab(Settings(self, self.tab_widget), "Settings")
        
        random_tab = RandomTabDialog(self, self.tab_widget)
        self.tab_widget.removeTab(Temp_index)
        self.tab_widget.insertTab(Temp_index, random_tab, "Random")
        translator.languageChanged.connect(self.translateUi)

        #Disable until Object is loaded
        self.tab_widget.setTabEnabled(0, False)
        self.tab_widget.setTabEnabled(1, False)
        self.tab_widget.setTabEnabled(2, False)
        self.tab_widget.setTabEnabled(3, False)
        self.tab_widget.setTabEnabled(4, False)
        self.tab_widget.setTabEnabled(5, True)


        self.tab_widget.setMaximumHeight(250)
        
        # enviroment
        self.environment = QWidget()

        #Viewport Variables
        self.old_log = Backend.update_log
        self.viewport_ongoing = False
        self.update_while_viewport = False

        #Viewport Instatiate
        Backend.update_log = self.update_viewport
        self.environment.setStyleSheet("background-position: center;background-repeat: no-repeat;background-image: url(viewport_temp/loading.png);")

        self.setMinimumSize(1350, 700) # minimum size of program

        # Layout of Main Page
        main_layout = QGridLayout()
        main_layout.addWidget(self.tab_widget, 0, 0, 1, 8)
        main_layout.addWidget(ObjectsStatusBar, 1, 0, 1, 2)
        main_layout.addWidget(self.environment, 1, 1, 1, 7)  
    
        self.setLayout(main_layout)
        translator.languageChanged.connect(self.translateUi)
        self.translateUi()
        
        """#Tests for all pages except Random (included in RandomTabDialog)
        from FrontTests import Tests
        Tests(self, tab_widget, shared_state, ObjectTab, PivotTab, Render, Lighting, backend)"""

    def visual_change(self, thread):
        #Updates Viewport Image
        thread.quit()
        self.environment.setStyleSheet("border-image: url(viewport_temp/0_colors.png) 0 0 0 0 stretch stretch")
        # environment.setStyleSheet("background-position: center;background-repeat: no-repeat;background-image: url(viewport_temp/0_colors.png);")

        self.viewport_ongoing = False

        if (self.update_while_viewport):
            #Ensures most up to date image is displayed
            self.update_while_viewport = False
            self.update_viewport(update_log = False)

    
    def update_viewport(self, interaction = "", update_log = True):
        # At least 10 seconds between viewport updates
        # if (time() - last_viewport_update > 5):
        if (not self.viewport_ongoing and "Render" not in interaction):
            self.old_log(interaction)
            config = backend.get_config()
            if (not config["objects"][0]): return
            backend.set_runtime_config(config)

            thread = ViewportThread(self.size())

            thread.finished.connect(lambda: self.visual_change(thread))

            self.viewport_ongoing = True
            thread.start()
        elif (update_log):
            if ("Program" not in interaction and "Render" not in interaction):
                self.update_while_viewport = True
            return self.old_log(interaction)
    
    def translateUi(self):
        current_lang = translator.current_language
        translation = translator.translations.get(current_lang, translator.translations.get("English", {}))
        self.tab_widget.setTabText(0, translation.get("Object", "Object"))
        self.tab_widget.setTabText(1, translation.get("Pivot Point", "Pivot Point"))
        self.tab_widget.setTabText(2, translation.get("Render", "Render"))
        self.tab_widget.setTabText(3, translation.get("Lighting", "Lighting"))
        self.tab_widget.setTabText(4, translation.get("Random", "Random"))
        self.tab_widget.setTabText(5, translation.get("Import/Export", "Import/Export"))
        self.tab_widget.setTabText(6, translation.get("Settings", "Settings"))

class ilyaMessageBox(QMessageBox):
    #IlyaCommentBox
    # Displays a custom messagebox
    def __init__(self, text, title):
        super().__init__()
        self.setText(text)
        self.setWindowTitle(title)
        self.exec()

class ObjectTab(QWidget):
    #Object Page
    def __init__(self, parent: QWidget, tab_widget: QTabWidget, Scroll: QVBoxLayout):
        super().__init__(parent)

        #Declare UI elements

        self.Object_pos_title = QLabel(f"Co-ords", self)

        self.XObj_pos = QLabel("X:", self)
        self.XObj_pos_input_field = QLineEdit(parent=self)
        self.XObj_pos_input_field.setText("0.0")
        #self.XObj_pos_input_field.setFocusPolicy(Qt.NoFocus)
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
        self.W_slider.setRange(0, 950)
        self.W_slider.setPageStep(0)
        self.W_slider.setOrientation(QtCore.Qt.Horizontal)

        self.Height_Obj_pos = QLabel("Height:", self)
        self.Height_Obj_pos_input_field = QLineEdit(parent=self)
        self.Height_Obj_pos_input_field.setText("1.0")

        self.H_slider = QtWidgets.QSlider(self)
        self.H_slider.setRange(0, 950)
        self.H_slider.setPageStep(0)
        self.H_slider.setOrientation(QtCore.Qt.Horizontal)
        
        self.Length_Obj_pos = QLabel("Length:", self)
        self.Length_Obj_pos_input_field = QLineEdit(parent=self)
        self.Length_Obj_pos_input_field.setText("1.0")

        self.L_slider = QtWidgets.QSlider(self)
        self.L_slider.setRange(0, 950)
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

        #First Section
        def Get_Object_Filepath(Scroll):
            current_lang = translator.current_language
            translations = translator.translations.get(current_lang, translator.translations.get("English", {}))
            import_box = QMessageBox()
            import_box.setText(translations.get("How would you like to import objects?", "How would you like to import objects?"))
            import_files_button = import_box.addButton(translations.get("Import Files", "Import Files"), QMessageBox.ActionRole)
            folder_button = import_box.addButton(translations.get("Folder", "Folder"), QMessageBox.ActionRole)
            cancel_button = import_box.addButton(translations.get("Cancel", "Cancel"), QMessageBox.RejectRole)
            
            import_box.exec()
            clicked_button = import_box.clickedButton()
            
            try:
                if clicked_button == import_files_button:
                    paths = QFileDialog.getOpenFileNames(self, 'Open files', 'c:\\', "3D Model (*.blend *.stl *.obj)")[0]
                    if not paths:
                        return
                    
                    for path in paths:
                        obj = backend.RenderObject(filepath=path)
                        Name = os.path.basename(os.path.normpath(path))
                        shared_state.add_item(obj, Name)
                        
                        button = QPushButton(Name)
                        button.setMaximumWidth(175)
                        menu = QMenu()
                        incexc = menu.addAction(translations.get("Included in Scene","Included in Scene"))
                        ground = menu.addAction(translations.get("Grounded","Grounded"))
                        incexc.setCheckable(True)
                        incexc.setChecked(True)
                        incexc.triggered.connect(lambda: show_hide_object(obj,incexc.isChecked()))

                        ground.setCheckable(True)
                        ground.triggered.connect(lambda: ground_object(obj,ground.isChecked()))
                        
                        button.setMenu(menu)
                        Scroll.addWidget(button)

                elif clicked_button == folder_button:
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
                                Name = os.path.basename(os.path.normpath(full_path))
                                shared_state.add_item(obj, Name)
                                
                                button = QPushButton(Name)
                                button.setMaximumWidth(175)
                                menu = QMenu()
                                incexc = menu.addAction(translations.get("Included in Scene","Included in Scene"))
                                ground = menu.addAction(translations.get("Grounded","Grounded"))
                                
                                incexc.setCheckable(True)
                                incexc.setChecked(True)
                                incexc.triggered.connect(lambda: show_hide_object(obj,incexc.isChecked()))

                                ground.setCheckable(True)
                                ground.triggered.connect(lambda: ground_object(obj,ground.isChecked()))
                                
                                button.setMenu(menu)
                                Scroll.addWidget(button)


                Object_detect(tab_widget)

            except Exception:
                error_title = translations.get("error_reading_title", "Error when reading model")
                error_msg = translations.get("error_reading_body", "The selected file is corrupt or invalid.")
                QMessageBox.warning(self, error_title, error_msg)
            except Exception as e:
                error_title = translations.get("Error when importing", "Error when importing")
                error_msg = translations.get("Error_Import", "Error: {}").format(str(e))
                QMessageBox.warning(self, error_title, error_msg)

        self.Import_Object_Button = QPushButton("Import Objects", self)
        self.Import_Object_Button.clicked.connect(lambda: Get_Object_Filepath(Scroll))

        def delete_object(tab_widget, scroll):
            current_lang = translator.current_language
            translations = translator.translations.get(current_lang, translator.translations.get("English", {}))
            
            to_delete = QMessageBox()
            to_delete.setText(translations.get("Please select an object to remove from below", "Please select an object to remove from below"))

            if (not shared_state.items):
                warning_text = translations.get("Warning", "Warning")
                warning_msg = translations.get("There are no objects to delete.", "There are no objects to delete.")
                return QMessageBox.warning(self, warning_text, warning_msg)

            for i in range(len(shared_state.itemNames)):
                to_delete.addButton(str(shared_state.itemNames[i]), QMessageBox.ActionRole)
            
            cancel_button = to_delete.addButton(translations.get("Cancel", "Cancel"), QMessageBox.ActionRole)
            to_delete.exec()
            choice = str(to_delete.clickedButton().text())



            if choice != cancel_button.text():
                obj_index = shared_state.itemNames.index(choice)
                obj = shared_state.items[obj_index]
                scroll.itemAt(obj_index).widget().setParent(None)
                try:
                    shared_state.remove_item(obj)
                    success_box = ilyaMessageBox("Object successfully deleted", "Success")
                    backend.update_log(f'{obj} object deleted\n')
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
                    QMessageBox.warning(self, translations.get("Warning", "Warning"),translations.get("You have deleted all of the objects, object manipulation tabs have been disabled.", "You have deleted all of the objects, object manipulation tabs have been disabled."))
    
        self.Delete_Object_Button = QPushButton('Delete Object', self)
        self.Delete_Object_Button.clicked.connect(lambda: delete_object(tab_widget, Scroll))

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

        #Declare Location of elements in a grid layout 
        #(Y, X)

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

        main_layout.addWidget(self.Length_Obj_pos, 2, 7)
        main_layout.addWidget(self.Length_Obj_pos_input_field, 2, 8)
        main_layout.addWidget(self.L_slider, 2, 9)

        main_layout.addWidget(self.Height_Obj_pos, 3, 7)
        main_layout.addWidget(self.Height_Obj_pos_input_field, 3, 8)
        main_layout.addWidget(self.H_slider, 3, 9)

        main_layout.addWidget(self.combo_box, 0, 9)

        main_layout.addWidget(self.Import_Object_Button, 4, 8)
        main_layout.addWidget(self.Delete_Object_Button, 4, 9)

        self.setLayout(main_layout)

        #Connect Page to functions
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

        self.Width_Obj_pos_input_field.textEdited.connect(lambda: self.Update_slider_Scale(self.W_slider, self.Width_Obj_pos_input_field.text()))
        self.Height_Obj_pos_input_field.textEdited.connect(lambda: self.Update_slider_Scale(self.H_slider, self.Height_Obj_pos_input_field.text()))
        self.Length_Obj_pos_input_field.textEdited.connect(lambda: self.Update_slider_Scale(self.L_slider, self.Length_Obj_pos_input_field.text()))

        # editingFinished callbacks that updates backend
        self.Width_Obj_pos_input_field.editingFinished.connect(self.update_object_scale)
        self.Height_Obj_pos_input_field.editingFinished.connect(self.update_object_scale)
        self.Length_Obj_pos_input_field.editingFinished.connect(self.update_object_scale)

        ########################################
        
        self.W_slider.sliderMoved.connect(lambda val: self.Slider_Update_Scale(val, self.Width_Obj_pos_input_field))
        self.H_slider.sliderMoved.connect(lambda val: self.Slider_Update_Scale(val, self.Height_Obj_pos_input_field))
        self.L_slider.sliderMoved.connect(lambda val: self.Slider_Update_Scale(val, self.Length_Obj_pos_input_field))

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
        translator.languageChanged.connect(self.translateUi)
        self.translateUi()

        #########################################

        def show_hide_object(object,state):
            backend.toggle_object(object,state)
        
        def ground_object(object,state):
            backend.grounf_object(object,state)

        def Object_detect(tab_widget):
            State = not Backend.is_config_objects_empty(tab_widget)
            for i in range(5):
                tab_widget.setTabEnabled(i, State)

    
        def delete_object(tab_widget, scroll):
            current_lang = translator.current_language
            translations = translator.translations.get(current_lang, translator.translations.get("English", {}))
            
            to_delete = QMessageBox()
            to_delete.setText(translations.get("Please select an object to remove from below", "Please select an object to remove from below"))

            if (not shared_state.items):
                warning_text = translations.get("Warning", "Warning")
                warning_msg = translations.get("There are no objects to delete.", "There are no objects to delete.")
                return QMessageBox.warning(self, warning_text, warning_msg)

            for i in range(len(shared_state.itemNames)):
                to_delete.addButton(str(shared_state.itemNames[i]), QMessageBox.ActionRole)
            
            cancel_button = to_delete.addButton(translations.get("Cancel", "Cancel"), QMessageBox.ActionRole)
            to_delete.exec()
            choice = str(to_delete.clickedButton().text())



            if choice != cancel_button.text():
                obj_index = shared_state.itemNames.index(choice)
                obj = shared_state.items[obj_index]
                scroll.itemAt(obj_index).widget().setParent(None)
                try:
                    shared_state.remove_item(obj)
                    success_box = ilyaMessageBox("Object successfully deleted", "Success")
                    backend.update_log(f'{obj} object deleted\n')
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
                    QMessageBox.warning(self, translations.get("Warning", "Warning"),translations.get("You have deleted all of the objects, object manipulation tabs have been disabled.", "You have deleted all of the objects, object manipulation tabs have been disabled."))
    
    def Object_detect(self, tab_widget):
            """On upload/delete to be called to check if any object is to be rendered and enables tabs accordingly"""
            State = not Backend.is_config_objects_empty(tab_widget)
            for i in range(5):
                tab_widget.setTabEnabled(i, State)
                
    def update_combo_box_items(self, items):
        """ Method could be called to update combo_box_items. Maybe Delete. """
        self.combo_box.clear()
        self.combo_box.addItems(map(lambda o: str(o), items))

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
        
        self.Update_slider_Scale(self.W_slider,self.Width_Obj_pos_input_field.text())
        self.Update_slider_Scale(self.H_slider,self.Height_Obj_pos_input_field.text())
        self.Update_slider_Scale(self.L_slider,self.Length_Obj_pos_input_field.text())
        self.Update_slider(self.X_Rotation,self.X_Rotation_input_field.text())
        self.Update_slider(self.Y_Rotation,self.Y_Rotation_input_field.text())
        self.Update_slider(self.Z_Rotation,self.Z_Rotation_input_field.text())



    def translateUi(self):
        current_lang = translator.current_language
        translations = translator.translations.get(current_lang, translator.translations.get("English", {}))

        self.Object_pos_title.setText(translations.get("Co-ords", "Co-ords"))
        self.XObj_pos.setText(translations.get("X:", "X:"))
        self.YObj_pos.setText(translations.get("Y:", "Y:"))
        self.ZObj_pos.setText(translations.get("Z:", "Z:"))
        self.Object_scale_title.setText(translations.get("Scale", "Scale"))
        self.Width_Obj_pos.setText(translations.get("Width:", "Width:"))
        self.Height_Obj_pos.setText(translations.get("Height:", "Height:"))
        self.Length_Obj_pos.setText(translations.get("Length:", "Length:"))        
        self.Object_rotation_title.setText(translations.get("Rotation", "Rotation"))
        self.X_Rotation_Label.setText(translations.get("Roll:", "Roll:"))
        self.Y_Rotation_Label.setText(translations.get("Pitch:", "Pitch:"))
        self.Z_Rotation_Label.setText(translations.get("Yaw:", "Yaw:"))
        self.Object_pos_title.setToolTip(translations.get('Changes the objects Position', 'Changes the objects Position'))
        self.Object_scale_title.setToolTip(translations.get('Changes the objects scale', 'Changes the objects scale'))
        self.Object_rotation_title.setToolTip(translations.get('Changes the objects rotation', 'Changes the objects rotation'))
        self.W_slider.setToolTip(translations.get("Adjust Width", "Adjust Width"))
        self.H_slider.setToolTip(translations.get("Adjust Height", "Adjust Height"))
        self.L_slider.setToolTip(translations.get("Adjust Length", "Adjust Length"))
        self.Delete_Object_Button.setText(translations.get("Delete Object", "Delete Object"))
        self.Import_Object_Button.setText(translations.get("Import Object", "Import Object"))
    
    def ValidType(self, val):
        """Validates if val type is string"""
        return type(val) == str
    
    def Update_slider(self, slider, val):
        """Updates slider to reflect InputField"""
        try:
            slider.setValue(int(round(float(val), 0)))
        except Exception as e:
            try:
                slider.setValue(0)
            except:
                print("Error", e)
    
    def Update_slider_Scale(self, slider, val):
        try:
            val = float(val)
            if val < 500:
                slider.setValue(int(round(float(val * 500), 0)))
            else:
                slider.setValue(int(round(float( (val * 50) + 450), 0)))
        except Exception as e:
            try:
                slider.setValue(0)
            except:
                print("Error", e)
    
    def Slider_Update_Scale(self, val, field):
        try:
            if field.isEnabled():
                if field.text() == '':
                    field.setText('0')
                if float(field.text()) > val or float(field.text()) + 0.5 < val:
                    if val < 500: # <1 true
                        trueValStr = str(val / 500)
                        if len(trueValStr) > 4:
                            field.setText(trueValStr[0:4])
                        else:
                            field.setText(trueValStr)

                    else: # >1 true
                        trueValStr = (val - 450) / 50
                        field.setText(str(round(trueValStr,1)))
        except:
            field.setText("0.0")

    def Slider_Update(self, val, field):
        """Set Field value to slider value"""
        if field.isEnabled():
            try:
                if field.text() == '':
                    field.setText('0.0')
                if float(field.text()) > val or float(field.text()) + 0.5 < val:
                    field.setText(str(val))
            except:
                field.setText('0.0')

            
    def update_object_pos(self):
        """ Method to dynamically update a targetted object's position """
        try: 
            x = float(self.XObj_pos_input_field.text() or 0)
            y = float(self.YObj_pos_input_field.text() or 0)
            z = float(self.ZObj_pos_input_field.text() or 0)
                
            location = [x,y,z]
            
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
            scale = [width,length,height]
            
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
            
            rotation = [np.deg2rad(x_rot),np.deg2rad(y_rot),np.deg2rad(z_rot)]
            
            # get the selected object's position from the combo box
            selected_object_index = self.combo_box.currentIndex()
            shared_state.itemNames[selected_object_index]
            obj = shared_state.items[selected_object_index]
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

class PivotTab(QWidget):
    def __init__(self, parent: QWidget):
        """Pivot Tab"""
        super().__init__(parent)

        # Pivot Point Coords Section
        self.Pivot_Point_Check = QCheckBox("Custom Pivot Point", self)
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
        self.Distance_Pivot_input_field.setText("0")
        self.Distance_Slider.setValue(0)
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
        translator.languageChanged.connect(self.translateUi)
        self.translateUi()



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
        self.translateUi()

        
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
            try: 
                if field.text() == '':
                    field.setText('0')
                if float(field.text()) > val or float(field.text()) + 0.5 < val:
                    field.setText(str(val))
            except:
                field.setText('0')
        
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
                field.editingFinished.emit()#
    
    def translateUi(self):
        current_lang = translator.current_language
        translation = translator.translations.get(current_lang, translator.translations.get("English", {}))
        self.Pivot_Point_Check.setText(translation.get("Custom Pivot Point", "Custom Pivot Point"))
        self.Distance_Pivot.setText(translation.get("Distance","Distance"))

class RandomTabDialog(QWidget):
    def __init__(self, parent: QWidget, ParentTab: QTabWidget):
        """Random Tab Nav Bar"""
        super().__init__(parent)

        self.tab_widget = QTabWidget()
        self.tab_widget.addTab(RandomDefault(self, self.tab_widget), "Base")
        self.tab_widget.addTab(RandomObject(self, ParentTab), "Object")
        self.tab_widget.addTab(RandomPivot(self, ParentTab), "Pivot Point")
        self.tab_widget.addTab(RandomRender(self, ParentTab), "Render")
        self.tab_widget.addTab(RandomLight(self, ParentTab), "Light")


        """
        from FrontTests import RandomTabTests
        RandomTabTests(self.tab_widget)"""

        main_layout = QVBoxLayout()
        main_layout.addWidget(self.tab_widget)
        self.setLayout(main_layout)
        translator.languageChanged.connect(self.translateUi)
        self.translateUi()


    def translateUi(self):
        """Apply translations to UI"""
        current_lang = translator.current_language
        translation = translator.translations.get(current_lang, translator.translations.get("English", {}))
        self.tab_widget.setTabText(0, translation.get("Base", "Base"))
        self.tab_widget.setTabText(1, translation.get("Object", "Object"))
        self.tab_widget.setTabText(2, translation.get("Pivot Point", "Pivot Point"))
        self.tab_widget.setTabText(3, translation.get("Render", "Render"))
        self.tab_widget.setTabText(4, translation.get("Light", "Light"))

class RandomDefault(QWidget):
    """Defualt page for Random"""
    def __init__(self, parent: QWidget, tab_widget: QTabWidget):
        super().__init__(parent)

        main_layout = QGridLayout()
        """Sets all fields in all random pages to enabled"""
        Field = QCheckBox("Set ALL RANDOM", self)
        Field.setToolTip('Sets all elements on all pages to random') 

        """Set per is XOR"""
        SetSetCheck = QCheckBox("Set per SET",self)
        SetSetCheck.setToolTip('Each selected field is randomly generated and its value is maintained throughout the entire set generation.') 
        SetFrameCheck = QCheckBox("Set per FRAME",self)
        SetFrameCheck.setToolTip('Each selected field is randomly generated and its value is changed for each frame.') 
        RandomSeed = QLineEdit("", self)

        """The random seed value used to generate random values"""
        RandomSeed.setText(str(backend.get_config()["seed"]))
        RandomSeed.setMaximumWidth(200)
        
        main_layout.addWidget(Field, 0, 0)
        main_layout.addWidget(SetSetCheck, 1, 0)
        main_layout.addWidget(SetFrameCheck, 2, 0)
        
        """XOR FUNCTIONS"""
        SetSetCheck.toggled.connect(lambda: self.SetSETChecks(main_layout))
        SetFrameCheck.toggled.connect(lambda: self.SetFRAMEChecks(main_layout))
        SetSetCheck.setChecked(True)
        main_layout.addWidget(RandomSeed, 3, 0)
        main_layout.setAlignment(Qt.AlignTop | Qt.AlignRight)
        
        Field.toggled.connect(lambda state: self.checkUpdate(tab_widget, state))
        RandomSeed.editingFinished.connect(lambda: self.SeedEdit(RandomSeed))
        
        self.setLayout(main_layout)


    def SetSETChecks(self, Layout):
        """XOR FUNCTIONS"""
        if Layout.itemAtPosition(1, 0).widget().isChecked():
            print('toggled: per set')
            # initial mode
            backend.toggle_random_mode("set")
            Layout.itemAtPosition(2, 0).widget().setChecked(False)
        self.notXOR(Layout)
    
    def SetFRAMEChecks(self, Layout):
        """XOR FUNCTIONS"""
        if Layout.itemAtPosition(2, 0).widget().isChecked():
            print('toggled: per frame')
            backend.toggle_random_mode("frame")
            Layout.itemAtPosition(1, 0).widget().setChecked(False)
        self.notXOR(Layout)

    def notXOR(self, Layout):
        """XOR FUNCTIONS"""
        if (not Layout.itemAtPosition(1, 0).widget().isChecked()) == (not Layout.itemAtPosition(2, 0).widget().isChecked()):
            Layout.itemAtPosition(1, 0).widget().setChecked(True)
        
    def checkUpdate(self, tab_widget, State):
        """Method to update all Random checkboxes"""
        """
        DO NOT DELETE 
        Path to check is state is checked
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
            backend.set_seed(val)
        except ValueError:
            field.setText(str(backend.get_config()["seed"]))

            field.setToolTip('Random seed') 


class RandomObject(QWidget):
    """Random Object"""
    def __init__(self, parent: QWidget, ParentTab: QTabWidget):
        super().__init__(parent)

        """Fields in Page"""
        """
        Intended to be accessed via self.CheckBoxes.Keys()
        """
        self.CheckBoxes = {}
        self.LowerBounds = {}
        self.UpperBounds = {}
        self.field_checkboxes = {}

        self.main_layout = QGridLayout()

        
        # create initial combo_box
        self.combo_box = QComboBox(self)
        # connecting shared state updates to combo box
        shared_state.items_updated.connect(lambda: self.update_combo_box_items(shared_state.itemNames))
        shared_state.selection_changed.connect(self.combo_box.setCurrentIndex)
        self.combo_box.currentIndexChanged.connect(self.on_object_selected)  # reattached the on_object_selected method

        # initialise items
        self.update_combo_box_items(shared_state.itemNames)
        shared_state.update_items(items=[])
        shared_state.update_selected(0)
        
        self.main_layout.addWidget(self.combo_box, 0, 10)
        
        self.set_all_checkbox = QCheckBox("Set all random", self)
        self.main_layout.addWidget(self.set_all_checkbox, 1, 10)
        self.set_all_checkbox.toggled.connect(lambda: 
            self.set_all_random(self.main_layout, self.set_all_checkbox.isChecked()))
        
        self.coords_label = QLabel("Co-ords:", self)
        self.main_layout.addWidget(self.coords_label, 0, 0)
        self.gen_field("X", self.main_layout, 0, 1, self.connFields(ParentTab, 1, 1))
        self.gen_field("Y", self.main_layout, 0, 2, self.connFields(ParentTab, 1, 2))
        self.gen_field("Z", self.main_layout, 0, 3, self.connFields(ParentTab, 1, 3))

        self.rotation_label = QLabel("Rotation", self)
        self.main_layout.addWidget(self.rotation_label, 0, 3)
        self.gen_field("Pitch", self.main_layout, 3, 1, self.connFields(ParentTab, 5, 1))
        self.gen_field("Roll", self.main_layout, 3, 2, self.connFields(ParentTab, 5, 2))
        self.gen_field("Yaw", self.main_layout, 3, 3, self.connFields(ParentTab, 5, 3))
        
        self.scale_label = QLabel("Scale", self)
        self.main_layout.addWidget(self.scale_label, 0, 7)
        self.gen_field("Width", self.main_layout, 6, 1, self.connFields(ParentTab, 8, 1))
        self.gen_field("Height", self.main_layout, 6, 2, self.connFields(ParentTab, 8, 2))
        self.gen_field("Length", self.main_layout, 6, 3, self.connFields(ParentTab, 8, 3))
        self.setLayout(self.main_layout)

        translator.languageChanged.connect(self.translateUi)
        self.translateUi()

    def gen_field(self, Fieldname, Layout, X, Y, ConField):
        """Generate a field including checkbox and 2 input fields"""
        Field = QCheckBox(Fieldname, self)
        Field_LowerBound = QLineEdit(parent=self)
        Field_UpperBound = QLineEdit(parent=self)
        self.field_checkboxes[Fieldname] = Field 

        """sets text to ensure Bounds and better error handling"""
        Field_LowerBound.setText('-inf')
        Field_UpperBound.setText('inf')
        
        """Hover over provides a  description"""
        Field_LowerBound.setToolTip('LowerBound') 
        Field_UpperBound.setToolTip('UpperBound') 

        """
        Creates and Adds field to layout
        Connects them to validation and bounds checking
        """
        self.addCheck(Field, Fieldname, Layout, X, Y, ConField)
        self.addLower(Field_LowerBound, Fieldname, Layout, X+1, Y)
        self.addUpper(Field_UpperBound, Fieldname, Layout, X+2, Y)
        Field_LowerBound.editingFinished.connect(lambda: self.validation(Field_LowerBound))
        Field_UpperBound.editingFinished.connect(lambda: self.validation(Field_UpperBound))
        
        Field_LowerBound.editingFinished.connect(lambda: self.boundChecker(Field_LowerBound, Field_UpperBound))
        Field_UpperBound.editingFinished.connect(lambda: self.boundChecker(Field_LowerBound, Field_UpperBound))

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
        """Connects field to related Field not in random"""
        return ParentTab.widget(0).layout().itemAtPosition(Y, X).widget()

    def addLower(self, Field, Fieldname, Layout, X, Y):
        """Generate Lowerbound Field"""
        Layout.addWidget(Field, Y, X)
        self.LowerBounds[f"{Layout.itemAtPosition(0, 10).widget().currentText()}{Fieldname}"] = (X, Y)
        
    def addUpper(self, Field, Fieldname, Layout, X, Y):
        """Generate Upperbound Field"""
        Layout.addWidget(Field, Y, X)
        self.UpperBounds[f"{Layout.itemAtPosition(0, 10).widget().currentText()}{Fieldname}"] = (X, Y)
        
    def boundChecker(self, Lower, Upper):
        """If not within bounds set adjust to mandatory legal values"""
        try:
            
            Lowerval = float(Lower.text())
            Upperval = float(Upper.text())
            
            if Lowerval > Upperval:
                Lower.setText('-inf')
            elif Upperval < Lowerval:
                Upper.setText('inf')
        except:
            Lower.setText('-inf')
            Upper.setText('inf')

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
        
    def on_object_selected(self, index):
        # get config from backend
        config = backend.get_config()

        # get specific index 
        objects_config = config.get("random", {}).get("objects", {})
        object_config = objects_config.get(index, {}).get("object", {})

        # list of all possible fields (can make this more modular later lol)
        all_fields = ["X", "Y", "Z", "Pitch", "Roll", "Yaw", "Width", "Height", "Length"]

        # temporary bug fix
        count = 0

        for field_name in all_fields:
            # get widgets by their object names
            checkbox = self.findChild(QCheckBox, field_name)
            lower_bound = self.findChild(QLineEdit, f"{field_name}_lower")
            upper_bound = self.findChild(QLineEdit, f"{field_name}_upper")

            if checkbox and lower_bound and upper_bound:
                if field_name in object_config:
                    bounds = object_config[field_name]

                    # activate checkbox and put in the bounds from config
                    checkbox.setChecked(True)
                    lower_bound.setText(str(bounds[0]))
                    upper_bound.setText(str(bounds[1]))
                    lower_bound.setEnabled(True)
                    upper_bound.setEnabled(True)
                    
                    # update to back end to fix previous index not updating bug :)
                    backend.update_random_attribute(index, 'object', field_name, checkbox.isChecked(), lower_bound.text(), upper_bound.text())
                    count += 1
                else:
                    # if field not in config: reset to default unchecked state
                    checkbox.setChecked(False)
                    lower_bound.setText("0")
                    upper_bound.setText("0")
                    lower_bound.setEnabled(False)
                    upper_bound.setEnabled(False)
        
        # update the toggle-all checkbox
        all_box = self.layout().itemAtPosition(1, 10).widget()
        
        # check if all fields are active
        if count == len(all_fields):  # all fields are active
            if not all_box.isChecked():  # if not already checked toggle it
                all_box.blockSignals(True)
                all_box.setChecked(True)
                all_box.blockSignals(False)
        else:  # when not all fields are active
            if all_box.isChecked():  # if already checked toggle it
                all_box.blockSignals(True)
                all_box.setChecked(False)
                all_box.blockSignals(False)

    def translateUi(self,):
        current_lang = translator.current_language
        translation = translator.translations.get(current_lang, translator.translations.get("English", {}))

        self.rotation_label.setText(translation.get("Rotation", "Rotation"))
        self.coords_label.setText(translation.get("Co-ords:", "Co-ords:"))
        self.scale_label.setText(translation.get("Scale", "Scale"))
        self.set_all_checkbox.setText(translation.get("Set all random", "Set all random"))
        
        for field_name, checkbox in self.field_checkboxes.items():
            translated = translation.get(field_name, field_name)
            checkbox.setText(translated)
            
class RandomPivot(QWidget):
    """Random PivotPage"""
    def __init__(self, parent: QWidget, ParentTab: QTabWidget):
        super().__init__(parent)
        

        self.CheckBoxes = {}
        self.LowerBounds = {}
        self.UpperBounds = {}
        self.field_checkboxes = {}


        self.main_layout = QGridLayout()
        
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

        self.main_layout.addWidget(self.combo_box, 0, 10)

        self.set_all_checkbox = QCheckBox("Set all random", self)
        self.main_layout.addWidget(self.set_all_checkbox, 1, 10)
        self.set_all_checkbox.toggled.connect(lambda: 
            self.set_all_random(self.main_layout, self.set_all_checkbox.isChecked()))
       
        self.coords_label = QLabel("Co-ords:", self)
        self.main_layout.addWidget(self.coords_label, 0, 0)
        self.gen_field("X", self.main_layout, 0, 1, self.connFields(ParentTab, 1, 1))
        self.gen_field("Y", self.main_layout, 0, 2, self.connFields(ParentTab, 1, 2))
        self.gen_field("Z", self.main_layout, 0, 3, self.connFields(ParentTab, 1, 3))

        """
        Special Connfields as this has a checkbox interaction that has to invert all related Fields
        """
        
        ParentTab.widget(1).layout().itemAtPosition(0, 0).widget().toggled.connect(lambda: self.un_checked(not ParentTab.widget(1).layout().itemAtPosition(0, 0).widget().isChecked(), self.main_layout.itemAtPosition(1, 1).widget(), self.main_layout.itemAtPosition(1, 2).widget()))
        ParentTab.widget(1).layout().itemAtPosition(0, 0).widget().toggled.connect(lambda: self.un_checked(not ParentTab.widget(1).layout().itemAtPosition(0, 0).widget().isChecked(), self.main_layout.itemAtPosition(2, 1).widget(), self.main_layout.itemAtPosition(2, 2).widget()))
        ParentTab.widget(1).layout().itemAtPosition(0, 0).widget().toggled.connect(lambda: self.un_checked(not ParentTab.widget(1).layout().itemAtPosition(0, 0).widget().isChecked(), self.main_layout.itemAtPosition(3, 1).widget(), self.main_layout.itemAtPosition(3, 2).widget()))
        
        self.distance_label = QLabel("Distance", self)
        self.main_layout.addWidget(self.distance_label, 0, 3)

        self.gen_field("Measurement", self.main_layout, 3, 1, self.connFields(ParentTab, 5, 1))
        self.setLayout(self.main_layout)
        translator.languageChanged.connect(self.translateUi)
        self.translateUi()


    """
    SEE RANDOM OBJECT CLASS FUNCTIONS FOR COMMENTS
    """

    def gen_field(self, Fieldname, Layout, X, Y, ConField):
        Field = QCheckBox(Fieldname, self)
        Field_LowerBound = QLineEdit(parent=self)
        Field_UpperBound = QLineEdit(parent=self)
        self.field_checkboxes[Fieldname] = Field
        
        Field_LowerBound.setText('-inf')
        Field_UpperBound.setText('inf')
        
        Field_LowerBound.setToolTip('LowerBound') 
        Field_UpperBound.setToolTip('UpperBound') 

        self.addCheck(Field, Fieldname, Layout, X, Y, ConField)
        self.addLower(Field_LowerBound, Fieldname, Layout, X+1, Y)
        self.addUpper(Field_UpperBound, Fieldname, Layout, X+2, Y)
        Field_LowerBound.editingFinished.connect(lambda: self.validation(Field_LowerBound))
        Field_UpperBound.editingFinished.connect(lambda: self.validation(Field_UpperBound))
        
        Field_LowerBound.editingFinished.connect(lambda: self.boundChecker(Field_LowerBound, Field_UpperBound))
        Field_UpperBound.editingFinished.connect(lambda: self.boundChecker(Field_LowerBound, Field_UpperBound))

        Field.toggled.connect(lambda: self.un_checked(Field.isChecked(), Field_LowerBound, Field_UpperBound))
        self.un_checked(False, Field_LowerBound, Field_UpperBound)

    def validation(self, Field):
        if Field.isEnabled():
            """Updates field value"""
            try:
                val = float(Field.text())
                Field.setText(str(val))
            except:
                Field.setText("0")
        
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
        
    def boundChecker(self, Lower, Upper):
        try:
            
            Lowerval = float(Lower.text())
            Upperval = float(Upper.text())
            
            if Lowerval > Upperval:
                Lower.setText('-inf')
            elif Upperval < Lowerval:
                Upper.setText('inf')
        except:
            Lower.setText('-inf')
            Upper.setText('inf')

    def un_checked(self, State, Field_LowerBound, Field_UpperBound):
        Field_LowerBound.setEnabled(State)
        Field_UpperBound.setEnabled(State)
        
        # if not State:
        Field_LowerBound.setText("0")
        Field_UpperBound.setText("0")

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


    def translateUi(self,):
        
        current_lang = translator.current_language
        translation = translator.translations.get(current_lang, translator.translations.get("English", {}))

        self.distance_label.setText(translation.get("Distance","Distance"))
        self.coords_label.setText(translation.get("Co-ords:","Co-ords:"))
        self.set_all_checkbox.setText(translation.get("Set all random","Set all random"))
        
        
        for field_name, checkbox in self.field_checkboxes.items():
            translated = translation.get(field_name, field_name)
            checkbox.setText(translated)

class RandomRender(QWidget):
    """Random Render"""
    def __init__(self, parent: QWidget, ParentTab: QTabWidget):
        super().__init__(parent)

        self.CheckBoxes = {}
        self.LowerBounds = {}
        self.UpperBounds = {}
        self.field_checkboxes = {}


        self.main_layout = QGridLayout()
        
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

        self.main_layout.addWidget(self.combo_box, 0, 10)

        self.set_all_checkbox = QCheckBox("Set all random", self)  # Store as instance variable
        self.main_layout.addWidget(self.set_all_checkbox, 1, 10)
        self.set_all_checkbox.toggled.connect(lambda: 
            self.set_all_random(self.main_layout, self.set_all_checkbox.isChecked()))

        self.degrees_label = QLabel("Degrees of Change:", self)
        self.main_layout.addWidget(self.degrees_label, 0, 0)
        self.gen_field("X", self.main_layout, 0, 1, self.connFields(ParentTab, 4, 1))
        self.gen_field("Y", self.main_layout, 0, 2, self.connFields(ParentTab, 4, 2))
        self.gen_field("Z", self.main_layout, 0, 3, self.connFields(ParentTab, 4, 3))

        self.render_label = QLabel("Render", self)
        self.main_layout.addWidget(self.render_label, 0, 3)
        self.gen_field("Quantity", self.main_layout, 3, 1, self.connFields(ParentTab, 0, 1))

        self.setLayout(self.main_layout)
        translator.languageChanged.connect(self.translateUi)
        self.translateUi()

    """
    SEE RANDOM OBJECT CLASS FUNCTIONS FOR COMMENTS
    """

    def gen_field(self, Fieldname, Layout, X, Y, ConField):
        Field = QCheckBox(Fieldname, self)
        Field_LowerBound = QLineEdit(parent=self)
        Field_UpperBound = QLineEdit(parent=self)
        self.field_checkboxes[Fieldname] = Field
        
        Field_LowerBound.setText('-inf')
        Field_UpperBound.setText('inf')
        
        Field_LowerBound.setToolTip('LowerBound') 
        Field_UpperBound.setToolTip('UpperBound') 

        self.addCheck(Field, Fieldname, Layout, X, Y, ConField)
        self.addLower(Field_LowerBound, Fieldname, Layout, X+1, Y)
        self.addUpper(Field_UpperBound, Fieldname, Layout, X+2, Y)
        Field_LowerBound.editingFinished.connect(lambda: self.validation(Field_LowerBound))
        Field_UpperBound.editingFinished.connect(lambda: self.validation(Field_UpperBound))
        
        Field_LowerBound.editingFinished.connect(lambda: self.boundChecker(Field_LowerBound, Field_UpperBound))
        Field_UpperBound.editingFinished.connect(lambda: self.boundChecker(Field_LowerBound, Field_UpperBound))

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
                Field.setText("0")

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
        
    def boundChecker(self, Lower, Upper):
        try:
            
            Lowerval = float(Lower.text())
            Upperval = float(Upper.text())
            
            if Lowerval > Upperval:
                Lower.setText('-inf')
            elif Upperval < Lowerval:
                Upper.setText('inf')
        except:
            Lower.setText('-inf')
            Upper.setText('inf')

    def un_checked(self, State, Field_LowerBound, Field_UpperBound):
        Field_LowerBound.setEnabled(State)
        Field_UpperBound.setEnabled(State)
        
        # if not State:
        Field_LowerBound.setText("0")
        Field_UpperBound.setText("0")

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

    def translateUi(self,):
        
        current_lang = translator.current_language
        translation = translator.translations.get(current_lang, translator.translations.get("English", {}))

        #translations for labels/checkboxes
        self.degrees_label.setText(translation.get("Degrees of Change:", "Degrees of Change:"))
        self.render_label.setText(translation.get("Render", "Render"))
        self.set_all_checkbox.setText(translation.get("Set all random", "Set all random"))

        #translation for gen fields
        for field_name, checkbox in self.field_checkboxes.items():
            translated = translation.get(field_name, field_name)
            checkbox.setText(translated)


class RandomLight(QWidget):
    """Random Lighting"""
    def __init__(self, parent: QWidget, ParentTab: QTabWidget):
        super().__init__(parent)

        self.CheckBoxes = {}
        self.LowerBounds = {}
        self.UpperBounds = {}
        self.field_checkboxes = {}


        self.main_layout = QGridLayout()
        
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
        self.main_layout.addWidget(self.combo_box, 0, 12)
        
        self.set_all_checkbox = QCheckBox("Set all random", self)
        self.main_layout.addWidget(self.set_all_checkbox, 1, 12)
        self.set_all_checkbox.toggled.connect(lambda: self.set_all_random(self.main_layout, self.set_all_checkbox.isChecked()))

        self.coords_label = QLabel("Co-ords:", self)
        self.main_layout.addWidget(self.coords_label, 0, 0)
        self.gen_field("X", self.main_layout, 0, 1, self.connFields(ParentTab, 5, 1))
        self.gen_field("Y", self.main_layout, 0, 2, self.connFields(ParentTab, 5, 2))
        self.gen_field("Z", self.main_layout, 0, 3, self.connFields(ParentTab, 5, 3))

        self.angle_label1 = QLabel("Angle", self)
        self.main_layout.addWidget(self.angle_label1, 0, 3)
        self.gen_field("Pitch", self.main_layout, 3, 1, self.connFields(ParentTab, 9, 1))
        self.gen_field("Roll", self.main_layout, 3, 2, self.connFields(ParentTab, 9, 2))
        self.gen_field("Yaw", self.main_layout, 3, 3, self.connFields(ParentTab, 9, 3))
        
        self.angle_label2 = QLabel("Angle", self)
        self.main_layout.addWidget(self.angle_label2, 0, 7)
        self.gen_field("Strength", self.main_layout, 6, 1, self.connFields(ParentTab, 1, 0))
        self.gen_field("Radius", self.main_layout, 6, 2, self.connFields(ParentTab, 1, 2))
        self.gen_field("Colour", self.main_layout, 6, 3, self.connFields(ParentTab, 2, 1))


        self.setLayout(self.main_layout)
        translator.languageChanged.connect(self.translateUi)
        self.translateUi()
        #self.gen_field("BackGround", main_layout, 9, 1)

        #print(main_layout.itemAtPosition(0, 0).widget().setText("Electric boogalo"))
        #how to change values


        self.main_layout.itemAtPosition(0, 12).widget().setHidden(True)

        self.setLayout(self.main_layout)
    
    """
    SEE RANDOM OBJECT CLASS FUNCTIONS FOR COMMENTS
    """
        

    def gen_field(self, Fieldname, Layout, X, Y, ConField):
        Field = QCheckBox(Fieldname, self)
        Field_LowerBound = QLineEdit(parent=self)
        Field_UpperBound = QLineEdit(parent=self)
        self.field_checkboxes[Fieldname] = Field

        
        Field_LowerBound.setText('-inf')
        Field_UpperBound.setText('inf')
        
        Field_LowerBound.setToolTip('LowerBound') 
        Field_UpperBound.setToolTip('UpperBound') 

        self.addCheck(Field, Fieldname, Layout, X, Y, ConField)
        self.addLower(Field_LowerBound, Fieldname, Layout, X+1, Y)
        self.addUpper(Field_UpperBound, Fieldname, Layout, X+2, Y)
        Field_LowerBound.editingFinished.connect(lambda: self.validation(Field_LowerBound))
        Field_UpperBound.editingFinished.connect(lambda: self.validation(Field_UpperBound))
        
        Field_LowerBound.editingFinished.connect(lambda: self.boundChecker(Field_LowerBound, Field_UpperBound))
        Field_UpperBound.editingFinished.connect(lambda: self.boundChecker(Field_LowerBound, Field_UpperBound))

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
                Field.setText("0")

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
        
    def boundChecker(self, Lower, Upper):
        try:
            
            Lowerval = float(Lower.text())
            Upperval = float(Upper.text())
            
            if Lowerval > Upperval:
                Lower.setText('-inf')
            elif Upperval < Lowerval:
                Upper.setText('inf')
        except:
            Lower.setText('-inf')
            Upper.setText('inf')

    def un_checked(self, State, Field_LowerBound, Field_UpperBound):
        Field_LowerBound.setEnabled(State)
        Field_UpperBound.setEnabled(State)
        
        # if not State:
        Field_LowerBound.setText("0")
        Field_UpperBound.setText("0")

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

    def translateUi(self):
        current_lang = translator.current_language
        translation = translator.translations.get(current_lang, translator.translations.get("English", {}))

        # Translate labels
        self.coords_label.setText(translation.get("Co-ords:", "Co-ords:"))
        self.angle_label1.setText(translation.get("Angle", "Angle"))
        self.angle_label2.setText(translation.get("Angle", "Angle"))
        self.set_all_checkbox.setText(translation.get("Set all random", "Set all random"))

        # Translate generated fields
        for field_name, checkbox in self.field_checkboxes.items():
            translated = translation.get(field_name, field_name)
            checkbox.setText(translated)



class Render(QWidget):
    def __init__(self, parent: QWidget):
        super().__init__(parent)
        self.mainpage = parent

        self.i = 1
        self.queue = []

        self.GenerateRenders_Button = QPushButton('Generate Renders', self)
        self.GenerateRenders_Button.clicked.connect(self.renderQueueControl)
        


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
        self.X_Degree_input_field.setText("0")
        self.X_Degree_input_field.editingFinished.connect(self.set_angles)
        self.X_Degree_slider = QtWidgets.QSlider(self)
        self.X_Degree_slider.setPageStep(0)
        self.X_Degree_slider.setOrientation(QtCore.Qt.Horizontal)
        self.X_Degree_slider.setMinimum(0) 
        self.X_Degree_slider.setMaximum(360)

        # Y Degree
        self.Y_Degree_Label = QLabel("Y:", self)
        self.Y_Degree_input_field = QLineEdit(parent=self)
        self.Y_Degree_slider = QtWidgets.QSlider(self)
        self.Y_Degree_input_field.setText("0")
        self.Y_Degree_input_field.editingFinished.connect(self.set_angles)
        self.Y_Degree_slider.setPageStep(0)
        self.Y_Degree_slider.setOrientation(QtCore.Qt.Horizontal)
        self.Y_Degree_slider.setMinimum(0)
        self.Y_Degree_slider.setMaximum(360)

        # Z Degree
        self.Z_Degree_Label = QLabel("Z:", self)
        self.Z_Degree_input_field = QLineEdit(parent=self)
        self.Z_Degree_input_field.setText("0")
        self.Z_Degree_input_field.editingFinished.connect(self.set_angles)
        self.Z_Degree_slider = QtWidgets.QSlider(self)
        self.Z_Degree_slider.setPageStep(0)
        self.Z_Degree_slider.setOrientation(QtCore.Qt.Horizontal)
        self.Z_Degree_slider.setMinimum(0)
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

        self.render_preview_button = QPushButton("Render Preview", self)
        self.render_preview_button.clicked.connect(self.renderPreview)
        

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

        main_layout.addWidget(self.render_preview_button, 2, 7)

        self.setLayout(main_layout)

        translator.languageChanged.connect(self.translateUi)
        self.translateUi()


    def translateUi(self):
        """Apply translations to UI elements."""
        current_lang = translator.current_language
        translation = translator.translations.get(current_lang, translator.translations.get("English", {}))
        self.GenerateRenders_Button.setText(translation.get("Generate Renders", "Generate Renders"))
        self.unlimited_render_button.setText(translation.get("Unlimited Renders", "Unlimited Renders"))
        self.Degree_Change_title.setText(translation.get("Degrees of Change", "Degrees of Change"))
        self.Number_of_renders_title.setText(translation.get("Number of Renders", "Number of Renders"))
        self.render_preview_button.setText(translation.get("Render Preview","Render Preview"))

    
    def unlimitedrender(self):
        unlimitedRenderConfig = backend.get_config()
        test = True
        while True:
            if (self.rendering):
                loop = QEventLoop()
                QTimer.singleShot(2000, loop.quit)
                loop.exec()
                continue
            if self.unlimited_render_button.isChecked():
                self.Number_of_renders_input_field.setText("1")
                self.queue.append(unlimitedRenderConfig)
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
            try:
                if field.text() == '':
                    field.setText('0')
                if float(field.text()) > val or float(field.text()) + 0.5 < val:
                    field.setText(str(val))
            except:
                field.setText("0.0")

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

    def renderPreview(self): 
        if not self.rendering and not self.mainpage.viewport_ongoing:
            config = backend.get_config()
            backend.set_runtime_config(config)
            self.rendering = True
            self.newThread = RenderThreadPreview()

            self.newThread.progress.connect(self.update_loading)
            self.newThread.finished.connect(self.complete_loading)

            self.newThread.start()
            
            self.windowUp()

            #self.thread.quit()
        else:
            renderingBox = QMessageBox()
            renderingBox.setText("Already rendering, please wait for current render to finish before starting new render.")
            renderingBox.exec()

    def renderQueueControl(self):
        if self.rendering and not self.mainpage.viewport_ongoing:
            config = backend.get_config()
            self.queue.append(config)

            renderingBox = QMessageBox()
            renderingBox.setText("Added to queue.")
            renderingBox.exec()
        
        elif self.mainpage.viewport_ongoing:
            renderingBox = QMessageBox()
            renderingBox.setText("Please wait for the viewport to finish its approximation before starting the main render.")
            renderingBox.exec()
            return

        else:
            config = backend.get_config()
            self.queue.append(config)

            self.generate_render()
            self.render_preview_button.setEnabled(False)
    
    def generate_render(self):
        if (self.mainpage.viewport_ongoing):
            renderingBox = QMessageBox()
            renderingBox.setText("Please wait for the viewport to finish its approximation before starting the main render.")
            renderingBox.exec()
            return
        self.rendering = True
        newConfig = self.queue.pop(0)
        
        print(newConfig)
        # if mode is set to generate per frame call
        if newConfig["random"]["mode"] == "frame":
            newConfig = backend.apply_all_random_limits()
            print('='*30)
            print(newConfig)
            

        
        backend.set_runtime_config(newConfig)
        
        self.newThread = RenderThread()
        self.newThread.progress.connect(self.update_loading)
        self.newThread.finished.connect(self.complete_loading)
        self.GenerateRenders_Button.setText("Add render job to queue")


        self.newThread.start()
        self.windowUp()
        
    
    
    def windowUp(self):
        self.LoadingBox = LoadingScreen("")
        self.LoadingBox.update_text("")
        self.LoadingBox.show()

    def update_loading(self,text):
        self.LoadingBox.update_text(text)
    
    def complete_loading(self):
        self.newThread.quit()
        if not self.queue:
            self.rendering = False
            self.LoadingBox.update_text("Rendering complete")
            self.GenerateRenders_Button.setText("Generate Renders")
            self.render_preview_button.setEnabled(True)
        else:
            self.generate_render()

    def set_renders(self):#
        try:
            val = int(self.Number_of_renders_input_field.text())
            if val <= 0:
                self.Number_of_renders_input_field.setText("1") 
        except:
            self.Number_of_renders_input_field.setText("1") 
        try: 
            backend.set_renders(int(self.Number_of_renders_input_field.text()))
        except:
            print("Error")
    
    def set_angles(self):
        try: 
            backend.set_angles( [np.deg2rad(float(self.X_Degree_input_field.text())), np.deg2rad(float(self.Y_Degree_input_field.text())), np.deg2rad(float(self.Z_Degree_input_field.text()))] )
            print([np.deg2rad(float(self.X_Degree_input_field.text())), np.deg2rad(float(self.Y_Degree_input_field.text())), np.deg2rad(float(self.Z_Degree_input_field.text()))])
        except:
            print("Error")

class Port(QWidget):
    def __init__(self, parent: QWidget, tab_widget: QTabWidget, Scroll: QVBoxLayout):
        super().__init__(parent)
        
        class ilyaMessageBox(QMessageBox):
                def __init__(self, text, title):
                    super().__init__()
                    self.setText(text)
                    self.setWindowTitle(title)
                    self.exec()
        
                    
        def _display_import_message(successful_imps, failed_imps):
            """ display appropriate import message """
            if successful_imps > 0 and not failed_imps:
                QMessageBox.information(self, "Import Successful", f"All {successful_imps} objects were successfully imported.")

            elif successful_imps > 0 and failed_imps:
                error_message = f"Successfully imported {successful_imps} objects.\nFailed to import:\n"
                error_message += "\n".join([f"{name}: {error}" for name, error in failed_imps])
                QMessageBox.warning(self, "Partial Import", error_message)

            elif not successful_imps and failed_imps:
                # may have to cap this in the future to stop massive folders
                error_message = f"Failed to import all objects:\n"
                error_message += "\n".join([f"{name}: {error}" for name, error in failed_imps])
                QMessageBox.critical(self, "Import Failed", error_message)

        def process_file(path):
            """ helper function to process each file """
            supported_extensions = ('.blend', '.stl', '.obj')
            
            if not path.lower().endswith(supported_extensions):
                raise Exception(f"Unsupported file type. Only {', '.join(supported_extensions)} files are supported.")

            name = os.path.basename(os.path.normpath(path))
            
            obj = backend.RenderObject(filepath=path)
            shared_state.add_item(obj, name)

            return name, obj


        def _process_import(path, Scroll, successful_imps, failed_imps):
            """ process a single file during import """
            try:
                name, obj = process_file(path)
                successful_imps += 1

                # OOP button creation with menu for imported object
                button = _create_object_button(name, obj)
                Scroll.addWidget(button)

            except Exception as e:
                name = os.path.basename(os.path.normpath(path))
                failed_imps.append((name, str(e)))
        
                
        def _create_object_button(name, obj):
            """ create the button with menu options for an object """
            button = QPushButton(name)
            button.setMaximumWidth(175)

            menu = QMenu()
            incexc = menu.addAction('Included in Scene')
            ground = menu.addAction('Grounded')

            incexc.setCheckable(True)
            incexc.setChecked(True)
            incexc.triggered.connect(lambda: show_hide_object(obj, incexc.isChecked()))

            ground.setCheckable(True)
            ground.triggered.connect(lambda: ground_object(obj,ground.isChecked()))
                                
            button.setMenu(menu)
            Scroll.addWidget(button)

            Object_detect(tab_widget)


                
        self.Import_Object_Button = QPushButton("Import Objects", self)
        self.Import_Object_Button.clicked.connect(lambda: Get_Object_Filepath(Scroll))

        def Get_Object_Filepath(Scroll):
                current_lang = translator.current_language
                translations = translator.translations.get(current_lang, translator.translations.get("English", {}))

                import_box = QMessageBox()
                import_box.setText(translations.get("How would you like to import objects?", "How would you like to import objects?"))
                import_files_button = import_box.addButton(translations.get("Import Files", "Import Files"), QMessageBox.ActionRole)
                folder_button = import_box.addButton(translations.get("Folder", "Folder"), QMessageBox.ActionRole)
                cancel_button = import_box.addButton(translations.get("Cancel", "Cancel"), QMessageBox.RejectRole)
                
                import_box.exec()
                clicked_button = import_box.clickedButton()
                
                try:
                    if clicked_button == import_files_button:
                        paths = QFileDialog.getOpenFileNames(self, 'Open files', 'c:\\', "3D Model (*.blend *.stl *.obj)")[0]
                        if not paths:
                            return
                        
                        for path in paths:
                            obj = backend.RenderObject(filepath=path)

                            Name = os.path.basename(os.path.normpath(path))
                            shared_state.add_item(obj, Name)

                            button = QPushButton(Name)
                            button.setMaximumWidth(175)
                            menu = QMenu()
                            incexc = menu.addAction(translations.get("Included in Scene","Included in Scene"))
                            ground = menu.addAction(translations.get("Grounded","Grounded"))
                            
                            incexc.setCheckable(True)
                            incexc.setChecked(True)
                            incexc.triggered.connect(lambda: show_hide_object(obj,incexc.isChecked()))

                            ground.setCheckable(True)
                            ground.triggered.connect(lambda: ground_object(obj,ground.isChecked()))
                            
                            button.setMenu(menu)
                            Scroll.addWidget(button)


                    elif clicked_button == folder_button:

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

                                    Name = os.path.basename(os.path.normpath(full_path))
                                    shared_state.add_item(obj, Name)

                                    button = QPushButton(Name)
                                    button.setMaximumWidth(175)
                                    menu = QMenu()
                                    incexc = menu.addAction(translations.get("Included in Scene","Included in Scene"))
                                    ground = menu.addAction(translations.get("Grounded","Grounded"))
                                    
                                    incexc.setCheckable(True)
                                    incexc.setChecked(True)
                                    incexc.triggered.connect(lambda: show_hide_object(obj,incexc.isChecked()))

                                    ground.setCheckable(True)
                                    ground.triggered.connect(lambda: ground_object(obj,ground.isChecked()))
                                    
                                    button.setMenu(menu)
                                    Scroll.addWidget(button)

                    Object_detect(tab_widget)

                except Exception:
                    QMessageBox.warning(self, "Error when reading model", "The selected file is corrupt or invalid.")


                except Exception as e:
                    QMessageBox.warning(self, "Error when importing", f"Error: {str(e)}")
                


        #Second Section
        def Tutorial_Object(Scroll):
            current_lang = translator.current_language
            translations = translator.translations.get(current_lang, translator.translations.get("English", {}))

            Tutorial_Box = QMessageBox()
            Tutorial_Box.setText(translations.get("Please select a tutorial object from below", "Please select a tutorial object from below"))            
            object_types = ["Cube", "Cylinder", "Cone", "Plane", "Sphere", "Monkey"]
            button_map = {}
            
            for obj_type in object_types:
                translated_text = translations.get(obj_type, obj_type)
                button = Tutorial_Box.addButton(translated_text, QMessageBox.ActionRole)
                button_map[button] = obj_type 


            cancel_button = Tutorial_Box.addButton(translations.get("Cancel", "Cancel"), QMessageBox.ActionRole)
            Tutorial_Box.exec()
            clicked_button = Tutorial_Box.clickedButton()
            selected_object = button_map.get(clicked_button)
 
            
            try:
                if clicked_button != cancel_button:
                    Name = self.GetName()
                    if Name != False and len(Name) < 25:
                        obj = backend.RenderObject(primative = selected_object.upper())
                        if Name == "Object":
                            count = 1
                            while f"{Name} {len(shared_state.itemNames)+count}" in shared_state.itemNames:
                                count+=1
                            Name = f"{Name} {len(shared_state.itemNames)+count}"
                        shared_state.add_item(obj, Name)

                        button = QPushButton(Name)
                        button.setMaximumWidth(175)
                        menu = QMenu()
                        incexc = menu.addAction(translations.get("Included in Scene","Included in Scene"))
                        ground = menu.addAction(translations.get("Grounded","Grounded"))
                        
                        incexc.setCheckable(True)
                        incexc.setChecked(True)
                        incexc.triggered.connect(lambda: show_hide_object(obj,incexc.isChecked()))

                        ground.setCheckable(True)
                        ground.triggered.connect(lambda: ground_object(obj,ground.isChecked()))
                        
                        button.setMenu(menu)
                        Scroll.addWidget(button)

                        QApplication.instance().focusWidget().clearFocus()
                    elif Name != False and len(Name) >= 10:
                        error_box = ilyaMessageBox("Name is too long!", "Error")
                    else:
                        pass
                        
            except Exception as e:
                print(e)

                error_title = translations.get("Error", "Error")
                error_text = translations.get("Error loading tutorial object.", "Error loading tutorial object.")
                error_box = QMessageBox()
                error_box.setWindowTitle(error_title)
                error_box.setText(error_text)
                error_box.exec()
                error_box = ilyaMessageBox(error_text, error_title)
                
    
            Object_detect(tab_widget)

        self.TutorialObjects_Button = QPushButton('Tutorial Objects', self)
        self.TutorialObjects_Button.clicked.connect(lambda: Tutorial_Object(Scroll))

        #Third Section --> LEFT FOR NOW
        

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
                    tab_widget(i).update_ui_by_config()

                success_box = ilyaMessageBox("Setting imported successfully.", "Success")
            except Exception:
                QMessageBox.warning(self, "Error when reading JSON", "The selected file is corrupt or invalid.")


        self.ImportSettings_Button = QPushButton('Import Settings', self)
        self.ImportSettings_Button.clicked.connect(lambda: Get_Settings_Filepath(tab_widget))

        def delete_object(tab_widget, scroll):
            current_lang = translator.current_language
            translations = translator.translations.get(current_lang, translator.translations.get("English", {}))
            
            to_delete = QMessageBox()
            to_delete.setText(translations.get("Please select an object to remove from below", "Please select an object to remove from below"))

            if (not shared_state.items):
                warning_text = translations.get("Warning", "Warning")
                warning_msg = translations.get("There are no objects to delete.", "There are no objects to delete.")
                return QMessageBox.warning(self, warning_text, warning_msg)

            for i in range(len(shared_state.itemNames)):
                to_delete.addButton(str(shared_state.itemNames[i]), QMessageBox.ActionRole)
            
            cancel_button = to_delete.addButton(translations.get("Cancel", "Cancel"), QMessageBox.ActionRole)
            to_delete.exec()
            choice = str(to_delete.clickedButton().text())




            if choice != cancel_button.text():
                obj_index = shared_state.itemNames.index(choice)
                obj = shared_state.items[obj_index]
                scroll.itemAt(obj_index).widget().setParent(None)
                try:
                    shared_state.remove_item(obj)
                    success_box = ilyaMessageBox("Object successfully deleted", "Success")
                    backend.update_log(f'{obj} object deleted\n')
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
                    QMessageBox.warning(self, translations.get("Warning", "Warning"),translations.get("You have deleted all of the objects, object manipulation tabs have been disabled.", "You have deleted all of the objects, object manipulation tabs have been disabled."))
    

        self.Delete_Object_Button = QPushButton('Delete Object', self)
        self.Delete_Object_Button.clicked.connect(lambda: delete_object(tab_widget, Scroll))
        
        
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

        self.Export_Interaction_Button = QPushButton("Export Interaction Log", self)
        self.Export_Interaction_Button.clicked.connect(lambda: Export_Interaction())

        main_layout = QGridLayout()

        main_layout.addWidget(self.TutorialObjects_Button, 0, 0)
        main_layout.addWidget(self.Import_Object_Button, 0, 1)
        main_layout.addWidget(self.Delete_Object_Button, 0, 2)
        main_layout.addWidget(self.ExportSettings_Button, 0, 3)
        main_layout.addWidget(self.ImportSettings_Button, 0, 4)
        main_layout.addWidget(self.SelectRenderFolder_Button, 0, 5)
        main_layout.addWidget(self.Export_Interaction_Button, 0, 6)
        self.setLayout(main_layout)

        def Export_Interaction():
            try:
                export_path = QFileDialog.getExistingDirectory(self, "Select Folder")

                if (export_path == "" or export_path == None):
                    pass
                else:
                    backend.export_interaction(export_path)
                    success_box = ilyaMessageBox("Interaction exported successfully.", "Success")
                   
            except:
                error_box = ilyaMessageBox("There was an error selecting folder, please try again.", "Error")

        def show_hide_object(object,state):
            backend.toggle_object(object,state)
        
        def ground_object(object,state):
            backend.ground_object(object,state)

                
        translator.languageChanged.connect(self.translateUi)
        self.translateUi()


    def translateUi(self):
        """Apply translations to UI elements."""
        current_lang = translator.current_language
        translation = translator.translations.get(current_lang, translator.translations.get("English", {}))
        self.Delete_Object_Button.setText(translation.get("Delete Object", "Delete Object"))
        self.Import_Object_Button.setText(translation.get("Import Object", "Import Object"))
        self.TutorialObjects_Button.setText(translation.get("Tutorial Object", "Tutorial Object"))
        self.ExportSettings_Button.setText(translation.get("Export Settings", "Export Settings"))
        self.ImportSettings_Button.setText(translation.get("Import Settings", "Import Settings"))
        self.SelectRenderFolder_Button.setText(translation.get("Change Render Folder", "Change Render Folder"))

            
        
    def GetName(self):
        try:
            current_lang = translator.current_language
            translations = translator.translations.get(current_lang, translator.translations.get("English", {}))
            window_title = translations.get("Object Name", "Object Name")
            window_text = translations.get("Enter Object Name:", "Enter Object Name:")
            ObjName, State = QtWidgets.QInputDialog.getText(self, window_title, window_text)

            if State and ObjName != "":
                return ObjName
            elif not State:
                return False
            else:
                return "Object"
        except:
            pass

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
        self.lighting_colour.editingFinished.connect(lambda: self.update_colour_example_text(self.lighting_colour.text()))
        self.colour_example = QLabel(self)
        self.lighting_colour.setText("#ffffff")
        
        
        #self.light.set_color("#000000")
        self.colour_example.setStyleSheet(("background-color: {c}").format(c = "#ffffff"))
        ###


        ###
        self.lighting_strength_label = QLabel("Strength: ", self)
        self.lighting_strength_label.setToolTip('Strength of lighting element')
        self.lighting_strength_input_field = QLineEdit(self)
        self.lighting_strength_input_field.setText("1")
        self.lighting_strength_input_field.textEdited.connect(lambda: self.Update_slider(self.strength_slider, self.lighting_strength_input_field.text()))
        self.lighting_strength_input_field.editingFinished.connect(self.update_strength)

        self.strength_slider = QSlider(self)
        self.strength_slider.setRange(0,100)
        self.strength_slider.setOrientation(QtCore.Qt.Horizontal)
        self.strength_slider.sliderMoved.connect(lambda val: self.Slider_Update(val, self.lighting_strength_input_field))
        self.strength_slider.sliderReleased.connect(self.update_strength)
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
        self.Xlight_angle_input_field.textEdited.connect(lambda: self.Update_slider(self.Xlight_angle_slider, self.Xlight_angle_input_field.text()))
        self.Xlight_angle_input_field.editingFinished.connect(lambda: self.set_rotation_from_field(self.Xlight_angle_slider, self.Xlight_angle_input_field.text()))

        self.Xlight_angle_slider = QSlider(self)
        self.Xlight_angle_slider.setRange(0,359)
        self.Xlight_angle_slider.setOrientation(QtCore.Qt.Horizontal)
        self.Xlight_angle_slider.sliderMoved.connect(lambda val: self.Slider_Update(val, self.Xlight_angle_input_field))
        self.Xlight_angle_slider.sliderReleased.connect(self.update_rotation)

        ###
        self.Ylight_angle_label = QLabel("Y:", self)
        self.Ylight_angle_input_field = QLineEdit(self)
        self.Ylight_angle_input_field.setText("0")
        self.Ylight_angle_input_field.textEdited.connect(lambda: self.Update_slider(self.Ylight_angle_slider, self.Ylight_angle_input_field.text()))
        self.Ylight_angle_input_field.editingFinished.connect(lambda: self.set_rotation_from_field(self.Ylight_angle_slider, self.Ylight_angle_input_field.text()))

        self.Ylight_angle_slider = QSlider(self)
        self.Ylight_angle_slider.setRange(0,359)
        self.Ylight_angle_slider.setOrientation(QtCore.Qt.Horizontal)
        self.Ylight_angle_slider.sliderMoved.connect(lambda val: self.Slider_Update(val, self.Ylight_angle_input_field))
        self.Ylight_angle_slider.sliderReleased.connect(self.update_rotation)
        ###
        self.Zlight_angle_label = QLabel("Z:", self)
        self.Zlight_angle_input_field = QLineEdit(self)
        self.Zlight_angle_input_field.setText("0")
        self.Zlight_angle_input_field.textEdited.connect(lambda: self.Update_slider(self.Zlight_angle_slider, self.Zlight_angle_input_field.text()))
        self.Zlight_angle_input_field.editingFinished.connect(lambda: self.set_rotation_from_field(self.Zlight_angle_slider, self.Zlight_angle_input_field.text()))

        self.Zlight_angle_slider = QSlider(self)
        self.Zlight_angle_slider.setRange(0,359)
        self.Zlight_angle_slider.setOrientation(QtCore.Qt.Horizontal)
        self.Zlight_angle_slider.sliderMoved.connect(lambda val: self.Slider_Update(val, self.Zlight_angle_input_field))
        self.Zlight_angle_slider.sliderReleased.connect(self.update_rotation)
       
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
        translator.languageChanged.connect(self.translateUi)
        self.translateUi()


    def change_type(self):
        self.light.set_type(self.light_type_combobox.currentText())


    def update_strength(self):
        field = self.lighting_strength_input_field
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
            self.light.set_loc([float(x),float(y),float(z)])
        except:
            pass
    
    def set_loc_from_field(self,):

        x = self.Xlight_coords_input_field.text()
        y = self.Ylight_coords_input_field.text()
        z = self.Zlight_coords_input_field.text()
        try:
            self.light.set_loc([float(x),float(y),float(z)])
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

    def update_rotation(self):

        x = self.Xlight_angle_input_field.text()
        y = self.Ylight_angle_input_field.text()
        z = self.Zlight_angle_input_field.text()

        self.light.set_rotation([float(x),float(y),float(z)])
        

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
        if field.isEnabled():
            try:
                if field.text() == '':
                    field.setText('0')
                if float(field.text()) > val or float(field.text()) + 0.5 < val:
                    field.setText(str(val))
            except:
                field.setText("0.0")
    
    def set_rotation_from_field(self, slider, val):
        try:
            self.Update_slider(slider, val)

            x = self.Xlight_angle_input_field.text()
            y = self.Ylight_angle_input_field.text()
            z = self.Zlight_angle_input_field.text()
            
            self.light.set_rotation([float(x),float(y),float(z)])
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
                
    def isValidHexaCode(self, str):
 
        if (str[0] != '#'):
            return
    
        if (not(len(str) == 4 or len(str) == 7)):
            self.lighting_colour.setText("#ffffff")
    
        for i in range(1, len(str)):
            if (not((str[i] >= '0' and str[i] <= '9') or (str[i] >= 'a' and str[i] <= 'f') or (str[i] >= 'A' or str[i] <= 'F'))):
                self.lighting_colour.setText("#ffffff")
    
        return


    def update_colour_example_text(self, colour):
        self.isValidHexaCode(self.lighting_colour.text())
        
        try:
            if bool(regex("(([0-9]|[a-f])([0-9]|[a-f])([0-9]|[a-f])([0-9]|[a-f])([0-9]|[a-f])([0-9]|[a-f]))", colour)) or bool(regex("#(([0-9]|[a-f])([0-9]|[a-f])([0-9]|[a-f])([0-9]|[a-f])([0-9]|[a-f])([0-9]|[a-f]))", colour)):
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



    def translateUi(self):
        """Apply translations to UI elements."""
        current_lang = translator.current_language
        translation = translator.translations.get(current_lang, translator.translations.get("English", {}))
        self.light_angle_label.setText(translation.get("Lighting Angle", "Lighting Angle"))
        self.light_coords_label.setText(translation.get("Lighting Co-ords", "Lighting Co-ords"))
        self.lighting_strength_label.setText(translation.get("Strength", "Strength"))
        self.radius_label.setText(translation.get("Radius", "Radius"))
        self.light_type_label.setText(translation.get("Type", "Type"))
        self.colour_label.setText(translation.get("Colour", "Colour"))
        self.colour_select_button.setText(translation.get("Select Colour", "Select Colour"))

        

class Settings(QWidget):
    def __init__(self, parent: QWidget, tab_widget: QTabWidget):
        super().__init__(parent)
        
        #Button Labels
        main_layout = QGridLayout()
        self.colour_scheme_button = QPushButton('Colour Theme', self)
        self.Help_button = QPushButton('Help', self)
        self.Languages = QPushButton('Languages', self)
        self.current_language = "English"
        self.translations = translator.translations

        #button clicks
        self.Help_button.clicked.connect(self.openWebsite)
        self.colour_scheme_button.clicked.connect(self.Colour_Scheme_Press)
        translator.languageChanged.connect(self.translateUi)
        self.Languages.clicked.connect(self.Language_button_press)
            
        #button Layout
        main_layout.addWidget(self.colour_scheme_button, 0, 1)
        main_layout.addWidget(self.Help_button, 0, 2)
        main_layout.addWidget(self.Languages, 0, 3)
        self.setLayout(main_layout)

        self.load_settings()
        
    def openWebsite(self):
        import webbrowser
        webbrowser.open('https://github.com/b3nb07/CS3028_Group_Project')

    def Colour_Scheme_Press(self):
        colour_box = QMessageBox(self)
        colour_box.setWindowTitle("Select Colour Scheme")
        colour_box.setText("Please select a colour scheme:")

        # Add buttons for different styles
        dark_mode = colour_box.addButton("Dark Mode", QMessageBox.ActionRole)
        light_mode = colour_box.addButton("Light Mode", QMessageBox.ActionRole)
        colourblind1 = colour_box.addButton("Factory New", QMessageBox.ActionRole)
        default = colour_box.addButton("Colourblind 2", QMessageBox.ActionRole)
        dyslexic = colour_box.addButton("Light Mode 2", QMessageBox.ActionRole)
        colour_scheme1 = colour_box.addButton("Colour Mode 1", QMessageBox.ActionRole)
        Image_test = colour_box.addButton("Imagetest", QMessageBox.ActionRole)
        colour_box.addButton(QMessageBox.Cancel)

        colour_box.exec()

        # Apply styles based on button clicked
        if colour_box.clickedButton() == dark_mode:
            self.apply_stylesheet("DarkMode.qss")
        elif colour_box.clickedButton() == light_mode:
            self.apply_stylesheet("LightMode.qss")
        elif colour_box.clickedButton() == colourblind1:
            self.apply_stylesheet("colourblind1.qss")
        elif colour_box.clickedButton() == default:
            self.apply_stylesheet("default.qss")
        elif colour_box.clickedButton() == dyslexic:
            self.apply_stylesheet("Dyslexic.qss")
        elif colour_box.clickedButton() == colour_scheme1:
            self.apply_stylesheet("ColourScheme1.qss")
        elif colour_box.clickedButton() == Image_test:
            self.apply_stylesheet("ImageTest.qss")


    def apply_stylesheet(self, filename):
        """Loads and applies stylesheet, then saves the choice"""
        qss_path = os.path.join(os.path.dirname(__file__), "..", "Style", filename)
        try:
            with open(qss_path, "r") as file:
                qss = file.read()
                QApplication.instance().setStyleSheet(qss)  
                self.save_settings(filename)  # Save the colour theme choice
        except FileNotFoundError:
            print(f"Error: {filename} not found")


    def Language_button_press(self):
        language_box = QMessageBox(self)
        language_box.setWindowTitle("Select a Language")
        language_box.setText("Please select a Language:")

        # Add buttons for different styles
        English = language_box.addButton("English", QMessageBox.ActionRole)
        Spanish = language_box.addButton("Español", QMessageBox.ActionRole)
        Portuguese = language_box.addButton("Português", QMessageBox.ActionRole)
        Mandarin = language_box.addButton("中文", QMessageBox.ActionRole)
        language_box.addButton(QMessageBox.Cancel)
        language_box.exec()

        # Apply styles based on button clicked
        if language_box.clickedButton() == English:
            translator.setLanguage("English")
        elif language_box.clickedButton() == Spanish:
            translator.setLanguage("Spanish")
        elif language_box.clickedButton() == Portuguese:
            translator.setLanguage("Portuguese")
        elif language_box.clickedButton() == Mandarin:
            translator.setLanguage("Mandarin")
        self.save_language_setting()



    def translateUi(self):
        current_lang = translator.current_language
        translation = self.translations.get(current_lang, self.translations.get("English"))
        self.colour_scheme_button.setText(translation.get("Colour Theme", "Colour Theme"))
        self.Help_button.setText(translation.get("Help", "Help"))
        self.Languages.setText(translation.get("Languages", "Languages"))

    def save_settings(self, Colour_Setup):
        settings = QSettings("UserSettings")
        settings.setValue("theme", Colour_Setup)
        settings.sync()

    def load_settings(self):
        settings = QSettings("UserSettings")
        Colour_Setup = settings.value("theme", "LightMode.qss")  # default mode is light mode 
        self.apply_stylesheet(Colour_Setup)

        saved_lang = settings.value("language", "English")
        if saved_lang in translator.translations:
            translator.setLanguage(saved_lang)
        else:
            translator.setLanguage("English") # default language english
        
        self.translateUi()

    def save_language_setting(self):
        settings = QSettings("UserSettings")
        settings.setValue("language", translator.current_language)

def startApp():
    app.exec()
    try:
        app.focusWidget().clearFocus()
    except:
        pass

if __name__ == "__main__":
    app = QApplication(sys.argv)
    tab_dialog = TabDialog()
    tab_dialog.show()

    sys.exit(startApp())