import csv

import pymysql
from slider import retry


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


# step 1
def set_jar(account, pwd):
    driver = retry(account, pwd)
    try:
        cookies = driver.get_cookies()
    except:
        return set_jar(account, pwd)
    # jar = RequestsCookieJar()
    jar = ""
    for cookie in cookies:
        if cookie['name'] == "sessionip":
            continue
        # jar.set(cookie['name'], cookie['value'])
        jar += cookie['name']
        jar += "="
        jar += cookie['value']
        jar += "; "
    # print(jar)
    driver.close()
    return jar


if __name__ == '__main__':
    with open("账号.csv", encoding="UTF-8-sig") as zh:
        reader = csv.reader(zh)
        for zh in reader:
            try:
                cookie = set_jar(zh[0], zh[1])
                with open("账号cookie.txt", "a") as f:
                    f.write("['" + zh[0] + "','" + zh[1] + "','" + cookie + "']" + ",")
            except:
                with open("未跑账号", "a") as f:
                    f.write(zh[0] + "," + zh[1] + "\n")