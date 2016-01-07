# -*- coding:utf-8 -*-  
from __future__ import unicode_literals
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

import scrapy

import codecs

import util

class PpSpider(scrapy.Spider):
    name = "25pp"
    fileout = codecs.open('25pp.txt', 'a', 'utf-8')
    allowed_domains = ["25pp.com"]
    start_urls = (
        'http://android.25pp.com/software/',
        'http://android.25pp.com/game/',
        'http://android.25pp.com/software/1001_0_0_1.html',
        'http://android.25pp.com/software/1002_0_0_1.html',
        'http://android.25pp.com/software/1003_0_0_1.html',
        'http://android.25pp.com/software/1004_0_0_1.html',
        'http://android.25pp.com/software/1005_0_0_1.html',
        'http://android.25pp.com/software/1006_0_0_1.html',
        'http://android.25pp.com/software/1007_0_0_1.html',
        'http://android.25pp.com/software/1008_0_0_1.html',
        'http://android.25pp.com/game/2001_0_0_1.html',
        'http://android.25pp.com/game/2002_0_0_1.html',
        'http://android.25pp.com/game/2003_0_0_1.html',
        'http://android.25pp.com/game/2004_0_0_1.html',
        'http://android.25pp.com/game/2005_0_0_1.html',
        'http://android.25pp.com/game/2006_0_0_1.html',
        'http://android.25pp.com/game/2007_0_0_1.html',
        'http://android.25pp.com/game/2008_0_0_1.html',
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
        at = response.xpath('//dl[@id="toggle"]/dt/a/@href').extract()[0]
        yield scrapy.Request(at, callback = self.parse_page)
        tags = response.xpath('//dl[@id="toggle"]//dd/a/@href').extract()
        for tag in tags:
            yield scrapy.Request(tag, callback = self.parse_page)

    def parse_page(self, response):
        app_list = response.xpath('//a[@class="h4_a"]/@href').extract()
        for i in app_list:
            yield scrapy.Request(i, callback=self.parse_item)
        next = response.xpath('//a[@class="nextpage"]/@href').extract()
        if next and next != response.url:
            yield scrapy.Request(next[0], callback=self.parse_page)
	
    def parse_item(self, response):

        source = '25pp'

        name = self.get_text(response, '//div[@class="title-stat"]/div[@class="txt"]/h1/text()')
        if not name:
            return

        version = self.get_text(response, '//div[@class="title-stat"]/div[@class="txt"]/ul/li[1]/text()')[3:]

        first = self.get_text(response, '//div[@class="location"]/a[2]/text()')
        second = self.get_text(response, '//div[@class="title-stat"]/div[@class="txt"]/ul/li[2]/text()')
        category = first + '-' + second

        time = ''

        size = self.get_text(response, '//div[@class="title-stat"]/div[@class="txt"]/ul/li[3]/text()')[3:]

        system = self.get_text(response, '//div[@class="title-stat"]/div[@class="txt"]/ul/li[5]/text()')[5:]

        text = self.get_text(response, '//div[@class="conTxt"][1]',0)

        download = self.get_text(response, '//li[@class="borderR"]/span/text()')

        pingfen = self.get_text(response, '//div[@class="downMunber"]/ul/li[3]/span/text()')
        try:
            pingfen = str(float(pingfen)*20)
        except Exception:
            pingfen =''

        tag = response.xpath('//li[@class="w-450"]//a/text()').extract()
        tags=','.join(tag)

        self.fileout.write(
            source + '\001' + name + '\001' + version + '\001' + category + '\001' + util.unify_data(time) + '\001' + size + '\001' + system + '\001' + text + '\001' + util.unify_download_count(download) + '\001' + pingfen + '\001' + tags
        )
        self.fileout.write('\n')
