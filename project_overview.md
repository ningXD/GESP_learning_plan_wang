# 竞赛特攻队项目概述

## 项目简介
这是一个面向 GESPC++ 竞赛的学习计划平台，包含前端和后端两部分，提供学习计划管理、在线编程、消课系统等功能。

## 项目结构

### 前端结构
```
frontend/
├── auth/
│   └── login.html          # 登录页面
├── core/
│   ├── study_plan.html     # 学习计划页面
│   └── wiki.html           # 知识库页面
├── course/
│   └── course_system.html  # 消课系统页面
├── materials/
│   └── real_test_question_materials/  # 真题材料
├── programming/
│   └── online_programming.html  # 在线编程界面
├── tests/
│   ├── code_examples.html        # 代码示例
│   └── test_python_input.html    # Python输入测试
├── user/
│   └── profile.html        # 用户个人资料页面
└── index.html              # 首页
```

### 后端结构
```
backend/
├── config/
│   └── .env               # 环境变量配置
├── migrations/            # Alembic数据库迁移文件
│   ├── versions/          # 迁移版本
│   ├── env.py             # 迁移环境配置
│   └── script.py.mako     # 迁移脚本模板
├── models/
│   ├── __init__.py
│   └── models.py          # 数据库模型定义
├── routes/
│   ├── __init__.py
│   ├── auth.py            # 认证相关API
│   ├── compile.py         # C++代码编译和运行
│   ├── course.py          # 消课系统API
│   ├── notes.py           # 笔记相关API
│   ├── study_plan.py      # 学习计划API
│   └── users.py           # 用户相关API
├── scripts/
│   ├── add_student_users.py      # 添加学生用户
│   ├── check_db.py               # 数据库检查
│   ├── check_users.py            # 用户检查
│   ├── create_test_accounts.py   # 创建测试账号
│   ├── generate_phone_numbers.py # 生成电话号码
│   ├── generate_test_data.py     # 生成测试数据
│   ├── init_db.py                # 数据库初始化
│   ├── init_study_plan.py        # 学习计划初始化
│   ├── sync_user_tables.py       # 同步用户表
│   └── update_db_schema.py       # 更新数据库 schema
├── tests/
│   ├── test_api.py           # API测试
│   ├── test_compile.py       # 编译测试
│   ├── test_output.py        # 输出测试
│   └── test_python_api.py    # Python API测试
├── alembic.ini              # Alembic配置文件
├── app.py                   # 应用主文件
├── check_db_tables.py       # 数据库表检查脚本
├── check_routes.py          # 路由检查脚本
├── decorators.py            # 装饰器
├── extensions.py            # 扩展初始化
├── init_postgres_db.py      # PostgreSQL数据库初始化
├── requirements.txt         # 依赖项
├── start_server.py          # 启动脚本
└── test_db_connection.py    # 数据库连接测试
```

## 技术栈

### 前端
- HTML5/CSS3/JavaScript
- 原生 DOM 操作
- 前端存储：SessionStorage
- 响应式设计

### 后端
- Python 3.14+
- Flask 框架
- SQLAlchemy ORM
- PostgreSQL 数据库
- JWT 认证
- CORS 支持
- C++编译支持（g++编译器）
- 子进程管理（subprocess模块）
- Alembic 数据库迁移工具
- pypinyin 中文拼音排序

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
2. **在线编程**：在线编写和测试C++代码，支持真实编译和运行
3. **知识库**：查看学习资料和测试账号信息，根据项目内容实时更新
4. **消课系统**：管理学生信息、教师信息，支持搜索、排序和分页
5. **用户管理**：个人资料查看和编辑

### 后端功能
1. **用户认证**：登录、注册、退出
2. **笔记管理**：创建、更新、删除笔记
3. **用户管理**：获取和更新用户信息
4. **C++代码编译**：真实编译和运行C++代码，支持错误捕获和超时处理
5. **消课系统**：学生和教师管理，包含新增字段（剩余课时数、剩余学费、入学时间）
6. **学习计划**：学习计划的创建和管理

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
   - 配置数据库：确保 PostgreSQL 数据库运行，在 `config/.env` 中设置数据库连接信息
   - 初始化数据库：`python init_postgres_db.py`
   - 启动服务：`python start_server.py`
   - 访问地址：`http://localhost:5000`

## 常见问题

1. **数据库初始化**：运行 `python init_postgres_db.py`
2. **创建测试账号**：运行 `python scripts/create_test_accounts.py`
3. **API 文档**：查看 routes 目录下的文件
4. **C++编译功能**：确保系统安装了 g++ 编译器，否则编译功能将不可用
5. **编译超时**：系统设置了 10 秒编译超时和 5 秒运行超时，超时的代码会被自动终止
6. **错误处理**：编译错误会在前端显示，帮助用户调试代码
7. **数据库迁移**：使用 Alembic 进行数据库结构变更

## 项目扩展

1. **添加新功能**：在 routes 目录下创建新的路由文件
2. **修改数据库模型**：编辑 models/models.py 文件，然后使用 Alembic 生成迁移
3. **添加前端页面**：在 frontend 目录下创建新的 HTML 文件

## 注意事项

1. **安全**：避免在前端存储敏感信息
2. **性能**：合理使用缓存和异步操作
3. **兼容性**：确保在主流浏览器中正常运行
4. **代码质量**：定期进行代码审查和测试
5. **数据库**：使用 PostgreSQL 数据库，确保数据库服务正常运行