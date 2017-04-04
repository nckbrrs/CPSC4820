from kivy.config import Config
#from win32api import GetSystemMetrics
#width = GetSystemMetrics(0)
#height = GetSystemMetrics(1)
width = 1280
height = 700

import math
from kivy.core.window import Window
from kivy.resources import resource_find
from kivy.graphics.transformation import Matrix
from kivy.graphics.opengl import *
from kivy.graphics.gl_instructions import ClearBuffers
from kivy.graphics import *
from NEWobjloader import ObjFileLoader
from kivy.uix.widget import Widget
from kivy.graphics.fbo import Fbo
from kivy.properties import ObjectProperty

class Renderer(Widget):
    
    texture = ObjectProperty(None, allownone=True)    
    
    def __init__(self, **kwargs):
        self.canvas = Canvas()
        self.scene = ObjFileLoader(resource_find("brain.obj"))
        
        self.meshes = []
        
        with self.canvas:
            self.fbo = Fbo(size=self.size, with_depthbuffer=True, compute_normal_mat=True, clear_color=(0., 0., 0., 0.))
            self.viewport = Rectangle(size=self.size, pos=self.pos)
            self.fbo.shader.source = resource_find('simple.glsl')
        

        super(Renderer, self).__init__(**kwargs)

        with self.fbo:
            self.cb = Callback(self.setup_gl_context)
            PushMatrix()
            self.setup_scene()
            PopMatrix()
            self.cb = Callback(self.reset_gl_context)
        
    def on_size(self, instance, value):
        self.fbo.size = value
        self.viewport.texture = self.fbo.texture
        self.viewport.size = self.size
	self.viewport.pos = (0,0)
        self.update_glsl()


    def setup_gl_context(self, *args):
        glEnable(GL_DEPTH_TEST)
        self.fbo.clear_buffer()

    def reset_gl_context(self, *args):
        glDisable(GL_DEPTH_TEST)
        

    def update_glsl(self, *largs):
        asp = self.width / float(self.height)
        proj = Matrix().view_clip(-asp, asp, -1, 1, 1, 100, 1)
        self.fbo['projection_mat'] = proj

    def setup_scene(self):
        Color(1, 1, 1, 0)

        PushMatrix()
        Translate(0, 0, -10)
        # This Kivy native Rotation is used just for
        # enabling rotation scene like trackball
        self.rotx = Rotate(0, 1, 0, 0)
        self.roty = Rotate(0, 0, 1, 0) # here just rotate scene for best view
        self.scale = Scale(1)
                
        UpdateNormalMatrix()
        
        self.draw_elements()
        
        PopMatrix()

    def draw_elements(self):
        """ Draw separately all objects on the scene
            to setup separate rotation for each object
        """
        def _draw_element(m):
            Mesh(
                vertices=m.vertices,
                indices=m.indices,
                fmt=m.vertex_format,
                mode='triangles',
            )
            
        def _set_color(*color, **kw):
            id_color = kw.pop('id_color', (0, 0, 0))
            return ChangeState(
                        Kd=color,
                        Ka=color,
                        Ks=(.3, .3, .3),
                        Tr=1., Ns=1.,
                        intensity=1.,
                        id_color=[i / 255. for i in id_color],
                    )
            
        # Draw sphere in the center
        brain = self.scene.objects['Brain']
        _set_color(.659,.439,.361, id_color=(0, 0, 0))
        _draw_element(brain)

        brain2 = self.scene.objects['Brain2']
        _set_color(.659,.439,.361, id_color=(0, 0, 0))
        _draw_element(brain2)
