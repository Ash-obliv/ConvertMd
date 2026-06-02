# ── core: pandoc wrapper ─────────────────────────────────────────────

import subprocess
import sys


def run(source: str, target: str, from_fmt: str, to_fmt: str,
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
