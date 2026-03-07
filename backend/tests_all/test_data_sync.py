import requests

# 测试数据同步功能
def test_data_sync():
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
    
    # 测试添加学生并验证数据同步
    print('\n=== 测试添加学生并验证数据同步 ===')
    
    # 添加学生
    add_student_url = 'http://127.0.0.1:5000/api/students'
    student_data = {
        'name': '测试学生同步',
        'phone': '13800138003',
        'gender': '男',
        'age': 15,
        'grade': '高一',
        'project': 'C++编程'
    }
    
    headers = {'Authorization': f'Bearer {admin_token}'}
    response = requests.post(add_student_url, json=student_data, headers=headers)
    print(f"添加学生响应: {response.status_code} - {response.json()}")
    
    if response.status_code == 201:
        # 验证User表中是否创建了对应用户
        print('\n=== 验证User表数据 ===')
        users_url = 'http://127.0.0.1:5000/api/users/teachers'
        response = requests.get(users_url, headers=headers)
        users = response.json().get('data', [])
        student_user = next((u for u in users if u['phone'] == '13800138003'), None)
        if student_user:
            print(f"User表中找到学生: {student_user['username']} - {student_user['nickname']}")
        else:
            print("User表中未找到学生")
        
        # 验证Student表中是否创建了对应记录
        print('\n=== 验证Student表数据 ===')
        students_url = 'http://127.0.0.1:5000/api/students'
        response = requests.get(students_url, headers=headers)
        students = response.json().get('data', [])
        student_record = next((s for s in students if s['phone'] == '13800138003'), None)
        if student_record:
            print(f"Student表中找到学生: {student_record['name']} - {student_record['project']}")
        else:
            print("Student表中未找到学生")
    
    # 测试更新学生信息并验证数据同步
    print('\n=== 测试更新学生信息并验证数据同步 ===')
    
    # 获取学生列表找到刚才添加的学生
    students_url = 'http://127.0.0.1:5000/api/students'
    response = requests.get(students_url, headers=headers)
    students = response.json().get('data', [])
    student_to_update = next((s for s in students if s['phone'] == '13800138003'), None)
    
    if student_to_update:
        student_id = student_to_update['id']
        update_url = f'http://127.0.0.1:5000/api/students/{student_id}'
        update_data = {
            'name': '测试学生同步更新',
            'phone': '13800138004'
        }
        
        response = requests.put(update_url, json=update_data, headers=headers)
        print(f"更新学生响应: {response.status_code} - {response.json()}")
        
        if response.status_code == 200:
            # 验证更新后的数据
            print('\n=== 验证更新后的数据 ===')
            response = requests.get(students_url, headers=headers)
            students = response.json().get('data', [])
            updated_student = next((s for s in students if s['phone'] == '13800138004'), None)
            if updated_student:
                print(f"更新后Student表数据: {updated_student['name']} - {updated_student['phone']}")
            else:
                print("更新后Student表中未找到学生")
            
            # 验证User表数据是否同步更新
            users_url = 'http://127.0.0.1:5000/api/users/teachers'
            response = requests.get(users_url, headers=headers)
            users = response.json().get('data', [])
            updated_user = next((u for u in users if u['phone'] == '13800138004'), None)
            if updated_user:
                print(f"更新后User表数据: {updated_user['nickname']} - {updated_user['phone']}")
            else:
                print("更新后User表中未找到学生")

if __name__ == "__main__":
    test_data_sync()
