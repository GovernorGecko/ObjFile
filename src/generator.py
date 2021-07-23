"""
    obj generator

    Order of faces position/texcoord/normal

    Ka: specifies ambient color, to account for light that is scattered about the entire scene [see Wikipedia entry for Phong Reflection Model] using values between 0 and 1 for the RGB components.
Kd: specifies diffuse color, which typically contributes most of the color to an object [see Wikipedia entry for Diffuse Reflection]. In this example, Kd represents a grey color, which will get modified by a colored texture map specified in the map_Kd statement
Ks: specifies specular color, the color seen where the surface is shiny and mirror-like [see Wikipedia entry for Specular Reflection].
Ns: defines the focus of specular highlights in the material. Ns values normally range from 0 to 1000, with a high value resulting in a tight, concentrated highlight.
Ni: defines the optical density (aka index of refraction) in the current material. The values can range from 0.001 to 10. A value of 1.0 means that light does not bend as it passes through an object.
d: specifies a factor for dissolve, how much this material dissolves into the background. A factor of 1.0 is fully opaque. A factor of 0.0 is completely transparent.
illum: specifies an illumination model, using a numeric value. See Notes below for more detail on the illum keyword. The value 0 represents the simplest illumination model, relying on the Kd for the material modified by a texture map specified in a map_Kd statement if present. The compilers of this resource believe that the choice of illumination model is irrelevant for 3D printing use and is ignored on import by some software applications. For example, the MTL Loader in the threejs Javascript library appears to ignore illum statements. Comments welcome.
map_Kd: specifies a color texture file to be applied to the diffuse reflectivity of the material. During rendering, map_Kd values are multiplied by the Kd values to derive the RGB components.

"""

import os
from shutil import copyfile

from .MultiD.src.vector import Vector2, Vector3
from .MultiD.src.triangle import Triangle


class Generator():
    """
    parameters:
        (required)
        string name of the Generator, used for saving.
        (optional)
        string path to image to use for texcoords
        string name of the image to use for texcoords
        bool of whether we should include Normals
        bool of whether we should include TexCoords
    """

    __slots__ = [
        "__name", "__normals", "__texcoords",
        "__image_path", "__image_name",
        "__ka", "__kd", "__ks", "__illum", "__ns", "__ni", "__d",
        "__faces", "__v", "__vn", "__vt"
        ]

    def __init__(
        self, name, image_path="./", image_name=None,
        normals=True, texcoords=False
    ):

        if not isinstance(name, str):
            raise ValueError("Name must be a string.")
        elif (
            image_name is not None and
            not isinstance(image_name, str)
        ):
            raise ValueError("Image Name must be a string.")
        elif (
            not isinstance(image_path, str) or
            not os.path.exists(image_path)
        ):
            raise ValueError("Image Path must exist.")
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

        # Store Image
        self.__image_name = image_name
        self.__image_path = image_path

        # Set Material Defaults
        self.__ka = Vector3(0.0, 0.2, 0.0)
        self.__kd = Vector3(0.0, 0.8, 0.0)
        self.__ks = Vector3(1.0, 1.0, 1.0)
        self.__ns = 1.0
        self.__ni = 1.0
        self.__d = 1.0
        self.__illum = 1

        # Store Normals/TexCoords options.
        self.__normals = normals
        self.__texcoords = texcoords

    def __str__(self):
        """
        returns:
            string representing our obj data.
        """

        return (
            f"{self.get_obj_as_string()}\n\n"
            f"{self.get_mtl_as_string()}"
        )

    def add_triangle(self, positions, texcoords=None):
        """
        parameters:
            (required)
            List[List[Float, Float, Float]] for Positions
            (optional)
            List[List[Float, Float]] for Texcoords
        """

        # Create a Triangle
        triangle = Triangle(positions, texcoords=texcoords)

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
                        triangle.get_texcoords()[i],
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

    def get_mtl_as_string(self):
        """
        returns
            string representing our Mtl
        """

        # We have an image name?
        if self.__image_name is None:
            return ""

        """
        Ka 0.0000 0.2000 0.0000
Kd 0.0000 0.8000 0.0000
illum 1
map_Ka brazil_logo.gif
map_Kd brazil_logo.gif
        """
        # Base mtl
        mtl_as_string = "newmtl material0\n"

        # Ambience
        mtl_as_string += "Ka " + " ".join(
            map(str, self.__ka.get_list())
        ) + "\n"

        # Diffuse
        mtl_as_string += "Kd " + " ".join(
            map(str, self.__kd.get_list())
        ) + "\n"

        """
        # Specular
        mtl_as_string += "Ks " + " ".join(
            map(str, self.__ks.get_list())
        ) + "\n"

        # Return!
        return (
            f"{mtl_as_string}"
            f"Ns {self.__ns}\n"
            f"Ni {self.__ni}\n"
            f"d {self.__d}\n"
            f"illum {self.__illum}\n"            
            f"map_Kd {self.__image_name}"
        )
        """

        # Return!
        return (
            f"{mtl_as_string}"
            f"illum {self.__illum}\n"            
            f"map_Ka {self.__image_name}\n"
            f"map_Kd {self.__image_name}"
        )

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
            obj_as_string += "\nvt " + "\nvt ".join(
                " ".join(map(str, vt.get_list())) for vt in self.__vt
             )

        # Normals
        if self.__normals:
            obj_as_string += "\nvn " + "\nvn ".join(
                " ".join(map(str, vn.get_list())) for vn in self.__vn
            )

        # Add Material
        obj_as_string += "\n\n"
        if self.__image_name is not None:
            obj_as_string += "usemtl material0"
        else:
            obj_as_string += "usemtl Default"
        obj_as_string += "\n"

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
        with open(os.path.join(path, self.__name + ".obj"), "w") as file:
            file.writelines(self.get_obj_as_string())

        # Have an image?
        if self.__image_name is not None:

            # Copy the image to our path.
            copyfile(
                os.path.join(
                    self.__image_path,
                    self.__image_name
                ),
                os.path.join(
                    path,
                    self.__image_name
                )
            )

            # Create the mtl file
            with open(os.path.join(path, self.__name + ".mtl"), "w") as file:
                file.writelines(self.get_mtl_as_string())
