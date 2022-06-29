# !/usr/bin/env python
# -*- coding:utf-8 -*-

' a *** module '

__author__ = 'Shiqiang Lin'

import concurrent
import os.path
import logging
import time
import os
import subprocess
import yt_dlp

TARGET = ''  # 设置url获取路径
PREFIX = ''
SAVE_PATH = ''  # 设置保存路径
# 某些视频可能需要登录才可以查看
USER_NAME = ''  # 输入youtube用户名
PASSWORD = ''  # 输入youtube密码
THREAD_NUM = 8  # 设置爬取的线程数量

# 配置logging参数
logging.basicConfig(level=logging.ERROR,
                    filename=SAVE_PATH + os.sep + 'log.txt',
                    filemode='a',
                    format='%(asctime)s - %(filename)s[line:%(lineno)d] - %(levelname)s: %(message)s')


def my_hook(d):
    if d['status'] == 'finished':
        print('Done downloading, now converting ... ')
        time.sleep(1)
    if d['status'] == 'downloading':
        print('downloading...')


class MyLogger(object):
    def debug(self, msg):
        pass

    def warning(self, msg):
        pass

    def error(self, msg):
        # print(msg)
        time.sleep(1)


ydl_opts = {
    'quiet': True,
    'username': USER_NAME,
    'password': PASSWORD,
    'logger': MyLogger(),
    'retries': 50
}


def type_download(refer, mytype):
    print('refer:' + refer + ' ' + mytype + ' start download')
    save_path = os.path.join(SAVE_PATH, mytype)
    if mytype == 'video+audio':
        ydl_opts['format'] = 'bestvideo+bestaudio'
    else:
        ydl_opts['format'] = 'best' + mytype
    ydl_opts['outtmpl'] = save_path + os.path.sep + '%(title)s.%(ext)s'

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            print('downloading...')
            ydl.download([PREFIX + refer])
    except yt_dlp.utils.DownloadError as e:
        if not 'unavailable' in str(e) and not 'Private' in str(e) and not 'terminated' in str(e):
            if mytype == 'video+audio':
                subprocess.call('yt-dlp --format bestvideo+bestaudio ' + PREFIX + refer + ' -o ' + save_path + ' -R 50')
            else:
                subprocess.call('yt-dlp --format best' + mytype + PREFIX + refer + ' -o ' + save_path + ' -R 50')
        logging.error('          ' + refer + '          ' + str(e))
        print(refer + ' ' + mytype + str(e))
        time.sleep(1)
    else:
        time.sleep(1)
        print(refer + ' ' + mytype + ' done')


def download(refer):
    type_download(refer, 'video')
    type_download(refer, 'audio')
    # type_download(refer,'video+audio')


if __name__ == '__main__':
    with concurrent.futures.ThreadPoolExecutor(max_workers=THREAD_NUM) as executor:
        for id_item in os.listdir(TARGET):
            if os.path.isdir(TARGET + os.sep + id_item):
                URLS = [refer for refer in os.listdir(TARGET + os.sep + id_item)]
                executor.map(download, URLS)