import requests
import execjs
#pip install PyExecJS
import time
import random

timestamp = str(int(time.time()))
rad = str(random.randint(0, 100000000))[2:7]
nonce = ''.join(random.sample('abcdefghijklmnopqrstuvwxyz1234567890', 10))
headers = {
    'Host': 'tai.qq.com',
    'Connection': 'keep-alive',
    'sec-ch-ua': '" Not A;Brand";v="99", "Chromium";v="90", "Google Chrome";v="90"',
    'Accept': 'application/json, text/plain, */*',
    'taiserver': 'tai.qq.com',
    'sec-ch-ua-mobile': '?1',
    'User-Agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.93 Mobile Safari/537.36',
    'Content-Type': 'application/json',
    'Sec-Fetch-Site': 'same-origin',
    'Sec-Fetch-Mode': 'cors',
    'Sec-Fetch-Dest': 'empty',
    'Referer': 'https://tai.qq.com/epidemic/index.html?from=fzrb2',
    'Accept-Encoding': 'gzip, deflate, br',
    'Accept-Language': 'zh-CN,zh;q=0.9',
    'Cookie': 'RK=VR5MTSPvyN; ptcz=d622d4cdc8628d3d2c51f7bf22fea083609237969a5f49882dee0d7d3a9399cc; pgv_pvid=8867103644; o_cookie=2473295246; pac_uid=1_2473295246; logout_page=dm_loginpage; dm_login_weixin_scan='
}
params = {
    'destCity': '邢台市',
    'destCityCode': '130500',
    'fromCity': '北京市',
    'fromCityCode': '110000',
    'nonce': nonce,
    'seqId': timestamp + rad,
    'sessionID': 'UlW_b4v_Z_RFcvU9fVRWltaW',
    'timestamp': '1628054187168',
    'userId': 'h5',
    'version': '1.0'
}
param_str = ''
for k, v in params.items():
    param_str += (k + v)
with open('testspider.js', 'r', encoding='gbk') as f:
    decrypt_js = f.read()
ctx = execjs.compile(decrypt_js)
data = ctx.call('getSign', param_str)
print(data)
params['sign'] = data
url = ' http://tai.qq.com/api/marketing/covid/citypolicy'
res = requests.get(url, params=params,headers=headers)
print(res.json())
