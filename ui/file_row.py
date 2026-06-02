# ── ui: file-row (label + readonly line + browse button) ────────────

import os

from PyQt6.QtCore import pyqtSignal
from PyQt6.QtWidgets import QFileDialog, QHBoxLayout, QLabel, QLineEdit, QPushButton, QWidget


class FileRow(QWidget):
    file_changed = pyqtSignal(str)

    def __init__(self, label: str, mode: str, filter_str: str, parent=None):
        """
        mode: "open" 选择已有文件, "save" 选择保存路径
        """
        super().__init__(parent)
        self._mode = mode
        self._filter = filter_str

        layout = QHBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(8)

        lbl = QLabel(label)
        lbl.setFixedWidth(56)
        layout.addWidget(lbl)

        self.edit = QLineEdit()
        self.edit.setReadOnly(True)
        self.edit.setPlaceholderText("点击右侧浏览按钮选择文件…")
        layout.addWidget(self.edit, 1)

        btn = QPushButton("浏览…")
        btn.setObjectName("browseBtn")
        btn.clicked.connect(self._browse)
        layout.addWidget(btn)

    def _browse(self):
        if self._mode == "open":
            path, _ = QFileDialog.getOpenFileName(self, "选择文件", "", self._filter)
        else:
            path, _ = QFileDialog.getSaveFileName(self, "保存到", "", self._filter)
        if path:
            self.edit.setText(path)
            self.file_changed.emit(path)

    def text(self) -> str:
        return self.edit.text().strip()

    def set_text(self, value: str):
        self.edit.setText(value)

    def set_enabled(self, enabled: bool):
        self.edit.setEnabled(enabled)
