# ConvertMD

Markdown ↔ Word 双向转换工具，基于 PyQt6 + Pandoc，支持 Windows。

## 功能

- **MD → Word**：Markdown 文件一键转换为 .docx 文档
- **Word → MD**：.docx 文档一键转换为 Markdown 文件
- 选择源文件后自动生成目标路径，无需手动填写
- 转换成功弹窗，可直接打开文件所在文件夹
- 支持浅色 / 深色主题切换
- 可自定义 Pandoc 路径

## 快速开始

### 方式一：下载 EXE（推荐）

从 [Releases](../../releases) 页面下载 `ConvertMD.exe`，双击运行即可。

> 需要先安装 [Pandoc](https://pandoc.org/installing.html) 并确保 `pandoc` 在系统 PATH 中。如果不在 PATH 里，可在软件的 **设置** 页面手动指定 pandoc.exe 路径。

### 方式二：从源码运行

```bash
# 1. 克隆仓库
git clone git@github.com:Ash-obliv/ConvertMd.git
cd ConvertMd

# 2. 创建虚拟环境（可选）
python -m venv venv
venv\Scripts\activate     # Windows
# source venv/bin/activate  # macOS / Linux

# 3. 安装依赖
pip install -r requirements.txt

# 4. 运行
python main.py
```

## 使用说明

1. 打开软件，左侧导航栏选择 **MD → Word** 或 **Word → MD**
2. 点击 **浏览…** 选择源文件，目标路径会自动生成在同目录下
3. 点击 **开始转换**，等待完成
4. 弹窗提示成功后，可点击 **打开所在文件夹** 直接定位文件

如果 Pandoc 不在系统 PATH 中：
- 进入 **设置** 页面，指定 pandoc.exe 的实际路径，点击保存

## 环境要求

| 依赖 | 说明 |
|------|------|
| Python | 3.10+（仅源码运行需要） |
| Pandoc | 3.x 推荐 |
| PyQt6 | 6.10+（pip 自动安装） |

## 打包

```bash
pip install pyinstaller
python main.py --gen-icon        # 生成图标文件
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
│   └── converter.py     # pandoc 调用封装
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
