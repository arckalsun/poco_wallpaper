# poco_wallpaper
poco.cn壁纸程序

### 爬取最新精选图片，自动设为壁纸
代码简单，具体使用方式请看代码注释

## 安装
```shell
pip install -r requirements.txt
```
其他依赖：win32gui,win32con请下载安装包手动安装

## 运行
```
# 运行poco爬虫
python run.py
```
或
```shell
# 运行Bing爬虫
python StealBing.py
```

- 目前仅支持Windows操作系统，Linux系统请自行修改代码使用
- 可以手动修改桌面背景图片契合度，Windows 10 的契合度有：填充，适应，
拉伸，平铺，居中，跨区。