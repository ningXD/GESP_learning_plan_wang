import requests
import json

# 测试Python代码执行
def test_python_execution():
    url = 'http://localhost:5000/api/compile'
    headers = {'Content-Type': 'application/json'}
    
    # 测试中文输出
    code = 'print("你好，Python！")'
    data = {
        'code': code,
        'language': 'python'
    }
    
    response = requests.post(url, headers=headers, json=data)
    print('Response status code:', response.status_code)
    print('Response content:', response.text)
    
    # 测试带输入的Python代码
    code_with_input = '''name = input("请输入你的名字：")
print("你好，" + name + "！")'''
    data_with_input = {
        'code': code_with_input,
        'input': '张三',
        'language': 'python'
    }
    
    response_with_input = requests.post(url, headers=headers, json=data_with_input)
    print('\nResponse with input status code:', response_with_input.status_code)
    print('Response with input content:', response_with_input.text)

if __name__ == '__main__':
    test_python_execution()
