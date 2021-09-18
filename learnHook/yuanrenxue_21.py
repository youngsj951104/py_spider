import requests
import execjs
import time
import warnings

warnings.filterwarnings('ignore')
sum = 0
for i in range(1, 101):
    timestamp = int(time.time() * 1000)
    with open('yuanrenxue_21.js', 'r', encoding='gbk') as f:
        decrypt_js = f.read()
    ctx = execjs.compile(decrypt_js)
    token = ctx.call('getToken', timestamp)
    print(token)
    cookies = {
        'sessionid': '75e2821quqlt12iywkermuop9s2dl8bq'
    }
    params = {
        'page': i,
        's': token,
        't': timestamp
    }
    print(params)
    res = requests.post('https://www.python-spider.com/api/challenge21', data=params, verify=False,
                        cookies=cookies).json()
    print(res)
    for value in res['data']:
        num = int(value['value'].replace('\r', ''))
        sum = sum + num
    print('前' + str(i) + '页结果为：' + str(sum))
    time.sleep(1)
print(sum)
