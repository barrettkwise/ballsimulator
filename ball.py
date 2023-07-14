# Class for ball object
import random
from vector import Vector2D
from math import pi, pow


class BallObject:
    colors = ["red", "lime", "blue", "yellow", "cyan", "magenta", "#826ba8", "pink"]
    materials = {"red": 1,
                 "lime": 1,
                 "blue": 1,
                 "yellow": 1,
                 "cyan": 1,
                 "magenta": 1,
                 "orange": 1,
                 "#826ba8": 1,
                 "pink": 1
                 }

    def __init__(self, position: tuple[float, float], velocity: Vector2D, diameter: int, color: str) -> None:
        self.position = position  # x cord and y cord
        self.velocity = velocity  # velocity vector
        self.speed_x = self.velocity.x  # x component of velocity
        self.speed_y = self.velocity.y  # y component of velocity
        self.diameter = diameter  # diameter of ball
        self.radius = diameter / 2  # radius of ball
        self.surface_area = pi * pow(self.radius, 2)  # surface area of ball
        if color is not "init":
            self.color = color
        else:
            self.color = random.choice(BallObject.colors)  # color of ball
        self.mass = BallObject.materials[self.color] * self.surface_area  # mass of ball
