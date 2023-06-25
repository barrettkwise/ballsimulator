import random
import turtle


# Class for handling interactions between
# turtle window and simulator.py

class Window:
    colors = ["red", "blue", "yellow", "purple", "orange", "pink", "brown"]

    def __init__(self, width: int, height: int, random_colors: bool) -> None:
        self.turtle = turtle.Turtle()
        self.screen = turtle.Screen()
        self.width = width
        self.height = height
        self.random_colors = random_colors
        self.__setup_window()

    def __setup_window(self):
        self.screen.screensize(self.width, self.height)
        self.turtle.hideturtle()
        self.turtle.speed("fastest")

    def draw_ball(self, position: tuple[float, float], ball_diameter: int) -> None:
        # Move the turtle to the specified position
        self.turtle.penup()
        self.turtle.goto(position)
        self.turtle.pendown()

        # Draw the ball
        self.turtle.begin_fill()
        if self.random_colors:
            self.turtle.dot(ball_diameter, random.choice(self.colors))
        else:
            self.turtle.dot(ball_diameter, "black")
        self.turtle.end_fill()
