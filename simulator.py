import math
import random
import types
from functools import partial
from multiprocessing import Pool, cpu_count
from operator import gt, lt

from ball import BallObject
from vector import Vector2D
from view import Window


def detect_collision(ball1_position: tuple[float, float],
                     ball1_diameter: int, ball2: BallObject) -> bool:
    print(ball2)
    # Calculate the distance between the two balls
    distance = math.sqrt((math.pow((ball2.position[0] - ball1_position[0]), 2) +
                          math.pow((ball2.position[1] - ball1_position[1]), 2)))

    # Calculate the sum of the two balls' radii
    radii_sum = (ball1_diameter / 2) + ball2.radius

    # Check if the distance is less than the sum of the radii
    if distance < radii_sum:
        return True
    else:
        return False


def is_nearby(pos: tuple[float, float], search_dist: int, gen_ball: BallObject) \
        -> tuple[float, float] or None:
    print(gen_ball.position)
    # only add balls if they are within the search distance
    # gen balls = list of currently generated balls
    if gen_ball.position == pos:
        return
    top = (gen_ball.position[0], gen_ball.position[1] + gen_ball.radius)
    bottom = (gen_ball.position[0], gen_ball.position[1] - gen_ball.radius)
    left = (gen_ball.position[0] - gen_ball.radius, gen_ball.position[1])
    right = (gen_ball.position[0] + gen_ball.radius, gen_ball.position[1])
    points = [top, bottom, left, right]
    in_range = True
    for point in points:
        dist = math.sqrt((math.pow((point[0] - pos[0]), 2) + math.pow((point[1] - pos[1]), 2)))
        if dist > search_dist:
            in_range = False
            break

    if in_range:
        return gen_ball


class Simulator:

    @staticmethod
    def __function_parallelizer(func: types.FunctionType, iterable: list, bound_parameters: list) -> list:
        partial_func = partial(func, *bound_parameters)
        c_size = int(len(iterable) / cpu_count())
        with Pool(processes=cpu_count()) as p:
            result = p.map(partial_func, iterable, chunksize=c_size)

        return [item for item in result if item is not None]

    @staticmethod
    def __ball_to_ball_physics_handler(ball1: BallObject, ball2: BallObject) -> \
            tuple[Vector2D, Vector2D]:
        def compute_velocity(v1: Vector2D, v2: Vector2D, m1: float, m2: float, x1: float, x2: float) \
                -> Vector2D:
            return v1 - (2 * m2 / (m1 + m2)) * ((v1 - v2) * (x1 - x2) / math.pow(abs(x1 - x2), 2)) * (x1 - x2)

        ball1_response_v = compute_velocity(ball1.velocity, ball2.velocity, ball1.mass, ball2.mass,
                                            ball1.position[0], ball2.position[0])
        ball2_response_v = compute_velocity(ball2.velocity, ball1.velocity, ball2.mass, ball1.mass,
                                            ball2.position[0], ball1.position[0])

        return ball1_response_v, ball2_response_v

    def __init__(self,
                 window_size: tuple[int, int],
                 num_of_balls: int = random.randint(2, 100),
                 time_step: float = 0.001,
                 debug: bool = False,
                 ) -> None:
        self.window = Window(window_size[0], window_size[1])
        self.num_of_balls = num_of_balls
        self.time = 0.0
        self.time_step = time_step
        self.debug = debug
        self.balls = []

    def start(self) -> None:
        self.__generate_balls()
        if self.debug:
            print("Ball generation complete. \nStarting simulation.")
        while True:
            self.window.draw_border()
            self.__draw_all_balls()
            self.window.screen.update()
            self.__move_balls()
            self.window.screen.update()
            self.window.turtle.clear()
            self.time += self.time_step

    def __move_balls(self) -> None:
        new_balls = []
        num_of_balls = len(self.balls)
        for ball1 in range(num_of_balls):
            nearby_balls = Simulator.__function_parallelizer(is_nearby,
                                                             iterable=self.balls,
                                                             bound_parameters=[self.balls[ball1].position, 45])
            num_of_nearby_balls = len(nearby_balls)

            if num_of_nearby_balls == 0:
                ball1_new_vel = self.__wall_collision(self.balls[ball1])
                ball1_new_x = self.balls[ball1].position[0] + (ball1_new_vel.x * self.time_step)
                ball1_new_y = self.balls[ball1].position[1] + (ball1_new_vel.y * self.time_step)
                new_pos = (ball1_new_x, ball1_new_y)
                new_balls.append(BallObject(new_pos, ball1_new_vel, self.balls[ball1].diameter,
                                            self.balls[ball1].color))
                continue

            elif num_of_nearby_balls > 0:
                if self.debug:
                    print("Ball", ball1, "has", len(nearby_balls), "nearby balls.")
                vel_vectors = []
                for ball2 in nearby_balls:
                    # Check if ball1 and ball2 have collided
                    if Simulator.__function_parallelizer(detect_collision,
                                                         iterable=nearby_balls,
                                                         bound_parameters=[self.balls[ball1].position,
                                                                           self.balls[ball1].diameter]):
                        if self.debug:
                            print(f"Collision detected between {self.balls[ball1]} and {ball2}.")
                        # Calculate new velocities
                        ball1_new_vel, ball2_new_vel = Simulator.__ball_to_ball_physics_handler(self.balls[ball1],
                                                                                                ball2)
                        vel_vectors.append(ball1_new_vel)

                if len(vel_vectors) == 0:
                    ball1_new_vel = self.__wall_collision(self.balls[ball1])
                    ball1_new_x = self.balls[ball1].position[0] + (ball1_new_vel.x * self.time_step)
                    ball1_new_y = self.balls[ball1].position[1] + (ball1_new_vel.y * self.time_step)
                    new_pos = (ball1_new_x, ball1_new_y)
                    new_balls.append(BallObject(new_pos, ball1_new_vel, self.balls[ball1].diameter,
                                                self.balls[ball1].color))

                else:
                    avg_vel = Vector2D(sum([v.x for v in vel_vectors]) / len(vel_vectors),
                                       sum([v.y for v in vel_vectors]) / len(vel_vectors))

                    new_pos = (self.balls[ball1].position[0] + (avg_vel.x * self.time_step),
                               self.balls[ball1].position[1] + (avg_vel.y * self.time_step))

                    new_balls.append(
                        BallObject(new_pos, avg_vel, self.balls[ball1].diameter, self.balls[ball1].color))

        if self.debug:
            print("Ball movement complete.")
        self.balls.clear()
        self.balls = new_balls

    def __generate_balls(self) -> None:

        def generate_position(d: float, x: float = None) -> tuple[float, float]:
            def sign(s):
                return -1 if s < 0 else 1

            # Check if valid x has been found
            # to prevent needless recursion
            if x is None:
                temp_x = random.uniform(-self.window.width, self.window.width)
                if sign(temp_x) == -1:
                    op = gt
                else:
                    op = lt
                if op(temp_x + (sign(temp_x) * d), sign(temp_x) * self.window.width):
                    x = temp_x
                else:
                    return generate_position(d, None)

            # Generate valid y value, reusing
            # the x value found above
            temp_y = random.uniform(-self.window.height, self.window.height)
            if sign(temp_y) == -1:
                op = gt
            else:
                op = lt
            if op(temp_y + (sign(temp_y) * d), sign(temp_y) * self.window.height):
                y = temp_y
            else:
                return generate_position(d, x)
            return x, y

        for ball_count in range(self.num_of_balls):
            # Generate a random ball size
            diameter = random.randint(10, 30)

            # Generate a random position within the window
            # such that ball is always drawn in window
            # and is not overlapping any other balls
            position_found = False
            position = (0, 0)
            while not position_found:
                temp_position = generate_position(diameter)
                if ball_count == 0:
                    if self.debug:
                        print("First ball position generated.")
                    position = temp_position
                    position_found = True

                elif ball_count > 0:
                    nearby_balls = Simulator.__function_parallelizer(is_nearby,
                                                                     iterable=self.balls,
                                                                     bound_parameters=[temp_position, 45])

                    nearby_balls = [b for b in nearby_balls if b is not None]
                    if len(nearby_balls) == 0:
                        if self.debug:
                            print("No nearby balls detected, ball position generated.")
                        position = temp_position
                        position_found = True

                    else:
                        if self.debug:
                            print(f"{len(nearby_balls)} Nearby balls detected: {nearby_balls}.")
                        if True in Simulator.__function_parallelizer(detect_collision,
                                                                     iterable=nearby_balls,
                                                                     bound_parameters=[temp_position, diameter]):
                            if self.debug:
                                print("Collision detected, generating new ball position.")
                            continue

                        else:
                            if self.debug:
                                print("No collision detected, ball position generated.")
                            position = temp_position
                            position_found = True
                else:
                    raise Exception("Unexpected error occurred while generating ball position.")

            # Generate a random x speed and y speed
            speed_x = random.uniform(10, 20)
            speed_y = random.uniform(10, 20)
            velocity = Vector2D(speed_x, speed_y)

            # Create a new ball object with the random position, velocity, diameter, and color
            new_ball = BallObject(position, velocity, diameter, color="init")

            # Add the new ball to the list of balls
            self.balls.append(new_ball)

    def __wall_collision(self, b: BallObject) -> Vector2D:
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
        for b in self.balls:
            self.window.draw_ball(b.position, b.diameter, b.color)
