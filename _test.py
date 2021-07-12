"""
    _test
"""

from src.generator import Generator
from src.MultiD.src.triangle import Triangle
from src.MultiD.src.vector import Vector3

g = Generator("test")

t1 = Triangle(
    [
        Vector3(1.0, 1.0, 1.0),
        Vector3(1.0, 1.0, 0.0),
        Vector3(0.0, 1.0, 1.0)
    ]
)

t2 = Triangle(
    [
        Vector3(1.0, 1.0, 1.0),
        Vector3(1.0, 1.0, 0.0),
        Vector3(0.0, 1.0, 0.0)
    ]
)

g.add_triangle(t1)
g.add_triangle(t2)

print(g)
