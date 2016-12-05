#-*-coding:utf-8-*-
import re
import os,sys
import random
from ich import html2ubb
from ich import DbHelper

user_list = [
(   2 , 'xhk               '),
(   3 , 'zhankc            '),
(   4 , 'hsgswxb123        '),
(   5 , 'yygy              '),
(   6 , 'ajdyvuduk         '),
(   7 , 'ham2000           '),
(   8 , 'zhujiang          '),
(   9 , 'pchwlp            '),
(  10 , 'xiaoaojhu         ')
]

def getThreadAuthor():
    count = len(user_list)
    i = random.randint(0,count-1)
    u = (user_list[i][0], user_list[i][1].strip())
    return u

def getPostAuthor(thread_author):
    count = len(user_list)
    i = random.randint(0,count-1)
    if thread_author == user_list[i][1]:
        return getPostAuthor(thread_author)
    
    u = (user_list[i][0], user_list[i][1].strip())
    return u
    
def getThread(thread, rand_author=True):
    nt = {}
    nt['subject']   = thread[0]
    
    if nt['subject'][:3] == '主题：':
        nt['subject'] = nt['subject'][3:]
    
    nt['post_list'] = []
    tauthor = getThreadAuthor()
    
    ta = thread[1][0]['author']
    for p in thread[1]:
        if len(p['time'])==0:
            continue
        if p['message'].find('用户已被锁定')!=-1:
            p['message'] = p['message'].replace('用户已被锁定', '支持楼主')
        if rand_author:
            if p['author'] == ta:
                p['author']   = tauthor[1]
                p['authorid'] = tauthor[0]
            else:
                pa = getPostAuthor(tauthor[1])
                p['author']   = pa[1]
                p['authorid'] = pa[0]
                
        p['message'] = html2ubb.embed2ubb(p['message'])
        p['message'] = html2ubb.html2ubb(p['message'])
        #print(p['message'])
        nt['post_list'].append(p)    
    return nt

user_list = []    

def useage():
    s = "post.py thread_dir begin_index count rand_author_flag(0 or 1)"
    print(s)
    
if __name__=='__main__':
    if len(sys.argv) !=5:
        useage()
        sys.exit()
        
    fp = open('userlist.txt' ,'r', encoding='utf8')
    c = fp.read()
    fp.close()
    #global user_list
    user_list = eval(c)
    
    dir = sys.argv[1]
    
    tl = os.listdir(dir)
    fl = []
    for t in tl:
        if t[-4:]!='.txt':
            continue
        fl.append(t)
    fl.sort()
    
    fp = open('db.txt' ,'r')
    c = fp.read()
    fp.close()
    
    db = eval(c)
    dh = DbHelper.DBHelper (db['server'], db['usr'], db['pwd'], db['dbname'], db['pre'])
    dh.connect()
    fid   = int(sys.argv[2])
    begin = int(sys.argv[3])
    count = len(fl)
    end   = int(sys.argv[4])
    rand_author = int(sys.argv[5])==1
    if end <=0 :
        end = count
    for i in range(begin-1, end):
        file = fl[i]
        print('{0}\t{1}'.format(i+1, file))
        fp = open( dir + '/'+file,'r', encoding='utf-8')
        c = fp.read()
        fp.close()
        thread = eval(c)
        nt = getThread(thread, rand_author)        
        dh.add_thread_posts(fid, nt['post_list'][0]['author'], nt['post_list'][0]['authorid'], nt['subject'], nt['post_list'])
        
    dh.updateforum(fid)
    