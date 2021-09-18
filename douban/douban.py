import requests
import execjs  # 这个库是PyExecJS
import re

response = requests.get('https://search.douban.com/book/subject_search?search_text=%E5%B2%9B%E7%94%B0&cat=1001')
r = re.search('window.__DATA__ = "([^"]+)"', response.text).group(1)  # 加密的数据
# 导入js
with open('main.js', 'r', encoding='gbk') as f:
    decrypt_js = f.read()
ctx = execjs.compile(decrypt_js)
data = ctx.call('decrypt', r)
for item in data['payload']['items']:
    print(item)
