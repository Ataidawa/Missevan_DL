# Missevan_DL
通过Python+Selenium的方式制作爬虫工具，批量下载M站上免费或已购买的剧集，正在努力改进中……仅用于学习与交流！
原项目地址： [M_Download](https://github.com/Ataidawa/M_Download)，因Selenium版本更新过快 遂放弃继续优化，推倒重新制作此版本Missevan下载工具。

# 基本信息
使用核心内容版本：
|程序|版本|
|:-----:|:-----:|
|Python|3.9.13|
|Selenium|4.21.0|
|Google Chrome|125.0.6422.113 / stable|
|ChromeDriver|125.0.6422.78 / r1287751|

# 使用方式
1. 如果你想试一试，可以在Pycharm中执行`main.py`,通过调用`venv\Scripts\python.exe`你应该也可以成功。我尝试了一下是可以的，但是次数多了之后开始出现`403 Forbidden`了，于是在代码里加了一些……
	```Python
	time.sleep(25)
	driver.implicitly_wait(15)
	WebDriverWait(driver, 60).until(
            	EC.url_changes(LoginUrl)
        	)
	```
	应该不会太有影响，如果你有更好的方式也欢迎大佬随时修改！
2. 如果你对代码并不太了解，也可以直接找`dist\Missevan_DL.exe`双击执行，程序会先让你登录获取您的Cookies，再在Console（控制台 ~是的我没做界面~）中输入你要找的剧集，之后程序会自动执行，等Console消失，前往`dist\output\`中转存你需要的文件就可以啦！
3. 如果我太久没更新，Webdriver版本可能会过时，很着急需要用的话可以前往[Chrome for Testing availability](https://googlechromelabs.github.io/chrome-for-testing/#stable)下载最新Stable版chromedriver-win64替换掉`chromedriver-win64`里和`dist\chromedriver-win64`的文件哈。

# 有的没的
我的文件还很粗糙，非常感谢[ravizhan](https://github.com/ravizhan)大佬提供的API！您说：
> 个人认为除了登录没必要用selenium
我的思路是把要下的音频加歌单里，然后用xpath解析html来提取 文件名和id

我已经尝试过了，使用Requests即使是携带Cookies和Headers都没办法获取到API中的SoundUrl或VideoUrl！~白嫖~不太可行。如果有更好的方法的话也欢迎大家在 Pull requests 和 Issues 中 告诉我喔！

### 本项目地址 [Missevan_DL](https://github.com/Ataidawa/Missevan_DL)