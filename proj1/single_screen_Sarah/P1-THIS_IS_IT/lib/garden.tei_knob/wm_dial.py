'''
Support for WM_PEN messages (Windows platform)
==============================================
'''

__all__ = ('WM_DialProvider', 'WM_Dial')

import os
from kivy.input.providers.wm_common import (
    PEN_OR_TOUCH_SIGNATURE, PEN_OR_TOUCH_MASK, GWL_WNDPROC,
    WM_MOUSEMOVE, WM_LBUTTONUP, WM_LBUTTONDOWN,
    WM_TABLET_QUERYSYSTEMGESTURE, QUERYSYSTEMGESTURE_WNDPROC,
    PEN_EVENT_TOUCH_MASK)
from kivy.input.motionevent import MotionEvent


class WM_Dial(MotionEvent):
    '''MotionEvent representing the WM_Pen event. Supports the pos profile.'''

    def depack(self, args):
        self.is_touch = True
        self.sx, self.sy = args[0], args[1]
        super(WM_Dial, self).depack(args)

    def __str__(self):
        i, u, s, d = (self.id, self.uid, str(self.spos), self.device)
        return '<WMPen id:%d uid:%d pos:%s device:%s>' % (i, u, s, d)
if 'KIVY_DOC' in os.environ:
    # documentation hack
    WM_DialProvider = None

else:
    from collections import deque
    from ctypes.wintypes import (ULONG, UINT, WPARAM, LPARAM,
                                 HANDLE, BOOL)
    from ctypes import (Structure, windll, byref, c_int16,
                        c_int, WINFUNCTYPE, POINTER)
    from kivy.input.provider import MotionEventProvider
    from kivy.input.factory import MotionEventFactory

    LRESULT = LPARAM
    WNDPROC = WINFUNCTYPE(LRESULT, HANDLE, UINT, WPARAM, LPARAM)

    class RECT(Structure):
        _fields_ = [
            ('left', ULONG),
            ('top', ULONG),
            ('right', ULONG),
            ('bottom', ULONG)]

        x = property(lambda self: self.left)
        y = property(lambda self: self.top)
        w = property(lambda self: self.right - self.left)
        h = property(lambda self: self.bottom - self.top)
    win_rect = RECT()

    try:
        windll.user32.SetWindowLongPtrW.restype = WNDPROC
        windll.user32.SetWindowLongPtrW.argtypes = [HANDLE, c_int, WNDPROC]
        SetWindowLong_wrapper = windll.user32.SetWindowLongPtrW
    except AttributeError:
        windll.user32.SetWindowLongW.restype = WNDPROC
        windll.user32.SetWindowLongW.argtypes = [HANDLE, c_int, WNDPROC]
        SetWindowLong_wrapper = windll.user32.SetWindowLongW

    windll.user32.GetMessageExtraInfo.restype = LPARAM
    windll.user32.GetMessageExtraInfo.argtypes = []
    windll.user32.GetClientRect.restype = BOOL
    windll.user32.GetClientRect.argtypes = [HANDLE, POINTER(RECT)]
    windll.user32.CallWindowProcW.restype = LRESULT
    windll.user32.CallWindowProcW.argtypes = [WNDPROC, HANDLE, UINT, WPARAM,
                                              LPARAM]
    windll.user32.GetActiveWindow.restype = HANDLE
    windll.user32.GetActiveWindow.argtypes = []

    class WM_DialProvider(MotionEventProvider):
        dial_signature = 257
        dial_right     = 39
        dial_left      = 37
        dial_press     = 40
        upd_type       = None

        def _is_pen_message(self, msg):
            info = windll.user32.GetMessageExtraInfo()
            # It's a touch or a pen
            if (self.dial_signature) == msg:
                if not info:
                    return True

        def _pen_handler(self, msg, wParam, lParam):
            windll.user32.GetClientRect(self.hwnd, byref(win_rect))
            #may be used in the future to identify position
            x = c_int16(lParam & 0xffff).value / float(win_rect.w)
            y = c_int16(lParam >> 16).value / float(win_rect.h)
            y = abs(1.0 - y)

            if wParam == self.dial_left:
                self.upd_type = 'left'
                self.pen_events.appendleft(('update', x, y))
                self.pen_status = True
            elif wParam == self.dial_right:
                self.upd_type = 'right'
                self.pen_events.appendleft(('update', x, y))
                self.pen_status = True
            elif wParam == self.dial_press:
                self.upd_type = 'press'
                self.pen_events.appendleft(('update', x, y))
                self.pen_status = True

        def _pen_wndProc(self, hwnd, msg, wParam, lParam):
            if self._is_pen_message(msg):
                self._pen_handler(msg, wParam, lParam)
                return 1
            else:
                return windll.user32.CallWindowProcW(self.old_windProc,
                                                     hwnd, msg, wParam, lParam)

        def start(self):
            self.uid = 0
            self.ud = {}
            #self.id = 0
            self.pen = None
            self.pen_status = None
            self.pen_events = deque()

            self.hwnd = windll.user32.GetActiveWindow()

            # inject our own wndProc to handle messages
            # before window manager does
            self.new_windProc = WNDPROC(self._pen_wndProc)
            self.old_windProc = SetWindowLong_wrapper(
                self.hwnd, GWL_WNDPROC, self.new_windProc)

        def update(self, dispatch_fn):
            while True:

                try:
                    etype, x, y = self.pen_events.pop()
                except:
                    break

                if self.pen == None:
                    self.uid += 1
                    self.pen = WM_Dial('wm_dial', self.uid, [x, y])


                if etype == 'update':
                    self.pen.ud = {'action':self.upd_type}
                    self.pen.move([x, y])
                elif etype == 'end':
                    self.pen.update_time_end()

                dispatch_fn(etype, self.pen)

        def stop(self):
            self.pen = None
            SetWindowLong_wrapper(self.hwnd, GWL_WNDPROC, self.old_windProc)

    MotionEventFactory.register('wm_dial', WM_DialProvider)
