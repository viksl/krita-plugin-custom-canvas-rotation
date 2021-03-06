"""
Author: viksl
Github: https://github.com/viksl
Github for this project: 
Licence:  See file LICENSE
          GNU GENERAL PUBLIC LICENSE
          Version 3
          <https://www.gnu.org/licenses/>
Date: 25.11.2020
Version: 1.1
Krita version: 4.4.1
Default shortcut: Ctrl + Alt + D + (Mouse left/middle button or Pen touch)
Description:
  - Free plugin for Krita <https://krita.org) -
  Krita's canvas rotation is currently bound to the center, which means
  no matter where on screen your cursor is the angle is always calculated
  towards the screen/window centre. This means that to rotate cans the
  cursor has to move across the whole screen for a full 360° rotation
  or you have to move the cursor closer to the center of the screen
  to use shorter circular movement for the rotation.
  This plugin introduces a new shortcut and a semi-new function which
  utilizes Krita's original canvas rotation but instead of having 
  window/screen as a centre for the rotation gizmo the cursor's position
  at the moment of shortcut activation is utilized as the gizmo's centre.

  Current active layer gets locked to avoid any accidental strokes during
  the rotation. The layer's original state (lock) is stored and restored
  after the rotation automatically there's no need to manually lock/unlock
  the layer.

  Note: Do not misunderstand. This does not rotate the canvas around the
        cursor, canvas rotation in Krita always works around the centre
        of your screen, this plugin on introduces a custom gizmo with the
        rotation.
        With smaller tablets/screens you might have not noticed a need for
        this but with larger screen if you work in on a side of your screen
        and want to rotate the canvas you still have to move the cursor
        around the centre of the screen which means a huge movemvet across
        half or the entire screen, this plugin mitigates this as mentioned
        above.

  !IMPORTANT!
  Changes you can make manually to this plugin:
  1. Locate the file __init__.py inside c_canvas_rotation directory.
  2. Open in a text editor of your choice.
  3. At the top on lines 60 you will find a constant:
      DISTANCE_BUFFER
  4. Increase/decrease (can't be negative!) DISTANCE_BUFFER (pixels radius)
      to grow/shrink area when the rotation is not responsive until the
      cursor leaves this area for the first time (after that the area
      is disabled and the rotation is allowed everywhere)

Copyright: (C) viksl
"""

from krita import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
import math

DISTANCE_BUFFER = 10                                  # THIS VALUE CAN BE CHANGED TO FIT YOUR NEEDS!
                                                      # Units: Pixels (screen not canvas pixels)
                                                      # Warning: Cannot be negative!
                                                      # How far (in pixels) you need to move your cursor for rotation to take effect (only initially).
                                                      # It makes the transition from not changin rotation to changing it a bit smoother (around 0 <- initial poin)
                                                      # In future it might also serve as a reset for canvas reset to facilitate another function related to
                                                      # canvas rotation.

current_active_layer = None
current_active_layer_locked_original = False
angle = 0                                             # Current canvas rotation
buffer_lock = False                                   # After cursor moves out of buffer area removes the buffer condition
init_offset_angle = 0                                 # An angle to keep smooth transition
                                                      # (vectors: v1 = base_vector - init; v2 = cursor (immediately after leaving buffer area) - init)
cursor_init_position = None                           # Cursor position when custom rotation invokation begins
base_vector = [1, 0]                                  # Unit vector as reference to measure angle from
shortcut_pressed = False
mouse_button_pressed = False
circleIcon = None

class RotationCentreIcon(QWidget):
  def __init__(self, position, width, height, parent=None):
    QWidget.__init__(self, parent)

    self.position = position
    self.width = int(width)
    self.height = int(height)
    self.setGeometry(int(position.x() - self.width / 2), int(position.y() - self.height / 2), self.width, self.height)
    self.setWindowFlags(self.windowFlags() | QtCore.Qt.Window | QtCore.Qt.FramelessWindowHint)
    self.setAttribute(QtCore.Qt.WA_TranslucentBackground)
    self.setStyleSheet("background: transparent;")
    self.setWindowTitle("icon")

  def showAt(self, position):
    self.move(position.x() - self.width / 2, position.y() - self.height / 2)
    self.show()

  def paintEvent(self, event):
    self.painter = QPainter(self)
    self.painter.setRenderHints( QPainter.HighQualityAntialiasing )
    self.painter.setPen( QPen(QColor(255, 255, 255, 150), 1) )
    self.painter.setBrush( QColor(47, 47, 47, 150) )
    self.painter.drawEllipse(0, 0, self.width, self.height)
    self.painter.end()

# Class for testing (replaces a print statement as I don't know how to print on win)
class Dialog(QDialog):
  def __init__(self, text, parent=None):
      super(Dialog, self).__init__(parent)
      self.setLayout(QVBoxLayout())
      self.label = QLabel(str(text))
      self.layout().addWidget(self.label)
      self.resize(200, 50)
      self.exec_()

def dot_product(v1, v2):
  return v1[0] * v2[0] + v1[1] * v2[1]

def determinant(v1, v2):
  return v1[0] * v2[1] - v1[1] * v2[0]

def vector_angle(v1, v2):
  return  math.degrees( math.atan2(determinant(v1, v2), dot_product(v1, v2)) )

def two_point_distance(v1, v2):
  return math.sqrt( math.pow(( v2.x() - v1.x() ), 2) + math.pow(( v2.y() - v1.y() ), 2)  )


def init_rotation():
  global current_active_layer
  global current_active_layer_locked_original
  global angle
  global buffer_lock
  global init_offset_angle
  global cursor_init_position
  global base_vector
  global circleIcon

  canvas = Krita.instance().activeWindow().activeView().canvas()
  cursor_init_position = QCursor.pos()
  angle = canvas.rotation()
  circleIcon.showAt(cursor_init_position)

def lock_active_layer():
    global current_active_layer
    global current_active_layer_locked_original

    current_active_layer = Krita.instance().activeDocument().activeNode()

    current_active_layer_locked_original = current_active_layer.locked()
    current_active_layer.setLocked(True)

def unlock_active_layer():
    global current_active_layer
    global current_active_layer_locked_original

    if current_active_layer != None:
      current_active_layer.setLocked(current_active_layer_locked_original)

    current_active_layer = None

def stop_rotation():
  global angle
  global buffer_lock
  global init_offset_angle
  global cursor_init_position
  global base_vector
  global shortcut_pressed
  global circleIcon

  shortcut_pressed = False
  cursor_init_position = None
  buffer_lock = False
  init_offset_angle = 0
  angle = 0
  circleIcon.hide()

  unlock_active_layer()

# Reset everything back to default state to be ready for next rotation event
def rotate():
  global angle
  global buffer_lock
  global init_offset_angle
  global cursor_init_position
  global base_vector

  if not buffer_lock:
    # Distance from initial point (cursor position trigger event was onvoked from)
    # to cursor's current position
    distance = two_point_distance(cursor_init_position, QCursor.pos())
    
    # If cursor outside buffer zone start immediately calculate initial offset angle
    # to ensure smooth transition when changing angles in followint passes
    if distance > DISTANCE_BUFFER:
      buffer_lock = True

      v1 = [base_vector[0] - cursor_init_position.x(), base_vector[1] - cursor_init_position.y()]
      v2 = [QCursor.pos().x() - cursor_init_position.x(), QCursor.pos().y() - cursor_init_position.y()]
      
      init_offset_angle = vector_angle(v1, v2)
  elif buffer_lock:
    # This handles the canvas rotation itself
    v1 = [base_vector[0] - cursor_init_position.x(), base_vector[1] - cursor_init_position.y()]
    v2 = [QCursor.pos().x() - cursor_init_position.x(), QCursor.pos().y() - cursor_init_position.y()]
    
    canvas = Krita.instance().activeWindow().activeView().canvas()
    canvas.setRotation(angle - init_offset_angle + vector_angle(v1, v2))

# Main event loop is here
class mdiAreaFilter(QMdiArea):
  def __init__(self, parent=None):
    super().__init__(parent)

  def eventFilter(self, obj, e):
    global mouse_button_pressed
    global shortcut_pressed

    """
      Get through only if shortcut hasn't been pressed yet and after that mouse button hasn't been
      After shortcut is pressed, only the mouse button press is a deciding factor to get through or not
      (this way you can release shortcut keys while only moving mosue around the same way
      as default canvas rotation works)
      In other cases just return False, no need to care about events not related to this code
    """
    if (
      not mouse_button_pressed and not shortcut_pressed
    ):
      return False

    """
      Use left mouse button or middle mouse button
      Initiate rotation vars
    """
    if (
      not mouse_button_pressed and
      e.type() == QEvent.MouseButtonPress and 
      (e.button() == QtCore.Qt.LeftButton or e.button() == QtCore.Qt.MidButton)
    ):
      mouse_button_pressed = True
      init_rotation()

    """
      Treat key release properly, now only mouse button press which is now True is the
      driving force.
      Set active layer's lock back to original state (since mouse left/middle button
      hasn't been pressed yet)
    """
    if e.type() == QEvent.KeyRelease and not e.isAutoRepeat() and not mouse_button_pressed:
      shortcut_pressed = False
      unlock_active_layer()
      return False

    if not mouse_button_pressed:
      return False

    """
      Left/Middle mouse button release
      Stop rotation
    """
    if (
      e.type() == QEvent.MouseButtonRelease and
      (e.button() == QtCore.Qt.LeftButton or  e.button() == QtCore.Qt.MidButton)
    ):
      mouse_button_pressed = False
      stop_rotation()
      return False
    
    """
      Main driving force for this event loop
    """
    if e.type() == QEvent.MouseMove:
      rotate()

    return False

class CustomCanvasRotationExtension(Extension):
  def __init__(self,parent):
    super(CustomCanvasRotationExtension, self).__init__(parent)

  def setup(self):
    pass

  def rotation_trigger(self):
    global shortcut_pressed

    shortcut_pressed = True
    lock_active_layer()

  def createActions(self, window):
    global circleIcon

    self.c_canvas_rotation = window.createAction("c_canvas_rotation", "Custom Canvas Rotation")
    self.c_canvas_rotation.triggered.connect(self.rotation_trigger)
    self.c_canvas_rotation.setAutoRepeat(False)
    if circleIcon is None:
      circleIcon = RotationCentreIcon(QPoint(0, 0), DISTANCE_BUFFER, DISTANCE_BUFFER, window.qwindow())
    self.MAFilter = mdiAreaFilter()
    self.MAFilter.setMouseTracking(True)


Krita.instance().addExtension(CustomCanvasRotationExtension(Krita.instance()))