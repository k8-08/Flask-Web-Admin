# Flask Web Admin

<div align="center">

**基于 Flask + Vue3 的轻量级企业后台管理系统**

一个开箱即用的前后端分离管理平台，内置基础的 RBAC 权限系统、路由控制机制。

[![Python](https://img.shields.io/badge/Python-3.x-blue.svg)](https://www.python.org/)
[![Flask](https://img.shields.io/badge/Flask-3.x-green.svg)](https://flask.palletsprojects.com/)
[![Vue](https://img.shields.io/badge/Vue-3.5-brightgreen.svg)](https://vuejs.org/)
[![License](https://img.shields.io/badge/License-MIT-purple.svg)](LICENSE)

</div>

---

## 🌈 项目介绍

Flask Web Admin 是一个面向企业级应用的轻量级后台管理平台脚手架，采用前后端完全分离的架构设计。
本项目由早期的 FastAPI 版本重构而来，旨在提供一个更简单、轻量、更易上手的 Flask 方案，降低企业和独立开发者的学习成本，提高开发效率，完美契合中小型后台管理系统的开发需求。

**核心特性：**
- 🚀 **开箱即用**：高度封装的基础组件和通用功能，助你在几分钟内搭建并运行后台系统。
- 🔐 **完备的 RBAC 权限管理**：内置 `用户-角色-权限(菜单/按钮)` 三层权限模型。
- 🎯 **路由机制**：支持静态和动态路由配置，根据用户角色动态计算并渲染侧边栏菜单。
- 🛡️ **安全认证**：采用密码防泄漏加密（Bcrypt）与跨端无状态鉴权（JWT token）体系。
- 🎨 **现代化 UI**：全面支持主题动态切换（含暗黑模式和自定义主题配色方案）。
- 🛠️ **开发者友好**：前后端解耦，清晰的项目物理结构，使得开发人员能够更聚焦于特定业务逻辑的编写。

---

## 📋 技术栈

### 后端技术栈 (Backend)
- **核心框架**：[Flask](https://flask.palletsprojects.com/) - 稳定高效的轻量级 Python Web 框架
- **持久层框架**：[Flask-SQLAlchemy](https://flask-sqlalchemy.palletsprojects.com/) - 强类型关联 ORM，抽象数据库操作
- **数据库驱动**：PyMySQL - 纯 Python 编写的 MySQL 连接库
- **身份认证**：PyJWT - 安全轻量的 Token 生成与验证标准
- **密码加密**：Bcrypt - 极高安全强度的哈希密码加密工具
- **跨域配置**：Flask-CORS - 轻松解决由于前后端分离所带来的浏览端跨域请求拦截限制问题

### 前端技术栈 (Frontend)
- **核心框架**：[Vue 3](https://vuejs.org/) (Composition API) - 渐进式前端框架
- **构建工具**：[Vite](https://vitejs.dev/) - 下一代超快前端构建及开发工具
- **编程语言**：[TypeScript](https://www.typescriptlang.org/) - JavaScript 的超集，提供严格的数据类型检查体系
- **UI 组件库**：[Element Plus](https://element-plus.org/) - 专为 Vue 3 准备的丰富组件库体系
- **状态管理**：[Pinia](https://pinia.vuejs.org/) - 新一代轻量且强类型支持的 Vuex 替代品
- **路由管理**：Vue Router 4 - 掌控全局路径拦截与权限验证分发

---

## 🚀 快速开始

### 1. 获取代码

将项目拉取到本地任意开发目录：

```bash
git clone https://github.com/k8-08/Flask-Web-Admin.git
cd Flask-Web-Admin
```

### 2. 后端部署 (Backend Setup)

#### 2.1 环境准备
- 确保本地已安装 **Python 3.8+** 和 **MySQL 8.0+**
- 连接 MySQL 并建库：`CREATE DATABASE flaskapiwebadmin CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;`

#### 2.2 安装依赖
推荐使用 Python 虚拟环境，以避免全局包污染：

```bash
cd backend
python -m venv venv

# Windows 下激活虚拟环境:
venv\Scripts\activate
# Mac/Linux 下激活虚拟环境:
# source venv/bin/activate

# 安装项目所有依赖配置文件
pip install -r requirements.txt
```

#### 2.3 配置文件修改
检查 `backend/config.py`，将其中 `SQLALCHEMY_DATABASE_URI` 的内容修改为你实际的数据库账号密码：

```python
class Config:
    # 格式: mysql+pymysql://<用户名>:<密码>@<主机>:<端口>/<数据库名>?charset=utf8mb4
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:123456@127.0.0.1:3306/flaskapiwebadmin?charset=utf8mb4'
    SECRET_KEY = 'your_secret_key_here' # 生产环境请务必替换并保密
    # ...
```

*(温馨提示：如果你是首次运行，系统启动连接数据库时，会自动帮你建立数据表)*

#### 2.4 启动后端服务
在 `backend` 目录下执行：
```bash
python run.py
```
默认配置下，后端服务将在 `http://127.0.0.1:8100` 端口上监听请求。

---

### 3. 前端部署 (Frontend Setup)

#### 3.1 环境要求
- 推荐使用 Node.js 版本 **18.x** 及以上
- 推荐包管理工具 **npm / pnpm / yarn**

#### 3.2 安装依赖与配置
```bash
cd frontend
# 安装项目依赖（请勿删除 package-lock.json 进行强制替换）
npm install
```

如需修改请求后端的接口地址，请在 `.env.development` (本地开发阶段) 或 `.env.production` (线上生产阶段) 中修改 `VITE_API_BASE_URL`：

```env
# .env.development 示例
VITE_API_BASE_URL = 'http://127.0.0.1:8100'
```

#### 3.3 启动开发服务器
```bash
npm run dev
```
打开浏览器访问：`http://localhost:5173`。

🎯 **系统初始测试账号**：
- 账号：`admin`
- 密码：`123456`
*(或是你数据库导入文件中的实际账密信息)*

---

## 📦 目录结构精讲

### 核心后端结构 (backend/)
```text
backend/
├── app/
│   ├── api/            # 核心 Controller：路由控制器实现（例如 Auth、User、Role、Permission 等）
│   ├── models/         # 数据库 ORM 定义，数据模型对象类（映射数据库表结构）
│   ├── utils/          # 共用工具函数类（如 JWT 生成解析验证工具、统一规范响应体构建类）
│   └── __init__.py     # 核心文件：Flask Application 工厂模式实例化及全局蓝图路由注册
├── config.py           # 数据库及全局系统配置文件
├── requirements.txt    # 项目核心及其拓展依赖包列表
└── run.py              # 项目主程序入口启动器
```

### 核心前端结构 (frontend/)
```text
frontend/
├── src/
│   ├── api/            # 前端 Axios 请求逻辑和后端 API 方法隔离封装调用层
│   ├── assets/         # 静态资源存放中心（例如全站统一使用的基础 icon 图片、SVG 等）
│   ├── components/     # 全局复用高级业务组件（比如自定义高级 Table、高级筛选表单等）
│   ├── layout/         # UI 基础骨架组件（Header 顶栏、Sidebar 侧边栏、Menu 分级菜单等）
│   ├── router/         # Vue 全局声明式路由表配置与按角色进行动态路由匹配逻辑
│   ├── stores/         # Pinia 集中式状态管理总线（全局主题状态、用户登录资料持久化）
│   ├── theme/          # 全局 SCSS 样式定义、基础 Variables 与主题色系覆盖策略
│   ├── utils/          # 前端常规工具类代码集合（包含核心 Request 数据流拦截器设置）
│   └── views/          # 分散式视图页面组件（登录界面页、系统监控页、及各类业务数据管理页）
├── .env.development    # 本地局域网开发时期特殊环境变量配置表
├── .env.production     # 线上生产网络打包时期环境变量配置表
├── package.json        # 前端依赖索引与工作流 scripts 脚本配置
└── vite.config.ts      # Vite 开发服务器网络配参及底层代码 Rollup 构建编译策略选项
```

---

## 📸 系统操作截图

### 首页看板
![首页](static/img/index.png)

### 个人中心设置
![个人中心](static/img/ge.png)

### 登录认证页
![登录页](static/img/func.png)

### 系统外观参数配置
![参数配置](static/img/csssa.png)

### 操作与监控日志管理
![日志管理](static/img/csssb.png)

### 组织部门与岗位管理
![部门管理](static/img/gen.png)

### 动态菜单树与按钮权限配置
![菜单管理](static/img/qy.png)

### 用户身份与角色分配
![角色管理](static/img/report.png)

*(其余模块与深入特性使用请在线下亲自体验或按需补充截图)*

---

## 💡 构建与发版 (Build)

如果希望将前端编译成纯静态文件发布到 Nginx 等服务器上，在 `frontend` 目录下执行打包指令：
```bash
npm run build
```
编译成功后，代码将会默认输出在 `frontend/dist/` 目录。

---

## 🤝 参与贡献 (Contributing)

欢迎提交 Issues 和 Pull Requests 以帮助我们完善改进该项目。
1. Fork 本仓库
2. 创建一个基于新特性的开发或修复分支 (`git checkout -b feature/AmazingFeature`)
3. 提交你的修改代码 (`git commit -m 'Add some AmazingFeature'`)
4. 将分支推送至自己的主干 (`git push origin feature/AmazingFeature`)
5. 开源社区通过 Pull Request 审阅集成

---

## 📄 开源协议 (License)

本项目采用 [MIT License](LICENSE) 许可协议。自由用于商业或非商业项目开发，但请保留原作者归属及版权声明。
