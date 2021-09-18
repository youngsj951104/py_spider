import requests
import execjs
import time
import warnings

warnings.filterwarnings('ignore')
sum = 0
for i in range(1, 101):
    timestamp = int(time.time() * 1000)
    with open('yuanrenxue_16.js', 'r', encoding='gbk') as f:
        decrypt_js = f.read()
    ctx = execjs.compile(decrypt_js)
    token = ctx.call('getToken', i)
    print(token)
    cookies = {
        'sessionid': '75e2821quqlt12iywkermuop9s2dl8bq'
    }
    params = {
        'page': i,
    }
    headers={
        'safe':token
    }
    res = requests.post('https://www.python-spider.com/api/challenge16', data=params, cookies=cookies, verify=False,headers=headers).json()
    for value in res['data']:
        num = int(value['value'].replace('\r', ''))
        sum = sum + num
    print('前' + str(i) + '页结果为：' + str(sum))
    time.sleep(1)
print(sum)