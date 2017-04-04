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

from renderer import Renderer
from controller import Controller
from ui import UI

from kivy.app import App
from kivy.properties import *
from kivy.uix.widget import Widget
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.behaviors import ButtonBehavior
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.relativelayout import RelativeLayout
from kivy.uix.image import Image
from kivy.animation import Animation
from kivy.uix.scatter import Scatter
from kivy.graphics.texture import Texture
from kivy.clock import Clock
from kivy.lib.osc import oscAPI
from kivy.garden.tei_knob import Knob

class MyKnob(Knob):
	ip = '127.0.0.1'
	sendPort = 5000

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

class SlideShow():
	def __init__(self):
		self.ip="127.0.0.1"
		self.recvPort=5001
		oscAPI.init()
		slideOSC = oscAPI.listen(ipAddr=self.ip, port= self.recvPort) 
		Clock.schedule_interval(lambda *x: oscAPI.readQueue(slideOSC), 0)
		oscAPI.bind(slideOSC, self.receiveSlideChoice, '/tuios/tok')
		
		slides = BoxLayout(orientation='vertical')
		self.slides = slides

		slide1 = BoxLayout(orientation='horizontal')
		slide1LeftLabel = Label(text="PAST:\nWhat\nwe've\ndone",
					halign="left",
					color=(255,255,255,0.8),
					bold=True,
					italic=True,
					font_size='50sp')
		slide1MidLabel = Label(text=" ")
		slide1RightLabel = Label(text="Lorem Ipsum / Lorem Ipsum\nHere's what we've \ndiscovered so far.",
					font_size='25sp')

		slide1.add_widget(slide1LeftLabel)
		slide1.add_widget(slide1MidLabel)
		slide1.add_widget(slide1RightLabel)
		self.slide1 = slide1

		slide2 = BoxLayout(orientation='horizontal')
		slide2LeftLabel = Label(text="PRESENT:\nWhat\nwe've\ndone",
					halign="left",
					color=(255,255,255,0.8),
					bold=True,
					italic=True,
					font_size='50sp')
		slide2MidLabel = Label(text=" ")
		slide2RightLabel = Label(text="Lorem Ipsum / Lorem Ipsum\nHere's what we're \nworking on at the moment.",
					font_size='25sp')

		slide2.add_widget(slide2LeftLabel)
		slide2.add_widget(slide2MidLabel)
		slide2.add_widget(slide2RightLabel)
		self.slide2 = slide2

		slide3 = BoxLayout(orientation='horizontal')
		slide3LeftLabel = Label(text="FUTURE:\nWhat\nwe'll\ndo",
					halign="left",
					color=(255,255,255,0.8),
					bold=True,
					italic=True,
					font_size='50sp')
		slide3MidLabel = Label(text=" ")
		slide3RightLabel = Label(text="Lorem Ipsum / Lorem Ipsum\nHere's what we \nplan on accomplishing.",
					font_size='25sp')

		slide3.add_widget(slide3LeftLabel)
		slide3.add_widget(slide3MidLabel)
		slide3.add_widget(slide3RightLabel)
		self.slide3 = slide3

		slides.add_widget(slide1)

	def receiveSlideChoice(self, value, instance):
		slide = value[2]

		if (slide==1):
			self.slides.clear_widgets()
			self.slides.add_widget(self.slide1)
		elif (slide==2):
			self.slides.clear_widgets()
			self.slides.add_widget(self.slide2)
		elif (slide==3):
			self.slides.clear_widgets()
			self.slides.add_widget(self.slide3)

class Application (App):
	
	def build(self):
		root = FloatLayout(size=(width, height))
		mainWindow = BoxLayout(orientation='vertical')	
		slidesLayout = SlideShow()
		trayLayout = BoxLayout(orientation='horizontal',
					size_hint=(1,None),
					height=300,
					padding=20)
		scatter = Scatter()

		homescreenImg = HomescreenButton(source='img/homescreen.jpg', 
					pos=(0,0),
					keep_ratio=False,
					allow_stretch=True,
					size_hint=(1,1))
		self.homescreenImg = homescreenImg

		backgroundImg = Image(source='img/background.png',
					pos=(0,0),
					keep_ratio=False,
					allow_stretch=True,
					size_hint=(1,1))

		topLabel = Label(text="Creating a 3-D Model of the Brain",
				font_size='50sp',
				font_color=(255,255,255,0.8))

		renderer = Renderer()
		controller = Controller(renderer = renderer)
		viewer = UI(renderer = renderer, controller = controller)


		trayLeftLabel = Label(text="Use an appropriate token\nor three fingers to\nexplore the presentation\nusing the knob",
					italic=True,
					color=(255,255,255,0.75),
					font_size='20sp')


		trayKnobWidget = RelativeLayout(size_hint=(None,None),
						size=(width/2,300))

		trayKnob = MyKnob(size=(300,300),
				pos=(-120,0),
				min=0, max=360, step=1,
				show_marker = True,
				knobimg_source = "img/knob_metal.png",
				marker_img = "img/knob_marker.png",
				markeroff_color = (.3, .3, .3, 1),
				pattern_id = 99,
				debug = False,
				obj = scatter, 
				knob_id=4)

		trayKnobLabel = Label(text="Choose\nSlide",
					pos=(-290,0),
					font_size='20sp',
					italic=True,
					bold=True,
					halign="center",
					color=(0,0,0,0.75))

		trayKnobWidget.add_widget(trayKnob)
		trayKnobWidget.add_widget(trayKnobLabel)

		trayLayout.add_widget(trayLeftLabel)
		trayLayout.add_widget(trayKnobWidget)

		mainWindow.add_widget(topLabel)
		mainWindow.add_widget(slidesLayout.slides)
		mainWindow.add_widget(trayLayout)

		root.add_widget(backgroundImg)
		root.add_widget(viewer)
		root.add_widget(mainWindow)
		root.add_widget(homescreenImg)
		return root

if __name__ == "__main__":
	Application().run()
	
