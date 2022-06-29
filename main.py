# !/usr/bin/env python
# -*- coding:utf-8 -*-

' a youtube_downloader module '

__author__ = 'waiwuo 1412'

import concurrent
import os.path
import logging
import time
import os
import subprocess
import yt_dlp

TARGET = ''  # 设置url获取路径
PREFIX = 'https://www.youtube.com/watch?v='
SAVE_PATH = ''  # 设置保存路径
# 某些视频可能需要登录才可以查看 [选填]
USER_NAME = 'null'  # 设置youtube用户名
PASSWORD = 'null'  # 设置youtube密码
THREAD_NUM = 8  # 设置爬取的线程数量 [选填]

# 配置logging参数,部分参数列表在另一个py中,按需自取
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
    'quiet': True,  # 启动安静模式。如果与——verbose一起使用，则将日志打印到stderr
    'username': USER_NAME,
    'password': PASSWORD,
    'logger': MyLogger(),
    'retries': 50
    # 'postprocessors': [{
    #     'key': 'FFmpegExtractAudio',
    #     'preferredcodec': suffix,
    #     'preferredquality': '192',
    # }],
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
        # 三种youtube视频源丢失的报错
        if not 'unavailable' in str(e) and not 'Private' in str(e) and not 'terminated' in str(e):
            if mytype == 'video+audio':
                ret = subprocess.call(
                    'yt-dlp --format bestvideo+bestaudio ' + PREFIX + refer + ' -o ' + save_path + ' -R 50')
            else:
                ret = subprocess.call('yt-dlp --format best' + mytype + PREFIX + refer + ' -o ' + save_path + ' -R 50')
            if ret:
                logging.error('          ' + refer + '          ' + str(e))
                print(refer + ' ' + mytype + str(e))
                time.sleep(1)
        else:
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
    # 根据需要数据格式和需要自行修改
    with concurrent.futures.ThreadPoolExecutor(max_workers=THREAD_NUM) as executor:
        for id_item in os.listdir(TARGET):
            # 这里是根据从CelebVox2官网下载的文件的文件夹名,形如vox2_test_txt\txt\id03969\6iCOXUNN9Qc的形式,提取文件夹名6iCOXUNN9Qc生成url
            if os.path.isdir(TARGET + os.sep + id_item):
                URLS = [refer for refer in os.listdir(TARGET + os.sep + id_item)]
                executor.map(download, URLS)
