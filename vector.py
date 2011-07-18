""" The vector module provides classes that can be used for basic,
three-dimensional vector manipulations.  Vectors are immutable and should not be
subclassed. """

from __future__ import division

import math
import random

class Vector(object):
    """ Represents a two-dimensional vector.  In particular, this class
    features a number of factory methods to create vectors from angles and
    other input and a number of overloaded operators to facilitate vector
    math. """

    # Factory Methods {{{1
    @staticmethod
    def null():
        """ Return a null vector. """
        return Vector(0, 0)

    @staticmethod
    def random(magnitude=1):
        """ Create a unit vector pointing in a random direction. """
        theta = random.uniform(0, 2 * math.pi)
        return magnitude * Vector(math.cos(theta), math.sin(theta))

    @staticmethod
    def from_radians(angle):
        """ Create a vector that makes the given angle with the x-axis. """
        return Vector(math.cos(angle), math.sin(angle))

    @staticmethod
    def from_degrees(angle):
        """ Create a vector that makes the given angle with the x-axis. """
        return Vector.from_radians(angle * math.pi / 180)

    @staticmethod
    def from_vector3D(v, strip='z'):
        """ Create a 2D vector from a 3D vector, default removes the Z axis."""
        if 'z' is strip:
            return Vector(v.x, v.y)
        elif 'x' is strip:
            return Vector(v.y, v.z)
        elif 'y' is strip:
            return Vector(v.x, v.z)


    # Math Methods {{{1
    @staticmethod
    def get_radians(A, B):
        """ Return the angle between the two given vectors in degrees.  If
        either of the inputs are null vectors, an exception is thrown. """

        try:
            temp = A.get_magnitude() * B.get_magnitude()
            temp = Vector.dot(A, B) / temp
            return math.acos(temp)

        # Floating point error will confuse the trig functions occasionally.
        except ValueError:
            return 0 if temp > 0 else pi

        # It doesn't make sense to find the angle of a null vector. 
        except ZeroDivisionError:
            raise NullVectorError()

    @staticmethod
    def get_degrees(A, B):
        """ Return the angle between the two given vectors in degrees.  If
        either of the inputs are null vectors, an exception is thrown. """
        return Vector.get_radians(A, B) * 180 / math.pi

    @staticmethod
    def get_distance(A, B):
        """ Return the Euclidean distance between the two input vectors. """
        return (A - B).magnitude

    @staticmethod
    def get_manhattan(A, B):
        """ Return the Manhattan distance between the two input vectors. """
        disp = B - A
        return abs(disp.x) + abs(disp.y)

    @staticmethod
    def dot_product(A, B):
        """ Return the dot product of the given vectors. """
        return A.x * B.x + A.y * B.y

    @staticmethod
    def perp_product(A, B):
        """ Return the perp product of the given vectors.  The perp product is
        just a cross product where the third dimension is taken to be zero and
        the result is returned as a scalar. """

        return A.x * B.y - A.y * B.x

    # Create shorter aliases for the dot and perp products.
    dot = dot_product
    perp = perp_product
    # }}}1

    #2D Operators {{{1
    def __init__(self, x, y):
        """ Construct a vector using the given coordinates. """
        self.__x = x
        self.__y = y

    def __iter__(self):
        """ Iterate over this vectors coordinates. """
        yield self.x; yield self.y

    def __add__(self, v):
        """ Return the sum of this vector and the argument. """
        return Vector(self.x + v.x, self.y + v.y)

    def __sub__(self, v):
        """ Return the difference between this vector and the argument. """
        return Vector(self.x - v.x, self.y - v.y)

    def __neg__(self):
        """ Return a copy of this vector with the signs flipped. """
        return Vector(-self.x, -self.y)

    def __abs__(self):
        """ Return the absolute value of this vector. """
        return Vector(abs(self.x), abs(self.y))
    
    def __mul__(self, c):
        """ Return the scalar product of this vector and the argument. """
        return Vector(c * self.x, c * self.y)

    def __rmul__(self, c):
        """ Return the scalar product of this vector and the argument. """
        return Vector(c * self.x, c * self.y)

    def __div__(self, c):
        """ Return the scalar quotient of this vector and the argument.  The
        argument is taken as a float to ensure true division. """
        return Vector(self.x / float(c), self.y / float(c))

    def __truediv__(self, c):
        """ Return the scalar quotient of this vector and the argument. """
        return Vector(self.x / c, self.y / c)

    def __floordiv__(self, c):
        """ Return the integer quotient of this vector and the argument. """
        return Vector(self.x // c, self.y // c)

    def __mod__(self, c):
        """ Return the remainder after dividing this vector by the argument.
        This should work with integer and floating point input. """
        return Vector(self.x % c, self.y % c)

    def __eq__(self, other):
        """ Return true if this vector is exactly the same as the argument.
        Floating point rounding error is completely unaccounted for. """
        return self.x == other.x and self.y == other.y

    def __ne__(self, other):
        """ Return true if this vector and the argument are not the same. """
        return self.x != other.x or self.y != other.y

    def __nonzero__(self):
        """ Return true is the vector is not degenerate. """
        return self.x != 0 or self.y != 0

    def __repr__(self):
        """ Return a string representation of this vector. """
        return "<%f, %f>" % self.get_tuple()

    def __str__(self):
        """ Return a string representation of this vector. """
        return self.__repr__()

    # Attributes {{{1
    @property
    def x(self):
        """ Get the first coordinate in this vector. """
        return self.__x

    @property
    def y(self):
        """ Get the second coordinate in this vector. """
        return self.__y

    @property
    def r(self):
        """ Get the first coordinate in this vector. """
        return self.__x
    
    @property
    def th(self):
        """ Get the second coordinate in this vector. """
        return self.__y

    @property
    def tuple(self):
        """ Return the vector as a tuple. """
        return self.x, self.y

    @property
    def pygame(self):
        """ Return the vector as a tuple of integers.  This is the format
        Pygame expects to receive coordinates in. """
        return int(self.x), int(self.y)

    @property
    def magnitude(self):
        """ Calculate the length of this vector. """
        return math.sqrt(self.magnitude_squared)

    @property
    def magnitude_squared(self):
        """ Calculate the square of the length of this vector.  This is
        slightly more efficient that finding the real length. """
        return self.x**2 + self.y**2

    @property
    def normal(self):
        """ Return a unit vector pointing in the same direction as this
        one. """

        try:
            return self / self.magnitude
        except ZeroDivisionError:
            raise NullVectorError()

    @property
    def orthogonal(self):
        """ Return a vector that is orthogonal to this one.  The resulting
        vector is not normalized. """
        return Vector(-self.y, self.x)

    @property
    def orthonormal(self):
        """ Return a vector that is both normalized and orthogonal to this
        one. """
        return self.orthogonal.normal

    def get_x(self):
        return self.x

    def get_y(self):
        return self.y

    def get_r(self):
        return self.r

    def get_th(self):
        return self.th

    def get_tuple(self):
        return self.tuple

    def get_pygame(self):
        return self.pygame

    def get_magnitude(self):
        return self.magnitude

    def get_magnitude_squared(self):
        return self.magnitude_squared

    def get_normal(self, magnitude=1):
        return magnitude * self.normal

    def get_orthogonal(self):
        return self.orthogonal

    def get_orthonormal(self, magnitude=1):
        return magnitude * self.orthonormal

    def get_components(self, v):
        """ Break this vector into one vector that is parallel to the given
        vector and another that is perpendicular to it. """

        tangent = v * Vector.dot(self, v)
        normal = self - tangent
        return normal, tangent

    # }}}1


class Vector3D(object):
    """ Represents a three-dimensional vector.  In particular, this class
    features a number of factory methods to create vectors from angles and
    other input and a number of overloaded operators to facilitate vector
    math. """

    # Factory Methods {{{1
    @staticmethod
    def null():
        """ Return a null vector. """
        return Vector3D(0, 0, 0)

    @staticmethod
    def random(magnitude=1):
        """ Create a unit vector pointing in a random direction. """
        theta = random.uniform(0, 2 * math.pi)
        phi = random.uniform(0, 2 * math.pi)

        return magnitude * Vector3D.from_radians(theta, phi)

    @staticmethod
    def from_radians(theta, phi, radius=1):
        """ Create a vector that makes the given angles with the x-axis and
        z-axis. """
        x = radius * math.sin(phi) * math.cos(theta)
        y = radius * math.sin(phi) * math.sin(theta)
        z = radius * math.cos(phi)
        return Vector3D(x, y, z)

    @staticmethod
    def from_degrees(silly_theta, silly_phi, radius=1):
        """ Create a vector that makes the given angles with the x-axis and
        z-axis. """
        theta = silly_theta * math.pi / 180
        phi = silly_phi * math.pi / 180
        return Vector3D.from_radians(theta, phi, radius)

    @staticmethod
    def from_vector2D(v, dims=('x','y'), third_dim=0):
        """ Create a 3D vector from a 2D vector, optional specifications for
        which axes the 2D vector refers to and the initial value of the third 
        axis."""
        if 'x' in dims and 'y' in dims:
            return Vector3D(v.x, v.y, third_dim)
        elif 'x' in dims and 'z' in dims:
            return Vector3D(v.x, third_dim, v.y)
        elif 'y' in dims and 'z' in dims:
            return Vector3D(third_dim, v.x, v.y)


    # Math Methods {{{1
    @staticmethod
    def get_radians(A, B):
        """ Return the angle between the two given vectors in degrees.  If
        either of the inputs are null vectors, an exception is thrown. """

        try:
            temp = A.get_magnitude() * B.get_magnitude()
            temp = Vector3D.dot(A, B) / temp
            return math.acos(temp)

        # Floating point error will confuse the trig functions occasionally.
        except ValueError:
            return 0 if temp > 0 else pi

        # It doesn't make sense to find the angle of a null vector. 
        except ZeroDivisionError:
            raise NullVectorError()

    @staticmethod
    def get_degrees(A, B):
        """ Return the angle between the two given vectors in degrees.  If
        either of the inputs are null vectors, an exception is thrown. """
        return Vector3D.get_radians(A, B) * 180 / math.pi

    @staticmethod
    def get_distance(A, B):
        """ Return the Euclidean distance between the two input vectors. """
        return (A - B).magnitude

    @staticmethod
    def get_manhattan(A, B):
        """ Return the Manhattan distance between the two input vectors. """
        disp = B - A
        return abs(disp.x) + abs(disp.y)

    @staticmethod
    def dot_product(A, B):
        """ Return the dot product of the given vectors. """
        return A.x * B.x + A.y * B.y + A.z * B.z

    @staticmethod
    def cross_product(A,B):
        """ Return the cross product of two 3 dimensional vectors."""
        x = A.y * B.z - A.z + B.y
        y = A.z * B.x - A.x + B.z
        z = A.x * B.y - A.y + B.x
        return Vector3D(x, y, z)

    # Create shorter aliases for the dot and perp products.
    dot = dot_product
    # }}}1

    # Operators {{{1
    def __init__(self, x, y, z):
        """ Construct a vector using the given coordinates. """
        self.__x = x
        self.__y = y
        self.__z = z

    def __iter__(self):
        """ Iterate over this vectors coordinates. """
        yield self.x; yield self.y; yield self.z

    def __add__(self, v):
        """ Return the sum of this vector and the argument. """
        return Vector3D(self.x + v.x, self.y + v.y, self.z + v.z)

    def __sub__(self, v):
        """ Return the difference between this vector and the argument. """
        return Vector3D(self.x - v.x, self.y - v.y, self.z - v.z)

    def __neg__(self):
        """ Return a copy of this vector with the signs flipped. """
        return Vector3D(-self.x, -self.y, -self.z)

    def __abs__(self):
        """ Return the absolute value of this vector. """
        return Vector3D(abs(self.x), abs(self.y), abs(self.z))
    
    def __mul__(self, c):
        """ Return the scalar product of this vector and the argument. """
        return Vector3D(c * self.x, c * self.y, c * self.z)

    def __rmul__(self, c):
        """ Return the scalar product of this vector and the argument. """
        return Vector3D(c * self.x, c * self.y, c * self.z)

    def __div__(self, c):
        """ Return the scalar quotient of this vector and the argument.  The
        argument is taken as a float to ensure true division. """
        return Vector3D(self.x / float(c), self.y / float(c), self.z / float(c))

    def __truediv__(self, c):
        """ Return the scalar quotient of this vector and the argument. """
        return Vector3D(self.x / c, self.y / c, self.z / c)

    def __floordiv__(self, c):
        """ Return the integer quotient of this vector and the argument. """
        return Vector3D(self.x // c, self.y // c, self.z // c)

    def __mod__(self, c):
        """ Return the remainder after dividing this vector by the argument.
        This should work with integer and floating point input. """
        return Vector3D(self.x % c, self.y % c, self.z % c)

    def __eq__(self, other):
        """ Return true if this vector is exactly the same as the argument.
        Floating point rounding error is completely unaccounted for. """
        return self.x == other.x and self.y == other.y and self.z == other.z

    def __ne__(self, other):
        """ Return true if this vector and the argument are not the same. """
        return self.x != other.x or self.y != other.y  or self.z != other.z

    def __nonzero__(self):
        """ Return true is the vector is not degenerate. """
        return self.x != 0 or self.y != 0 or self.z != 0

    def __repr__(self):
        """ Return a string representation of this vector. """
        return "<%f, %f, %f>" % self.get_tuple()

    def __str__(self):
        """ Return a string representation of this vector. """
        return self.__repr__()

    # Attributes {{{1
    @property
    def x(self):
        """ Get the first coordinate in this vector. """
        return self.__x

    @property
    def y(self):
        """ Get the second coordinate in this vector. """
        return self.__y

    @property
    def z(self):
        """ Get the third coordinate in this vector. """
        return self.__z

    @property
    def r(self):
        """ Get the first coordinate in this vector. """
        return self.__x
    
    @property
    def th(self):
        """ Get the second coordinate in this vector. """
        return self.__y

    @property
    def phi(self):
        """ Get the third coordinate in this vector. """
        return self.__z
    @property
    def tuple(self):
        """ Return the vector as a tuple. """
        return self.x, self.y, self.z

    @property
    def pygame(self, dims=('x','y')):
        """ Return the vector as a tuple of integers.  This is the format
        Pygame expects to receive coordinates in. """
        if 'x' in dims and 'y' in dims:
            return int(self.x), int(self.y)
        elif 'x' in dims and 'z' in dims:
            return int(self.x), int(self.z)
        elif 'y' in dims and 'z' in dims:
            return int(self.y), int(self.z)

    @property
    def magnitude(self):
        """ Calculate the length of this vector. """
        return math.sqrt(self.magnitude_squared)

    @property
    def magnitude_squared(self):
        """ Calculate the square of the length of this vector.  This is
        slightly more efficient that finding the real length. """
        return self.x**2 + self.y**2 + self.z**2

    @property
    def normal(self):
        """ Return a unit vector pointing in the same direction as this
        one. """

        try:
            return self / self.magnitude
        except ZeroDivisionError:
            raise NullVectorError()

    
    #def strip_z(self):

    def get_x(self):
        return self.x

    def get_y(self):
        return self.y

    def get_z(self):
        return self.z

    def get_r(self):
        return self.r

    def get_th(self):
        return self.th

    def get_phi(self):
        return self.phi

    def get_tuple(self):
        return self.tuple

    def get_pygame(self, dims=('x','y')):
        return self.pygame(dims)(dims)

    def get_magnitude(self):
        return self.magnitude

    def get_magnitude_squared(self):
        return self.magnitude_squared

    def get_normal(self, magnitude=1):
        return magnitude * self.normal

    #def get_components(self, v):
    #    """ Break this vector into one vector that is parallel to the given
    #    vector and another that is perpendicular to it. """
    #    tangent = v * Vector3D.dot(self, v)
    #    normal = self - tangent
    #    return normal, tangent

    # }}}1

class NullVectorError(Exception):
    """ Thrown when an operation chokes on a null vector. """
    pass
