import os
import io
import PySimpleGUI as sg
import cv2

from utils import resize, resize_file
from PIL import Image


class PyJigGUI():
    sg.theme('DarkAmber')

    input_frame = sg.Frame(
        title='Input Image',
        layout=[
            [sg.Input(key='-IN-', enable_events=True), sg.FileBrowse()],
            [sg.T('Original size'), sg.T(k='-ORIG WIDTH-'), sg.T('X'), sg.T(k='-ORIG HEIGHT-')],
            [sg.T('Resized size'), sg.T(k='-NEW WIDTH-'), sg.T('X'), sg.T(k='-NEW HEIGHT-')]
        ],
        expand_x=True
    )

    actions_frame = sg.Frame(
        title='Actions',
        layout=[
            [sg.Button(button_text='Crop'), sg.Button(button_text='Grid'), sg.Button(button_text='Search')],
        ],
        expand_y=True,
        expand_x=True
    )

    output_frame = sg.Frame(
        title='Log',
        layout=[
            [sg.Output(key='-OUT-', expand_y=True, expand_x=True)]
        ],
        pad=(0, 0),
        expand_y=True,
        expand_x=True
    )

    graph = sg.Graph(
        canvas_size=(1500, 840),
        graph_bottom_left=(0, 840),
        graph_top_right=(1500, 0),
        key="-GRAPH-",
        enable_events=True
    )

    viewer_frame = sg.Frame(
        title='Jigsaw Viewer',
        layout=[
            [graph]
        ]
    )

    viewer_col = sg.Column(layout=[[viewer_frame]], expand_y=True)

    editor_col = sg.Column(layout=[[input_frame], [actions_frame], [output_frame]], expand_y=True)

    def __init__(self):

        # Root GUI layout
        self.layout = [
            [self.viewer_col, self.editor_col],
        ]

        # Current editor action (Crop)
        self.action = None

        # x,y points (top left, bottom left, top right, bottom right)
        self.crop_cords = []

        self.orignal_image = None
        self.viewer_image = None

        self.window = sg.Window('PyJig', self.layout)

    def render(self):
        while True:
            event, values = self.window.read()
            if event == sg.WIN_CLOSED or event == 'Exit':
                break
            infile = values['-IN-']
            if event == '-IN-':
                if os.path.isfile(infile):
                    # Read file
                    self.orignal_image = Image.open(infile)
                    self.window['-ORIG WIDTH-'].update(self.orignal_image.size[0])
                    self.window['-ORIG HEIGHT-'].update(self.orignal_image.size[1])

                    # Resize to static size
                    self.viewer_image = resize_file(infile, (1500, 840))
                    self.window['-NEW WIDTH-'].update(self.viewer_image.size[0])
                    self.window['-NEW HEIGHT-'].update(self.viewer_image.size[1])

                    # Set viewer image
                    self.draw_viewer_image(self.viewer_image)

            if '-GRAPH-' in event:
                self.handle_graph_event(event, values)
            if event == 'Crop':
                self.handle_crop_button_event(event, values)
            if event == 'Grid':
                self.handle_grid_button_event(event, values)
            if event == 'Search':
                self.handle_search_button_event(event, values)

        self.window.close()

    def handle_graph_event(self, event, values):
        xy_cords = values.get("-GRAPH-", None)
        print(f'Mouse clicked at {xy_cords}')

        # Store X,Y cords if cropping
        if self.action == 'Crop':
            self.crop_cords.append(xy_cords)
            print(f'Stored crop cords: {xy_cords}')

            if len(self.crop_cords) == 2:
                self.viewer_image = resize(self.viewer_image.crop(
                    (self.crop_cords[0][0], self.crop_cords[0][1], self.crop_cords[1][0], self.crop_cords[1][1])), (1500, 840))
                self.draw_viewer_image(self.viewer_image)
                self.crop_cords = []
                self.action = None

    def handle_crop_button_event(self, event, values):
        if self.action:
            self.action = None
            self.crop_cords = []
        else:
            self.action = 'Crop'
            print('Entering cropping mode, click on the 2 corners of the puzzle (top left, bottom right)')

    def handle_search_button_event(self, event, values):
        layout = [
            [sg.Input(key='-IN-SEARCH-', enable_events=True), sg.FileBrowse()]
        ]

        window = sg.Window('Draw grid', layout)
        event, values = window.read()
        window.close()

        self.graph.DrawRectangle((200, 200), (230, 230), line_color="red", line_width=3)

    def handle_grid_button_event(self, event, values):
        layout = [
            [sg.Text('Please enter some information about the jigsaw puzzle')],
            [sg.Text('Total pieces', size=(15, 1)), sg.InputText()],
            [sg.Text('Width pieces', size=(15, 1)), sg.InputText()],
            [sg.Text('Height pieces', size=(15, 1)), sg.InputText()],
            [sg.Submit(), sg.Cancel()]
        ]

        window = sg.Window('Draw grid', layout)
        event, values = window.read()
        window.close()

        puzzle_total = values[0]
        puzzle_width = values[1]
        puzzle_height = values[2]

        print(f'Total puzzle pieces: {puzzle_total} = (width: {puzzle_width} * height: {puzzle_height})')

    def draw_viewer_image(self, image, pos=(0, 0)):
        bio = io.BytesIO()
        image.save(bio, format="PNG")
        self.window["-GRAPH-"].draw_image(data=bio.getvalue(), location=pos)

    def slice_2d_grid(self, image, width, height):
        # TODO: Impl
        print()
