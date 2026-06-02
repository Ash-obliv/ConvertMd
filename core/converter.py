# ── core: converters ─────────────────────────────────────────────────

import subprocess
import sys


def run_pandoc(source: str, target: str, from_fmt: str, to_fmt: str,
               pandoc_path: str) -> tuple[bool, str]:
    """执行 pandoc 转换。返回 (成功, 消息)。"""
    cmd = [pandoc_path, source, "-f", from_fmt, "-t", to_fmt, "-o", target]
    try:
        proc = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            creationflags=subprocess.CREATE_NO_WINDOW if sys.platform == "win32" else 0,
        )
        if proc.returncode == 0:
            return True, target
        detail = proc.stderr.strip() or f"pandoc 返回错误码 {proc.returncode}"
        return False, detail
    except FileNotFoundError:
        return False, "找不到 pandoc，请在设置中指定正确的路径。"
    except Exception as exc:
        return False, f"执行出错: {exc}"


def pdf_to_md(source: str, target: str) -> tuple[bool, str]:
    """使用 pdfplumber 将 PDF 转为 Markdown。返回 (成功, 消息)。"""
    try:
        import pdfplumber
    except ImportError:
        return False, "缺少 pdfplumber 库，请运行: pip install pdfplumber"

    try:
        md_parts = []
        with pdfplumber.open(source) as pdf:
            for i, page in enumerate(pdf.pages, 1):
                text = page.extract_text()
                if text:
                    md_parts.append(f"## 第 {i} 页\n\n{text}\n")
        if not md_parts:
            return False, "PDF 中没有可提取的文本内容。"

        with open(target, "w", encoding="utf-8") as f:
            f.write("\n".join(md_parts))
        return True, target
    except Exception as exc:
        return False, f"PDF 转换出错: {exc}"
