# 竞赛特攻队项目概述

## 服务器启动指南

### 基本启动步骤

#### 启动后端服务器
1. 打开命令提示符或 PowerShell
2. 导航到项目根目录：
   ```powershell
   cd "d:\paitou\Trae\GESPC++_studyPlan"
   ```
3. 激活虚拟环境：
   ```powershell
   .venv\Scripts\Activate.ps1
   ```
4. 安装依赖（包括 pypinyin 库和 PostgreSQL 驱动）：
   ```powershell
   pip install -r backend\requirements.txt
   ```
5. 确保 PostgreSQL 数据库服务已启动
6. 初始化数据库（首次运行时）：
   ```powershell
   python backend\init_postgres_db.py
   ```
7. 运行以下命令启动服务器：
   ```powershell
   python backend\start_server.py
   ```
8. 服务器将在 `http://127.0.0.1:5000` 上运行

#### 访问前端页面
1. 打开浏览器
2. 导航到前端首页：
   ```
   d:\paitou\Trae\GESPC++_studyPlan\frontend\index.html
   ```
3. 使用以下演示账号登录：
   - 用户名：`demo`
   - 密码：`123456`

### 在后台运行服务器

#### 使用 PowerShell 在后台启动
1. 打开 PowerShell 窗口
2. 运行以下命令：
   ```powershell
   Start-Process python -ArgumentList "start_server.py" -WorkingDirectory "d:\paitou\Trae\GESPC++_studyPlan\backend" -NoNewWindow
   ```

#### 使用 cmd 命令在后台启动
1. 打开命令提示符
2. 运行以下命令：
   ```cmd
   cd /d "d:\paitou\Trae\GESPC++_studyPlan\backend"
   start /B python start_server.py
   ```

### 查看服务器状态

#### 查看 Python 进程
```powershell
Get-Process python
```

#### 查看端口占用
```powershell
netstat -ano | findstr :5000
```

### 停止服务器

#### 在当前窗口中停止
1. 确保运行服务器的 PowerShell 或命令提示符窗口是活动窗口
2. 按下 `Ctrl+C` 组合键
3. 服务器会停止运行并返回到命令提示符

#### 通过进程 ID 停止
1. 打开一个新的 PowerShell 窗口
2. 运行以下命令获取 Python 进程 ID：
   ```powershell
   Get-Process python
   ```
3. 找到与服务器相关的进程 ID
4. 运行以下命令停止进程：
   ```powershell
   Stop-Process -Id <进程ID>
   ```

#### 通过端口停止
1. 打开一个新的 PowerShell 窗口
2. 运行以下命令获取端口 5000 对应的进程 ID：
   ```powershell
   netstat -ano | findstr :5000
   ```
3. 运行以下命令停止进程：
   ```powershell
   taskkill /F /PID <进程ID>
   ```

### 数据库配置

#### PostgreSQL 配置（当前使用）
- 配置文件：`backend\config\.env`
- 配置项：
  ```
  DATABASE_URL=postgresql://gesp_user:123456@localhost/gesp_study_plan
  ```

#### SQLite 配置（备用）
- 配置文件：`backend\config\.env`
- 配置项：
  ```
  # DATABASE_URL=sqlite:///gesp_study_plan.db
  ```

#### MySQL 配置（备用）
- 配置文件：`backend\config\.env`
- 配置项：
  ```
  # DATABASE_URL=mysql+pymysql://root:password@localhost/gesp_study_plan
  ```

### 常见问题和解决方案

#### 服务器无法启动
- **原因**：可能是端口被占用或依赖项缺失
- **解决方案**：
  1. 检查端口 5000 是否被占用
  2. 确保已安装所有依赖项：
     ```powershell
     python -m pip install -r backend\requirements.txt
     ```

#### 数据库连接错误
- **原因**：可能是数据库配置错误或数据库未初始化
- **解决方案**：
  1. 检查 `backend\config\.env` 文件中的数据库配置
  2. 确保 PostgreSQL 数据库服务已启动
  3. 运行数据库初始化脚本：
     ```powershell
     python backend\init_postgres_db.py
     ```

#### 前端无法连接到后端
- **原因**：可能是后端服务器未运行或 CORS 配置错误
- **解决方案**：
  1. 确保后端服务器正在运行
  2. 检查浏览器控制台是否有 CORS 错误

#### 数据库迁移
- **原因**：当修改数据库模型时需要进行迁移
- **解决方案**：
  1. 生成迁移文件：
     ```powershell
     python -m alembic revision --autogenerate -m "迁移描述"
     ```
  2. 执行迁移：
     ```powershell
     python -m alembic upgrade head
     ```

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
│   ├── add_students_from_users.py  # 从users表添加学生到students表
│   ├── add_teachers_from_users.py  # 从users表添加教师到teachers表
│   ├── check_phone_format.py       # 检查手机号格式
│   ├── check_users.py              # 用户检查
│   ├── clear_teacher_subjects.py   # 清空教师科目
│   ├── create_test_accounts.py     # 创建测试账号
│   ├── generate_test_data.py       # 生成测试数据
│   ├── generate_valid_phones.py    # 生成有效手机号
│   └── init_study_plan.py          # 学习计划初始化
├── tests/
│   ├── test_api.py           # API测试
│   ├── test_compile.py       # 编译测试
│   ├── test_output.py        # 输出测试
│   └── test_python_api.py    # Python API测试
├── alembic.ini              # Alembic配置文件
├── app.py                   # 应用主文件
├── decorators.py            # 装饰器
├── extensions.py            # 扩展初始化
├── requirements.txt         # 依赖项
└── start_server.py          # 启动脚本
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