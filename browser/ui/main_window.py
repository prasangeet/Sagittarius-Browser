import re
from types import NoneType
from typing import Optional, cast
from PySide6.QtCore import QFile, QIODevice, QIODeviceBase, QPluginLoader, QUrl
from PySide6.QtUiTools import QUiLoader
from PySide6.QtWebEngineWidgets import QWebEngineView
from PySide6.QtWidgets import QLineEdit, QTabBar, QToolButton, QVBoxLayout, QWidget

from browser.ui.browser_tab import BrowserTab
from browser.utils.debug import dbg

class MainWindow:
    def __init__(self, controller) -> None:
        self.controller = controller

        ui_file = QFile("browser/ui/main_window.ui")
        ui_file.open(QIODeviceBase.OpenModeFlag.ReadOnly)
        self.window = QUiLoader().load(ui_file)
        ui_file.close()

        #Bind Widgets
        self.back_button = cast(QToolButton, self.window.findChild(QToolButton, "backButton"))
        self.forward_button = cast(QToolButton, self.window.findChild(QToolButton, "forwardButton"))
        self.reload_button = cast(QToolButton, self.window.findChild(QToolButton, "reloadButton"))
        self.new_tab_button = cast(QToolButton, self.window.findChild(QToolButton, "newTabButton"))
        self.address_bar = cast(QLineEdit, self.window.findChild(QLineEdit, "addressBar"))

        self.tab_container = cast(QWidget, self.window.findChild(QWidget, "tabBar"))
        self.view_container = cast(QWidget, self.window.findChild(QWidget, "viewContainer"))

        # Layout for views
        self.view_layout = self.view_container.layout()
        if self.view_layout is None:
            self.view_layout = QVBoxLayout(self.view_container)
            self.view_layout.setContentsMargins(0,0,0,0)

        # Tab bar
        tab_layout = self.tab_container.layout()
        if tab_layout is None:
            tab_layout = QVBoxLayout(self.tab_container)
            tab_layout.setContentsMargins(0,0,0,0)

        self.tab_bar = QTabBar()
        self.tab_bar.setMovable(True)
        self.tab_bar.setExpanding(False)
        tab_layout.addWidget(self.tab_bar)

        ## Internal States
        self.tabs: list[BrowserTab] = []
        self.current_tab: Optional[BrowserTab] = None

        ## Signals
        self.tab_bar.currentChanged.connect(self._on_tab_changed)
        self.new_tab_button.clicked.connect(
            lambda: self._new_tab(url="https://www.google.com")
        )


        self.back_button.clicked.connect(self._go_back)
        self.forward_button.clicked.connect(self._go_forward)
        self.reload_button.clicked.connect(self._reload)
        self.address_bar.returnPressed.connect(self._load_from_address_bar)

        self._new_tab(url="https://www.google.com")

        dbg("MainWindow.__init__ end")

    def show(self):
        self.window.show()

    def _new_tab(self, url: str | None):
        dbg("Creating new Tab")

        tab = BrowserTab(self.controller.profile, url = url, parent=self.view_container)

        tab.hide()
        self.view_layout.addWidget(tab)
        self.tabs.append(tab)

        index = self.tab_bar.addTab("New Tab")
        
        tab.titleChanged.connect(
            lambda title, i = index: self.tab_bar.setTabText(i, title)
        )

        tab.urlChanged.connect(
            lambda qurl, t = tab: self._sync_address_bar(t, qurl)
        )

        self.tab_bar.setCurrentIndex(index)

    def _on_tab_changed(self, index: int):
        if self.current_tab:
            self.current_tab.hide()

        self.current_tab = self.tabs[index]
        self.current_tab.show()

        self.address_bar.setText(self.current_tab.url().toString())

    def _go_back(self):
        if self.current_tab:
            self.current_tab.back()

    def _go_forward(self):
        if self.current_tab:
            self.current_tab.forward()

    def _reload(self):
        if self.current_tab:
            self.current_tab.reload()

    def _load_from_address_bar(self):
        if not self.current_tab:
            return

        text = self.address_bar.text().strip()
        if not text:
            return
        
        if ".//" not in text:
            if "." in text:
                text = "https://" + text;
            else:
                text = f"https://www.google.com/search?q={text}"

        self.current_tab.setUrl(QUrl(text))

    def _sync_address_bar(self, tab: BrowserTab, qurl: QUrl):
        if tab is self.current_tab:
            self.address_bar.setText(qurl.toString())
