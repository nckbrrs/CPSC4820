from kivy.config import Config
from win32api import GetSystemMetrics
width = GetSystemMetrics(0)
height = GetSystemMetrics(1)
Config.set('graphics', 'borderless', 1)
Config.set('graphics', 'resizable', 0)
Config.set('graphics', 'position', 'custom')
Config.set('graphics', 'left', 0)
Config.set('graphics', 'top', 0)
Config.set('graphics', 'height', height)
Config.set('graphics', 'width', width)

from kivy.app import App

from ui import UI
from controllerVert import Controller
from renderer import Renderer
from kivy.uix.widget import Widget
from kivy.uix.label import Label
from kivy.uix.gridlayout import GridLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.relativelayout import RelativeLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.properties import *


class Application(App):
    def build(self):  
        root = BoxLayout(orientation="vertical", size=(width, height))

        topLabel = Label(valign="middle",
                    halign="left",
                    text="Here's a cool brain",
                    color=(255, 255, 255, 255),
                    font_size='40sp',
                    size_hint=(1, 0.2))

        renderer = Renderer()
        controller = Controller(renderer = renderer)
        ui = UI(renderer = renderer, controller = controller)

        root.add_widget(topLabel)
        root.add_widget(ui)

        return root

if __name__ == "__main__":
    Application().run()
