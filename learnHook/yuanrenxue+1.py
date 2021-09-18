import requests
import time
import base64
import hashlib
import json
# var a = '9622';
# var timestamp = String(Date.parse(new Date()) / 1000);
# var tokens = hex_md5(window.btoa(a + timestamp));
# request.setRequestHeader("safe", tokens);
# request.setRequestHeader("timestamp", timestamp)
def md5(str):

    md5 = hashlib.md5()
    md5.update(str)
    return md5.hexdigest()
count=0

for i in range(1,86):
    try:
        a = '9622'
        timestamp=str(int(time.time()))
        tokens=base64.b64encode((a+timestamp).encode())
        safe=md5(tokens)
        headers = {
            'Referer': 'https://www.python-spider.com/challenge/1',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.131 Safari/537.36',
            'safe': safe,
            'timestamp': timestamp,
            'sec-ch-ua': '"Chromium";v="92", " Not A;Brand";v="99", "Google Chrome";v="92"',
            'sec-ch-ua-mobile': '?0',
            'Sec-Fetch-Dest': 'empty',
            'Sec-Fetch-Mode': 'cors',
            'Sec-Fetch-Site': 'same-origin',
            'Cookie': '1; Hm_lvt_337e99a01a907a08d00bed4a1a52e35d=1629267823; vaptchaNetway=cn; no-alert=true; sessionid=u1tu7zt51r3i134fdn2qj6ktyg28x6vn; sign=1629267823~YWlkaW5nX3dpbjE2MjkyNzI5MjU0NDQ=|4bf87237ea2935810f4029cace8b9b00; Hm_lpvt_337e99a01a907a08d00bed4a1a52e35d=1629279330'
        }
        res = requests.get('https://www.python-spider.com/challenge/api/json?page='+str(i)+'&count=14', headers=headers,verify=False).json()
        info=res['infos']
        for value in info:
            if str.find(value['message'],'招')!=-1:
                print(value['message']+' 含有招字')
                count=count+1
            else:
                print(value['message'] + ' 不含有招字')
                continue
        time.sleep(1)
    except:
        continue
print(count)
exit('success')
