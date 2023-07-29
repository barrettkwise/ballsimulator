# Class for ball object
import random
from vector import Vector2D
from math import pi, pow


class BallObject:
    materials = {"red": 2,
                 "lime": 3,
                 "blue": 0.5,
                 "yellow": 1,
                 "cyan": 4,
                 "magenta": 0.25,
                 "orange": 5,
                 "#826ba8": 5.5,
                 "pink": 6
                 }

    @classmethod
    def add_material(cls, color: str, weight: float) -> None:
        cls.materials[color] = weight

    def __init__(self, position: tuple[float, float], velocity: Vector2D, diameter: int, color: str) -> None:
        self.position = position  # x cord and y cord
        self.velocity = velocity  # velocity vector
        self.diameter = diameter  # diameter of ball
        self.radius = diameter / 2  # radius of ball
        self.surface_area = pi * pow(self.radius, 2)  # surface area of ball
        if color is not "init":
            self.color = color
        else:
            self.color = random.choice(list(BallObject.materials.keys()))  # color of ball
        self.mass = BallObject.materials[self.color] * self.surface_area  # mass of ball

    def __getstate__(self) -> tuple[tuple[float, float], Vector2D, int, str]:
        return {
            'position': self.position,
            'velocity': self.velocity,
            'diameter': self.diameter,
            'radius': self.radius,
            'color': self.color,
            'surface_area': self.surface_area,
            'mass': self.mass
        }

    def __setstate__(self, state):
        self.position = state['position']
        self.velocity = state['velocity']
        self.diameter = state['diameter']
        self.radius = state['radius']
        self.color = state['color']
        self.surface_area = state['surface_area']
        self.mass = state['mass']
