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

import time

import pygame
from RPIO import PWM

try:
    import scrollphat
except ImportError:
    scrollphat = None

running = False


def render():
    if not scrollphat:
        return


def main(dma_channel):
    # not that I'm planning on writing to this...
    global running

    pygame.init()

    # Reading only button presses via events, to avoid tracking state
    # manually. Axes are read by snapshotting.
    pygame.event.set_allowed(pygame.JOYBUTTONDOWN)

    # ~10 bit accuracy
    PWM.setup(pulse_incr_us=1)
    PWM.init_channel(channel=dma_channel)

    while running:
        for event in pygame.event.get():
            if event.type == pygame.JOYBUTTONDOWN:
                TODO

        render()

        # NO BUSYLOOPING. And locking with ``pygame.event.wait`` doesn't sound
        # very sophisticated (at this point, at least).
        time.sleep(.01)


if __name__ == '__main__':
    running = True
    main(dma_channel=0)
