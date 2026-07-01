from unittest.mock import Mock, patch
from urllib.error import HTTPError, URLError

import pytest
from PyQt6 import QtWidgets

from rascal2.dialogs.check_update_dialog import CheckUpdateDialog
from tests.utils import TestWorker


@pytest.fixture
def update_dialog():
    with (
        patch("rascal2.dialogs.check_update_dialog.logging", autospec=True) as log_mock,
        patch("rascal2.dialogs.check_update_dialog.Worker", TestWorker),
    ):
        dialog = CheckUpdateDialog(QtWidgets.QMainWindow())
        dialog.show = Mock()
        dialog.logger = log_mock

        yield dialog


@patch("rascal2.dialogs.check_update_dialog.urllib.request.urlopen", autospec=True)
def test_check_for_update(urlopen_mock, update_dialog, global_setting):
    global_setting.setValue("check_update_on_start", False)
    update_dialog.check(True)
    urlopen_mock.assert_not_called()

    test_version = "2.0.0"
    with patch("rascal2.dialogs.check_update_dialog.RASCAL2_VERSION", test_version):
        global_setting.setValue("check_update_on_start", True)
        urlopen_mock.return_value.__enter__.return_value.read.return_value = '{"tag_name":""}'
        update_dialog.check(True)
        update_dialog.show.assert_not_called()  # No tag so no update
        urlopen_mock.return_value.__enter__.return_value.read.return_value = '{"tag_name":"2.0.0"}'
        update_dialog.check(True)
        update_dialog.show.assert_not_called()  # same tag so no update
        urlopen_mock.return_value.__enter__.return_value.read.return_value = '{"tag_name":"3.0.0"}'
        update_dialog.check(True)
        update_dialog.show.assert_called_once()  # same tag so no update

    urlopen_mock.return_value.__enter__.return_value.read.return_value = '{"tag_name":"0.0.0a"}'
    update_dialog.worker.isRunning = Mock(return_value=True)
    update_dialog.worker.terminate = Mock()
    update_dialog.check()
    assert update_dialog.result.text() == "You are running the latest version of RasCAL-2.\n"
    assert update_dialog.show.call_count == 2
    update_dialog.close()
    update_dialog.worker.terminate.assert_called()


@patch("rascal2.dialogs.check_update_dialog.urllib.request.urlopen", autospec=True)
def test_check_update_exception(urlopen_mock, update_dialog, global_setting):
    global_setting.setValue("check_update_on_start", "True")
    urlopen_mock.return_value.__enter__.return_value.read.return_value = '{"tag_name":"2.0.0"}'
    update_dialog.worker.side_effect = HTTPError("", 400, "", {}, None)
    update_dialog.check(True)
    assert update_dialog.result.text() == ""
    assert update_dialog.logger.error.call_count == 1
    assert update_dialog.show.call_count == 0

    update_dialog.check()
    assert update_dialog.result.text() == "You are running the latest version of RasCAL-2.\n"
    assert update_dialog.logger.error.call_count == 2
    assert update_dialog.show.call_count == 1

    update_dialog.worker.side_effect = URLError("")
    update_dialog.check()
    assert update_dialog.result.text() == (
        "An error occurred when attempting to connect to the update server. "
        "Check your internet connection and/or firewall and try again.\n"
    )
    assert update_dialog.logger.error.call_count == 3
    assert update_dialog.show.call_count == 2

    update_dialog.worker.side_effect = ValueError("blah")
    update_dialog.check()
    assert update_dialog.result.text() == "An unexpected error occurred when checking for updates: blah\n"
    assert update_dialog.logger.error.call_count == 4
    assert update_dialog.show.call_count == 3
