# Author: viksl
# Github: https://github.com/viksl
# Github for this project: 
# Licence: 
# Date: 24.11.2020
# Version 1.0

from krita import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import QTimer
import math

DISTANCE_BUFFER = 10          # THIS VALUE CAN BE CHANGED TO FIT YOUR NEEDS!
                              # Units: Pixels
                              # How far (in pixels) you need to move your cursor for rotation to take effect (only initially).
                              # It makes the transition from not changin rotation to changing it a bit smoother (around 0 <- initial poin)
                              # In future it might also serve as a reset for canvas reset to facilitate another function related to
                              # canvas rotation.

TIMER_INTERVAL = 50           # THIS VALUE CAN BE CHANGED TO FIT YOUR NEEDS!
                              # Units: Miliseconds
                              # For me 50ms works as minimum value just fine.
                              # (you can go higher, if you need a lot more than this
                              # there might be other problems interfering with your program), anything below
                              # may cause the plugin seem unreactive (timer ends sooned than Krita can actually deal with the methods)

def dot_product(v1, v2):
  return v1[0] * v2[0] + v1[1] * v2[1]

def determinant(v1, v2):
  return v1[0] * v2[1] - v1[1] * v2[0]

def vector_angle(v1, v2):
  return  math.degrees( math.atan2(determinant(v1, v2), dot_product(v1, v2)) )

def two_point_distance(v1, v2):
  return math.sqrt( math.pow(( v2.x() - v1.x() ), 2) + math.pow(( v2.y() - v1.y() ), 2)  )

# Class for testing (replaces a print statement as I don't know how to print on win)
class Dialog(QDialog):
    def __init__(self, text, text2, parent=None):
        super(Dialog, self).__init__(parent)
        self.setLayout(QVBoxLayout())
        self.label = QLabel(str(text))
        self.label2 = QLabel(str(text2))
        self.layout().addWidget(self.label)
        self.layout().addWidget(self.label2)
        self.resize(200, 50)
        self.exec_()

class CustomCanvasRotationExtension(Extension):
  def __init__(self,parent):
    self.current_active_layer = None
    self.current_active_layer_locked_original = False
    self.angle = 0                                            # Current canvas rotation
    self.buffer_lock = False                                  # After cursor moves out of buffer area removes the buffer condition
    self.key_press_lock = False                               # Locks initial key press (sets initial values for trigger event only at the
                                                              # beginning of the event, these values are reset in the timeout method of the timer below)
    self.timer_interval = TIMER_INTERVAL
    self.init_offset_angle = 0                                # An angle to keep smooth transition
                                                              # (vectors: v1 = base_vector - init; v2 = cursor (immediately after leaving buffer area) - init)
    self.cursor_init_position = None                          # Cursor position when custom rotation invokation begins
    self.base_vector = [1, 0]                                 # Unit vector as reference to measure angle from
    self.timer = QTimer()                                     # Handles reset to init state
    self.timer.setInterval(self.timer_interval)
    self.timer.timeout.connect(self.rotate_timer_timeout)
    super(CustomCanvasRotationExtension, self).__init__(parent)

  # Reset everything back to default state to be ready for next rotation event
  def rotate_timer_timeout(self):
    self.key_press_lock = False
    self.cursor_init_position = None
    self.buffer_lock = False
    self.init_offset_angle = 0
    self.angle = 0
    self.current_active_layer.setLocked(self.current_active_layer_locked_original)
    self.current_active_layer = None
    self.timer.stop()
  def setup(self):
    pass

  def createActions(self, window):
    self.c_canvas_rotation = window.createAction("c_canvas_rotation", "Custom Canvas Rotation", "tools/scripts")
    self.c_canvas_rotation.setAutoRepeat(True)

    @self.c_canvas_rotation.triggered.connect
    def on_trigger():
      canvas = Krita.instance().activeWindow().activeView().canvas()

      # Init custom rotation (vars, timer, active layer reference)
      if not self.key_press_lock:
        self.key_press_lock = True
        self.cursor_init_position = QCursor.pos()
        self.angle = canvas.rotation()
        self.current_active_layer = Krita.instance().activeDocument().activeNode()
        self.current_active_layer_locked_original = self.current_active_layer.locked()
        self.current_active_layer.setLocked(True)
      else:
        if not self.buffer_lock:
          # Distance from initial point (cursor position trigger event was onvoked from)
          # to cursor's current position
          distance = two_point_distance(self.cursor_init_position, QCursor.pos())
          
          # If cursor outside buffer zone start immediately calculate initial offset angle
          # to ensure smooth transition when changing angles in followint passes
          if distance > DISTANCE_BUFFER:
            self.buffer_lock = True

            v1 = [self.base_vector[0] - self.cursor_init_position.x(), self.base_vector[1] - self.cursor_init_position.y()]
            v2 = [QCursor.pos().x() - self.cursor_init_position.x(), QCursor.pos().y() - self.cursor_init_position.y()]
            
            self.init_offset_angle = vector_angle(v1, v2)
        elif self.buffer_lock:
          # This handles the canvas rotation itself
          v1 = [self.base_vector[0] - self.cursor_init_position.x(), self.base_vector[1] - self.cursor_init_position.y()]
          v2 = [QCursor.pos().x() - self.cursor_init_position.x(), QCursor.pos().y() - self.cursor_init_position.y()]
          
          canvas.setRotation(self.angle - self.init_offset_angle + vector_angle(v1, v2))

          # Start timer if it's active which means it stops the timer (without triggering
          # timeout event) and starts again. Timer will keep running as long as the
          # shortcut is being pressed
          self.timer.start()

Krita.instance().addExtension(CustomCanvasRotationExtension(Krita.instance()))