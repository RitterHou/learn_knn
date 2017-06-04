import requests

from image.images import get_verification_value
from image.kNN import test_num
from image.kNN_symbol import test_symbol

cookie = 'isGuifan=1; PHPSESSID=jih9d458bj4h2767q38p3bdop2'

# 通过HTTP请求获取验证码信息
value = get_verification_value(cookie)

first = test_num(value[0])
second = test_num(value[1])

# 0为加；1为减；2为乘
symbol = test_symbol(value[2])

result = 0
if symbol == '0':
    result = int(first) + int(second)
elif symbol == '1':
    result = int(first) - int(second)
elif symbol == '1':
    result = int(first) * int(second)

print(first + second + symbol)
print(result)


url = 'https://www.woshidai.com/?app=sms&act=send'
headers = {
        'Cookie': cookie
    }
data = {
    'mobile': 15195935889,
    'vcode': result
}
r = requests.post(url, headers=headers, data=data)
print(r.content.decode('gbk'))

