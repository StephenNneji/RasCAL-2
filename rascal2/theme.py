import re
from contextlib import suppress

from PyQt6 import QtCore, QtGui, QtWidgets

from rascal2.paths import IMAGES_PATH, STATIC_PATH, path_for


def get_correct_qt_color_scheme():
    """Get the correct colour scheme."""
    # On linux PyQt 6.9.1 sometimes returns incorrect scheme.
    # A workaround is to store the scheme to ensure it is correct.
    # This issue is fixed in PyQt 6.10 but 6.10 is not available on IDAaas
    # due to older GLIBC, so we are stuck on 6.9.1 for now.
    app = QtWidgets.QApplication.instance()
    scheme = app.styleHints().property("colour_scheme")
    if scheme is None:
        return QtCore.Qt.ColorScheme.Light
    elif scheme == QtCore.Qt.ColorScheme.Unknown:
        return app.styleHints().colorScheme()
    return scheme


def colorize_icon(icon, colour):
    """Change icon colour to given colour.

    Parameters
    ----------
    icon : QtGui.QIcon
        The icon to colourize
    colour : QtGui.QColor
        The new colour of the icon
    """
    pixmap = icon.pixmap(200, 200)
    mask = pixmap.createMaskFromColor(QtGui.QColor(QtCore.Qt.GlobalColor.transparent), QtCore.Qt.MaskMode.MaskInColor)
    pixmap.fill(colour)
    pixmap.setMask(mask)

    return QtGui.QIcon(pixmap)


def set_stylesheet(app):
    """Set the stylesheet of the app according to the given style.css file if available."""
    with suppress(FileNotFoundError), open(STATIC_PATH / "style.css") as stylesheet:
        app.setStyleSheet("* {}")  # This is a hack to force PyQt 6.9.1 to update the palette on Linux
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


class ThemeManager(QtCore.QObject):
    """Class to manage the Theme of the UI."""

    def __init__(self):
        super().__init__()
        scheme = get_correct_qt_color_scheme()
        self.cur_style = "light" if scheme == QtCore.Qt.ColorScheme.Light else "dark"

    def eventFilter(self, obj, event):
        """Catch close event for overlay widget."""
        if isinstance(obj, QtWidgets.QApplication) and event.type() == QtCore.QEvent.Type.ApplicationPaletteChange:
            scheme = get_correct_qt_color_scheme()
            style = "light" if scheme == QtCore.Qt.ColorScheme.Light else "dark"
            if style != self.cur_style:
                set_stylesheet(obj)
                self.cur_style = style
                return True
        return False


THEMES = ThemeManager()


class IconEngine(QtGui.QIconEngine):
    """Load the appropriate icon for the application theme.

    Parameters
    ----------
    filename : str
        The path of the icon
    """

    def __init__(self, filename):
        super().__init__()
        self.name = re.split(r"-dark.png|-light.png", filename)[0]
        self.update_icon()

    def update_icon(self):
        """Update the icon to match the current theme."""
        scheme = get_correct_qt_color_scheme()
        style = "light" if scheme == QtCore.Qt.ColorScheme.Light else "dark"

        filename = f"{self.name}-light.png" if style == "light" else f"{self.name}-dark.png"
        path = path_for(filename)
        self.icon = QtGui.QIcon(path)

    def pixmap(self, size, mode, state):
        """Create the pixmap."""
        self.update_icon()
        return self.icon.pixmap(size, mode, state)

    def paint(self, painter, rect, mode, state):
        """Paint the icon."""
        self.update_icon()
        return self.icon.pixmap.paint(painter, rect, mode, state)
