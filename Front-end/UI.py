from functools import cached_property
import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QTabWidget
from PyQt5 import QtCore, QtWidgets

#https://stackoverflow.com/questions/66852575/how-to-create-navigation-bar-in-in-pyqt5
class Page(QtWidgets.QWidget):
    """
    Navbar page creation class
    """
    completeChanged = QtCore.pyqtSignal()

    def __init__(self, parent=None):
        super().__init__(parent)
        lay = QtWidgets.QVBoxLayout(self)
        lay.addWidget(self.container)

    @cached_property
    def container(self):
        return QtWidgets.QWidget()

class TabWizard(QTabWidget):
    """
    creates a tab like
    """
    def __init__(self, parent=None):
        super().__init__(parent)

    def addPage(self, page, title):
        if not isinstance(page, Page):
            raise TypeError(f"{page} must be a Page object")
        self.addTab(page, title)

class Widget(QtWidgets.QWidget):
    """
    Adding all pages into a tabwizard
    """
    def __init__(self):
        super().__init__()
        #nav bar widget adding
        self.tabwizard = TabWizard()
        lay = QVBoxLayout(self)
        lay.addWidget(self.tabwizard)
        #pages
        self.tabwizard.addPage(Page1(), "Page 1")
        self.tabwizard.addPage(Page2(), "Page 2")
        self.tabwizard.addPage(Page3(), "Page 3")
        self.tabwizard.addPage(Page4(), "Page 4")
        self.tabwizard.addPage(Page5(), "Page 5")

class Page1(Page):
    def __init__(self, parent=None):
        """
        Page 1: Dibs
        """
        super().__init__(parent)

class Page2(Page):
    """
    Page 2:
    """
    def __init__(self, parent=None):
        super().__init__(parent)

class Page3(Page):
    """
    Page 3:
    """
    def __init__(self, parent=None):
        super().__init__(parent)

class Page4(Page):
    """
    Page 4:
    """
    def __init__(self, parent=None):
        super().__init__(parent)

class Page5(Page):
    """
    Page 5:
    """
    def __init__(self, parent=None):
        super().__init__(parent)

class MainWindow(QMainWindow):
    """
    Main Window for all the elements
    """
    def __init__(self):
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
        self.setMinimumSize(400, 300) # minimum size of rogram
        self.show()

    def resizeEvent(self, event):
        """
        On re sizing all elements in the program should be re-adjusted to fit
        """
        window_height = self.height() # get screen height
        navbar_height = int(window_height * 0.20)  # Top 20% for navbar
        self.navbar.setFixedHeight(navbar_height) # emviroment
        super().resizeEvent(event)  # handle resize event

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
