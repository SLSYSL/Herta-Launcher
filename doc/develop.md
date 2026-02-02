<h1 align="center">黑塔终端开发文档</h1>

## 环境要求
- Node.js
- Python 3.9+

## 安装依赖
- 前端:
  - 方法一: `make frontend-install`
  - 方法二: `cd packages/frontend && npm install`
- 后端:
  - 方法一: `make install`
  - 方法二: `pip install -r requirements.txt`

## Makefile 说明
- `frontend-install`: 使用 NPM 安装前端依赖
- `frontend-build`: 使用 NPM 编译前端文件
- `install`: 使用 PIP 安装后端依赖
- `run`: 启动程序
- `build`: 使用 Pyinstaller 编译二进制文件
- `example`: 启动示例程序