import pygame.joystick


class Joystick(object):
    def __init__(self, joy_id):
        pygame.joystick.init()
        self._joy = pygame.joystick.Joystick(joy_id)
        self._joy.init()

    def axis(self, axis):
        return lambda clicks: self._joy.get_axis(axis)

    def button(self, button):
        return lambda clicks: 1. if self._joy.get_button(button) else -1.


def Neg(ch):
    return lambda clicks: -ch(clicks)



class Corsshair(object):
    def __init__(self, center):
        self.center_x, self.center_y = center
        self.x = self.y = 0

    def maybe_render(self, scrollphat):
        if not (self.x is None or self.y is None):
            scrollphat.set_pixel(self.x, 4 - self.y, True)
            self.x = self.y = None

    def horizontal(self):
        def render(value, scrollphat):
            self.x = self.center_x + int(round(value * 2))
            self.maybe_render(scrollphat)
        return render

    def vertical(self):
        def render(value, scrollphat):
            self.y = self.center_y + int(round(value * 2))
            self.maybe_render(scrollphat)
        return render


def HPoint(center):
    x, y = center

    def render(value, scrollphat):
        _x = x + int(round(value * 2))
        scrollphat.set_pixel(_x, 4 - y, True)

    return render


def VPoint(center):
    x, y = center

    def render(value, scrollphat):
        _y = y + int(round(value * 2))
        scrollphat.set_pixel(x, 4 - _y, True)

    return render


def VBar(x_pos, width=1):
    xs = [x_pos + x for x in range(width)]

    def render(value, scrollphat):
        height = int(round((value + 1) / 2 * 5))
        # could be optimized by using ``scrollphat.set_col``, but
        # would be difficult to read
        for x in xs:
            for y in range(0, height):
                scrollphat.set_pixel(x, 4 - y, True)

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
