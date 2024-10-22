"""Importing"""

from functools import cached_property
import sys
from PyQt5.QtWidgets import QApplication, QPushButton, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QTabWidget, QLabel, QLineEdit, QComboBox
from PyQt5 import QtCore, QtWidgets

"""Importing"""

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
        self.tabwizard.addPage(Page2(), "Page 2")
        self.tabwizard.addPage(Page3(), "Page 3")
        self.tabwizard.addPage(Page4(), "Page 4")
        self.tabwizard.addPage(Page5(), "Page 5")

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
        self.Position_layout = QVBoxLayout()
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

        self.XObj_pos.setGeometry(int(self.width()*0.01), int(self.height()*0.25),5, 30)
        self.XObj_pos_input_field.setGeometry(int(self.width()*0.02), int(self.height()*0.25), int(self.width()*0.1), 20)
        
        self.X_button_minus.setGeometry(int(self.width()*0.125), int(self.height()*0.25), int(self.width()*0.025), 20)
        self.X_button_plus.setGeometry(int(self.width()*0.125+int(self.width()*0.025)), int(self.height()*0.25), int(self.width()*0.025), 20)

        self.YObj_pos.setGeometry(int(self.width()*0.01), int(self.height()*0.50),5, 30)
        self.YObj_pos_input_field.setGeometry(int(self.width()*0.02), int(self.height()*0.5), int(self.width()*0.1), 20)

        self.Y_button_minus.setGeometry(int(self.width()*0.125), int(self.height()*0.50), int(self.width()*0.025), 20)
        self.Y_button_plus.setGeometry(int(self.width()*0.125+int(self.width()*0.025)), int(self.height()*0.50), int(self.width()*0.025), 20)

        self.ZObj_pos.setGeometry(int(self.width()*0.01), int(self.height()*0.75),5, 30)
        self.ZObj_pos_input_field.setGeometry(int(self.width()*0.02), int(self.height()*0.75), int(self.width()*0.1), 20)

        self.Z_button_minus.setGeometry(int(self.width()*0.125), int(self.height()*0.75), int(self.width()*0.025), 20)
        self.Z_button_plus.setGeometry(int(self.width()*0.125+int(self.width()*0.025)), int(self.height()*0.75), int(self.width()*0.025), 20)
    

        ##########################################################

        self.Object_scale_title.setGeometry(int(self.width()*0.30), int(self.height()*0.01), 200, 30)

        self.Width_Obj_pos.setGeometry(int(self.width()*0.30), int(self.height()*0.2), 50, 30)
        self.Width_Obj_pos_input_field.setGeometry(int(self.width()*0.35), int(self.height()*0.25), int(self.width()*0.1), 20)
        self.W_slider.setGeometry(QtCore.QRect(int(self.width()*0.48), int(self.height()*0.28), int(self.width()*0.2), 16))

        self.Height_Obj_pos.setGeometry(int(self.width()*0.30), int(self.height()*0.45), 50, 30)
        self.Height_Obj_pos_input_field.setGeometry(int(self.width()*0.35), int(self.height()*0.5), int(self.width()*0.1), 20)
        self.H_slider.setGeometry(QtCore.QRect(int(self.width()*0.48), int(self.height()*0.52), int(self.width()*0.2), 16))

        self.Length_Obj_pos.setGeometry(int(self.width()*0.30), int(self.height()*0.7), 50, 30)
        self.Length_Obj_pos_input_field.setGeometry(int(self.width()*0.35), int(self.height()*0.75), int(self.width()*0.1), 20)
        self.L_slider.setGeometry(QtCore.QRect(int(self.width()*0.48), int(self.height()*0.77), int(self.width()*0.2), 16))

        self.combo_box.setGeometry(self.width()-self.combo_box.width(), 0, self.combo_box.width(), self.combo_box.height())


class Page2(Page):
    """
    Page 2:
    """
    def __init__(self, parent=None):
        """
        Initialise "Page n"

        Args:
            parent
            
        Methods:

        """
        super().__init__(parent)
        

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

class Page4(Page):
    """
    Page 4:
    """
    def __init__(self, parent=None):
        """
        Initialise "Page n"

        Args:
            parent
            
        Methods:

        """
        super().__init__(parent)

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
        navbar_height = int(window_height * 0.25)  # Top 20% for navbar
        if navbar_height > 150: # Prevents Navbar being massive
            navbar_height = 150
        self.navbar.setFixedHeight(navbar_height) # emviroment
        super().resizeEvent(event)  # handle resize event

if __name__ == "__main__":
    
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
