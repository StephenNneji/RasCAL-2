import os
import sys
from pathlib import Path

from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPixmap
from PyQt6.QtWidgets import QApplication, QSplashScreen

if os.environ.get("RASCAL_SPLASH") is None:
    app = QApplication([])
    SOURCE_PATH = Path(sys.executable).parent.parent
    if Path(SOURCE_PATH / "MacOS").is_dir():
        SOURCE_PATH = SOURCE_PATH / "Resources"

    splash = QSplashScreen()
    splash.setAttribute(Qt.WidgetAttribute.WA_DeleteOnClose)
    splash.setPixmap(QPixmap(str(SOURCE_PATH / "static" / "images" / "splash.png")))
    splash.show()
    app.processEvents()
    os.environ["RASCAL_SPLASH"] = "1"
