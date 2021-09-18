import requests
import time
import warnings
warnings.filterwarnings('ignore')
s=requests.session()
s.headers.clear()
headers={
'Host': 'www.python-spider.com',
'Content-Length': '6',
'Accept': 'application/json, text/javascript, */*; q=0.01',
'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.159 Safari/537.36',
'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
'Origin': 'https://www.python-spider.com',
'Referer': 'https://www.python-spider.com/challenge/10',
'Accept-Encoding': 'gzip, deflate, br',
'Accept-Language': 'zh-CN,zh;q=0.9',
'Cookie':'sessionid=j6dipzmsc37o2ppnsr5kibfuayp8yknu; Hm_lpvt_337e99a01a907a08d00bed4a1a52e35d=1629708312'
}
sum=0
for i in range(1,101):
    params={
        'page':i
    }
    res=s.post('https://www.python-spider.com/api/challenge10',data=params,headers=headers,verify=False).json()
    for value in res['data']:
       num=int(value['value'].replace('\r',''))
       sum=sum+num
    print(res)
    print('前'+str(i)+'页结果为：'+str(sum))
    time.sleep(1)
print(sum)