from dataclasses import dataclass
from typing import Callable

from PIL import Image


@dataclass
class Viewport:
    image: Image.Image
    center: complex  # point of interest
    zoom: float

    @property
    def aspect_ratio(self):
        return  self.image.width / self.image.height

    def center_point(self, point: complex) -> complex:
        return point + self.center - complex(self.image.width / 2, self.image.height / 2)

    def scale_point(self, point: complex) -> complex:
        return self.move_to_zero_and_apply_transformation(point, lambda c: complex(c.real / self.image.width,
                                                                                   c.imag / self.image.height))

    def invert_y_axis(self, point: complex) -> complex:
        return self.move_to_zero_and_apply_transformation(point, lambda c: c.conjugate())

    def account_for_aspect_ratio(self, point: complex) -> complex:
        # we leave the y axis the same and scale out the x axis, this will make things more visible initially
        return self.move_to_zero_and_apply_transformation(point, lambda c: complex(c.real * self.aspect_ratio, c.imag))
    def account_for_zoom(self, point: complex) -> complex:
        return self.move_to_zero_and_apply_transformation(point, lambda c: c / self.zoom)

    def pixel_to_point(self, x, y):
        raw_point = complex(x, y)
        return self.account_for_zoom(
            self.account_for_aspect_ratio(self.invert_y_axis(self.scale_point(self.center_point(raw_point)))))

    def move_to_zero_and_apply_transformation(self, point: complex, transformation: Callable) -> complex:
        zero_centered_point = point - self.center
        transformed_point = transformation(zero_centered_point)
        recentered_point = transformed_point + self.center
        return recentered_point

    def __iter__(self):
        """
        description:
            Allows the viewport to be iterated over, starting from the first row, going through each horizontal pixel
            one by one

        :returns a pixel
        """
        for y in range(self.image.height):
            for x in range(self.image.width):
                yield Pixel(self, x, y)

    def __len__(self):
        return self.image.width * self.image.height

@dataclass
class Pixel:
    viewport: Viewport
    x: int
    y: int

    @property
    def color(self):
        return self.viewport.image.getpixel((self.x, self.y))

    @color.setter
    def color(self, value):
        self.viewport.image.putpixel((self.x, self.y), value)

    def __complex__(self):
        return self.viewport.pixel_to_point(self.x, self.y)
