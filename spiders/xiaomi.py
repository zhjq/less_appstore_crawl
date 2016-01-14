# -*- coding:utf-8 -*-  
from __future__ import unicode_literals
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

import scrapy

import codecs

import util

class XiaomiSpider(scrapy.Spider):
    name = "xiaomi"
    fileout = codecs.open('xiaomi.txt', 'a', 'utf-8')
    allowed_domains = ["mi.com"]
    start_urls = (
        'http://app.mi.com',
    )

    def parse(self, response):
        soft_cats = response.xpath('//ul[@class="category-list"][1]//li/a/@href').extract()
        for cat in soft_cats:
            yield scrapy.Request('http://app.mi.com/categotyAllListApi?page=0&categoryId='+cat.split('/')[-1]+'&pageSize=1', callback = self.parse_page, meta={'cat':cat,'first':'软件'})
        game_cats = response.xpath('//ul[@class="category-list"][2]//li/a/@href').extract()
        for cat in soft_cats:
            yield scrapy.Request('http://app.mi.com/categotyAllListApi?page=0&categoryId='+cat.split('/')[-1]+'&pageSize=1', callback = self.parse_page, meta={'cat':cat,'first':'游戏'})

    def parse_page(self, response):
        body = response.body
        cat = response.meta['cat']
        import json
        count = json.loads(body)['count']
        yield scrapy.Request('http://app.mi.com/categotyAllListApi?page=0&categoryId='+cat+'&pageSize='+str(count), callback = self.parse_page2, meta={'first':response.meta['first']})

    def parse_page2(self,response):
        body = response.body
        import json
        info = json.loads(body)
        datas = info['data']
        for data in datas:
            yield scrapy.Request('http://app.mi.com/detail/'+str(data['appId']), callback = self.parse_item, meta={'first':response.meta['first']})
	
    def parse_item(self, response):

        source = 'xiaomi'

        name = util.get_text(response, '//div[@class="intro-titles"]/h3/text()')
        if not name:
            return

        version = util.get_text(response, '//ul[@class=" cf"]/li[4]/text()')

        first = response.meta['first']
        second = util.get_text(response, '//div[@class="bread-crumb"]/ul/li[2]/a/text()')
        category = first + '-' + second

        time = util.get_text(response, '//ul[@class=" cf"]/li[6]/text()')

        size = util.get_text(response, '//ul[@class=" cf"]/li[2]/text()')

        system = ''

        text = util.get_text(response, '//p[@class="pslide"]',0)

        download = ''

        pingfen = util.get_text(response, '//div[@class="star1-empty"]/div/@class')
        try:
            pingfen = str(float(pingfen.split('star1-hover star1-')[1])*10)
        except Exception:
            pingfen =''

        tags=''

        self.fileout.write(
            source + '\001' + name + '\001' + version + '\001' + category + '\001' + util.unify_data(time) + '\001' + size + '\001' + system + '\001' + text + '\001' + util.unify_download_count(download) + '\001' + pingfen + '\001' + tags
        )
        self.fileout.write('\n')
