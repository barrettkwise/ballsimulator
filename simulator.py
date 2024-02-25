import math
import random
import time as Timer
import os

from ball import BallObject
from vector import Vector2D
from view import Window
from file_handler import save_to_file as save
from file_handler import load_from_file as load


class Simulator:
    """A class to simulate the movement of balls in a window."""

    @staticmethod
    def __closest_ball(pos: tuple[float, float], gen_balls: list[BallObject], search_dist: float) \
            -> BallObject or None:
        """
        Finds the closest ball to a given position.
        :param pos: tuple[float, float]
        :param gen_balls: list[BallObject]
        :param search_dist: int
        :return: BallObject or None
        """
        if not isinstance(pos, tuple):
            raise TypeError("pos parameter must be a tuple.")
        if not isinstance(gen_balls, list):
            raise TypeError("gen_balls parameter must be a list.")
        if not isinstance(search_dist, (int, float)):
            raise TypeError("search_dist parameter must be an int or float.")

        nearby_balls = []
        # only add balls if they are within the search distance
        # gen balls = list of currently generated balls
        for b in gen_balls:
            if b.position == pos:
                continue
            # rough_dist = distance between the centers of the two balls
            rough_dist = math.sqrt((math.pow((b.position[0] - pos[0]), 2) +
                                    math.pow((b.position[1] - pos[1]), 2)))
            # only do further check on balls with a center to center distance
            # less than or equal to the search distance
            if rough_dist <= search_dist:
                points = {
                    "top": [(b.position[0], b.position[1] + b.radius), False],
                    "bottom": [(b.position[0], b.position[1] - b.radius), False],
                    "left": [(b.position[0] - b.radius, b.position[1]), False],
                    "right": [(b.position[0] + b.radius, b.position[1]), False]
                }
                distances = []
                for point in points.keys():
                    cords = points[point][0]
                    dist = math.sqrt(math.pow(cords[0] - pos[0], 2) +
                                     math.pow(cords[1] - pos[1], 2))
                    if dist <= search_dist:
                        points[point][1] = True
                        distances.append(dist)
                    else:
                        break

                # if all points are within the search distance, add the ball
                if all([point[1] for point in points.values()]):
                    nearby_balls.append((b, min(distances)))

        len_nearby_balls = len(nearby_balls)
        if len_nearby_balls == 1:
            nearest_ball = nearby_balls[0][0]
            return nearest_ball

        elif len_nearby_balls > 1:
            nearby_balls.sort(key=lambda x: x[1])
            nearest_ball = nearby_balls[0][0]
            return nearest_ball

        else:
            return None

    @staticmethod
    def __detect_collision(ball1_position: tuple[float, float], ball1_radius: float,
                           ball2: tuple[float, float], ball2_radius: float) -> bool:
        """
        Detects if two balls have collided.
        :param ball1_position: tuple[float, float]
        :param ball1_radius: int
        :param ball2: tuple[float, float]
        :param ball2_radius: int
        :return: bool
        """
        if not isinstance(ball1_position, tuple):
            raise TypeError("ball1_position parameter must be a tuple.")
        if not isinstance(ball1_radius, (int, float)):
            raise TypeError("ball1_radius parameter must be an int or float.")
        if not isinstance(ball2, tuple):
            raise TypeError("ball2 parameter must be a tuple.")
        if not isinstance(ball2_radius, (int, float)):
            raise TypeError("ball2_radius parameter must be an int or float.")

        # Calculate the distance between the two balls
        distance = math.sqrt((math.pow((ball2[0] - ball1_position[0]), 2) +
                              math.pow((ball2[1] - ball1_position[1]), 2)))

        # Calculate the sum of the two balls' radii
        radii_sum = ball1_radius + ball2_radius
        # Check if the distance is less than the sum of the radii
        return distance < radii_sum

    @staticmethod
    def __ball_to_ball_physics(ball1: BallObject, ball2: BallObject) -> Vector2D:
        """
        Determines the new velocity of a ball after a collision with another ball.
        :param ball1: BallObject
        :param ball2: BallObject
        :return: Vector2D
        """
        if not isinstance(ball1, BallObject):
            raise TypeError("ball1 parameter must be a BallObject.")
        if not isinstance(ball2, BallObject):
            raise TypeError("ball2 parameter must be a BallObject.")

        def compute_velocity(v1: Vector2D, v2: Vector2D, m1: float,
                             m2: float, x1: float, x2: float) -> Vector2D: return v1 - (2 * m2 / (m1 + m2)) \
            * (((v1 - v2) * (x1 - x2)) / math.pow(x1 - x2, 2)) * (x1 - x2)

        return compute_velocity(ball1.velocity, ball2.velocity, ball1.mass, ball2.mass,
                                ball1.position[0], ball2.position[0])

    @staticmethod
    def __get_quadrant(position: tuple[float, float] or None, ball: BallObject or None) \
            -> int or BallObject:
        """
        Find which quadrant the ball is in. If ball parameter is supplied, will update
        ball.quadrant attribute. If ball parameter is None, will return the quadrant as an int.
        :param position: tuple[float, float]
        :param ball: BallObject
        :return: int or BallObject
        """
        if not isinstance(position, tuple) and position is not None:
            raise TypeError("position parameter must be a tuple or None.")
        if not isinstance(ball, BallObject) and ball is not None:
            raise TypeError("ball parameter must be a BallObject or None.")

        if position is not None:
            if position[0] > 0:
                if position[1] > 0:
                    return 0
                else:
                    return 3
            else:
                if position[1] > 0:
                    return 1
                else:
                    return 2

        else:
            if ball.position[0] > 0:
                if ball.position[1] > 0:
                    ball.quadrant = 0
                    return ball
                else:
                    ball.quadrant = 3
                    return ball
            else:
                if ball.position[1] > 0:
                    ball.quadrant = 1
                    return ball
                else:
                    ball.quadrant = 2
                    return ball

    def __init__(self,
                 window_size: tuple[int, int],
                 num_of_balls: int = random.randint(2, 100),
                 load_from_file: bool = False,
                 save_to_file: bool = False,
                 time_step: float = 0.05,
                 drawing_accuracy: int = 0,
                 length_of_simulation: float or None = None,
                 debug: bool = False,
                 ) -> None:
        """
        Initializes a Simulator object.
        drawing_accuracy is the number of decimal places to round to when drawing the balls.
        :param window_size: tuple[int, int]
        :param num_of_balls: int
        :param time_step: float
        :param drawing_accuracy: int
        :param length_of_simulation: float or None
        :param debug: bool
        """
        self.window = Window(window_size[0], window_size[1], drawing_accuracy)
        self.num_of_balls = num_of_balls
        self.balls = ([], [], [], [])
        self.time = 0.0
        self.time_step = time_step
        self.search_dist = max(self.window.width, self.window.height) / 2
        self.length_of_simulation = length_of_simulation
        self.pid = os.getpid()
        self.load_from_file = load_from_file
        self.save_to_file = save_to_file
        self.debug = debug

    def start(self) -> None:
        """
        Starts the simulation.
        :return: None
        """
        self.window.draw_border()
        if self.load_from_file:
            self.balls = load("balls.pkl")
            if self.debug:
                print("Loaded balls from file.")
        else:
            self.__generate_balls()
            if self.save_to_file:
                save(self.balls, "balls.pkl")
            if self.debug:
                print("Ball generation complete.\nStarting simulation.")

        while True:
            if self.length_of_simulation is not None:
                if Timer.process_time() >= self.length_of_simulation:
                    os.kill(self.pid, 9)

            self.window.draw_border()
            self.window.draw_axis()
            self.__draw_all_balls()
            self.window.screen.update()
            self.__move_balls()
            self.window.turtle.clear()
            self.time += self.time_step
            if self.save_to_file:
                # save the state of the balls to a file
                save(self.balls, "balls.pkl")

    def __move_balls(self) -> None:
        """
        Determines the new position of each ball.
        :return: None
        """
        # tuple of lists representing the quadrants of the window
        # each list contains the balls in that quadrant
        new_balls = ([], [], [], [])

        # list of tuples representing pairs of
        # balls that have collided
        collision_balls = []

        for quadrant in self.balls:
            if len(quadrant) == 0:
                continue
            if len(quadrant) == 1:
                ball1_new_vel = self.__wall_collision(quadrant[0])
                ball1_new_x = quadrant[0].position[0] + \
                    (ball1_new_vel.x * self.time_step)
                ball1_new_y = quadrant[0].position[1] + \
                    (ball1_new_vel.y * self.time_step)
                new_pos = (ball1_new_x, ball1_new_y)
                new_quadrant = Simulator.__get_quadrant(new_pos, None)
                new_ball = BallObject(new_pos, ball1_new_vel, quadrant[0].diameter,
                                      new_quadrant, quadrant[0].color)
                new_balls[new_quadrant].append(new_ball)
                continue

            for ball in quadrant:
                if len(quadrant) == 2:
                    closest_ball = quadrant[1] if ball is quadrant[0] else quadrant[0]

                else:
                    closest_ball = Simulator.__closest_ball(
                        ball.position, quadrant, self.search_dist)

                if closest_ball is None:
                    ball1_new_vel = self.__wall_collision(ball)
                    ball1_new_x = ball.position[0] + \
                        (ball1_new_vel.x * self.time_step)
                    ball1_new_y = ball.position[1] + \
                        (ball1_new_vel.y * self.time_step)
                    new_pos = (ball1_new_x, ball1_new_y)
                    new_quadrant = Simulator.__get_quadrant(new_pos, None)
                    new_ball = BallObject(new_pos, ball1_new_vel, ball.diameter,
                                          new_quadrant, ball.color)
                    new_balls[new_quadrant].append(new_ball)
                    continue

                if closest_ball is not None:
                    if self.debug:
                        print(f"Closest ball to {ball} is {closest_ball}.")

                    if self.__detect_collision(ball.position, ball.radius,
                                               closest_ball.position, closest_ball.radius):
                        if self.debug:
                            print(f"Collision detected between {
                                  ball} and {closest_ball}.")
                        # Add the pair of balls to list of collided balls
                        collision_balls.append((ball, closest_ball))
                        continue

                    ball1_new_vel = self.__wall_collision(ball)
                    ball1_new_x = ball.position[0] + \
                        (ball1_new_vel.x * self.time_step)
                    ball1_new_y = ball.position[1] + \
                        (ball1_new_vel.y * self.time_step)
                    new_pos = (ball1_new_x, ball1_new_y)
                    new_quadrant = Simulator.__get_quadrant(new_pos, None)
                    new_ball = BallObject(
                        new_pos, ball1_new_vel, ball.diameter, new_quadrant, ball.color)
                    new_balls[new_quadrant].append(new_ball)

        if len(collision_balls) > 0:
            for pair in collision_balls:
                reversed_pair = tuple(reversed(pair))
                if reversed_pair in collision_balls:
                    collision_balls.remove(reversed_pair)

                ball1 = pair[0]
                ball2 = pair[1]

                ball1_new_vel = Simulator.__ball_to_ball_physics(ball1, ball2)
                ball2_new_vel = Simulator.__ball_to_ball_physics(ball2, ball1)

                ball1_new_x = ball1.position[0] + \
                    (ball1_new_vel.x * self.time_step)
                ball1_new_y = ball1.position[1] + \
                    (ball1_new_vel.y * self.time_step)

                ball2_new_x = ball2.position[0] + \
                    (ball2_new_vel.x * self.time_step)
                ball2_new_y = ball2.position[1] + \
                    (ball2_new_vel.y * self.time_step)

                new_pos1 = (ball1_new_x, ball1_new_y)
                new_pos2 = (ball2_new_x, ball2_new_y)

                new_quadrant1 = Simulator.__get_quadrant(new_pos1, None)
                new_balls[new_quadrant1].append(BallObject(new_pos1, ball1_new_vel, ball1.diameter,
                                                           new_quadrant1, ball1.color))

                new_quadrant2 = Simulator.__get_quadrant(new_pos2, None)
                new_balls[new_quadrant2].append(BallObject(new_pos2, ball2_new_vel, ball2.diameter,
                                                           new_quadrant2, ball2.color))

        if self.debug:
            print("Ball movement complete.")
            print(f"Number of balls: {
                  sum(len(quadrant) for quadrant in self.balls)}")
            print(f"Number of expected balls: {self.num_of_balls}")
        del self.balls
        self.balls = new_balls

    def __generate_balls(self) -> None:
        """
        Generates the balls upon starting the simulation.
        :return: None
        """

        def generate_position(d: int) -> tuple[float, float]:
            return random.uniform(-self.window.width + d / 2, self.window.width - d / 2), \
                random.uniform(-self.window.height + d / 2,
                               self.window.height - d / 2)

        for ball_count in range(self.num_of_balls):
            # Generate a random position within the window
            # such that ball is always drawn in window
            # and is not overlapping any other balls
            position_found = False
            position = None
            quadrant = None
            diameter = None
            while not position_found:
                diameter = random.randint(10, 15)
                temp_position = generate_position(diameter)
                temp_quadrant = Simulator.__get_quadrant(temp_position, None)
                if ball_count == 0:
                    if self.debug:
                        print("First ball position generated.")
                    position = temp_position
                    quadrant = temp_quadrant
                    position_found = True

                elif ball_count > 0:
                    closest_ball = Simulator.__closest_ball(temp_position,
                                                            [ball for quadrant in self.balls for ball in quadrant],
                                                            self.search_dist)

                    if closest_ball is None:
                        if self.debug:
                            print(
                                "No nearby balls detected, ball position generated.")
                        position = temp_position
                        quadrant = temp_quadrant
                        position_found = True

                    elif closest_ball is not None:
                        if self.debug:
                            print(f"Closest ball: {closest_ball}.")

                        if Simulator.__detect_collision(ball1_position=temp_position,
                                                        ball1_radius=diameter / 2,
                                                        ball2=closest_ball.position,
                                                        ball2_radius=closest_ball.radius):
                            if self.debug:
                                print(
                                    "Ball collision detected, generating new position.")
                            continue

                        else:
                            if self.debug:
                                print(
                                    "No ball collision detected, ball position generated.")
                            position = temp_position
                            quadrant = temp_quadrant
                            position_found = True

            # Generate a random x speed and y speed
            speed_x = random.uniform(-20, 20)
            speed_y = random.uniform(-20, 20)
            velocity = Vector2D(speed_x, speed_y)

            # Create a new ball object with the random position, velocity, diameter, and color
            new_ball = BallObject(position, velocity, diameter,
                                  quadrant, color=None)

            # Add the new ball to its quadrant list
            self.balls[quadrant].append(new_ball)

    def __wall_collision(self, b: BallObject) -> Vector2D:
        """
        Determines the new velocity of a ball after a collision with a wall.
        :param b:
        :return: Vector2D
        """
        if not isinstance(b, BallObject):
            raise TypeError("b parameter must be a BallObject.")

        x = b.position[0]
        y = b.position[1]
        new_speed_x = b.velocity.x
        new_speed_y = b.velocity.y

        if x + b.radius >= self.window.width or x - b.radius <= -self.window.width:
            new_speed_x *= -1

        if y + b.radius >= self.window.height or y - b.radius <= -self.window.height:
            new_speed_y *= -1

        return Vector2D(new_speed_x, new_speed_y)

    def __draw_all_balls(self) -> None:
        """
        Draws all balls in the window.
        :return: None
        """
        for b in [ball for quadrant in self.balls for ball in quadrant]:
            self.window.draw_ball(b.position, b.diameter, b.color)
