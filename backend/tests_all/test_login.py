import requests

# 测试登录API
def test_login():
    url = 'http://127.0.0.1:5000/api/auth/login'
    
    # 测试demo账号
    print('=== 测试demo账号 ===')
    data = {
        'username': 'demo',
        'password': '123456'
    }
    
    response = requests.post(url, json=data)
    print(f"Status code: {response.status_code}")
    print(f"Response: {response.json()}")
    
    # 测试teacher_test账号
    print('\n=== 测试teacher_test账号 ===')
    data = {
        'username': 'teacher_test',
        'password': '123456'
    }
    
    response = requests.post(url, json=data)
    print(f"Status code: {response.status_code}")
    print(f"Response: {response.json()}")
    
    # 测试student_test账号
    print('\n=== 测试student_test账号 ===')
    data = {
        'username': 'student_test',
        'password': '123456'
    }
    
    response = requests.post(url, json=data)
    print(f"Status code: {response.status_code}")
    print(f"Response: {response.json()}")

if __name__ == "__main__":
    test_login()
