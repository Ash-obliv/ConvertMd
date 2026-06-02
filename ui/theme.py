# ── ui: stylesheets ──────────────────────────────────────────────────

LIGHT_QSS = """
QMainWindow, QWidget {
    background-color: #f8fafc;
    color: #334155;
    font-family: "Microsoft YaHei", "Segoe UI", sans-serif;
}
QLineEdit {
    background-color: #fff;
    border: 1px solid #cbd5e1;
    border-radius: 6px;
    padding: 6px 10px;
    font-size: 13px;
    color: #1e293b;
}
QLineEdit:focus { border-color: #6366f1; }

QPlainTextEdit {
    background-color: #fff;
    border: 1px solid #cbd5e1;
    border-radius: 6px;
    padding: 8px;
    font-size: 12px;
    color: #334155;
}

QPushButton {
    background-color: #f1f5f9;
    border: 1px solid #cbd5e1;
    border-radius: 6px;
    padding: 6px 16px;
    font-size: 13px;
    color: #334155;
}
QPushButton:hover { background-color: #e2e8f0; }
QPushButton:pressed { background-color: #cbd5e1; }

QPushButton#convertBtn {
    background-color: #4f46e5;
    color: #fff;
    border: none;
    font-size: 15px;
    font-weight: bold;
    padding: 10px 28px;
}
QPushButton#convertBtn:hover { background-color: #4338ca; }
QPushButton#convertBtn:pressed { background-color: #3730a3; }
QPushButton#convertBtn:disabled { background-color: #a5b4fc; }

QPushButton#browseBtn {
    background-color: #f1f5f9;
    border: 1px solid #cbd5e1;
    border-radius: 6px;
    padding: 6px 14px;
    font-size: 12px;
    color: #475569;
}
QPushButton#browseBtn:hover { background-color: #e2e8f0; }

QFrame#sidebar {
    background-color: #eef2ff;
    border-right: 1px solid #c7d2fe;
}
QPushButton#navBtn {
    background: transparent;
    border: none;
    border-radius: 8px;
    text-align: left;
    padding: 12px 16px;
    font-size: 13px;
    color: #4338ca;
}
QPushButton#navBtn:hover { background-color: #e0e7ff; }
QPushButton#navBtn:checked {
    background-color: #c7d2fe;
    font-weight: bold;
    color: #312e81;
}

QLabel#pageTitle {
    font-size: 20px;
    font-weight: bold;
    padding: 4px 0 12px 0;
    color: #1e1b4b;
}
QLabel#sectionLabel {
    font-size: 13px;
    font-weight: bold;
    color: #6366f1;
    padding-top: 8px;
}
"""

DARK_QSS = """
QMainWindow, QWidget {
    background-color: #0f172a;
    color: #cbd5e1;
    font-family: "Microsoft YaHei", "Segoe UI", sans-serif;
}
QLineEdit {
    background-color: #1e293b;
    border: 1px solid #475569;
    border-radius: 6px;
    padding: 6px 10px;
    font-size: 13px;
    color: #e2e8f0;
}
QLineEdit:focus { border-color: #818cf8; }

QPlainTextEdit {
    background-color: #1e293b;
    border: 1px solid #475569;
    border-radius: 6px;
    padding: 8px;
    font-size: 12px;
    color: #cbd5e1;
}

QPushButton {
    background-color: #1e293b;
    border: 1px solid #475569;
    border-radius: 6px;
    padding: 6px 16px;
    font-size: 13px;
    color: #cbd5e1;
}
QPushButton:hover { background-color: #334155; }
QPushButton:pressed { background-color: #475569; }

QPushButton#convertBtn {
    background-color: #6366f1;
    color: #fff;
    border: none;
    font-size: 15px;
    font-weight: bold;
    padding: 10px 28px;
}
QPushButton#convertBtn:hover { background-color: #4f46e5; }
QPushButton#convertBtn:pressed { background-color: #4338ca; }
QPushButton#convertBtn:disabled { background-color: #3730a3; }

QPushButton#browseBtn {
    background-color: #1e293b;
    border: 1px solid #475569;
    border-radius: 6px;
    padding: 6px 14px;
    font-size: 12px;
    color: #94a3b8;
}
QPushButton#browseBtn:hover { background-color: #334155; }

QFrame#sidebar {
    background-color: #1e1b4b;
    border-right: 1px solid #312e81;
}
QPushButton#navBtn {
    background: transparent;
    border: none;
    border-radius: 8px;
    text-align: left;
    padding: 12px 16px;
    font-size: 13px;
    color: #a5b4fc;
}
QPushButton#navBtn:hover { background-color: #312e81; }
QPushButton#navBtn:checked {
    background-color: #3730a3;
    font-weight: bold;
    color: #e0e7ff;
}

QLabel#pageTitle {
    font-size: 20px;
    font-weight: bold;
    padding: 4px 0 12px 0;
    color: #e0e7ff;
}
QLabel#sectionLabel {
    font-size: 13px;
    font-weight: bold;
    color: #818cf8;
    padding-top: 8px;
}
"""


def apply_theme(app, dark: bool):
    app.setStyleSheet(DARK_QSS if dark else LIGHT_QSS)
