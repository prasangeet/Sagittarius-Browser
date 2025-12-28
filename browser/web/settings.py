import os

def apply_chromium_flags():
    os.environ["QTWEBENGINE_CHROMIUM_FLAGS"] = (
        "--disable-quic "
        "--disable-http2 "
        "--disable-background-networking "
        "--disable-sync"
    )

