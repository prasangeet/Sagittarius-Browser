from sys import setswitchinterval
from PySide6.QtWebEngineCore import QWebEngineProfile


class EngineProfile:

    def __init__(self, app) -> None:
        self.profile = QWebEngineProfile("SagittariusProfile", app)
        
        self.profile.setHttpCacheType(
            QWebEngineProfile.HttpCacheType.MemoryHttpCache
        )

        self.profile.setPersistentCookiesPolicy(
            QWebEngineProfile.PersistentCookiesPolicy.NoPersistentCookies
        )

    def get(self) -> QWebEngineProfile:
        return self.profile
