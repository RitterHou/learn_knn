from time import time

import requests
from PIL import Image


def get_verification_value():
    image_url = 'https://www.woshidai.com/?plugins&q=imgcode?nocache=' + str(int(time() * 1000))

    headers = {
        'Cookie': 'isGuifan=1; PHPSESSID=amb85h83ut86smj5gmrge3moh3'
    }

    r = requests.get(image_url, headers=headers, stream=True)
    if r.status_code == 200:
        r.raw.decode_content = True
        bw = Image.open(r.raw).convert('L').point(lambda x: 0 if x < 128 else 255, '1')

        first = bw.crop((4, 3, 14, 15))
        second = bw.crop((24, 3, 34, 15))
        symbol = bw.crop((14, 5, 24, 14))
        return first, second, symbol


if __name__ == '__main__':
    i = 0
    while True:
        value = get_verification_value()
        value[0].save('num/' + str(i * 2) + '.png')
        value[1].save('num/' + str(i * 2 + 1) + '.png')
        value[2].save('symbol/' + str(i) + '.png')
        i += 1
        print(i)
