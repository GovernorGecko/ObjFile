"""
    _test
"""

from src.generator import Generator
from src.MultiD.src.triangle import Triangle
from src.MultiD.src.vector import Vector3

g = Generator("test")

t = Triangle(
    [
        Vector3(1.0, 1.0, 1.0),
        Vector3(1.0, 1.0, 0.9),
        Vector3(0.0, 1.0, 1.0)
    ]
)

g.add_triangle(t)

print(g)
