from kivy.core.window import Window
import sys

from ui import UI

from kivy.lib.osc import oscAPI
from kivy.clock import Clock

class Controller():
    def __init__(self, **kwargs):
        self.ip = "127.0.0.1"
        self.sendPort = 5001
        self.recvPort = 5002

        self.renderer = kwargs['renderer']

        self._touches = []

        oscAPI.init()  
        dialOSC = oscAPI.listen(ipAddr=self.ip, port=5000) 
        Clock.schedule_interval(lambda *x: oscAPI.readQueue(dialOSC), 0)
        oscAPI.bind(dialOSC, self.dialListener, '/tuios/tok')

    #    recvOSC = oscAPI.listen(ipAddr=self.ip, port= self.recvPort) 
    #    Clock.schedule_interval(lambda *x: oscAPI.readQueue(recvOSC), 0)
    #    oscAPI.bind(recvOSC, self.receive, '/tuios/tok')

    #def _keyboard_closed(self):
     #   self._keyboard.unbind(on_key_down=self._on_keyboard_down)
      #  self._keyboard = None

    #def _on_keyboard_down(self, keyboard, keycode, text, modifiers):
     #   if keycode[1] == 'left':
     #       self.rotate(-5,0)
     #   elif keycode[1] == 'right':
     #       self.rotate(5,0)
     #   if keycode[1] == 'up':
     #       self.rotate(0,-5)
     #   elif keycode[1] == 'down':
     #       self.rotate(0,5)
     #   elif keycode[1] == 'n':
     #       self.setRotation(0,0)
     #   elif keycode[1] == 'escape':
     #       sys.exit()
     #   elif keycode[1] == '.':
     #       self.zoom(-0.1)
     #   elif keycode[1] == ',':
     #       self.zoom(0.1)

     #   return True     

    def send(self):
        x = self.renderer.rotx.angle
        y = self.renderer.roty.angle
        z = self.renderer.camera_translate[2]
        print "sending:", x, y, z

        oscAPI.sendMsg('/tuios/tok', [x,y,z], 
                                    ipAddr= self.ip, 
                                    port= self.sendPort) 

    def receive(self, value, instance):
        x = value[2]
        y = value[3]
        z = value[4]

        self.renderer.rotx.angle = x
        self.renderer.roty.angle = y
        self.renderer.camera_translate[2] = z

    def rotate(self, rotX, rotY):
        self.renderer.rotx.angle += rotX
        self.renderer.roty.angle += rotY
        self.send()

    def setRotationX(self, x):
        self.renderer.rotx.angle = x
        self.send()

    def setRotationY(self, y):
        self.renderer.roty.angle = y
        self.send()

    def setRotation(self, x, y):
        self.renderer.rotx.angle = x
        self.renderer.roty.angle = y
        self.send()

    def zoom(self, zoom):
        print self.renderer.camera_translate
        if (self.renderer.camera_translate[2] + zoom < 30 and 
                self.renderer.camera_translate[2] + zoom > 0):
            self.renderer.camera_translate[2] += zoom

            self.send()

    def setZoom(self, zoom):
        self.renderer.camera_translate[2] = zoom

        self.send()

    def setSlide(self, slide):
	print "sending:", slide, "\n\n\n\n\n\n\n\n"

        oscAPI.sendMsg('/tuios/tok', [slide], 
                                    ipAddr= self.ip, 
                                    port= 5003)

    def dialListener(self, value, instance):
        print ("value", value, "instance:", instance)
        knob = value[2]
        try:
            angle = float(value[7])
        except:
            angle = 1
        if (knob == 1):
            self.setRotationX(angle)
        elif (knob == 2):
            self.setRotationY(angle)
        elif (knob == 3):
            self.setZoom(angle/360 * 30)
        elif (knob == 4):
            self.setSlide(angle)
