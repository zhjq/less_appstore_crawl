  # -*- coding:utf-8 -*-  
from __future__ import unicode_literals
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

import scrapy

import codecs

import util

class AnzowSpider(scrapy.Spider):
    name = "anzow"
    fileout = codecs.open('anzow.txt', 'a', 'utf-8')
    allowed_domains = ["anzow.com"]
    start_urls = (
        'http://www.anzow.com/Software.shtml',
        'http://www.anzow.com/Game.shtml',
    )

    def parse(self, response):
        applist = response.xpath("//dl[@class='down_list pd20']")
        for app in applist:
            app_url = util.get_text(app, "./dd[@class='down_title']/h2/a/@href")
            time = util.get_text(app, "./dd[@class='down_attribute align_l']/span[3]/text()")
            system = util.get_text(app, "./dd[@class='down_attribute align_l']/span[5]/text()")
            download = util.get_text(app, "./dd[@class='down_attribute align_l']/span[7]/text()")
            yield scrapy.Request(app_url, callback = self.parse_item, meta = {"time":time,"system":system,"download":download})

        next = response.xpath('//a[text()="下一页"]/@href').extract()
        if next:
            yield scrapy.Request(next[0], callback = self.parse)
	
    def parse_item(self, response):

        source = 'anzow'

        name = util.get_text(response, "//dl[@class='down_info clear']/dd/div[1]/h1/text()")
        if not name:
            return

        version = ''

        first = util.get_text(response, "//div[@class='crumbs fl']/a[2]/text()")[-2:]
        second = util.get_text(response, "//div[@class='crumbs fl']/a[3]/text()")
        category = first + '-' + second

        time = response.meta['time']

        size = util.get_text(response, '//div[@class="xiazai1"][1]/../dl/dt/ul/li[3]/text()')

        system = response.meta['system']

        text = util.get_text(response, '//div[@class="down_intro"]',0)

        download = response.meta['download']

        pingfen = util.get_text(response, '//dl[@class="down_info clear"]/dd/dl/dt/ul/li[7]/strong/text()')
        try:
            pingfen = str(pingfen.count('★')*20)
        except Exception:
            pingfen =''

        tag = response.xpath('//p[@class="keywords"]//a/text()').extract()
        tags=','.join(tag)

        self.fileout.write(
            source + '\001' + name + '\001' + version + '\001' + category + '\001' + util.unify_data(time) + '\001' + size + '\001' + system + '\001' + text + '\001' + util.unify_download_count(download) + '\001' + pingfen + '\001' + tags
        )
        self.fileout.write('\n')