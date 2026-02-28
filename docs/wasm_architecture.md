# WebAssembly 编译和执行架构设计

## 1. 架构概述

本架构设计旨在将当前基于JavaScript模拟执行的C++在线编程工具替换为基于WebAssembly的真实编译执行方案。

### 1.1 核心组件

| 组件 | 描述 | 技术栈 |
|------|------|--------|
| 前端编辑器 | 代码编辑和用户界面 | CodeMirror 5, HTML5, CSS3, JavaScript |
| 编译服务 | C++到WebAssembly的编译 | Emscripten, Node.js |
| 通信层 | 前后端数据传输 | HTTP API, JSON |
| 执行环境 | WebAssembly模块加载和执行 | WebAssembly JavaScript API |
| 输出捕获 | 捕获和显示程序输出 | 自定义stdout/stderr重定向 |

## 2. 详细设计

### 2.1 前端架构

#### 2.1.1 现有组件
- **CodeMirror编辑器**：保持不变，负责代码编辑
- **UI界面**：保持不变，提供运行、清空等按钮

#### 2.1.2 新增组件
- **编译请求模块**：将代码发送到后端编译服务
- **WebAssembly加载器**：加载和实例化编译后的WASM模块
- **执行控制器**：管理WASM模块的执行生命周期
- **输出捕获器**：捕获和显示程序输出

### 2.2 后端架构

#### 2.2.1 编译服务
- **代码接收**：接收前端发送的C++代码
- **编译处理**：使用Emscripten编译C++到WebAssembly
- **错误处理**：捕获和格式化编译错误
- **结果返回**：返回编译后的WASM模块或错误信息

#### 2.2.2 技术选型
- **运行环境**：Node.js
- **编译工具**：Emscripten SDK
- **API框架**：Express.js
- **文件管理**：临时文件存储和清理

### 2.3 通信协议

#### 2.3.1 请求格式
```json
{
  "code": "#include <iostream>\nusing namespace std;\nint main() { cout << \"Hello\" << endl; return 0; }",
  "options": {
    "optimization": "O2",
    "features": ["exception", "rtti"]
  }
}
```

#### 2.3.2 响应格式
```json
{
  "success": true,
  "data": {
    "wasm": "base64-encoded wasm module",
    "js": "base64-encoded javascript wrapper"
  },
  "error": null
}
```

```json
{
  "success": false,
  "data": null,
  "error": {
    "type": "compilation",
    "message": "error: 'cout' was not declared in this scope",
    "line": 3,
    "column": 5
  }
}
```

### 2.4 执行流程

1. **用户编写代码**：在CodeMirror编辑器中编写C++代码
2. **点击运行按钮**：触发编译请求
3. **发送代码到后端**：前端将代码通过HTTP POST发送到编译服务
4. **后端编译**：Emscripten将C++编译为WebAssembly
5. **返回编译结果**：后端返回编译后的WASM模块或错误信息
6. **前端处理**：
   - 如有错误，显示编译错误
   - 如成功，加载和实例化WASM模块
7. **执行程序**：运行WASM模块，捕获输出
8. **显示结果**：在输出区域显示程序输出

## 3. 技术实现细节

### 3.1 前端实现

#### 3.1.1 编译请求
```javascript
async function compileCode(code) {
  const response = await fetch('/api/compile', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json'
    },
    body: JSON.stringify({ code })
  });
  return await response.json();
}
```

#### 3.1.2 WebAssembly加载
```javascript
async function loadWasm(wasmData, jsData) {
  // 解码base64数据
  const wasmBuffer = Uint8Array.from(atob(wasmData), c => c.charCodeAt(0));
  const jsCode = atob(jsData);
  
  // 创建WASM模块
  const module = await WebAssembly.compile(wasmBuffer);
  
  // 创建执行环境
  const importObject = {
    env: {
      memory: new WebAssembly.Memory({ initial: 1024 }),
      table: new WebAssembly.Table({ initial: 10, element: 'anyfunc' }),
      __wasi_unstable_preopens_get: () => 0,
      __wasi_unstable_fd_close: () => 0,
      __wasi_unstable_fd_write: (fd, iovs, iovs_len, nwritten) => {
        // 处理输出
        return 0;
      }
    }
  };
  
  // 实例化模块
  const instance = await WebAssembly.instantiate(module, importObject);
  return instance;
}
```

### 3.2 后端实现

#### 3.2.1 编译服务
```javascript
const express = require('express');
const fs = require('fs');
const { execSync } = require('child_process');
const app = express();

app.use(express.json());

app.post('/api/compile', (req, res) => {
  const { code } = req.body;
  
  // 写入临时文件
  fs.writeFileSync('temp.cpp', code);
  
  try {
    // 使用Emscripten编译
    execSync('emcc temp.cpp -o output.js -s WASM=1 -s NO_EXIT_RUNTIME=1 -s EXPORTED_FUNCTIONS=["_main"]');
    
    // 读取编译结果
    const wasm = fs.readFileSync('output.wasm', 'base64');
    const js = fs.readFileSync('output.js', 'base64');
    
    res.json({ success: true, data: { wasm, js }, error: null });
  } catch (error) {
    res.json({ success: false, data: null, error: { type: 'compilation', message: error.message } });
  } finally {
    // 清理临时文件
    fs.unlinkSync('temp.cpp');
    if (fs.existsSync('output.js')) fs.unlinkSync('output.js');
    if (fs.existsSync('output.wasm')) fs.unlinkSync('output.wasm');
  }
});

app.listen(3000, () => console.log('Compiler service running on port 3000'));
```

## 4. 优势与挑战

### 4.1 优势
- **真实编译**：使用Emscripten进行真实的C++编译
- **完整支持**：支持几乎所有C++特性和标准库
- **性能提升**：WebAssembly执行速度接近原生
- **错误处理**：提供详细的编译错误信息

### 4.2 挑战
- **环境依赖**：需要安装Emscripten SDK
- **编译时间**：编译过程可能比模拟执行慢
- **内存限制**：WebAssembly模块有内存限制
- **跨浏览器兼容性**：需要确保浏览器支持WebAssembly

## 5. 实施计划

1. **搭建后端编译服务**：安装Emscripten，创建编译API
2. **修改前端代码**：添加编译请求和WASM加载逻辑
3. **实现输出捕获**：重定向stdout/stderr到前端
4. **测试与优化**：测试各种C++代码，优化性能和用户体验
5. **部署与集成**：将服务部署到生产环境

## 6. 结论

WebAssembly方案相比当前的模拟执行方案，提供了更真实、更完整的C++编译执行环境，能够支持更复杂的C++代码和特性。虽然实施过程中存在一些挑战，但这些挑战都可以通过合理的设计和优化来克服。

通过本架构设计，C++在线编程工具将能够提供接近本地IDE的编译执行体验，为用户提供更准确、更全面的C++编程环境。