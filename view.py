import turtle


class Window:
    """Window class for handling interactions between the turtle window and the simulator."""

    def __init__(self, width: int, height: int, drawing_accuracy: int) -> None:
        if not all(isinstance(i, int) for i in (width, height, drawing_accuracy)):
            raise TypeError("Width, height, and drawing accuracy must be integers")

        self.turtle = turtle.Turtle()
        self.screen = turtle.Screen()
        self.width = width
        self.height = height
        self.drawing_accuracy = drawing_accuracy
        self.__setup_window()

    def __setup_window(self) -> None:
        """
        Set up the window for the simulator.
        return: None
        """
        self.screen.title("Ball Simulator")
        self.screen.screensize(self.width, self.height)
        self.screen.tracer(0)
        self.turtle.speed(0)
        self.turtle.hideturtle()

    def draw_border(self) -> None:
        """
        Draw a border around the window.
        return: None
        """
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

    def draw_axis(self) -> None:
        """
        Draw the x and y axes.
        return: None
        """
        self.turtle.penup()
        self.turtle.goto(0, self.height)
        self.turtle.pendown()
        self.turtle.goto(0, -self.height)
        self.turtle.penup()
        self.turtle.goto(-self.width, 0)
        self.turtle.pendown()
        self.turtle.goto(self.width, 0)
        self.turtle.penup()
        self.turtle.goto(0, 0)
        self.turtle.pendown()

    def draw_ball(
        self, position: tuple[float, float], ball_diameter: int, color: str
    ) -> None:
        """
        Draw a ball at the specified position with the specified diameter and color.
        param: position: tuple of floats
        param: ball_diameter: int
        param: color: str
        return: None
        """
        if not all(isinstance(i, (float, int)) for i in position):
            raise TypeError("Position must be a tuple of floats")
        if not isinstance(ball_diameter, int):
            raise TypeError("Ball diameter must be an integer")
        if not isinstance(color, str):
            raise TypeError("Color must be a string")

        if self.drawing_accuracy != 0:
            position = (
                round(position[0], self.drawing_accuracy),
                round(position[1], self.drawing_accuracy),
            )
        # Move the turtle to the specified position
        self.turtle.penup()
        self.turtle.goto(position)
        self.turtle.pendown()

        # Draw the ball
        self.turtle.begin_fill()
        self.turtle.dot(ball_diameter, color)
        self.turtle.end_fill()
