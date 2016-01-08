# -*- coding:utf-8 -*-  
from __future__ import unicode_literals
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

import scrapy

import codecs

import util

class Apk91Spider(scrapy.Spider):
    name = "apk91"
    fileout = codecs.open('apk91.txt', 'a', 'utf-8')
    allowed_domains = ["91.com"]
    start_urls = (
        'http://apk.91.com/game/',
        'http://apk.91.com/soft/',
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
        cats = response.xpath('//ul[@class="cate_list nav-content"]//li/a/@href').extract()[1:]
        for cat in cats:
            yield scrapy.Request('http://apk.91.com'+cat, callback = self.parse_pages)

    def parse_pages(self, response):
        url = response.url
        for i in xrange(20):
            su = url.split('_')
            su[1]=str(i+1)
            url='_'.join(su)
            yield scrapy.Request(url, callback=self.parse_page)

    def parse_page(self, response):
        app_list = response.xpath('//div[@class="topic_before"]/a/@href').extract()
        cat = self.get_text(response, '//div[@class="l_box_title"]/h3/text()')
        for i in app_list:
            yield scrapy.Request('http://apk.91.com'+i, callback=self.parse_item, meta={'cat':cat})
	
    def parse_item(self, response):

        source = 'apk91'

        name = self.get_text(response, '//h1[@class="ff f20 fb fl"]/text()')
        if not name:
            return

        version = self.get_text(response, '//ul[@class="s_info"]/li[1]/text()')[3:]

        first = self.get_text(response, '//div[@class="crumb clearfix"]/a[2]/text()')
        second = response.meta['cat']
        category = first + '-' + second

        time = self.get_text(response, '//ul[@class="s_info"]/li[5]/text()')[5:15]

        size = self.get_text(response, '//ul[@class="s_info"]/li[3]/text()')[5:]

        system = self.get_text(response, '//ul[@class="s_info"]/li[4]/text()')[5:]

        text = self.get_text(response, '//div[@class="o-content"]',0)

        download = self.get_text(response, '//ul[@class="s_info"]/li[2]/text()')

        pingfen = self.get_text(response, '//div[@class="s_intro_pic fl"]/span[@class="spr star"]/a/@class')
        try:
            pingfen = str(float(pingfen.split('w')[1].split(' ')[0])*20)
        except Exception:
            pingfen =''

        tag = response.xpath('//ul[@class="s_info"]/li[10]/a/text()').extract()
        tags=','.join(tag)

        self.fileout.write(
            source + '\001' + name + '\001' + version + '\001' + category + '\001' + util.unify_data(time) + '\001' + size + '\001' + system + '\001' + text + '\001' + util.unify_download_count(download) + '\001' + pingfen + '\001' + tags
        )
        self.fileout.write('\n')
