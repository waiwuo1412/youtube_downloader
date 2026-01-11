# !/usr/bin/env python
# -*- coding:utf-8 -*-

import concurrent.futures
import os
import logging
import yt_dlp

# --- 配置区域 ---
SAVE_PATH = 'downloads'  # 默认保存路径
THREAD_NUM = 5           # 线程数量
LOG_FILE = 'download_log.txt'
# 如果需要下载会员/限制级视频，请导出浏览器的cookies为txt文件并填入路径，否则留空
COOKIES_FILE = ''        # 例如: 'cookies.txt' 

# 设置日志
if not os.path.exists(SAVE_PATH):
    os.makedirs(SAVE_PATH)

logging.basicConfig(
    level=logging.INFO, # 建议平时用INFO，出错看ERROR
    filename=os.path.join(SAVE_PATH, LOG_FILE),
    filemode='a',
    format='%(asctime)s - %(threadName)s - %(levelname)s: %(message)s'
)

def get_ydl_opts(save_folder):
    """
    生成独立的配置选项，防止多线程冲突
    """
    opts = {
        # 格式：下载最佳视频+最佳音频，并自动合并为mp4。如果失败则回退到最佳单一文件。
        'format': 'bestvideo+bestaudio/best',
        'merge_output_format': 'mp4', 
        
        # 输出模板：保存路径/标题.扩展名
        'outtmpl': os.path.join(save_folder, '%(title)s.%(ext)s'),
        
        # 忽略错误，继续下一个
        'ignoreerrors': True,
        'no_warnings': True,
        'quiet': True, 
        
        # 重试次数
        'retries': 10,
        
        # 如果有cookies文件则加载
        'cookiefile': COOKIES_FILE if COOKIES_FILE else None,
        
        # 进度钩子
        'progress_hooks': [my_hook],
    }
    return opts

def my_hook(d):
    """下载进度回调"""
    if d['status'] == 'finished':
        print(f"[{d.get('info_dict', {}).get('title', 'Unknown')}] 下载完成，正在处理/合并...")

def download_single_url(url):
    """
    单个URL下载处理函数
    """
    if not url or not url.strip():
        return

    url = url.strip()
    print(f"开始处理: {url}")
    
    # 为每个线程创建独立的配置，解决竞争问题
    current_opts = get_ydl_opts(SAVE_PATH)

    try:
        with yt_dlp.YoutubeDL(current_opts) as ydl:
            # 提取信息但不下载，先检查标题等信息（可选）
            # info = ydl.extract_info(url, download=False)
            
            # 开始下载
            ydl.download([url])
            logging.info(f"成功下载: {url}")
            
    except yt_dlp.utils.DownloadError as e:
        error_msg = str(e)
        logging.error(f"下载失败 {url}: {error_msg}")
        print(f"❌ 下载出错: {url} - {error_msg}")
    except Exception as e:
        logging.exception(f"未知错误 {url}")
        print(f"❌ 未知错误: {url} - {e}")

def run_downloader(url_list):
    """
    多线程执行器
    """
    print(f"即将在 {THREAD_NUM} 个线程中处理 {len(url_list)} 个任务...")
    
    with concurrent.futures.ThreadPoolExecutor(max_workers=THREAD_NUM) as executor:
        # 使用 map 自动分配任务
        executor.map(download_single_url, url_list)
        
    print("所有任务处理完毕。")

if __name__ == '__main__':
    # --- 方式1：从文件读取URL列表 (推荐) ---
    input_file = 'urls.txt'
    target_urls = []
    
    if os.path.exists(input_file):
        with open(input_file, 'r', encoding='utf-8') as f:
            target_urls = [line.strip() for line in f if line.strip() and not line.startswith('#')]
    else:
        # --- 方式2：如果没有文件，可以使用硬编码列表测试 ---
        print(f"未找到 {input_file}，使用测试列表。")
        target_urls = [
            'https://www.youtube.com/watch?v=dQw4w9WgXcQ', # 测试链接
            # 'https://www.youtube.com/watch?v=XXXXXX',
        ]

    if target_urls:
        run_downloader(target_urls)
    else:
        print("没有需要下载的URL。请创建 urls.txt 文件，每行一个链接。")
