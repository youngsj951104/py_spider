import requests
import execjs

headers = {
    'authority': 'thor.weidian.com',
    'sec-ch-ua': '"Google Chrome";v="93", " Not;A Brand";v="99", "Chromium";v="93"',
    'accept': 'application/json, */*',
    'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
    'sec-ch-ua-mobile': '?0',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.63 Safari/537.36',
    'sec-ch-ua-platform': '"Windows"',
    'origin': 'https://d.weidian.com',
    'sec-fetch-site': 'same-site',
    'sec-fetch-mode': 'cors',
    'sec-fetch-dest': 'empty',
    'referer': 'https://d.weidian.com/',
    'accept-language': 'zh-CN,zh;q=0.9',
    'cookie': '__spider__visitorid=e37638bc373b0383; wdtoken=5e2a587e; __spider__sessionid=efb3dc164ccf2d98',
}
ua=''
with open('weidian.js', 'r', encoding='utf-8') as f:
    decrypt_js = f.read()
ctx = execjs.compile(decrypt_js)
# ua=ctx.call('getToken')
data = {
  'param': '{"phone":"18852549878","countryCode":86,"vcode":"584680","ua":"{'+ua+'}"}',
  'wdtoken': '5e2a587e'
}

response = requests.post('https://thor.weidian.com/passport/login.vcode/1.0', headers=headers, data=data,verify=False)
print(response.text)
