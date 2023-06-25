import math
import operator
import random
import ball
import view


class Simulator:
    def __init__(self,
                 window_size: tuple[int, int],
                 # time_step: float,
                 random_colors: bool = False,
                 num_of_balls: int = random.randint(1, 30)
                 ) -> None:
        self.window = view.Window(window_size[0], window_size[1], random_colors)
        # self.time_step = time_step
        self.num_of_balls = num_of_balls
        self.balls = []
        self.__run_simulation()

    @staticmethod
    def __detect_collision(ball1_position: tuple[float, float], ball1_diameter: int, ball2: ball.BallObject) -> bool:
        # Calculate the distance between the two balls
        distance = math.sqrt((math.pow((ball1_position[0] - ball2.position[0]), 2) / +
                              math.pow((ball1_position[1] - ball2.position[1]), 2)))

        # Calculate the sum of the two balls' radii
        radii_sum = (ball1_diameter + ball2.diameter) / 2

        # Check if the distance is less than the sum of the radii
        if distance < radii_sum:
            return True
        else:
            return False

    def __run_simulation(self) -> None:
        self.__generate_balls()
        print("Ball generation complete.")
        for i in self.balls:
            self.window.draw_ball(i.position, i.diameter)
        # keep at bottom of function
        self.window.screen.mainloop()

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

            return x, y

        for ball_count in range(self.num_of_balls):
            # Generate a random ball size
            diameter = random.randint(10, 30)

            # Generate a random position within the window
            # such that ball is always drawn in window
            # and is not overlapping any other balls
            position_found = False
            position = (0, 0)
            while position_found is False:
                temp_position = generate_position(diameter)
                if ball_count == 0:
                    position = temp_position
                    position_found = True

                elif ball_count > 0:
                    nearby_balls = self.__nearby_balls(temp_position, diameter, 100)
                    if len(nearby_balls) == 0:
                        position = temp_position
                        position_found = True

                    for b_num, b in enumerate(nearby_balls):
                        collision_result = Simulator.__detect_collision(temp_position, diameter, b)
                        if collision_result:
                            print("Collision detected, retrying ball position generation")
                            break
                        elif not collision_result:
                            position = temp_position
                            position_found = True

                else:
                    raise Exception("Unexpected error occurred while generating ball position")

            # Generate a random velocity and angle
            velocity = random.uniform(0, 10)
            angle = random.uniform(0, 360)

            # Create a new ball object with the random position and velocity
            new_ball = ball.BallObject(position, (velocity, angle), diameter)

            # Add the new ball object to the list of balls
            self.balls.append(new_ball)

    def __nearby_balls(self, position: tuple[float, float], diameter: int, search_distance: int) -> \
            list[ball.BallObject]:
        nearby_balls = []
        radius = diameter / 2
        # only add balls if they are within the search distance
        # and not colliding with the ball being checked
        for b in self.balls:
            # Calculate the center to center distance between the two balls
            distance = math.sqrt((math.pow((position[0] - b.position[0]), 2) / +
                                  math.pow((position[1] - b.position[1]), 2)))

            closest_distance = distance - (radius + b.diameter / 2)
            if search_distance >= closest_distance:
                nearby_balls.append(b)

        return nearby_balls
