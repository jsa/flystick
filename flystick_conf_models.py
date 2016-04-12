import pygame.joystick


class Joystick(object):
    def __init__(self, joy_id):
        self._joy = pygame.joystick.Joystick(joy_id)
        self._joy.init()

    def axis(self, axis):
        return lambda clicks: self._joy.get_axis(axis)

    def button(self, button):
        return lambda clicks: 1. if self._joy.get_button(button) else -1.


def HPoint(center):
    x, y = center

    def render(value, scrollphat):
        _x = x + (int(round(value * 5 / 2)))
        scrollphat.set_pixel(_x, y, True)

    return render


def VPoint(center):
    x, y = center

    def render(value, scrollphat):
        _y = y + (int(round(value * 5 / 2)))
        scrollphat.set_pixel(x, _y, True)

    return render


def VBar(x_pos, width=1):
    xs = [x_pos + x for x in range(width)]

    def render(value, scrollphat):
        height = int(round((value + 1) / 2 * 5))
        # could be optimized by using ``scrollphat.set_col``, but
        # would be difficult to read
        for x in xs:
            for y in range(0, height + 1):
                scrollphat.set_pixel(x, y, True)

    return render


def Dot(pos, size=(1, 1)):
    # unpack for readability
    x_pos, y_pos = pos
    x_size, y_size = size
    xs = [x_pos + x for x in range(x_size)]
    ys = [y_pos + y for y in range(y_size)]

    def render(value, scrollphat):
        if value >= 0:
            for x in xs:
                for y in ys:
                    scrollphat.set_pixel(x, y, True)

    return render
