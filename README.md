# flystick

A python script for Raspberry Pi that reads a USB joystick
(with [pygame](http://www.pygame.org/)) and outputs a PPM signal to
RC transmitter (with [pigpio](http://abyz.co.uk/rpi/pigpio/python.html)).

For the mandatory blinky-blinky, supports VERY FANCY (or so) visualizations
for [Scroll pHAT](https://github.com/pimoroni/scroll-phat).

The input/output-mapping and visualization are
[highly configurable](flystick_config.py).

## Installation

1. `sudo apt-get install python-pygame git`

2. http://abyz.co.uk/rpi/pigpio/download.html

3. from https://github.com/pimoroni/scroll-phat:

   `curl -sS https://get.pimoroni.com/scrollphat | bash`

4. `git clone https://github.com/jsa/flystick.git`

## Running

Append to [`/etc/rc.local`](https://www.raspberrypi.org/documentation/linux/usage/rc-local.md)
BEFORE THE LINE `exit 0`:

```
pigpiod

cd ~pi/flystick
python flystick.py &
cd -
```

See also the [`jscal`](http://linux.die.net/man/1/jscal) linux utility to
calibrate joystick. (Also the related `jstest`, `jscal-store`, and
`jscal-restore`.)
