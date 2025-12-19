import os

os.environ["QTWEBENGINE_CHROMIUM_FLAGS"] = (
    "--disable-features=NetworkServiceSandbox"
)


import sys
from PySide6.QtWidgets import QApplication
from browser.controller.browser_controller import BrowserController
from browser.ui.main_window import MainWindow
from PySide6.QtWebEngineCore import QWebEngineProfile

def main():
    app = QApplication(sys.argv)

    profile = QWebEngineProfile.defaultProfile()
    profile.setHttpCacheType(QWebEngineProfile.HttpCacheType.DiskHttpCache)
    profile.setPersistentCookiesPolicy(
        QWebEngineProfile.PersistentCookiesPolicy.AllowPersistentCookies
    )
    
    font = app.font()
    font.setFamily("Segoe UI")
    font.setPointSize(10)
    app.setFont(font)

    # UPDATED STYLESHEET
    app.setStyleSheet("""
    /* --- MAIN COLORS --- */
    QMainWindow { background-color: #1B1D21; }
    QWidget { color: #E8E8E8; }

    /* --- TABS --- */
    QTabBar {
        background-color: #1B1D21;
        qproperty-drawBase: 0;
    }

    QTabBar::tab {
        background-color: transparent;
        color: #909090;
        padding: 8px 16px;
        margin-top: 4px;
        border-top-left-radius: 12px;
        border-top-right-radius: 12px;
        font-size: 12px;
        min-width: 120px;
        max-width: 240px;
    }

    QTabBar::tab:hover {
        background-color: #26282C;
        color: #F0F0F0;
    }

    QTabBar::tab:selected {
        background-color: #303236; 
        color: #FFFFFF;
        font-weight: bold;
    }

    /* --- MANUAL CLOSE BUTTON (Replacing the CSS SVG) --- */
    #TabCloseButton {
        background-color: transparent;
        color: #AAAAAA;
        border-radius: 10px; /* Round hover effect */
        font-weight: bold;
        font-size: 12px;
        padding: 2px;
        margin-left: 5px;
    }
    
    #TabCloseButton:hover {
        background-color: #FF5F57; /* Red background */
        color: white;
    }

    /* --- NEW TAB BUTTON (+) --- */
    #NewTabButton {
        background-color: transparent;
        border: none;
        border-radius: 14px;
        margin: 4px 0 0 4px; 
        padding: 0px;
        width: 28px; height: 28px;
        font-size: 16px;
        font-weight: bold;
        color: #909090;
    }
    #NewTabButton:hover {
        background-color: #3F4249;
        color: white;
    }

    /* --- TOOLBAR --- */
    QToolBar {
        background-color: #303236; 
        border: none;
        padding: 6px;
        spacing: 8px;
    }

    QToolBar::separator { width: 0px; }
    
    /* Toolbar Buttons */
    QToolButton {
        background: transparent;
        border: none;
        border-radius: 6px;
        padding: 4px;
    }
    QToolButton:hover { background-color: #3A3D43; }

    /* --- ROUNDED ADDRESS BAR (Pill) --- */
    QLineEdit {
        background-color: #1F2124;
        color: #FFFFFF;
        border: 1px solid #3F4249;
        border-radius: 17px; 
        padding: 6px 16px;
        font-size: 14px;
        selection-background-color: #FB542B;
    }
    QLineEdit:hover {
        border: 1px solid #666;
        background-color: #242629;
    }
    QLineEdit:focus {
        border: 2px solid #FB542B; 
        background-color: #1F2124;
    }

    /* --- SCROLLBARS --- */
    QScrollBar:vertical {
        background: #1B1D21;
        width: 12px;
        margin: 0px;
    }
    QScrollBar::handle:vertical {
        background: #4B4E55;
        min-height: 20px;
        border-radius: 6px;
        margin: 2px;
    }
    """)

    controller = BrowserController()
    window = MainWindow(controller)
    window.show()

    sys.exit(app.exec())

if __name__ == "__main__":
    main()
