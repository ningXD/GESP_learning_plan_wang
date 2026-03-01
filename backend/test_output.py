import subprocess
import tempfile
import os

# 测试代码
code = '''#include <iostream>
using namespace std;

int main() {
    cout << "1到10的数字: " << endl;
    for (int i = 1; i <= 10; i++) {
        cout << i << " ";
    }
    cout << endl;
    return 0;
}
'''

# 创建临时文件
with tempfile.NamedTemporaryFile(suffix='.cpp', delete=False) as f:
    f.write(code.encode('utf-8'))
    cpp_file = f.name

try:
    # 编译代码
    exe_file = cpp_file.replace('.cpp', '.exe')
    compile_cmd = f'g++ "{cpp_file}" -o "{exe_file}"'
    
    compile_result = subprocess.run(
        compile_cmd,
        shell=True,
        capture_output=True,
        text=True,
        encoding='utf-8',
        errors='replace'
    )
    
    print(f"编译返回码: {compile_result.returncode}")
    print(f"编译错误: {compile_result.stderr}")
    
    if compile_result.returncode == 0:
        # 运行程序
        run_result = subprocess.run(
            f'"{exe_file}"',
            shell=True,
            capture_output=True,
            text=True,
            encoding='utf-8',
            errors='replace'
        )
        
        print(f"运行返回码: {run_result.returncode}")
        print(f"运行输出: {repr(run_result.stdout)}")
        print(f"运行错误: {run_result.stderr}")
        
finally:
    # 清理临时文件
    try:
        if os.path.exists(cpp_file):
            os.unlink(cpp_file)
        if os.path.exists(exe_file):
            os.unlink(exe_file)
    except:
        pass
