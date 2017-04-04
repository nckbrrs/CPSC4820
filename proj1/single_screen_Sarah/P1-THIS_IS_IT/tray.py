from kivy.config import Config

import sys
import os
sys.path.append(os.getcwd() + "/lib/garden.tei_knob/")

width = 4500/2
height = 3000/2
Config.set('graphics', 'borderless', 1)
Config.set('graphics', 'window_state', 'visible')
Config.set('graphics', 'resizable', 0)
Config.set('graphics', 'position', 'custom')
Config.set('graphics', 'left', 0)             
Config.set('graphics', 'top', height - 300)
Config.set('graphics', 'width', width) #alas, must be called before other imports
Config.set('graphics', 'height', 300) #1440http://kivy.org/docs/api-kivy.config.html

import kivy
from kivy.app import App
from kivy.properties     import *
from kivy.uix.gridlayout import GridLayout
from kivy.uix.relativelayout import RelativeLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.widget     import Widget
from kivy.uix.scatter    import Scatter
from kivy.uix.image      import Image

from tei_knob import Knob

# Import kivy osc library
from kivy.lib.osc         import oscAPI

class MyKnob(Knob):

    #Set IP and port of receiver
    ip = '127.0.0.1' # Receiver ip
    port = 5000      # Receiver port

    #string with knob name
    knob_id = ObjectProperty('')
    #knob angle
    knob_angle = ObjectProperty()

    # Object property that receives the image
    obj = ObjectProperty()

    # on_knob is called if value, token_id or token_placed chage
    def on_knob(self, value, pattern_id):
        self.knob_angle = value
        # update the rotation of the scatter widget
        self.obj.rotation = self.knob_angle

        # Send OSC message
        ################################################
        # Simplified Tuio Message
        # s   Session ID (temporary object ID)    int32 - knob_id
        # i   Class ID (e.g. marker ID)           int32 - pattern_id
        # x, y, z Position                      float32 - knob position
        # a   Angle                             float32 - knob angle
        # p   Free parameter                            - token_placed

        s = self.knob_id
        i = self.pattern_id
        x = self.token_pos[0]
        y = self.token_pos[1]
        z = 0
        a = int(self.knob_angle)
        p = str(True) #Token placed


        oscAPI.sendMsg('/tuios/tok', [s,i,x,y,z,a,p], 
                                    ipAddr= self.ip, 
                                    port= self.port) 

    # on_value is called when the angle is updated
    def on_value(self, instance, value):
        #print "token value: " + str(value)
        pass

     # on_pattern_id is called when the id is updated
    def on_pattern_id(self, instance, value):
        #print "token id: " + str(value)
        pass

    def on_token_placed(self, instance, value):
        self.tk_placed = value
        print 'tray::on_token_placed: ' + 'knob_id: ' + str(self.knob_id) + \
                                  ' pattern_id: ' + str(self.pattern_id) + \
                                  ' token_pos: ' + str(self.token_pos) + \
                                  ' knob_angle: ' + str(self.knob_angle) + \
                                  ' token_placed: ' + str(self.tk_placed)
        # Send OSC message
        ################################################
        # Simplified Tuio Message
        # s   Session ID (temporary object ID)    int32 - knob_id
        # i   Class ID (e.g. marker ID)           int32 - pattern_id
        # x, y, z Position         float32, range 0...1 - knob position
        # a, b, c Angle           float32, range 0..2PI - knob angle
        # P   Free parameter                            - token_placed

        s = self.knob_id
        i = self.pattern_id
        x = self.token_pos[0]
        y = self.token_pos[1]
        z = 0
        a = self.knob_angle
        p = str(self.tk_placed) 

        oscAPI.sendMsg('/tuios/tok', [s,i,x,y,z,a,p], 
                                    ipAddr= self.ip, 
                                    port= self.port) 

        print 'tray::on_knob:sendOSCMsg ' + 'knob_id: ' + str(self.knob_id) + \
                                  ' pattern_id: ' + str(self.pattern_id) + \
                                  ' token_pos: ' + str(self.token_pos) + \
                                  ' knob_angle: ' + str(self.knob_angle) + \
                                  ' token_placed: ' + str(self.tk_placed)

class TeiKnobApp(App):
    tray_width = width
    banner_width = width - 3 * (300 + 10)

    def build(self):
        oscAPI.init()
        # creates a grid layout with two columns
        root = FloatLayout(size=(self.tray_width,300), pos = (0,0))

        # Creates an image widget for the root
        root_image = Image(source='img/cool-background.jpg', size_hint_x=None, width=self.tray_width,
                                              size_hint_y=None, height=300,
                                              allow_stretch = True,
                                              keep_ratio = False)
        root.add_widget(root_image)

        tray = GridLayout(cols = 4, spacing = 10, padding = 0)

        scatter = Scatter()
        # Creates a MyKnob object
        widgetA = RelativeLayout(size_hint = (None, None), 
                                 size = (300,300),
                                 pos = (0,0))


        knobA = MyKnob(size = (300, 300),
                         min = 0, max = 360,
                         step = 10,
                         show_marker = True,
                         knobimg_source = "img/knob_metal.png",
                         marker_img = "img/bline.png",
                         markeroff_color = (0.3, 0.3, .3, 1),
                         pattern_id= 99, #(ids 1 to 8, or 99 for no id)
                         debug = False,
                         obj = scatter, # Passes the object to the knob
                         knob_id = 001,
                         ms_dial = True)
        widgetA.add_widget(knobA)

        # Creates a MyKnob object
        widgetB = RelativeLayout(size_hint = (None, None), 
                                 size = (300,300),
                                 pos = (0,0))

        knobB = MyKnob(size = (300, 300),
                         min = 0, max = 360,
                         step = 10,
                         show_marker = True,
                         knobimg_source = "img/knob_metal.png",
                         marker_img = "img/bline.png",
                         markeroff_color = (0.3, 0.3, .3, 1),
                         pattern_id= 99, #(ids 1 to 8, or 99 for no id)
                         debug = False,
                         obj = scatter, # Passes the object to the knob
                         knob_id = 002,
                         ms_dial = True)
        widgetB.add_widget(knobB)

        # Creates a MyKnob object
        widgetC = RelativeLayout(size_hint = (None, None), 
                                 size = (300,300),
                                 pos = (0,0))


        knobC = MyKnob(size = (300, 300),
                         min = 0, max = 360,
                         step = 10,
                         show_marker = True,
                         knobimg_source = "img/knob_metal.png",
                         marker_img = "img/bline.png",
                         markeroff_color = (0.3, 0.3, .3, 1),
                         pattern_id= 99, #(ids 1 to 8, or 99 for no id)
                         debug = False,
                         obj = scatter, # Passes the object to the knob
                         knob_id = 003,
                         ms_dial = True) 
        widgetC.add_widget(knobC)

        # Creates an image widget
        image = Image(source='img/black.jpg', size_hint_x=None, width=self.banner_width,
                                              size_hint_y=None, height=300,
                                              allow_stretch = True,
                                              keep_ratio = False, opacity = 0)

        # Adds objects to the root
        tray.add_widget(image)
        tray.add_widget(widgetA)
        tray.add_widget(widgetB)
        tray.add_widget(widgetC)
        root.add_widget(tray)
        return root

TeiKnobApp().run()