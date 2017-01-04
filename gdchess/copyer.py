
from pyquery import PyQuery as pq
import re
import gather
import sys,os
sys.path.insert(0, '../ich')
import DbHelper

new_thread_list_url = 'http://www.gdchess.com/bbs/index.asp?boardid=1'
watch_record_file  = 'watch_record.txt'

forum_mapping = {
    42:36,
    4:39,
    40:2,
    30:38,
    2:36,
    50:36,
    57:38,
    56:42,
    6:2,
    41:37,
    51:37,
    15:42,
    49:42,
    43:2
}

class Copyer:
    def __init__(self):
        fp = open('update_list.txt', 'r')
        self.update_list = {}
        c = fp.read()
        if len(c)>0:
            self.update_list = eval(c)
        fp.close()

        fp = open('db.txt' ,'r')
        c = fp.read()
        fp.close()
    
        db = eval(c)
        self.dh = DbHelper.DBHelper (db['server'], db['usr'], db['pwd'], db['dbname'], db['pre'])
    
    def save(self):
        fp = open('update_list.txt', 'w')
        if fp :
            fp.write(str(self.update_list))
            fp.close()
        
    
    def __del__(self):
        pass
        
    def need_update(self, boardid, postid):
        r = self.update_list.get(boardid)
        if r==None:
            return True
        
        return r < postid
        

    def update(self, boardid, postid, url):
        url = 'http://www.gdchess.com/bbs/dispbbs.asp?boardid={0}&ID={1}'.format(boardid, postid) 
        print(url)
        subject,plist = gather.get_thread_post(url)
        fid = forum_mapping[boardid]
        author = '名侦探下棋'
        self.dh.add_thread_posts(fid, author, 124, subject, plist)
        self.dh.updateforum(fid)
        
        self.update_list[boardid] = postid
    
    
    def run(self):
        d = pq(url=new_thread_list_url)
        new_thread_links = d('a.blue')
        for link in new_thread_links:
            link = pq(link)
            url  = link.attr('href')
            p = re.compile(r'boardid=(\d+)[^\b]*ID=(\d+)')
            m = re.search(p, url)
            boardid = int(m.group(1))
            postid  = int(m.group(2))
            if self.need_update(boardid, postid):
                self.update(boardid, postid, url)
    
if __name__ == '__main__':
    c = Copyer()
    c.run()
    c.save()
    
        
        
        
    