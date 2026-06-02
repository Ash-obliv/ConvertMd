# ── ui: conversion page (md→word or word→md) ────────────────────────

import os

from PyQt6.QtCore import QSettings
from PyQt6.QtWidgets import (
    QApplication,
    QLabel,
    QMessageBox,
    QPlainTextEdit,
    QPushButton,
    QVBoxLayout,
    QWidget,
)

from core import find_pandoc
from core.converter import run
from ui.file_row import FileRow


class ConvertPage(QWidget):
    def __init__(self, title: str, from_fmt: str, to_fmt: str,
                 in_ext: str, out_ext: str, in_filter: str, out_filter: str,
                 settings: QSettings, parent=None):
        super().__init__(parent)
        self._from_fmt = from_fmt
        self._to_fmt = to_fmt
        self._out_ext = out_ext
        self._settings = settings

        layout = QVBoxLayout(self)
        layout.setContentsMargins(32, 28, 32, 24)
        layout.setSpacing(14)

        # 标题
        page_title = QLabel(title)
        page_title.setObjectName("pageTitle")
        layout.addWidget(page_title)

        # 说明
        layout.addWidget(QLabel(f"选择 {in_ext.upper()} 文件，自动生成 {out_ext.upper()} 保存路径。"))

        # 源文件
        src_label = QLabel("源文件")
        src_label.setObjectName("sectionLabel")
        layout.addWidget(src_label)
        self.src_row = FileRow(in_ext.upper(), "open", in_filter)
        self.src_row.file_changed.connect(self._on_src_changed)
        layout.addWidget(self.src_row)

        # 目标文件
        dst_label = QLabel("保存到")
        dst_label.setObjectName("sectionLabel")
        layout.addWidget(dst_label)
        self.dst_row = FileRow(out_ext.upper(), "save", out_filter)
        layout.addWidget(self.dst_row)

        # 转换按钮
        self.convert_btn = QPushButton("开始转换")
        self.convert_btn.setObjectName("convertBtn")
        self.convert_btn.setFixedHeight(44)
        self.convert_btn.clicked.connect(self._convert)
        layout.addWidget(self.convert_btn)
        layout.addSpacing(8)

        # 日志区
        self.log = QPlainTextEdit()
        self.log.setReadOnly(True)
        self.log.setFixedHeight(100)
        self.log.setPlaceholderText("转换日志将显示在这里…")
        layout.addWidget(self.log)

        layout.addStretch()

    # ── auto-fill ─────────────────────────────────────────────────

    def _on_src_changed(self, path: str):
        """源文件变动时自动推算目标路径"""
        if not path:
            return
        base, _ = os.path.splitext(path)
        target = base + self._out_ext
        self.dst_row.set_text(target)

    # ── convert ───────────────────────────────────────────────────

    def _convert(self):
        src = self.src_row.text()
        dst = self.dst_row.text()
        if not src:
            self._log("请先选择源文件。")
            return
        if not dst:
            self._log("请指定保存路径。")
            return

        pandoc = find_pandoc(self._settings)
        self._log("正在转换，请稍候…")
        self.convert_btn.setEnabled(False)
        QApplication.processEvents()

        ok, msg = run(src, dst, self._from_fmt, self._to_fmt, pandoc)

        self.convert_btn.setEnabled(True)
        if ok:
            self._log("转换成功。")
            self._show_success(msg)
        else:
            self._log(f"转换失败: {msg}")

    def _show_success(self, filepath: str):
        msg = QMessageBox(self)
        msg.setWindowTitle("转换完成")
        msg.setIcon(QMessageBox.Icon.Information)
        msg.setText("文件转换成功！")
        msg.setInformativeText(filepath)
        ok_btn = msg.addButton("确定", QMessageBox.ButtonRole.AcceptRole)
        folder_btn = msg.addButton("打开所在文件夹", QMessageBox.ButtonRole.ActionRole)
        msg.setDefaultButton(ok_btn)
        msg.exec()

        if msg.clickedButton() == folder_btn:
            folder = os.path.dirname(filepath)
            os.startfile(folder)

    def _log(self, text: str):
        self.log.appendPlainText(text)
