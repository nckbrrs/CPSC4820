### Sarah Thompson
### February, 2017
#########################################
#04 - knob_API
#tangible knob API - object rotation
#########################################
from kivy.config import Config
 
import sys
import os
sys.path.append(os.getcwd() + "/lib/garden.tei_knob/")

width = 4500/2
height = 3000/2 - 300
Config.set('graphics', 'borderless', 1)
Config.set('graphics', 'window_state', 'visible')
Config.set('graphics', 'resizable', 0)
Config.set('graphics', 'position', 'custom')
Config.set('graphics', 'left', 0)             
Config.set('graphics', 'top', 0)
Config.set('graphics', 'width', width) #alas, must be called before other imports
Config.set('graphics', 'height', height) #1440http://kivy.org/docs/api-kivy.config.html

import kivy
from kivy.app import App
from kivy.properties     import *
from kivy.uix.gridlayout import GridLayout
from kivy.uix.relativelayout import RelativeLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.widget     import Widget
from kivy.uix.scatter    import Scatter
from kivy.uix.image      import Image
from kivy.core.window   import Window #Sarah
from kivy.animation     import * # Sarah
from kivy.uix.label     import Label #Sarah

from tei_knob import Knob

# Import kivy osc library
from kivy.lib.osc         import oscAPI 
# Import clock (required by osc listener)
from kivy.clock           import Clock

class ReceiverApp(App):
    # Set ip and port to listen to
    ip = '0.0.0.0' # listens to any sender IP
    port = 5000    # listens only to this port

    currImg = 0
    prevAngle1 = 0
    prevAngle2 = 0
    getBig = 0

    def __init__(self, *args, **kwargs):
        super(ReceiverApp, self).__init__(*args, **kwargs)
        self._keyboard = Window.request_keyboard(self._keyboard_closed, self)
        self._keyboard.bind(on_key_down=self._on_keyboard_down)

    def build(self):
        # Starts OSC
        oscAPI.init()  
        # Instanciates OSC listener
        oscid = oscAPI.listen(ipAddr=self.ip, port= self.port) 
        # listens for osc messages every screen refresh
        Clock.schedule_interval(lambda *x: oscAPI.readQueue(oscid), 0)

        # binds messages - this listens to messages if prefix /1/tok
        oscAPI.bind(oscid, self.cb_tok, '/tuios/tok')

        # creates a grid layout with two columns
    	#root = GridLayout(cols = 3, spacing = 50, padding = 30)

        # Sarah -------------
        root = FloatLayout(pos = (0, 0))
        self.background = Image(source='img/cool-background.jpg', 
            size_hint = (1, 1), 
            allow_stretch = True,
            keep_ratio = False)

        # Defining colors
        # use a (r, g, b, a) tuple (a = alpha channel = tranparency)
        self.grey = (0.5, 0.5, 0.5, 1)
        self.black = (0, 0, 0, 1)

        # Creates an image widget
        self.image1 = Image(source='brain/frame_0_delay-0.1s.gif', size = (800,800), allow_stretch = True,
            keep_ratio = True)

        # instantiate a label
        self.label1 =  Label(text="3-D Brain Model", font_size=200, color=self.black, pos=(Window.width/2, Window.height-200))
        self.label1Wid = Widget(pos = (Window.width/2, Window.height-100))
        self.label1Wid.add_widget(self.label1)

        self.label2 =  Label(text="Rotate X", font_size=50, bold = True, color=self.grey, pos=(Window.width-800, 0))
        self.label2Wid = Widget(pos = (0, 0))
        self.label2Wid.add_widget(self.label2)

        self.label3 =  Label(text="Rotate Y", font_size=50, bold = True, color=self.grey, pos=(Window.width-500, 0))
        self.label3Wid = Widget(pos = (0, 0))
        self.label3Wid.add_widget(self.label3)

        self.label4 =  Label(text="Zoom", font_size=50, bold = True, color=self.grey, pos=(Window.width-200, 0))
        self.label4Wid = Widget(pos = (0, 0))
        self.label4Wid.add_widget(self.label4)

        self.label5 =  Label(text="LOADING IMAGES", bold = True, font_size=50, color=self.black, pos=(Window.width/2, Window.height-600))
        self.label5Wid = Widget(pos = (Window.width/2, Window.height-100))
        self.label5Wid.add_widget(self.label5)

        self.wid = Widget()
        # Creates a scatter widget
        self.scatter1 = Scatter(size=(800, 800), pos= (720,200))

        # Adds image widget to the scatter
        self.scatter1.add_widget(self.image1)
        self.wid.add_widget(self.scatter1)

        # add label1 widget to the box layout 
        root.add_widget(self.background)
        root.add_widget(self.label1Wid)
        root.add_widget(self.label2Wid)
        root.add_widget(self.label3Wid)
        root.add_widget(self.label4Wid)
        
        # Adds scatter to the layout
        root.add_widget(self.wid)
        root.add_widget(self.label5Wid)

        self.fadeIn() # Fade in image1 and labels

        return root

    #OSC callback function
    def cb_tok(self, value, instance): 
        # print message received to console
        print "Message received: " + str(value)

        if value[2] == 1:
            try:
                self.scatter1.rotation = int(value[7])
            except:
                pass
        # Sarah 
        elif value[2] == 2: # rotoates the brain in the 3rd dimension
            try:
                if value[7] > self.prevAngle1:
                    self.moveRight() 
                    print "right"
                    print value[7]
                    print self.prevAngle1
                else:
                    self.moveLeft()
            except:
                pass

        elif value[2] == 3: 
            try:
                if float(value[7]) > 350:
                    self.getBig = 0
                elif float(value[7]) < 7:
                    self.getBig = 1

                if self.getBig == 1:
                    self.scatter1.scale = (float(value[7]) /60) + 0.01
                else:
                    self.scatter1.scale = (float(value[7])/60) + 0.01
            except:
                self.scatter1.scale = 1
        self.prevAngle1 = value[7]

    def moveRight(self):
        self.currImg -=1
        if self.currImg < 0:
            self.currImg = 150
        print self.image1.source
        # add or subtract the wrap-around so value != -1
        self.image1.source = 'brain/frame_'+str(self.currImg)+'_delay-0.1s.gif'

    def moveLeft(self):
        self.currImg +=1
        if self.currImg > 150:
            self.currImg = 0
        print self.image1.source
        self.image1.source = 'brain/frame_'+str(self.currImg)+'_delay-0.1s.gif'

    def _keyboard_closed(self):
        pass

    # when left or right arrows are pressed down, switch images for Rotation 2
    def _on_keyboard_down(self, keyboard, keycode, text, modifiers):
        print keycode[1]
        if keycode[1] == "right" : 
             self.moveRight()
        elif keycode[1] == "left":
             self.moveLeft()
        elif keycode[1] == "s" :
            self.loadImages()

    # Fades the image and labels onto the screen when they first appear
    def fadeIn(self):
        # Fade for label1
        self.label1.opacity=0 
        self.fade = Animation(opacity=1, duration=2)
        self.fade.start(self.label1)

        # Fade for label2
        self.label2.opacity=0
        self.fade = Animation(opacity=1, duration=2)
        self.fade.start(self.label2)

        # Fade for label3
        self.label3.opacity=0
        self.fade = Animation(opacity=1, duration=2)
        self.fade.start(self.label3)

        # Fade for label4
        self.label4.opacity=0
        self.fade = Animation(opacity=1, duration=2)
        self.fade.start(self.label4)

        # Fade for image1
        self.image1.opacity=0
        self.fade = Animation(opacity=1, duration=2)
        self.fade.start(self.image1)

    def loadImages(self):

        loader = 0
        for loader in range (0, 150):
            self.image1.source = 'brain/frame_'+str(loader)+'_delay-0.1s.gif'
            print loader
        # Fade for label5
        self.fade = Animation(opacity=0, duration=1)
        self.fade.start(self.label5)
        self.image1.source = 'brain/frame_'+str(0)+'_delay-0.1s.gif'

ReceiverApp().run()