import requests

# 测试管理员权限
def test_admin_permissions():
    # 登录获取token
    login_url = 'http://127.0.0.1:5000/api/auth/login'
    
    # 管理员登录
    admin_data = {
        'username': 'demo',
        'password': '123456'
    }
    
    response = requests.post(login_url, json=admin_data)
    admin_token = response.json()['access_token']
    print('管理员登录成功')
    
    # 测试教师登录
    teacher_data = {
        'username': 'teacher_test',
        'password': '123456'
    }
    
    response = requests.post(login_url, json=teacher_data)
    teacher_token = response.json()['access_token']
    print('教师登录成功')
    
    # 测试学生登录
    student_data = {
        'username': 'student_test',
        'password': '123456'
    }
    
    response = requests.post(login_url, json=student_data)
    student_token = response.json()['access_token']
    print('学生登录成功')
    
    # 测试API权限
    test_apis = [
        {'name': '消课系统 - 课程记录', 'url': 'http://127.0.0.1:5000/api/course-records'},
        {'name': '消课系统 - 班级记录', 'url': 'http://127.0.0.1:5000/api/class-records'},
        {'name': '学生列表', 'url': 'http://127.0.0.1:5000/api/students'},
        {'name': '学习计划', 'url': 'http://127.0.0.1:5000/api/study-plans'}
    ]
    
    # 测试管理员权限
    print('\n=== 测试管理员权限 ===')
    headers = {'Authorization': f'Bearer {admin_token}'}
    for api in test_apis:
        response = requests.get(api['url'], headers=headers)
        print(f"{api['name']}: {response.status_code} - {response.json() if response.status_code == 200 else response.json().get('error', 'Unknown error')}")
    
    # 测试教师权限
    print('\n=== 测试教师权限 ===')
    headers = {'Authorization': f'Bearer {teacher_token}'}
    for api in test_apis:
        response = requests.get(api['url'], headers=headers)
        print(f"{api['name']}: {response.status_code} - {response.json() if response.status_code == 200 else response.json().get('error', 'Unknown error')}")
    
    # 测试学生权限
    print('\n=== 测试学生权限 ===')
    headers = {'Authorization': f'Bearer {student_token}'}
    for api in test_apis:
        response = requests.get(api['url'], headers=headers)
        print(f"{api['name']}: {response.status_code} - {response.json() if response.status_code == 200 else response.json().get('error', 'Unknown error')}")

if __name__ == "__main__":
    test_admin_permissions()
