# -*- coding:UTF-8 -*-

import requests
from bs4 import BeautifulSoup
from docx import Document

def getHTMLText(url):
    kv = {'User-agent': 'Baiduspider'}
    try:
        r = requests.get(url, headers = kv, timeout = 30)
        r.raise_for_status()
        r.encoding = r.apparent_encoding
        return r.text
    except:
        return ''

def findPList(html):
    plist = []
    soup = BeautifulSoup(html, "html.parser")
    plist.append(soup.title.string)
    for div in soup.find_all('div', attrs={"class": "bd doc-reader"}):
        plist.extend(div.get_text().split('\n'))

    plist = [c.replace(' ', '') for c in plist]
    plist = [c.replace('\x0c', '') for c in plist]
    return plist



def toDOC(plist, path = 'baiduwenku1.txt'):
    file3 = open(path, 'wb')
    document = Document()
    for str in plist:
        document.add_paragraph(str)
        file3.write(str.encode('utf-8'))
        file3.write('\n'.encode('utf-8'))
    document.save('test' + ".docx")
    file3.close()

def main():

    url = 'https://wenku.baidu.com/view/3c5375f482eb6294dd88d0d233d4b14e85243e39.html?fr=search-1-wk_sea_es-incomeN#'
    html = getHTMLText(url)
    file1 = open('html.txt', 'wb')
    file1.write(html.encode('utf-8'))
    file1.write('\n'.encode('utf-8'))
    file1.close()
    plist = findPList(html)
    file2 = open('plist.txt', 'wb')
    file2.write(plist[0].encode('utf-8'))
    file2.write('\n'.encode('utf-8'))
    file2.close()
    toDOC(plist)

main()