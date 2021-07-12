"""
    obj generator
"""

from .MultiD.src.vector import Vector2, Vector3
from .MultiD.src.triangle import Triangle


class Generator():

    __slots__ = [
        "__name", "__colors", "__normals", "__texcoords",
        "__faces", "__v", "__vc", "__vn", "__vt"
        ]

    def __init__(self, name, normals=True, colors=False, texcoords=False):

        if not isinstance(name, str):
            raise ValueError("Name must be a string.")
        elif (
            not isinstance(normals, bool) or
            not isinstance(colors, bool) or
            not isinstance(texcoords, bool)
        ):
            raise ValueError("Normals, Colors, TexCoords must be bool.")

        # Name is used for storing the obj/mtl files
        self.__name = name

        # Face/Vertex Defaults
        self.__faces = []
        self.__v = []
        self.__vc = []
        self.__vn = []
        self.__vt = []

        # Store Normals/Colors/TexCoords options.
        self.__colors = colors
        self.__normals = normals
        self.__texcoords = texcoords

    def __str__(self):
        """
        """

        return self.get_obj_data()

    def add_triangle(self, triangle):
        """
        """

        if not isinstance(triangle, Triangle):
            raise ValueError("Triangle must be of type Triangle")

        # Triangles are made up of three pieces of vertex data
        for i in range(0, 3):

            face_data = []

            # Positions
            face_data.append(
                self.__add_vertex_data(
                    triangle.get_positions()[i],
                    self.__v
                )
            )

            # Normals
            if self.__normals:
                face_data.append(
                    self.__add_vertex_data(
                        triangle.get_normals(),
                        self.__vn
                    )
                )

            # Colors
            
            # TexCoords

            # Add to Faces
            self.__faces.append(face_data)

    def __add_vertex_data(self, vertex_data, vertex_list):
        """
        """

        if not isinstance(vertex_data, (Vector3, Vector2)):
            raise ValueError("Vertex Data must be a Vector3 or Vector2.")
        elif not isinstance(vertex_list, list):
            raise ValueError("Vertex List must be a list.")

        face_data = None
        if vertex_data in vertex_list:
            face_data = vertex_list.index(vertex_data)
        else:
            face_data = len(vertex_list)
            vertex_list.append(vertex_data)
        return face_data

    def get_obj_data(self):
        """
        """

        return (
            f"o {self.__name}\n"
            f"\n"
            f"# Vertex list\n"
            f"{self.__faces}"
            f"{self.__v}"
            f"{self.__vn}"
        )
