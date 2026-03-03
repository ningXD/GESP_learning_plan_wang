from flask import Blueprint, request, jsonify
import subprocess
import os
import tempfile
import base64

# 创建蓝图
bp = Blueprint('compile', __name__, url_prefix='/api')

@bp.route('/compile', methods=['POST'])
def compile_code():
    """编译代码并返回执行结果，支持C++和Python"""
    try:
        # 获取代码、输入和语言
        data = request.get_json()
        code = data.get('code', '')
        input_data = data.get('input', '')
        language = data.get('language', 'cpp')  # 默认C++
        
        if not code:
            return jsonify({"success": False, "error": {"message": "No code provided"}}), 400
        
        if language == 'python':
            # 处理Python代码
            with tempfile.NamedTemporaryFile(suffix='.py', delete=False) as f:
                f.write(code.encode('utf-8'))
                py_file = f.name
            
            try:
                # 直接运行Python代码
                run_result = subprocess.run(
                    f'python "{py_file}"',
                    shell=True,
                    capture_output=True,
                    text=True,
                    encoding='utf-8',
                    errors='replace',
                    input=input_data,
                    timeout=10,  # 10秒运行超时
                    env={**os.environ, 'PYTHONIOENCODING': 'utf-8'}
                )
                
                # 构建响应
                response = {
                    "success": True,
                    "data": {
                        "output": run_result.stdout,
                        "error": run_result.stderr
                    }
                }
                
            finally:
                # 清理临时文件
                try:
                    if os.path.exists(py_file):
                        os.unlink(py_file)
                except:
                    pass
        else:
            # 处理C++代码
            with tempfile.NamedTemporaryFile(suffix='.cpp', delete=False) as f:
                f.write(code.encode('utf-8'))
                cpp_file = f.name
            
            # 编译代码
            exe_file = cpp_file.replace('.cpp', '.exe')
            compile_cmd = f'g++ "{cpp_file}" -o "{exe_file}"'
            
            try:
                # 执行编译
                compile_result = subprocess.run(
                    compile_cmd,
                    shell=True,
                    capture_output=True,
                    text=True,
                    encoding='utf-8',
                    errors='replace',
                    timeout=10  # 10秒超时
                )
                
                if compile_result.returncode != 0:
                    # 编译失败
                    return jsonify({
                        "success": False,
                        "error": {
                            "type": "compile",
                            "message": compile_result.stderr
                        }
                    })
                
                # 运行编译后的程序
                run_result = subprocess.run(
                    f'"{exe_file}"',
                    shell=True,
                    capture_output=True,
                    text=True,
                    encoding='utf-8',
                    errors='replace',
                    input=input_data,
                    timeout=5  # 5秒运行超时
                )
                
                # 构建响应
                response = {
                    "success": True,
                    "data": {
                        "output": run_result.stdout,
                        "error": run_result.stderr
                    }
                }
                
            finally:
                # 清理临时文件
                try:
                    if os.path.exists(cpp_file):
                        os.unlink(cpp_file)
                    if os.path.exists(exe_file):
                        os.unlink(exe_file)
                except:
                    pass
        
        return jsonify(response)
        
    except subprocess.TimeoutExpired:
        return jsonify({
            "success": False,
            "error": {
                "type": "timeout",
                "message": "Execution timed out"
            }
        })
    except Exception as e:
        return jsonify({
            "success": False,
            "error": {
                "type": "system",
                "message": str(e)
            }
        })
