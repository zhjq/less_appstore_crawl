# -*- coding:utf-8 -*-  
from __future__ import unicode_literals
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

import scrapy

import codecs

import util

class BaiduSpider(scrapy.Spider):
    name = "baidu"
    fileout = codecs.open('baidu.txt', 'a', 'utf-8')
    allowed_domains = ["baidu.com"]
    start_urls = ['http://shouji.baidu.com/software/item?docid='+str(i) for i in range(10000000)]

    def parse(self, response):

        source = 'baidu'

        name = util.get_text(response, '//span[@class="gray"]/text()')
        if not name:
            return

        version = util.get_text(response, '//span[@class="version"]/text()')[3:]

        first = util.get_text(response, '//div[@class="nav"]//a/text()')
        second = util.get_text(response, '//div[@class="nav"]/span[3]/a/text()')
        category = first + '-' + second

        time = ''

        size = util.get_text(response, '//span[@class="size"]/text()')[3:]

        system = ''

        text = util.get_text(response, '//div[@class="brief-long"]/p', 0)

        download = util.get_text(response, '//span[@class="download-num"]/text()')[5:]

        pingfen = util.get_text(response, '//span[@class="star-percent"]/@style')
        try:
            pingfen = pingfen.split(':')[1].split('%')[0]
        except Exception:
            pingfen =''

        tags = ''

        self.fileout.write(
            source + '\001' + name + '\001' + version + '\001' + category + '\001' + util.unify_data(time) + '\001' + size + '\001' + system + '\001' + text + '\001' + util.unify_download_count(download) + '\001' + pingfen + '\001' + tags
        )
        self.fileout.write('\n')
