from OpenGL.GL import *
from OpenGL.GLUT import *
import numpy as np
from PySide6.QtOpenGLWidgets import QOpenGLWidget
from PySide6.QtCore import Qt

class GLWidget(QOpenGLWidget):
    def __init__(self, parent):
        super().__init__(parent)
        self.points = []
        self.rotation_x = 30
        self.rotation_y = 30
        self.last_pos = None
        self.scaler = 0.5

    def initializeGL(self):
        # Initialize GLUT
        glutInit()

        # Set up OpenGL settings
        glClearColor(1.0, 1.0, 1.0, 1.0)
        glEnable(GL_DEPTH_TEST)

        # Enable lighting
        glEnable(GL_LIGHTING)
        glEnable(GL_LIGHT0)

        # Set up light properties
        light_position = [1.0, 1.0, 1.0, 0.0]  # Directional light from the top-right
        light_color = [1.0, 1.0, 1.0, 1.0]  # White light
        glLightfv(GL_LIGHT0, GL_POSITION, light_position)
        glLightfv(GL_LIGHT0, GL_DIFFUSE, light_color)

        # Set up material properties
        self.material_diffuse = [1.0, 0.0, 0.0, 1.0]  # Red color
        self.material_specular = [1.0, 1.0, 1.0, 1.0]  # White specular highlights
        self.material_shininess = [50.0]  # Shininess (higher = sharper highlights)

    def resizeGL(self, w, h):
        glViewport(0, 0, w, h)
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()

        # Define a perspective projection matrix manually
        aspect = w / h
        fov = 45.0  # Field of view
        near = 1.0  # Near clipping plane
        far = 100.0  # Far clipping plane

        # Perspective projection matrix
        f = 1.0 / np.tan(np.radians(fov) / 2.0)
        projection_matrix = np.array([
            [f / aspect, 0, 0, 0],
            [0, f, 0, 0],
            [0, 0, (far + near) / (near - far), (2 * far * near) / (near - far)],
            [0, 0, -1, 0]
        ], dtype=np.float32)

        # Load the projection matrix into OpenGL
        glLoadMatrixf(projection_matrix.T)

        glMatrixMode(GL_MODELVIEW)

    def paintGL(self):
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glLoadIdentity()
        glTranslatef(0.0, 0.0, -5.0)
        glRotatef(self.rotation_x, 1, 0, 0)
        glRotatef(self.rotation_y, 0, 1, 0)

        self.draw_axes()
        self.draw_grid_xy()
        self.draw_grid_xz()
        self.draw_grid_yz()

        # Set material properties
        glMaterialfv(GL_FRONT, GL_DIFFUSE, self.material_diffuse)
        glMaterialfv(GL_FRONT, GL_SPECULAR, self.material_specular)
        glMaterialfv(GL_FRONT, GL_SHININESS, self.material_shininess)

        # Draw small spheres instead of points
        for point in self.points:
            glPushMatrix()  # Save the current transformation matrix
            glTranslatef(*point)  # Move to the point's position
            glutSolidSphere(0.05, 32, 32)  # Draw a small sphere (radius=0.1)
            glPopMatrix()  # Restore the transformation matrix

    def draw_grid_xy(self):
        glDisable(GL_LIGHTING)  # Disable lighting for the grid
        glColor3f(0.5, 0.5, 0.5)  # Gray color for the grid

        # Draw horizontal lines (parallel to X-axis)
        for y in range(-10, 11, 1):  # From -10 to 10 with step 1
            glBegin(GL_LINES)
            glVertex3f(-10.0, y, 0.0)
            glVertex3f(10.0, y, 0.0)
            glEnd()

        # Draw vertical lines (parallel to Y-axis)
        for x in range(-10, 11, 1):  # From -10 to 10 with step 1
            glBegin(GL_LINES)
            glVertex3f(x, -10.0, 0.0)
            glVertex3f(x, 10.0, 0.0)
            glEnd()

        glEnable(GL_LIGHTING)  # Re-enable lighting
    
    def draw_grid_xz(self):
        glDisable(GL_LIGHTING)  # Disable lighting for the grid
        glColor3f(0.5, 0.5, 0.5)  # Gray color for the grid

        # Draw horizontal lines (parallel to X-axis)
        for z in range(-10, 11, 1):  # From -10 to 10 with step 1
            glBegin(GL_LINES)
            glVertex3f(-10.0, 0.0, z)
            glVertex3f(10.0, 0.0, z)
            glEnd()

        # Draw vertical lines (parallel to Y-axis)
        for x in range(-10, 11, 1):  # From -10 to 10 with step 1
            glBegin(GL_LINES)
            glVertex3f(x, 0.0, -10.0)
            glVertex3f(x, 0.0, 10.0)
            glEnd()

        glEnable(GL_LIGHTING)  # Re-enable lighting

    def draw_grid_yz(self):
        glDisable(GL_LIGHTING)  # Disable lighting for the grid
        glColor3f(0.5, 0.5, 0.5)  # Gray color for the grid

        # Draw horizontal lines (parallel to X-axis)
        for z in range(-10, 11, 1):  # From -10 to 10 with step 1
            glBegin(GL_LINES)
            glVertex3f(0.0, -10.0, z)
            glVertex3f(0.0, 10.0, z)
            glEnd()

        # Draw vertical lines (parallel to Y-axis)
        for y in range(-10, 11, 1):  # From -10 to 10 with step 1
            glBegin(GL_LINES)
            glVertex3f(0.0, y, -10.0)
            glVertex3f(0.0, y, 10.0)
            glEnd()

        glEnable(GL_LIGHTING)  # Re-enable lighting
    
    def draw_axes(self):
        # Disable lighting for axes
        glDisable(GL_LIGHTING)

        # Draw X-axis (red)
        glColor3f(1.0, 0.0, 0.0)  # Red
        glBegin(GL_LINES)
        glVertex3f(-10.0, 0.0, 0.0)  # Start at -10 on X-axis
        glVertex3f(10.0, 0.0, 0.0)  # End at 10 on X-axis
        glEnd()

        # Draw Y-axis (green)
        glColor3f(0.0, 1.0, 0.0)  # Green
        glBegin(GL_LINES)
        glVertex3f(0.0, -10.0, 0.0)  # Start at -10 on Y-axis
        glVertex3f(0.0, 10.0, 0.0)  # End at 10 on Y-axis
        glEnd()

        # Draw Z-axis (blue)
        glColor3f(0.0, 0.0, 1.0)  # Blue
        glBegin(GL_LINES)
        glVertex3f(0.0, 0.0, -10.0)  # Start at -10 on Z-axis
        glVertex3f(0.0, 0.0, 10.0)  # End at 10 on Z-axis
        glEnd()

        # Re-enable lighting for other objects
        glEnable(GL_LIGHTING)

    def update_points(self, points):
        self.points = points
        self.update()  # Trigger a repaint

    def mousePressEvent(self, event):
        self.last_pos = event.pos()

    def mouseMoveEvent(self, event):
        dx = event.x() - self.last_pos.x()
        dy = event.y() - self.last_pos.y()

        if event.buttons() & Qt.LeftButton:
            self.rotation_x += dy
            self.rotation_y += dx

        self.last_pos = event.pos()
        self.update()  # Trigger a repaint