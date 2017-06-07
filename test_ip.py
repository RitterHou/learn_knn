import requests

url = 'http://ip.chinaz.com/'

proxies = {
  "http": "http://127.0.0.1:10800",
  "https": "http://127.0.0.1:10800",
}

r = requests.get(url, proxies=proxies)
print(r.content.decode('utf-8'))
