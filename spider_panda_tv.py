#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date  : 2018/11/1 16:52
# @Author: PythonVampire
# @email : vampire@ivamp.cn
# @File  : spider_panda_tv.py
import re
from urllib import request


class Spider:
    url = 'https://www.panda.tv/cate/lol'
    root_pattern = '<div class="video-info">(.*?)</div>'
    name_pattern = '<span class="video-nickname" title="(.*?)">'
    number_pattern = '<span class="video-number">(.*?)</span>'

    def go(self):
        html = self.__fetch_content()  # 获取数据
        anchors = self.__analysis(html)  # 分析数据
        anchors = list(self.__refine(anchors))  # 精简数据
        anchors = self.__sort(anchors)  # 对观看人数排序
        self.__show(anchors)  # 打印结果
        print('Spider End')

    @staticmethod
    def __fetch_content():
        r = request.urlopen(Spider.url)
        html = r.read()
        html = str(html, encoding='utf-8')
        return html
        # with open('panda_tv.html', 'w') as f:
        #     f.write(str(html))

    @staticmethod
    def __analysis(html):
        root_html = re.findall(Spider.root_pattern, html, re.S)

        anchors = []
        for item in root_html:
            name = re.findall(Spider.name_pattern, item, re.S)
            number = re.findall(Spider.number_pattern, item, re.S)
            anchor = {'name': name, 'number': number}
            anchors.append(anchor)
        # for item in anchors:  # 循环打印主播
        #     print(item)
        return anchors

    @staticmethod
    def __refine(anchors):  # 精炼数据
        return map(lambda anchor: {'name': anchor['name'][0], 'number': anchor['number'][0]}, anchors)

    def __sort(self, anchors):
        anchors = sorted(anchors, key=self.__sort_seed, reverse=True)
        return anchors

    @staticmethod
    def __sort_seed(anchor):
        r = re.findall('\d*', anchor['number'])
        number = float(r[0])
        if '万' in anchor['number']:
            number *= 10000
        return number

    @staticmethod
    def __show(anchors):
        for rank in range(len(anchors)):
            print('rank ' + str(rank + 1)
                  + ':   ' + anchors[rank]['name']
                  + '       ' + anchors[rank]['number'])


spider = Spider()
spider.go()
