import pickle

from ball import BallObject


def save_to_file(balls: dict[int, list[BallObject]], filename: str) -> None:
    """
    Save the balls to a file using pickle.
    :param: balls: dict of lists of BallObjects (quadrants)
    :param: filename: str
    :return: None
    """
    if not isinstance(balls, dict):
        raise TypeError("balls must be a dictionary")

    with open(filename, "wb") as f:
        for quadrant in balls.keys():
            pickle.dump(balls[quadrant], f)


def load_from_file(filename: str) -> dict[int, list[BallObject]]:
    """
    Load the balls from a file using pickle.
    :param: filename: str
    :return: dict of lists of BallObjects (quadrants)
    """
    if not isinstance(filename, str):
        raise TypeError("Filename must be a string")
    with open(filename, "rb") as f:
        balls = {}
        for i in range(4):
            try:
                balls[i] = pickle.load(f)
            except EOFError:
                break
    print("Loaded balls from file successfully.")
    return balls
