# ── ui: main window ─────────────────────────────────────────────────

from PyQt6.QtCore import QSettings
from PyQt6.QtWidgets import (
    QApplication,
    QHBoxLayout,
    QMainWindow,
    QStackedWidget,
    QWidget,
)

from ui.app_icon import make_icon
from ui.convert_page import ConvertPage
from ui.settings_page import SettingsPage
from ui.sidebar import Sidebar
from ui.theme import apply_theme
from core.converter import pdf_to_md

SETTINGS_KEY_THEME = "theme/mode"


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("ConvertMD — 文档转换工具")
        self.resize(800, 540)
        self.setMinimumSize(680, 440)
        self.setWindowIcon(make_icon())

        self._settings = QSettings("ConvertMD", "ConvertMD")
        self._stack = QStackedWidget()

        # page 0: MD → Word
        self._stack.addWidget(ConvertPage(
            "MD → Word", "markdown", "docx",
            ".md", ".docx",
            "Markdown (*.md);;所有文件 (*)",
            "Word 文档 (*.docx);;所有文件 (*)",
            self._settings,
        ))

        # page 1: Word → MD
        self._stack.addWidget(ConvertPage(
            "Word → MD", "docx", "markdown",
            ".docx", ".md",
            "Word 文档 (*.docx);;所有文件 (*)",
            "Markdown (*.md);;所有文件 (*)",
            self._settings,
        ))

        # page 2: PDF → MD
        self._stack.addWidget(ConvertPage(
            "PDF → MD", "pdf", "markdown",
            ".pdf", ".md",
            "PDF 文件 (*.pdf);;所有文件 (*)",
            "Markdown (*.md);;所有文件 (*)",
            self._settings,
            convert_func=pdf_to_md,
        ))

        # page 3: Settings
        self._stack.addWidget(SettingsPage(
            QApplication.instance(), self._settings))

        # layout
        sidebar = Sidebar(self._stack)

        central = QWidget()
        hbox = QHBoxLayout(central)
        hbox.setContentsMargins(0, 0, 0, 0)
        hbox.setSpacing(0)
        hbox.addWidget(sidebar)
        hbox.addWidget(self._stack, 1)
        self.setCentralWidget(central)

        # theme
        mode = self._settings.value(SETTINGS_KEY_THEME, "light")
        apply_theme(QApplication.instance(), mode == "dark")
