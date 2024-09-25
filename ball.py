import random
from math import pi

from vector import Vector2D


class BallObject:
    """
    A class to represent a ball object.
    """

    colors = ["red", "lime", "blue", "yellow", "cyan", "magenta", "#826ba8", "pink"]
    materials = {
        "red": 1.2,
        "lime": 1.3,
        "blue": 1.5,
        "yellow": 1.1,
        "cyan": 1.4,
        "magenta": 2,
        "orange": 1,
        "#826ba8": 1.7,
        "pink": 1.8,
    }

    def __init__(
        self,
        position: tuple[float, float],
        velocity: Vector2D,
        diameter: int,
        quadrant: int,
        color: str | None,
    ) -> None:
        """
        Create a new ball object with the specified position, velocity, diameter, quadrant, and color.
        :param: position: tuple of floats
        :param: velocity: Vector2D
        :param: diameter: int
        :param: quadrant: int
        :param: color: str
        :return: None
        """
        if not all(isinstance(i, (float, int)) for i in position):
            raise TypeError("Position must be a tuple of floats")
        if not isinstance(velocity, Vector2D):
            raise TypeError("Velocity must be a Vector2D object")
        if not isinstance(diameter, int):
            raise TypeError("Diameter must be an integer")
        if not isinstance(quadrant, int):
            raise TypeError("Quadrant must be an integer")
        if color is not None and not isinstance(color, str):
            raise TypeError("Color must be a string")

        self.position = position  # x cord and y cord
        self.velocity = velocity  # velocity vector
        self.speed_x = self.velocity.x  # x component of velocity
        self.speed_y = self.velocity.y  # y component of velocity
        self.diameter = diameter  # diameter of ball
        self.radius = diameter / 2  # radius of ball
        self.surface_area = pi * pow(self.radius, 2)  # surface area of ball
        self.quadrant = quadrant  # quadrant of ball
        if color is not None:
            self.color = color
        else:
            self.color = random.choice(BallObject.colors)  # color of ball
        self.mass = BallObject.materials[self.color] * self.surface_area  # mass of ball
