from PySide6.QtWebEngineCore import QWebEngineUrlRequestInterceptor


class RequestInterceptor(QWebEngineUrlRequestInterceptor):
    def interceptRequest(self, info) -> None:
        url = info.requestUrl().toString()
        resource_type = info.resourceType()
        print(f"[REQUEST] {resource_type} -> {url}")

