from unittest.mock import patch, Mock

import pytest
from PIL import Image

from pyjig.gui.event_handlers import handle_input_piece_event

test_jigsaw_image = Image.new("RGB", (64, 64), (255, 255, 255))
test_piece_image = Image.new("RGB", (4, 4), (255, 255, 255))

test_context = {
    'viewer_image': test_jigsaw_image
}
test_values = {}


@pytest.fixture()
def input_piece():
    mock_load_img = Mock()
    mock_contour_crop = Mock()
    mock_resize_img = Mock()
    mock_draw_img = Mock()
    mock_search_img = Mock()

    mock_resize_img.return_value = test_piece_image
    mock_contour_crop.return_value = test_piece_image

    @patch('pyjig.gui.event_handlers.draw_image', new=mock_draw_img)
    @patch('pyjig.gui.event_handlers.search_for_piece', new=mock_search_img)
    @patch('pyjig.gui.event_handlers.resize', new=mock_resize_img)
    @patch('pyjig.gui.event_handlers.contour_crop', new=mock_contour_crop)
    @patch('pyjig.gui.event_handlers.load_img_from_input', new=mock_load_img)
    def ut():
        return handle_input_piece_event(test_context, test_values)

    return ut, mock_load_img, mock_search_img, mock_draw_img


def test_handle_input_piece_displays_image(input_piece):
    ut, m_load_img, *_ = input_piece
    m_load_img.return_value = test_piece_image

    ut()

    m_load_img.assert_called_once_with('input_piece', test_values)


def test_handle_input_piece_handles_no_image(input_piece):
    ut, m_load_img, m_search_img, m_draw_img, *_ = input_piece
    m_load_img.return_value = None

    ut()

    m_search_img.assert_not_called()
    m_draw_img.assert_not_called()


def test_handle_input_piece_invokes_search(input_piece):
    ut, m_load_img, m_search_img, *_ = input_piece
    m_load_img.return_value = test_piece_image

    ut()

    m_search_img.assert_called_once_with(test_jigsaw_image, test_piece_image, mode='ORB')
