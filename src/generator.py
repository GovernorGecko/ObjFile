"""
    obj generator

    Order of faces position/texcoord/normal
"""

import os

from .MultiD.src.vector import Vector2, Vector3
from .MultiD.src.triangle import Triangle


class Generator():
    """
    parameters:
        (required)
        string name of the Generator, used for saving.
        (optional)
        bool of whether we should include Normals
        bool of whether we should include TexCoords
    """

    __slots__ = [
        "__name", "__colors", "__normals", "__texcoords",
        "__faces", "__v", "__vn", "__vt"
        ]

    def __init__(self, name, normals=True, texcoords=False):

        if not isinstance(name, str):
            raise ValueError("Name must be a string.")
        elif (
            not isinstance(normals, bool) or
            not isinstance(texcoords, bool)
        ):
            raise ValueError("Normals and TexCoords must be bool.")

        # Name is used for storing the obj/mtl files
        self.__name = name

        # Face/Vertex Defaults
        self.__faces = []
        self.__v = []
        self.__vn = []
        self.__vt = []

        # Store Normals/TexCoords options.
        self.__normals = normals
        self.__texcoords = texcoords

    def __str__(self):
        """
        returns:
            string representing our obj data.
        """

        return self.get_obj_as_string()

    def add_triangle(self, triangle):
        """
        parameters:
            Triangle
        """

        if not isinstance(triangle, Triangle):
            raise ValueError("Triangle must be of type Triangle")

        # Face Data to add to our faces
        face_data = []

        # Triangles are made up of three pieces ofvertex data
        for i in range(0, 3):

            # List of Vertexes to Face Indexes
            vertex_face_indexes = []

            # Positions
            vertex_face_indexes.append(
                self.__get_vertex_face_data(
                    triangle.get_positions()[i],
                    self.__v
                )
            )

            # TexCoords
            if self.__texcoords:
                vertex_face_indexes.append(
                    self.__get_vertex_face_data(
                        triangle.get_texcoords(),
                        self.__vt
                    )
                )
            else:
                vertex_face_indexes.append('')

            # Normals
            if self.__normals:
                vertex_face_indexes.append(
                    self.__get_vertex_face_data(
                        triangle.get_normals(),
                        self.__vn
                    )
                )
            else:
                vertex_face_indexes.append('')

            # Add to Face Data
            face_data.append(vertex_face_indexes)

        # Add to Faces
        self.__faces.append(face_data)

    def __get_vertex_face_data(self, vertex_data, vertex_list):
        """
        parameters:
            Vector2 or Vector3
            List of Vector2s or Vector3s
        returns:
            int of which face this Vector2 or Vector3 is at.
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
        return face_data + 1

    def get_obj_as_string(self):
        """
        returns:
            string representing our Obj.
        """

        # Base Obj
        obj_as_string = (
            f"o {self.__name}\n"
        )

        # Positions
        obj_as_string += "\nv " + "\nv ".join(
            " ".join(map(str, v.get_list())) for v in self.__v
        )

        # TexCoords?
        if self.__texcoords:
            obj_as_string += "\nvt" + "\nvt ".join(
                " ".join(map(str, vt.get_list())) for vt in self.__vt
             )

        # Normals
        if self.__normals:
            obj_as_string += "\nvn " + "\nvn ".join(
                " ".join(map(str, vn.get_list())) for vn in self.__vn
            )

        # Add Material
        obj_as_string += "\n\nusemtl Default\n"

        # Iterate Faces
        obj_as_string += "f " + "\nf ".join(
            [" ".join(
                ["/".join(map(str, k)) for k in j]
            ) for j in self.__faces]
        )

        # Return
        return obj_as_string

    def save(self, path):
        """
        parameters:
            string path to store the obj file.
        """

        # String and path exists?
        if (
            not isinstance(path, str) or
            not os.path.exists(path)
        ):
            raise ValueError(f"{path} doesn't exist!")

        # File Path
        file_path = open(os.path.join(path, self.__name + ".obj"), "w")

        # Write our data!
        file_path.writelines(self.get_obj_as_string())

        # Close  it!
        file_path.close()
