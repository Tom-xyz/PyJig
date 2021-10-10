import io

from utils import resize
import PySimpleGUI as sg
from PIL import Image

import os


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
        [sg.Button(button_text='Crop')]
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
    canvas_size=(1500, 800),
    graph_bottom_left=(0, 0),
    graph_top_right=(1500, 800),
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


def main():
    layout = [
        [viewer_col, editor_col],
    ]

    window = sg.Window('PyJig', layout)

    while True:
        event, values = window.read()
        # print(event, values) ENABLE TO SEE ALL EVENTS
        if event == sg.WIN_CLOSED or event == 'Exit':
            break
        infile = values['-IN-']
        if event == '-IN-':
            if os.path.isfile(infile):
                # Read file
                image = Image.open(infile)
                window['-ORIG WIDTH-'].update(image.size[0])
                window['-ORIG HEIGHT-'].update(image.size[1])

                # Resize to static size
                image = resize(infile, (1500, 800))
                window['-NEW WIDTH-'].update(image.size[0])
                window['-NEW HEIGHT-'].update(image.size[1])

                # Set viewer image
                bio = io.BytesIO()
                image.save(bio, format="PNG")
                window["-GRAPH-"].draw_image(data=bio.getvalue(), location=(0, 800))
        elif '-GRAPH-' in event:
            print(f'Mouse clicked at {values.get("-GRAPH-", None)}')

    window.close()


if __name__ == '__main__':
    main()
