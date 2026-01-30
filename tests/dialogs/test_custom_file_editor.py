"""Tests for the custom file editor."""

import logging
import tempfile
from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest
from PyQt6 import Qsci, QtWidgets
from ratapi.utils.enums import Languages

from rascal2.dialogs.custom_file_editor import CustomFileEditorDialog, edit_file, edit_file_matlab

parent = QtWidgets.QMainWindow()


@pytest.fixture
def custom_file_dialog():
    """Fixture for a custom file dialog."""
    dlg = CustomFileEditorDialog(parent)
    yield dlg
    dlg.reject()


@pytest.fixture
def temp_file():
    with tempfile.NamedTemporaryFile("w+", suffix=".py", delete=False) as f:
        f.write("Test text for a test dialog!")
        f.flush()
        yield Path(f.name)
        f.close()


@patch("rascal2.dialogs.custom_file_editor.CustomFileEditorDialog.show")
def test_edit_file(exec_mock):
    """Test that the dialog is executed when edit_file() is called on a valid file."""
    with tempfile.TemporaryDirectory() as tmp:
        file = Path(tmp, "testfile.py")
        file.touch()
        edit_file(file, Languages.Python, parent)

        exec_mock.assert_called_once()


@pytest.mark.parametrize("filepath", ["dir/", "not_there.m"])
@patch("rascal2.dialogs.custom_file_editor.CustomFileEditorDialog")
def test_edit_incorrect_file(dialog_mock, filepath, caplog):
    """A logger error should be emitted if a directory or nonexistent file is given to the editor."""
    with tempfile.TemporaryDirectory() as tmp:
        file = Path(tmp, filepath)
        edit_file(file, Languages.Python, parent)

    errors = [record for record in caplog.get_records("call") if record.levelno == logging.ERROR]
    assert len(errors) == 1
    assert "Attempted to edit a custom file which does not exist!" in caplog.text


@patch("rascal2.dialogs.custom_file_editor.MatlabHelper", autospec=True)
def test_edit_file_matlab(mock_matlab):
    """Assert that a file is passed to the engine when the MATLAB editor is called."""
    mock_engine = MagicMock()
    mock_engine.edit = MagicMock()
    mock_helper = MagicMock()
    mock_helper.get_local_engine = MagicMock(return_value=mock_engine)
    mock_matlab.return_value = mock_helper
    with tempfile.TemporaryDirectory() as tmp:
        file = Path(tmp, "testfile.m")
        file.touch()
        edit_file_matlab(file)

    mock_helper.get_local_engine.assert_called_once()
    mock_engine.edit.assert_called_once_with(str(file))


@patch("rascal2.dialogs.custom_file_editor.MatlabHelper", autospec=True)
def test_edit_no_matlab_engine(mock_matlab, caplog):
    """A logging error should be produced if a user tries to edit a file in MATLAB with no engine available."""
    mock_helper = MagicMock()
    mock_helper.get_local_engine = MagicMock(side_effect=ValueError)
    mock_matlab.return_value = mock_helper
    with tempfile.TemporaryDirectory() as tmp:
        file = Path(tmp, "testfile.m")
        file.touch()
        edit_file_matlab(file)
    mock_helper.get_local_engine.assert_called_once()

    errors = [record for record in caplog.get_records("call") if record.levelno == logging.ERROR]
    assert len(errors) == 1
    assert "Attempted to edit a file in MATLAB engine" in caplog.text


@pytest.mark.parametrize(
    "language, expected_lexer",
    [(Languages.Python, Qsci.QsciLexerPython), (Languages.Matlab, Qsci.QsciLexerMatlab), (None, type(None))],
)
def test_dialog_init(custom_file_dialog, temp_file, language, expected_lexer):
    """Ensure the custom file editor is set up correctly."""
    custom_file_dialog.open_file(temp_file, language)

    assert isinstance(custom_file_dialog.editor.lexer(), expected_lexer)
    assert custom_file_dialog.editor.text() == "Test text for a test dialog!"


@patch("rascal2.dialogs.custom_file_editor.LOGGER")
@patch("rascal2.dialogs.custom_file_editor.QtWidgets.QMessageBox")
def test_dialog_save(mock_msg_box, mock_logger, custom_file_dialog):
    """Text changes to the editor are saved to the file when save_file is called."""
    temp_file = MagicMock()
    temp_file.read_text = MagicMock(return_value="This is a test")

    custom_file_dialog.open_file(temp_file, Languages.Python)

    assert not custom_file_dialog.is_modified

    # No changes so no save
    custom_file_dialog.save_file()
    temp_file.write_text.assert_not_called()
    custom_file_dialog.unchanged_text = temp_file.read_text()

    custom_file_dialog.editor.setText("New test text...")

    assert custom_file_dialog.is_modified

    temp_file.is_relative_to = MagicMock(return_value=True)  # file is relative to example dir
    # No save in example dir
    custom_file_dialog.save_file()
    mock_msg_box.warning.assert_called_once()
    temp_file.write_text.assert_not_called()
    custom_file_dialog.unchanged_text = temp_file.read_text()

    temp_file.is_relative_to = MagicMock(return_value=False)
    custom_file_dialog.save_file()
    temp_file.write_text.assert_called_once()
    assert not custom_file_dialog.is_modified
    custom_file_dialog.unchanged_text = temp_file.write_text.call_args[0]

    temp_file.write_text = MagicMock(side_effect=OSError)
    custom_file_dialog.save_file()
    mock_logger.error.assert_called_once()
    mock_msg_box.critical.assert_called_once()


@patch("rascal2.dialogs.custom_file_editor.QtWidgets.QMessageBox.question")
def test_save_changes_when_opening_file(mock_msg_box, custom_file_dialog, temp_file):
    """Text changes to the editor are saved to the file when save_file is called."""
    custom_file_dialog.open_file(temp_file, Languages.Python)

    custom_file_dialog.editor.setText("New test text...")

    # Opening the same file should not trigger a save warning
    custom_file_dialog.open_file(temp_file, Languages.Python)

    mock_msg_box.assert_not_called()
    assert temp_file.read_text() != "New test text..."

    with tempfile.TemporaryDirectory() as tmp:
        new_file = Path(tmp, "filename.py")
        new_file.write_text("This is a new file")
        mock_msg_box.return_value = QtWidgets.QMessageBox.StandardButton.Save
        # Changing the file should save old file if user selects save in msg box
        custom_file_dialog.open_file(new_file, Languages.Python)
        mock_msg_box.assert_called_once()
        assert temp_file.read_text() == "New test text..."

        custom_file_dialog.editor.setText("Another test text...")
        mock_msg_box.return_value = QtWidgets.QMessageBox.StandardButton.Discard
        # Changes should be discarded as user selected discard in msg box
        custom_file_dialog.open_file(temp_file, Languages.Python)
        assert new_file.read_text() == "This is a new file"
