from PySide6.QtCore import QUrl, Qt
from PySide6.QtWebEngineWidgets import QWebEngineView
from PySide6.QtWebEngineCore import QWebEnginePage
from browser.utils.debug import dbg

OFFLINE_HTML = "<h1>Offline</h1>"


class BrowserTab(QWebEngineView):
    def __init__(self, profile, url: str | None = None, parent=None):
        dbg("BrowserTab.__init__ start")

        # IMPORTANT: create without parent first
        super().__init__(None)

        # ✅ Qt6-correct widget attributes
        # self.setAttribute(Qt.WidgetAttribute.WA_NativeWindow, True)
        # self.setAttribute(Qt.WidgetAttribute.WA_DontCreateNativeAncestors, True)

        # ✅ Qt6-correct page creation
        page = QWebEnginePage(profile, self)
        self.setPage(page)

        if parent is not None:
            self.setParent(parent)

        self.loadFinished.connect(self._on_load_finished)

        if url:
            dbg(f"Setting initial URL: {url}")
            self.setUrl(QUrl(url))

        dbg("BrowserTab.__init__ end")

    def _on_load_finished(self, ok: bool):
        dbg(f"Load finished: ok={ok}")
        if not ok:
            self.setHtml(OFFLINE_HTML)

