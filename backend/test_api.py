import requests
import json

# 测试C++编译API
code = '''#include <iostream>
using namespace std;

int main() {
    cout << "1到10的数字: " << endl;
    for (int i = 1; i <= 10; i++) {
        cout << i << " ";
    }
    cout << endl;
    return 0;
}'''

url = 'http://localhost:5000/api/compile'
headers = {'Content-Type': 'application/json'}
data = {'code': code}

response = requests.post(url, headers=headers, data=json.dumps(data))

print('Status Code:', response.status_code)
print('Response:', response.json())

# 检查输出是否完整
if response.status_code == 200:
    result = response.json()
    if result['success']:
        print('\nOutput:', repr(result['data']['output']))
        print('Error:', repr(result['data']['error']))
