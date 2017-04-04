from kivy.config import Config
#from win32api import GetSystemMetrics
#width = GetSystemMetrics(0)
#height = GetSystemMetrics(1)
width = 1280
height = 720
times_pressed = 0
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
from kivy.uix.behaviors import ButtonBehavior
from kivy.uix.image import Image
from kivy.animation import Animation
from kivy.uix.label import Label

# garden.tei_knob lib folder must exist at \.kivy\garden
from kivy.garden.tei_knob import  Knob

# Import kivy osc library
from kivy.lib.osc         import oscAPI
from kivy.clock import Clock

class ImageButton(ButtonBehavior, Image):
    def on_other_press(self):
	global times_pressed
	shrink = Animation(x=10, y=10, 
		size_hint=(0.2, 0.2))
	grow = Animation(x=0, y=0, 
		size_hint=(1, 2.2))

	if (times_pressed % 2 == 0):
		shrink.start(self)
	else:
		grow.start(self)

	times_pressed = times_pressed + 1


    def on_press(self):
	global times_pressed
	shrink = Animation(x=10, y=10, 
		size_hint=(0.2, 0.2))
	grow = Animation(x=0, y=0, 
		size_hint=(1, 2.2))

	if (times_pressed % 2 == 0):
		shrink.start(self)
	else:
		grow.start(self)


	oscAPI.sendMsg('/tuios/tok', [1],
			ipAddr="127.0.0.1",
			port=5007)

	times_pressed = times_pressed + 1

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
        a = self.knob_angle
        p = str(True) #Token placed


        oscAPI.sendMsg('/tuios/tok', [s,i,x,y,z,a,p], 
                                    ipAddr= self.ip, 
                                    port= self.port) 

    # on_value is called when the angle is updated
    def on_value(self, instance, value):
        print "token value: " + str(value)
        pass

     # on_pattern_id is called when the id is updated
    def on_pattern_id(self, instance, value):
        print "token id: " + str(value)
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

    def receive(self, value, instance):
	if (value[2] == 1):
		self.mainImg.on_other_press()

    def build(self):
	self.sendip = "127.0.0.1"
	self.sendPort=5007
	self.recvPort=5006

        oscAPI.init()
	oscid = oscAPI.listen(ipAddr=self.sendip,
				 port=self.recvPort)
	Clock.schedule_interval(lambda *x: oscAPI.readQueue(oscid), 0)
	oscAPI.bind(oscid, self.receive, '/tuios/tok')

        root = FloatLayout(size=(self.tray_width,300), pos = (0,0))

        # Creates an image widget for the root
        root_image = Image(source='img/black.jpg', size_hint_x=None, width=self.tray_width,
                                              size_hint_y=None, height=300,
                                              allow_stretch = True,
                                              keep_ratio = False)
        root.add_widget(root_image)

        tray = GridLayout(rows = 1, cols = 4, spacing = 0, padding = 0)

        scatter = Scatter()
 
	leftLabel = Label(valign="middle",
				halign="left",
				text="Use an appropriate token\nor three fingers to\nexplore the object\nusing the knobs",
				italic=True,
				color=(255, 255, 255, 0.75),
				font_size='20sp')

       # Creates a MyKnob object
        widgetA = RelativeLayout(size_hint = (None, None), 
                                 size = (300,300))


        knobA = MyKnob(size = (300, 300),
                         min = 0, max = 360,
                         step = 1,
                         show_marker = True,
                         knobimg_source = "img/knob_metal.png",
                         marker_img = "img/bline.png",
                         markeroff_color = (0.3, 0.3, .3, 1),
                         pattern_id= 99, #(ids 1 to 8, or 99 for no id)
                         debug = False,
                         obj = scatter, # Passes the object to the knob
                         knob_id = 001)

	labelA = Label(text = "Rotate object\nhorizontally",
			font_size = '20sp',
			italic = True,
			bold = True,
			color = (0, 0, 0, 0.75),
			halign = "center")
 
        widgetA.add_widget(knobA)
	widgetA.add_widget(labelA)

        # Creates a MyKnob object
        widgetB = RelativeLayout(size_hint = (None, None), 
                                 size = (300,300))

        knobB = MyKnob(size = (300, 300),
                         min = 0, max = 360,
                         step = 1,
                         show_marker = True,
                         knobimg_source = "img/knob_metal.png",
                         marker_img = "img/bline.png",
                         markeroff_color = (0.3, 0.3, .3, 1),
                         pattern_id= 99, #(ids 1 to 8, or 99 for no id)
                         debug = False,
                         obj = scatter, # Passes the object to the knob
                         knob_id = 002) 

	labelB = Label(text = "Rotate object\nvertically",
			font_size = '20sp',
			italic = True,
			bold = True,
			color = (0, 0, 0, 0.75),
			halign = "center")

        widgetB.add_widget(knobB)
	widgetB.add_widget(labelB)

        # Creates a MyKnob object
        widgetC = RelativeLayout(size_hint = (None, None), 
                                 size = (300,300))


        knobC = MyKnob(size = (300, 300),
                         min = 0, max = 360,
                         step = 1,
                         show_marker = True,
                         knobimg_source = "img/knob_metal.png",
                         marker_img = "img/bline.png",
                         markeroff_color = (0.3, 0.3, .3, 1),
                         pattern_id= 99, #(ids 1 to 8, or 99 for no id)
                         debug = False,
                         obj = scatter, # Passes the object to the knob
                         knob_id = 003) 

	labelC = Label(text = "Zoom",
			font_size = '20sp',
			italic = True,
			bold = True,
			color = (0, 0, 0, 0.75),
			halign = "center")

        widgetC.add_widget(knobC)
	widgetC.add_widget(labelC)

	mainImg = ImageButton(source='img/background.jpg',
		pos=(0,0),
		keep_ratio=False,
		allow_stretch=True,
		size_hint=(1, 2.2))

	self.mainImg = mainImg

        # Adds objects to the root
        tray.add_widget(leftLabel)
	tray.add_widget(widgetA)
        tray.add_widget(widgetB)
        tray.add_widget(widgetC)
        root.add_widget(tray)
	root.add_widget(mainImg)
        return root

TeiKnobApp().run()
