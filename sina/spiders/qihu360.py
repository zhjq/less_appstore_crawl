# -*- coding:utf-8 -*-  
from __future__ import unicode_literals
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

import scrapy

import codecs

import util

class QihuSpider(scrapy.Spider):
    name = "360"
    fileout = codecs.open('360.txt', 'a', 'utf-8')
    allowed_domains = ["360.cn"]
    start_urls = (
        'http://zhushou.360.cn/list/index/cid/1/',
        'http://zhushou.360.cn/list/index/cid/2/',
    )

    def get_text(self, response, rule, not_text=1):
        if not_text:
            try:
                s = response.xpath(rule).extract()
                if s:
                    return s[0].replace('\n', ' ').replace('\r', '').strip()
                return ''
            except Exception ,e:
                return ''
        else:
            try:
                rule = rule + ' | ' + rule + '//*[text()]'
                s = ''
                ns = response.xpath(rule)
                for n in ns:
                    ts = n.xpath('text()').extract()
                    for t in ts:
                        m = t.replace('\n', ' ').replace('\r', '').strip()
                        if m:
                            s = s + m + ';'
                return s
            except Exception:
                return ''

    def parse(self, response):
        type_list = response.xpath('//ul[@class="select"]/li[1]/a[position()>1]/@href').extract()
        categroy = response.xpath('//ul[@class="select"]/li[1]/a[position()>1]/text()').extract()
        j=0
        for i in type_list:
            print categroy[j] + '#' + i
            yield scrapy.Request('http://zhushou.360.cn/' + i, callback=self.parse_page_num,meta={'categroy': categroy[j]})
            j=j+1

    def parse_page_num(self, response):
        #page_num = response.xpath('//div[@id="pages_pg_2"]//div[@class="page_no"]/a[last()]/text()').extract()[0]
        page_num = 50
        categroy = response.meta['categroy']
        for i in xrange(page_num):
            yield scrapy.Request(response.url + '?page=%d' % (i+1), callback=self.parse_page, meta={'categroy': categroy})

    def parse_page(self, response):
        app_list = response.xpath('//ul[@class="iconList"]/li/a/@href').extract()
        categroy = response.meta['categroy']
        for i in app_list:
            yield scrapy.Request('http://zhushou.360.cn' + i, callback=self.parse_item, meta={'categroy': categroy})
    
    def parse_item(self, response):

        source = '360'

        name = self.get_text(response, '//h2[@id="app-name"]/span/text()')
        if not name:
            return

        version = self.get_text(response, '//div[@class="breif"]/div[@class="base-info"]/table/tbody/tr[2]/td[1]/text()')

        first = self.get_text(response, '//div[@class="nav"]/ul/li[@class="cur"]/a/text()')[1:]
        second = response.meta['categroy']
        category = first + '-' + second

        time = self.get_text(response, '//div[@class="breif"]/div[@class="base-info"]/table/tbody/tr[1]/td[2]/text()')

        size = self.get_text(response, '//div[@class="pf"]/span[@class="s-3"][2]/text()')

        system = self.get_text(response, '//div[@class="breif"]/div[@class="base-info"]/table/tbody/tr[2]/td[2]/text()')

        text = self.get_text(response, '//div[@class="breif"]',0)

        download = self.get_text(response, '//div[@class="pf"]/span[@class="s-3"][1]/text()')

        pingfen = self.get_text(response, '//div[@class="pf"]/span[@class="s-1 js-votepanel"]/text()')
        try:
            pingfen = str(float(pingfen)*10)
        except Exception:
            pingfen =''

        tag = response.xpath('//div[@class="app-tags"]//a/text()').extract()
        tags=','.join(tag)

        self.fileout.write(
            source + '\001' + name + '\001' + version + '\001' + category + '\001' + util.unify_data(time) + '\001' + size + '\001' + system + '\001' + text + '\001' + util.unify_download_count(download) + '\001' + pingfen + '\001' + tags
        )
        self.fileout.write('\n')