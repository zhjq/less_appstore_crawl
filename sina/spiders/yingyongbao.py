# -*- coding:utf-8 -*-  
from __future__ import unicode_literals
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

import scrapy

import codecs

import util

class YingyongbaoSpider(scrapy.Spider):
    name = "yingyongbao"
    allowed_domains = ["qq.com"]
    fileout = codecs.open('yingyongbao.txt', 'w', 'utf-8')
    start_urls = (
        'http://sj.qq.com/myapp/category.htm?orgame=1',
        'http://sj.qq.com/myapp/category.htm?orgame=2',

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
        urls = response.xpath('//ul[@data-modname="cates"]/li/a/@href').extract()
        for i in xrange(len(urls)-1):
            yield scrapy.Request('http://sj.qq.com/myapp/cate/appList.htm%s&pageSize=1000'%urls[i], callback=self.parse_page)

    def parse_page(self, response):
        import json
        body = response.body
        data = json.loads(body)

        for i in data['obj']:
            yield scrapy.Request('http://sj.qq.com/myapp/detail.htm?apkName=' + i["pkgName"], callback=self.parse_item, meta={'name':i["appName"],'version':i["versionName"],'category':i["categoryName"],'time':i["apkPublishTime"],'size':i["fileSize"],'appdown':i["appDownCount"],'pingfen':i["averageRating"]})  

    def parse_item(self, response):

        source = 'yingyongbao'

        name = response.meta['name']
        if not name:
            return

        version = response.meta['version']

        # first = response.meta['first']
        second = response.meta['category']
        category = response.meta['category']

        t = response.meta['time']
        import time
        try:
            st = time.strftime('%Y-%m-%d',time.localtime(t))
        except Exception:
            st = ''

        size = response.meta['size']
        size = str(size/1000000)+'M'

        system = ''

        text = self.get_text(response, '//div[@class="det-intro-text"]',0)

        download = str(response.meta['appdown'])

        pingfen = str(response.meta['pingfen'])

        tags=''

        self.fileout.write(
            source + '\001' + name + '\001' + version + '\001' + category + '\001' + st + '\001' + size + '\001' + system + '\001' + text + '\001' + util.unify_download_count(download) + '\001' + pingfen + '\001' + tags
        )
        self.fileout.write('\n')