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

class SlideShow():
	def __init__(self):
		print "\n\n\n\n\nslideshow built\n\n\n\n"
		self.ip="127.0.0.1"
		self.recvPort=5003

		oscAPI.init()
		slideOSC = oscAPI.listen(ipAddr=self.ip, port= self.recvPort) 
		Clock.schedule_interval(lambda *x: oscAPI.readQueue(slideOSC), 0)
		oscAPI.bind(slideOSC, self.receiveSlideChoice, '/tuios/tok')
	
		slides = BoxLayout(orientation='vertical')
		self.slides = slides

		slide1 = BoxLayout(orientation='vertical', size_hint=(1, None), height=300)
		slide1MedLayout = BoxLayout(orientation='horizontal')
		slide1TopLabel = Label(text="INTRODUCTION",
				color=(255, 255, 255, 0.8),
				font_size='30sp')

		slide1MedLeftLabel = Label(text="s1 med left", 
					color=(255,255,255,0.8),
					font_size='20sp')
		slide1MedMedLabel = Label(text="s1 med med",
					color=(255, 255, 255, 0.8),
					font_size='20sp')
		slide1MedRightLabel = Label(text="s1 med right",
					color=(255,255,255,0.8),
					font_size='20sp')

		slide1MedLayout.add_widget(slide1MedLeftLabel)
		slide1MedLayout.add_widget(slide1MedMedLabel)
		slide1MedLayout.add_widget(slide1MedRightLabel)

		slide1.add_widget(slide1TopLabel)
		slide1.add_widget(slide1MedLayout)
		self.slide1 = slide1

		slide2 = BoxLayout(orientation='vertical', size_hint=(1, None), height=300)
		slide2MedLayout = BoxLayout(orientation='horizontal',
					size_hint=(1, None),
					height=200)
		slide2TopLabel = Label(text="PRESENT SLIDE",
				color=(255, 255, 255, 0.8),
				font_size='30sp')

		slide2MedLeftLabel = Label(text="here's the brain we're tryna look at",
					color=(255,255,255,0.8),
					font_size='20sp')

		renderer = Renderer()
		controller = Controller(renderer = renderer)
		ui = UI(renderer = renderer, controller = controller)

		slide2MedLayout.add_widget(slide2MedLeftLabel)
		slide2MedLayout.add_widget(ui)

		slide2.add_widget(slide2TopLabel)
		slide2.add_widget(slide2MedLayout)
		self.slide2 = slide2

		slide3 = BoxLayout(orientation='vertical', size_hint=(1, None), height=300)
		slide3MedLayout = BoxLayout(orientation='horizontal')
		slide3TopLabel = Label(text="FUTURE",
				color=(255, 255, 255, 0.8),
				font_size='30sp')

		slide3MedLeftLabel = Label(text="s3 med left", 
					color=(255,255,255,0.8),
					font_size='20sp')
		slide3MedMedLabel = Label(text="s3 med med",
					color=(255, 255, 255, 0.8),
					font_size='20sp')
		slide3MedRightLabel = Label(text="s3 med right",
					color=(255,255,255,0.8),
					font_size='20sp')

		slide3MedLayout.add_widget(slide3MedLeftLabel)
		slide3MedLayout.add_widget(slide3MedMedLabel)
		slide3MedLayout.add_widget(slide3MedRightLabel)

		slide3.add_widget(slide3TopLabel)
		slide3.add_widget(slide3MedLayout)

		self.slide3 = slide3

		slides.add_widget(slide1)
		
	def receiveSlideChoice(self, value, instance):
		slide = value[2]
		print "\n\n\nslide = ", slide, "\n\n\n\n\n"
		if (slide>0 and slide <121):
			self.slides.clear_widgets()
			self.slides.add_widget(self.slide1)
		elif (slide > 120 and slide < 241):
			self.slides.clear_widgets()
			self.slides.add_widget(self.slide2)
		elif (slide > 240 and slide < 361):
			self.slides.clear_widgets()
			self.slides.add_widget(self.slide3)

class Application(App):

	def build(self):
		root = FloatLayout(size=(width, height))
		brainAndTray = BoxLayout(orientation='vertical')
		topLayout = SlideShow()
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

		trayLeftLabel = Label(valign="middle",
					text="Use an appropriate token\nor three fingers to\nexplore the presentation\nusing the knob",
					italic=True,
					color=(255,255,255,0.75),
					font_size='20sp')

		widgetD = RelativeLayout(size_hint=(None,None), 
					size=(width/2-100,300))

		knobD = MyKnob(size=(300,300),
				min=0, max=360,
				step=1,
				show_marker=True,
				knobimg_source="img/knob_metal.png",
				marker_img="img/knob_marker.png",
				markeroff_color = (0.3, 0.3, 0.3, 1),
				pattern_id=99,
				debug=False,
				obj = scatter,
				knob_id=004)

		labelD = Label(text = "Choose\nSlide",
				font_size='20sp',
				italic=True,
				bold=True,
				color=(0,0,0,0.75),
				halign="center",
				pos=(-120, 0))

		widgetD.add_widget(knobD)
		widgetD.add_widget(labelD)
		
		trayLayout.add_widget(trayLeftLabel)
		trayLayout.add_widget(widgetD)		

		brainAndTray.add_widget(topTopLabel)
		brainAndTray.add_widget(topLayout.slides)
		brainAndTray.add_widget(trayLayout)
	
		root.add_widget(backgroundImg)
		root.add_widget(brainAndTray)
		root.add_widget(mainImg)

		return root

if __name__ == "__main__":
    Application().run()
