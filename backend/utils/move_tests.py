import os
import shutil

# 获取当前目录
current_dir = os.path.dirname(os.path.abspath(__file__))
tests_all_dir = os.path.join(current_dir, 'tests_all')

# 确保tests_all目录存在
if not os.path.exists(tests_all_dir):
    os.makedirs(tests_all_dir)

# 移动所有test_开头的py文件
for file in os.listdir(current_dir):
    if file.startswith('test_') and file.endswith('.py'):
        src_path = os.path.join(current_dir, file)
        dst_path = os.path.join(tests_all_dir, file)
        print(f"移动 {file} 到 tests_all")
        shutil.move(src_path, dst_path)

print("移动完成！")
