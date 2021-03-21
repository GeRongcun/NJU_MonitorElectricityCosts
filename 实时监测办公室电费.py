import time
from selenium import webdriver
import time # 时间模块，用于暂停
import datetime

# 有界面模式
driver = webdriver.Chrome(r"D:\00_OneDrive\学习笔记20200104\00Code\Python\ChromeDriver\chromedriver_v88.0.4324.96.exe")
# 注意chromedriver的版本与chrome的版本对应； chromedriver下载网址：http://chromedriver.chromium.org/downloads

# # 无界面模式
# from selenium.webdriver.chrome.options import Options
# options = Options()
# options.add_argument('--headless')
# options.add_argument('--disable-gpu')
# driver = webdriver.Chrome(executable_path=r"D:\00_OneDrive\学习笔记20200104\00Code\Python\ChromeDriver\chromedriver_v88.0.4324.96.exe",options=options)

# 监测570电费情况
def getPowerNum570():
    sleepTime=10
    #
    url='http://172.27.2.95:8899/query/'
    driver.get(url)
    time.sleep(sleepTime) # 单位是秒
    
    # 点击“请选择房间”
    building = driver.find_element_by_id('city-title')
    building.click()
    time.sleep(sleepTime) # 单位是秒
    
    kunshan = driver.find_element_by_link_text("地理楼（昆山楼）")
    kunshan.click()
    time.sleep(sleepTime) # 单位是秒
    
    fifthFloor = driver.find_element_by_link_text("第5层")
    fifthFloor.click()
    time.sleep(sleepTime) # 单位是秒
    
    B515 = driver.find_element_by_link_text("B570")
    B515.click()
    time.sleep(sleepTime) # 单位是秒
    
    power = driver.find_element_by_id('J_remain')
    nowTime = datetime.datetime.now()
    nowPowerNumber=power.get_attribute('value')
    print(nowTime,end=" ")
    print(nowPowerNumber)
    time.sleep(sleepTime) # 单位是秒
    return nowTime,nowPowerNumber

# 如果电费发生变化，就发送邮件到指定邮箱
# https://www.runoob.com/python/python-email.html

#!/usr/bin/python
# -*- coding: UTF-8 -*-
import smtplib
from email.mime.text import MIMEText
from email.utils import formataddr
 
my_sender='gerongcun@qq.com'    # 发件人邮箱账号
my_pass = 'jiftonddkhixbecd'        # 注意：这里不是密码，而应该填写授权码！！
my_user='1612134704@qq.com'     # 收件人邮箱账号，我这边发送给自己

def mail(message):
    ret=True
    try:
#         msg=MIMEText('老板房间电费发生变化！！！','plain','utf-8')
        msg=MIMEText(message,'plain','utf-8')
        msg['From']=formataddr(["葛荣存",my_sender])  # 括号里的对应发件人邮箱昵称、发件人邮箱账号
        msg['To']=formataddr(["葛荣存",my_user])              # 括号里的对应收件人邮箱昵称、收件人邮箱账号
        msg['Subject']="【主题】房间电费发生变化！！！"                # 邮件的主题，也可以说是标题
        server=smtplib.SMTP_SSL("smtp.qq.com", 465)  # 发件人邮箱中的SMTP服务器，端口是25
        server.login(my_sender, my_pass)  # 括号中对应的是发件人邮箱账号、邮箱密码
        server.sendmail(my_sender,[my_user,],msg.as_string())  # 括号中对应的是发件人邮箱账号、收件人邮箱账号、发送邮件
        server.quit()  # 关闭连接
    except Exception:  # 如果 try 中的语句没有执行，则会执行下面的 ret=False
        ret=False
    return ret

# 执行代码
def main():
    lastTime570,lastPowerNumber570=getPowerNum570()
    for i in range(14400):
        print(i)
        print("570",end=" ")
        nowTime570,nowPowerNumber570=getPowerNum570()

        with open(r'D:\00Desktop20201002\00Code\Python\JupyterNotebookCode\20201201实时记录电费使用情况\Result\570电费v2.txt', 'a') as f:
            f.write(str(nowTime570)+" "+nowPowerNumber570+"\n")
        f.close()

        if lastPowerNumber570!=nowPowerNumber570:
            message="570房间电费发生变化\n"+"上条记录："+str(lastTime570)+" "+lastPowerNumber570+"\n"+"当前记录："+str(nowTime570)+" "+nowPowerNumber570+"\n"
            ret=mail(message)
            if ret:
                print("邮件发送成功")
            else:
                print("邮件发送失败")
        lastTime570=nowTime570
        lastPowerNumber570=nowPowerNumber570
    
if __name__ == '__main__':
    main()
