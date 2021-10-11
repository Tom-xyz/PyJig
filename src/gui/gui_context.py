import PySimpleGUI as sg


class GUIWindowContext():
    sg.theme('DarkAmber')

    def __init__(self, window):
        self.window = window

        # TODO: Encapsulate state vars
        # x,y points (top left, bottom left, top right, bottom right)
        self.crop_cords = []
        self.action = None
        self.orignal_image = None
        self.viewer_image = None
