#-*-coding:utf-8-*-
from pyquery import PyQuery as pq
import urllib
import sys
import urllib.request
import urllib.error  
#import ImgHelper
import time
import random
import os

def download_img(url, refurl):
    b = url.rfind('/')
    b = url.rfind("/", 0, b)
    e = url.rfind('.')
    #pre = ''.join(random.sample(['z','y','x','w','v','u','t','s','r','q','p','o','n','m','l','k','j','i','h','g','f','e','d','c','b','a'], 5)).replace(' ','')
    #file_name = 'www.ichinachess.com\\0001\\' + pre + url[b+1:]
    # 用路径做名字，如果再重复，就认为是同意给文件喽
    file_name = 'www.ichinachess.com\\0001\\' + url[b+1:].replace('/','_')
    if os.path.exists(file_name):
        print('文件{0}已存在，不用下载'.format(file_name))
        return file_name.replace('\\', '/')
    #print(file_name)
    #print(url)
    req = urllib.request.Request(url)
    #req.add_header('Accept', 'image/webp,image/*,*/*;q=0.8')
    #req.add_header('Accept-Encoding', 'gzip, deflate, sdch ')
    #req.add_header('Accept-Language', 'zh-CN,zh;q=0.8')
    #req.add_header('Cache-Control', 'max-age=0')
    #req.add_header('Connection', 'keep-alive')
    #req.add_header('Referer', refurl)
    req.add_header('User_Agent','Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.143 Safari/537.36')
    #req.add_header('Cookie','DvForum+8%2E3%5Fwww%2Egdchess%2Ecom=StatUserID=18322899361; ASPSESSIONIDQSSCTDSD=LAIFIIMDNPOOOBLBCNFKAFMC; geturl=%2Fbbs%2Fdispbbs%2Easp%3Fboardid%3D4%26Id%3D1288%26page%3D228; AJSTAT_ok_pages=1; AJSTAT_ok_times=7; Hm_lvt_8fe8cb7fb43af70e7e0c775fde7984af=1478524893,1478529392,1478776827,1479009635; Hm_lpvt_8fe8cb7fb43af70e7e0c775fde7984af=1479028162; jiathis_rdc=%7B%22http%3A//www.gdchess.com/bbs/dispbbs.asp%3Fboardid%3D4%26Id%3D101666%22%3A1%7C1479009641606%2C%22http%3A//www.gdchess.com/bbs/dispbbs.asp%3Fboardid%3D4%26Id%3D1288%26page%3D228%22%3A%220%7C1479028162336%22%7D')
    #rsp = urllib.request.urlopen(req)
    
    rsp = None
    for i in range(1):
        time.sleep(1)
        print('第{0}尝试'.format(i+1))
        try:
            rsp = urllib.request.urlopen(req)
            break
        except Exception as e:
            print(e)
            continue
            
    # 不行就用原来的喽
    if rsp == None :
        return url
        
    f = open(file_name,'wb')  
    f.write(rsp.read())  
    f.close()  
    ih = ImgHelper.ImgHelper()
    ih.watermarkfull(file_name, file_name, 'ichinachess_big_wm.png', 'ichinachess_small_wm.png', 0.2)
    return  file_name.replace('\\', '/')
    

# 获取帖子列表
def get_thread_list():
    pass
# 获取帖子内容
def get_thread_post(url):
    d = None
    try_count = 0
    while d == None:
        try_count = try_count+1
        try:
            d = pq(url=url)
        except urllib.error.HTTPError as e:
            print('第{0}次尝试{1}'.format(try_count, url) )
            time.sleep(5)
    subject = d('table.topic h1').text()
    #print(subject)
    plist = []
    
    
    post_list = d('table.bbslist')
    for post in post_list:
        post = pq(post)        
        
        postinfo = {'author':'','time':'', 'message':''}
        postinfo['author'] = post('tr:first td:first').text()
        postinfo['time']   = post('td.usermenu span').text()
        
        # 时间:2014-1-9 22:21:00 [ 只看作者 ] 本帖ID：394724'
        pos = postinfo['time'].find(' [')
        postinfo['time'] = postinfo['time'][3:pos]

        newd = post('td.inforight')
        # 修改框架路径
        iframe_list = newd('iframe')
        if len(iframe_list)>0:
            for iframe in iframe_list:
                iframe = pq(iframe)
                if iframe.attr('src').lower().find('dhtmlxq')!=-1:
                    #iframe.attr('src','/DhtmlXQ_www_ichinachess_com/DhtmlXQ_ichinachess_com.htm')
                    # 将name拿出处理下
                    n = iframe.attr('name')
                    n = n.replace("NoFile_[DhtmlXQiFrame]","[DhtmlXQ]")
                    n = n.replace("gdchess","ichinachess")
                    n = n.replace("dpxq", "ichinachess")
                    n = n.replace("东萍公司", "华夏棋坛")
                    n = n.replace("东萍", "华夏棋坛")
                    # 将棋盘替换到ichinachess的上面的
                    # 用一个自电影的标签，在html2ubb的时候，标签会自动被删除
                    iframe.replaceWith('<will_be_deleted>'+n+'</will_be_deleted>')
        # 移除js
        newd('script').remove()
        
        # 下载图片，并修改图片路径
        #img_list = newd('img')
        #for img in img_list:
        #    img = pq(img)
        #    if img.attr('src') == None:
        #        continue
        #    img_url = 'http://www.gdchess.com/bbs/' + img.attr('src')
        #    file_path = download_img(img_url, url)
        #    img.attr('src', file_path)
        
        postinfo['message'] = str(newd)
        # 单引号替换掉，方便插入sql
        postinfo['message']  = postinfo['message'] .replace("'", "\'")
        subject = subject.replace("'","\'")
        plist.append(postinfo)
    return subject,plist
            
if __name__ == '__main__':
    #get_thread_post('http://www.gdchess.com/bbs/dispbbs.asp?boardid=30&ID=124882&page=1')
    # 测试下载图片
    #download_img('http://www.gdchess.com/bbs/UploadFile/2016-11/2016111013530952497.jpg', '')
    #download_img('http://pic2.sc.chinaz.com/files/pic/pic9/201309/apic520.jpg')
    #download_img('http://www.gdchess.com/bbs/images/emot/em07.gif', 'http://www.gdchess.com/bbs/dispbbs.asp?boardid=4&Id=1288&page=228')
    
    # iframe 测试
    #r = get_thread_post('http://gdchess.com/bbs/dispbbs.asp?boardid=4&Id=101988')
    #print(r)
    
    fp = open('thread_url.txt', 'r', encoding='utf-8')
    c = fp.read()
    fp.close()
    url_list = eval(c)
    count = len(url_list)
    for i in range(count):
        print('{0} {1}'.format(i+1,url_list[i]))
        r = get_thread_post(url_list[i][1])
        fp = open('thread\\%s_%05d.txt' %(sys.argv[1],i), 'w', encoding='utf-8')
        fp.write(str(r))
        fp.close()
        time.sleep(2)

     
        