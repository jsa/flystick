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
from flystick_config import *

import logging
import pigpio
import pygame
import threading
import time

try:
    import scrollphat
except (ImportError, IOError) as e:
    logging.warn(e, exc_info=True)
    scrollphat = None


_running = False

_current_output = []


def render():
    while _running:
        scrollphat.clear_buffer()
        # ``_current_output`` access should be thread-safe; should be
        # de-referenced only once
        for rend, value in zip(DISPLAY, _current_output):
            rend(value, scrollphat)
        scrollphat.update()
        time.sleep(.05)


def main(dma_channel, gpio):
    global _current_output

    if scrollphat:
        scrollphat.clear()
        scrollphat.set_brightness(DISPLAY_BRIGHTNESS)
        th = threading.Thread(target=render)
        th.daemon = True
        th.start()

    pygame.init()

    # Reading only "clicks" via events. These are used for advanced
    # mappings. Events to avoid tracking state manually.
    # Axes are read by snapshotting.
    pygame.event.set_allowed([pygame.JOYBUTTONDOWN,
                              pygame.JOYHATMOTION])

    pi = pigpio.pi()
    pi.set_mode(gpio, pigpio.OUTPUT)

    #import signal
    #signal.signal(signal.SIGCHLD, signal.SIG_IGN)

    pi_gpio = 1 << gpio

    pi.wave_add_generic([pigpio.pulse(pi_gpio, 0, 2000)])
    # padding to make deleting logic easier
    waves = [None, None, pi.wave_create()]
    pi.wave_send_repeat(waves[0])

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

        _current_output = [ch((clicks, hats)) for ch in CHANNELS]
        #print "Channels: %s" % (output,)

        if _current_output != prev:
            pulses, pos = [], 0
            for value in _current_output:
                us = int(round(1500 + 500 * value))
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

        prev = _current_output

        # NO BUSYLOOPING. And locking with ``pygame.event.wait`` doesn't sound
        # very sophisticated. (At this point, at least.)
        time.sleep(.02)


if __name__ == '__main__':
    _running = True
    # DMA channel: https://www.raspberrypi.org/forums/viewtopic.php?f=32&t=86339
    main(dma_channel=5, gpio=18)
