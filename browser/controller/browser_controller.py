from PySide6.QtCore import QUrl
from PySide6.QtWebEngineWidgets import QWebEngineView
from PySide6.QtWebEngineCore import QWebEnginePage, QWebEngineProfile
from browser.privacy.request_interceptor import RequestInterceptor

class BrowserController:
    def __init__(self) -> None:
        self.profile = QWebEngineProfile.defaultProfile()

        self.profile.setHttpCacheType(
            QWebEngineProfile.HttpCacheType.DiskHttpCache
        )
        self.profile.setPersistentCookiesPolicy(
            QWebEngineProfile.PersistentCookiesPolicy.AllowPersistentCookies
        )

        self.interceptor = RequestInterceptor()
        self.profile.setUrlRequestInterceptor(self.interceptor)

    def create_view(self, url: str | None = None) -> QWebEngineView:
        page = QWebEnginePage(self.profile)
        view = QWebEngineView()
        view.setPage(page)

        if url:
            view.setUrl(QUrl(url))
        return view
