#!/usr/bin/python3
# -*- coding: UTF-8 -*-
'''
@project: 桌面壁纸
@name: StealBing
@date: 2019/5/21 11:13 
@author：arckal sun
@email: arckalsun@gmail.com
'''
import re
import sys
import os
import time
import requests
import win32gui
import win32api
import win32con
from PIL import Image


class StealBing(object):

    def __init__(self, bingUrl="http://cn.bing.com"):
        self.bingUrl = bingUrl
        self.content = requests.get(bingUrl).content
        self.bgImageUrl = ''
        self.localFileName = ''
        self.localBMPFileName = ''
        self.localImageDir = './img/'

    def parseImageUrl(self):

        patten = r'id="bgLink" rel="preload" href="(.*?jpg)"?'
        data = self.content.decode()


        imgurls = re.findall(patten,data,re.S)
        if imgurls:
            imgurl = self.bingUrl+imgurls[0]
            self.bgImageUrl = imgurl
        else:
            sys.exit('Not found image!')

    def createLocalFileName(self):
        path = os.path.abspath(self.localImageDir)
        if not os.path.exists(path):
            os.mkdir(path)
        randomStr = time.strftime("%Y%m%d", time.localtime())
        self.localFileName = path + randomStr + '.jpg'
        self.localBMPFileName = path + randomStr + '.bmp'

    def downloadImage(self):
        if self.bgImageUrl == '':
            self.parseImageUrl()

        if self.localFileName == '':
            self.createLocalFileName()

        img = requests.get(self.bgImageUrl).content
        with open(self.localFileName,'wb') as f:
            f.write(img)

    def updateBGImage(self):
        img = Image.open(self.localFileName)
        img.save(self.localBMPFileName)
        os.remove(self.localFileName)
        # k = win32api.RegOpenKeyEx(win32con.HKEY_CURRENT_USER, "Control Panel\\Desktop", 0, win32con.KEY_SET_VALUE)
        # win32api.RegSetValueEx(k, "WallpaperStyle", 0, win32con.REG_SZ, "2")  # 2拉伸适应桌面,0桌面居中
        # win32api.RegSetValueEx(k, "TileWallpaper", 0, win32con.REG_SZ, "0")
        win32gui.SystemParametersInfo(win32con.SPI_SETDESKWALLPAPER, self.localBMPFileName, 1 + 2)

if __name__ == '__main__':
    stealBing = StealBing()
    stealBing.downloadImage()
    stealBing.updateBGImage()