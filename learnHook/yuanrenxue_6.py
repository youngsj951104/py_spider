import requests
import time
import execjs
import warnings

warnings.filterwarnings('ignore')
session = requests.session()
params = {
    'page': 1
}
cookies = {
    'sessionid': 'lh1uzp6gfqpi0f9oft3rmrfhno76jfl8',
    'm': 'pua',
    'sign': '1629449079~YWlkaW5nX3dpbjM5LjE1NS4xODkuMT*'
}
sum=0
res = session.post('https://www.python-spider.com/api/challenge6', data=params, cookies=cookies,verify=False).json()
for value in res['data']:
       num=int(value['value'].replace('\r',''))
       sum=sum+num
print(sum)
for i in range(2,101):
    param2={
        'page':i,
    }
    res = session.post('https://www.python-spider.com/api/challenge6', data=param2,verify=False).json()
    print(session.cookies)
    for value in res['data']:
       num=int(value['value'].replace('\r',''))
       sum=sum+num
    print(res)
    print('前'+str(i)+'页结果为：'+str(sum))
    time.sleep(1)
print(sum)
