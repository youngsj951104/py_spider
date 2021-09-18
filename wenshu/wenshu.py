import requests
# from fun import *
import json
import base64
import math
import json
import time
import random
from Crypto.Cipher import DES3
from Crypto.Util.Padding import pad, unpad
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

##以下实现方式通过selenium模拟web浏览器登陆中国文书网后获取登陆cookie，将cookie作为登陆凭证传给页面进行爬取
##本来尝试逆向获取文书网密码字段加密流程直接获取cookie登陆凭证，但是在尝试中发现登陆接口返回内容，并没有可以作为登陆凭证的内容，并且登陆接口getcookie获得的参数也不是作为登陆凭证的真实cookie
##所以采用selenium作为取巧的方法
##这个实例仅能做到简单的爬取文书接口后伪造请求参数获取加密内容并进行解密，考虑到selenium的效率和性能问题不能尝试大量爬虫
##并且页面在请求次数过多的情况下可能会被ip封禁，原理未知。

def des3encrypt(plain_text: str, key: str, iv: str) -> str:
    des3 = DES3.new(key=key.encode(), mode=DES3.MODE_CBC, iv=iv.encode())
    encrypted_data = des3.encrypt(pad(plain_text.encode(), DES3.block_size))
    cipher_text = base64.b64encode(encrypted_data).decode()
    return cipher_text


def des3decrypt(cipher_text: str, key: str, iv: str) -> str:
    des3 = DES3.new(key=key.encode(), mode=DES3.MODE_CBC, iv=iv.encode())
    decrypted_data = des3.decrypt(base64.b64decode(cipher_text))
    plain_text = unpad(decrypted_data, DES3.block_size).decode()
    return plain_text


def get_pageid():
    guid = ""
    for i in range(1, 33):
        n = hex(math.floor(random.random() * 16))[-1]
        guid += n
    return guid


def get_token(size=24):
    arr = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', 'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j',
           'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E',
           'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
    token_str = ""
    for i in range(size):
        token_str += arr[round(random.random() * (len(arr) - 1))]
    return token_str


def get_cipher():
    timestamp = str(int(time.time() * 1000))
    salt = get_token()
    year = time.strftime('%Y')
    month = time.strftime('%m') if int(time.strftime('%m')) < 10 else str(int(time.strftime('%m')) - 1)
    day = time.strftime('%d')
    iv = year + month + day
    text_1 = des3encrypt(timestamp, salt, iv)
    text_2 = salt + iv + text_1
    result = []
    l = list(text_2)
    for i in range(len(l)):
        if i != 0:
            result.append(' ')
        item = l[i]
        result.append(bin(ord(item))[2:])
    return ''.join(result)


# 解密访问网页获取的result
def decrypt(text: str) -> json:
    try:
        # print(text)
        data = json.loads(text)
        _key = data['secretKey']
        result = data['result']
        _iv = time.strftime('%Y%m%d')
        print(_iv)
        dtext = des3decrypt(result, _key, _iv)
        return json.loads(dtext)
    except Exception as e:
        print("结果解密错误: " + str(e))
        return None


def login_with_selenium():

    options = webdriver.ChromeOptions()
    options.add_argument("start-maximized")  # 窗口最大化

    # 隐藏"Chrome正在受到自动软件的控制"
    options.add_argument('disable-infobars')

    options.add_argument("service_args = ['–ignore-ssl-errors = true', '–ssl-protocol = TLSv1']")

    # 无浏览器模式,无浏览器模式无法定位元素
    # options.add_argument("--headless")
    options.add_argument('--disable-gpu')

    # Exclude the collection of enable-automation switches
    options.add_experimental_option("excludeSwitches", ["enable-automation"])

    # Turn-off useAutomationExtension
    options.add_experimental_option('useAutomationExtension', False)

    # driver
    driver = webdriver.Chrome()

    # set navigator.webdriver = undefined，防止被反爬识别为自动化webdriver
    driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
        "source": """
                    Object.defineProperty(navigator, 'webdriver', {
                      get: () => undefined
                    })
                  """
    })

    wait = WebDriverWait(driver, 20)

    driver.execute_cdp_cmd('Network.setUserAgentOverride', {
        "userAgent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36"})

    url = f'https://wenshu.court.gov.cn/website/wenshu/181217BMTKHNT2W0/index.html?pageId=1&s8=02'

    # 打开网页
    driver.get(url)
    # 刷新
    driver.refresh()

    # 点击登录
    frame = wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="contentIframe"]')))
    driver.switch_to.frame(frame)

    # 手机号输入框
    click_phone = wait.until(EC.presence_of_element_located(
        (By.XPATH, '//*[@id="root"]/div/form/div[1]/div[1]/div/div/div/input')))

    click_phone.send_keys("18852549878")
    time.sleep(1)

    # 密码输入框
    click_pwd = wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="root"]/div/form/div[1]/div[2]/div/div/div/input')))
    click_pwd.send_keys("Y%sj951104!")
    time.sleep(1)  # 等一秒是最优选择，短了网络错误

    # 登录按钮
    button_login = wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="root"]/div/form/div[3]/span')))
    button_login.click()

    # 必须加上表单退出，否者就是死元素无法定位
    driver.switch_to.default_content()

    # 新版改变，导致无法直接进入刑事，需要点击返回首页
    # click 返回首页
    click = wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="_view_1540966819000"]/div/ul/li[2]/a')))
    click.click()

    # get cookie
    cookie_list = driver.get_cookies()
    # print(cookie_list)
    cookie_dict = {}
    for cookie in cookie_list:
        cookie_dict[cookie['name']] = cookie['value']

    cookie_string = "; ".join([str(x) + "=" + str(y) for x, y in cookie_dict.items()])
    # 浏览器关闭
    driver.close()

    return cookie_string

cookie=login_with_selenium()
print(cookie)


post_url = 'https://wenshu.court.gov.cn/website/parse/rest.q4w'
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36",
    "Cookie": cookie
}

data = {
    'pageId': get_pageid(),
    's8': '04',
    'sortFields': 's50:desc',
    'ciphertext': get_cipher(),
    'pageNum': '1',
    'pageSize': '5',
    'queryCondition': '[{"key":"s8","value":"03"}]',
    'cfg': 'com.lawyee.judge.dc.parse.dto.SearchDataDsoDTO@queryDoc',
    '__RequestVerificationToken': get_token(24)
}


r = requests.post(post_url, headers=headers, data=data,verify=False)
print(r.text)
print(decrypt(r.text))



