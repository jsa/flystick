"""
flystick - python script to control an RC plane with a USB joystick.
Copyright (C) 2016 Janne Savukoski

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""
from flystick_config import CHANNELS, DISPLAY, DISPLAY_BRIGHTNESS

import logging
import pygame
import signal
import threading
import time

try:
    import pigpio
except ImportError as e:
    logging.warn(e, exc_info=True)
    logging.warn("Failed to load pigpio library, running in debug mode")
    pigpio = None

try:
    import scrollphat
except (ImportError, IOError) as e:
    logging.warn(e, exc_info=True)
    logging.warn("Failed to load Scroll pHAT library, you'll be missing all the fancy graphics")
    scrollphat = None


_running = False

_output = ()


def render():
    # LED check
    scrollphat.clear_buffer()
    for col in range(0, 13):
        if col > 1:
            scrollphat.set_col(col - 2, 0)
        if col < 11:
            scrollphat.set_col(col, 0b11111)
        scrollphat.update()
        time.sleep(.1)

    time.sleep(.3)

    while _running:
        scrollphat.clear_buffer()
        # ``_output`` access should be thread-safe; de-referenced just once
        for rend, value in zip(DISPLAY, _output):
            try:
                rend(value, scrollphat)
            except ValueError as e:
                logging.warn(e, exc_info=True)
        scrollphat.update()
        time.sleep(.05)


def shutdown(signum, frame):
    global _running
    _running = False


def main(gpio):
    global _output

    pygame.init()

    # Reading only "clicks" via events. These are used for advanced
    # mappings. Events to avoid tracking state manually. Axes are read
    # by snapshotting.
    pygame.event.set_allowed([pygame.JOYBUTTONDOWN,
                              pygame.JOYHATMOTION])

    pi_gpio = 1 << gpio

    if pigpio:
        pi = pigpio.pi()
        pi.set_mode(gpio, pigpio.OUTPUT)
        pi.wave_add_generic([pigpio.pulse(pi_gpio, 0, 2000)])
        # padding to make deleting logic easier
        waves = [None, None, pi.wave_create()]
        pi.wave_send_repeat(waves[-1])
    else:
        pi = None

    if scrollphat:
        scrollphat.clear()
        scrollphat.set_brightness(DISPLAY_BRIGHTNESS)
        # fork to avoid crash in case of I2C connection issues
        th = threading.Thread(target=render)
        th.daemon = True
        th.start()

    prev = None

    while _running:
        # clicks for advanced mapping
        clicks, hats = [], []
        for evt in pygame.event.get():
            if evt.type == pygame.JOYBUTTONDOWN:
                #print "JOYBUTTONDOWN: %r\n%s" % (evt, dir(evt))
                clicks.append(evt)
            elif evt.type == pygame.JOYHATMOTION and any(evt.value):
                #print "JOYHATMOTION: %r\n%s" % (evt, dir(evt))
                hats.append(evt)

        # tuple to enforce immutability
        _output = tuple(max(min(ch((clicks, hats)), 1.), -1.)
                        for ch in CHANNELS)

        if _output == prev:
            # do nothing
            pass

        elif pigpio:
            pulses, pos = [], 0
            for value in _output:
                # calibrated with Taranis to [-99.6..0..99.4]
                us = int(round(1333 + 453 * value))
                pulses += [pigpio.pulse(0, pi_gpio, 300),
                           pigpio.pulse(pi_gpio, 0, us - 300)]
                pos += us

            pulses += [pigpio.pulse(0, pi_gpio, 300),
                       pigpio.pulse(pi_gpio, 0, 20000 - 300 - pos - 1)]

            pi.wave_add_generic(pulses)
            waves.append(pi.wave_create())
            pi.wave_send_using_mode(waves[-1], pigpio.WAVE_MODE_REPEAT_SYNC)

            last, waves = waves[0], waves[1:]
            if last:
                pi.wave_delete(last)

        else:
            # debugging
            print str(_output)

        prev = _output

        # NO BUSYLOOPING. And locking with ``pygame.event.wait`` doesn't sound
        # very sophisticated. (At this point, at least.)
        time.sleep(.02)

    if scrollphat:
        scrollphat.clear()
    if pi:
        pi.stop()


if __name__ == '__main__':
    _running = True
    signal.signal(signal.SIGCHLD, signal.SIG_IGN)
    signal.signal(signal.SIGTERM, shutdown)
    signal.signal(signal.SIGINT, shutdown)
    main(gpio=18)
