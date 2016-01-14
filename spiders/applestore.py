# -*- coding:utf-8 -*-  
from __future__ import unicode_literals
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

import scrapy

import codecs

import util

class AppleSpider(scrapy.Spider):
    name = "applestore"
    fileout = codecs.open('applestore.txt', 'a', 'utf-8')
    allowed_domains = ["apple.com"]
    start_urls = (
        'https://itunes.apple.com/cn/genre/ios-tu-shu/id6018?mt=8',
    )

    def parse(self, response):
        type_list = response.xpath('//div[@id="genre-nav"]//ul[@class="list column first"]/li/a/@href').extract()
        j=1
        for i in type_list:
            yield scrapy.Request(i, callback=self.parse_app)
            print 'deal is ' + str(j)
            j=j+1

    def parse_app(self, response):
        nav_list = response.xpath('//div[@class="grid3-column"]//li/a/@href').extract()
        print 'one nav:' + str(len(nav_list))
        for i in nav_list:
            yield scrapy.Request( i, callback=self.parse_item)

    def parse_item(self, response):

        source = 'applestore'

        name = util.get_text(response, '//div[@id="desktopContentBlockId"]//div[@id="title"]//h1/text()')
        if not name:
            return

        version = util.get_text(response, '//div[@id="left-stack"]//span[@itemprop="softwareVersion"]/text()')

        first = '软件'
        second = util.get_text(response, '//div[@id="left-stack"]//span[@itemprop="applicationCategory"]/text()')
        category = first + '-' + second

        time = util.get_text(response, '//div[@id="left-stack"]//span[@itemprop="datePublished"]/text()')

        size = ''

        system = util.get_text(response, '//div[@id="left-stack"]//span[@itemprop="operatingSystem"]/text()')

        text = util.get_text(response, '//div[@class="center-stack"]/div[@class="product-review"]/p',0)

        download = util.get_text(response, '//div[@class="extra-list customer-ratings"]/div[4]/span/text()')

        pingfen = util.get_text(response, '//div[@class="extra-list customer-ratings"]/div[4]/@aria-label')
        try:
            pingfen = str(float(pingfen.split('星, ')[0])*20)
        except Exception:
            pingfen =''

        tags=''

        self.fileout.write(
            source + '\001' + name + '\001' + version + '\001' + category + '\001' + util.unify_data(time) + '\001' + size + '\001' + system + '\001' + text + '\001' + util.unify_download_count(download) + '\001' + pingfen + '\001' + tags
        )
        self.fileout.write('\n')