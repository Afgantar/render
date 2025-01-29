import sys
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QVBoxLayout, QHBoxLayout, QWidget, QLineEdit, QPushButton, QLabel, QSplitter
)
from PySide6.QtCore import Qt
from render import GLWidget

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("3D Point Renderer")
        self.setGeometry(100, 100, 1280, 720)  # Larger window size

        # Central widget
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        # Main layout
        self.main_layout = QHBoxLayout(self.central_widget)

        # Left panel for input fields
        self.left_panel = QWidget()
        self.left_panel.setMaximumWidth(300)  # Limit the width of the input panel
        self.left_layout = QVBoxLayout(self.left_panel)

        # Points container
        self.point_container = QWidget()
        self.point_container.setMaximumWidth(300)
        self.container_layout = QVBoxLayout(self.point_container)

        # Input fields for XYZ
        self.x_input = QLineEdit(self)
        self.y_input = QLineEdit(self)
        self.z_input = QLineEdit(self)
        self.add_point_button = QPushButton("Add Point", self)

        # Point container title
        self.container_layout.addWidget(QLabel("Points:"))

        # Add input fields and button to the left layout
        self.left_layout.addWidget(QLabel("X:"))
        self.left_layout.addWidget(self.x_input)
        self.left_layout.addWidget(QLabel("Y:"))
        self.left_layout.addWidget(self.y_input)
        self.left_layout.addWidget(QLabel("Z:"))
        self.left_layout.addWidget(self.z_input)
        self.left_layout.addWidget(self.add_point_button)
        self.left_layout.addWidget(self.point_container)
        self.left_layout.addStretch()  # Add stretch to push fields to the top

        # OpenGL widget for rendering
        self.gl_widget = GLWidget(self)

        # Splitter to separate the input panel and the rendering widget
        self.splitter = QSplitter(Qt.Horizontal)
        self.splitter.addWidget(self.left_panel)
        self.splitter.addWidget(self.gl_widget)
        self.splitter.setSizes([200, 800])  # Allocate more space to the rendering widget

        # Add the splitter to the main layout
        self.main_layout.addWidget(self.splitter)

        # Connect button to add point function
        self.add_point_button.clicked.connect(self.add_point)

        # List to store points
        self.points = []

    def add_point(self):
        try:
            x = float(self.x_input.text())
            y = float(self.y_input.text())
            z = float(self.z_input.text())
            self.points.append((x, y, z))
            self.gl_widget.update_points(self.points)
            self.container_layout.addWidget(QLabel(f"{x}, {y}, {z}"))
        except ValueError:
            print("Invalid input")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())