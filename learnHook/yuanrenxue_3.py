import requests
import time
import execjs
import warnings
warnings.filterwarnings('ignore')

sum=0
for i in range(1,101):
    timestamp = str(int(time.time())) + '000'
    with open('yuanrenxue_3.js', 'r', encoding='gbk') as f:
        decrypt_js = f.read()
    ctx = execjs.compile(decrypt_js)
    cookie = ctx.call('getCookie', timestamp)
    cookie = {
        'm': cookie.split(';')[0].replace('m=', ''),
        'sessionid': 'lh1uzp6gfqpi0f9oft3rmrfhno76jfl8'
    }
    params={
        'page':i,
        'count':100
    }
    res=requests.post('https://www.python-spider.com/api/challenge3',cookies=cookie,verify=False,data=params).json()
    print(res)
    for value in res['data']:
       num=int(value['value'].replace('\r',''))
       sum=sum+num
    print('前'+str(i)+'页结果为：'+str(sum))
    time.sleep(1)
print(sum)