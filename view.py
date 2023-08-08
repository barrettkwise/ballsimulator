import turtle


# Class for handling interactions between
# turtle window and simulator.py

class Window:

    def __init__(self, width: int, height: int, drawing_accuracy: int) -> None:
        self.turtle = turtle.Turtle()
        self.screen = turtle.Screen()
        self.width = width
        self.height = height
        self.drawing_accuracy = drawing_accuracy
        self.__setup_window()

    def __setup_window(self) -> None:
        self.screen.title("Ball Simulator")
        self.screen.screensize(self.width, self.height)
        self.turtle.radians()
        self.screen.tracer(0, 0)
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
        if self.drawing_accuracy != 0:
            position = (round(position[0], self.drawing_accuracy), round(position[1], self.drawing_accuracy))
        # Move the turtle to the specified position
        self.turtle.penup()
        self.turtle.goto(position)
        self.turtle.pendown()

        # Draw the ball
        self.turtle.begin_fill()
        self.turtle.dot(ball_diameter, color)
        self.turtle.end_fill()

