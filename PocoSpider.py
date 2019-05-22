#!/usr/bin/python3
# -*- coding: UTF-8 -*-
'''
@project: Twisted学习
@name: PocoSpider
@date: 2019/5/21 14:09 
@author：arckal sun
@email: arckalsun@gmail.com
'''
import requests
import json
import os
import re
import time
from ImageHandler import ImgText
from bs4 import BeautifulSoup
from html import unescape

from requests.packages.urllib3.exceptions import InsecureRequestWarning

# 禁用安全请求警告
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

class PocoSpider(object):
    '''poco.cn 爬虫'''
    def __init__(self):
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.121 Safari/537.36",
            "Referer": "https://www.poco.cn/skill/detail?article_id=32672",
        }
        self.localImageDir = './poco/'

    def _parseWorksInfo(self,worksInfo):
        for works in worksInfo['list']:
            worksUrl = works['works_url']
            try:
                # print('加载：' + worksUrl)
                self.loadWorkDetail(worksUrl)
            except TypeError:
                pass
            except KeyError:
                pass

    def loadWorksListByType(self, classify_type=0, works_type='medal'):
        '''加载勋章作品
            classify_type:
                0
                1   人像
                2   风景
                3   生态
                4   纪实
                6   生活
                21  航拍
                22  手机摄影
                ...
            works_type:
                medal   勋章作品
                day     今日人气榜
                editor  编辑推荐
        '''
        url = "https://www.poco.cn/works/works_list?classify_type=%s&works_type=%s" % (classify_type,works_type)
        resp = requests.get(url, headers=self.headers, verify=False)
        # 解析
        soup = BeautifulSoup(resp.text, 'lxml')
        textarea = soup.find(name='textarea', attrs={"jsonname": "works_list_json"})
        worksInfo = json.loads(textarea.text)
        self._parseWorksInfo(worksInfo)

    def loadUserCenter(self, user_id: int):
        '''加载用户中心的博文列表'''
        url = "https://www.poco.cn/user/user_center?user_id=%s" % user_id
        resp = requests.get(url,headers=self.headers)
        # print(resp.text)
        # 解析
        soup = BeautifulSoup(resp.text,'lxml')
        articles = soup.find_all(name='div')
        # 第一页 最多20篇博文
        for a in articles[5:]:
            try:
                print(a.a['href'])
                self.loadWorkDetail(a.a['href'])
                # 解析博文
                # print(a.text)
            except TypeError:
                pass
            except KeyError:
                pass

    def loadWorkDetail(self, worksUrl):
        '''加载博文详情'''
        resp = requests.get(worksUrl, headers=self.headers,verify=False)
        # 解析
        soup = BeautifulSoup(resp.text, 'lxml')
        textarea = soup.find(name='textarea',attrs={"jsonname":"works_info"})
        worksInfo = json.loads(textarea.text)
        click_count = worksInfo.get('click_count')
        like_count = worksInfo.get('like_count')
        create_time = worksInfo.get('create_time')
        user_nickname = worksInfo.get('user_nickname')
        user_signature = worksInfo.get('user_signature')
        camera_brand_name = worksInfo.get('camera_brand_name')
        camera_model_name = worksInfo.get('camera_model_name')
        description = worksInfo.get('description')
        blogInfo = worksInfo.get('title')

        if worksInfo.get('works_blog_data'):
            media_info = worksInfo.get('works_blog_data')[0]['data'][0]['media_info']
            # 博文信息
            blogInfo = worksInfo.get('works_blog_data')[3]['data'][0]['content']
            blogInfo = unescape(blogInfo)
            blogInfo = unescape(blogInfo)
            blogInfo = re.sub(r'<[^>]+>', '', blogInfo)
        elif worksInfo.get('works_photo_data'):
            media_info = worksInfo.get('works_photo_data')[0]['media_info']
        else:
            print('解析失败: ' + worksUrl)
            return None

        ImageInfo = blogInfo + '\n'
        if description: ImageInfo += description + '\n'
        if click_count: ImageInfo += '浏览量: ' + str(click_count) + '\t'
        if like_count: ImageInfo += '点赞量: ' + str(like_count) + '\n'
        if user_nickname: ImageInfo += '作者: ' + user_nickname + '\t'
        if user_signature: ImageInfo += '签名: ' + user_signature + '\n'
        if camera_brand_name: ImageInfo += '设备: ' + camera_brand_name + '  ' + camera_model_name


        # randomStr = time.strftime("%Y%m%d%H%M%S", time.localtime())
        randomStr = ''
        # 图片信息
        imgFilename = media_info['file_name']
        imgHeight = media_info['height']
        imgWidth = media_info['width']
        imgUrl = media_info['file_url']
        imgUrl = 'http:' + imgUrl

        print(imgUrl)
        print(blogInfo)
        if (imgHeight>=1080 or imgWidth>=1441) and (imgHeight < 2000):
            if imgWidth >= imgHeight:
                self.downloadImage(imgUrl,imgFilename,imgInfo=ImageInfo)


    def downloadImage(self, imgUrl, filename,imgInfo=''):
        '''下载图片'''
        path = os.path.abspath(self.localImageDir)
        if not os.path.exists(path):
            os.mkdir(path)
        localFileName = os.path.join(path , filename + '.jpg')
        localBMPFileName = os.path.join(path , filename + '.bmp')
        img = requests.get(imgUrl).content
        with open(localFileName, 'wb') as f:
            f.write(img)
        # 转bmp, 加水印
        cvt = ImgText(localFileName,imgInfo,localBMPFileName)
        cvt.draw_text()
        try:
            os.remove(localFileName)
        except:
            pass
        return localBMPFileName

if __name__ == '__main__':
    spider = PocoSpider()
    # spider.loadUserCenter(200657070)
    spider.loadWorksListByType(21,'day')
