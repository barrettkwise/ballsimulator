import turtle


class Window:
    """
    Window class for handling interactions between the turtle window and the simulator.
    """

    def __init__(self, width: int, height: int, drawing_accuracy: int) -> None:
        """
        Create a new window with the specified width, height, and drawing accuracy.
        :param: width: int
        :param: height: int
        :param: drawing_accuracy: int
        :return: None
        """
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
        :return: None
        """
        self.screen.title("Ball Simulator")
        self.screen.screensize(self.width, self.height)
        self.screen.tracer(0)
        self.turtle.speed(0)
        self.turtle.hideturtle()

    def draw_border(self) -> None:
        """
        Draw a border around the window.
        :return: None
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
        :return: None
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

    def sim_info(
        self, step: int, iteration_time: float, num_of_balls: int, memory_usage: int
    ) -> None:
        """
        Display infomation about the simulation.
        :param: step: int
        :param: iteration_time: float
        :param: num_of_balls: int
        :param: memory_usage: int
        :return: None
        """
        if not isinstance(step, int):
            raise TypeError("Step must be an integer")
        if not isinstance(iteration_time, float):
            raise TypeError("Iteration time must be a float")
        if not isinstance(num_of_balls, int):
            raise TypeError("Number of balls must be an integer")

        self.turtle.penup()
        # put the step count in the top left corner
        self.turtle.goto(-self.width + 10, self.height - 20)
        self.turtle.write(f"Step: {step}", font=("Arial", 12, "normal"))
        # put the iteration time below the step count
        self.turtle.goto(-self.width + 10, self.height - 40)
        self.turtle.write(
            f"Iteration Time: {round(iteration_time, 2)} ms",
            font=("Arial", 12, "normal"),
        )
        # put the number of balls below the iteration time
        # also put the amount of memory used by the balls
        self.turtle.goto(-self.width + 10, self.height - 60)
        self.turtle.write(
            f"Number of Balls: {num_of_balls}", font=("Arial", 12, "normal")
        )
        self.turtle.goto(-self.width + 10, self.height - 80)
        self.turtle.write(
            f"Memory Usage: {memory_usage} bytes", font=("Arial", 12, "normal")
        )

    def draw_ball(
        self, position: tuple[float, float], ball_diameter: int, color: str
    ) -> None:
        """
        Draw a ball at the specified position with the specified diameter and color.
        :param: position: tuple of floats
        :param: ball_diameter: int
        :param: color: str
        :return: None
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
