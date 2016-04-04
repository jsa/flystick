# flystick

A python script for Raspberry Pi that reads a USB joystick ([pygame](http://www.pygame.org/)) and outputs PPM signal to RC transmitter ([RPIO.PWM](https://pythonhosted.org/RPIO/pwm_py.html)).

For the mandatory blinky-blinky, supports VERY FANCY (or so) visualizations using [Scroll pHAT](https://github.com/pimoroni/scroll-phat).

## Installation

```
sudo apt-get install python-setuptools python-pygame
sudo easy_install -U RPIO
# from https://github.com/pimoroni/scroll-phat/blob/master/README.md:
curl -sS https://get.pimoroni.com/scrollphat | bash
```
