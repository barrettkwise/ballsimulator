# Class for ball object
import random
from vector import Vector2D
from math import pi, pow


class BallObject:
    colors = ["red", "lime", "blue", "yellow", "cyan", "magenta", "#826ba8", "pink"]
    materials = {"red": 1.2,
                 "lime": 1.3,
                 "blue": 1.5,
                 "yellow": 1.1,
                 "cyan": 1.4,
                 "magenta": 2,
                 "orange": 1,
                 "#826ba8": 1.7,
                 "pink": 1.8
                 }

    def __init__(self, position: tuple[float, float], velocity: Vector2D,
                 diameter: int, quadrant: int, color: str or None) -> None:
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