from PySide6.QtWidgets import QLineEdit

class AddressBar(QLineEdit):
    def __init__(self):
        super().__init__()
        self.setFixedHeight(34)
        self.setPlaceholderText("Search or enter address")
        self.setTextMargins(16, 0, 16, 0)
