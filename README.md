# krita-plugin-custom-canvas-rotaion
Author: viksl
Github: https://github.com/viksl
Github for this project: https://github.com/viksl/krita-plugin-custom-canvas-rotaion
Licence:  See file LICENSE
          GNU GENERAL PUBLIC LICENSE
          Version 3
          <https://www.gnu.org/licenses/>
Copyright: (C) viksl
Date: 25.11.2020
Version: 1.0
Default shortcut: Ctrl + Alt + D
##Description:
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

##Installation:
    1. Download this plugin from:
        https://github.com/viksl/krita-plugin-custom-canvas-rotaion
        (on the right side there's a green button label Code, press it
        then click on Download ZIP)
    2. Open the zip file
    3. Locate directory c_canvas_rotation and c_canvas_rotation.desktop
        file inside krita-plugin-custom-canvas-rotaion-main directory
    4. Copy the file and the directory to pykrita directory located
        through: Open Krita, go to:
        Settings
            - Manage Resources...
                - Press the button Open Resource Folder
                (there you can find the pykrita directory)
    5. Restart Krita
    6. Enable the plugin
        Settings
            - Configure Krita ...
                - Python Plugin Manager
                (Locate name Custom Canvas Rotation and tick it to enable)
                Press OK
    7. Restart Krita
    8. Setup your shortcut
        Settings
            - Configure Krita ...
                - Keyboard Shortcuts
                (Locate action: Scripts - Custom Canvas Rotation)
                Change the shortcut to whatever you like
                (default is Ctrl + Alt + D)

##How to use:
    PRESS and HOLD the shortcut, move the cursor around to rotate the canvas.

##Adjustments you can make if needed:
  !IMPORTANT!
  Changes you can make manually to this plugin:
  1. Locate the file __init__.py inside c_canvas_rotation directory.
  2. Open in a text editor of your choice.
  3. At the top on lines 74 and 81 you will find constants:
      DISTANCE_BUFFER and TIMER_INTERVAL
  4. Increase/decrease (can't be negative!) DISTANCE_BUFFER (pixels radius)
      to grow/shrink area when the rotation is not responsive until the
      cursor leaves this area for the first time (after that the area
      is disabled and the rotation is allowed everywhere)
  5.  Increase/decrease (can't be negative!) TIMER_INTERVAL (milliseconds)
      to increase/decrease how quickly you can rotate the canvas again
      minimum value is set to 50 milliseconds (ms) which works just fine for
      my system but you might need to increase it.
      Don't go to low with this as if the timer gets shorter then a tick of
      Krita's event loop the rotation won't work (you won't experiecen any
      error as the code works just fine but the window for rotation would
      be soo short that it ends before you can move your cursor)
      50 ms = 0.050 s which is a very short time so you won't notice any
      possible "lag", even increasing to 100 ms (= 0.100 s) you will be just
      fine, feel free to adjust to anything that works for you.
      I suggest to keep it at 50 ms if the rotation works since increasing it
      can eventually lead to intrusive lag-like experience (for example
      if you set the value to 1000 ms = 1 s which means you will have to wait
      for 1 whole second until you can rotate again which I believe doesn't
      really make sense for anyone but I'm leaving this note here just in case)

