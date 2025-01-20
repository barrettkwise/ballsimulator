from math import atan2, sqrt


class Vector2D:
    """A two-dimensional vector with Cartesian coordinates."""

    def __init__(self, x: int | float, y: int | float) -> None:
        """Create a new vector with components x and y."""
        if not all(isinstance(i, (int, float)) for i in (x, y)):
            raise TypeError("Vector components must be integers or floats")
        self.x, self.y = x, y

    def __str__(self) -> str:
        """Human-readable string representation of the vector."""
        return f"({self.x}i, {self.y}j)"

    def __repr__(self) -> str:
        """Unambiguous string representation of the vector."""
        return repr((self.x, self.y))

    def dot(self, other: "Vector2D") -> float:
        """The scalar (dot) product of self and other. Both must be vectors."""

        if not isinstance(other, Vector2D):
            raise TypeError("Can only take dot product of two Vector2D objects")
        return self.x * other.x + self.y * other.y

    # Alias the __matmul__ method to dot so we can use a @ b as well as a.dot(b).
    __matmul__ = dot

    def __sub__(self, other: "Vector2D") -> "Vector2D":
        """Vector subtraction."""
        if not isinstance(other, Vector2D):
            raise TypeError("Can only subtract two Vector2D objects")
        return Vector2D(self.x - other.x, self.y - other.y)

    def __add__(self, other: "Vector2D") -> "Vector2D":
        """Vector addition."""
        if not isinstance(other, Vector2D):
            raise TypeError("Can only add two Vector2D objects")
        return Vector2D(self.x + other.x, self.y + other.y)

    def __mul__(self, scalar: int | float) -> "Vector2D":
        """Multiplication of a vector by a scalar."""

        if isinstance(scalar, (int, float)):
            return Vector2D(self.x * scalar, self.y * scalar)
        raise NotImplementedError("Can only multiply Vector2D by a scalar")

    def __rmul__(self, scalar: int | float) -> "Vector2D":
        """Multiplication of a vector by a scalar."""

        if isinstance(scalar, (int, float)):
            return Vector2D(self.x * scalar, self.y * scalar)
        raise NotImplementedError("Can only multiply Vector2D by a scalar")

    def __neg__(self) -> "Vector2D":
        """Negation of the vector (invert through origin.)"""
        return Vector2D(-self.x, -self.y)

    def __truediv__(self, scalar: int | float) -> "Vector2D":
        """True division of the vector by a scalar."""
        if isinstance(scalar, (int, float)):
            return Vector2D(self.x / scalar, self.y / scalar)
        raise NotImplementedError("Can only divide Vector2D by a scalar")

    def __mod__(self, scalar: int | float) -> "Vector2D":
        """One way to implement modulus operation: for each component."""
        if isinstance(scalar, (int, float)):
            return Vector2D(self.x % scalar, self.y % scalar)
        raise NotImplementedError("Can only take modulus of Vector2D by a scalar")

    def __abs__(self) -> float:
        """Absolute value (magnitude) of the vector."""
        return sqrt(pow(self.x, 2) + pow(self.y, 2))

    def distance_to(self, other: "Vector2D") -> float:
        """The distance between vectors self and other."""
        if not isinstance(other, Vector2D):
            raise TypeError("Can only take distance between two Vector2D objects")
        else:
            return abs(self - other)

    def to_polar(self) -> tuple[float, float]:
        """Return the vector's components in polar coordinates."""
        return abs(self), atan2(self.y, self.x)