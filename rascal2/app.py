import logging
import multiprocessing

from PyQt6 import QtWidgets, QtCore

from rascal2.config import MatlabHelper, handle_scaling, setup_logging
from rascal2.theme import THEMES, set_stylesheet
from rascal2.ui.view import MainWindowView


def ui_execute(splash):
    """Create main window and executes GUI event loop.

    Returns
    -------
    exit code : int
        QApplication exit code
    """
    handle_scaling()
    app = QtWidgets.QApplication.instance()
    app.setStyle("Fusion")
    app.installEventFilter(THEMES)
    app.styleHints().setColorScheme(QtCore.Qt.ColorScheme.Unknown)
    set_stylesheet(app)

    window = MainWindowView()
    window.show()
    splash.finish(window)

    return app.exec()


def start_app(splash):
    """Start RasCAL app."""
    multiprocessing.set_start_method("spawn", force=True)
    setup_logging()
    matlab_helper = MatlabHelper()
    exit_code = ui_execute(splash)
    matlab_helper.close_event.set()
    logging.shutdown()
    return exit_code
