#-*-coding:utf-8-*-
import re
import os

url ='http://www.gdchess.com/bbs/index.asp?boardid=4'
base_url = 'http://www.gdchess.com/bbs/'

from pyquery import PyQuery as pq

def get_page_thread_list(page_url,fp):
    d = pq(url=page_url)
    tr_list = d('tr[onmouseover="this.className=\'tron\'"]')
    for tr in tr_list:
        tr = pq(tr)
        if tr('td.list1 a img').attr('src').find('top') != -1:
            continue
        
        link = tr('td.list2 a:first') 
        title = link.text()
        url = link.attr('href')
        try:
            print(title)
            print(url)
            fp.write(str((title,base_url+url)))
            fp.write(',\n')
        except UnicodeEncodeError:
            continue
        
        
def get_thread_list(forum_url, fp):
    d = pq(url=forum_url)
    last_page = d('a.page:last')
    pageCountStr = last_page.text().replace('.','')
    pageCount = int (pageCountStr)
    pageCount = 110
    thread_url = base_url + last_page.attr('href')
    i = pageCount
    while i>0:
        print('========第%d页======='%(i))
        url = thread_url.replace('Page='+pageCountStr,'Page='+str(i))
        get_page_thread_list(url, fp)
        i = i -1
 
if __name__ == '__main__' :
    #get_page_thread_list('http://www.gdchess.com/bbs/index.asp?boardid=4&TopicMode=0&List_Type=&Page=228')
    fp = open('thread_url.txt', 'a', encoding='utf-8')
    get_thread_list('http://www.gdchess.com/bbs/index.asp?boardid=4', fp)
    fp.close()
    