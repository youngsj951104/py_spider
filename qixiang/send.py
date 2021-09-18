import warnings
import execjs
warnings.filterwarnings('ignore')
import requests
requests.packages.urllib3.util.ssl_.DEFAULT_CIPHERS='ALL'
cookies = {
    'UM_distinctid': '17bc3d61e50316-0fac7b4c1aacff-c343365-1fa400-17bc3d61e51d09',
    'CNZZDATA5808503': 'cnzz_eid%3D1918087794-1631073458-%26ntime%3D1631073458',
}

headers = {
    'Connection': 'keep-alive',
    'sec-ch-ua': '"Chromium";v="92", " Not A;Brand";v="99", "Google Chrome";v="92"',
    'Accept': '*/*',
    'X-Requested-With': 'XMLHttpRequest',
    'sec-ch-ua-mobile': '?0',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.159 Safari/537.36',
    'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
    'Origin': 'https://www.aqistudy.cn',
    'Sec-Fetch-Site': 'same-origin',
    'Sec-Fetch-Mode': 'cors',
    'Sec-Fetch-Dest': 'empty',
    'Referer': 'https://www.aqistudy.cn/html/city_realtime.php?v=2.3',
    'Accept-Language': 'zh-CN,zh;q=0.9',
}


with open('test.js', 'r', encoding='utf-8') as f:
    decrypt_js = f.read()
ctx = execjs.compile(decrypt_js)
token = ctx.call('getToken')
data = {
  'hv8mn6PbI': token
}

print(data)
response = requests.post('https://www.aqistudy.cn/apinew/aqistudyapi.php', headers=headers,verify=False, cookies=cookies, data=data)
print(response.text)