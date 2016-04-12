from flystick_conf_models import *

stick = Joystick(0)

# Output (PPM) channels.
CHANNELS = (
    stick.axis(0), # channel 1
    Neg(stick.axis(1)), # channel 2
    Neg(stick.axis(2)), # channel 3
    stick.button(0), # channel 4
    stick.button(1), # channel 5
)

cross = Crosshair(center=(5, 2))

# Render outputs (channels). One-to-one line match to CHANNELS.
DISPLAY = (
    # channel 1: cross-hair horizontal line
    cross.horizontal(),
    # channel 2: cross-hair vertical line
    cross.vertical(),
    # channel 3: throttle bar
    VBar(x_pos=0, width=2),
    # channel 4: button square blinky
    Dot(pos=(9, 0), size=(2, 2)),
    # channel 5: button square blinky
    Dot(pos=(9, 3), size=(2, 2)),
)

# TODO what's the range? 128? http://www.issi.com/WW/pdf/31FL3730.pdf
DISPLAY_BRIGHTNESS = 10
