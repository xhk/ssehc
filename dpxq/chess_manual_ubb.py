#-*-coding:utf-8-*-
from pyquery import PyQuery as pq
import sys
import re
import os
import time
import urllib

def get_chess_manual(id):
    url = "http://www.dpxq.com/hldcg/search/view.asp?owner=m&id={0}".format(id)
    d = None
    while True:
        try:
            d = pq(url=url)
            break
        except urllib.error.URLError as e:
            print(e)
            time.sleep(10)
        
        
        
    dhtmlxq   = re.search(r"\[DhtmlXQ\][^\b]*\[\/DhtmlXQ\]", d.html(), re.I)
    dhtmlxq   = dhtmlxq.group(0)
    #dhtmlxq   = dhtmlxq.replace("\\\\", "\\")
    move_list = re.search(r"\'\[DhtmlXQ_movelist\]([^\b]*)\[\/DhtmlXQ_movelist\]", d.html(), re.I)
    move_list = move_list.group(1)
    cm = {}
    tags = [
       "ver",
        "init",
        "pver",
        "viewurl",
        "adddate",
        "editdate",
        "title",
        "binit",
        "movelist",
        "firstnum",
        "length",
        "type",
        "gametype",
        "open",
        "class",
        "event",
        "group",
        "round",
        "table",
        "date",
        "place",
        "timerule",
        "red",
        "redteam",
        "redname",
        "redlevel",
        "redeng",
        "redrating",
        "redtime",
        "black",
        "blackteam",
        "blackname",
        "blacklevel",
        "blackeng",
        "blackrating",
        "blacktime",
        "result",
        "endtype",
        "judge",
        "record",
        "remark",
        "author",
        "refer",
        "other",
        "hits",
        "price",
        "sortid",
        "owner",
        "oldowner",
        "hidden" 
    ]
    for tag in tags:
        cm[tag] = re.search(r"\[DhtmlXQ_"+tag+"\]([^\b]*)\[\/DhtmlXQ_"+tag+"\]", dhtmlxq, re.I).group(1)
        cm[tag] = cm[tag].encode("utf8").decode('unicode-escape')
        #print()
    cm['movelist'] = move_list
    cm['dpid'] = id
    fp = open("chess_manual/{0}.txt".format(id), "w", encoding="utf8")  
    fp.write(str(cm))
    fp.close()
    
    
if __name__=='__main__':
    #get_chess_manual(76262)
    
    begin_page = int(sys.argv[1])
    end_page   = int(sys.argv[2])
    i = begin_page
    while i<= end_page:
        file = 'chess_manual_list/chess_manual_list_%03d.txt' % (i);
        print(file)
        fp = open( file,'r', encoding="utf8")
        c = fp.read()
        cmlist = eval(c)
        fp.close()
        for p in cmlist:
            print(p[0])
            get_chess_manual(p[0])
            time.sleep(1)
        i = i + 1
    