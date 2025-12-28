import os
from browser.utils.debug import dbg

def apply_chromium_flags():
    dbg("Applying Chromium flags")

    os.environ["QT_QPA_PLATFORM"] = "wayland"
    os.environ["QTWEBENGINE_DISABLE_SANDBOX"] = "1"
    os.environ["QTWEBENGINE_CHROMIUM_FLAGS"] = (
        "--disable-dev-shm-usage "
        "--no-sandbox "
        "--no-zygote "
    )

    dbg(f"QT_QPA_PLATFORM={os.environ.get('QT_QPA_PLATFORM')}")
    dbg(f"QTWEBENGINE_DISABLE_SANDBOX={os.environ.get('QTWEBENGINE_DISABLE_SANDBOX')}")
    dbg(f"QTWEBENGINE_CHROMIUM_FLAGS={os.environ.get('QTWEBENGINE_CHROMIUM_FLAGS')}")

