"""
    _test
"""

from src.generator import Generator
from src.MultiD.src.plane import Plane
# from src.MultiD.src.triangle import Triangle
from src.MultiD.src.vector import Vector2

# Plane Test
g = Generator("test", image_name="test.jpg")

p = Plane(
    1.0,
    None,
    texcoords=[
        Vector2(1.0, 0.0),
        Vector2(0.0, 0.0),
        Vector2(0.0, 1.0),
        Vector2(1.0, 1.0),
    ]
)

for t in p.get_triangles(
    roll=90.0,
):
    g.add_triangle(
        t.get_positions(),
        t.get_texcoords(),
    )

# print(p)
g.save("tests")

"""
g = Generator("test", image_name="test.jpg")

t1 = Triangle(
    [
        Vector3(1.0, 0.0, 0.0),
        Vector3(0.0, 0.0, 0.0),
        Vector3(0.0, 0.0, 1.0),
    ],
    texcoords=[
        Vector2(1.0, 0.0),
        Vector2(0.0, 0.0),
        Vector2(0.0, 1.0),
    ]
)

t2 = Triangle(
    [
        Vector3(0.0, 0.0, 1.0),
        Vector3(1.0, 0.0, 1.0),
        Vector3(1.0, 0.0, 0.0),
    ],
    texcoords=[
        Vector2(0.0, 1.0),
        Vector2(1.0, 1.0),
        Vector2(1.0, 0.0),
    ]
)


g.add_triangle(t1.get_positions(), t1.get_texcoords())
g.add_triangle(t2.get_positions(), t2.get_texcoords())

# print(g)
g.save("tests")

"""
