# -*- coding: utf-8 -*-

'''

File: main.py
Author: Ataida
Date: 2024-05-26

Version Info:
Python 3.9.13
Selenium 4.21.0
Google Chrome 125.0.6422.113
ChromeDriver 125.0.6422.78（Revision:r1287751)

Other:
ChromeDriver更新地址：https://googlechromelabs.github.io/chrome-for-testing/#stable

'''

# 请求用户Cookies的函数，请求到的Cookies会保存至json中
def GetUserCookies():
    global chrome_options
    # 先关闭无头模式
    is_headless = "--headless" in chrome_options.arguments
    if is_headless:
        chrome_options.remove_argument("--headless")
        driver.maximize_window()
    LoginUrl = 'https://www.missevan.com/member/login'
    driver.get(LoginUrl)  # 访问登录页面
    sleep(25)  # 等待25秒用户操作
    # 浏览器等待Url发生变化
    try:
        WebDriverWait(driver, 60).until(
            EC.url_changes(LoginUrl)
        )
        Cookies = driver.get_cookies()
        # 保存Cookies文件
        with open('data/Cookies.json', "w") as file:
            json.dump(Cookies, file)
        print('Cookies写入完成！')
    except:
        print('操作超时')
        x = input('是否需要重新进行登录呢？输入“Y”重新执行登录，直接回车“Enter”则结束程序:')
        if x == 'Y':
            GetUserCookies()
        else:
            driver.quit()

# 让Selenium携带Cookies访问网站
def OpenWithCookies():
    global chrome_options
    chrome_options.add_argument("--window-size=1280,720")  # 设置为1920x1080的窗口大小
    chrome_options.add_argument("--headless")  # 不知道为什么没有效果
    Url = 'https://www.missevan.com/'
    driver.get(Url)
    # 读取Cookies
    with open('data/Cookies.json', 'r') as file:
        Cookies = json.load(file)
        for cookie in Cookies:
            # 将Cookies添加到浏览器
            driver.add_cookie(cookie)
    # 添加完成后刷新页面应用Cookies
    driver.refresh()

# 获取API列表
def GetAPIList(Title):
    SearchUrl = 'https://www.missevan.com/sound/search?type=drama&keyword='+ Title
    driver.get(SearchUrl)
    # 点击“更多”按钮
    MoreButton = driver.find_element(By.XPATH, '//*[@id="root"]/div[2]/div[2]/div[1]/div/div[4]/div[7]/a')
    Link = MoreButton.get_attribute('href')
    driver.get(Link)
    # 匹配album列表，获取每个文件的id
    Atags = driver.find_elements(By.XPATH,'//*[@id="drama-detail-content"]/div/div[1]/div/ul/a')
    with open('data/Urls.txt', 'w') as file:
        for id in Atags:
            src = id.get_attribute('href')
            IdNum = src.split('=')[-1]
            # 感谢Github大佬ravizhan提供的API！
            file.write('https://www.missevan.com/sound/getsound?soundid='+ IdNum + '\n')

# 获取页面中的详细数据
def GetInfo(Url):
    driver.get(Url)
    sleep(2)
    # JsonTxt = driver.find_element(By.TAG_NAME, 'body').text  # 从页面中提取 JSON 数据
    # JsonData = json.loads(JsonTxt)  # 解析 JSON 数据
    # # 提取VideoUrl、SoundUrl、Soundstr
    # Title = JsonData.get('soundstr')
    # Sound = JsonData.get('soundurl')
    # Video = JsonData.get('videourl')
    page_content = driver.page_source  # 获取页面内容
    SoundStr = re.search(r'"soundstr":"(.*?)"', page_content)
    Title = SoundStr.group(1)
    SoundUrl = re.search(r'"soundurl":"(.*?)"', page_content)
    Sound = SoundUrl.group(1)
    VideoUrl = re.search(r'"videourl":"(.*?)"', page_content)
    Video = VideoUrl.group(1)
    return Title, Sound, Video

# 保存文件
def SaveFile(Title, Sound, Video):
    # # 检查文件名称是否合法
    # if re.match(r'^[a-zA-Z0-9_-]+$', Title) and not Title.startswith('-'):
    #     sanitized_filename = Title
    # else:
    #     sanitized_filename = re.sub(r'[^\w\-\.]', '', Title)

    # 获取文件后缀名并保存文件
    try:
        parsed_url = urlparse(Sound)
        path = parsed_url.path
        if path is not None:
            SoundFileName = path.split('/')[-1]
            # 其他操作
            with open('output/' + Title + '.' + SoundFileName, 'wb') as file:
                response = requests.get(Sound)
                file.write(response.content)
    except:
        parsed_url = urlparse(Video)
        path = parsed_url.path
        if path is not None:
            VideoFileName = path.split('/')[-1]
            # 其他操作
            with open('output/' + Title + '.' + VideoFileName, 'wb') as file:
                response = requests.get(Video)
                file.write(response.content)
    finally:
        with open('data/ErrorLog.txt', 'a') as file:
            # 获取当前日期和时间
            current_datetime = datetime.now()
            formatted_datetime = current_datetime.strftime("%Y-%m-%d %H:%M")
            # 要追加的内容
            content_to_append = f"{formatted_datetime} | {Title} | {Sound} | {Video}"
            file.write(content_to_append + '\n')

if __name__ == '__main__':
    from selenium import webdriver
    from selenium.webdriver.chrome.service import Service
    from selenium.webdriver.support.ui import WebDriverWait
    from selenium.webdriver.support import expected_conditions as EC
    from time import sleep
    import json
    import os
    from selenium.webdriver.common.by import By
    import re
    import requests
    from urllib.parse import urlparse
    from datetime import datetime
    from selenium.webdriver.chrome.options import Options

    # 创建实例
    chrome_options = Options()
    service = Service(executable_path='chromedriver-win64/chromedriver.exe')  # 设定驱动器位置
    driver = webdriver.Chrome(service=service, options=chrome_options)  # 创建实例
    driver.implicitly_wait(15)  # 设置15秒隐式等待

    # 获取Cookies
    if os.path.exists('data/Cookies.json'):
        OpenWithCookies()
    else:
        GetUserCookies()

    # 请求关键词
    Title = input('请输入想要搜索的剧集名称（确认后按下回车）：')
    GetAPIList(Title)

    # 获取基本信息
    with open('data/Urls.txt', "r") as file:
        for line in file:
            T, S, V = GetInfo(line.strip())  # 使用 strip() 方法去除每行末尾的换行符
            SaveFile(T, S, V)

    # 关闭实例
    driver.quit()