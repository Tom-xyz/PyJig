import io
import sys

import cv2 as cv
import numpy as np

from PIL import Image

# from gui.elements import search_piece_window
from core.experiments.img_contour_crop import contour_crop
from gui.elements import pv_canvas_size, jv_canvas_size
from src.utils.img_utils import resize, cut_image_to_grid, run_SIFT_search, run_ORB_search


def handle_None_event(*_):
    sys.exit(0)


def handle_Exit_event(*_):
    sys.exit(0)


def handle_input_image_event(context, event, values):
    infile = values['input_image']
    original_image = Image.open(infile)
    viewer_image = resize(original_image, jv_canvas_size)

    context.set('original_image', original_image)
    context.set('viewer_image', viewer_image)

    context.window['original_img_width'].update(original_image.size[0])
    context.window['original_img_height'].update(original_image.size[1])
    context.window['new_img_width'].update(viewer_image.size[0])
    context.window['new_img_height'].update(viewer_image.size[1])

    draw_image('viewer', context, viewer_image)


def handle_input_piece_event(context, event, values):
    print('Searching for piece')

    infile = values['input_piece']
    original_piece_image = cv.imread(infile)

    p_image = contour_crop(np.array(original_piece_image))
    p_image_resized = resize(p_image, pv_canvas_size)

    j_image = context.get('viewer_image')
    draw_image('piece_viewer', context, p_image_resized)
    mode = context.get('mode', 'ORB')

    print(f'Searching for piece, mode: {mode}')
    img_with_matches = search_for_piece(j_image, p_image, mode=mode)
    draw_image('viewer', context, img_with_matches)


def handle_viewer_event(context, event, values):
    click_xy_cords = values.get('viewer', None)
    print(f'Mouse clicked at {click_xy_cords}')

    action = context.get('action')
    crop_cords = context.get('crop_cords')
    viewer_image = context.get('viewer')

    crop_cords.append(click_xy_cords)

    if action == 'crop' and len(crop_cords) == 2:
        cropped_image = resize(
            viewer_image.crop((crop_cords[0][0], crop_cords[0][1], crop_cords[1][0], crop_cords[1][1])),
            jv_canvas_size)
        draw_image('viewer', context, cropped_image)
        context.set('crop_cords', [])
        print('Successfully cropped image')


def handle_button_crop_event(context, event, values):
    context.set('crop_cords', [])

    if context.get('action') == 'crop':
        context.set('action', None)
        print('Exited cropping mode')
    else:
        context.set('action', 'crop')
        print('Entered cropping mode, click on the 2 corners of the puzzle (top left, bottom right)')


def handle_button_grid_event(context, event, values):
    grid_image = cut_image_to_grid(context.get('viewer'))
    draw_image('viewer', context, grid_image)


def handle_button_SIFT_event(context, event, values):
    print('Set mode to SIFT')
    context.set('mode', 'SIFT')


def handle_button_ORB_event(context, event, values):
    print('Set mode to ORB ')
    context.set('mode', 'ORB')


# TODO: Replace with Jigsaw.search()
def search_for_piece(j_image, p_image, mode='ORB'):
    # TODO: Determine appropriate color mode
    # TODO: Remove this, causes image loss
    j_image = cv.cvtColor(np.array(j_image), cv.COLOR_RGB2BGR)
    p_image = cv.cvtColor(np.array(p_image), cv.COLOR_RGB2BGR)

    if mode == 'ORB':
        return run_ORB_search(j_image, p_image)
    elif mode == 'SIFT':
        return run_SIFT_search(j_image, p_image)
    else:
        raise Exception(f'Invalid mode specified: {mode}')


def draw_image(key, context, image, pos=(0, 0)):
    bio = io.BytesIO()
    image.save(bio, format="PNG")
    context.set(key, image)
    context.window[key].draw_image(data=bio.getvalue(), location=pos)
