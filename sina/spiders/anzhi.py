# -*- coding:utf-8 -*-  
from __future__ import unicode_literals
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

import scrapy

import codecs

import util

class AnzhiSpider(scrapy.Spider):
    name = "anzhi"
    fileout = codecs.open('anzhi.txt', 'a', 'utf-8')
    allowed_domains = ["anzhi.com"]
    start_urls = (
        'http://www.anzhi.com/sort_67_1_hot.html',
        'http://www.anzhi.com/sort_82_1_hot.html',
        'http://www.anzhi.com/sort_84_1_hot.html',
        'http://www.anzhi.com/sort_39_1_hot.html',
        'http://www.anzhi.com/sort_40_1_hot.html',
        'http://www.anzhi.com/sort_41_1_hot.html',
        'http://www.anzhi.com/sort_42_1_hot.html',
        'http://www.anzhi.com/sort_43_1_hot.html',
        'http://www.anzhi.com/sort_44_1_hot.html',
        'http://www.anzhi.com/sort_45_1_hot.html',
        'http://www.anzhi.com/sort_46_1_hot.html',
        'http://www.anzhi.com/sort_47_1_hot.html',
        'http://www.anzhi.com/sort_48_1_hot.html',
        'http://www.anzhi.com/sort_49_1_hot.html',
        'http://www.anzhi.com/sort_50_1_hot.html',
        'http://www.anzhi.com/sort_51_1_hot.html',
        'http://www.anzhi.com/sort_52_1_hot.html',
        'http://www.anzhi.com/sort_53_1_hot.html',
        'http://www.anzhi.com/sort_54_1_hot.html',
        'http://www.anzhi.com/sort_55_1_hot.html',
        'http://www.anzhi.com/sort_21_1_hot.html',
        'http://www.anzhi.com/sort_69_1_hot.html',
        'http://www.anzhi.com/sort_14_1_hot.html',
        'http://www.anzhi.com/sort_15_1_hot.html',
        'http://www.anzhi.com/sort_16_1_hot.html',
        'http://www.anzhi.com/sort_19_1_hot.html',
        'http://www.anzhi.com/sort_20_1_hot.html',
        'http://www.anzhi.com/sort_24_1_hot.html',
        'http://www.anzhi.com/sort_56_1_hot.html',
        'http://www.anzhi.com/sort_57_1_hot.html',
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
        cate = self.get_text(response, '//li[@class="current"]/a/text()')[2:]
        app_list = response.xpath('//div[@class="app_list border_three"]//div[@class="app_info"]//a/@href').extract()
        for i in app_list:
            yield scrapy.Request('http://www.anzhi.com' + i, callback=self.parse_item, meta={'cate':cate})

        next = response.xpath('//div[@class="pagebars"]//a[@class="next"]/@href').extract()
        if next:
            yield scrapy.Request('http://www.anzhi.com' + next[0], callback=self.parse)

	
    def parse_item(self, response):

        source = 'anzhi'

        name = self.get_text(response, '//div[@class="detail_line"]/h3//text()')
        if not name:
            return

        version = self.get_text(response, '//div[@class="detail_line"]/span//text()')[1:-1]

        first = response.meta['cate']

        data = response.xpath('//ul[@id="detail_line_ul"]/li//text()').extract()
        if len(data) == 7 :
            second = data[0][3:]
            download = data[1][3:]
            time = data[2][3:]
            size = data[3][3:]
            system = data[4][3:]

        if len(data) == 6 :
            second = data[0][3:]
            download = ''
            time = data[1][3:]
            size = data[2][3:]
            system = data[3][3:]

        category = first + '-' + second

        text = self.get_text(response, '//div[@class="app_detail_infor"]',0)

        pingfen = self.get_text(response, '//div[@id="stars_detail"]/@style')
        p = pingfen.split('-')
        if len(p) == 2:
            pingfen = '0.0'
        elif len(p) == 3:
            pingfen = p[2][:-3]
        try:
            pingfen = str(float(pingfen)/15*10)
        except Exception:
            pingfen =''

        tags=''

        self.fileout.write(
            source + '\001' + name + '\001' + version + '\001' + category + '\001' + util.unify_data(time) + '\001' + size + '\001' + system + '\001' + text + '\001' + util.unify_download_count(download) + '\001' + pingfen + '\001' + tags
        )
        self.fileout.write('\n')
