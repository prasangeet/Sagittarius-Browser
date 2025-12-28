from PySide6.QtWebEngineWidgets import QWebEngineView
from PySide6.QtWebEngineCore import QWebEnginePage
from PySide6.QtCore import QUrl
from browser.utils.debug import dbg

OFFLINE_HTML = """<h1>Offline</h1>"""

class BrowserTab(QWebEngineView):
    def __init__(self, page: QWebEnginePage, url: str | None = None):
        dbg("BrowserTab.__init__ start")

        super().__init__()
        dbg("QWebEngineView constructed")

        self.setPage(page)
        dbg("Page attached to view")

        self.loadFinished.connect(self._on_load_finished)

        if url:
            dbg(f"Setting initial URL: {url}")
            self.setUrl(QUrl(url))

        dbg("BrowserTab.__init__ end")

    def _on_load_finished(self, ok: bool):
        dbg(f"Load finished: ok={ok}")
        if not ok:
            self.setHtml(OFFLINE_HTML)

