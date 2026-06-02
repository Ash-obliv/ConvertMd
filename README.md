# ConvertMD

Markdown 与 Word 文档互转工具，基于 PyQt6 + Pandoc。

## 功能

- **MD → Word**：将 Markdown 文件转换为 Word 文档（.docx）
- **Word → MD**：将 Word 文档转换为 Markdown 文件
- 支持自定义选择输入文件和输出路径
- 可自定义 Pandoc 可执行文件路径
- 支持深色 / 浅色主题切换

## 环境要求

- Python 3.10+
- [Pandoc](https://pandoc.org/installing.html)（推荐 3.x）

## 安装

```bash
# 1. 克隆仓库
git clone git@github.com:Ash-obliv/ConvertMd.git
cd ConvertMd

# 2. 创建虚拟环境（可选）
python -m venv venv
# Windows
venv\Scripts\activate
# macOS / Linux
source venv/bin/activate

# 3. 安装依赖
pip install -r requirements.txt
```

## 使用

```bash
python main.py
```

首次运行会自动检测 Pandoc 路径。如果默认路径不对，在 **设置** 页面中指定 Pandoc 的正确位置。

## 许可

MIT License — 详见 [LICENSE](LICENSE) 文件。
