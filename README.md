# 天猫爬虫
![](https://img.shields.io/badge/Python-3.5.3-green.svg) ![](https://img.shields.io/badge/selenium-3.141.0-green.svg) ![](https://img.shields.io/badge/pyquery-1.4.0-green.svg)
#### 天猫官网 - https://www.tmall.com/
|Author|Gobi Xu|
|---|---|
|Email|792799564@qq.com|
****
## 前言
#### 全程使用selenium进行自动化爬取
## 声明
#### 任何内容都仅用于学习交流，请勿用于任何商业用途。
## 介绍
- **防止被检测出为机器人**
- **对应的爬虫在spiders/suning_xxxx.py里**
> **目前只有爬取[手机](https://search.suning.com/%E6%89%8B%E6%9C%BA/)这个类目<br>**
> **对应的spider里有详细过程注释，请放心食用 :point_left:**
## 运行环境
#### Version: Python3
## 安装依赖库
```
pip install selenium
pip install pyquery
```
## 类目
#### :telephone_receiver:[手机](https://search.suning.com/%E6%89%8B%E6%9C%BA/)
#### 爬取字段：
- **商品id (id)**
- **商品标题 (title)**
- **商品价格 (price)**
- **商品牌子 (brand)**
- **商品型号 (model)**
- **商品的网店名称 (shop_name)**
- **商品评论数量 (comment_count)**
- **商品详情页网址 (url)**
