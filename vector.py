import math


class Vector2D:
    """A two-dimensional vector with Cartesian coordinates."""

    def __init__(self, x, y) -> None:
        """Create a new vector with components x and y."""
        if not all(isinstance(i, (int, float)) for i in (x, y)):
            raise TypeError('Vector components must be integers or floats')
        self.x, self.y = x, y

    def __str__(self) -> str:
        """Human-readable string representation of the vector."""
        return f'({self.x}i, {self.y}j)'

    def __repr__(self) -> str:
        """Unambiguous string representation of the vector."""
        return repr((self.x, self.y))

    def dot(self, other) -> float:
        """The scalar (dot) product of self and other. Both must be vectors."""

        if not isinstance(other, Vector2D):
            raise TypeError(
                'Can only take dot product of two Vector2D objects')
        return self.x * other.x + self.y * other.y

    # Alias the __matmul__ method to dot so we can use a @ b as well as a.dot(b).
    __matmul__ = dot

    def __sub__(self, other) -> object:
        """Vector subtraction."""
        return Vector2D(self.x - other.x, self.y - other.y)

    def __add__(self, other) -> object:
        """Vector addition."""
        return Vector2D(self.x + other.x, self.y + other.y)

    def __mul__(self, scalar) -> object:
        """Multiplication of a vector by a scalar."""

        if isinstance(scalar, (int, float)):
            return Vector2D(self.x * scalar, self.y * scalar)
        raise NotImplementedError('Can only multiply Vector2D by a scalar')

    def __rmul__(self, scalar) -> object:
        """Reflected multiplication so vector * scalar also works."""
        return self.__mul__(scalar)

    def __neg__(self) -> object:
        """Negation of the vector (invert through origin.)"""
        return Vector2D(-self.x, -self.y)

    def __truediv__(self, scalar) -> object:
        """True division of the vector by a scalar."""
        return Vector2D(self.x / scalar, self.y / scalar)

    def __mod__(self, scalar) -> object:
        """One way to implement modulus operation: for each component."""
        return Vector2D(self.x % scalar, self.y % scalar)

    def __abs__(self) -> float:
        """Absolute value (magnitude) of the vector."""
        return math.sqrt(math.pow(self.x, 2) + math.pow(self.y, 2))

    def distance_to(self, other) -> float:
        """The distance between vectors self and other."""
        return abs(self - other)

    def to_polar(self) -> tuple[float, float]:
        """Return the vector's components in polar coordinates."""
        return abs(), math.atan2(self.y, self.x)
