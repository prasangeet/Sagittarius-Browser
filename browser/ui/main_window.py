from typing import cast
from PySide6.QtWidgets import (
    QMainWindow, QStyle, QWidget, QVBoxLayout, QHBoxLayout,
    QToolBar, QTabBar, QStackedWidget, QToolButton
)
from PySide6.QtGui import QAction
from PySide6.QtCore import QUrl, QTimer
from PySide6.QtWebEngineWidgets import QWebEngineView
from browser.ui.address_bar import AddressBar
from browser.utils.debug import dbg

class MainWindow(QMainWindow):
    def __init__(self, controller):
        super().__init__()
        dbg("MainWindow.__init__ start")

        self.controller = controller
        self.setWindowTitle("Sagittarius Browser")
        self.resize(1200, 800)

        central = QWidget(self)
        self.setCentralWidget(central)

        layout = QVBoxLayout(central)
        layout.setContentsMargins(0, 0, 0, 0)

        # Tabs
        tab_row = QWidget()
        tab_layout = QHBoxLayout(tab_row)
        tab_layout.setContentsMargins(0, 0, 0, 0)

        self.tab_bar = QTabBar()
        self.tab_bar.currentChanged.connect(self._on_tab_changed)
        tab_layout.addWidget(self.tab_bar)

        add_btn = QToolButton()
        add_btn.setText("+")
        add_btn.clicked.connect(self.add_tab)
        tab_layout.addWidget(add_btn)

        layout.addWidget(tab_row)

        # Toolbar
        toolbar = QToolBar()
        layout.addWidget(toolbar)

        style = self.style()

        back = QAction(style.standardIcon(QStyle.StandardPixmap.SP_ArrowBack), "", self)
        back.setToolTip("Back")
        back.triggered.connect(self.go_back)
        toolbar.addAction(back)

        fwd = QAction(style.standardIcon(QStyle.StandardPixmap.SP_ArrowForward), "", self)
        fwd.setToolTip("Forward")
        fwd.triggered.connect(self.go_forward)
        toolbar.addAction(fwd)

        reload_ = QAction(style.standardIcon(QStyle.StandardPixmap.SP_BrowserReload), "", self)
        reload_.setToolTip("Reload")
        reload_.triggered.connect(self.reload_page)
        toolbar.addAction(reload_)

        self.address_bar = AddressBar()
        self.address_bar.returnPressed.connect(self.load_url)
        toolbar.addWidget(self.address_bar)

        # Pages
        self.pages = QStackedWidget()
        layout.addWidget(self.pages)

        self.add_tab()

        # 🚨 THIS IS THE IMPORTANT PART 🚨
        # Defer navigation until event loop is alive
        QTimer.singleShot(0, self._load_initial_url)

        dbg("MainWindow.__init__ end")

        self.setStyleSheet("""
        /* =========================
           GLOBAL
           ========================= */
        QMainWindow {
            background-color: #0f1115;
        }

        QWidget {
            color: #e5e7eb;
            font-family: Inter, Segoe UI, sans-serif;
        }

        /* =========================
           TAB BAR
           ========================= */
        QTabBar {
            background: #0f1115;
            padding-left: 8px;
        }

        QTabBar::tab {
            background: #16181d;
            color: #9ca3af;
            padding: 8px 16px;
            margin-right: 6px;
            border-top-left-radius: 10px;
            border-top-right-radius: 10px;
            min-width: 120px;
        }

        QTabBar::tab:selected {
            background: #1f2937;
            color: #ffffff;
        }

        QTabBar::tab:hover {
            background: #23262d;
            color: #ffffff;
        }

        /* =========================
           TOOLBAR
           ========================= */
        QToolBar {
            background: #16181d;
            border: none;
            padding: 6px;
        }

        QToolButton {
            background: transparent;
            border-radius: 6px;
            padding: 6px;
        }

        QToolButton:hover {
            background: #23262d;
        }

        /* =========================
           ADD TAB BUTTON
           ========================= */
        QToolButton[text="+"] {
            font-size: 18px;
            padding: 0 10px;
        }

        /* =========================
           STACKED PAGES
           ========================= */
        QStackedWidget {
            background: #0f1115;
        }
        """)
    def add_tab(self):
        dbg("Adding new tab")
        view = self.controller.create_view()

        idx = self.pages.addWidget(view)
        self.tab_bar.addTab("New Tab")

        self.pages.setCurrentIndex(idx)
        self.tab_bar.setCurrentIndex(idx)

    def _load_initial_url(self):
        dbg("Deferred URL load")
        view = cast(QWebEngineView, self.pages.currentWidget())
        view.setUrl(QUrl("https://www.google.com"))

    def _on_tab_changed(self, index: int):
        self.pages.setCurrentIndex(index)

    def go_back(self):
        view = cast(QWebEngineView, self.pages.currentWidget())
        view.back()

    def go_forward(self):
        view = cast(QWebEngineView, self.pages.currentWidget())
        view.forward()

    def reload_page(self):
        view = cast(QWebEngineView, self.pages.currentWidget())
        view.reload()

