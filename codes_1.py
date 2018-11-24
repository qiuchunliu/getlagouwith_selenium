from selenium import webdriver
# 模拟操作浏览器
from lxml import etree
# 用xpath 来提取元素
import time
# 等待操作


class Spider(object):

    def __init__(self):
        self.driver = webdriver.Firefox(executable_path='geckodriver.exe')
        self.driver2 = webdriver.Firefox(executable_path='geckodriver.exe')
        # 设置两个浏览器，分别打开网页
        # 因为在 43 行有问题
        # 待优化
        self.url = 'https://www.lagou.com/jobs/list_python?labelWords=&fromSearch=true&suginput='

    def run(self):
        self.driver.get(self.url)
        while True:
            source = self.driver.page_source
            # 此处获取的source 就是页面检查元素所看到的内容了
            # 不需要考虑Ajax或者json数据了
            self.parse(source)
            # 获取所需数据
            next_button = self.driver.find_element_by_xpath('//div[@class="pager_container"]/span[last()]')
            # 找到进入‘下一页’的按钮，在下面进行点击，以进入下一页
            if "pager_next pager_next_disabled" in next_button.get_attribute('class'):
                # 如果是最后一页了，则推出循环
                break
            else:
                next_button.click()
                time.sleep(2)
                # 此时只能是从第一页跳到第二页，
                # 需要一个循环结构来实现所有下一页的跳转

    def parse(self, sour):
        htlx = etree.HTML(sour)
        position_links = htlx.xpath('//a[@class="position_link"]/@href')
        # 找到页面里职位的链接
        # 并且对每个链接进入职位页面来提取数据
        for i in position_links[:1]:
            self.get_detail_page(i)

    def get_detail_page(self, url):
        self.driver2.get(url)
        # 这样的话，新的页面会覆盖原来的页面，但是有影响，新打开的页面是职位详情，没有‘下一页’
        # 因为原来的页面已经存储数据了
        source = self.driver2.page_source
        htlx = etree.HTML(source)
        # 获取元素:职位描述
        job_description = ''.join(htlx.xpath('//dd[@class="job_bt"]//text()')).strip()
        # .strip() 删除前后空白,包括换行符
        # 输出dd下的所有文本，存在列表里
        # 用 ''.join(list) 来把列表里的元素连接起来
        # 很好用，不错哦
        print(job_description)


if __name__ == '__main__':
    spider = Spider()
    spider.run()
