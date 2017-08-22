# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import sys
class HhuPipeline(object):
    def process_item(self, item, spider):
        return item
class  PrintStuGrade(object):
    def process_item(self, item, spider):
        len_ts=20-len(item['cource_name'])
        ts=''
        for i in range(0,len_ts):
            ts+="-"
        with open(sys.path[1]+"/HHU/result/"+item['name']+".txt",'a',encoding='utf-8') as f:
            f.write(item['cource_name']+ts+"成绩:"+item['cource_grade']+ts+"名次"+item['cource_rank']+"\n")
        print(item['name'],item['cource_name'],item['cource_grade'],item['cource_rank'])
        return item