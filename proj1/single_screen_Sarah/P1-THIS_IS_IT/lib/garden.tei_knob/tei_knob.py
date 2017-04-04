"""
    Knob
    ====

    The :class:`Knob` widget creates a component that looks like a
    control Knob or Dial (from Wikipedia : "A control knob is a rotary
    control used to provide input to a device when grasped by an
    operator and turned, so that the degree of rotation corresponds to
    the desired input." http://en.wikipedia.org/wiki/Control_knob).
    To configure a knob a max/min, slope and step values should be provided.
    Additionally, knobimg_source could be set to load
    a texture that visually represents the knob.

"""
__all__     = ('Knob',)
__version__ = '0.2'

from kivy.config import Config
Config.set('input', 'wm_dial', 'wm_dial')


import math

from kivy.lang          import  Builder
from kivy.uix.widget    import  Widget
from kivy.properties    import  NumericProperty, ObjectProperty, StringProperty,\
                                BooleanProperty, ReferenceListProperty, BoundedNumericProperty,\
                                ListProperty
from knobPatternId   import *
import wm_dial

Builder.load_string('''
#
#    Knob
#    ====
#     To create a basic knob (in a kv file):
#
#     Knob:
#       size:               100, 100
#       min:                0
#       max:                100
#       step:               1
#       slope:              1
#       value:              0                       # Default position of knob.
#       knobimg_source:     "img/knob_metal.png"    # Knob texture
#       show_marker:        False                   # Do not show surrounding marker
#       pattern_id          3                       # accepts only knob id 3. 
#                                                   # If not present defauts to 99-any token
#
#     To create a knob with a surrounding marker:
#
#     Knob:
#       size:               100, 100
#       min:                0
#       max:                100
#       step:               1
#       slope:              1
#       value:              0                       # Default position of knob.
#       knobimg_source:     "img/knob_metal.png"    # Knob texture
#       show_marker:        True                    # Show surrounding marker
#       marker_img:         "img/bline.png"         # Marker texture image
#       knob_size:          0.9                     # Scales knob size to leave space for marker
#       markeroff_color:    0, 0, 0, 0

<Knob>
    size_hint: None, None

    canvas.before:
        #Color:
        #    rgba: self.markeroff_color
        #Ellipse:
        #    pos: self.pos
        #    size: self.size[0], self.size[1]
        #    angle_start: 0
        #    angle_end: 360
        #    source: self.markeroff_img

        Color:
            rgba: self.marker_color
        Ellipse:
            pos: self.pos
            size: self.size[0]*1, self.size[1]*1
            angle_start: self.marker_startangle
            angle_end: self._angle + self.marker_ahead if self._angle > self.marker_startangle else self.marker_startangle
            source: self.marker_img

        Color:
            rgba: self.knobimg_bgcolor
        Ellipse:
            pos: self.pos[0] + (self.size[0] * (1 - self.knobimg_size))/2, self.pos[1] + (self.size[1] * (1 - self.knobimg_size)) / 2
            size: self.size[0] * (self.knobimg_size), self.size[1] * (self.knobimg_size)

        Color:
            rgba: self.knobimg_color
        PushMatrix
        Rotate:
            angle: 360 - self._angle
            origin: self.center
        Rectangle:
            pos: self.pos[0] + (self.size[0] * (1 - self.knobimg_size)) /2, self.pos[1] + (self.size[1] * (1 - self.knobimg_size)) / 2
            size: self.size[0] * (self.knobimg_size), self.size[1] * (self.knobimg_size)
            source: self.knobimg_source

    canvas:
        PopMatrix

''')

class Knob(Widget):
    """Class for creating a Knob widget."""

    min = NumericProperty(0)
    '''Minimum value for value :attr:`value`.
    :attr:`min` is a :class:`~kivy.properties.NumericProperty` and defaults
    to 0.
    '''

    max = NumericProperty(100)
    '''Maximum value for value :attr:`value`.
    :attr:`max` is a :class:`~kivy.properties.NumericProperty` and defaults
    to 100.
    '''

    range = ReferenceListProperty(min, max)
    ''' Range of the values for Knob.
    :attr:`range` is a :class:`~kivy.properties.ReferenceListProperty` of
    (:attr:`min`, :attr:`max`).
    '''

    value = NumericProperty(0)
    '''Current value of the knob. Set :attr:`value` when creating a knob to
    set its initial position. An internal :attr:`_angle` is calculated to set
    the position of the knob.
    :attr:`value` is a :class:`~kivy.properties.NumericProperty` and defaults
    to 0.
    '''

    step = BoundedNumericProperty(1, min=0)
    '''Step interval of knob to go from min to max. An internal
    :attr:`_angle_step` is calculated to set knob step in degrees.
    :attr:`step` is a :class:`~kivy.properties.BoundedNumericProperty`
    and defaults to 1 (min=0).
    '''

    curve = BoundedNumericProperty(1, min=1)
    '''This parameter determines the shape of the map function. It represent the
    reciprocal of a power function's exponent used to map the input value.
    So, for higher values of curve the contol is more reactive, and conversely.
    '''

    knobimg_source = StringProperty("")
    '''Path of texture image that visually represents the knob. Use PNG for
    transparency support. The texture is rendered on a centered rectangle of
    size = :attr:`size` * :attr:`knobimg_size`.
    :attr:`knobimg_source` is a :class:`~kivy.properties.StringProperty`
    and defaults to empty string.
    '''

    knobimg_color = ListProperty([1, 1, 1, 1])
    '''Color to apply to :attr:`knobimg_source` texture when loaded.
    :attr:`knobimg_color` is a :class:`~kivy.properties.ListProperty`
    and defaults to [1,1,1,1].
    '''

    knobimg_size = BoundedNumericProperty(0.9, max=1.0, min=0.1)
    ''' Internal proportional size of rectangle that holds
    :attr:`knobimg_source` texture.
    :attr:`knobimg_size` is a :class:`~kivy.properties.BoundedNumericProperty`
    and defaults to 0.9.
    '''

    show_marker = BooleanProperty(True)
    ''' Shows/hides marker surrounding knob. use :attr:`knob_size` < 1.0 to
    leave space to marker.
    :attr:`show_marker` is a :class:`~kivy.properties.BooleanProperty`
    and defaults to True.
    '''

    marker_img = StringProperty("")
    '''Path of texture image that visually represents the knob marker. The
    marker is rendered in a centered Ellipse (Circle) with the same size of
    the widget and goes from angle_start=:attr:`marker_startangle` to
    angle_end=:attr:`_angle`.
    :attr:`marker_img` is a :class:`~kivy.properties.StringProperty` and
    defaults to "".
    '''

    marker_color = ListProperty([1, 1, 1, 0.5])
    '''Color to apply to :attr:`marker_img` texture when loaded.
    :attr:`marker_color` is a :class:`~kivy.properties.ListProperty`
    and defaults to [1,1,1,1].
    '''

    knobimg_bgcolor = ListProperty([0, 0, 0, 0.05])
    ''' Background color behind :attr:`knobimg_source` texture.
    :attr:`value` is a :class:`~kivy.properties.ListProperty` and defaults
    to [0,0,0,1].
    '''

    markeroff_img = StringProperty("")
    '''Path of texture image that visually represents the knob marker where
    it's off, that is, parts of the marker that haven't been reached yet by
    the knob (:attr:`value`).
    :attr:`markeroff_img` is a :class:`~kivy.properties.StringProperty`
    and defaults to "".
    '''

    markeroff_color = ListProperty([0, 0, 0, 1])
    '''Color applied to :attr:`markeroff_img` int the Canvas.
    :attr:`markeroff_color` is a :class:`~kivy.properties.ListProperty`
    and defaults to [0,0,0,0].
    '''

    marker_startangle = NumericProperty(0)
    '''Starting angle of Ellipse where :attr:`marker_img` is rendered.
    :attr:`value` is a :class:`~kivy.properties.NumericProperty` and defaults
    to 0.
    '''

    marker_ahead = NumericProperty(0)
    ''' Adds degrees to angle_end of marker (except when :attr:`value` == 0).
    :attr:`marker_ahead` is a :class:`~kivy.properties.NumericProperty`
    and defaults to 0.
    '''

    pattern_id = NumericProperty(99)
    ''' Defines which pattern id the knob will recognize. 
    Use 99 for any.
    Ids range from 1 to 8.
    '''
    token_placed    = BooleanProperty(False)        
    '''flag to indicate a token is placed. 
    '''
    token_pos       = (0,0)
    '''variable with touch info of tpuid point
    '''

    ms_dial         = BooleanProperty(False)
    '''When true dial receives input from 
    '''
    ignore_token_placed = BooleanProperty(False)

    debug = BooleanProperty(False)

    _angle          = NumericProperty(0)            # Internal angle calculated from value.
    _angle_step     = NumericProperty(0)            # Internal angle_step calculated from step.
    _tokenId = 0                                    # Internal token id
    _points = ListProperty([None, None, None])      # Internal list of points on a knob
    pts = {}
    _pointid = NumericProperty(-1)                  # Internal count of points of a knob
    _patternId = PatternId()                        # Internal object of pattern identifying class
    _tpuid = None                                   # Internal uid of top point
    _tptouch = None                                 # Internal variable with touch info of tpuid point
    _dialtouch = False

    def __init__(self, *args, **kwargs):
        super(Knob, self).__init__(*args, **kwargs)
        self.bind(show_marker   =   self._show_marker)
        self.bind(value         =   self._value)
        self._patternId.DEBUG = self.debug

    def _value(self, instance, value):
        self._angle     =   pow( (value - self.min)/(self.max - self.min), 1./self.curve) * 360.
        self._angle = value
        if self.token_placed:
            tid = self._tokenId
        else:
            tid = 0
        self.on_knob(value, tid)

    def _show_marker(self, instance, flag):
        # "show/hide" marker.
        if flag:
            self.knobimg_bgcolor[3] = 1
            self.marker_color[3] = 1
            self.markeroff_color[3] = 1
        else:
            self.knobimg_bgcolor[3] = 0
            self.marker_color[3] = 0
            self.markeroff_color[3] = 0


    def on_touch_down(self, touch):
        if self.collide_point(*touch.pos):
            self.checkTokenPlaced(touch)
            if self.token_placed:
                self._tpuid = self._patternId.getTopPointUid()
            return False

    def on_touch_up(self, touch):
        if self._pointid >= 0:
            self._pointid -= 1
            if self._pointid == -1 or touch.uid == self._tpuid:
                self.token_placed = False
                self._tpuid = -1
                self._patternId.clearTopPointUid()
                self._tptouch = None
                self.token_pos = (0,0)
                self._pointid = -1
                self._dialtouch = False


    def on_touch_move(self, touch):
        if touch.device == 'wm_dial' and self.ms_dial \
           and (self.token_placed == True or self.ignore_token_placed == True):

            self._dialtouch = True
        #and self.token_placed:
            #print str(touch.device) + str(touch.ud) + str(touch.uid)
            new_angle = self.value
            if touch.ud['action'] == 'press':
                print "No action for dial press"
            if touch.ud['action'] == 'left':
                new_angle -= (self.step*360)/(self.max - self.min)
            if new_angle < 0:
                new_angle = 360

            if touch.ud['action'] == 'right':
                new_angle += (self.step*360)/(self.max - self.min)
            if new_angle > 360:
                new_angle = (self.step*360)/(self.max - self.min)
            self.update_angle_dial(new_angle)

        elif self.token_placed and self._dialtouch == False:
            if touch.uid == self._tpuid:
                self.update_angle(touch)

    def update_angle_dial(self, angle):

        self._angle_step    =   (self.step*360)/(self.max - self.min)
        self._angle         =   self._angle_step
        while self._angle < angle:
            self._angle     =   self._angle + self._angle_step

        relativeValue   =   pow((angle/360.), 1./self.curve)
        self.value      =   (relativeValue * (self.max - self.min)) + self.min


    def update_angle(self, touch):
        self._tptouch = touch
        self.token_pos = self.to_window(touch.pos[0], touch.pos[1])
        posx, posy          =   touch.pos
        cx, cy              =   self.center
        rx, ry              =   posx - cx, posy - cy

        if ry >= 0:                                 # Quadrants are clockwise.
            quadrant = 1 if rx >= 0 else 4
        else:
            quadrant = 3 if rx <= 0 else 2

        try:
            angle    = math.atan(rx / ry) * (180./math.pi)
            if quadrant == 2 or quadrant == 3:
                angle = 180 + angle
            elif quadrant == 4:
                angle = 360 + angle

        except:                                   # atan not def for angle 90 and 270
            angle = 90 if quadrant <= 2 else 270

        self._angle_step    =   (self.step*360)/(self.max - self.min)
        self._angle         =   self._angle_step
        while self._angle < angle:
            self._angle     =   self._angle + self._angle_step

        relativeValue   =   pow((angle/360.), 1./self.curve)
        self.value      =   (relativeValue * (self.max - self.min)) + self.min


    #TO OVERRIDE
    def on_knob(self, value, pattern_id):
        pass


    # Extension functions for pattern identification 
    def checkTokenPlaced(self, touch):
        if self.token_placed == False:
            return self.identifyToken(touch)

    def identifyToken(self, touch):
        if self.identifyPoints(touch):
            return self.tokenIdPool(self.pts)

    def identifyPoints(self, touch):
        if self._pointid < 2:
            self._pointid += 1
            self._points[self._pointid] = touch
            self.pts[self._pointid] = (touch.x,touch.y)
            if self._pointid == 2:
                return True
            else:
                return False
        else: 
            return False

    def tokenIdPool(self, points): 
        self._tokenId = self._patternId.findTokenId(points, self._points)
        if (self._tokenId == self.pattern_id) or (self.pattern_id == 99):
            self.token_placed = True
            return True
        else:
            self.token_placed = False
            return False