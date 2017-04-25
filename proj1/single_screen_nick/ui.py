from kivy.uix.widget import Widget
from kivy.uix.anchorlayout import AnchorLayout

class UI(AnchorLayout):
    def __init__(self, **kwargs):
        super(UI, self).__init__(**kwargs)
        self.controller = kwargs['controller']

        self.controller = kwargs['controller']
        self.renderer = kwargs['renderer']
        self.add_widget(self.renderer)
        self._touches = []

    def define_rotate_angle(self, touch):
        x_angle = (touch.dx/self.width)*360
        y_angle = -1*(touch.dy/self.height)*360
        return x_angle, y_angle  

    def on_touch_down(self, touch):
        if touch.y > 310:
            self._touch = touch
            touch.grab(self)
            self._touches.append(touch)
        
    def on_touch_up(self, touch): 
        if touch in self._touches:
            touch.ungrab(self)
            self._touches.remove(touch)
        
    def on_touch_move(self, touch):
        if touch in self._touches and touch.grab_current == self:
            if len(self._touches) == 1:
                ax, ay = self.define_rotate_angle(touch)
                self.controller.rotate(ax, ay)


            elif len(self._touches) == 2: # scaling here
                #use two touches to determine do we need scal
                touch1, touch2 = self._touches 
                old_pos1 = (touch1.x - touch1.dx, touch1.y - touch1.dy)
                old_pos2 = (touch2.x - touch2.dx, touch2.y - touch2.dy)
                
                old_dx = old_pos1[0] - old_pos2[0]
                old_dy = old_pos1[1] - old_pos2[1]
                
                old_distance = (old_dx*old_dx + old_dy*old_dy)
                
                new_dx = touch1.x - touch2.x
                new_dy = touch1.y - touch2.y
                
                new_distance = (new_dx*new_dx + new_dy*new_dy)
                
                SCALE_FACTOR = 0.1
                
                if new_distance > old_distance: 
                    scale = -1*SCALE_FACTOR
                elif new_distance == old_distance:
                    scale = 0
                else:
                    scale = SCALE_FACTOR
                
                if scale:
                    self.controller.zoom(scale)
