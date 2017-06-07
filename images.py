from time import time

import requests
from PIL import Image

proxies = {
    "http": "http://127.0.0.1:10800",
    "https": "http://127.0.0.1:10800",
}


def get_verification_value(cookie='isGuifan=1; PHPSESSID=amb85h83ut86smj5gmrge3moh3'):
    image_url = 'https://www.woshidai.com/?plugins&q=imgcode?nocache=' + str(int(time() * 1000))

    headers = {
        'Cookie': cookie
    }

    r = requests.get(image_url, headers=headers, proxies=proxies, stream=True)
    if r.status_code == 200:
        r.raw.decode_content = True
        bw = Image.open(r.raw).convert('L').point(lambda x: 0 if x < 128 else 255, '1')

        first = bw.crop((4, 3, 14, 15))
        second = bw.crop((24, 3, 34, 15))
        symbol = bw.crop((14, 5, 24, 14))
        return first, second, symbol


if __name__ == '__main__':
    value = get_verification_value()

    from image.kNN import test_num

    print(test_num(value[0]))
    print(test_num(value[1]))
    value[0].save('first.png')
    value[1].save('second.png')
    from image.kNN_symbol import test_symbol

    # 0为加；1为减；2为乘
    print(test_symbol(value[2]))
    value[2].save('symbol.png')
