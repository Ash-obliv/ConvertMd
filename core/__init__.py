# ── core: settings keys & defaults ───────────────────────────────────

import os
from PyQt6.QtCore import QSettings

SETTINGS_KEY_PANDOC = "pandoc/path"
SETTINGS_KEY_THEME = "theme/mode"

DEFAULT_PANDOC = "pandoc"


def find_pandoc(settings: QSettings) -> str:
    path = settings.value(SETTINGS_KEY_PANDOC, "")
    if path and os.path.isfile(path):
        return path
    if os.path.isfile(DEFAULT_PANDOC):
        return DEFAULT_PANDOC
    return "pandoc"
