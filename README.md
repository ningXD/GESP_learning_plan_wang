# C++ 在线编程工具 - WebAssembly 方案

## 项目概述

本项目将基于JavaScript模拟执行的C++在线编程工具替换为基于WebAssembly的真实编译执行方案。

## 架构组成

### 1. 前端
- **文件**：`online_programming.html`
- **技术**：HTML5, CSS3, JavaScript, CodeMirror 5
- **功能**：代码编辑、编译请求、WebAssembly加载和执行

### 2. 后端
- **目录**：`compiler/`
- **技术**：Node.js, Express.js, Emscripten
- **功能**：C++代码编译为WebAssembly

## 快速开始

### 步骤1：安装依赖

1. 安装 Node.js：https://nodejs.org/
2. 安装 Emscripten SDK：https://emscripten.org/docs/getting_started/downloads.html
3. 进入编译服务目录并安装依赖：

```bash
cd compiler
npm install
```

### 步骤2：启动编译服务

```bash
npm start
```

编译服务将在 `http://localhost:3000` 启动。

### 步骤3：打开前端页面

在浏览器中打开 `online_programming.html` 文件。

### 步骤4：测试编译和执行

1. 在代码编辑器中编写C++代码
2. 点击"运行"按钮
3. 查看编译结果和执行输出

## 测试用例

### 1. 简单输出

```cpp
#include <iostream>
using namespace std;

int main() {
    cout << "Hello, GESP C++!" << endl;
    return 0;
}
```

### 2. 变量和表达式

```cpp
#include <iostream>
using namespace std;

int main() {
    int a = 10, b = 5;
    cout << "a = " << a << endl;
    cout << "b = " << b << endl;
    cout << "a + b = " << a + b << endl;
    return 0;
}
```

### 3. 循环

```cpp
#include <iostream>
using namespace std;

int main() {
    cout << "1到10的数字: " << endl;
    for (int i = 1; i <= 10; i++) {
        cout << i << " ";
    }
    cout << endl;
    return 0;
}
```

## 技术特点

### 优势
- **真实编译**：使用Emscripten进行真实的C++编译
- **完整支持**：支持几乎所有C++特性和标准库
- **性能提升**：WebAssembly执行速度接近原生
- **错误处理**：提供详细的编译错误信息

### 限制
- **环境依赖**：需要安装Emscripten SDK
- **编译时间**：编译过程可能比模拟执行慢
- **内存限制**：WebAssembly模块有内存限制
- **跨浏览器兼容性**：需要确保浏览器支持WebAssembly

## 故障排除

### 编译服务连接失败
- 确保编译服务正在运行：`npm start`
- 检查Emscripten是否正确安装：`emcc --version`
- 检查端口3000是否被占用

### 编译错误
- 检查C++代码语法是否正确
- 确保包含了必要的头文件
- 检查是否使用了Emscripten不支持的特性

### 执行错误
- 检查WebAssembly是否被浏览器支持
- 检查代码是否有运行时错误
- 检查内存使用是否超出限制

## 未来计划

1. **优化编译速度**：使用缓存和增量编译
2. **扩展标准库支持**：增加对更多STL容器和算法的支持
3. **添加调试功能**：支持断点和变量查看
4. **实现多文件编译**：支持多个源文件的编译
5. **添加项目管理**：支持保存和加载项目

## 联系方式

如有问题或建议，请联系项目维护者。