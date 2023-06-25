# Class for ball object

class BallObject:
    def __init__(self, position: tuple[float, float], velocity: tuple[float, float], diameter: int) -> None:
        self.position = position  # x cord and y cord
        self.velocity = velocity  # magnitude and direction
        self.diameter = diameter  # diameter of ball
