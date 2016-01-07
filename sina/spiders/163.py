# -*- coding:utf-8 -*-  
from __future__ import unicode_literals
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

import scrapy

import codecs

import util

class WangyiSpider(scrapy.Spider):
    name = "163"
    fileout = codecs.open('163.txt', 'a', 'utf-8')
    allowed_domains = ["163.com"]
    start_urls = (
        'http://m.163.com/android/category/allapp/index.html',
        'http://m.163.com/android/game/allgame/index.html',
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
        applist = response.xpath('//p[@class="f-s3 t-overflow"]/a/@href').extract()
        for app in applist:
            yield scrapy.Request('http://m.163.com'+app, callback = self.parse_item)

        next = self.get_text(response, '//a[text()="下一页"]/@href')
        if next != '#next':
            yield scrapy.Request('http://m.163.com'+next, callback = self.parse)

	
    def parse_item(self, response):

        source = '163'

        name = self.get_text(response, '//span[@class="f-h1"]/text()')
        if not name:
            return

        version = self.get_text(response, '//table[@class="table-appinfo"]/tr[3]/td/text()')

        first = self.get_text(response, "//div[@class='sect']/div[@class='crumb']/a[2]/text()")[-2:]
        second = self.get_text(response, "//div[@class='sect']/div[@class='crumb']/a[3]/text()")
        category = first + '-' + second

        time = ''

        size = self.get_text(response, '//table[@class="table-appinfo"]/tr[2]/td[1]/text()')

        system = ''

        text = self.get_text(response, '//div[@id="app-desc"]',0)

        download = self.get_text(response, '//span[@class="vote-text-s"]/text()')[1:-1]

        pingfen = self.get_text(response, '//span[@class="vote-column-s"]/i/@style')
        try:
            pingfen = pingfen.split(':')[1].split('%')[0]
        except Exception:
            pingfen =''

        tags = ''

        self.fileout.write(
            source + '\001' + name + '\001' + version + '\001' + category + '\001' + util.unify_data(time) + '\001' + size + '\001' + system + '\001' + text + '\001' + util.unify_download_count(download) + '\001' + pingfen + '\001' + tags
        )
        self.fileout.write('\n')