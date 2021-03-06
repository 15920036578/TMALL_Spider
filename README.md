# 天猫爬虫
![](https://img.shields.io/badge/Python-3.5.3-green.svg) ![](https://img.shields.io/badge/selenium-3.141.0-green.svg) ![](https://img.shields.io/badge/pyquery-1.4.0-green.svg)
#### 天猫官网 - https://www.tmall.com/
|Author|Gobi Xu|
|---|---|
|Email|xusanity@aliyun.com|
****
## 声明
#### 任何内容都仅用于学习交流，请勿用于任何商业用途。
## 前言
#### 开始之前，你需要
- **注册一个[淘宝账号](https://reg.taobao.com/member/reg/fill_mobile.htm)**
- **注册一个[微博账号](https://weibo.com/signup/signup.php)**
- **下载[chrome浏览器](https://chrome.en.softonic.com/)**
- **下载对应chrome浏览器版本的[chromedriver驱动](http://chromedriver.storage.googleapis.com/index.html)**
#### 简单说明
- **全程使用selenium进行爬取**
- **请求时需要携带cookies（即需要先登录），否则极易出现验证码**
## 运行环境
#### Version: Python3
## 安装依赖库
```
pip install selenium
pip install pyquery
```
## 细节
- **防止被检测出为机器**
###### 一般我们在chrome浏览器的Console里输入window.navigator.webdriver后会返回undefined的值
![enter image description here](picture/undefined.jpg)
###### 如果你在chromedriver驱动的Console里输入window.navigator.webdriver后会返回true的值
![enter image description here](picture/true.jpg)
###### 解决办法
```
options = webdriver.ChromeOptions()
options.add_experimental_option('excludeSwitches', ['enable-automation'])  # 设置为开发者模式
# 在options里加上这个参数使得chromedriver驱动不会被检测出为机器
```
- **模仿人类行为**
###### 匀加速下滑浏览器
```
for i in range(1, 52):
  drop_down = "var q=document.documentElement.scrollTop=" + str(i*100)
  self.browser.execute_script(drop_down)
  time.sleep(0.01)  # 值越小越顺滑，越像人类行为
  # 模仿人类，发现喜欢的商品时会停止滑动
  if i == 5:
    time.sleep(1.3)
  if i == 15:
    time.sleep(1.9)
  if i == 29:
    time.sleep(0.7)
  if i == 44:
    time.sleep(0.3)
```
###### 匀加速右滑验证码的滑块（每次请求下一页商品列表页时可能会出现滑块验证码）
```
slider_button = WebDriverWait(self.browser, 5, 0.5).until(EC.presence_of_element_located((By.ID, 'nc_1_n1z')))
action = ActionChains(self.browser)
action.click_and_hold(slider_button).perform()
action.reset_actions()
# 模拟人类 向左拖动滑块（拖动有加速度）
for i in range(100):
  action.move_by_offset(i*1, 0).perform()
  time.sleep(0.01)  # 值越小越顺滑，越像人类行为
```
## 最后
- **taobao_spider.py里有大量注释，请放心食用:meat_on_bone:**
- **如有任何问题都可以邮箱:email:联系我，我会尽快回复你。**
