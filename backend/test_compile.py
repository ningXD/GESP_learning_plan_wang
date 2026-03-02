import requests
import json

# 测试C++编译API
code = '''#include <iostream>
using namespace std;
int main() {
    cout << "Hello, GESP C++!" << endl;
    return 0;
}'''

url = 'http://localhost:5000/api/compile'
headers = {'Content-Type': 'application/json'}
data = {'code': code}

response = requests.post(url, headers=headers, data=json.dumps(data))

print('Status Code:', response.status_code)
print('Response:', response.json())
