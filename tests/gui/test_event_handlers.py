from unittest.mock import patch, Mock, MagicMock

import pytest
from PIL import Image

from pyjig.gui.constants import INPUT_J_IMG_KEY, INPUT_P_IMG_KEY
from pyjig.gui.context import WindowContext
from pyjig.gui.elements import jv_canvas_size
from pyjig.gui.event_handlers import handle_input_piece_event, handle_None_event, handle_Exit_event, \
    handle_input_jigsaw_event

test_jigsaw_image = Image.new("RGB", (64, 64), (255, 255, 255))
test_piece_image = Image.new("RGB", (4, 4), (255, 255, 255))

mock_window = MagicMock()
test_context = WindowContext(mock_window)

test_values = {}


@patch('pyjig.gui.event_handlers.sys.exit')
def test_handle_None_event_exits(mock_sys_exit):
    handle_None_event(test_context, test_values)
    mock_sys_exit.assert_called_once()


@patch('pyjig.gui.event_handlers.sys.exit')
def test_handle_Exit_event_exits(mock_sys_exit):
    handle_Exit_event(test_context, test_values)
    mock_sys_exit.assert_called_once()


@pytest.fixture()
def input_image():
    mock_load_img = Mock()
    mock_contour_crop = Mock()
    mock_resize_img = Mock()
    mock_draw_img = Mock()

    mock_resize_img.return_value = test_jigsaw_image
    mock_contour_crop.return_value = test_jigsaw_image
    mock_load_img.return_value = test_jigsaw_image

    @patch('pyjig.gui.event_handlers.draw_image', new=mock_draw_img)
    @patch('pyjig.gui.event_handlers.resize', new=mock_resize_img)
    @patch('pyjig.gui.event_handlers.contour_crop', new=mock_contour_crop)
    @patch('pyjig.gui.event_handlers.load_img_from_input', new=mock_load_img)
    def ut():
        return handle_input_jigsaw_event(test_context, test_values)

    return ut, mock_load_img, mock_resize_img, mock_draw_img


def test_handle_input_image_displays_image(input_image):
    handle_input_image, m_load_img, m_resize_img, m_draw_img = input_image

    handle_input_image()

    m_load_img.assert_called_once_with(INPUT_J_IMG_KEY, test_values)
    m_resize_img.assert_called_once_with(test_jigsaw_image, jv_canvas_size)
    m_draw_img.assert_called_once_with('viewer', test_context, test_jigsaw_image)


@pytest.fixture()
def input_piece():
    mock_load_img = Mock()
    mock_contour_crop = Mock()
    mock_resize_img = Mock()
    mock_draw_img = Mock()
    mock_search_img = Mock()

    mock_resize_img.return_value = test_piece_image
    mock_contour_crop.return_value = test_piece_image

    test_context.set('viewer_image', test_jigsaw_image)

    @patch('pyjig.gui.event_handlers.draw_image', new=mock_draw_img)
    @patch('pyjig.gui.event_handlers.search_for_piece', new=mock_search_img)
    @patch('pyjig.gui.event_handlers.resize', new=mock_resize_img)
    @patch('pyjig.gui.event_handlers.contour_crop', new=mock_contour_crop)
    @patch('pyjig.gui.event_handlers.load_img_from_input', new=mock_load_img)
    def ut():
        return handle_input_piece_event(test_context, test_values)

    return ut, mock_load_img, mock_search_img, mock_draw_img


def test_handle_input_piece_displays_image(input_piece):
    handle_input_piece, m_load_img, *_ = input_piece
    m_load_img.return_value = test_piece_image

    handle_input_piece()

    m_load_img.assert_called_once_with(INPUT_P_IMG_KEY, test_values)


def test_handle_input_piece_handles_no_image(input_piece):
    handle_input_piece, m_load_img, m_search_img, m_draw_img, *_ = input_piece
    m_load_img.return_value = None

    handle_input_piece()

    m_search_img.assert_not_called()
    m_draw_img.assert_not_called()


def test_handle_input_piece_invokes_search(input_piece):
    handle_input_piece, m_load_img, m_search_img, *_ = input_piece
    m_load_img.return_value = test_piece_image

    handle_input_piece()

    m_search_img.assert_called_once_with(test_jigsaw_image, test_piece_image, mode='ORB')
