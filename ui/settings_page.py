# ── ui: settings page ────────────────────────────────────────────────

from PyQt6.QtCore import QSettings
from PyQt6.QtWidgets import (
    QFileDialog,
    QFrame,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QMessageBox,
    QPushButton,
    QVBoxLayout,
    QWidget,
)

from core import find_pandoc, SETTINGS_KEY_PANDOC, SETTINGS_KEY_THEME
from ui.theme import apply_theme


class SettingsPage(QWidget):
    def __init__(self, app, settings: QSettings, parent=None):
        super().__init__(parent)
        self._app = app
        self._settings = settings

        layout = QVBoxLayout(self)
        layout.setContentsMargins(32, 28, 32, 24)
        layout.setSpacing(14)

        page_title = QLabel("设置")
        page_title.setObjectName("pageTitle")
        layout.addWidget(page_title)

        # ── pandoc ──────────────────────────────────────────────────
        sec1 = QLabel("Pandoc 路径")
        sec1.setObjectName("sectionLabel")
        layout.addWidget(sec1)

        row = QHBoxLayout()
        row.setSpacing(8)
        self.pandoc_edit = QLineEdit()
        self.pandoc_edit.setText(find_pandoc(settings))
        row.addWidget(self.pandoc_edit, 1)

        browse_btn = QPushButton("浏览…")
        browse_btn.setObjectName("browseBtn")
        browse_btn.clicked.connect(self._browse_pandoc)
        row.addWidget(browse_btn)
        layout.addLayout(row)

        save_btn = QPushButton("保存路径")
        save_btn.clicked.connect(self._save_pandoc)
        layout.addWidget(save_btn)

        # ── separator ──
        line = QFrame()
        line.setFrameShape(QFrame.Shape.HLine)
        layout.addWidget(line)

        # ── theme ──
        sec2 = QLabel("外观主题")
        sec2.setObjectName("sectionLabel")
        layout.addWidget(sec2)

        self.theme_status = QLabel()
        layout.addWidget(self.theme_status)

        theme_row = QHBoxLayout()
        theme_row.setSpacing(10)

        self.btn_light = QPushButton("☀  浅色模式")
        self.btn_light.clicked.connect(lambda: self._set_theme("light"))

        self.btn_dark = QPushButton("🌙  深色模式")
        self.btn_dark.clicked.connect(lambda: self._set_theme("dark"))

        theme_row.addWidget(self.btn_light)
        theme_row.addWidget(self.btn_dark)
        layout.addLayout(theme_row)

        self._refresh_theme_label()

        layout.addStretch()

    def _refresh_theme_label(self):
        current = self._settings.value(SETTINGS_KEY_THEME, "light")
        self.theme_status.setText(f"当前：{'深色模式' if current == 'dark' else '浅色模式'}")

    def _browse_pandoc(self):
        path, _ = QFileDialog.getOpenFileName(
            self, "选择 pandoc.exe", "",
            "可执行文件 (*.exe);;所有文件 (*)")
        if path:
            self.pandoc_edit.setText(path)

    def _save_pandoc(self):
        path = self.pandoc_edit.text().strip()
        if not path:
            QMessageBox.warning(self, "提示", "请输入有效的路径。")
            return
        self._settings.setValue(SETTINGS_KEY_PANDOC, path)
        QMessageBox.information(self, "已保存", f"Pandoc 路径已更新。")

    def _set_theme(self, mode: str):
        self._settings.setValue(SETTINGS_KEY_THEME, mode)
        apply_theme(self._app, mode == "dark")
        self._refresh_theme_label()
