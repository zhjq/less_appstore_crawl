# -*- coding:utf-8 -*-  
from __future__ import unicode_literals
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

import scrapy

import codecs

import util

class HiapkSpider(scrapy.Spider):
    name = "hiapk"
    fileout = codecs.open('hiapk.txt', 'a', 'utf-8')
    allowed_domains = ["hiapk.com"]
    start_urls = (
        'http://apk.hiapk.com/apps',
        'http://apk.hiapk.com/games',
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
        cats = response.xpath('//ul[@id="cateListUl"]//li/a/@href').extract() 
        for cat in cats:
            yield scrapy.Request('http://apk.hiapk.com'+cat, callback = self.parse_page)

    def parse_page(self, response):
        applist = response.xpath('//span[@class="list_title font14_2"]/a/@href').extract()
        for app in applist:
            yield scrapy.Request('http://apk.hiapk.com'+app, callback = self.parse_item)

        next = response.xpath('//span[@class="page_item page_next page_able"]/../@href').extract()
        if next:
            yield scrapy.Request('http://apk.hiapk.com'+next[0], callback = self.parse_page)
	
    def parse_item(self, response):

        source = 'hiapk'

        name_and_version = self.get_text(response, "//div[@id='appSoftName']/text()")
        try:
            version = name_and_version.split('(')[1].split(')')[0]
            name = name_and_version.split('(')[0]
        except Exception:
            version = ''
            name = name_and_version
        if not name:
            return

        first = self.get_text(response, "//a[@id='categoryParent']/text()")
        second = self.get_text(response, "//a[@id='categoryLink']/text()")
        category = first + '-' + second

        time = self.get_text(response, '//div[@class="code_box_border"]/div[@class="line_content"][7]/span[2]/text()')

        size = self.get_text(response, '//span[@id="appSize"]/text()')

        system = self.get_text(response, '//span[@class="font14 detailMiniSdk d_gj_line left"]/text()')

        text = self.get_text(response, '//pre[@id="softIntroduce"]',0)

        download = self.get_text(response, '//div[@class="code_box_border"]/div[@class="line_content"][2]/span[2]/text()')

        pingfen = self.get_text(response, '//div[@id="appIconTips"]/div[1]/@class')
        try:
            pingfen = str(float(pingfen.split(" ")[2].split("_")[2])*2)
        except Exception:
            pingfen =''

        tags=''

        self.fileout.write(
            source + '\001' + name + '\001' + version + '\001' + category + '\001' + util.unify_data(time) + '\001' + size + '\001' + system + '\001' + text + '\001' + util.unify_download_count(download) + '\001' + pingfen + '\001' + tags
        )
        self.fileout.write('\n')