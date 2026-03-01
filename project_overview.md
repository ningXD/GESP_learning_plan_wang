# GESPC++ 学习计划项目概述

## 项目简介
这是一个面向 GESPC++ 编程竞赛的学习计划平台，包含前端和后端两部分。

## 项目结构

### 前端结构
```
frontend/
├── core/
│   ├── index.html          # 首页
│   ├── study_plan.html     # 学习计划页面
│   ├── wiki.html           # 知识库页面
│   └── progress.html       # 进度跟踪页面
├── programming/
│   ├── online_programming.html  # 在线编程界面
│   └── code_editor.js      # 代码编辑器相关功能
└── static/
    ├── css/                # 样式文件
    ├── js/                 # JavaScript 文件
    └── images/             # 图片资源
```

### 后端结构
```
backend/
├── config/                 # 配置文件
│   └── .env               # 环境变量配置
├── models/                 # 数据库模型
│   ├── __init__.py
│   └── models.py          # 模型定义
├── routes/                 # API 路由
│   ├── __init__.py
│   ├── auth.py            # 认证相关
│   ├── notes.py           # 笔记相关
│   └── users.py           # 用户相关
├── scripts/                # 脚本文件
│   ├── init_db.py         # 数据库初始化
│   └── create_test_accounts.py  # 创建测试账号
├── tests/                  # 测试文件
│   ├── test_flask.py       # Flask 测试
│   └── test_minimal.py     # 最小测试
├── instance/               # 实例文件
│   └── gesp_study_plan.db  # SQLite 数据库
├── app.py                  # 应用主文件
├── extensions.py           # 扩展初始化
├── requirements.txt        # 依赖项
└── start_server.py         # 启动脚本
```

## 技术栈

### 前端
- HTML5/CSS3/JavaScript
- 原生 DOM 操作
- 前端存储：SessionStorage、IndexedDB
- 响应式设计

### 后端
- Python 3.14+
- Flask 框架
- SQLAlchemy ORM
- SQLite 数据库
- JWT 认证
- CORS 支持

## 编程规范与习惯

### 前端规范
1. **函数命名**：使用 `gesp_` 前缀，如 `gesp_updateProgress()`
2. **代码风格**：使用 4 空格缩进，遵循 ES6 语法
3. **文件组织**：按功能模块划分文件
4. **错误处理**：使用 try-catch 捕获异常
5. **性能优化**：使用事件委托，避免频繁 DOM 操作

### 后端规范
1. **代码风格**：遵循 PEP 8 规范
2. **文件组织**：按 MVC 模式组织代码
3. **数据库操作**：使用 SQLAlchemy ORM，避免原生 SQL
4. **API 设计**：RESTful API 风格，返回 JSON 格式
5. **认证**：使用 JWT 进行身份验证

## 核心功能

### 前端功能
1. **学习计划管理**：查看和更新学习进度
2. **在线编程**：在线编写和测试代码
3. **知识库**：查看学习资料和测试账号信息，根据项目内容实时更新
4. **进度跟踪**：记录学习进度和完成情况

### 后端功能
1. **用户认证**：登录、注册
2. **笔记管理**：创建、更新、删除笔记
3. **用户管理**：获取和更新用户信息
4. **文件上传**：支持图片上传功能

## 测试账号

### 学生账号
- 用户名：student
- 密码：student123

### 教师账号
- 用户名：teacher
- 密码：teacher123

### 管理员账号
- 用户名：demo
- 密码：123456

## 开发环境设置

1. **前端**：直接打开 HTML 文件即可
2. **后端**：
   - 安装依赖：`pip install -r requirements.txt`
   - 启动服务：`python start_server.py`
   - 访问地址：`http://localhost:5000`

## 常见问题

1. **数据库初始化**：运行 `python scripts/init_db.py`
2. **创建测试账号**：运行 `python scripts/create_test_accounts.py`
3. **API 文档**：查看 routes 目录下的文件

## 项目扩展

1. **添加新功能**：在 routes 目录下创建新的路由文件
2. **修改数据库模型**：编辑 models/models.py 文件
3. **添加前端页面**：在 frontend 目录下创建新的 HTML 文件

## 注意事项

1. **安全**：避免在前端存储敏感信息
2. **性能**：合理使用缓存和异步操作
3. **兼容性**：确保在主流浏览器中正常运行
4. **代码质量**：定期进行代码审查和测试
