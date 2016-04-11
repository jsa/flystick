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
import flystick_config

import logging
import random
import time

import pygame
from RPIO import PWM

try:
    #import scrollphat
    scrollphat = None
except (ImportError, IOError) as e:
    logging.warn(e, exc_info=1)
    scrollphat = None

running = False


def render():
    if not scrollphat:
        return
    scrollphat.set_pixels(lambda x, y: random.random() > .5, auto_update=True)


def main(dma_channel, gpio):
    # not that I'm planning on writing to this...
    global running

    if scrollphat:
        scrollphat.clear()
        scrollphat.set_brightness(1)
        render()

    pygame.init()

    # Reading only button presses via events, to avoid tracking state
    # manually. Axes are read by snapshotting.
    pygame.event.set_allowed(pygame.JOYBUTTONDOWN)

    PWM.set_loglevel(PWM.LOG_LEVEL_ERRORS)

    # ~10 bit accuracy
    PWM.setup(pulse_incr_us=1)
    # didn't work with under 20ms subcycle (which happens to
    # be quite ok in this case)
    PWM.init_channel(channel=dma_channel,
                     subcycle_time_us=20000)

    #import signal
    #signal.signal(signal.SIGCHLD, signal.SIG_IGN)

    sticks = map(pygame.joystick.Joystick,
                 range(pygame.joystick.get_count()))
    for stick in sticks:
        stick.init()
    print "Found %d joysticks" % len(sticks)

    pulse = 0
    while running:
        for event in pygame.event.get():
            if event.type == pygame.JOYBUTTONDOWN:
                print "JOYBUTTONDOWN", repr(event)

        for stick in sticks:
            state = ["%s (%d)" % (stick.get_name(), stick.get_id())]
            state += ["B%d: %s" % (b, stick.get_button(b))
                      for b in range(stick.get_numbuttons())]
            state += ["A%d: %f" % (a, stick.get_axis(a))
                      for a in range(stick.get_numaxes())]
            state += ["H%d: %r" % (h, stick.get_hat(h))
                      for h in range(stick.get_numhats())]
            print "; ".join(state)

        render()

        def us(x):
            return int(500 + (x + 1) * 500)

        #PWM.add_channel_pulse(dma_channel, gpio, 500, us(stick.get_axis(2)))
        for chan in range(8):
            PWM.add_channel_pulse(dma_channel, gpio, start=500 + chan * 2000, width=500 + pulse)

        # NO BUSYLOOPING. And locking with ``pygame.event.wait`` doesn't sound
        # very sophisticated. (At this point, at least.)
        time.sleep(.1)
        pulse += 50
        pulse %= 1000


if __name__ == '__main__':
    running = True
    # ended up to channel 5: https://www.raspberrypi.org/forums/viewtopic.php?f=32&t=86339
    main(dma_channel=14, gpio=18)
