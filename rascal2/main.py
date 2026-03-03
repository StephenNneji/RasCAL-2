import logging
import multiprocessing
import re
import sys
from contextlib import suppress

from PyQt6 import QtCore, QtGui, QtWidgets

from rascal2.config import IMAGES_PATH, STATIC_PATH, MatlabHelper, handle_scaling, path_for, setup_logging
from rascal2.ui.view import MainWindowView


def close_splash(window):
    """Close the splash screen.

    Parameters
    ----------
    window: MainWindowView
        The rascal main window.
    """
    app = QtWidgets.QApplication.instance()
    for widget in app.topLevelWidgets():
        if isinstance(widget, QtWidgets.QSplashScreen):
            widget.finish(window)
            window.showMinimized()
            window.showNormal()
            break


def ui_execute():
    """Create main window and executes GUI event loop.

    Returns
    -------
    exit code : int
        QApplication exit code
    """
    handle_scaling()
    QtWidgets.QApplication.setStyle("Fusion")
    app = QtWidgets.QApplication.instance()
    if app is None:
        app = QtWidgets.QApplication([])

    app.setWindowIcon(QtGui.QIcon(path_for("logo.png")))
    with suppress(FileNotFoundError), open(STATIC_PATH / "style.css") as stylesheet:
        palette = app.palette()
        replacements = {
            "@Path": IMAGES_PATH.as_posix(),
            "@Window": palette.window().color().name(),
            "@Highlight": palette.highlight().color().name(),
            "@Midlight": palette.midlight().color().name(),
            "@Text": palette.text().color().name(),
        }
        style = re.sub("|".join(replacements), lambda x: replacements[x.group(0)], stylesheet.read())
        app.setStyleSheet(style)

    window = MainWindowView()
    QtCore.QTimer.singleShot(100, lambda: close_splash(window))
    window.show()
    return app.exec()


def main():
    """Entry point function for starting RasCAL."""
    multiprocessing.freeze_support()
    multiprocessing.set_start_method("spawn", force=True)
    setup_logging()
    matlab_helper = MatlabHelper()
    exit_code = ui_execute()
    matlab_helper.close_event.set()
    logging.shutdown()
    sys.exit(exit_code)


if __name__ == "__main__":
    main()
