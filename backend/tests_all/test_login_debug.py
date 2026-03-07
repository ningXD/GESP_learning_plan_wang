import requests
import json

# 测试登录API，打印详细信息
def test_login_debug():
    url = 'http://127.0.0.1:5000/api/auth/login'
    
    # 测试demo账号
    print('=== 测试demo账号 ===')
    data = {
        'username': 'demo',
        'password': '123456'
    }
    
    print(f"请求数据: {json.dumps(data, ensure_ascii=False)}")
    response = requests.post(url, json=data)
    print(f"状态码: {response.status_code}")
    print(f"响应头: {dict(response.headers)}")
    print(f"响应内容: {response.json()}")
    print()

if __name__ == "__main__":
    test_login_debug()
