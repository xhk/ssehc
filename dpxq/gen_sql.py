import os

def strtime2timestamp(self,s):
    t = None
    pos = s.find('时间:')
    if  pos != -1:
        s = s[pos+3:]
    try:
        t = time.strptime(s, '%Y-%m-%d %H:%M:%S')
    except ValueError as e:
        t = time.strptime(s, '%Y-%m-%d')
    
    return int (time.mktime(t))

def gen_sql(m):
    

if __name__ == '__main__':
    dir = sys.argv[1]
    tl = os.listdir(dir)
    sql = "insert into ich_chess_manual(ver,init,pver,viewurl,adddate,editdate,title,binit,movelist,firstnum,length,type,gametype,open,class,event,group,round,table,date,place,timerule,red,redteam,redname,redlevel,redeng,redrating,redtime,black,blackteam,blackname,blacklevel,blackeng,blackrating,blacktime,result,endtype,judge,record,remark,author,refer,other,hits,price,sortid,owner,oldowner,hidden) values"
    for t in tl:
        if t[-4:]!='.txt':
            continue
        fp = open(dir+"/"+t, "r", encoding="utf8")
        c =  fp.fread()
        fp.close()
        m = eval(c)