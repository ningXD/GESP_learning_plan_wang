import requests

# 测试API端点是否存在，避免404错误
def test_api_endpoints():
    # 登录获取token
    login_url = 'http://127.0.0.1:5000/api/auth/login'
    admin_data = {
        'username': 'demo',
        'password': '123456'
    }
    
    response = requests.post(login_url, json=admin_data)
    admin_token = response.json()['access_token']
    print('管理员登录成功')
    
    # 测试API端点
    test_endpoints = [
        {'name': '登录API', 'url': 'http://127.0.0.1:5000/api/auth/login', 'method': 'POST', 'data': admin_data},
        {'name': '获取当前用户', 'url': 'http://127.0.0.1:5000/api/users/me', 'method': 'GET', 'headers': True},
        {'name': '获取教师列表', 'url': 'http://127.0.0.1:5000/api/users/teachers', 'method': 'GET', 'headers': True},
        {'name': '获取学生列表', 'url': 'http://127.0.0.1:5000/api/students', 'method': 'GET', 'headers': True},
        {'name': '获取班级记录', 'url': 'http://127.0.0.1:5000/api/class-records', 'method': 'GET', 'headers': True},
        {'name': '获取消课记录', 'url': 'http://127.0.0.1:5000/api/course-records', 'method': 'GET', 'headers': True},
        {'name': '获取学习计划', 'url': 'http://127.0.0.1:5000/api/study-plans', 'method': 'GET', 'headers': True},
        {'name': '前端首页', 'url': 'http://127.0.0.1:5000/index.html', 'method': 'GET'},
        {'name': '登录页面', 'url': 'http://127.0.0.1:5000/auth/login.html', 'method': 'GET'},
        {'name': '消课系统', 'url': 'http://127.0.0.1:5000/course/course_system.html', 'method': 'GET'},
        {'name': 'Wiki页面', 'url': 'http://127.0.0.1:5000/core/wiki.html', 'method': 'GET'},
        {'name': '学习计划', 'url': 'http://127.0.0.1:5000/core/study_plan.html', 'method': 'GET'},
        {'name': '在线编程', 'url': 'http://127.0.0.1:5000/programming/online_programming.html', 'method': 'GET'},
        {'name': '用户 profile', 'url': 'http://127.0.0.1:5000/user/profile.html', 'method': 'GET'}
    ]
    
    print('\n=== 测试API端点 ===')
    for endpoint in test_endpoints:
        headers = {'Authorization': f'Bearer {admin_token}'} if endpoint.get('headers') else {}
        data = endpoint.get('data', {})
        
        if endpoint['method'] == 'GET':
            response = requests.get(endpoint['url'], headers=headers)
        elif endpoint['method'] == 'POST':
            response = requests.post(endpoint['url'], json=data, headers=headers)
        
        status = '✓' if response.status_code < 400 else '✗'
        print(f"{status} {endpoint['name']}: {response.status_code} - {endpoint['url']}")
        if response.status_code >= 400:
            print(f"  错误信息: {response.json() if response.headers.get('Content-Type') == 'application/json' else response.text}")

if __name__ == "__main__":
    test_api_endpoints()
