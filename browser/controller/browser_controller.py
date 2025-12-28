from PySide6.QtWebEngineWidgets import QWebEngineView
from PySide6.QtWebEngineCore import QWebEngineProfile, QWebEnginePage
from PySide6.QtCore import QUrl
from browser.utils.debug import dbg

class BrowserController:
    def __init__(self, app):
        dbg("BrowserController.__init__ start")

        self.profile = QWebEngineProfile("SagittariusProfile", app)
        self.profile.setHttpCacheType(QWebEngineProfile.HttpCacheType.MemoryHttpCache)
        self.profile.setPersistentCookiesPolicy(
            QWebEngineProfile.PersistentCookiesPolicy.NoPersistentCookies
        )

        dbg("QWebEngineProfile created")
        dbg("BrowserController.__init__ end")

    def create_view(self) -> QWebEngineView:
        dbg("Creating QWebEngineView + QWebEnginePage")

        page = QWebEnginePage(self.profile)
        view = QWebEngineView()
        view.setPage(page)

        return view

