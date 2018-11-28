import requests
from bs4 import BeautifulSoup
import os
import threading
# url = 'http://a.66d.club'

same_url = 'http://1200b.com/'
url = 'http://1200b.com/htm/Video1/'
rq = requests.get(url).text.encode('latin1').decode('utf-8')
bs = BeautifulSoup(rq, 'lxml').find('div', class_='box dy_list').find_all('a')
video_save_path = '/data/video/tmp/'

if not os.path.exists(video_save_path):
    os.makedirs(video_save_path)
os.chdir(video_save_path)

threads = []

# 下载方法
def download(videourl, num):
    video_url = videourl+'/video'+str(num)+'.ts'
    video_name = str(num)+'.ts'
    print('开始下载：', dir_name+video_name)
    video = requests.get(video_url)
    f = open(video_name, 'wb')
    f.write(video.content)
    f.close()
    print(dir_name+video_name, '下载完成')


for i in range(0, len(bs)):
    video_name = bs[i]['title']
    # 替换链接
    video_url = same_url+bs[i]['href'].replace('vod', 'vodplay')
    # print(video_name, video_url.replace('vod','vodplay'))
    rq = requests.get(video_url).text.encode('latin1').decode('utf-8')
    # 获取到视频m3u8文件的URL，开始获取视频片段最大数值
    video_m3u8 = rq[rq.find('video:[[\'') +9:rq.find('0],]') - 8]
   
    # 判断视频分段数位数并取出
    if requests.get(video_m3u8).content[-22:-19].isdigit():
        max_num = requests.get(video_m3u8).content[-22:-19]
    elif requests.get(video_m3u8).content[-21:-19].isdigit(): 
        max_num = requests.get(video_m3u8).content[-21:-19]
    else:
        max_num = requests.get(video_m3u8).content[-20:-19]
    # 找到视频下载链接，并取出相同部分
    video_m3u8_sameurl = video_m3u8[:video_m3u8.find('video')]
    # print(video_name, video_m3u8_sameurl, rq_m3u8_max_num)
    # 单线程
    if not os.path.exists(video_name):
        os.makedirs(video_name)
        os.chdir(video_name)
        for i in range(1, int(max_num) + 1):
            t = threading.Thread(target=download, args=(video_m3u8_sameurl, i))
            threads.append(t)
        for t in threads:
            t.start()
    else:
        continue
    

    os.chdir(video_save_path)
