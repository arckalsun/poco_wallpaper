#!/usr/bin/python3
# -*- coding: UTF-8 -*-
'''
@project: Twisted学习
@name: ImageHandler
@date: 2019/5/21 17:21 
@author：arckal sun
@email: arckalsun@gmail.com
'''
from PIL import Image,ImageFont,ImageDraw
import numpy as np

class ImgText:


    def __init__(self, img_path, img_text, img_savepath):
        self.img = Image.open(img_path).convert("RGBA")
        # 预设宽度 可以修改成你需要的图片宽度
        self.fillColor = (0, 0, 0)
        self.text_left = self.img.width // 4
        self.text_top = int(45 * (self.img.height/1080))
        self.text_width = self.img.width // 2
        self.font = ImageFont.truetype(r'C:\Windows\Fonts\STZHONGS.TTF',int(18*(self.img.height/1080)))
        # 文本
        self.text = img_text
        self.img_savepath = img_savepath
        # 段落 , 行数, 行高
        self.duanluo, self.note_height, self.line_height = self.split_text()

        # print('文本区位置(%s,%s) 文字大小%s' % (self.text_left,self.text_top,self.font.size))

    def get_duanluo(self, text):
        txt = Image.new('RGBA', (100, 100), (255, 255, 255, 0))
        draw = ImageDraw.Draw(txt)
        # 所有文字的段落
        duanluo = ""
        # 宽度总和
        sum_width = 0
        # 几行
        line_count = 1
        # 行高
        line_height = 1
        for char in text:
            width, height = draw.textsize(char, self.font)
            sum_width += width
            if sum_width > self.text_width:  # 超过预设宽度就修改段落 以及当前行数
                line_count += 1
                sum_width = 0
                duanluo += '\n'
            duanluo += char
            line_height = max(height*1.5, line_height)
        if not duanluo.endswith('\n'):
            duanluo += '\n'
        return duanluo, line_height, line_count

    def split_text(self):
        # 按规定宽度分组
        max_line_height, total_lines = 0, 0
        allText = []
        for text in self.text.split('\n'):
            duanluo, line_height, line_count = self.get_duanluo(text)
            max_line_height = max(line_height, max_line_height)
            total_lines += line_count
            allText.append((duanluo, line_count))
        line_height = max_line_height
        total_height = total_lines * line_height
        return allText, total_height, line_height

    def draw_text(self):
        """
        绘图以及文字
        :return:
        """
        self.detect_fillColor()
        draw = ImageDraw.Draw(self.img)
        # 左上角开始
        x, y = self.text_left, self.text_top
        for duanluo, line_count in self.duanluo:
            draw.text((x, y), duanluo, fill=self.fillColor, font=self.font)
            y += self.line_height * line_count
        self.img.save(self.img_savepath)

    def detect_fillColor(self):
        '''探测图片颜色值'''
        imgCrop = self.img.crop((self.text_left, self.text_top, self.text_width+self.text_left, self.img.height // 5))
        imgBin = imgCrop.convert("1")   # 图像二值化
        arr = np.array(imgBin)
        is_black = np.count_nonzero(arr) < arr.size/2
        if is_black:
            self.fillColor = (255,255,255)
        else:
            self.fillColor = (0, 0, 0)



if __name__ == '__main__':
    n = ImgText(r'D:\我的文档\python项目\Twisted学习\wallpaper\poco\file_1558486616158_3890.747240133973.bmp',
                "测试一下，就好了。" * 30, r'D:\我的文档\python项目\Twisted学习\wallpaper\poco\1_mark.bmp')
    n.draw_text()
    # n.detect_gray()
