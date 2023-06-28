# Class for ball object
import random
from turtle import Vec2D
from math import pi, pow


class BallObject:
    colors = ["red", "lime", "blue", "yellow", "cyan", "magenta", "orange", "#826ba8", "pink"]
    materials = {"red": 1.0,
                 "lime": 2.0,
                 "blue": 0.7,
                 "yellow": 0.4,
                 "cyan": 0.8,
                 "magenta": 5.0,
                 "orange": 0.5,
                 "#826ba8": 0.3,
                 "pink": 0.75
                 }

    def __init__(self, position: Vec2D, velocity: Vec2D, diameter: int) -> None:
        self.position = position  # x cord and y cord
        self.speed = velocity[0]  # magnitude
        self.angle = velocity[1]  # direction
        self.diameter = diameter  # diameter of ball
        self.radius = diameter / 2  # radius of ball
        self.surface_area = pi * pow(self.radius, 2)  # surface area of ball
        self.color = random.choice(BallObject.colors)  # color of ball
        self.mass = BallObject.materials[self.color] * self.surface_area  # mass of ball
