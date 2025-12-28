from PySide6.QtWebEngineWidgets import QWebEngineView
from PySide6.QtCore import QUrl

OFFLINE_HTML = """
<html>
  <body style="font-family:sans-serif;background:#111;color:#eee;
               display:flex;align-items:center;justify-content:center;height:100vh;">
    <div>
      <h2>Connection lost</h2>
      <p>Please check your internet connection.</p>
    </div>
  </body>
</html>
"""

class BrowserTab(QWebEngineView):
    def __init__(self, url: str | None = None):
        super().__init__()

        self.loadFinished.connect(self._on_load_finished)

        if url:
            self.setUrl(QUrl(url))

    def _on_load_finished(self, ok: bool):
        if not ok:
            self.setHtml(OFFLINE_HTML)

