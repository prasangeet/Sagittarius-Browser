from PySide6.QtWebEngineWidgets import QWebEngineView
from PySide6.QtWebEngineCore import QWebEngineProfile
from browser.privacy.request_interceptor import RequestInterceptor

class BrowserController:
    def __init__(self) -> None:
        self.profile = QWebEngineProfile.defaultProfile()
        self.interceptor = RequestInterceptor()
        self.profile.setUrlRequestInterceptor(self.interceptor)

    def create_view(self):
        view = QWebEngineView()
        view.setUrl("https://www.google.com")
        return view
