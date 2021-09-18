import requests
from fontTools.ttLib import TTFont
from lxml import etree
import requests
from tempfile import TemporaryFile
from env import woff_string
from html import unescape
"""
    解密字体映射关系
    数字使用的是 d7321af4.woff 文件
    汉字使用的是 d944fb11.woff 文件
    :return: 加密字体映射表
"""
file_html='html.txt'
with open (file_html,'r',encoding='utf-8') as fp:
 result=fp.read()
font_num = TTFont('d7321af4.woff')
font_word = TTFont('d944fb11.woff')
font_num_keys = font_num.getGlyphOrder()
font_word_keys = font_word.getGlyphOrder()
texts = ['', ''] + [i for i in woff_string if i != '\n' and i != ' ']
font_num_dict = {}
font_word_dict = {}
for index, value in enumerate(texts):
        a = font_num_keys[index].replace('uni', '&#x').lower() + ';'
        b = font_word_keys[index].replace('uni', '&#x').lower() + ';'
        font_num_dict[a] = value
        font_word_dict[b] = value
for key in font_num_dict:
        if key in result:
                result = result.replace(f'<d class="num">{key}</d>', str(font_num_dict[key]))
for key in font_word_dict:
        if key in result:
                result = result.replace(f'<e class="address">{key}</e>', str(font_word_dict[key]))
result=etree.HTML(result)
selctor_name=result.xpath('//*[@id="basic-info"]/h1/text()')[0]
selctor_address=result.xpath('//*[@id="address"]/text()')[0]
selctor_tel=result.xpath('//*[@id="basic-info"]/p')[0]
result=etree.tostring(selctor_tel)
selctor_tel=unescape(str(result))
print(selctor_name,selctor_address,selctor_tel)
