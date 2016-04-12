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
import pygame
from RPIO import PWM
import time

try:
    import scrollphat
except (ImportError, IOError) as e:
    logging.warn(e, exc_info=1)
    scrollphat = None


_running = False


def loop(dma_channel, gpio):
    # not that I'm planning on writing to this...
    global _running

    if scrollphat:
        scrollphat.clear()
        scrollphat.set_brightness(DISPLAY_BRIGHTNESS)

    pygame.init()

    # Reading only "clicks" via events. These are used for advanced
    # mappings. Events to avoid tracking state manually.
    # Axes are read by snapshotting.
    pygame.event.set_allowed([pygame.JOYBUTTONDOWN,
                              pygame.JOYHATMOTION])

    PWM.set_loglevel(PWM.LOG_LEVEL_ERRORS)

    # ~10 bit accuracy
    PWM.setup(pulse_incr_us=1)
    PWM.init_channel(channel=dma_channel, subcycle_time_us=20000)

    #import signal
    #signal.signal(signal.SIGCHLD, signal.SIG_IGN)

    _prev = None

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

        output = [ch((clicks, hats)) for ch in CHANNELS]
        #print "Channels: %s" % (output,)

        if output != _prev:
            PWM.add_channel_pulse(dma_channel, gpio, start=0, width=20000)
            pos = 500
            for ch, value in enumerate(output):
                PWM.add_channel_pulse(dma_channel,
                                      gpio,
                                      start=pos,
                                      width=300)
                pos += int(round(1500 + 500 * value))

            if scrollphat:
                scrollphat.clear_buffer()
                for rend, value in zip(DISPLAY, output):
                    rend(value, scrollphat)
                scrollphat.update()

        _prev = output

        # NO BUSYLOOPING. And locking with ``pygame.event.wait`` doesn't sound
        # very sophisticated. (At this point, at least.)
        time.sleep(.02)


if __name__ == '__main__':
    _running = True
    # ended up to channel 5: https://www.raspberrypi.org/forums/viewtopic.php?f=32&t=86339
    loop(dma_channel=5, gpio=18)
