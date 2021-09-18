import requests
import execjs
import re
import time
from lxml import etree

cookies={
    'sessionid':'oebz5aedhq2jcklbs98og5ktfmvwkx3e'
}
res= requests.get('https://www.python-spider.com/challenge/11',cookies=cookies,verify=False).text
reg=re.search(',\'([0-9a-zA-Z]{32})\',',res).group(1)
timestamp=str(round(time.time(),3))
with open('yuanrenxue_11.js', 'r', encoding='gbk') as f:
    decrypt_js = f.read()
ctx = execjs.compile(decrypt_js)
cookie = ctx.call('getCookie', reg)
cookie=timestamp+'|0|'+cookie
cookies={
    'sessionid':'oebz5aedhq2jcklbs98og5ktfmvwkx3e',
    '__jsl_clearance':cookie
}
res= requests.get('https://www.python-spider.com/challenge/11',cookies=cookies,verify=False).text
print(res)
res=etree.HTML(res)
num=res.xpath("//td[@class=\"info\"]/text()")
sum=0
for value in num:
    num_str=int(value.replace('\n','').replace('\t',''))
    sum=sum+num_str
print(sum)