#!/usr/bin/python3
# -*- coding: UTF-8 -*-
'''
@project: Twisted学习
@name: run
@date: 2019/5/21 15:25 
@author：arckal sun
@email: arckalsun@gmail.com
'''
from PocoSpider import PocoSpider
import time
import os
import win32gui
import win32con
import threading

# 切换周期，单位 秒
SWITCH_TIME = 60*5

def run():
    # 轮播集合
    imgSet = set()
    spider = PocoSpider()
    while True:
        for filename in spider.run():
            if filename and filename not in imgSet:
                timeStr = time.strftime("%Y/%m/%d %H:%M:%S", time.localtime())
                print('[%s]切换下一张：%s' % (timeStr, filename))
                win32gui.SystemParametersInfo(win32con.SPI_SETDESKWALLPAPER, filename, 3)
                imgSet.add(filename)
                t = threading.Thread(target=input, args=('键入[回车]切换\n',))
                t.start()
                t.join(SWITCH_TIME)

        print('轮播结束，共轮播了%s张图片' % len(imgSet))
        time.sleep(60)
        print('开始新一轮')

if __name__ == '__main__':
    run()