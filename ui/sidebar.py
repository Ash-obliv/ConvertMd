# ── ui: sidebar navigation ──────────────────────────────────────────

from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QFrame, QLabel, QPushButton, QStackedWidget, QVBoxLayout


class Sidebar(QFrame):
    def __init__(self, stack: QStackedWidget, parent=None):
        super().__init__(parent)
        self.setObjectName("sidebar")
        self.setFixedWidth(168)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(10, 18, 10, 18)
        layout.setSpacing(2)

        # logo
        logo = QLabel("ConvertMD")
        logo.setAlignment(Qt.AlignmentFlag.AlignCenter)
        logo.setStyleSheet(
            "font-size: 17px; font-weight: bold; padding: 10px 0 2px 0;"
            "color: #4f46e5;"
        )
        layout.addWidget(logo)

        sub = QLabel("Markdown  Word")
        sub.setAlignment(Qt.AlignmentFlag.AlignCenter)
        sub.setStyleSheet("font-size: 11px; color: #94a3b8; padding: 0 0 6px 0;")
        layout.addWidget(sub)

        sep = QFrame()
        sep.setFrameShape(QFrame.Shape.HLine)
        layout.addWidget(sep)
        layout.addSpacing(6)

        self.btn_md2word = QPushButton("  MD  →  Word")
        self.btn_word2md = QPushButton("  Word  →  MD")
        self.btn_pdf2md = QPushButton("  PDF  →  MD")
        self.btn_settings = QPushButton("  设置")

        for btn in (self.btn_md2word, self.btn_word2md, self.btn_pdf2md, self.btn_settings):
            btn.setObjectName("navBtn")
            btn.setCheckable(True)
            btn.setFixedHeight(40)
            btn.setCursor(Qt.CursorShape.PointingHandCursor)
            layout.addWidget(btn)

        layout.addSpacing(6)

        self.btn_md2word.clicked.connect(lambda: self._switch(0, self.btn_md2word))
        self.btn_word2md.clicked.connect(lambda: self._switch(1, self.btn_word2md))
        self.btn_pdf2md.clicked.connect(lambda: self._switch(2, self.btn_pdf2md))
        self.btn_settings.clicked.connect(lambda: self._switch(3, self.btn_settings))

        self._buttons = [self.btn_md2word, self.btn_word2md, self.btn_pdf2md, self.btn_settings]
        self._stack = stack
        self._switch(0, self.btn_md2word)

        layout.addStretch()

    def _switch(self, index: int, active_btn: QPushButton):
        for btn in self._buttons:
            btn.setChecked(btn is active_btn)
        self._stack.setCurrentIndex(index)
