from kivy.config import Config
#from win32api import GetSystemMetrics
#width = GetSystemMetrics(0)
#height = GetSystemMetrics(1)
width = 1280
height = 720
dial = 300
Config.set('graphics', 'borderless', 1)
Config.set('graphics', 'resizable', 0)
Config.set('graphics', 'position', 'custom')
Config.set('graphics', 'left', 0)
Config.set('graphics', 'top', 0)
Config.set('graphics', 'height', height)
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
from kivy.uix.relativelayout import RelativeLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.properties import *
from kivy.uix.gridlayout import GridLayout
from kivy.uix.scatter import Scatter
from kivy.uix.image import Image
from kivy.animation import Animation
from kivy.graphics.texture import Texture
from kivy.properties import *
from kivy.lib.osc import oscAPI
from kivy.clock import Clock
from kivy.garden.tei_knob import Knob
from kivy.lib.osc import oscAPI

class MyKnob(Knob):
	ip = '127.0.0.1'
	sendPort = 5000
	recvPort = 5001

	knob_id = ObjectProperty('')
	knob_angle = ObjectProperty()

	obj = ObjectProperty()

	def on_knob(self, value, pattern_id):
		self.knob_angle = value
		self.obj.rotation = self.knob_angle
	
		s = self.knob_id
		i = self.pattern_id
		x = self.token_pos[0]
		y = self.token_pos[1]
		z = 0
		a = self.knob_angle
		p = str(True)
	
		oscAPI.sendMsg('/tuios/tok', [s,i,x,y,z,a,p],
				ipAddr=self.ip,
				port=self.sendPort)

	def on_value(self, instance, value):
		print "token value: " + str(value)
		pass

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


		s = self.knob_id
		i = self.pattern_id
		x = self.token_pos[0]
		y = self.token_pos[1]
		z = 0
		a = self.knob_angle
		p = str(self.tk_placed)
		
		oscAPI.sendMsg('/tuios/tok', [s,i,x,y,z,a,p],
				ipAddr=self.ip,
				port=self.sendPort)

		print 'tray::on_knob:sendOSCMsg ' + 'knob_id: ' + str(self.knob_id) + \
                                  ' pattern_id: ' + str(self.pattern_id) + \
                                  ' token_pos: ' + str(self.token_pos) + \
                                  ' knob_angle: ' + str(self.knob_angle) + \
                                  ' token_placed: ' + str(self.tk_placed)

class HomescreenButton(ButtonBehavior, Image):
 
	def on_press(self):
		goAway = Animation(pos=(width/2, height/2), duration=0.75)
		goAway &= Animation(size_hint=(0.0001,0.0001), duration=0.75)
		goAway.start(self)

class Application(App):

	def build(self):
		root = FloatLayout(size=(width, height))
		brainAndTray = BoxLayout(orientation='vertical')
		topLayout = BoxLayout(orientation='horizontal')
		trayLayout = BoxLayout(orientation='horizontal',
					size_hint=(1, None),
					height=300,
					padding=20)

		scatter = Scatter()

		mainImg = HomescreenButton(source='img/homescreen.jpg',
					pos=(0,0),
					keep_ratio=False,
					allow_stretch=True,
					size_hint=(1, 1))
		self.mainImg = mainImg

		backgroundImg = Image(source='img/background.jpg')

		topTopLabel = Label(valign="middle",
					halign="center",
					text="Creating a 3-D Model of the Brain",
					color=(255,255,255,1),
					bold=True,
					font_size='50sp')

		topLeftLabel = Label(valign="middle",
					halign="left",
					text="Our goal is to be able to make a 3D printed model"+
						" of a brain that is specific to an individual in"+
						" order to help surgeons practice surgery before an actual procedure.",
					color=(255, 255, 255, 0.8),
					text_size = (400, None),
					font_size='30sp')
		self.topLeftLabel = topLeftLabel

		topMiddleLabel = Label(valign="middle",
					halign="center",
					text="brain will go here\n",
					color=(255,255,255,0.8),
					font_size='30sp')

		topRightLabel = Label(valign="middle",
					halign="left",
					text="look! more neat\nbrain facts!",
					color=(255, 255, 255, 0.8),
					font_size='30sp')
		self.topRightLabel = topRightLabel

		trayLeftLabel = Label(valign="middle",
					halign="left",
					text="Use an appropriate token\nor three fingers to\nexplore the object\nusing the knobs",
					italic=True,
					color=(255,255,255,0.75),
					font_size='20sp')

		widgetA = RelativeLayout(size_hint=(None,None),
					size=(300,300))

		knobA = MyKnob(size=(300,300),
				min=0, max=360,
				step=1,
				show_marker=True,
				knobimg_source="img/knob_metal.png",
				marker_img="img/knob_marker.png",
				markeroff_color=(0.3,0.3,0.3,1),
				pattern_id=99,
				debug=True,
				obj=scatter,
				knob_id=001)

		labelA = Label(text = "Rotate\nhorizontally",
				font_size='20sp',
				italic=True,
				bold=True,
				color=(0, 0, 0, 0.75),
				halign="center")

		widgetA.add_widget(knobA)
		widgetA.add_widget(labelA)

		widgetB = RelativeLayout(size_hint=(None, None),
					size = (300, 300))

		knobB = MyKnob(size = (300, 300),
				min = 0, max = 360,
				step = 1,
				show_marker = True,
				knobimg_source = "img/knob_metal.png",
				marker_img = "img/knob_marker.png",
				markeroff_color = (0.3, 0.3, .3, 1),
				pattern_id= 99,
				debug = False,
				obj = scatter,
				knob_id = 002)

		labelB = Label(text = "Rotate\nvertically",
				font_size='20sp',
				italic=True,
				bold=True,
				color=(0, 0, 0, 0.75),
				halign="center")

		widgetB.add_widget(knobB)
		widgetB.add_widget(labelB)

		widgetC = RelativeLayout(size_hint = (None,None),
					size=(300, 300))

		knobC = MyKnob(size = (300, 300),
				min = 0, max = 360,
				step = 1,
				show_marker = True,
				knobimg_source = "img/knob_metal.png",
				marker_img = "img/knob_marker.png",
				markeroff_color = (0.3, 0.3, 0.3, 1),
				pattern_id=99,
				debug=False,
				obj = scatter,
				knob_id = 003)

		labelC = Label(text = "Zoom",
				font_size = '20sp',
				italic=True,
				bold=True,
				color = (0, 0, 0, 0.75),
				halign="center")

		widgetC.add_widget(knobC)
		widgetC.add_widget(labelC)	
			
		renderer = Renderer()
		controller = Controller(renderer = renderer)
		ui = UI(renderer = renderer, controller = controller)

		topLayout.add_widget(topLeftLabel)
		#topLayout.add_widget(ui)
		#topLayout.add_widget(topRightLabel)
	
		trayLayout.add_widget(trayLeftLabel)
		trayLayout.add_widget(widgetA)
		trayLayout.add_widget(widgetB)
		trayLayout.add_widget(widgetC)

		brainAndTray.add_widget(topTopLabel)
		brainAndTray.add_widget(topLayout)
		brainAndTray.add_widget(trayLayout)
	
		root.add_widget(backgroundImg)
		root.add_widget(brainAndTray)
		root.add_widget(mainImg)

		return root

if __name__ == "__main__":
    Application().run()
