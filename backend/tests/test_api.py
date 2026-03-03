import requests

# 测试登录获取token
def test_login():
    url = 'http://localhost:5000/api/auth/login'
    data = {
        'username': 'demo',
        'password': '123456'
    }
    response = requests.post(url, json=data)
    print('Login response:', response.status_code)
    print('Login data:', response.json())
    return response.json().get('access_token')

# 测试获取学习计划
def test_get_study_plans(token):
    url = 'http://localhost:5000/api/study-plans'
    headers = {
        'Authorization': f'Bearer {token}'
    }
    response = requests.get(url, headers=headers)
    print('Study plans response:', response.status_code)
    print('Study plans data:', response.json())

# 测试获取学生列表
def test_get_students(token):
    url = 'http://localhost:5000/api/students'
    headers = {
        'Authorization': f'Bearer {token}'
    }
    response = requests.get(url, headers=headers)
    print('Students response:', response.status_code)
    print('Students data:', response.json())

if __name__ == '__main__':
    print('Testing API...')
    token = test_login()
    if token:
        test_get_study_plans(token)
        test_get_students(token)
