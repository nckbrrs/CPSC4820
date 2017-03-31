from kivy.config import Config
#from win32api import GetSystemMetrics
#width = GetSystemMetrics(0)
#height = GetSystemMetrics(1)
width = 1280
height = 720
dial = 300
times_pressed = 0
Config.set('graphics', 'borderless', 1)
Config.set('graphics', 'resizable', 0)
Config.set('graphics', 'position', 'custom')
Config.set('graphics', 'left', 0)
Config.set('graphics', 'top', 0)
Config.set('graphics', 'height', height-dial)
Config.set('graphics', 'width', width)

from kivy.app import App

from ui import UI
from controller import Controller
from renderer import Renderer
from kivy.uix.widget import Widget
from kivy.uix.label import Label
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.button import Button
from kivy.uix.behaviors import ButtonBehavior
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.image import Image
from kivy.animation import Animation
from kivy.graphics.texture import Texture
from kivy.properties import *
from kivy.lib.osc import oscAPI
from kivy.clock import Clock

class ImageButton(ButtonBehavior, Image):
    def on_other_press(self):
	global times_pressed
	shrink = Animation(x=10, y=-500, 
		size_hint=(0.2, 0.2))
	grow = Animation(x=0, y=0-dial, 
		size_hint=(1, 1.77))

	if (times_pressed % 2 == 0): 
		shrink.start(self)
	else:
		grow.start(self)

	times_pressed = times_pressed + 1

    def on_press(self):
	global times_pressed
	shrink = Animation(x=10, y=-500, 
		size_hint=(0.2, 0.2))
	grow = Animation(x=0, y=0-dial, 
		size_hint=(1, 1.77))

	if (times_pressed % 2 == 0): 
		shrink.start(self)
	else:
		grow.start(self)

	oscAPI.sendMsg('/tuios/tok', [1],
			ipAddr="127.0.0.1",
			port=5006)
	
	times_pressed = times_pressed + 1

class Application(App):
    def receive(self, value, instance):
	if (value[2] == 1):
		self.mainImg.on_other_press()

    def build(self):
	self.sendip = "127.0.0.1"
	self.sendPort=5006
	self.recvPort=5007

	oscAPI.init()
	oscid = oscAPI.listen(ipAddr=self.sendip,
				 port=self.recvPort)
	Clock.schedule_interval(lambda *x: oscAPI.readQueue(oscid), 0)
	oscAPI.bind(oscid, self.receive, '/tuios/tok')

        root = FloatLayout(size=(width, height))

        bottomLabel = Label(valign="middle",
                    halign="left",
                    text="This could be a brain soon!",
                    color=(255, 255, 255, 255),
                    font_size='40sp',
                    size_hint=(1, 0.2))

	mainImg = ImageButton(source='img/background.jpg',
		pos=(0,0-dial),
		keep_ratio=False,
		allow_stretch=True,
		size_hint=(1, 1.77))

	self.mainImg = mainImg

	middleLayout = BoxLayout(orientation="horizontal")
	leftLabel = Label(valign="middle",
			halign="left",
			text="various cool facts\n about the human brain!",
			color=(255, 255, 255, 0.8),
			font_size='30sp')

	rightLabel = Label(valign="middle",
			halign="left",
			text="look! more neat\nbrain facts!",
			color=(255, 255, 255, 0.8),
			font_size='30sp')

        renderer = Renderer()
        controller = Controller(renderer = renderer)
        ui = UI(renderer = renderer, controller = controller)

	middleLayout.add_widget(leftLabel)
	middleLayout.add_widget(ui)
	middleLayout.add_widget(rightLabel)	

        root.add_widget(bottomLabel)
        root.add_widget(middleLayout)
	root.add_widget(mainImg)

        return root

if __name__ == "__main__":
    Application().run()
