from typing import cast, Optional, Union
from PySide6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QToolBar, QLineEdit, QTabBar, QStackedWidget,
    QToolButton, QStyle
)
from PySide6.QtGui import QAction, QIcon
from PySide6.QtCore import QUrl, QSize, Qt
from PySide6.QtWebEngineWidgets import QWebEngineView

# Optional icons
try:
    import qtawesome as qta
except ImportError:
    qta = None

class AddressBar(QLineEdit):
    def __init__(self):
        super().__init__()
        self.setFixedHeight(34)
        self.setPlaceholderText("Search or enter address")
        self.setTextMargins(16, 0, 16, 0)

class MainWindow(QMainWindow):
    def __init__(self, controller):
        super().__init__()
        self.controller = controller
        self.setWindowTitle("Sagittarius Browser")
        self.resize(1200, 800)

        # -------- Central widget --------
        central = QWidget(self)
        self.setCentralWidget(central)

        self.main_layout = QVBoxLayout(central)
        self.main_layout.setContentsMargins(0, 0, 0, 0)
        self.main_layout.setSpacing(0)

        # -------- Tab bar row --------
        tab_row = QWidget()
        tab_layout = QHBoxLayout(tab_row)
        tab_layout.setContentsMargins(0, 0, 0, 0)
        tab_layout.setSpacing(0)

        self.tab_bar = QTabBar()
        self.tab_bar.setDocumentMode(True)
        self.tab_bar.setMovable(True)
        self.tab_bar.setTabsClosable(False)
        self.tab_bar.setExpanding(False)
        self.tab_bar.currentChanged.connect(self._on_tab_changed)
        
        tab_layout.addWidget(self.tab_bar)

        # Add Tab Button
        self.add_tab_btn = QToolButton()
        self.add_tab_btn.setText("+")
        self.add_tab_btn.setToolTip("New Tab")
        self.add_tab_btn.setObjectName("NewTabButton")
        self.add_tab_btn.clicked.connect(self.add_tab)
        tab_layout.addWidget(self.add_tab_btn)

        tab_layout.addStretch()
        self.main_layout.addWidget(tab_row)

        # -------- Toolbar --------
        toolbar = QToolBar()
        toolbar.setMovable(False)
        toolbar.setFixedHeight(46)
        toolbar.setIconSize(QSize(18, 18))
        self.main_layout.addWidget(toolbar)

        # Icon Helper
        def icon(name: str, fallback: QStyle.StandardPixmap) -> QIcon:
            if qta:
                return qta.icon(name, color="#EAEAEA", color_active="#FB542B")
            return self.style().standardIcon(fallback)

        back_act = QAction(icon("fa5s.arrow-left", QStyle.StandardPixmap.SP_ArrowBack), "Back", self)
        back_act.triggered.connect(self.go_back)
        toolbar.addAction(back_act)

        fwd_act = QAction(icon("fa5s.arrow-right", QStyle.StandardPixmap.SP_ArrowForward), "Forward", self)
        fwd_act.triggered.connect(self.go_forward)
        toolbar.addAction(fwd_act)

        reload_act = QAction(icon("fa5s.redo", QStyle.StandardPixmap.SP_BrowserReload), "Reload", self)
        reload_act.triggered.connect(self.reload_page)
        toolbar.addAction(reload_act)

        self.url_bar = AddressBar()
        self.url_bar.returnPressed.connect(self.load_url)
        toolbar.addWidget(self.url_bar)

        # -------- Web views --------
        self.pages = QStackedWidget()
        self.main_layout.addWidget(self.pages)

        # Initial tab
        self.add_tab()

    # ==================================================
    # Tabs
    # ==================================================
    def add_tab(self, url: Union[str, bool, None] = None):
        if not isinstance(url, str):
            url = "https://search.brave.com"

        view = self.controller.create_view()
        view.setUrl(QUrl(url))

        index = self.pages.addWidget(view)
        self.tab_bar.addTab("New Tab")
        
        # --- MANUAL CLOSE BUTTON ---
        close_btn = QToolButton()
        close_btn.setText("✕") 
        close_btn.setObjectName("TabCloseButton")
        close_btn.setToolTip("Close Tab")
        close_btn.clicked.connect(self.close_tab_from_button)

        self.tab_bar.setTabButton(index, QTabBar.ButtonPosition.RightSide, close_btn)
        
        self.tab_bar.setCurrentIndex(index)
        self.pages.setCurrentIndex(index)

        # --- SIGNALS ---
        view.titleChanged.connect(lambda t, v=view: self._update_title(v, t))
        view.urlChanged.connect(self.update_url_bar)
        
        # THIS WAS MISSING: Connect the icon signal
        view.iconChanged.connect(lambda i, v=view: self._update_icon(v, i))

    def _update_icon(self, view: QWebEngineView, icon: QIcon):
        """Updates the tab icon when the website favicon loads."""
        index = self.pages.indexOf(view)
        if index != -1 and not icon.isNull():
            self.tab_bar.setTabIcon(index, icon)

    def close_tab_from_button(self):
        btn = self.sender()
        for i in range(self.tab_bar.count()):
            if self.tab_bar.tabButton(i, QTabBar.ButtonPosition.RightSide) == btn:
                self.close_tab(i)
                break

    def close_tab(self, index: int):
        if self.tab_bar.count() > 1:
            widget = self.pages.widget(index)
            self.pages.removeWidget(widget)
            widget.deleteLater()
            self.tab_bar.removeTab(index)

    def _on_tab_changed(self, index: int):
        if index >= 0:
            self.pages.setCurrentIndex(index)
            self.update_url_bar()

    def _update_title(self, view: QWebEngineView, title: str):
        index = self.pages.indexOf(view)
        if index != -1:
            self.tab_bar.setTabText(index, title[:20])

    # ==================================================
    # Navigation
    # ==================================================
    def load_url(self):
        text = self.url_bar.text().strip()
        if not text: return
        if " " in text and "." not in text:
            text = f"https://search.brave.com/search?q={text}"
        elif not text.startswith("http"):
            text = "https://" + text
        
        view = cast(QWebEngineView, self.pages.currentWidget())
        if view: view.setUrl(QUrl(text))

    def update_url_bar(self):
        view = self.pages.currentWidget()
        if isinstance(view, QWebEngineView):
            self.url_bar.setText(view.url().toString())

    def go_back(self):
        view = cast(QWebEngineView, self.pages.currentWidget())
        if view: view.back()

    def go_forward(self):
        view = cast(QWebEngineView, self.pages.currentWidget())
        if view: view.forward()

    def reload_page(self):
        view = cast(QWebEngineView, self.pages.currentWidget())
        if view: view.reload()