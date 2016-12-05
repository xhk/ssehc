#-*-coding:utf-8-*-
from pyquery import PyQuery as pq
import sys
import re
import os
import time

if __name__=='__main__':
    begin_page = int(sys.argv[1])
    end_page   = int(sys.argv[2])
    
    i = begin_page
    while i<= end_page:
        print(i)
        url = "http://www.dpxq.com/hldcg/search/list.asp?owner=m&page=%d" % (i)
        d = pq(url=url)
        
        fp = open('chess_manual_list/chess_manual_list_%03d.txt' % (i), 'w', encoding="utf8")
        fp.write('[')
        table = d('#st')
        trs = table('tr')
        count = len(trs)
        for j in range(4,count):
            tr = pq(trs[j])
            tds = tr('td')
            sortid = (pq(tds[0]).text())
            if sortid=='-':
                break
            title  = pq(tds[1]).text()
            click_count    = (pq(tds[2]).text())
            
            #print(sortid)
            if j!=4 :
                fp.write(',\n')
            fp.write("({0},'{1}', {2})".format(sortid, title, click_count))
            
            
        fp.write(']')
        fp.close()
        i = i + 1
        time.sleep(1)