import turtle


# Class for handling interactions between
# turtle window and simulator.py

class Window:
    # List of color palettes to choose from

    def __init__(self, width: int, height: int) -> None:
        self.turtle = turtle.Turtle()
        self.screen = turtle.Screen()
        self.width = width
        self.height = height
        self.__setup_window()

    def __setup_window(self) -> None:
        self.screen.title("Ball Simulator")
        self.screen.screensize(self.width, self.height)
        self.turtle.radians()
        self.screen.tracer(False)
        self.turtle.speed("fastest")
        self.turtle.hideturtle()

    def draw_ball(self, position: tuple[float, float], ball_diameter: int, color: str) -> None:
        # Move the turtle to the specified position
        position = (round(position[0], 2), round(position[1], 2))
        self.turtle.penup()
        self.turtle.goto(position)
        self.turtle.pendown()

        # Draw the ball
        self.turtle.begin_fill()
        self.turtle.dot(ball_diameter, color)
        self.turtle.end_fill()

