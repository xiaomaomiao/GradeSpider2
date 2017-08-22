# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class HhuItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass
class StudentItem(scrapy.Item):
    #学生姓名
    name=scrapy.Field()
    #学生课程名称
    cource_name=scrapy.Field()
    #学生课程成绩
    cource_grade=scrapy.Field()
    #学生课程在全院的名次
    cource_rank=scrapy.Field()
    #学生绩点
    gpa=scrapy.Field()

#class ImageItem(scrapy)