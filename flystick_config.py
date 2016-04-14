"""
This "demo" configuration is for the most spartanly-named
"Thrustmaster USB Joystick" (http://www.thrustmaster.com/products/usb-joystick).
It was the cheapest joystick in my local electronics shop, and - as an added
bonus - it had just the throttle lever I wanted.
"""
from flystick_conf_models import *

stick = Joystick(0)

ele_trim = Switch(steps=20, source=stick.event(hat=(0, 0)))

# Output (PPM) channels.
CHANNELS = (
    # channel 1: aileron
    stick.axis(0),
    # channel 2: elevator (reversed)
    #-stick.axis(1),
    (-stick.axis(1) + 0.1) * 0.7 + ele_trim * 0.5,
    # channel 3: throttle (reversed)
    -stick.axis(2),
    # channel 4: flight mode; 5 states to match scrollphat vertical resolution
    Switch(steps=5, source=stick.event(hat=(0, 1))),
    # channels 5-8: buttons demo
    stick.button(0),
    stick.button(1),
    stick.button(2),
    stick.button(3),
)

# dual-channel display component
stick_dot = XYDot(center_x=5)

# Render outputs (channels). One-to-one line match to CHANNELS.
DISPLAY = (
    # channel 1: dot horizontal axis
    stick_dot.horizontal(),
    # channel 2: dot vertical axis
    stick_dot.vertical(),
    # channel 3: throttle bar
    YBar(center_x=0, width=2),
    # channel 4: flight mode switch
    YDot(center_x=9),
    # channels 5-8: buttons demo
    Block(corner=(10, 0)),
    Block(corner=(10, 1)),
    Block(corner=(10, 2)),
    Block(corner=(10, 3)),
)

# TODO what's the range? 128? http://www.issi.com/WW/pdf/31FL3730.pdf
DISPLAY_BRIGHTNESS = 10
