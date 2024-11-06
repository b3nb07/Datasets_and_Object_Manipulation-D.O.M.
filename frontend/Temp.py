import sys
from PyQt5.QtWidgets import QApplication, QWidget, QSlider, QLabel, QVBoxLayout
from PyQt5.QtCore import Qt

class SliderApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Slider App")
        self.setGeometry(100, 100, 400, 200)  # (x, y, width, height)

        layout = QVBoxLayout()

        # Create a QSlider widget
        self.slider = QSlider(Qt.Horizontal, self)

        # Create a QLabel widget
        self.label = QLabel("Slider Value: 0", self)
        layout.addWidget(self.label)

        # Connect the slider's valueChanged signal to the update_label slot
        self.slider.valueChanged.connect(self.update_label)

        self.setLayout(layout)

    # Slot function to update the label with the current slider value
    def update_label(self):
        value = self.slider.value()
        self.label.setText(f"Slider Value: {value}")

def main():
    app = QApplication(sys.argv)
    window = SliderApp()
    window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()