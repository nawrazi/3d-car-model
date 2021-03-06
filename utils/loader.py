import pygame
from OpenGL.GL import *

class Loader:
    """
    A class that loads the car model and applies a skin to it.

    PARAMETERS
    ----------
    filename : string
        The relative location of the object to be loaded.
    color : int
        The color of the skin to be applied to the object.

    METHODS
    -------
    loadObject(filename)
        Reads the file passed to it and organizes the class property data structures based on the wavefront format.
    loadSkin(color : int)
        Loads a skin based on the specified color and organizes it into the appropriate data structure.
    generate()
        Creates the 3D mesh ready to be rendered. Applies the loaded skin to the object and stores the generated 3D
        object in the appropriate data structure ready to be rendered.
    """
    def __init__(self, filename, color):
        if not 0 <= color <= 6:
            raise Exception(f"Invalid color selection: {color}")

        self.vertices = []
        self.normals = []
        self.textures = []
        self.faces = []
        self.gl_list = 0
        self.texture_id = None

        self.loadObject(filename)
        self.loadSkin(color)
        self.generate()

    def loadObject(self, filename):
        for line in open(filename):
            values = line.split()
            if not values:
                continue
            tag = values[0]

            if tag == 'v':
                v = list(map(float, values[1:4]))
                v[1], v[2] = v[2], v[1]
                self.vertices.append(v)

            elif tag == 'vn':
                v = list(map(float, values[1:4]))
                v[1], v[2] = v[2], v[1]
                self.normals.append(v)

            elif tag == 'vt':
                self.textures.append(list(map(float, values[1:3])))

            elif tag == 'f':
                faces, textures, norms = [], [], []
                for v in values[1:]:
                    w = v.split('/')
                    faces.append(int(w[0]))
                    if len(w) >= 2 and len(w[1]) > 0:
                        textures.append(int(w[1]))
                    else:
                        textures.append(0)
                    if len(w) >= 3 and len(w[2]) > 0:
                        norms.append(int(w[2]))
                    else:
                        norms.append(0)

                self.faces.append((faces, norms, textures))

    def loadSkin(self, color):
        surface = pygame.image.load(f'assets/skins/skin{color}.BMP')
        image = pygame.image.tostring(surface, 'RGBA', True)
        ix, iy = surface.get_rect().size
        texture_id = glGenTextures(1)

        glBindTexture(GL_TEXTURE_2D, texture_id)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
        glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, ix, iy, 0, GL_RGBA, GL_UNSIGNED_BYTE, image)

        self.texture_id = texture_id

    def generate(self):
        self.gl_list = glGenLists(1)
        glNewList(self.gl_list, GL_COMPILE)
        glEnable(GL_TEXTURE_2D)
        glFrontFace(GL_CCW)

        for vertices, normals, textures in self.faces:
            glBindTexture(GL_TEXTURE_2D, self.texture_id)
            glBegin(GL_POLYGON)

            for i in range(len(vertices)):
                if normals[i] > 0:
                    glNormal3fv(self.normals[normals[i] - 1])
                if textures[i] > 0:
                    glTexCoord2fv(self.textures[textures[i] - 1])
                glVertex3fv(self.vertices[vertices[i] - 1])

            glEnd()

        glDisable(GL_TEXTURE_2D)
        glEndList()
