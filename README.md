
## 摘要

利用Selenium库每隔5分钟爬取学校电费查询网站的数据，检测导师办公室电费使用情况，判断导师是否来学校。

项目内容介绍：  

- README.md，本项目的说明资料；
- README_attachments，README.md文件的附件；
- chromedriver_v89.0.4389.23.exe，chromedriver安装包；
- 实时监测办公室电费.py，实现代码；

## 思路

学校有个网址<http://172.27.2.95:8899/query/>(内网访问)可以查询电表余量，界面如下：

![校园内网查询电表余量网址1](README_attachments/校园内网查询电表余量网址1.png)

![校园内网查询电表余量网址2](README_attachments/校园内网查询电表余量网址2.png)

每隔5分钟爬取这个网站的数据，检测导师办公室电费使用情况，就可以判断导师是否来学校。

因为该网站页面跳转时，url不发生变化，如果使用Request库爬取比较麻烦，所以，我选择使用Selenium库爬取。利用Selenium，就可以模拟鼠标点击、键盘输入，进行网页操作。

PS：Selenium是一个用于测试网站的自动化测试工具，支持各种浏览器包括Chrome、Firefox、Safari等主流界面浏览器，同时也支持phantomJS无界面浏览器。

## 代码实现

### selenium启动WebDriver

```python
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
```

```python
# 监测570电费情况
def getPowerNum570():
    sleepTime=10
    # 因为学校网站有点卡，所以，在进行一步网页操作后，需要等待一段时间，再进行下一步操作，我设置的等待时间是10s

    url='http://172.27.2.95:8899/query/'
    driver.get(url)
    time.sleep(sleepTime) # 单位是秒
    
    # 点击“请选择房间”
    building = driver.find_element_by_id('city-title')
    building.click()
    time.sleep(sleepTime) # 单位是秒
    
    # 点击"地理楼（昆山楼）"
    kunshan = driver.find_element_by_link_text("地理楼（昆山楼）")
    kunshan.click()
    time.sleep(sleepTime) # 单位是秒
    
    # 点击"第5层"
    fifthFloor = driver.find_element_by_link_text("第5层")
    fifthFloor.click()
    time.sleep(sleepTime) # 单位是秒
    
    # 点击"B570"
    B570 = driver.find_element_by_link_text("B570")
    B570.click()
    time.sleep(sleepTime) # 单位是秒
    
    # 获得电费余量
    power = driver.find_element_by_id('J_remain')
    nowTime = datetime.datetime.now()
    nowPowerNumber=power.get_attribute('value')
    print(nowTime,end=" ")
    print(nowPowerNumber)
    time.sleep(sleepTime) # 单位是秒
    return nowTime,nowPowerNumber
```

### 发送邮件

```python
# 如果电费发生变化，就发送邮件到指定邮箱
# https://www.runoob.com/python/python-email.html

#!/usr/bin/python
# -*- coding: UTF-8 -*-
import smtplib
from email.mime.text import MIMEText
from email.utils import formataddr
 
my_sender='gerongcun@qq.com'
# 发件人邮箱账号
my_pass = 'jifxonddkhixbecd'
# 注意：这里不是密码，而应该填写授权码！
# 为了保护隐私，这里的授权码不是真的，是我伪造的！
my_user='1612134704@qq.com'
# 收件人邮箱账号，我这边发送给自己

def mail(message):
    ret=True
    try:
        # msg=MIMEText('老板房间电费发生变化！！！','plain','utf-8')
        msg=MIMEText(message,'plain','utf-8')
        msg['From']=formataddr(["葛荣存",my_sender])
        # 括号里的对应发件人邮箱昵称、发件人邮箱账号
        msg['To']=formataddr(["葛荣存",my_user])       
        # 括号里的对应收件人邮箱昵称、收件人邮箱账号
        msg['Subject']="【主题】房间电费发生变化！！！"
        # 邮件的主题，也可以说是标题
        server=smtplib.SMTP_SSL("smtp.qq.com", 465)
        # 发件人邮箱中的SMTP服务器，端口是25
        server.login(my_sender, my_pass)
        # 括号中对应的是发件人邮箱账号、邮箱密码
        server.sendmail(my_sender,[my_user,],msg.as_string())
        # 括号中对应的是发件人邮箱账号、收件人邮箱账号、发送邮件
        server.quit()  # 关闭连接
    except Exception:  # 如果 try 中的语句没有执行，则会执行下面的 ret=False
        ret=False
    return ret
```

### main函数

```python
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
```

### 执行效果

![代码执行情况](README_attachments/代码执行情况.png)

![代码执行情况](README_attachments/代码执行情况2.png)

## 后话

学校电费查询网站一般在上午10点和晚上10点进行一次数据更新，更新频率较低。

![代码执行情况](README_attachments/代码执行情况3.png)

以这样的频率检测导师办公室电费使用情况，判断导师是否来学校，是不可行的。
