# test_qtwebengine_url.py
import sys
from PySide6.QtWidgets import QApplication
from PySide6.QtWebEngineWidgets import QWebEngineView
from PySide6.QtCore import QUrl

app = QApplication(sys.argv)

view = QWebEngineView()
view.setUrl(QUrl("https://example.com"))  # NOT Google yet
view.resize(1200, 800)
view.show()

sys.exit(app.exec())

