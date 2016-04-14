# flystick

A python script for Raspberry Pi that reads a USB joystick
(with [pygame](http://www.pygame.org/)) and outputs a PPM signal to RC transmitter
(with [pigpio](http://abyz.co.uk/rpi/pigpio/python.html)).

For the mandatory blinky-blinky, supports VERY FANCY (or so) visualizations
using [Scroll pHAT](https://github.com/pimoroni/scroll-phat).

The input/output-mapping and visualization are [highly configurable](flystick_conf.py).

## Installation

1. `sudo apt-get install python-pygame`

2. pigpio: http://abyz.co.uk/rpi/pigpio/download.html

3. from https://github.com/pimoroni/scroll-phat/blob/master/README.md:

   `curl -sS https://get.pimoroni.com/scrollphat | bash`

See also the `jscal` linux utility to calibrate joystick. (`man jscal`;
also `jstest`, `jscal-store`, and `jscal-restore`.)
