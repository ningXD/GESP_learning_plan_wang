import requests
import json

# 测试登录API
def test_login_detail():
    url = 'http://127.0.0.1:5000/api/auth/login'
    
    # 测试demo账号
    print('=== 测试demo账号 ===')
    data = {
        'username': 'demo',
        'password': '123456'
    }
    
    # 发送请求并打印详细信息
    print(f"请求URL: {url}")
    print(f"请求数据: {json.dumps(data, indent=2)}")
    
    response = requests.post(url, json=data)
    print(f"\n响应状态码: {response.status_code}")
    print(f"响应头: {dict(response.headers)}")
    print(f"响应内容: {response.json()}")

if __name__ == "__main__":
    test_login_detail()
