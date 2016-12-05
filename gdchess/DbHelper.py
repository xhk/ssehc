#-*-coding:utf-8-*-
import MySQLdb
import time

class DBHelper:
    def __init__(self,host,user,pwd,db,table_prefix):
        self.host = host
        self.user = user
        self.pwd = pwd
        self.db = db
        self.conn = None
        self.table_prefix = table_prefix # 表名前缀
        self.cur = None
    def __del__(self) :
        if self.conn is not None:
            self.conn.close()
        
    def connect(self):
        #print(1)
        self.conn = MySQLdb.connect(host=self.host,user=self.user,password=self.pwd,database=self.db, charset='utf8')
        #self.conn = pymssql.connect('127.0.0.1','sa','147258','StraTrace')
        #print(2)
        cur = self.conn.cursor()
        if not cur:
            raise(NameError,"连接数据库失败")
        else:
            self.cur = cur
    def query(self, sql):
        self.cur.execute(sql)
        rs = self.cur.fetchall()
        return rs
    def exec(self, sql):
        self.cur.execute(sql)
        self.conn.commit()
    
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
    
    def updateforum(self,fid):
        sql = """
        update {0}_forum_forum set 
        threads=(select count(*) from {0}_forum_thread where fid={1}), 
        posts  =(select count(*) from {0}_forum_post   where fid={1})
        """.format(self.table_prefix, fid)
        self.exec(sql)
        
    def updatethread(self, tid):
        sql = """
        update {0}_forum_thread set replies=(select count(*)  from {0}_forum_post where tid={1})
        """.format(self.table_prefix, tid)
        self.exec(sql)
        
    
    def add_post(self, fid, tid, post, first, last):
        # 获取post id
        sql = "insert into {0}_forum_post_tableid values()".format(self.table_prefix)
        self.exec(sql)
        rs = self.query("select last_insert_id()")
        pid = int(rs[0][0])
        
        sql = """
        insert into {0}_forum_post(
pid         , -- int(10) unsigned NOT NULL,
fid         , -- mediumint(8) unsigned NOT NULL DEFAULT '0',
tid         , -- mediumint(8) unsigned NOT NULL DEFAULT '0',
`first`     , -- tinyint(1) NOT NULL DEFAULT '0',
author      , -- varchar(15) NOT NULL DEFAULT '',
authorid    , -- mediumint(8) unsigned NOT NULL DEFAULT '0',
`subject`   , -- varchar(80) NOT NULL DEFAULT '',
dateline    , -- int(10) unsigned NOT NULL DEFAULT '0',
message     , -- mediumtext NOT NULL,
useip       , -- varchar(15) NOT NULL DEFAULT '',
`port`      , -- smallint(6) unsigned NOT NULL DEFAULT '0',
invisible   , -- tinyint(1) NOT NULL DEFAULT '0',
anonymous   , -- tinyint(1) NOT NULL DEFAULT '0',
usesig      , -- tinyint(1) NOT NULL DEFAULT '0',
htmlon      , -- tinyint(1) NOT NULL DEFAULT '0',
bbcodeoff   , -- tinyint(1) NOT NULL DEFAULT '0',
smileyoff   , -- tinyint(1) NOT NULL DEFAULT '0',
parseurloff , -- tinyint(1) NOT NULL DEFAULT '0',
attachment  , -- tinyint(1) NOT NULL DEFAULT '0',
rate        , -- smallint(6) NOT NULL DEFAULT '0',
ratetimes   , -- tinyint(3) unsigned NOT NULL DEFAULT '0',
`status`    , -- int(10) NOT NULL DEFAULT '0',
tags        , -- varchar(255) NOT NULL DEFAULT '0',
`comment`   , -- tinyint(1) NOT NULL DEFAULT '0',
replycredit   -- int(10) NOT NULL DEFAULT '0',
-- position    ,  int(8) unsigned NOT NULL AUTO_INCREMENT,
  )values
  (
{1}/*pid         */, 
{2}/*fid         */,  
{3}/*tid         */,   
{4}/*`first`     */, 
'{5}'/*author      */, 
{6}/*authorid    */, 
''/*`subject`   */, 
{7}/*dateline    */, 
'{8}'/*message     */, 
'192.168.1.1'/*useip       */, 
1234/*`port`      */, 
0/*invisible   */, 
0/*anonymous   */, 
0/*usesig      */, 
0/*htmlon      */, 
0/*bbcodeoff   */, 
0/*smileyoff   */, 
0/*parseurloff */, 
0/*attachment  */, 
0/*rate        */, 
0/*ratetimes   */, 
0/*`status`    */, 
0/*tags        */, 
0/*`comment`   */, 
0/*replycredit  */
);
  """.format(self.table_prefix, pid, fid, tid, first, post['author'], post['authorid'], 
    self.strtime2timestamp(post['time']), post['message'].replace("'","\\'")
  )
        #print(sql)
        self.exec(sql)
        if last : 
            sql = "update {0}_forum_thread set maxposition={1} where tid={2}".format(self.table_prefix, pid, tid)
            self.exec(sql)

  
    def add_thread_posts(self, fid, author, authorid, subject, post_list):
        post_count = len(post_list)
        lastpost =  self.strtime2timestamp(post_list[post_count-1]['time'])
        lastposter = post_list[post_count-1]['author']
        dateline = self.strtime2timestamp(post_list[0]['time'])
        # 添加thread
        sql = """insert into {0}_forum_thread(
--  tid           , -- mediumint(8) unsigned NOT NULL AUTO_INCREMENT,
  fid           , -- mediumint(8) unsigned NOT NULL DEFAULT '0',
  posttableid   , -- smallint(6) unsigned NOT NULL DEFAULT '0',
  typeid        , -- smallint(6) unsigned NOT NULL DEFAULT '0',
  sortid        , -- smallint(6) unsigned NOT NULL DEFAULT '0',
  readperm      , -- tinyint(3) unsigned NOT NULL DEFAULT '0',
  price         , -- smallint(6) NOT NULL DEFAULT '0',
  author        , -- char(15) NOT NULL DEFAULT '',
  authorid      , -- mediumint(8) unsigned NOT NULL DEFAULT '0',
  `subject`     , -- char(80) NOT NULL DEFAULT '',
  dateline      , -- int(10) unsigned NOT NULL DEFAULT '0',
  lastpost      , -- int(10) unsigned NOT NULL DEFAULT '0',
  lastposter    , -- char(15) NOT NULL DEFAULT '',
  views         , -- int(10) unsigned NOT NULL DEFAULT '0',
  replies       , -- mediumint(8) unsigned NOT NULL DEFAULT '0',
  displayorder  , -- tinyint(1) NOT NULL DEFAULT '0',
  highlight     , -- tinyint(1) NOT NULL DEFAULT '0',
  digest        , -- tinyint(1) NOT NULL DEFAULT '0',
  rate          , -- tinyint(1) NOT NULL DEFAULT '0',
  special       , -- tinyint(1) NOT NULL DEFAULT '0',
  attachment    , -- tinyint(1) NOT NULL DEFAULT '0',
  moderated     , -- tinyint(1) NOT NULL DEFAULT '0',
  closed        , -- mediumint(8) unsigned NOT NULL DEFAULT '0',
  stickreply    , -- tinyint(1) unsigned NOT NULL DEFAULT '0',
  recommends    , -- smallint(6) NOT NULL DEFAULT '0',
  recommend_add , -- smallint(6) NOT NULL DEFAULT '0',
  recommend_sub , -- smallint(6) NOT NULL DEFAULT '0',
  heats         , -- int(10) unsigned NOT NULL DEFAULT '0',
  `status`      , -- smallint(6) unsigned NOT NULL DEFAULT '0',
  isgroup       , -- tinyint(1) NOT NULL DEFAULT '0',
  favtimes      , -- mediumint(8) NOT NULL DEFAULT '0',
  sharetimes    , -- mediumint(8) NOT NULL DEFAULT '0',
  stamp         , -- tinyint(3) NOT NULL DEFAULT '-1',
  icon          , -- tinyint(3) NOT NULL DEFAULT '-1',
  pushedaid     , -- mediumint(8) NOT NULL DEFAULT '0',
  cover         , -- smallint(6) NOT NULL DEFAULT '0',
  replycredit   , -- smallint(6) NOT NULL DEFAULT '0',
  relatebytag   , -- char(255) NOT NULL DEFAULT '0',
  maxposition   , -- int(8) unsigned NOT NULL DEFAULT '0',
  bgcolor       , -- char(8) NOT NULL DEFAULT '',
  comments      , -- int(10) unsigned NOT NULL DEFAULT '0',
  hidden        -- smallint(6) unsigned NOT NULL DEFAULT '0',
)
values(
{1} /*fid           */,
0  /*posttableid   */,
0  /*typeid        */,
0  /*sortid        */,
0  /*readperm      */,
0  /*price         */,
'{2}'  /*author        */,
{3}  /*authorid      */,
'{4}'  /*`subject`     */,
{5}  /*dateline      */,
{6}  /*lastpost      */,
'{7}' /*lastposter    */,
0  /*views         */,
0  /*replies       */,
0  /*displayorder  */,
0  /*highlight     */,
0  /*digest        */,
0  /*rate          */,
0  /*special       */,
0  /*attachment    */,
0  /*moderated     */,
0  /*closed        */,
0  /*stickreply    */,
0  /*recommends    */,
0  /*recommend_add */,
0  /*recommend_sub */,
0  /*heats         */,
0  /*`status`      */,
0  /*isgroup       */,
0  /*favtimes      */,
0  /*sharetimes    */,
-1  /*stamp         */,
-1  /*icon          */,
0  /*pushedaid     */,
0  /*cover         */,
0  /*replycredit   */,
0  /*relatebytag   */,
1  /*maxposition   */,
''  /*bgcolor       */,
0  /*comments      */,
0  /*hidden        */
);
""".format(self.table_prefix, fid, author, authorid, subject.replace("'", "\\'")[:78], dateline, lastpost, lastposter)
    
        #print(sql)
        self.exec(sql)
        # 获取刚插入的thread id
        sql = "select LAST_INSERT_ID()"
        rs = self.query(sql)
        tid = int(rs[0][0])
        # 插入post
        for i in range(post_count) :
            first = 0
            if i == 0 :
                first = 1
            self.add_post(fid, tid, post_list[i], first, i==(post_count-1))
        self.updatethread(tid)
        
if __name__ == '__main__':
    dh = DBHelper ('192.168.86.130', 'root', '', 'ultrax', 'pre')
    dh.connect()
    dh.add_thread_posts(38, 'xhk', 2, 'py insert xhk', [{'author':'xhk', 'authorid':2, 'time':'2010-1-1 10:00:00','message':'py insertor'}])
    

        
    
    
    
    
    
    
    
    
    
    