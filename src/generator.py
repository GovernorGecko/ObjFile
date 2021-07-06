"""
    obj generator
"""

from .MultiD.src.triangle import Triangle


class Generator():

    __slots__ = ["__faces", "__name", "__positions"]

    def __init__(self, name, normals=True, colors=False, texcoords=False):

        if not isinstance(name, str):
            raise ValueError("Name must be a string.")

        self.__faces = []
        self.__name = name
        self.__positions = []

    def __str__(self):
        """
        """

        return (
            f"o {self.__name}\n"
            f"\n"
            f"# Vertex list\n"
        )

    def add_triangle(self, triangle):
        """
        """

        if not isinstance(triangle, Triangle):
            raise ValueError("Triangle must be of type Triangle")

    def add_vertex_data(self, vertex_data):
        """
        """
        