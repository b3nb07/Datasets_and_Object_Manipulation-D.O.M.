from functools import cached_property
import sys
from PyQt5 import QtCore, QtWidgets
from functools import cached_property

from PyQt5.QtWidgets import QApplication, QPushButton, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QTabWidget, QLabel, QLineEdit, QComboBox, QCheckBox
from PyQt5.QtCore import * 
from PyQt5.QtGui import * 
from PyQt5.QtWidgets import *

class RandomTabDialog(QWidget):
    def __init__(self, parent: QWidget = None):
        super().__init__(parent)

        self.setWindowTitle("Datasets and Object Modeling")

        tab_widget = QTabWidget()
        tab_widget.addTab(RandomObject(self), "Object")
        tab_widget.addTab(RandomPivot(self), "Pivot Point")
        tab_widget.addTab(RandomRender(self), "Render")
        tab_widget.addTab(RandomLight(self), "Light")

        main_layout = QVBoxLayout()
        main_layout.addWidget(tab_widget)
        self.setLayout(main_layout)

class RandomObject(QWidget):
    def __init__(self, parent: QWidget):
        super().__init__(parent)

        self.CheckBoxes = {}
        self.LowerBounds = {}
        self.UpperBounds = {}

        main_layout = QGridLayout()

        main_layout.addWidget(QComboBox(), 0, 10)
        main_layout.itemAtPosition(0, 10).widget().addItem("Object1")
        main_layout.itemAtPosition(0, 10).widget().addItem("Object2")
        main_layout.addWidget(QCheckBox("Set all random", self), 1, 10)
        main_layout.itemAtPosition(1, 10).widget().toggled.connect(lambda:
             self.set_all_random(main_layout, main_layout.itemAtPosition(1, 10).widget().isChecked()))

        main_layout.addWidget(QLabel("Co-ords:", self), 0, 0)
        self.gen_field("X", main_layout, 0, 1)
        self.gen_field("Y", main_layout, 0, 2)
        self.gen_field("Z", main_layout, 0, 3)

        main_layout.addWidget(QLabel("Rotation", self), 0, 3)
        self.gen_field("Pitch", main_layout, 3, 1)
        self.gen_field("Roll", main_layout, 3, 2)
        self.gen_field("Yaw", main_layout, 3, 3)
        
        main_layout.addWidget(QLabel("Scale", self), 0, 7)
        self.gen_field("Width", main_layout, 6, 1)
        self.gen_field("Height", main_layout, 6, 2)
        self.gen_field("Length", main_layout, 6, 3)

        #print(main_layout.itemAtPosition(0, 0).widget().setText("Electric boogalo"))
        #how to change values

        self.setLayout(main_layout)

    def gen_field(self, Fieldname, Layout, X, Y):
        Field = QCheckBox(Fieldname, self)
        Field_LowerBound = QLineEdit(parent=self)
        Field_UpperBound = QLineEdit(parent=self)

        self.addCheck(Field, Fieldname, Layout, X, Y)
        self.addLower(Field_LowerBound, Fieldname, Layout, X+1, Y)
        self.addUpper(Field_UpperBound, Fieldname, Layout, X+2, Y)

        Field.toggled.connect(lambda: self.un_checked(Field.isChecked(), Field_LowerBound, Field_UpperBound))
        self.un_checked(False, Field_LowerBound, Field_UpperBound)
        
    def addCheck(self, Field, Fieldname, Layout, X, Y):
        Layout.addWidget(Field, Y, X)
        self.CheckBoxes[f"{Layout.itemAtPosition(0, 10).widget().currentText()}{Fieldname}"] = (X, Y)

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
            print(keys)
            main_layout.itemAtPosition(self.CheckBoxes[keys][1], self.CheckBoxes[keys][0]).widget().setChecked(State)


class RandomPivot(QWidget):
    def __init__(self, parent: QWidget):
        super().__init__(parent)

        def __init__(self):
            pass

class RandomRender(QWidget):
    def __init__(self, parent: QWidget):
        super().__init__(parent)

        def __init__(self):
            pass

class RandomLight(QWidget):
    def __init__(self, parent: QWidget):
        super().__init__(parent)

        def __init__(self):
            pass


if __name__ == "__main__":
    app = QApplication(sys.argv)
    tab_dialog = RandomTabDialog()
    tab_dialog.show()

    sys.exit(app.exec())