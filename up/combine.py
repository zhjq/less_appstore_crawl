# -*- coding:utf-8 -*-  
from __future__ import unicode_literals
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

import codecs
import glob

def main():
    file_list = ['baidu.txt', 'yingyonghui.txt', 'apk91.txt', '3310.txt', 'hiapk.txt', 'mumayi.txt', 'applestore.txt', 'yingyongbao.txt', '360.txt', 'anzhi.txt', 'wandoujia.txt', 'xiaomi.txt', '25pp.txt', 'anzow.txt', '163.txt']
    for f in file_list:
        merge(f)
    combine(file_list)

def merge(file):
    print 'merge', file
    apps = {}
    with codecs.open(file, encoding='utf-8') as f:
        for line in f:
            app = line.split('\001')
            source = app[0]
            name = app[1]
            version = app[2].strip()
            category = app[3]
            time = app[4]
            size = app[5]
            system = app[6]
            text = app[7]
            try:
                download = app[8]
            except Exception:
                print file
                print line
                print app
                print len(app)
                sys.exit(-1)
            pingfen = app[9]
            tags = app[10]  
            if name in apps:
                if version > apps[name]['version']:
                    apps[name] = {
                        'source': source,
                        'name': name,
                        'version': version,
                        'category': category,
                        'time': time,
                        'size': size,
                        'system': system,
                        'text': text,
                        'download': download,
                        'pingfen': pingfen,
                        'tags': tags
                        }
            else:
                apps[name] = {
                    'source': source,
                    'name': name,
                    'version': version,
                    'category': category,
                    'time': time,
                    'size': size,
                    'system': system,
                    'text': text,
                    'download': download,
                    'pingfen': pingfen,
                    'tags': tags
                    }
    with codecs.open(file, 'w', encoding='utf-8') as f:
        for i in apps:
            line = apps[i]['source'] + '\001' + \
                    apps[i]['name'] + '\001' + \
                    apps[i]['version'] + '\001' + \
                    apps[i]['category'] + '\001' + \
                    apps[i]['time'] + '\001' + \
                    apps[i]['size'] + '\001' + \
                    apps[i]['system'] + '\001' + \
                    apps[i]['text'] + '\001' + \
                    apps[i]['download'] + '\001' + \
                    apps[i]['pingfen'] + '\001' + \
                    apps[i]['tags']
            f.writelines(line)
    print 'merge',file,' end'

def combine(file_list):
    apps = {}
    for file in file_list:
    	print 'start read', file
        with codecs.open(file,encoding='utf-8') as f:
            for line in f:
                app = line.split('\001')
                name = app[1]
                version = app[2]
                category = app[3]
                time = app[4]
                size = app[5]
                system = app[6]
                text = app[7]
                download = app[8]
                pingfen = app[9]
                tags = app[10]
                if name in apps:
                    if version>apps[name]['version']:
                        apps[name]['version'] = version
                        apps[name]['size'] = size
                        apps[name]['system'] = system
                        apps[name]['time'] = time
                    if len(tags)>len(apps[name]['tags']):
                        apps[name]['tags'] = tags
                    if len(text)>len(apps[name]['text']):
                        apps[name]['text'] = text
                    try:
                        if download != '':
                            if apps[name]['download'] == '':
                                apps[name]['download'] = download
                            else:
                                if int(download)>int(apps[name]['download']):
                                    apps[name]['download'] = download
                        if pingfen != '':
                            if apps[name]['pingfen'] == '':
                                apps[name]['pingfen'] = pingfen
                            else:
                                if float(pingfen)>float(apps[name]['pingfen']):
                                    apps[name]['pingfen'] = pingfen
                    except Exception:
                        print line
                        print app
                        print len(app)
                        import sys
                        sys.exit(-1)
                else:
                    apps[name]={'name':name,'version':version,'category':category,'time':time,'size':size,'system':system,'text':text,'download':download,'pingfen':pingfen,'tags':tags}
    print 'start write total.txt'
    with codecs.open('total.txt','w',encoding='utf-8') as f:
        for i in apps:
            line =  apps[i]['name'] + '\001' + \
                    apps[i]['version'] + '\001' + \
                    apps[i]['category'] + '\001' + \
                    apps[i]['time'] + '\001' + \
                    apps[i]['size'] + '\001' + \
                    apps[i]['system'] + '\001' + \
                    apps[i]['text'] + '\001' + \
                    apps[i]['download'] + '\001' + \
                    apps[i]['pingfen'] + '\001' + \
                    apps[i]['tags']
            f.writelines(line)

if __name__ == '__main__':
	main()