import sys
import PySimpleGUI as sg
import io

from PIL import Image
from utils.img_utils import resize, resize_file, cut_image_to_grid


def handle_None_event(context, event, values):
    sys.exit(0)


def handle_Exit_event(context, event, values):
    sys.exit(0)


def handle_input_image_event(context, event, values):
    infile = values['input_image']
    # Read file
    context.orignal_image = Image.open(infile)
    context.window['-ORIG WIDTH-'].update(context.orignal_image.size[0])
    context.window['-ORIG HEIGHT-'].update(context.orignal_image.size[1])
    # Resize to static size
    context.viewer_image = resize_file(infile, (1500, 840))
    context.window['-NEW WIDTH-'].update(context.viewer_image.size[0])
    context.window['-NEW HEIGHT-'].update(context.viewer_image.size[1])
    # Set viewer image
    draw_viewer_image(context, context.viewer_image)


def handle_sg_graph_event(context, event, values):
    xy_cords = values.get('sg_graph', None)
    print(f'Mouse clicked at {xy_cords}')
    if context.action == 'crop':
        context.crop_cords.append(xy_cords)
        print(f'Stored crop cords: {xy_cords}')
        if len(context.crop_cords) == 2:
            context.viewer_image = resize(context.viewer_image.crop(
                (context.crop_cords[0][0], context.crop_cords[0][1], context.crop_cords[1][0], context.crop_cords[1][1])), (1500, 840))
            draw_viewer_image(context, context.viewer_image)
            context.crop_cords = []
            context.action = None


def handle_crop_event(context, event, values):
    if context.action:
        context.action = None
        context.crop_cords = []
    else:
        context.action = 'crop'
        print('Entering cropping mode, click on the 2 corners of the puzzle (top left, bottom right)')


def handle_search_event(context, event, values):
    layout = [
        [sg.Input(key='-IN-SEARCH-', enable_events=True), sg.FileBrowse()]
    ]
    window = sg.Window('Draw grid', layout)
    event, values = window.read()
    window.close()
    graph = context.window['sg_graph']
    graph.DrawRectangle((200, 200), (230, 230), line_color="red", line_width=3)


def handle_grid_event(context, event, values):
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
    print(f'Drawing grid: Total puzzle pieces: {puzzle_total} = (width: {puzzle_width} * height: {puzzle_height})')
    grid_image = cut_image_to_grid(context.viewer_image)
    draw_viewer_image(context, grid_image)


def draw_viewer_image(context, image, pos=(0, 0)):
    bio = io.BytesIO()
    image.save(bio, format="PNG")
    context.window["sg_graph"].draw_image(data=bio.getvalue(), location=pos)
