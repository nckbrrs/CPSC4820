import sys
import os
sys.path.append(os.getcwd() + "/lib/garden.tei_knob/")

from kivy.config import Config
#from win32api import GetSystemMetrics
#width = GetSystemMetrics(0)
#height = GetSystemMetrics(1)
width = 1280
height = 700
times_pressed = 0
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
from kivy.uix.image import Image
from kivy.uix.video import Video
from kivy.uix.label import Label
from kivy.uix.widget import Widget
from kivy.uix.button import Button
from kivy.uix.behaviors import ButtonBehavior
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.videoplayer import VideoPlayer
from kivy.uix.relativelayout import RelativeLayout
from kivy.animation import Animation
from kivy.uix.scatter import Scatter
from kivy.graphics.texture import Texture
from kivy.clock import Clock
from kivy.lib.osc import oscAPI
#from kivy.garden.tei_knob import Knob
from tei_knob import Knob

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

class MethodsImages(ButtonBehavior, Image):
	def on_press(self):
		global times_pressed
		times_pressed = times_pressed + 1

		if (times_pressed % 4 == 1):
			self.source="img/methods2.jpg"
		elif (times_pressed % 4 == 2):
			self.source="img/methods3.png"
		elif (times_pressed % 4 == 3):
			self.source="img/methods4.png"
		else:
			self.source="img/methods1.jpg"

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

		slide1 = BoxLayout(orientation='horizontal', padding=50)
		slide1LeftLabel = Label(text="[b][i][color=#ffffff][size=50]BACKGROUND:[/size][/b]\n[size=20]\nExplore the brain by pinching it to zoom\nand touch-and-dragging it to rotate\n\n[/size][/color][/i]",
								markup=True,
								halign="left")
		slide1MidLabel = Label(text=" ", text_size=(5, None))
		slide1RightLabel = Label(text="We've partnered with the St. Louis School of Engineering to begin quantifying how advanced manufacturing practices such as 3D printing will enhance the training and surgical practice for neurosurgeons. Our on-going study, which focuses on specifically undertaking the task of saving a patient experiencing a brain aneurysm, compares 3D printing against traditional training methodologies such as cadavers (human, animal), foam models, and other conventional practices.",
								halign="left",
								color=(255,255,255,0.8),
								font_size='20sp',
								text_size= (width/3, None))

		slide1.add_widget(slide1LeftLabel)
		slide1.add_widget(slide1MidLabel)
		slide1.add_widget(slide1RightLabel)
		self.slide1 = slide1

		slide2 = BoxLayout(orientation='horizontal', padding=50)
		slide2LeftLabel = Label(text="[b][i][color=#ffffff][size=50]METHODS:[/size][/b]\n[size=20]\nTap the picture to\niterate through different pictures.\n\n[/size][/color][/i]",
								markup=True,
								halign="left")
		slide2MidImage = MethodsImages(source="img/methods1.jpg", size_hint=(2.5,2.5))
		slide2RightLabel = Label(text="The fabrication process entails converting images obtained from medical scans into computer generated designs and, through the assistance of 3D printing, fabricating lifelike organs that can be poked, prodded, and dissected. The process begins with images obtained from MRI, CT, or ultrasound scans into computer-assisted designs (CAD). Instead of using these designs to create rigid plastic replicas of human anatomy, we converted the CADs of organs into molds which were built using a 3D printer. These molds are then injected with a hydrogel which, after freezing, assumes a solid state. The water consistency of the hydrogel is identical to that found in our bodies giving the artificial brain the same feeling as the real thing.",
								halign="left",
								color=(255,255,255,0.8),
								font_size='20sp',
								padding_x=20,
								text_size= (width/3.8, None))

		slide2.add_widget(slide2LeftLabel)
		slide2.add_widget(slide2MidImage)
		slide2.add_widget(slide2RightLabel)
		self.slide2 = slide2

		slide3 = BoxLayout(orientation='horizontal')
		slide3LeftLabel = Label(text="[b][i][color=#ffffff][size=50]IMPACT:[/size][/b]\n[size=20]\nDouble-tap the video to\nview it in fullscreen\n\n[/size][/color][/i]",
								markup=True,
								halign="left")

		playerWidget = BoxLayout(orientation='vertical')
		player = VideoPlayer(source='vid/video.mp4', allow_fullscreen=True)
		self.player = player
		playerWidget.add_widget(player)
	

		slide3RightLabel = Label(text="In this video you can see just how powerful the real life effects of this research can be. \n\n\"I've done a lot of aneurysm operations in my career and I can confidently say that having the 3D printed model here has a very positive impact on the procedure results,\" states Dr. Abdulrauf, Neurosurgeon-in-Chief at St. Louis University Hospital. \"The model has helped to idenfity and overcome surgical challenges, like optimum access to the aneurysm or the depth and angle of the approach, before surgery begins.\"",
								halign="left",
								color=(255,255,255,0.8),
								font_size='20sp',
								text_size= (width/4, None))

		slide3.add_widget(slide3LeftLabel)
		slide3.add_widget(playerWidget)
		slide3.add_widget(slide3RightLabel)
		self.slide3 = slide3


		slides.add_widget(slide1)

	def receiveSlideChoice(self, value, instance):
		slide = value[2]

		if (slide==1):
			self.slides.clear_widgets()
			self.slides.add_widget(self.slide1)
			self.player.seek(0)
			self.player.state='stop'
		elif (slide==2):
			self.slides.clear_widgets()
			self.slides.add_widget(self.slide2)
			self.player.seek(0)
			self.player.state='stop'
		elif (slide==3):
			self.slides.clear_widgets()
			self.slides.add_widget(self.slide3)
			self.player.state='play'

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


		trayLeftLabel = Label(text="Use an appropriate token or three fingers\nto explore the presentation using the knob\n\n",
							italic=True,
							color=(255,255,255,0.85),
							font_size='20sp')


		trayKnobWidget = RelativeLayout(size_hint=(None,None),
										size=(300,300))

		trayKnob = MyKnob(size=(300,300),
						min=0, max=360, step=1,
						show_marker = True,
						knobimg_source = "img/knob_metal.png",
						marker_img = "img/knob_marker.png",
						markeroff_color = (.3, .3, .3, 1),
						pattern_id = 99,
						debug = False,
						obj = scatter,
						knob_id=1)

		trayKnobLabel = Label(text="Choose\nSlide",
							font_size='20sp',
							italic=True,
							bold=True,
							halign="center",
							color=(0,0,0,0.75))

		trayRightLabel = Label(text=" ", font_size='20sp')

		trayKnobWidget.add_widget(trayKnob)
		trayKnobWidget.add_widget(trayKnobLabel)

		trayLayout.add_widget(trayLeftLabel)
		trayLayout.add_widget(trayKnobWidget)
		trayLayout.add_widget(trayRightLabel)

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
	
