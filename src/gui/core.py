
import PySimpleGUI as sg
import gui.event_handlers

from gui.gui_context import GUIWindowContext
from gui.app_layout import viewer_col, editor_col


class PyJigGUI():

    def __init__(self):
        
        self.layout = [[viewer_col, editor_col]]
        self.context = GUIWindowContext(sg.Window('PyJig', self.layout))
        

    def render(self):
        while True:
            event, values = self.context.window.read()
            event_handler_func = getattr(gui.event_handlers, f'handle_{event}_event')
            event_handler_func(self.context, event, values)
