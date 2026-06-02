# ── ui: programmatic app icon ───────────────────────────────────────

from PyQt6.QtCore import Qt, QRectF, QPointF, QSize
from PyQt6.QtGui import (
    QColor, QFont, QIcon, QLinearGradient, QPainter, QPainterPath,
    QPen, QPixmap, QPolygonF,
)


def make_icon() -> QIcon:
    """Generate the app icon at runtime (no external files needed)."""
    SIZE = 256
    pix = QPixmap(SIZE, SIZE)
    pix.fill(Qt.GlobalColor.transparent)

    p = QPainter(pix)
    p.setRenderHint(QPainter.RenderHint.Antialiasing)

    # Background rounded rect with indigo-violet gradient
    r = 48
    bg_rect = QRectF(4, 4, SIZE - 8, SIZE - 8)
    grad = QLinearGradient(0, 0, SIZE, SIZE)
    grad.setColorAt(0.0, QColor("#4f46e5"))
    grad.setColorAt(1.0, QColor("#7c3aed"))
    bg_path = QPainterPath()
    bg_path.addRoundedRect(bg_rect, r, r)
    p.fillPath(bg_path, grad)

    # Left document icon (semi-transparent white)
    doc_color = QColor("#ffffff")
    doc_color.setAlpha(230)
    p.setPen(Qt.PenStyle.NoPen)
    p.setBrush(doc_color)

    lx, dy, dw, dh, dr = 58, 84, 52, 64, 8
    ldoc = QPainterPath()
    ldoc.addRoundedRect(QRectF(lx, dy, dw, dh), dr, dr)
    ldoc.moveTo(lx + dw - 12, dy)
    ldoc.lineTo(lx + dw - 12, dy + 12)
    ldoc.lineTo(lx + dw, dy + 12)
    ldoc.closeSubpath()
    p.drawPath(ldoc)

    # Text lines on left doc
    p.setPen(QPen(QColor("#7c3aed"), 3, Qt.PenStyle.SolidLine))
    ll, lr = lx + 10, lx + dw - 16
    for yd in (20, 29, 38):
        yy = dy + yd
        p.drawLine(QPointF(ll, yy), QPointF(lr, yy))

    # Right document icon
    rx = 146
    rdoc = QPainterPath()
    rdoc.addRoundedRect(QRectF(rx, dy, dw, dh), dr, dr)
    rdoc.moveTo(rx + dw - 12, dy)
    rdoc.lineTo(rx + dw - 12, dy + 12)
    rdoc.lineTo(rx + dw, dy + 12)
    rdoc.closeSubpath()
    p.drawPath(rdoc)

    # "W" on right doc
    p.setPen(Qt.PenStyle.NoPen)
    f = QFont("Segoe UI", 26, QFont.Weight.Bold)
    p.setFont(f)
    p.setPen(QColor("#7c3aed"))
    p.drawText(QRectF(rx, dy, dw, dh), Qt.AlignmentFlag.AlignCenter, "W")

    # Bidirectional arrows in amber
    arrow_color = QColor("#fbbf24")
    p.setPen(Qt.PenStyle.NoPen)
    p.setBrush(arrow_color)
    cx = SIZE / 2
    cy = dy + dh / 2

    left_arrow = QPolygonF([
        QPointF(cx - 18, cy),
        QPointF(cx - 4, cy - 11),
        QPointF(cx - 4, cy - 4),
        QPointF(cx + 10, cy - 4),
        QPointF(cx + 10, cy + 4),
        QPointF(cx - 4, cy + 4),
        QPointF(cx - 4, cy + 11),
    ])
    p.drawPolygon(left_arrow)

    right_arrow = QPolygonF([
        QPointF(cx + 18, cy),
        QPointF(cx + 4, cy - 11),
        QPointF(cx + 4, cy - 4),
        QPointF(cx - 10, cy - 4),
        QPointF(cx - 10, cy + 4),
        QPointF(cx + 4, cy + 4),
        QPointF(cx + 4, cy + 11),
    ])
    p.drawPolygon(right_arrow)

    # Bottom text
    f2 = QFont("Segoe UI", 18, QFont.Weight.Bold)
    p.setFont(f2)
    p.setPen(QColor("#c7d2fe"))
    p.drawText(QRectF(0, 170, SIZE, 50), Qt.AlignmentFlag.AlignHCenter, "ConvertMD")

    p.end()
    return QIcon(pix)
