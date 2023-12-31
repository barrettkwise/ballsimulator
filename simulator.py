import math
import random
from operator import gt, lt

from ball import BallObject
from vector import Vector2D
from view import Window


class Simulator:
    @staticmethod
    def __closest_ball(pos: tuple[float, float], gen_balls: list[BallObject], search_dist: int) \
            -> BallObject or None:
        nearby_balls = []
        # only add balls if they are within the search distance
        # gen balls = list of currently generated balls
        for b in gen_balls:
            if b.position == pos:
                continue
            rough_dist = math.sqrt((math.pow((b.position[0] - pos[0]), 2) +
                                    math.pow((b.position[1] - pos[1]), 2)))
            # only do further check on balls with a center to center distance
            # less than the search distance
            if rough_dist < search_dist:
                distances = []
                top = (b.position[0], b.position[1] + b.radius)
                bottom = (b.position[0], b.position[1] - b.radius)
                left = (b.position[0] - b.radius, b.position[1])
                right = (b.position[0] + b.radius, b.position[1])
                points = ([top, False], [bottom, False], [left, False], [right, False])
                for point in points:
                    dist = math.sqrt((math.pow((point[0][0] - pos[0]), 2) +
                                      math.pow((point[0][1] - pos[1]), 2)))
                    if dist <= search_dist:
                        point[1] = True
                        distances.append(dist)

                # if all points are within the search distance, add the ball
                if all([point[1] for point in points]):
                    nearby_balls.append((b, min(distances)))

        if len(nearby_balls) == 1:
            nearest_ball = nearby_balls[0][0]
            return nearest_ball

        elif len(nearby_balls) > 1:
            nearby_balls.sort(key=lambda x: x[1])
            nearest_ball = nearby_balls[0][0]
            return nearest_ball

        else:
            return None

    @staticmethod
    def __detect_collision(ball1_position: tuple[float, float], ball1_radius: int, ball2: BallObject) -> bool:
        # Calculate the distance between the two balls
        distance = math.sqrt((math.pow((ball2.position[0] - ball1_position[0]), 2) +
                              math.pow((ball2.position[1] - ball1_position[1]), 2)))

        # Calculate the sum of the two balls' radii
        radii_sum = ball1_radius + ball2.radius
        # Check if the distance is less than the sum of the radii
        if distance < radii_sum:
            return True
        else:
            return False

    @staticmethod
    def __ball_to_ball_physics(ball1: BallObject, ball2: BallObject) -> Vector2D:
        def compute_velocity(v1: Vector2D, v2: Vector2D, m1: float, m2: float, x1: float, x2: float) -> Vector2D:
            return v1 - (2 * m2 / (m1 + m2)) * (((v1 - v2) * (x1 - x2)) / math.pow(x1 - x2, 2)) * (x1 - x2)

        return compute_velocity(ball1.velocity, ball2.velocity, ball1.mass, ball2.mass,
                                ball1.position[0], ball2.position[0])

    def __init__(self,
                 window_size: tuple[int, int],
                 num_of_balls: int = random.randint(2, 100),
                 drawing_accuracy: int = 0,
                 time_step: float = 0.05,
                 debug: bool = False,
                 ) -> None:
        self.window = Window(window_size[0], window_size[1], drawing_accuracy)
        self.num_of_balls = num_of_balls
        self.balls = list()
        self.time = 0.0
        self.time_step = time_step
        self.debug = debug

    def start(self) -> None:
        self.__generate_balls()
        if self.debug:
            print("Ball generation complete.\nStarting simulation.")
        while True:
            self.window.draw_border()
            self.__draw_all_balls()
            self.window.screen.update()
            self.__move_balls()
            self.window.turtle.clear()
            self.time += self.time_step

    def __move_balls(self) -> None:
        new_balls = []

        # list of tuples representing pairs of
        # balls that have collided
        collision_balls = []

        num_of_balls = len(self.balls)
        for ball1 in range(num_of_balls):
            ball1_object = self.balls[ball1]
            closest_ball = Simulator.__closest_ball(ball1_object.position, self.balls, 20)

            if closest_ball is None:
                ball1_new_vel = self.__wall_collision(ball1_object)
                ball1_new_x = ball1_object.position[0] + (ball1_new_vel.x * self.time_step)
                ball1_new_y = ball1_object.position[1] + (ball1_new_vel.y * self.time_step)
                new_pos = (ball1_new_x, ball1_new_y)
                new_balls.append(BallObject(new_pos, ball1_new_vel, self.balls[ball1].diameter,
                                            self.balls[ball1].color))
                continue

            elif closest_ball is not None:
                if self.debug:
                    print(f"Closest ball to {ball1_object} is {closest_ball}.")

                if self.__detect_collision(ball1_object.position, ball1_object.radius, closest_ball):
                    if self.debug:
                        print(f"Collision detected between {ball1_object} and {closest_ball}.")
                    # Add the pair of balls to list of collided balls
                    collision_balls.append((ball1_object, closest_ball))
                    continue

                else:
                    ball1_new_vel = self.__wall_collision(ball1_object)
                    ball1_new_x = ball1_object.position[0] + (ball1_new_vel.x * self.time_step)
                    ball1_new_y = ball1_object.position[1] + (ball1_new_vel.y * self.time_step)
                    new_pos = (ball1_new_x, ball1_new_y)
                    new_balls.append(BallObject(new_pos, ball1_new_vel, ball1_object.diameter,
                                                ball1_object.color))
                    continue

        if len(collision_balls) > 0:
            for pair in collision_balls:
                reversed_pair = tuple(reversed(pair))
                if collision_balls.count(reversed_pair) > 0:
                    collision_balls.remove(reversed_pair)

                ball1 = pair[0]
                ball2 = pair[1]

                ball1_new_vel = Simulator.__ball_to_ball_physics(ball1, ball2)
                ball2_new_vel = Simulator.__ball_to_ball_physics(ball2, ball1)

                ball1_new_x = ball1.position[0] + (ball1_new_vel.x * self.time_step)
                ball1_new_y = ball1.position[1] + (ball1_new_vel.y * self.time_step)

                ball2_new_x = ball2.position[0] + (ball2_new_vel.x * self.time_step)
                ball2_new_y = ball2.position[1] + (ball2_new_vel.y * self.time_step)

                new_pos1 = (ball1_new_x, ball1_new_y)
                new_pos2 = (ball2_new_x, ball2_new_y)

                new_balls.append(BallObject(new_pos1, ball1_new_vel, ball1.diameter, ball1.color))
                new_balls.append(BallObject(new_pos2, ball2_new_vel, ball2.diameter, ball2.color))

        if self.debug:
            print("Ball movement complete.")

        if len(new_balls) != self.num_of_balls:
            raise Exception("Unexpected error occurred while moving balls.")

        self.balls.clear()
        self.balls = new_balls

    def __generate_balls(self) -> None:

        def generate_position(d: int, x: float = None) -> tuple[float, float]:
            def sign(s):
                return -1 if s < 0 else 1

            # Check if valid x has been found
            # to prevent needless recursion
            if x is None:
                temp_x = random.uniform(-self.window.width, self.window.width)
                x_cord_sign = sign(temp_x)
                if x_cord_sign == -1:
                    op = gt
                else:
                    op = lt
                if op(temp_x + (x_cord_sign * d / 2), x_cord_sign * self.window.width):
                    x = temp_x
                else:
                    return generate_position(d, None)

            # Generate valid y value, reusing
            # the x value found above
            temp_y = random.uniform(-self.window.height, self.window.height)
            y_cord_sign = sign(temp_y)
            if y_cord_sign == -1:
                op = gt
            else:
                op = lt
            if op(temp_y + (y_cord_sign * d / 2), y_cord_sign * self.window.height):
                y = temp_y
            else:
                return generate_position(d, x)
            return x, y

        for ball_count in range(self.num_of_balls):
            # Generate a random position within the window
            # such that ball is always drawn in window
            # and is not overlapping any other balls
            position_found = False
            position = (0, 0)
            diameter = 0
            closest_ball = None
            while not position_found:
                diameter = random.randint(10, 15)
                temp_position = generate_position(diameter)
                if ball_count == 0:
                    if self.debug:
                        print("First ball position generated.")
                    position = temp_position
                    position_found = True

                elif ball_count > 0:
                    closest_ball = Simulator.__closest_ball(temp_position, self.balls, 45)

                    if closest_ball is None:
                        if self.debug:
                            print("No nearby balls detected, ball position generated.")
                        position = temp_position
                        position_found = True

                    elif closest_ball is not None:
                        if self.debug:
                            print(f"Closest ball: {closest_ball}.")

                        if Simulator.__detect_collision(ball1_position=temp_position,
                                                        ball1_radius=diameter / 2,
                                                        ball2=closest_ball):
                            if self.debug:
                                print("Ball collision detected, generating new position.")
                            continue

                        else:
                            if self.debug:
                                print("No ball collision detected, ball position generated.")
                            position = temp_position
                            position_found = True

                else:
                    raise Exception("Unexpected error occurred while generating ball position.")

            # Generate a random x speed and y speed
            speed_x = random.uniform(-20, 20)
            speed_y = random.uniform(-20, 20)
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
