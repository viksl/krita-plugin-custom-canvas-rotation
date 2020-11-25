# krita-plugin-custom-canvas-rotaion

Author: viksl

Github: https://github.com/viksl

Github for this project: https://github.com/viksl/krita-plugin-custom-canvas-rotaion

Krita version: 4.4.1

Licence:
- See file LICENSE

- GNU GENERAL PUBLIC LICENSE

- Version 3

- <https://www.gnu.org/licenses/>

Copyright: (C) viksl

Release Date: 25.11.2020

Version: 1.1

Default shortcut: Ctrl + Alt + D + (Mouse left/middle button or Pen touch)

## 1/ Description:

  - Free plugin for Krita (<https://krita.org>)
  - Youtube video (<https://youtu.be/tfZ2WgdKL-0>)

  Krita's canvas rotation's gizmo is currently bound to the center, which means
  no matter where on screen your cursor is the gizmo remains in centre.
  This means that to rotate canvas the cursor has to move across the whole screen
  for a full 360° rotation or you have to move the cursor closer to the
  center of the screen to use shorter circular movement for the rotation.

  This plugin introduces a new shortcut and a semi-new function which
  utilizes Krita's original canvas rotation but instead of having 
  window/screen as a centre for the rotation gizmo the cursor's position
  at the moment of shortcut activation is utilized as the gizmo's centre.

  Current active layer gets locked to avoid any accidental strokes during
  the rotation. The layer's original state (lock) is stored and restored
  after the rotation automatically there's no need to manually lock/unlock
  the layer.

  Note:

  Do not misunderstand. This does not rotate the canvas around the
  cursor, canvas rotation in Krita always works around the centre
  of your screen, this plugin on introduces a custom gizmo with the
  rotation.
  With smaller tablets/screens you might have not noticed a need for
  this but with larger screen if you work in on a side of your screen
  and want to rotate the canvas you still have to move the cursor
  around the centre of the screen which means a huge movemvet across
  half or the entire screen, this plugin mitigates this as mentioned
  above.

## 2/ Installation:

    1. Download this plugin from:
        https://github.com/viksl/krita-plugin-custom-canvas-rotaion
        (on the right side there's a green button labeled Code, press it
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

## 3/ How to use:

(Use is the exactly same as Krita's default canvas rotation - custom shortcut + mouse left or middle button click or shortcut + pen touch)

PRESS the shortcut + press left mouse button or middle mouse button or put the pen on the tablet's surface, move the cursor around to rotate the canvas.

## 4/ Adjustments you can make if needed:

  !IMPORTANT!

  Changes you can make manually to this plugin:
  1. Locate the file \_\_init\_\_.py inside c_canvas_rotation directory.
  2. Open in a text editor of your choice.
  3. At the top on lines 60 you will find a constant:
      DISTANCE_BUFFER
  4. Increase/decrease (can't be negative!) DISTANCE_BUFFER (pixels radius)
      to grow/shrink area when the rotation is not responsive until the
      cursor leaves this area for the first time (after that the area
      is disabled and the rotation is allowed everywhere)

## 5/ Known Issues
- A red crossed circle might appear while rotating the canvas (or may hang around after)
    Solution:   This it not a problem but a feature. This tells you the layer is locked
                so you know you can't draw on it. Krita doesn't do update when the lock
                is released but only when you move the cursor so the icon can sometimes
                hang around if you don't move the cursor at all.
                Again this is not an issues but Krita's built-in functionality
- If the plugin is enabled correctly (meaning after restartin Krita if you go to
    the settings, the plugins name can't be greyed out) it might in some rare
    cases look like it's not working (not responding), this means that your machines
    performance is probably just slow or got stuck by something. If restart of your machine
    doesn't help you can simply increase TIMER_INTERVAL (check the section 5/ above) a bit
    to reduce performance drain.
- During canvas rotation if the cursor stays too long over icons in GUI Krita gives focus to
    these icons which loses the focus from the custom canvas rotation event.
    Solution:   Don't leave the cursor hanging for too long over icons. But
                It should be jsut a marginal problem since rotating canvas doesn't require
                use of GUI and rotation usually only happens when over canvas so hopefully
                not much of an issue, just noting it here just in case.

## 6/ Possible future updates

- Perhaps an icon to idicate the centre for rotation gizmo (cursor)
- Utilize buffer area for canas rotation reset
- Cursor icon maybe

## 7/ Thanks to

wojtryb (<https://krita-artists.org/u/wojtryb>)

EyeOdin (<https://krita-artists.org/u/EyeOdin>)

For helping me better understand pyqt and python