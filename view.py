import turtle


# Class for handling interactions between
# turtle window and simulator.py

class Window:

    def __init__(self, width: int, height: int) -> None:
        self.turtle = turtle.Turtle()
        self.screen = turtle.Screen()
        self.width = width
        self.height = height
        self.__setup_window()

    def __setup_window(self) -> None:
        self.screen.title("Ball Simulator")
        self.screen.screensize(self.width, self.height)
        self.screen.tracer(0)
        self.turtle.speed("fastest")
        self.turtle.hideturtle()

    def draw_border(self) -> None:
        self.turtle.penup()
        self.turtle.goto(self.width, self.height)
        self.turtle.pendown()
        self.turtle.goto(self.width, -self.height)
        self.turtle.goto(-self.width, -self.height)
        self.turtle.goto(-self.width, self.height)
        self.turtle.goto(self.width, self.height)
        self.turtle.penup()
        self.turtle.goto(0, 0)
        self.turtle.pendown()

    def draw_ball(self, position: tuple[float, float], ball_diameter: int, color: str) -> None:
        # Move the turtle to the specified position
        self.turtle.penup()
        self.turtle.goto(position)
        self.turtle.pendown()

        # Draw the ball
        self.turtle.begin_fill()
        self.turtle.dot(ball_diameter, color)
        self.turtle.end_fill()

