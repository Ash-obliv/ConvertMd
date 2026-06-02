# ConvertMD

Markdown、Word、PDF 文档互转工具，基于 PyQt6 + Pandoc + pdfplumber。

## 功能

- **MD → Word**：Markdown 文件一键转换为 .docx 文档
- **Word → MD**：.docx 文档一键转换为 Markdown 文件
- **PDF → MD**：提取 PDF 文本内容，按页输出为 Markdown 文件
- 选择源文件后自动生成目标路径，无需手动填写
- 转换成功弹窗，可直接打开文件所在文件夹
- 支持浅色 / 深色主题切换
- 可自定义 Pandoc 路径

## 快速开始

### 方式一：下载 EXE（推荐）

从 [Releases](../../releases) 页面下载 `ConvertMD.exe`，双击运行即可。

> - MD/Word 互转需要安装 [Pandoc](https://pandoc.org/installing.html) 并在系统 PATH 中
> - PDF 转 MD 无需 Pandoc，内置 pdfplumber 处理
> - 如果 Pandoc 不在 PATH 里，可在软件的 **设置** 页面手动指定路径

### 方式二：从源码运行

```bash
git clone git@github.com:Ash-obliv/ConvertMd.git
cd ConvertMd

python -m venv venv
venv\Scripts\activate      # Windows

pip install -r requirements.txt
python main.py
```

## 使用说明

1. 打开软件，左侧导航栏选择转换模式（MD→Word / Word→MD / PDF→MD）
2. 点击 **浏览…** 选择源文件，目标路径会自动生成在同目录下
3. 点击 **开始转换**，等待完成
4. 弹窗提示成功后，可点击 **打开所在文件夹** 直接定位文件

> PDF 转 MD 会将每页内容以 `## 第 N 页` 标题分隔，方便后续用 AI 处理。

## 环境要求

| 依赖 | 说明 |
|------|------|
| Python | 3.10+（仅源码运行需要） |
| Pandoc | 3.x 推荐（MD/Word 互转必需，PDF 转 MD 不需要） |
| PyQt6 | 6.10+（pip 自动安装） |
| pdfplumber | 0.11+（pip 自动安装，仅 PDF 转 MD） |

## 打包

```bash
pip install pyinstaller
python main.py --gen-icon
pyinstaller --onefile --windowed --icon=icon.ico --name=ConvertMD main.py
# 输出在 dist/ConvertMD.exe
```

## 项目结构

```
Convertmd/
├── main.py              # 入口
├── requirements.txt
├── core/
│   ├── __init__.py      # 配置常量、find_pandoc()
│   └── converter.py     # pandoc / pdfplumber 转换封装
├── ui/
│   ├── app_icon.py      # 程序化生成图标
│   ├── convert_page.py  # 转换页面
│   ├── file_row.py      # 文件选择行组件
│   ├── main_window.py   # 主窗口
│   ├── settings_page.py # 设置页面
│   ├── sidebar.py       # 左侧导航栏
│   └── theme.py         # 浅色/深色主题
```

## 许可

MIT License — 详见 [LICENSE](LICENSE) 文件。
