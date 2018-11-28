#!/usr/bin/python3
import requests
from bs4 import BeautifulSoup
import os

same_url='http://ww585.com/html/part/index'
dir_name ='/usr/local/nginx/html'
print('图片存放目录' + dir_name)
a1 = os.path.exists(dir_name)
if not a1:
  os.makedirs(dir_name)
os.chdir(dir_name)
def download (weburl,type_dir):
    r = requests.get(weburl)
    soup = BeautifulSoup(r.text, 'lxml')
    for link in soup.find_all('a'):
        if 'article' in link.get('href'):
            list_url = 'http://ww585.com' + link.get('href')
            # print(list_url)
            rb = requests.get(list_url).text.encode("latin1").decode("gbk")
            soup2 = BeautifulSoup(rb, 'lxml').find_all('img')
            img_dirname = BeautifulSoup(rb, 'lxml').find('div', class_='title').get_text()
            # print (img_dirname)
            # 创建目录
            print('开始下载： ' + type_dir+'/'+img_dirname)

            a = os.path.exists(type_dir+'/'+img_dirname)
            if not a:
                os.makedirs(type_dir+'/'+img_dirname)
            else:
                print("已存在，跳过下载，如需重新下载，请手动删除此目录")
                continue
            os.chdir(type_dir+'/'+img_dirname)
            for a in soup2:
                img_url = a['src']
                img_name = img_url[-15:-4]
                img = requests.get(img_url)
                f = open(img_name + '.jpg', 'ab')
                f.write(img.content)
                print(img_name, '图片已保存:' + dir_name + '\\' + img_dirname)
                f.close()
            print(img_dirname + '下载完毕')
            os.chdir(dir_name)

for i in range(16,23):
    typeurl=same_url+str(i)+'.html'
    print(typeurl)
    download(typeurl,str(i))
    r=requests.get(typeurl).text.encode("latin1").decode("gbk")
    bs=BeautifulSoup(r,'lxml').find('span').get_text()
    max_page=bs[-3:-1]
    for m in range(2,int(max_page)+1):
        weburl=same_url+str(i)+'_'+str(m)+'.html'
        print(weburl)
        download(weburl, str(i))
