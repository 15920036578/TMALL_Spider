# -*- coding: utf-8 -*-
__author__ = 'Gobi Xu'


import re
import time
from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from pyquery import PyQuery as pq


class TaobaoLogin(object):
    def __init__(self, username, password, chromedriver_path):
        self.url = 'https://login.taobao.com/member/login.jhtml'  # 淘宝登录地址
        self.username = username  # 接收传入的 账号
        self.password = password  # 接收传入的 密码
        options = webdriver.ChromeOptions()
        options.add_experimental_option("prefs", {"profile.managed_default_content_settings.images": 2})  # 不加载图片，加快访问速度
        options.add_experimental_option('excludeSwitches', ['enable-automation'])  # 设置为开发者模式，防止被各大网站识别出来使用了Selenium
        self.browser = webdriver.Chrome(executable_path=chromedriver_path, options=options)  # 接收传入的 chromedriver地址 和设置好的 options
        self.browser.maximize_window()  # 设置窗口最大化
        self.wait = WebDriverWait(self.browser, 10)  # 设置一个智能等待为10秒

    def login(self):
        self.browser.get(self.url)
        username_password_button = self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '.login-box.no-longlogin.module-quick > .hd > .login-switch')))  # 用css选择器选择 用账号密码登录按钮
        username_password_button.click()  # 点击 用账号密码登录按钮
        weibo_button = self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '.weibo-login')))  # 用css选择器选择 用微博登录按钮
        weibo_button.click()  # 点击 用微博登录按钮
        input_username = self.wait.until(EC.presence_of_element_located((By.XPATH, '//input[@name="username"]')))  # 用xpath选择器选择 账号框
        input_username.send_keys(self.username)  # 输入 账号
        input_password = self.wait.until(EC.presence_of_element_located((By.XPATH, '//input[@name="password"]')))  # 用xpath选择器选择 密码框
        input_password.send_keys(self.password)  # 输入 密码
        login_button = self.wait.until(EC.presence_of_element_located((By.XPATH, '//span[text()="登录"]')))  # 用xpath选择器选择 登录按钮
        login_button.click()  # 点击 登录按钮
        taobao_name = self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '.site-nav-login-info-nick')))  # 用css选择器选择 淘宝昵称
        print(''.join(['淘宝账号为：', taobao_name.text]))  # 输出 淘宝昵称

    def getPageTotal(self):
        page_total = self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '.ui-page-skip > form')))  # 用css选择器选择 商品列表页 总页数框
        page_total = page_total.text
        page_total = re.match('.*?(\d+).*', page_total).group(1)  # 清洗
        return page_total

    def dropDown(self):
        # 模拟人类 向下滑动浏览（下拉有加速度）
        for i in range(1, 52):
            drop_down = "var q=document.documentElement.scrollTop=" + str(i*100)
            self.browser.execute_script(drop_down)
            time.sleep(0.01)
            if i == 5:
                time.sleep(0.7)
            if i == 15:
                time.sleep(0.5)
            if i == 29:
                time.sleep(0.3)
            if i == 44:
                time.sleep(0.1)
        # 直接下拉到最底部
        # drop_down = "var q=document.documentElement.scrollTop=10000"
        # self.browser.execute_script(drop_down)

    def nextPage(self):
        # 获取 下一页的按钮 并 点击
        next_page_submit = self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '.ui-page-next')))
        next_page_submit.click()

    def sliderVerification(self):
        # 每次翻页后 检测是否有 滑块验证
        try:
            slider_button = WebDriverWait(self.browser, 5, 0.5).until(EC.presence_of_element_located((By.ID, 'nc_1_n1z')))
            action = ActionChains(self.browser)
            action.click_and_hold(slider_button).perform()
            action.reset_actions()
            # 模拟人类 向左拖动滑块（拖动有加速度）
            for i in range(100):
                action.move_by_offset(i*1, 0).perform()
                time.sleep(0.01)
            action.reset_actions()
        except:
            print('没有检测到滑块验证码')

    def crawlGoods(self, category):
        self.login()
        self.browser.get('https://list.tmall.com/search_product.htm?q={0}'.format(category))  # 天猫商品列表页地址，format()里面输入要爬取的类目
        page_total = self.getPageTotal()  # 获取 商品列表页 总页数
        print(''.join(['爬取的类目一共有：', page_total, '页']))
        for page in range(2, int(page_total)):  # 遍历 全部 商品列表页
            goods_total = self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '#J_ItemList .product .product-iWrap')))  # 确认 当前商品列表页 的 全部商品 都 加载完成
            page_frame = self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '.ui-page-skipTo')))  # 获取 当前页数框
            page_now = page_frame.get_attribute('value')  # 获取 当前页数
            print(''.join(['当前页数：', page_now, ' ', '总页数：', page_total]))
            html = self.browser.page_source  # 获取 当前页面的 源代码
            doc = pq(html)  # pq模块 解析 网页源代码
            goods_items = doc('#J_ItemList .product').items()  # 获取 当前页 全部商品数据
            for item in goods_items:  # 遍历 全部商品数据
                goods_title = item.find('.productTitle').text().replace('\n', '')  # 获取 商品标题 并清洗
                goods_sales_volume = item.find('.productStatus').text().replace('该款月成交\n', '').replace('笔', '')  # 获取 商品月销量 并清洗
                if goods_sales_volume:  # 是否有 月销量 的判断
                    goods_sales_volume = int(float(goods_sales_volume.replace('万', ''))*10000) if '万' in goods_sales_volume else int(goods_sales_volume)  # 进一步清洗 商品月销量
                else:
                    goods_sales_volume = 0
                goods_price = float(item.find('.productPrice').text().replace('¥\n', ''))  # 获取 商品价格 并清洗
                goods_shop = item.find('.productShop').text().replace('\n', '')  # 获取 店名 并清洗
                goods_url = ''.join(['https:', item.find('.productImg').attr('href')])  # 获取 详情页网址 并在地址最前面加上 https:
                goods_id = re.match('.*?id=?(\d+)&.*', goods_url).group(1)  # 获取 商品id
                print(''.join(['商品id：', goods_id, '\u0020\u0020\u0020\u0020\u0020', '商品标题：', goods_title, '\u0020\u0020\u0020\u0020\u0020', '商品价格：', str(goods_price), '\u0020\u0020\u0020\u0020\u0020', '商品月销量：', str(goods_sales_volume), '\u0020\u0020\u0020\u0020\u0020', '店名：', goods_shop, '\u0020\u0020\u0020\u0020\u0020', '详情页网址：', goods_url]))
            self.dropDown()  # 执行下拉动作
            self.nextPage()
            time.sleep(2)
            self.sliderVerification()
            time.sleep(3)


username = '123456789'  # 您的 微博账号
password = '*********'  # 您的 微博密码
chromedriver_path = 'x:/xxxxxxxx/xxxxxxxxx.exe'  # 您的 selenium驱动 存放地址
category = 'xx'  # 您要爬取的 类目

if __name__ == '__main__':
    a = TaobaoLogin(username, password, chromedriver_path)
    a.crawlGoods(category)
