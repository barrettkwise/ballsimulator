import math
import random
from operator import gt, lt

import ball
import vector
import view


class Simulator:
    @staticmethod
    def __detect_collision(ball1_position: tuple[float, float], ball1_diameter: int, ball2: ball.BallObject) -> bool:
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

    @staticmethod
    def __nearby_balls(pos: tuple[float, float], gen_balls: list[ball.BallObject], search_dist: int) \
            -> list[ball.BallObject]:
        nearby_balls = []
        # only add balls if they are within the search distance
        # gen balls = list of currently generated balls
        for b in gen_balls:
            top = (b.position[0], b.position[1] + b.radius)
            bottom = (b.position[0], b.position[1] - b.radius)
            left = (b.position[0] - b.radius, b.position[1])
            right = (b.position[0] + b.radius, b.position[1])
            points = [top, bottom, left, right]
            in_range = True
            for point in points:
                dist = math.sqrt((math.pow((point[0] - pos[0]), 2) + math.pow((point[1] - pos[1]), 2)))
                if dist > search_dist:
                    in_range = False
                    break

            if in_range:
                nearby_balls.append(b)

        return nearby_balls

    @staticmethod
    def __ball_to_ball_physics_handler(ball1: ball.BallObject, ball2: ball.BallObject) -> \
            tuple[vector.Vector2D, vector.Vector2D]:
        v1 = vector.Vector2D(ball1.speed_x, ball1.speed_y)
        v2 = vector.Vector2D(ball2.speed_x, ball2.speed_y)

        norm_vect = vector.Vector2D(ball2.position[0] - ball1.position[0],
                                    ball2.position[1] - ball1.position[1])
        unit_norm_vect = norm_vect / abs(norm_vect)
        unit_tan_vect = vector.Vector2D(-norm_vect.y, norm_vect.x)
        v1n = unit_norm_vect.dot(v1)
        v1t = unit_tan_vect.dot(v1)
        v2n = unit_norm_vect.dot(v2)
        v2t = unit_tan_vect.dot(v2)
        v1t_prime = v1t
        v2t_prime = v2t
        v1n_prime = (v1n * (ball1.mass - ball2.mass) + (2 * ball2.mass * v2n)) / (ball1.mass + ball2.mass)

        v2n_prime = (v2n * (ball2.mass - ball1.mass) + (2 * ball1.mass * v1n)) / (ball1.mass + ball2.mass)
        v1n_prime = vector.Vector2D(v1n_prime * unit_norm_vect.x, v1n_prime * unit_norm_vect.y)
        v1t_prime = vector.Vector2D(v1t_prime * unit_tan_vect.x, v1t_prime * unit_tan_vect.y)
        v2n_prime = vector.Vector2D(v2n_prime * unit_norm_vect.x, v2n_prime * unit_norm_vect.y)
        v2t_prime = vector.Vector2D(v2t_prime * unit_tan_vect.x, v2t_prime * unit_tan_vect.y)

        v1_prime = v1n_prime + v1t_prime
        v2_prime = v2n_prime + v2t_prime

        return v1_prime, v2_prime

    @staticmethod
    def __draw_all_balls(balls: list[ball.BallObject], window: view.Window) -> None:
        for b in balls:
            window.draw_ball(b.position, b.diameter, b.color)

    def __init__(self,
                 window_size: tuple[int, int],
                 num_of_balls: int = random.randint(2, 100),
                 time_step: float = 0.000001,
                 debug: bool = False,
                 ) -> None:
        self.window = view.Window(window_size[0], window_size[1])
        self.num_of_balls = num_of_balls
        self.time = 0
        self.time_step = time_step
        self.debug = debug
        self.balls = []

    def start(self) -> None:
        self.__generate_balls()
        if self.debug:
            print("Ball generation complete.")
            print("Starting simulation.")
        while True:
            self.window.draw_border()
            Simulator.__draw_all_balls(self.balls, self.window)
            self.window.screen.update()
            self.__move_balls()
            self.window.screen.update()
            self.window.turtle.clear()
            self.time += self.time_step

    def __move_balls(self) -> None:
        new_balls = []
        for ball1 in range(len(self.balls)):
            nearby_balls = Simulator.__nearby_balls(self.balls[ball1].position, self.balls,
                                                    45)
            if len(nearby_balls) == 0:
                ball1_new_vel = self.__wall_collision(self.balls[ball1])
                ball1_new_x = self.balls[ball1].position[0] + (ball1_new_vel.x * self.time_step)
                ball1_new_y = self.balls[ball1].position[1] + (ball1_new_vel.y * self.time_step)
                new_pos = (ball1_new_x, ball1_new_y)
                new_balls.append(ball.BallObject(new_pos, ball1_new_vel, self.balls[ball1].diameter,
                                                 self.balls[ball1].color))

            elif len(nearby_balls) > 0:
                if self.debug:
                    print("Ball", ball1, "has", len(nearby_balls), "nearby balls.")
                ball1_new_x = self.balls[ball1].position[0] + (self.balls[ball1].speed_x * self.time_step)
                ball1_new_y = self.balls[ball1].position[1] + (self.balls[ball1].speed_y * self.time_step)
                new_pos = (ball1_new_x, ball1_new_y)
                vel_vectors = []
                for ball2 in self.balls:
                    # Check if ball2 is in nearby_balls
                    if ball2 in nearby_balls and ball2 is not self.balls[ball1]:
                        # Check if ball1 and ball2 have collided
                        if Simulator.__detect_collision(new_pos, self.balls[ball1].diameter,
                                                        ball2):
                            if self.debug:
                                print("Collision detected between ball:", ball1, "and ball:", ball2, ".")
                            # Calculate new velocities
                            ball1_new_vel, ball2_new_vel = Simulator.__ball_to_ball_physics_handler(self.balls[ball1],
                                                                                                    ball2)
                            vel_vectors.append(ball1_new_vel)
                            ball2.velocity = ball2_new_vel

                if len(vel_vectors) == 0:
                    ball1_new_vel = self.__wall_collision(self.balls[ball1])
                    ball1_new_x = self.balls[ball1].position[0] + (ball1_new_vel.x * self.time_step)
                    ball1_new_y = self.balls[ball1].position[1] + (ball1_new_vel.y * self.time_step)
                    new_pos = (ball1_new_x, ball1_new_y)
                    new_balls.append(ball.BallObject(new_pos, ball1_new_vel, self.balls[ball1].diameter,
                                                     self.balls[ball1].color))

                else:
                    avg_vel = vector.Vector2D(sum([v.x for v in vel_vectors]) / len(vel_vectors),
                                              sum([v.y for v in vel_vectors]) / len(vel_vectors))
                    new_pos = (ball1_new_x + (avg_vel.x * self.time_step),
                               ball1_new_y + (avg_vel.y * self.time_step))

                    new_balls.append(
                        ball.BallObject(new_pos, avg_vel, self.balls[ball1].diameter, self.balls[ball1].color))

        if self.debug:
            print("Ball movement complete.")
        self.balls.clear()
        self.balls = new_balls

    # Code run to create simulation environment
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
                    nearby_balls = Simulator.__nearby_balls(temp_position, self.balls, 45)

                    if len(nearby_balls) == 0:
                        if self.debug:
                            print("No nearby balls detected, ball position generated.")
                        position = temp_position
                        position_found = True

                    else:
                        if self.debug:
                            print(f"{len(nearby_balls)} Nearby balls detected: {nearby_balls}.")
                        for b_count, b in enumerate(nearby_balls):
                            collision_result = Simulator.__detect_collision(temp_position, diameter, b)
                            if collision_result:
                                if self.debug:
                                    print("Collision detected, retrying ball position generation.")
                                break
                            elif not collision_result and b_count == len(nearby_balls):
                                if self.debug:
                                    print("No collisions detected, ball position generated.")
                                position = temp_position
                                position_found = True

                else:
                    raise Exception("Unexpected error occurred while generating ball position.")

            # Generate a random x speed and y speed
            # such that the ball moves at a reasonable speed
            # regardless of the time step
            speed_x = random.uniform(0.1, 1) * math.pow(10, int(str(self.time_step)[-2:]))
            speed_y = random.uniform(0.1, 1) * math.pow(10, int(str(self.time_step)[-2:]))
            velocity = vector.Vector2D(speed_x, speed_y)

            # Create a new ball object with the random position, velocity, diameter, and color
            new_ball = ball.BallObject(position, velocity, diameter, "init")

            # Add the new ball to the list of balls
            self.balls.append(new_ball)

    def __out_of_bounds(self, b: ball.BallObject) -> None:
        x = round(b.position[0], 5)
        y = round(b.position[1], 5)
        buffer = 0.9
        if x - buffer > self.window.width or x + buffer < -self.window.width:
            raise ValueError(f"{b} is out of bounds. Position: {b.position}")

        if y - buffer > self.window.height or y + buffer < -self.window.height:
            raise ValueError(f"{b} is out of bounds. Position: {b.position}")

    def __wall_collision(self, b: ball.BallObject) -> vector.Vector2D:
        x = round(b.position[0], 5)
        y = round(b.position[1], 5)
        buffer = b.radius
        new_speed_x = b.speed_x
        new_speed_y = b.speed_y

        if x + buffer >= self.window.width or x - buffer <= -self.window.width:
            new_speed_x *= -1

        if y + buffer >= self.window.height or y - buffer <= -self.window.height:
            new_speed_y *= -1

        return vector.Vector2D(new_speed_x, new_speed_y)

    # Code run to move individual ball according to its velocity
    # and angle. Also check for collisions.
