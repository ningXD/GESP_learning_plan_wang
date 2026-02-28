const express = require('express');
const fs = require('fs');
const path = require('path');
const { execSync } = require('child_process');
const cors = require('cors');

const app = express();
const port = 3000;

// 中间件
app.use(cors());
app.use(express.json({ limit: '5mb' }));

// 编译API
app.post('/api/compile', (req, res) => {
  const { code } = req.body;
  
  if (!code || typeof code !== 'string') {
    return res.status(400).json({
      success: false,
      data: null,
      error: { type: 'validation', message: 'Invalid code provided' }
    });
  }
  
  // 创建临时目录
  const tempDir = path.join(__dirname, 'temp');
  if (!fs.existsSync(tempDir)) {
    fs.mkdirSync(tempDir, { recursive: true });
  }
  
  // 生成唯一文件名
  const fileName = `temp_${Date.now()}.cpp`;
  const filePath = path.join(tempDir, fileName);
  const outputName = `output_${Date.now()}`;
  const outputPath = path.join(tempDir, outputName);
  
  try {
    // 写入临时文件
    fs.writeFileSync(filePath, code);
    
    // 使用Emscripten编译
    // 注意：这里假设Emscripten已经安装并添加到PATH
    const compileCommand = `emcc "${filePath}" -o "${outputPath}.js" -s WASM=1 -s NO_EXIT_RUNTIME=1 -s EXPORTED_FUNCTIONS=["_main"] -s EXPORTED_RUNTIME_METHODS=["ccall","cwrap"]`;
    execSync(compileCommand, { timeout: 30000 }); // 30秒超时
    
    // 读取编译结果
    const wasmPath = `${outputPath}.wasm`;
    const jsPath = `${outputPath}.js`;
    
    if (!fs.existsSync(wasmPath) || !fs.existsSync(jsPath)) {
      throw new Error('Compilation failed: Output files not generated');
    }
    
    const wasm = fs.readFileSync(wasmPath, 'base64');
    const js = fs.readFileSync(jsPath, 'base64');
    
    res.json({
      success: true,
      data: { wasm, js },
      error: null
    });
  } catch (error) {
    res.json({
      success: false,
      data: null,
      error: {
        type: 'compilation',
        message: error.message,
        stack: error.stack
      }
    });
  } finally {
    // 清理临时文件
    try {
      if (fs.existsSync(filePath)) fs.unlinkSync(filePath);
      if (fs.existsSync(`${outputPath}.js`)) fs.unlinkSync(`${outputPath}.js`);
      if (fs.existsSync(`${outputPath}.wasm`)) fs.unlinkSync(`${outputPath}.wasm`);
    } catch (cleanupError) {
      console.error('Cleanup error:', cleanupError);
    }
  }
});

// 健康检查
app.get('/api/health', (req, res) => {
  res.json({ status: 'ok', timestamp: new Date().toISOString() });
});

// 启动服务器
app.listen(port, () => {
  console.log(`Compiler service running on port ${port}`);
  console.log('Health check: http://localhost:3000/api/health');
  console.log('Compile endpoint: http://localhost:3000/api/compile');
});