import os
import subprocess
import sys

from PyQt6.QtCore import Qt, QSettings
from PyQt6.QtWidgets import (
    QApplication,
    QFileDialog,
    QFrame,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QMainWindow,
    QMessageBox,
    QPlainTextEdit,
    QPushButton,
    QStackedWidget,
    QVBoxLayout,
    QWidget,
)


SETTINGS_KEY_PANDOC = "pandoc/path"
SETTINGS_KEY_THEME = "theme/mode"
DEFAULT_PANDOC = r"D:\App\pandoc-3.9\pandoc.exe"


# ── helpers ──────────────────────────────────────────────────────────

def _find_pandoc(settings: QSettings) -> str:
    path = settings.value(SETTINGS_KEY_PANDOC, "")
    if path and os.path.isfile(path):
        return path
    if os.path.isfile(DEFAULT_PANDOC):
        return DEFAULT_PANDOC
    return "pandoc"


def _run_pandoc(pandoc_path: str, input_file: str, output_file: str,
                from_fmt: str, to_fmt: str) -> tuple[bool, str]:
    cmd = [pandoc_path, input_file, "-f", from_fmt, "-t", to_fmt, "-o", output_file]
    try:
        proc = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            creationflags=subprocess.CREATE_NO_WINDOW if sys.platform == "win32" else 0,
        )
        if proc.returncode == 0:
            return True, f"转换成功 → {output_file}"
        return False, proc.stderr.strip() or f"pandoc 返回错误码 {proc.returncode}"
    except FileNotFoundError:
        return False, "找不到 pandoc，请在设置中指定正确的 pandoc 路径"
    except Exception as exc:
        return False, f"执行出错: {exc}"


# ── theme ────────────────────────────────────────────────────────────

LIGHT_QSS = """
QMainWindow, QWidget {
    background-color: #f5f5f5;
    color: #1a1a1a;
}
QLineEdit, QPlainTextEdit {
    background-color: #ffffff;
    border: 1px solid #ccc;
    border-radius: 4px;
    padding: 4px;
}
QPushButton {
    background-color: #e0e0e0;
    border: 1px solid #bbb;
    border-radius: 4px;
    padding: 6px 16px;
}
QPushButton:hover { background-color: #d0d0d0; }
QPushButton:pressed { background-color: #c0c0c0; }
QPushButton#convertBtn {
    background-color: #0078d4;
    color: #fff;
    border: none;
    font-size: 14px;
    padding: 8px 24px;
}
QPushButton#convertBtn:hover { background-color: #106ebe; }
QPushButton#convertBtn:pressed { background-color: #005a9e; }
QPushButton#convertBtn:disabled { background-color: #a0c4e8; }
QFrame#sidebar {
    background-color: #e8e8e8;
    border-right: 1px solid #ccc;
}
QPushButton#navBtn {
    background: transparent;
    border: none;
    border-radius: 6px;
    text-align: left;
    padding: 10px 16px;
    font-size: 13px;
}
QPushButton#navBtn:hover { background-color: #ddd; }
QPushButton#navBtn:checked { background-color: #d0d0d0; font-weight: bold; }
QLabel#title {
    font-size: 16px;
    font-weight: bold;
    padding: 8px 0;
}
"""

DARK_QSS = """
QMainWindow, QWidget {
    background-color: #1e1e1e;
    color: #d4d4d4;
}
QLineEdit, QPlainTextEdit {
    background-color: #2d2d2d;
    border: 1px solid #555;
    border-radius: 4px;
    padding: 4px;
    color: #d4d4d4;
}
QPushButton {
    background-color: #3c3c3c;
    border: 1px solid #555;
    border-radius: 4px;
    padding: 6px 16px;
    color: #d4d4d4;
}
QPushButton:hover { background-color: #4a4a4a; }
QPushButton:pressed { background-color: #505050; }
QPushButton#convertBtn {
    background-color: #0078d4;
    color: #fff;
    border: none;
    font-size: 14px;
    padding: 8px 24px;
}
QPushButton#convertBtn:hover { background-color: #1a8ad4; }
QPushButton#convertBtn:pressed { background-color: #005a9e; }
QPushButton#convertBtn:disabled { background-color: #3a5a7a; }
QFrame#sidebar {
    background-color: #252526;
    border-right: 1px solid #3c3c3c;
}
QPushButton#navBtn {
    background: transparent;
    border: none;
    border-radius: 6px;
    text-align: left;
    padding: 10px 16px;
    font-size: 13px;
    color: #d4d4d4;
}
QPushButton#navBtn:hover { background-color: #37373d; }
QPushButton#navBtn:checked { background-color: #37373d; font-weight: bold; }
QLabel#title {
    font-size: 16px;
    font-weight: bold;
    padding: 8px 0;
}
"""


def apply_theme(app: QApplication, dark: bool):
    qss = DARK_QSS if dark else LIGHT_QSS
    app.setStyleSheet(qss)


# ── common: file-row widget ──────────────────────────────────────────

class FileRow(QWidget):
    """一行：标签 | 路径输入框 | 浏览按钮"""

    def __init__(self, label: str, dialog_mode: str, filter_str: str, parent=None):
        super().__init__(parent)
        self.dialog_mode = dialog_mode  # "open" or "save"
        self.filter_str = filter_str

        layout = QHBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)

        lbl = QLabel(label)
        lbl.setFixedWidth(70)
        layout.addWidget(lbl)

        self.edit = QLineEdit()
        self.edit.setReadOnly(True)
        layout.addWidget(self.edit, 1)

        btn = QPushButton("浏览…")
        btn.clicked.connect(self._browse)
        layout.addWidget(btn)

    def _browse(self):
        if self.dialog_mode == "open":
            path, _ = QFileDialog.getOpenFileName(self, "选择文件", "", self.filter_str)
        else:
            path, _ = QFileDialog.getSaveFileName(self, "保存到", "", self.filter_str)
        if path:
            self.edit.setText(path)

    def text(self) -> str:
        return self.edit.text()


# ── pages ────────────────────────────────────────────────────────────

class ConvertPage(QWidget):
    """通用的转换页面：选输入 → 选输出 → 转换"""

    def __init__(self, from_label: str, to_label: str, from_fmt: str, to_fmt: str,
                 in_filter: str, out_filter: str, app_settings: QSettings, parent=None):
        super().__init__(parent)
        self.from_fmt = from_fmt
        self.to_fmt = to_fmt
        self.settings = app_settings

        layout = QVBoxLayout(self)
        layout.setContentsMargins(24, 24, 24, 24)
        layout.setSpacing(16)

        title = QLabel(f"{from_label} → {to_label}")
        title.setObjectName("title")
        layout.addWidget(title)

        layout.addWidget(QLabel(f"源文件（{from_label}）："))
        self.src_row = FileRow("文件", "open", in_filter)
        layout.addWidget(self.src_row)

        layout.addWidget(QLabel(f"目标文件（{to_label}）："))
        self.dst_row = FileRow("保存到", "save", out_filter)
        layout.addWidget(self.dst_row)

        self.convert_btn = QPushButton("开始转换")
        self.convert_btn.setObjectName("convertBtn")
        self.convert_btn.setFixedHeight(40)
        self.convert_btn.clicked.connect(self._convert)
        layout.addWidget(self.convert_btn)

        self.log = QPlainTextEdit()
        self.log.setReadOnly(True)
        self.log.setFixedHeight(120)
        layout.addWidget(self.log)

        layout.addStretch()

    def _convert(self):
        src = self.src_row.text()
        dst = self.dst_row.text()
        if not src:
            self._log("请选择源文件。")
            return
        if not dst:
            self._log("请选择保存路径。")
            return

        pandoc = _find_pandoc(self.settings)
        self._log(f"正在转换…")
        ok, msg = _run_pandoc(pandoc, src, dst, self.from_fmt, self.to_fmt)
        self._log(msg)

    def _log(self, text: str):
        self.log.appendPlainText(text)


class SettingsPage(QWidget):
    """设置页面：pandoc 路径 + 深浅主题切换"""

    def __init__(self, app: QApplication, settings: QSettings, parent=None):
        super().__init__(parent)
        self.app = app
        self.settings = settings

        layout = QVBoxLayout(self)
        layout.setContentsMargins(24, 24, 24, 24)
        layout.setSpacing(16)

        title = QLabel("设置")
        title.setObjectName("title")
        layout.addWidget(title)

        # ── pandoc path ──
        layout.addWidget(QLabel("Pandoc 可执行文件路径："))
        pandoc_row = QHBoxLayout()
        self.pandoc_edit = QLineEdit()
        self.pandoc_edit.setText(_find_pandoc(settings))
        pandoc_row.addWidget(self.pandoc_edit, 1)

        pandoc_btn = QPushButton("浏览…")
        pandoc_btn.clicked.connect(self._browse_pandoc)
        pandoc_row.addWidget(pandoc_btn)
        layout.addLayout(pandoc_row)

        save_btn = QPushButton("保存 pandoc 路径")
        save_btn.clicked.connect(self._save_pandoc)
        layout.addWidget(save_btn)

        # ── separator ──
        line = QFrame()
        line.setFrameShape(QFrame.Shape.HLine)
        line.setFrameShadow(QFrame.Shadow.Sunken)
        layout.addWidget(line)

        # ── theme ──
        layout.addWidget(QLabel("界面主题："))
        self.theme_dark_btn = QPushButton("切换为深色模式")
        self.theme_light_btn = QPushButton("切换为浅色模式")
        self.theme_dark_btn.clicked.connect(lambda: self._set_theme("dark"))
        self.theme_light_btn.clicked.connect(lambda: self._set_theme("light"))
        layout.addWidget(self.theme_dark_btn)
        layout.addWidget(self.theme_light_btn)

        # 文字提示当前主题
        current = settings.value(SETTINGS_KEY_THEME, "light")
        self.theme_label = QLabel(f"当前：{'深色' if current == 'dark' else '浅色'}模式")
        layout.addWidget(self.theme_label)

        layout.addStretch()

    def _browse_pandoc(self):
        path, _ = QFileDialog.getOpenFileName(self, "选择 pandoc.exe", "",
                                              "可执行文件 (*.exe);;所有文件 (*)")
        if path:
            self.pandoc_edit.setText(path)

    def _save_pandoc(self):
        path = self.pandoc_edit.text().strip()
        if path:
            self.settings.setValue(SETTINGS_KEY_PANDOC, path)
            QMessageBox.information(self, "已保存", f"Pandoc 路径已保存:\n{path}")
        else:
            QMessageBox.warning(self, "错误", "请输入有效的路径。")

    def _set_theme(self, mode: str):
        self.settings.setValue(SETTINGS_KEY_THEME, mode)
        apply_theme(self.app, mode == "dark")
        self.theme_label.setText(f"当前：{'深色' if mode == 'dark' else '浅色'}模式")


# ── sidebar ──────────────────────────────────────────────────────────

class Sidebar(QFrame):
    def __init__(self, stack: QStackedWidget, parent=None):
        super().__init__(parent)
        self.setObjectName("sidebar")
        self.setFixedWidth(160)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(8, 16, 8, 16)
        layout.setSpacing(4)

        logo = QLabel("ConvertMD")
        logo.setAlignment(Qt.AlignmentFlag.AlignCenter)
        logo.setStyleSheet("font-size: 15px; font-weight: bold; padding: 8px 0;")
        layout.addWidget(logo)

        line = QFrame()
        line.setFrameShape(QFrame.Shape.HLine)
        line.setFrameShadow(QFrame.Shadow.Sunken)
        layout.addWidget(line)

        self.btn_md2word = QPushButton("  MD → Word")
        self.btn_word2md = QPushButton("  Word → MD")
        self.btn_settings = QPushButton("  设置")

        for btn in (self.btn_md2word, self.btn_word2md, self.btn_settings):
            btn.setObjectName("navBtn")
            btn.setCheckable(True)
            btn.setFixedHeight(38)
            layout.addWidget(btn)

        self.btn_md2word.clicked.connect(lambda: self._switch(0, self.btn_md2word))
        self.btn_word2md.clicked.connect(lambda: self._switch(1, self.btn_word2md))
        self.btn_settings.clicked.connect(lambda: self._switch(2, self.btn_settings))

        self._buttons = [self.btn_md2word, self.btn_word2md, self.btn_settings]
        self._stack = stack
        self._switch(0, self.btn_md2word)

        layout.addStretch()

    def _switch(self, index: int, active_btn: QPushButton):
        for btn in self._buttons:
            btn.setChecked(btn is active_btn)
        self._stack.setCurrentIndex(index)


# ── main window ──────────────────────────────────────────────────────

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("ConvertMD — Markdown ⇄ Word 转换工具")
        self.resize(760, 520)

        self.settings = QSettings("ConvertMD", "ConvertMD")

        self._stack = QStackedWidget()

        self._page_md2word = ConvertPage("Markdown", "Word", "markdown", "docx",
                                         "Markdown 文件 (*.md);;所有文件 (*)",
                                         "Word 文档 (*.docx);;所有文件 (*)",
                                         self.settings)
        self._page_word2md = ConvertPage("Word", "Markdown", "docx", "markdown",
                                         "Word 文档 (*.docx);;所有文件 (*)",
                                         "Markdown 文件 (*.md);;所有文件 (*)",
                                         self.settings)
        self._page_settings = SettingsPage(
            QApplication.instance(), self.settings)

        self._stack.addWidget(self._page_md2word)   # 0
        self._stack.addWidget(self._page_word2md)   # 1
        self._stack.addWidget(self._page_settings)  # 2

        sidebar = Sidebar(self._stack)

        central = QWidget()
        hbox = QHBoxLayout(central)
        hbox.setContentsMargins(0, 0, 0, 0)
        hbox.setSpacing(0)
        hbox.addWidget(sidebar)
        hbox.addWidget(self._stack, 1)
        self.setCentralWidget(central)

        # 加载主题
        theme_mode = self.settings.value(SETTINGS_KEY_THEME, "light")
        apply_theme(QApplication.instance(), theme_mode == "dark")


# ── entry ────────────────────────────────────────────────────────────

def main():
    app = QApplication(sys.argv)
    app.setOrganizationName("ConvertMD")
    app.setApplicationName("ConvertMD")
    win = MainWindow()
    win.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
