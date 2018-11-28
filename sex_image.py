import requests
from bs4 import BeautifulSoup
import os
import threading


web_url = "http://1200b.com"
same_url = "http://1200b.com/htm/Picture1/"
#list_url = "http://1200b.com/htm/Picture1/1.htm"

dir_name = '/data/seximage/toupaizipai'
a1 = os.path.exists(dir_name)
if not a1:
	os.makedirs(dir_name)
os.chdir(dir_name)
def download(pagenum):
    list_url=same_url+str(pagenum)+".htm"
    r=requests.get(list_url).text.encode("latin1").decode("UTF-8")
    bs=BeautifulSoup(r,'lxml')

    for link in bs.find_all('a'):
    	if 'Pic1' in link.get('href'):
    		list_url = web_url + link.get('href')
    		rb = requests.get(list_url).text.encode("latin1").decode("UTF-8")
    		soup2 = BeautifulSoup(rb, 'lxml').find_all('img')
    		for a in soup2:
    			img_name=a['alt']
    			img_url=a['src']
    			img = requests.get(img_url)
    			if not os.path.exists(img_name + '.jpg'):
    				print('正在下载'+':'+img_name)
    				f = open(img_name + '.jpg', 'ab')
    				f.write(img.content)
    				f.close()
    			else:
    				print(img_name+"已存在,跳过下载")
    				continue				                                   		                         

#多线程下载，多页
threads = []
for i in range(1,100):
	t = threading.Thread(target=download,args=str(i))
	threads.append(t)

for t in threads:
	t.start()

for t in threads:
	t.join()	
