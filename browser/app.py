import sys
from browser.utils.debug import dbg

dbg(">>> app.py import start")

# 🔴 REQUIRED
# from PySide6.QtWebEngineCore import QtWebEngine
# QtWebEngine.initialize()
#
import browser.resources.icons_rc

from browser.web.settings import apply_chromium_flags
apply_chromium_flags()

from PySide6.QtWidgets import QApplication
from browser.controller.browser_controller import BrowserController
from browser.ui.main_window import MainWindow


def main():
    dbg("Entering main()")

    app = QApplication(sys.argv)
    dbg("QApplication created")

    controller = BrowserController(app)
    dbg("BrowserController created")

    window = MainWindow(controller)
    dbg("MainWindow created")

    window.show()
    dbg("MainWindow shown")

    dbg("Starting Qt event loop")
    sys.exit(app.exec())


if __name__ == "__main__":
    main()

