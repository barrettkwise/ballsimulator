# Class for ball object
import random
import turtle


class BallObject:
    bright_colors = ["red", "lime", "blue", "yellow", "cyan", "magenta", "orange", "#826ba8", "pink"]
    dark_colors = ["black", "gray", "brown", "darkgreen", "darkblue", "darkred", "darkcyan", "darkmagenta"]
    pastel_colors = ["#c382b9", "#eae2e0", "#e5c8a5", "#a1d6cc", "#616691", "#a5ad9c", "#d9dad9", "#dde0f8", "#e2f1f0"]
    color_palettes = [bright_colors, dark_colors, pastel_colors]

    def __init__(self, position: turtle.Vec2D, velocity: turtle.Vec2D, diameter: int) -> None:
        self.position = position  # x cord and y cord
        self.speed = velocity[0]  # magnitude
        self.angle = velocity[1]  # direction
        self.diameter = diameter  # diameter of ball
        self.color = random.choice(random.choice(BallObject.color_palettes))  # color of ball
