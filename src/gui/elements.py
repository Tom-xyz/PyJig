import PySimpleGUI as sg


def build_default_frame(title, layout, expand_y=True, expand_x=True):
    return sg.Frame(title, layout, expand_y=expand_y, expand_x=expand_x)


def build_default_column(layout, expand_y=True, expand_x=True):
    return sg.Column(layout, expand_y=expand_y, expand_x=expand_x)


# DEFAULT THEME #
sg.theme('DarkAmber')

# GUI Frames #
input_frame = build_default_frame('Input', [
    [sg.Input(key='input_image', enable_events=True), sg.FileBrowse()],
    [sg.T('Original size'), sg.T(k='original_img_height'), sg.T('X'), sg.T(k='original_img_width')],
    [sg.T('Resized size'), sg.T(k='new_img_width'), sg.T('X'), sg.T(k='new_img_height')]
])

# LEFT COL #
graph = sg.Graph(
    canvas_size=(1500, 840),
    graph_bottom_left=(0, 840),
    graph_top_right=(1500, 0),
    key='sg_graph',
    enable_events=True
)
viewer_frame = build_default_frame('Jigsaw Viewer', [[graph]])

# RIGHT COL #
actions_frame = build_default_frame('Actions', [
    [sg.Button(button_text='crop'), sg.Button(button_text='grid'), sg.Button(button_text='search')]
])
log_frame = build_default_frame('Log', [
    [sg.Output(key='log', expand_y=True, expand_x=True)]
])

# GUI COLs #
viewer_col = build_default_column([[viewer_frame]])
editor_col = build_default_column([[input_frame], [actions_frame], [log_frame]])

# EDITOR WINDOWS #
grid_window = sg.Window('Search piece', [
    [sg.Text('Please enter some information about the jigsaw puzzle')],
    [sg.Text('Total pieces', size=(15, 1)), sg.InputText()],
    [sg.Text('Width pieces', size=(15, 1)), sg.InputText()],
    [sg.Text('Height pieces', size=(15, 1)), sg.InputText()],
    [sg.Submit(), sg.Cancel()]
])
search_piece_window = sg.Window('Draw grid', [
    [sg.Input(key='search_image', enable_events=True), sg.FileBrowse()]
])
