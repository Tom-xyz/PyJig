import sys
import io

from PIL import Image

# from gui.elements import search_piece_window
from gui.elements import viewer_canvas_size
from src.utils.img_utils import resize, cut_image_to_grid


def handle_None_event(*_):
    sys.exit(0)


def handle_Exit_event(*_):
    sys.exit(0)


def handle_input_image_event(context, event, values):
    infile = values['input_image']
    original_image = Image.open(infile)
    viewer_image = resize(original_image, viewer_canvas_size)

    context.set('original_image', original_image)
    context.set('viewer_image', viewer_image)

    context.window['original_img_width'].update(original_image.size[0])
    context.window['original_img_height'].update(original_image.size[1])
    context.window['new_img_width'].update(viewer_image.size[0])
    context.window['new_img_height'].update(viewer_image.size[1])

    draw_viewer_image(context, viewer_image)


def handle_input_piece_event(context, event, values):
    print('Searching for piece')

    infile = values['input_piece']
    original_piece_image = Image.open(infile)
    viewer_piece_image = resize(original_piece_image, viewer_canvas_size)

    print('Scaled piece image to Jigsaw puzzle')

    # puzzle.grid.search()

    piece_x_pos = (0, 0)
    piece_y_pos = (0, 0)
    viewer = context.window['viewer']
    viewer.DrawRectangle((200, 200), (230, 230), line_color="red", line_width=3)

    print(f'Found piece match at ({piece_x_pos}, {piece_y_pos})')


def handle_viewer_event(context, event, values):
    click_xy_cords = values.get('viewer', None)
    print(f'Mouse clicked at {click_xy_cords}')

    action = context.get('action')
    crop_cords = context.get('crop_cords')
    viewer_image = context.get('viewer_image')

    crop_cords.append(click_xy_cords)

    if action == 'crop' and len(crop_cords) == 2:
        cropped_image = resize(viewer_image.crop((crop_cords[0][0], crop_cords[0][1], crop_cords[1][0], crop_cords[1][1])), viewer_canvas_size)
        draw_viewer_image(context, cropped_image)
        context.set('crop_cords', [])
        action = None
        print(f'Succesfully cropped image')


def handle_button_crop_event(context, event, values):
    context.set('action', 'crop')
    context.set('crop_cords', [])
    print('Entered cropping mode, click on the 2 corners of the puzzle (top left, bottom right)')


def handle_button_grid_event(context, event, values):
    grid_image = cut_image_to_grid(context.get('viewer_image'))
    draw_viewer_image(context, grid_image)


def draw_viewer_image(context, image, pos=(0, 0)):
    bio = io.BytesIO()
    image.save(bio, format="PNG")
    context.set('viewer_image', image)
    context.window["viewer"].draw_image(data=bio.getvalue(), location=pos)
