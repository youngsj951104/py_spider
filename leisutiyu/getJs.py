import requests
import re
result_path='js.js'
headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.93 Safari/537.36',
    }
res=requests.get('https://live.leisu.com/wanchang-20210702',headers=headers,verify=False).text
with open(result_path, "w", encoding='utf-8') as f:
    f.write(res)
    f.close()