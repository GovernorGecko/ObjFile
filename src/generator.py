"""
    obj generator
"""

from .MultiD.src.triangle import Triangle


class Generator():

    __slots__ = [
        "__faces", "__name", "__normals", "__positions",
        "__render_colors", "__render_normals", "__render_texcoords"
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

        self.__faces = []
        self.__name = name
        self.__normals = []
        self.__positions = []
        self.__render_colors = colors
        self.__render_normals = normals
        self.__render_texcoords = texcoords

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

        # Set up our Face Data
        face_data = []
        for p in triangle.__positions:
            if p in self.__positions:
                face_data.append(
                    self.__positions.index(p)
                )
            else:
                self.__positions.append(p)
                face_data.append(
                    len(face_data)
                )
        
        """
        self.__faces.append(len(self.__faces))
        triangle.__positions

        vertex_data = triangle.get_vertex_data(
            positions=True,
            normals=self.__render_normals,
            colors=self.__render_colors,
            texcoords=self.__render_texcoords
        )

        print(vertex_data)
        """
