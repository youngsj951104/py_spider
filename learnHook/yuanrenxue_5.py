import requests
import execjs
import warnings
warnings.filterwarnings('ignore')
with open('5.js', 'r', encoding='utf-8') as f:
    decrypt_js = f.read()
ctx = execjs.compile(decrypt_js)
url1 = ctx.call('_yrxyA$', '/cityjson')
cookies={
    'sessionid':'pqlba4yf2l760fwkfzp7z9mks3eh2p3s'
}
s=requests.session()
try1=s.post(url1,cookies=cookies,verify=False)
with open('yuanrenxue_5.js', 'r', encoding='utf-8') as f:
    decrypt_js_1 = f.read()
ctx = execjs.compile(decrypt_js_1)
url = ctx.call('_yrxyA$', '/api/challenge5')
url=url.replace('undefined','').replace('qqqqqqqqqqqqqqqqqqqqql','')
params={
    'page':3
}
print(url)
res=s.post(url,cookies=cookies,data=params,verify=False).text
print(res)