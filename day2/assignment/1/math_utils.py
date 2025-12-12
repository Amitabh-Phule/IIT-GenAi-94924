"""
math_utils.py
A math utility module for calculating areas of different shapes.
"""

import math


def area_circle(radius: float) -> float:
    if radius < 0:
        raise ValueError("Radius cannot be negative.")
    return math.pi * (radius ** 2)


def area_rectangle(length: float, width: float) -> float:
    if length < 0 or width < 0:
        raise ValueError("Length and width cannot be negative.")
    return length * width


def area_triangle(base: float, height: float) -> float:
    if base < 0 or height < 0:
        raise ValueError("Base and height cannot be negative.")
    return 0.5 * base * height


def area_square(side: float) -> float:
    if side < 0:
        raise ValueError("Side cannot be negative.")
    return side ** 2
