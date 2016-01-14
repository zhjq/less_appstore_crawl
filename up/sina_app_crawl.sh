#! /bin/sh

#########################################
#Author:shixi_jiqian
#Date:20160112
#Describe:每周一次app信息抓取
########################################

cd /data0/result/dw/zhjq/app

scrapy crawl 163
scrapy crawl 25pp
scrapy crawl 3310
scrapy crawl 360
scrapy crawl anzhi
scrapy crawl anzow
scrapy crawl apk91
scrapy crawl applestore
scrapy crawl baidu
scrapy crawl hiapk
scrapy crawl mumayi
scrapy crawl wandoujia
scrapy crawl xiaomi
scrapy crawl yingyongbao
scrapy crawl yingyonghui

python combine.py

d=`date "+%Y%m%d"`
lo="""/dw/tmp/tmp_sina_crawl_app_info/${d}"""
hive_sql="""alter table tmp_sina_crawl_app_info add if not exists partition(dt='${d}') location '${lo}';"""
echo $hive_sql
hive -S -e "${hive_sql}"

hadoop fs -put "total.txt" /dw/tmp/tmp_sina_crawl_app_info/${d}
#rm *.txt

