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
            a = 11
        else:
            # 加速度为-2
            a = -0.3
        v0 = v
        # 当前速度
        v = v0 + a * t
        # 移动距离
        move = v0 * t + 1 / 2 * a * t * t
        # 当前位移
        current += move
        # 加入轨迹
        track.append(round(move))
    # random.shuffle(track)
    track.sort(reverse=True)
    # print(track)
    return track


# step7
def move_to_gap(driver, slider, instance):     # slider是要移动的滑块,tracks是要传入的移动轨迹
    ActionChains(driver).click_and_hold(slider).perform()
    tracks = get_track(instance)
    for x in tracks:
        ActionChains(driver).move_by_offset(xoffset=x, yoffset=0).perform()
    # ActionChains(driver).move_by_offset(xoffset=instance, yoffset=0).perform()
    time.sleep(0.3)
    ActionChains(driver).release().perform()


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


def find_qk(driver):
    time.sleep(2)
    # 获取背景图
    driver.save_screenshot('full.png')
    bg = driver.find_element_by_css_selector(".geetest_window")
    blocation = bg.location
    bsize = bg.size
    top, bottom, left, right = blocation['y'], blocation['y'] + bsize['height'], blocation['x'], blocation['x'] + \
                               bsize[
                                   'width']
    img = Image.open('full.png')
    bg_img = img.crop((left, top, right, bottom))
    bg_img.save("bg.png")
    x, y, save_img_wid = get_diff_location("qk.png", "bg.png")
    slider = driver.find_element_by_css_selector(".geetest_slider_button")
    # print(y)
    move_to_gap(driver, slider, y - 5)


# step 1
def move_slider(account, pwd):
    print(account)
    option = ChromeOptions()
    option.add_experimental_option('excludeSwitches', ['enable-logging', 'enable-automation'])
    option.add_argument('--incognito')
    option.add_argument("--headless")
    driver = webdriver.Chrome(chrome_options=option)
    driver.set_page_load_timeout(20)
    driver.set_script_timeout(20)
    try:
        # my_ip = vali_ip()
        # os.system('代理.bat {}'.format(my_ip))

        # # option.add_argument(('--user-agent=' + ua))
        # option.add_experimental_option('excludeSwitches', ['enable-automation'])

        # option.add_argument('disable-infobars')
        # option.add_argument(('--proxy-server=http://' + ip[0] + ":" + ip[1]))
        driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
            "source": """Object.defineProperty(navigator, 'webdriver', {get: () => undefined})""",
        })
        driver.get(
            "https://account.m.autohome.com.cn/login?isphone=1&backurl=https%3A%2F%2Fyou.m.autohome.com.cn%2Ffe%2Fm%2Fpersonal%2Fhome")
        # # driver.maximize_window()
        WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.ID, "btnLogin")))
        driver.find_element_by_css_selector("#txtUserName").send_keys(account)
        driver.find_element_by_css_selector("#txtPwd").send_keys(pwd)
        driver.find_element_by_css_selector("#check_submitpassword").click()
        WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.XPATH, "//div[@class='geetest_radar_tip']")))
        driver.find_element_by_css_selector(".geetest_radar_tip_content").click()
        WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, "//div[@class='geetest_radar_tip']/span[1][text()='请完成验证']")))
        # 滑块
        find_qk(driver)
        time.sleep(2)
        driver.find_element_by_xpath("//div[@id='btnLogin' and @class='handle-login']").click()
        WebDriverWait(driver, 16).until(EC.presence_of_element_located((By.ID, "app")))
        return driver
    except Exception as e:
        driver.close()
        return move_slider(account, pwd)


def retry(account, pwd):
    driver = move_slider(account, pwd)
    return driver


if __name__ == '__main__':
    my_ip = vali_ip()
    os.system('代理.bat {}'.format(my_ip))

          
