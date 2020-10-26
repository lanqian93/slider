import os

import numpy as np
import cv2
from PIL import Image
from selenium.webdriver.support import expected_conditions as EC
from selenium import webdriver
from selenium.webdriver import ChromeOptions, ActionChains
import requests
import time
import random
import pymysql

from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait

user_agent = [
    "Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_6_8; en-us) AppleWebKit/534.50 (KHTML, like Gecko) Version/5.1 Safari/534.50",
    "Mozilla/5.0 (Windows; U; Windows NT 6.1; en-us) AppleWebKit/534.50 (KHTML, like Gecko) Version/5.1 Safari/534.50",
    "Mozilla/5.0 (Windows NT 10.0; WOW64; rv:38.0) Gecko/20100101 Firefox/38.0",
    "Mozilla/5.0 (Windows NT 10.0; WOW64; Trident/7.0; .NET4.0C; .NET4.0E; .NET CLR 2.0.50727; .NET CLR 3.0.30729; .NET CLR 3.5.30729; InfoPath.3; rv:11.0) like Gecko",
    "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Trident/5.0)",
    "Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.0; Trident/4.0)",
    "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.0)",
    "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1)",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.6; rv:2.0.1) Gecko/20100101 Firefox/4.0.1",
    "Mozilla/5.0 (Windows NT 6.1; rv:2.0.1) Gecko/20100101 Firefox/4.0.1",
    "Opera/9.80 (Macintosh; Intel Mac OS X 10.6.8; U; en) Presto/2.8.131 Version/11.11",
    "Opera/9.80 (Windows NT 6.1; U; en) Presto/2.8.131 Version/11.11",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_0) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.56 Safari/535.11",
    "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; Maxthon 2.0)",
    "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; TencentTraveler 4.0)",
    "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)",
    "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; The World)",
    "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; Trident/4.0; SE 2.X MetaSr 1.0; SE 2.X MetaSr 1.0; .NET CLR 2.0.50727; SE 2.X MetaSr 1.0)",
    "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; 360SE)",
    "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; Avant Browser)",
    "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)",
    "Mozilla/5.0 (iPhone; U; CPU iPhone OS 4_3_3 like Mac OS X; en-us) AppleWebKit/533.17.9 (KHTML, like Gecko) Version/5.0.2 Mobile/8J2 Safari/6533.18.5",
    "Mozilla/5.0 (iPod; U; CPU iPhone OS 4_3_3 like Mac OS X; en-us) AppleWebKit/533.17.9 (KHTML, like Gecko) Version/5.0.2 Mobile/8J2 Safari/6533.18.5",
    "Mozilla/5.0 (iPad; U; CPU OS 4_3_3 like Mac OS X; en-us) AppleWebKit/533.17.9 (KHTML, like Gecko) Version/5.0.2 Mobile/8J2 Safari/6533.18.5",
    "Mozilla/5.0 (Linux; U; Android 2.3.7; en-us; Nexus One Build/FRF91) AppleWebKit/533.1 (KHTML, like Gecko) Version/4.0 Mobile Safari/533.1",
    "MQQBrowser/26 Mozilla/5.0 (Linux; U; Android 2.3.7; zh-cn; MB200 Build/GRJ22; CyanogenMod-7) AppleWebKit/533.1 (KHTML, like Gecko) Version/4.0 Mobile Safari/533.1",
    "Opera/9.80 (Android 2.3.4; Linux; Opera Mobi/build-1107180945; U; en-GB) Presto/2.8.149 Version/11.10",
    "Mozilla/5.0 (Linux; U; Android 3.0; en-us; Xoom Build/HRI39) AppleWebKit/534.13 (KHTML, like Gecko) Version/4.0 Safari/534.13",
    "Mozilla/5.0 (BlackBerry; U; BlackBerry 9800; en) AppleWebKit/534.1+ (KHTML, like Gecko) Version/6.0.0.337 Mobile Safari/534.1+",
    "Mozilla/5.0 (hp-tablet; Linux; hpwOS/3.0.0; U; en-US) AppleWebKit/534.6 (KHTML, like Gecko) wOSBrowser/233.70 Safari/534.6 TouchPad/1.0",
    "Mozilla/5.0 (SymbianOS/9.4; Series60/5.0 NokiaN97-1/20.0.019; Profile/MIDP-2.1 Configuration/CLDC-1.1) AppleWebKit/525 (KHTML, like Gecko) BrowserNG/7.1.18124",
    "Mozilla/5.0 (compatible; MSIE 9.0; Windows Phone OS 7.5; Trident/5.0; IEMobile/9.0; HTC; Titan)",
    "UCWEB7.0.2.37/28/999",
    "NOKIA5700/ UCWEB7.0.2.37/28/999",
    "Openwave/ UCWEB7.0.2.37/28/999",
    "Mozilla/4.0 (compatible; MSIE 6.0; ) Opera/UCWEB7.0.2.37/28/999",
    # iPhone 6：
    "Mozilla/6.0 (iPhone; CPU iPhone OS 8_0 like Mac OS X) AppleWebKit/536.26 (KHTML, like Gecko) Version/8.0 Mobile/10A5376e Safari/8536.25",

]


def get_ip():
    conn = pymysql.connect(host="192.168.0.108", user="root", password="cdyn00", database="ippool", charset="utf8")
    cursor = conn.cursor()
    # 定义要执行的SQL语句
    sql = "select ip, port from ippool"
    cursor.execute(sql)
    ips = cursor.fetchall()
    # 关闭光标对象
    cursor.close()
    # 关闭数据库连接
    conn.close()
    return ips


def get_track(distance):  # distance为传入的总距离
    # 移动轨迹
    track = []
    # 当前位移
    current = 0
    # 减速阈值
    mid = distance * 4 / 5
    # 计算间隔
    t = 0.2
    # 初速度
    v = 0

    while current < distance:
        if current < mid:
            # 加速度为2
            a = 2
        else:
            # 加速度为-2
            a = -3
        v0 = v
        # 当前速度
        v = v0 + a * t
        # 移动距离
        move = v0 * t + 1 / 2 * a * t * t
        # 当前位移
        current += move
        # 加入轨迹
        track.append(round(move))
    return track


# step7
def move_to_gap(driver, slider, instance):     # slider是要移动的滑块,tracks是要传入的移动轨迹
    ActionChains(driver).click_and_hold(slider).perform()
    # for x in tracks:
    #     ActionChains(driver).move_by_offset(xoffset=x, yoffset=0).perform()
    ActionChains(driver).move_by_offset(xoffset=instance, yoffset=0).perform()
    time.sleep(0.5)
    ActionChains(driver).release().perform()


# step4 更换ip重试
def change_req(src, block_src):
    ua = random.choice(user_agent)
    ips = get_ip()
    ip = random.choice(ips)
    headers = {
        'Accept': 'image/webp,image/apng,image/*,*/*;q=0.8',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
        'Host': 't.captcha.qq.com',
        'Sec-Fetch-Dest': 'image',
        'Sec-Fetch-Mode': 'no-cors',
        'Sec-Fetch-Site': 'same-origin',
        'User-Agent': ua
    }
    proxies = {
        "http": "http://{}:{}".format(ip[0], ip[1]),
        "https": "http://{}:{}".format(ip[0], ip[1]),
    }
    res = requests.get(src, headers=headers, proxies=proxies, timeout=8)
    blc = requests.get(block_src, headers=headers, proxies=proxies, timeout=8)
    return res, blc


# step3 发送图片请求
def get_image(driver, src, block_src):
    try:
        res, blc = change_req(src, block_src)
    except:
        res, blc = None, None
    return res, blc


# step2 获取图片url
def get_image_src(driver):
    time.sleep(2)
    img = driver.find_element_by_css_selector("#slideBg")
    src = img.get_attribute("src")
    block = driver.find_element_by_css_selector("#slideBlock")
    block_src = block.get_attribute("src")
    return src, block_src, img, block


# step5 保存图片
def save_img(driver):
    time.sleep(2)
    # 背景图
    img = driver.find_element_by_css_selector("#slideBg")
    src = img.get_attribute("src")
    # 滑块
    block = driver.find_element_by_css_selector("#slideBlock")
    block_src = block.get_attribute("src")
    # 等待滑块加载出来获取图片src
    if not src or not block_src:
        count = 0
        while count < 10:
            src, block_src, img, block = get_image_src(driver)
            if src and block_src:
                count += 10
            else:
                count += 1
    # 保存图片
    if src and block_src:
        res, blc = get_image(driver, src, block_src)
        if res and blc:
            with open("bg.jpeg", "wb") as fp:
                fp.write(res.content)
            with open("block.jpeg", "wb") as fp:
                fp.write(blc.content)
                return 1, img, block
        else:
            count = 0
            print("第{}次重新请求图片".format(count + 1))
            while count < 10:
                res, blc = get_image(driver, src, block_src)
                if res and blc:
                    with open("bg.jpeg", "wb") as fp:
                        fp.write(res.content)
                    with open("block.jpeg", "wb") as fp:
                        fp.write(blc.content)
                    count += 10
                else:
                    count += 1
            if res and blc:
                return 1, img, block
            else:
                driver.close()
                return 0, img, block

    else:
        return 0, img, block


# step6 计算缺口的位置
def get_diff_location(blo, bg):
    target = cv2.imread(blo, 0)
    template = cv2.imread(bg, 0)
    w, h = target.shape[::-1]
    temp = 'temp.jpg'
    targ = 'targ.jpg'
    cv2.imwrite(temp, template)
    cv2.imwrite(targ, target)
    target = cv2.imread(targ)
    target = cv2.cvtColor(target, cv2.COLOR_BGR2GRAY)
    target = abs(255 - target)
    cv2.imwrite(targ, target)
    target = cv2.imread(targ)
    template = cv2.imread(temp)
    result = cv2.matchTemplate(target, template, cv2.TM_CCOEFF_NORMED)
    x, y = np.unravel_index(result.argmax(), result.shape)
    # print(x, y)
    # 展示圈出来的区域
    # cv2.rectangle(template, (y, x), (y + w, x + h), (7, 249, 151), 2)
    # cv2.imshow('Show', template)
    # cv2.waitKey(0)
    # cv2.destroyAllWindows()
    return x, y, template.shape[1]


# 验证码
def yzm(driver, photo):
    # 截图
    driver.save_screenshot('code.png')
    # 获取验证码位置
    # 截图起点（x，y） 824,160 验证码大小（width，height）90 41
    x = photo.location['x']
    y = photo.location['y']
    width = photo.size['width']
    height = photo.size['height']
    #
    # # 打开图片
    # # 截图
    im = Image.open('code.png')
    im = im.crop((x, y, x + width, y + height))
    im.save('hehe.png')
    with open("hehe.png", "rb") as f:
        img_bytes = f.read()
    ret = requests.get('http://192.168.0.108:6607/captcha', data=img_bytes)
    return ret.text


def vali_ip():
    try:
        ip = random.choice(get_ip())
        headers = {
            'Connection': 'close'
        }
        proxies = {
            'https': 'http://{}:{}'.format(ip[0], ip[1]),
            'http': 'http://{}:{}'.format(ip[0], ip[1]),
        }
        resp = requests.get(r'https://www.baidu.com', proxies=proxies, timeout=1, headers=headers)
        if resp.status_code and resp.status_code == 200:
            i = ip[0] + ":" + ip[1]
            return i
        else:
            return vali_ip()
    except Exception as e:
        return vali_ip()


# step 1
def move_slider(account, pwd):
    option = ChromeOptions()
    option.add_experimental_option('excludeSwitches', ['enable-logging'])
    option.add_argument('--incognito')
    option.add_argument("--headless")
    driver = webdriver.Chrome(chrome_options=option)
    driver.set_page_load_timeout(20)
    driver.set_script_timeout(20)
    try:
        print(account)
        # my_ip = vali_ip()
        # os.system('代理.bat {}'.format(my_ip))

        # # option.add_argument(('--user-agent=' + ua))
        # option.add_experimental_option('excludeSwitches', ['enable-automation'])

        # option.add_argument('disable-infobars')
        # option.add_argument(('--proxy-server=http://' + ip[0] + ":" + ip[1]))
        driver.get(
            "https://account.m.autohome.com.cn/login?pvareaid=6826313&fPosition=0&sPosition=0&platform=2&isphone=1&backurl=https%3A%2F%2Fyou.m.autohome.com.cn%2Ffe%2Fm%2Fpersonal%2Fhome")
        # # driver.maximize_window()
        WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.ID, "btnLogin")))
        driver.find_element_by_css_selector("#txtUserName").send_keys(account)
        driver.find_element_by_css_selector("#txtPwd").send_keys(pwd)
        driver.find_element_by_css_selector("#check_submitpassword").click()
        driver.find_element_by_css_selector("#autoCaptcha").click()
        WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.ID, "tcaptcha_iframe")))
        driver.switch_to.frame(driver.find_element_by_css_selector("#tcaptcha_iframe"))
        result, bg_img, block_img = save_img(driver)
        # 没有加载出验证码
        if not result:
            print("验证码加载失败,重试")
            driver.close()
            return move_slider(account, pwd)
        x, y, save_img_wid = get_diff_location("block.jpeg", "bg.jpeg")
        # 背景宽度
        bg_wid = bg_img.size['width']
        # 背景x
        bg_x = bg_img.location["x"]
        # 滑块x
        block_x = block_img.location["x"]
        instance = (bg_wid / save_img_wid) * y - (block_x - bg_x)
        # instance = y / 2 - 26  # 208.5   341-
        # print("距离", instance)
        # track = get_track(instance)
        # # 滑块
        slider = driver.find_element_by_css_selector("#tcaptcha_drag_thumb")
        move_to_gap(driver, slider, instance)
        time.sleep(2)
        driver.switch_to.default_content()
        try:
            driver.find_element_by_css_selector("#btnLogin").click()
        except:
            time.sleep(2)
            driver.find_element_by_css_selector("#btnLogin").click()
        # input("登录之后回车")
        WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.ID, "app")))
        return driver
    except:
        driver.close()
        return move_slider(account, pwd)


def retry(account, pwd):
    driver = move_slider(account, pwd)
    return driver


if __name__ == '__main__':
    my_ip = vali_ip()
    os.system('代理.bat {}'.format(my_ip))

          
