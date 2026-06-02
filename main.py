# ── ConvertMD: Markdown ⇄ Word converter ────────────────────────────

import struct
import sys

from PyQt6.QtWidgets import QApplication

from ui.app_icon import make_icon
from ui.main_window import MainWindow


def _generate_icons():
    """Generate icon.png and icon.ico in the current directory, then exit."""
    pix = make_icon().pixmap(256, 256)
    pix.save("icon.png")
    print("icon.png saved")

    # Build a minimal .ico wrapping the PNG
    png_bytes = bytearray()
    buf = bytearray()
    pix.save("_tmp_icon.png")
    with open("_tmp_icon.png", "rb") as f:
        png_bytes = f.read()

    # ICO = 6-byte header + 16-byte dir-entry + PNG data
    import os
    os.remove("_tmp_icon.png")

    data_offset = 6 + 16
    ico = struct.pack("<HHH", 0, 1, 1)  # reserved, type=ICO, 1 image
    ico += struct.pack("<BBBBHHII",
        0, 0, 0, 0,     # 256x256 stored as 0
        1, 32,           # planes=1, bpp=32
        len(png_bytes),  # image size
        data_offset,     # offset to image data
    )
    with open("icon.ico", "wb") as f:
        f.write(ico + png_bytes)
    print("icon.ico saved")


def main():
    app = QApplication(sys.argv)
    app.setOrganizationName("ConvertMD")
    app.setApplicationName("ConvertMD")

    if "--gen-icon" in sys.argv:
        _generate_icons()
        return

    app.setWindowIcon(make_icon())
    win = MainWindow()
    win.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
