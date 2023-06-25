import math
import operator
import random
import turtle

import ball
import view


class Simulator:
    def __init__(self,
                 window_size: tuple[int, int],
                 num_of_balls: int = random.randint(1, 30),
                 debug: bool = False,
                 ) -> None:
        self.window = view.Window(window_size[0], window_size[1])
        self.num_of_balls = num_of_balls
        self.debug = debug
        self.balls = []
        self.__run_simulation()

    @staticmethod
    def __detect_collision(ball1_position: tuple[float, float], ball1_diameter: int, ball2: ball.BallObject) -> bool:
        # Calculate the distance between the two balls
        distance = math.sqrt((math.pow((ball2.position[0] - ball1_position[0]), 2) +
                              math.pow((ball2.position[1] - ball1_position[1]), 2)))

        # Calculate the sum of the two balls' radii
        radii_sum = (ball1_diameter / 2) + (ball2.diameter / 2)

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
        for b in gen_balls:
            # Calculate the center to center distance between the two balls
            distance = math.sqrt((math.pow((b.position[0] - pos[0]), 2) + math.pow((b.position[1] - pos[1]), 2)))

            if distance <= search_dist:
                nearby_balls.append(b)
            else:
                continue

        return nearby_balls

    @staticmethod
    def __draw_all_balls(balls: list[ball.BallObject], window: view.Window) -> None:
        for b in balls:
            window.draw_ball(b.position, b.diameter, b.color)

    def __run_simulation(self) -> None:
        self.__generate_balls()
        if self.debug:
            print("Ball generation complete.")
        while True:
            if self.debug:
                print("Simulating...")
            Simulator.__draw_all_balls(self.balls, self.window)
            self.window.screen.update()
            self.__move_balls()
            self.window.turtle.clear()

    # Code run to move individual ball according to its velocity
    # and angle. Also check for collisions.
    def __move_balls(self) -> None:
        for b in self.balls:
            if self.debug:
                print("Moving balls...")
            # Calculate the new position of the ball
            new_x = b.position[0] + (b.speed * math.cos(b.angle))
            new_y = b.position[1] + (b.speed * math.sin(b.angle))
            new_pos = turtle.Vec2D(new_x, new_y)

            # Check if the ball has collided with the wall
            if new_x + b.diameter >= self.window.width or new_x - b.diameter <= -self.window.width:
                # If so, then change the angle of the ball
                b.angle = math.pi - b.angle
            if new_y + b.diameter >= self.window.height or new_y - b.diameter <= -self.window.height:
                # If so, then change the angle of the ball
                b.angle = math.tau - b.angle

            # Check if the ball has collided with another ball
            nearby_balls = Simulator.__nearby_balls(new_pos, self.balls, b.diameter)
            if len(nearby_balls) > 0:
                for ball_inst in nearby_balls:
                    if Simulator.__detect_collision(new_pos, b.diameter, ball_inst):
                        # If so, then change the angle of the ball
                        b.angle -= math.pi
                        b.speed += math.cos(b.angle) * ball_inst.speed

            else:
                # Update the ball's position
                b.position = new_pos

            # Update the ball's position
            b.position = new_pos
            if self.debug:
                print("Ball moved.")

    # Code run to create simulation environment
    def __generate_balls(self) -> None:

        def generate_position(d: float, x: float = None) -> turtle.Vec2D:
            def sign(s):
                return -1 if s < 0 else 1

            # Check if valid x has been found
            # to prevent needless recursion
            if x is None:
                temp_x = random.uniform(-self.window.width, self.window.width)
                if sign(temp_x) == -1:
                    op = operator.gt
                else:
                    op = operator.lt

                if op(temp_x + (sign(temp_x) * d), sign(temp_x) * self.window.width):
                    x = temp_x
                else:
                    return generate_position(d, None)

            # Generate valid y value, reusing
            # the x value found above
            temp_y = random.uniform(-self.window.height, self.window.height)
            if sign(temp_y) == -1:
                op = operator.gt
            else:
                op = operator.lt

            if op(temp_y + (sign(temp_y) * d), sign(temp_y) * self.window.height):
                y = temp_y
            else:
                return generate_position(d, x)

            return turtle.Vec2D(x, y)

        for ball_count in range(self.num_of_balls):
            # Generate a random ball size
            diameter = random.randint(10, 30)

            # Generate a random position within the window
            # such that ball is always drawn in window
            # and is not overlapping any other balls
            position_found = False
            position = turtle.Vec2D(0, 0)
            while not position_found:
                temp_position = generate_position(diameter)
                if ball_count == 0:
                    if self.debug:
                        print("First ball position generated.")
                    position = temp_position
                    position_found = True

                elif ball_count > 0:
                    nearby_balls = Simulator.__nearby_balls(temp_position, self.balls, diameter * 2)

                    if len(nearby_balls) == 0:
                        if self.debug:
                            print("No nearby balls detected, ball position generated.")
                        position = temp_position
                        position_found = True

                    else:
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

            # Generate a random speed and direction
            speed = random.uniform(-10, 10)
            angle = math.radians(random.uniform(0, 360))
            velocity = turtle.Vec2D(speed, angle)

            # Create a new ball object with the random position and velocity
            new_ball = ball.BallObject(position, velocity, diameter)

            # Add the new ball to the list of balls
            self.balls.append(new_ball)
        pass
