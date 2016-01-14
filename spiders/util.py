# -*- coding:utf-8 -*-  
from __future__ import unicode_literals
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

def get_text(response, rule, not_text=1):
    if not_text:
        try:
            s = response.xpath(rule).extract()
            if s:
                return s[0].replace('\n', ' ').replace('\r', '').replace('\u2028','').replace('\u2029','').strip()
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
                    m = t.replace('\n', ' ').replace('\r', '').replace('\u2028','').replace('\u2029','').strip()
                    if m:
                        s = s + m + ';'
            return s
        except Exception:
            return ''

#统一日期格式
def unify_data(data_str):
    data_str = data_str.replace("年","-")
    data_str = data_str.replace("月","-")
    data_str = data_str.replace(".","-")
    data_str = data_str.replace("/","-")
    if not '-' in data_str:
        return ''
    data_str = filter(lambda ch:ch in '0123456789-',data_str)
    return data_str

#统一下载次数
def unify_download_count(download_count_str):
    download_count_str = filter(lambda ch:ch in '.0123456789-十百千万亿',download_count_str)
    t=0
    a = download_count_str.split("-")
    try:
        for s in a:
            if "千万" in s:
                t=t+float(s.split("千万")[0])*10000000
            elif "百万" in s:
                t=t+float(s.split("百万")[0])*1000000
            elif "十万" in s:
                t=t+float(s.split("百万")[0])*100000
            elif "万" in s:
                t=t+float(s.split("万")[0])*10000
            elif "千" in s:
                t=t+float(s.split("千")[0])*1000
            elif "百" in s:
                t=t+float(s.split("百")[0])*100
            elif "亿" in s:
                t=t+float(s.split("亿")[0])*100000000
            else:
                t=t+float(s)
        return str(int(t/len(a)))
    except Exception:
        return ''
