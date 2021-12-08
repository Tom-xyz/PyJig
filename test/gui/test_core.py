from unittest import mock
from unittest.mock import Mock

import pytest
from PySimpleGUI import Window

from src.gui.core import PyJigGUI


@pytest.fixture()
def gui():
    gui: PyJigGUI

    with mock.patch('PySimpleGUI.Window') as mock_window:
        mock_gui_window = Mock()
        mock_window.return_value = mock_gui_window
        mock_gui_window.read.return_value = ('debug', 'test_value')
        gui = PyJigGUI()

    mock_active = Mock()
    mock_active.side_effect = [True, False]
    gui._is_active = mock_active

    return gui


def test_gui_contains_main_window():
    ut = PyJigGUI()
    assert isinstance(ut.window, Window)


def test_gui_render_calls_read_window(gui):
    gui.render()
    gui.window.read.assert_called_once()
