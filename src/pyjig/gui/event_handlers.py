import io
import sys

# from gui.elements import search_piece_window
from pyjig.gui.constants import ORIGINAL_IMG_WIDTH, ORIGINAL_IMG_HEIGHT, \
    NEW_IMG_WIDTH, NEW_IMG_HEIGHT, J_IMG, VIEWER_J_IMG, INPUT_J_IMG_KEY, INPUT_P_IMG_KEY
from pyjig.gui.elements import pv_canvas_size, jv_canvas_size
from pyjig.utils.img_utils import resize, cut_image_to_grid, run_SIFT_search, run_ORB_search, contour_crop, \
    convert_to_cv_img, load_img_from_input


def handle_None_event(*_):
    sys.exit(0)


def handle_Exit_event(*_):
    sys.exit(0)


def handle_input_jigsaw_event(context, values):
    original_image = load_img_from_input(INPUT_J_IMG_KEY, values)
    if original_image is None:
        return

    viewer_image = resize(original_image, jv_canvas_size)

    context.set(J_IMG, original_image)
    context.set(VIEWER_J_IMG, viewer_image)

    context.window[ORIGINAL_IMG_WIDTH].update(original_image.size[0])
    context.window[ORIGINAL_IMG_HEIGHT].update(original_image.size[1])
    context.window[NEW_IMG_WIDTH].update(viewer_image.size[0])
    context.window[NEW_IMG_HEIGHT].update(viewer_image.size[1])

    draw_image('viewer', context, viewer_image)


def handle_input_piece_event(context, values):
    original_piece_image = load_img_from_input(INPUT_P_IMG_KEY, values)
    if original_piece_image is None:
        return

    p_image = contour_crop(original_piece_image)
    p_image_resized = resize(p_image, pv_canvas_size)
    p_image_resized_2 = resize(p_image, (100, 100))

    j_image = context.get(J_IMG)
    draw_image('piece_viewer', context, p_image_resized)
    mode = context.get('mode', 'ORB')

    print(f'Searching for piece, mode: {mode}')
    img_with_matches = search_for_piece(j_image, p_image_resized_2, mode=mode)
    img_with_matches = resize(img_with_matches, jv_canvas_size)
    draw_image('viewer', context, img_with_matches)


def handle_viewer_event(context, values):
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
        context.set('viewer_image', cropped_image)
        print('Successfully cropped image')


def handle_piece_viewer_event(context, values):
    click_xy_cords = values.get('piece_viewer', None)
    print(f'Mouse clicked at {click_xy_cords}')


def handle_button_crop_event(context, values):
    context.set('crop_cords', [])

    if context.get('action') == 'crop':
        context.set('action', None)
        print('Exited cropping mode')
    else:
        context.set('action', 'crop')
        print('Entered cropping mode, click on the 2 corners of the puzzle (top left, bottom right)')


def handle_button_grid_event(context, values):
    grid_image = cut_image_to_grid(context.get('viewer'))
    draw_image('viewer', context, grid_image)


def handle_button_SIFT_event(context, values):
    print('Set mode to SIFT')
    context.set('mode', 'SIFT')


def handle_button_ORB_event(context, values):
    print('Set mode to ORB ')
    context.set('mode', 'ORB')


# TODO: Impl zoom on graph hover
def handle_mouse_Hover_event(context, values):
    print("Mouse hover event: TODO")


def handle_test_event(context, values):
    print(f'Got test event, values: {values}')


# TODO: Replace with Jigsaw.search()
def search_for_piece(j_image, p_image, mode='ORB'):
    print('Searching for piece')
    j_image = convert_to_cv_img(j_image)
    p_image = convert_to_cv_img(p_image)

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
