import json
import logging
import urllib.request
from urllib.error import HTTPError, URLError

from packaging.version import Version
from PyQt6 import QtCore, QtWidgets

from rascal2 import RASCAL2_VERSION
from rascal2.core.worker import Worker
from rascal2.settings import get_global_settings

RELEASES_URL = "https://github.com/RascalSoftware/RasCAL-2/releases"
UPDATE_URL = "https://api.github.com/repos/RascalSoftware/RasCAL-2/releases/latest"


def get_check_on_start_setting():
    """Get the `check_update_on_start` setting.

    When loaded from file, QSetting will not cast back to boolean so this function
    ensures the returned setting is a boolean.

    Returns
    -------
    check_on_start: bool
        Indicates if updates should be checked for  on startup

    """
    check_on_start = get_global_settings().value("check_update_on_start", True)
    if isinstance(check_on_start, str):
        check_on_start = check_on_start.lower() == "true"
    return check_on_start


class CheckUpdateDialog(QtWidgets.QDialog):
    """Dialog for checking software updates.

    Parameters
    ----------
    parent : QtWidgets.QWidget
        The parent of this widget.
    """

    def __init__(self, parent):
        super().__init__(parent)

        self.startup = False
        self.parent = parent
        self.setFixedSize(400, 200)
        self.setWindowTitle("Check for Update")

        main_layout = QtWidgets.QVBoxLayout()
        self.setLayout(main_layout)

        self.stack = QtWidgets.QStackedLayout()
        main_layout.addLayout(self.stack)
        self.stack.addWidget(QtWidgets.QWidget())
        self.stack.addWidget(QtWidgets.QWidget())

        progress_bar = QtWidgets.QProgressBar()
        progress_bar.setTextVisible(False)
        progress_bar.setMinimum(0)
        progress_bar.setMaximum(0)

        message = QtWidgets.QLabel("Checking the Internet for Updates")
        message.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)

        sub_layout = QtWidgets.QVBoxLayout()
        sub_layout.addStretch(1)
        sub_layout.addWidget(progress_bar)
        sub_layout.addWidget(message)
        sub_layout.addStretch(1)
        widget = self.stack.widget(0)
        widget.setLayout(sub_layout)

        self.result = QtWidgets.QLabel("")
        self.result.setWordWrap(True)
        self.result.setOpenExternalLinks(True)
        self.result.setTextFormat(QtCore.Qt.TextFormat.RichText)
        self.result.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)

        checkbox = QtWidgets.QCheckBox("Check for updates on startup")
        checkbox.setChecked(get_check_on_start_setting())
        checkbox.stateChanged.connect(
            lambda state: get_global_settings().setValue(
                "check_update_on_start", state == QtCore.Qt.CheckState.Checked.value
            )
        )

        sub_layout = QtWidgets.QVBoxLayout()
        sub_layout.addStretch(1)
        sub_layout.addWidget(self.result)
        sub_layout.addSpacing(10)
        sub_layout.addWidget(checkbox)
        sub_layout.addStretch(1)
        widget = self.stack.widget(1)
        widget.setLayout(sub_layout)

        button_layout = QtWidgets.QHBoxLayout()
        button_layout.addStretch(1)
        close_button = QtWidgets.QPushButton("Close")
        close_button.clicked.connect(self.close)
        button_layout.addWidget(close_button)
        main_layout.addLayout(button_layout)

        self.worker = Worker(self.check_helper, [])
        self.worker.job_succeeded.connect(self.on_success)
        self.worker.job_failed.connect(self.on_failure)

    def check(self, startup=False):
        """Asynchronous check for new release using the GitHub release API.

        The user is notified when update is found, not found or an error occurred. If startup is true, the user will
        only be notified if update is found.

        Parameters
        ----------
        startup : bool
            indicates the check is happening at startup.
        """
        if startup and not get_check_on_start_setting():
            return

        self.startup = startup
        if not startup:
            self.stack.setCurrentIndex(0)
            self.show()
        self.worker.start()

    def check_helper(self):
        """Check for the latest release version on the GitHub repository.

        Returns
        -------
        startup : str
            The latest version tag.
        """
        with urllib.request.urlopen(UPDATE_URL) as response:
            tag_name = json.loads(response.read()).get("tag_name")

        return tag_name

    def on_success(self, latest_version):
        """Report the version found after successful check.

        Parameters
        ----------
        latest_version : str
            version tag.
        """
        if latest_version and Version(latest_version) > Version(RASCAL2_VERSION):
            self.update_message(
                f"A new version ({latest_version}) of RasCAL-2 is available. Download "
                f'the installer from <a href="{RELEASES_URL}">{RELEASES_URL}</a>.<br/><br/>'
            )
            self.show()  # Always tell user of new version even if startup

        else:
            if not self.startup:
                self.update_message("You are running the latest version of RasCAL-2.\n")

    def on_failure(self, exception):
        """Log and report error after failed check.

        Parameters
        ----------
        exception: : Exception
            An exception which occurred when checking for update.
        """
        logging.error("An error occurred while checking for updates", exc_info=exception)
        if self.startup:
            return

        if isinstance(exception, HTTPError):
            self.update_message("You are running the latest version of RasCAL-2.\n")
        elif isinstance(exception, URLError):
            self.update_message(
                "An error occurred when attempting to connect to the update server. "
                "Check your internet connection and/or firewall and try again.\n"
            )
        else:
            self.update_message(f"An unexpected error occurred when checking for updates: {exception}\n")

    def update_message(self, message):
        """Update UI and show the given message.

        Parameters
        ----------
        message: : str
            A message to display.
        """
        self.stack.setCurrentIndex(1)
        self.result.setText(message)

    def closeEvent(self, event):
        if self.worker.isRunning():
            self.worker.terminate()
        event.accept()
