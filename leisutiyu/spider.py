import base64
import zlib
from time import sleep
from urllib import parse
import re
import requests


# 获取加密字符串所在的js文件名
def getJs(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.93 Safari/537.36',
    }
    res = requests.get(url, headers=headers, verify=False).text
    reg = re.search('(https://static.leisu.com/public/askaliy/askftb/wc-[^.]*.js)', res).group(1)
    print('查询js网址为：' + reg)
    return reg


# 请求js文件获取对应的加密字段
def getBase64(url):
    headers = {
        'authority': 'static.leisu.com',
        'method': 'GET',
        'path': '/public/askaliy/askftb/wc-30c217c8d84f.js',
        'scheme': 'https',
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'accept-encoding': 'gzip, deflate, br',
        'accept-language': 'zh-CN,zh;q=0.9,en;q=0.8',
        'cache-control': 'no-cache',
        # 'cookie': 'UM_distinctid=17af1b850cd442-0f4909c048f583-404e0f2f-15f900-17af1b850ce431; Hm_lvt_63b82ac6d9948bad5e14b1398610939a=1627553026',
        'pragma': 'no-cache',
        'sec-ch-ua': '" Not A;Brand";v="99", "Chromium";v="90", "Google Chrome";v="90"',
        'sec-ch-ua-mobile': '?0',
        'sec-fetch-dest': 'document',
        'sec-fetch-mode': 'navigate',
        'sec-fetch-site': 'none',
        'sec-fetch-user': '?1',
        'upgrade-insecure-requests': '1',
        'user-agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36',
    }
    result_path = 'ceshi.js'
    print("目标js网址：" + url)
    res = requests.get(url, headers=headers, verify=False).text
    with open(result_path, "w", encoding='utf-8') as f:
        f.write(res)
        f.close()
    reg = re.search("window[^=]* ='([^']*)'", res).group(1)
    return reg


def roott(t, e):
    i = ""
    for n in t:
        a = ord(n)
        o = a
        if 65 <= a <= 90:
            o = (a - 65 - 1 * e + 26) % 26 + 65
        if 97 <= a <= 122:
            o = (a - 97 - 1 * e + 26) % 26 + 97
        i += chr(o)
    return i


def pushmsg(t):
    # 对应atob
    r = base64.b64decode(t.encode())
    # 解压
    b = zlib.decompress(r)
    p = parse.unquote(b.decode())
    return p.replace('%', '\\').encode().decode('unicode-escape')


def rot(t, e):
    i = roott(t, e)
    return pushmsg(i)


if __name__ == '__main__':
    for i in range(1, 32):
        if i < 10:
            time = '2021010' + str(i)
        else:
            time = '202101' + str(i)
        result_path = 'res-' + time + '.json'
        url = 'https://live.leisu.com/wanchang-' + time
        js_url = getJs(url)
        base64_ = getBase64(js_url)
        print("对应的加密字段：" + base64_)
        e = 13
        res = rot(base64_, e)
        with open(result_path, "w", encoding='utf-8') as f:
            f.write(res)
            f.close()
        sleep(1)
