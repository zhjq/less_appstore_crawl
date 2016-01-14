# -*- coding:utf-8 -*-  
from __future__ import unicode_literals
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

import scrapy

import codecs

import util

class HaozhuoSpider(scrapy.Spider):
    name = "3310"
    fileout = codecs.open('3310.txt', 'a', 'utf-8')
    allowed_domains = ["3310.com"]
    start_urls = (
        'http://apk.3310.com/game/',
        'http://apk.3310.com/apps/',
    )
    
    def parse(self, response):
        cats = response.xpath('//div[@class="apply-menu"]/ul//li/a/@href').extract()
        for cat in cats:
            yield scrapy.Request(cat, callback = self.parse_page)

    def parse_page(self, response):
        app_list = response.xpath('//ul[@class="clearfix pictxt-a"]//li/a/@href').extract()
        for i in app_list:
            yield scrapy.Request(i, callback=self.parse_item)
        next = response.xpath('//a[@rel="next"]/@href').extract()
        if next:
            next_urls = response.url.split('/')
            next_urls[-1] = next[0]
            next_url = '/'.join(next_urls)
            yield scrapy.Request(next_url, callback=self.parse_page)
	
    def parse_item(self, response):

        source = '3310'

        name_version = util.get_text(response, '//div[@class="cont"]/h2/text()')
        if not name_version:
            return
        
        ns = name_version.split(' ')
        version = ns.pop(-1)
        name = ' '.join(ns)

        first = util.get_text(response, '//div[@class="guide"]/a[3]/text()')
        second = util.get_text(response, '//div[@class="guide"]/a[4]/text()')
        category = first + '-' + second

        time = util.get_text(response, '//div[@class="cont"]/p[2]/text()')[5:]

        size = util.get_text(response, '//div[@class="cont"]/p[1]/span/text()')[3:]

        system = util.get_text(response, '//div[@class="cont"]/p[3]/span/text()')[5:]

        text = util.get_text(response, '//div[@class="pictxt item"][not(@style)]',0)

        download = util.get_text(response, '//span[@id="downnum"]/text()')

        pingfen = util.get_text(response, '//div[@class="score"]/span/text()')
        try:
            pingfen = str(float(pingfen)*20)
        except Exception:
            pingfen =''

        tags=''

        self.fileout.write(
            source + '\001' + name + '\001' + version + '\001' + category + '\001' + util.unify_data(time) + '\001' + size + '\001' + system + '\001' + text + '\001' + util.unify_download_count(download) + '\001' + pingfen + '\001' + tags
        )
        self.fileout.write('\n')
