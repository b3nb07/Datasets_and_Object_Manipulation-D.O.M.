#import stuff

import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QPushButton

#main
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        # Get screen geometry and set window size to half
        screen = QApplication.primaryScreen()
        screen_geometry = screen.geometry()
        self.setGeometry(
            screen_geometry.width() // 4,  # x position to center the window
            screen_geometry.height() // 4,  # y position to center the window
            screen_geometry.width() // 2,
            screen_geometry.height() // 2
        )
        self.setWindowTitle('CS 3028 Project')

        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        self.layout = QVBoxLayout()

        # Remove spacing and margins to touch
        self.layout.setSpacing(0)
        self.layout.setContentsMargins(0, 0, 0, 0)

        # Button bar
        self.button_bar = QWidget()
        button_layout = QHBoxLayout()
        button_layout.setSpacing(0)
        button_layout.setContentsMargins(0, 0, 0, 0)

        # Create buttons (temp since buttons need dfifferent stuff)
        self.buttons = []
        for i in range(1, 6):
            button = QPushButton(f'Button {i}', self.button_bar)
            button.setFixedHeight(int(self.height() * 0.05))  # Set buttons to take full height
            button.clicked.connect(self.on_click)
            button_layout.addWidget(button)
            self.buttons.append(button)

        self.button_bar.setLayout(button_layout)
        self.button_bar.setStyleSheet("border: 1px solid black; background-color: gray;")

        # Top bar
        self.top_bar = QWidget()
        self.top_bar.setStyleSheet("background-color: gray;")

        # Environment
        self.environment = QWidget()
        self.environment.setStyleSheet("background-color: black;")

        # Add widgets to layout
        self.layout.addWidget(self.button_bar)
        self.layout.addWidget(self.top_bar)
        self.layout.addWidget(self.environment)
        central_widget.setLayout(self.layout)

        # Minimum size
        self.setMinimumSize(400, 300)

        #dispaly all widgets/buttons
        self.show()

    # Resize dynamically
    def resizeEvent(self, event):
        ##https://stackoverflow.com/questions/35887237/current-screen-size-in-python3-with-pyqt5
        window_height = self.height()
        button_bar_height = int(window_height * 0.05)  # button_bar height to 5%
        top_bar_height = int(window_height * 0.10)     # top_bar height to 10%
        self.top_bar.setFixedHeight(top_bar_height)
        self.button_bar.setFixedHeight(button_bar_height)

        # Adjust button height dynamically
        for button in self.buttons:
            button.setFixedHeight(int(button_bar_height))

        super().resizeEvent(event)  # resize

    #clicky clicky tee hee
    def on_click(self):
        print('PyQt5 button click')

# Main function
def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
