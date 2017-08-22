# -*- coding: utf-8 -*-
import logging
import scrapy
import sys
import os
import random
import re
from HHU.utils import AutoRecognize,GPA
from HHU import items
class HhuSpider(scrapy.Spider):
    name = "hhu"
    allowed_domains = ["202.119.113.135"]
    start_urls = ['http://202.119.113.135/validateCodeAction.do?random=0.657518063071526']


    def parse(self, response):
        image_path=sys.path[1]+"/HHU/image/verify.jpg"
        with open(image_path,'wb') as f:
            f.write(response.body)
        #获取验证码
        verify=AutoRecognize.AutoRecognize().get_verify()
        url='http://202.119.113.135/loginAction.do'
        formdata={'zjh':self.id,'mm':self.id,'v_yzm':verify}

        yield scrapy.FormRequest(url=url,formdata=formdata,callback=self.after_login)
    def after_login(self,response):
        #判断是否登录成功
        if len(response.xpath("//td[@class='errorTop']"))!=0:
            #登录失败
            #获取一个随机数
            random_link_param=random.random()
            random_link="http://202.119.113.135/validateCodeAction.do?random="+str(random_link_param)
            return scrapy.Request(random_link,dont_filter=True,callback=self.parse)
        #提取姓名等信息
        url="http://202.119.113.135/menu/top.jsp"
        return scrapy.Request(url,callback=self.get_name)
    def get_name(self,response):
        item=items.StudentItem()
        nameStr=response.xpath("//td[@nowrap]/text()").extract_first()
        name=re.compile(".*\((.*)\)").search(nameStr).group(1)
        item['name']=name
        print(name)
        #爬取成绩信息
        grade_url="http://202.119.113.135/bxqcjcxAction.do"
        yield scrapy.Request(url=grade_url,meta={'item_toGrade':item},callback=self.get_grades)
    def get_grades(self,response):
        grades=response.xpath("//td[@class='pageAlign']/table/thead/tr[position()>1]")
        item = response.meta['item_toGrade']
        grades_countGpa=[]
        for grade in grades:
            #课程名
            cource_name_str=grade.xpath("td[3]/text()").extract()[0]
            cource_name=cource_name_str.replace("\t","").replace("\n","").replace("\r","")
            #课程成绩
            cource_grade_str=grade.xpath("td[10]/text()").extract()[0]
            cource_grade=cource_grade_str.replace(' ','').replace("\t","").replace("\n","").replace("\r","")
            #课程名次
            cource_rank_str=grade.xpath("td[11]/text()").extract()[0]
            cource_rank=cource_rank_str.replace(' ','').replace("\t","").replace("\n","").replace("\r","")

            stu_item=items.StudentItem()
            stu_item['name']=item['name']
            stu_item['cource_name']=cource_name
            stu_item['cource_grade']=cource_grade
            stu_item['cource_rank']=cource_rank

            #为计算绩点做准备
            credit=grade.xpath("td[5]/text()").extract()[0].replace(' ','').replace("\t","").replace("\n","").replace("\r","")
            if grade.xpath("td[6]/text()").extract()[0].replace(' ','').replace("\t","").replace("\n","").replace("\r","")=='必修' and cource_grade!="":
                grades_countGpa.append({'score':cource_grade,'credit':float(credit)})

            yield stu_item
        #计算绩点
        gpa=GPA.CountGpa(grades_countGpa).count_Gpa()
        with open(sys.path[1]+"/HHU/result/"+item['name']+".txt",'a',encoding='utf-8') as f:
            f.write("绩点："+str(gpa))
