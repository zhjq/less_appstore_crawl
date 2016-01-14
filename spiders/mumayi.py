# -*- coding:utf-8 -*-  
from __future__ import unicode_literals
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

import scrapy

import codecs

import util

class MumayiSpider(scrapy.Spider):
    name = "mumayi"
    fileout = codecs.open('mumayi.txt', 'a', 'utf-8')
    allowed_domains = ["mumayi.com"]
    start_urls = (
        'http://www.mumayi.com/update/',
    )

    def parse(self, response):
        import datetime

        for i in ['http://www.mumayi.com/update/'+(datetime.datetime.now()-datetime.timedelta(hours=i*24)).strftime("%Y-%m-%d")+'-1.html' for i in range((datetime.datetime.now()-datetime.datetime(2010,5,6,0,0,0)).days)]:
            yield scrapy.Request(i, callback = self.parse_page)

    def parse_page(self, response):
        time = response.url.split('update/')[1].split('.html')[0][:-2]
        apps = response.xpath('//ul[@class="listapp"]/li/a/@href').extract()
        for app in apps:
            yield scrapy.Request(app, callback = self.parse_item, meta={'time':time})
        next = response.xpath('//a[text()="下一页"]/@href').extract()
        if next:
            yield scrapy.Request(next[0], callback = self.parse)
	
    def parse_item(self, response):

        source = 'mumayi'

        name_version = util.get_text(response, '//h1[@class="iappname hidden fl"]/text()')
        if not name_version:
            return
        sn = name_version.split('V')
        version = sn.pop(-1) if len(sn)>1 else ''
        name = 'V'.join(sn) if sn else name_version

        first = util.get_text(response, '//div[@id="classlists"]/a[2]/text()')[:2]
        second = util.get_text(response, '//div[@id="classlists"]/a[3]/text()')
        category = first + '-' + second

        time = response.meta['time']

        size = util.get_text(response, '//span[text()="程序大小："]/../text()')

        system = util.get_text(response, '//div[@class="sel_text fl"]/text()')

        text = util.get_text(response, '//ul[@class="author"]/..//p[position()<last()]',0)

        download = ''

        pingfen = util.get_text(response, '//div[@id="starlist"]/@class')
        try:
            pingfen = str(float(pingfen.split('now')[1])*2)
        except Exception:
            pingfen =''

        tags = ''

        self.fileout.write(
            source + '\001' + name + '\001' + version + '\001' + category + '\001' + util.unify_data(time) + '\001' + size + '\001' + system + '\001' + text + '\001' + util.unify_download_count(download) + '\001' + pingfen + '\001' + tags
        )
        self.fileout.write('\n')
