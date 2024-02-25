import pickle
from ball import BallObject


def save_to_file(balls: tuple[list[BallObject]], filename: str) -> None:
    '''
    Save the balls to a file using pickle.
    param: balls: tuple of lists of BallObjects
    param: filename: str
    return: None
    '''
    if not isinstance(balls, tuple):
        raise TypeError('balls must be a tuple of lists')

    with open(filename, 'wb') as f:
        for quadrant in balls:
            pickle.dump(quadrant, f)


def load_from_file(filename: str) -> tuple[list[BallObject]]:
    '''
    Load the balls from a file using pickle.
    param: filename: str
    return: tuple of lists of BallObjects
    '''
    with open(filename, "rb") as f:
        balls = []
        while True:
            try:
                balls.append(pickle.load(f))
            except EOFError:
                break
    return tuple(balls)
