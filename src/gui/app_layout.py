import PySimpleGUI as sg

# GUI Frames #
input_frame = sg.Frame(
    title='Input Image',
    layout=[
        [sg.Input(key='input_image', enable_events=True), sg.FileBrowse()],
        [sg.T('Original size'), sg.T(k='-ORIG WIDTH-'), sg.T('X'), sg.T(k='-ORIG HEIGHT-')],
        [sg.T('Resized size'), sg.T(k='-NEW WIDTH-'), sg.T('X'), sg.T(k='-NEW HEIGHT-')]
    ],
    expand_x=True
)

actions_frame = sg.Frame(
    title='Actions',
    layout=[
        [sg.Button(button_text='crop'), sg.Button(button_text='grid'), sg.Button(button_text='search')],
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
    key="sg_graph",
    enable_events=True
)

viewer_frame = sg.Frame(
    title='Jigsaw Viewer',
    layout=[
        [graph]
    ]
)

# GUI Main Window Columns #
viewer_col = sg.Column(layout=[[viewer_frame]], expand_y=True)
editor_col = sg.Column(layout=[[input_frame], [actions_frame], [output_frame]], expand_y=True)
