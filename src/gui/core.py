import PySimpleGUI as sg

import gui.event_handlers
from gui.context import WindowContext
from gui.elements import viewer_col, editor_col


class PyJigGUI():

    def __init__(self):
        self.layout = [[viewer_col, editor_col]]
        self.window = sg.Window('PyJig', self.layout, resizable=True)
        self.context = WindowContext(self.window)

    def render(self):
        while True:
            event, values = self.window.read()
            event_handler_func = getattr(gui.event_handlers, f'handle_{event}_event')
            event_handler_func(self.context, event, values)
