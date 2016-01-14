# -*- coding:utf-8 -*-  
from __future__ import unicode_literals
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

import scrapy

import codecs

import util

class WandoujiaSpider(scrapy.Spider):
    name = "wandoujia"
    fileout = codecs.open('wandoujia.txt', 'a', 'utf-8')
    allowed_domains = ["wandoujia.com"]
    start_urls = (
        'http://www.wandoujia.com/tag/app',
        'http://www.wandoujia.com/tag/game',
    )

    def parse(self, response):
        first = util.get_text(response, '//span[@class="last"]/text()')[2:4]
        cats = response.xpath('//ul[@class="clearfix tag-box"]//li/a/span/text()').extract()
        for cat in cats:
            yield scrapy.Request('http://apps.wandoujia.com/api/v1/apps?tag='+cat+'&max=60&start=0&opt_fields=apps.packageName', callback = self.parse_page, meta={'cat':cat,'first':first})

    def parse_page(self, response):
        headers = response.headers
        count = int(headers['apps-count'])
        cat = response.meta['cat']
        for i in xrange(count/60+1):
            yield scrapy.Request('http://apps.wandoujia.com/api/v1/apps?tag='+cat+'&max=60&start='+str(i*60)+'&opt_fields=apps.packageName', callback = self.parse_page2, meta={'first':response.meta['first']})

    def parse_page2(self,response):
        body = response.body[1:-1]
        import json
        info = json.loads(body)
        datas = info['apps']
        for data in datas:
            yield scrapy.Request('http://www.wandoujia.com/apps/'+str(data['packageName']), callback = self.parse_item, meta={'first':response.meta['first']})
	
    def parse_item(self, response):

        source = 'wandoujia'

        name = util.get_text(response, '//p[@class="app-name"]/span/text()')
        if not name:
            return

        version = util.get_text(response, '//dl[@class="infos-list"]/dd[4]/text()')

        first = response.meta['first']
        second = util.get_text(response, '//div[@class="crumb"]/div[2]/a/span/text()')
        category = first + '-' + second

        time = util.get_text(response, '//time[@id="baidu_time"]/text()')

        size = util.get_text(response, '//dl[@class="infos-list"]/dd[1]/text()')

        system = util.get_text(response, '//dl[@class="infos-list"]/dd[5]/text()')

        text = util.get_text(response, '//div[@itemprop="description"]',0)

        download = util.get_text(response, '//i[@itemprop="interactionCount"]/@content')

        pingfen = ''

        tag = response.xpath('//dd[@class="tag-box"]//a/text()').extract()
        tags=','.join([i.strip() for i in tag])

        self.fileout.write(
            source + '\001' + name + '\001' + version + '\001' + category + '\001' + util.unify_data(time) + '\001' + size + '\001' + system + '\001' + text + '\001' + util.unify_download_count(download) + '\001' + pingfen + '\001' + tags
        )
        self.fileout.write('\n')
