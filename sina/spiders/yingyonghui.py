# -*- coding:utf-8 -*-  
from __future__ import unicode_literals
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

import scrapy

import codecs

import util

class YingyonghuiSpider(scrapy.Spider):
    name = "yingyonghui"
    fileout = codecs.open('yingyonghui.txt', 'a', 'utf-8')
    allowed_domains = ["appchina.com"]
    start_urls = (
        'http://www.appchina.com/category/30.html',
        'http://www.appchina.com/category/40.html',
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
        cats = response.xpath('//div[@class="has-border classify"]/ul//li/a/@href').extract()[1:]
        for cat in cats:
            yield scrapy.Request('http://www.appchina.com'+cat, callback = self.parse_page)

    def parse_page(self, response):
        applist = response.xpath('//div[@class="app-info"]/h1[@class="app-name"]/a/@href').extract()
        for app in applist:
            yield scrapy.Request('http://www.appchina.com'+app, callback = self.parse_item)
        next = response.xpath('//a[@class="next"]/@href').extract()
        if len(next) != 0:
            yield scrapy.Request('http://www.appchina.com'+next[0], callback = self.parse_page)
	
    def parse_item(self, response):

        source = 'yingyonghui'

        name = self.get_text(response, '//h1[@class="app-name"]/text()')
        if not name:
            return

        version = self.get_text(response, '//div[@class="intro"]/p[1]/text()[2]')[3:]

        first = self.get_text(response, '//div[@class="breadcrumb centre-content"]/a[2]/text()')
        second = self.get_text(response, '//div[@class="breadcrumb centre-content"]/a[3]/text()')
        category = first + '-' + second

        time = self.get_text(response, '//div[@class="intro"]/p[1]/text()')[3:]

        size = self.get_text(response, '//span[@class="app-statistic"]/text()[2]')
        try:
            size = size.split('大小：')[1].split(' 更新')[0]
        except Exception:
            size = ''

        system = self.get_text(response, '//p[@class="art-content"][3]/text()[4]')[3:]

        text = self.get_text(response, '//div[@class="main-info"]/p[1]',0)

        download = self.get_text(response, '//span[@class="app-statistic"]/text()')
        try:
            download = download.split('下载')[0]
        except Exception:
            download = ''

        pingfen = ''

        tags=''

        self.fileout.write(
            source + '\001' + name + '\001' + version + '\001' + category + '\001' + util.unify_data(time) + '\001' + size + '\001' + system + '\001' + text + '\001' + util.unify_download_count(download) + '\001' + pingfen + '\001' + tags
        )
        self.fileout.write('\n')
