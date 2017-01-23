import random
import sys
sys.path.insert(0, '../ich')
import html2ubb

class ForumThread:
    def __init__(self):
        self.user_list = []
        fp = open('userlist.txt', 'r', encoding='utf8')
        c = fp.read()
        self.user_list = eval(c)
        fp.close()
        
    def getThreadAuthor(self):
        count = len(self.user_list)
        i = random.randint(0,count-1)
        u = (self.user_list[i][0], self.user_list[i][1].strip())
        return u

    def getPostAuthor(self,thread_author):
        count = len(self.user_list)
        i = random.randint(0,count-1)
        if thread_author == self.user_list[i][1]:
            return self.getPostAuthor(thread_author)
        
        u = (self.user_list[i][0], self.user_list[i][1].strip())
        return u
        
    def getThread(self, thread, rand_author=True):
        nt = {}
        nt['subject']   = thread[0]
        
        if len(nt['subject'])>3 and nt['subject'][:3] == '主题：':
            nt['subject'] = nt['subject'][3:]
        
        nt['post_list'] = []
        tauthor = self.getThreadAuthor()
        
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
                    pa = self.getPostAuthor(tauthor[1])
                    p['author']   = pa[1]
                    p['authorid'] = pa[0]
                    
            p['message'] = html2ubb.embed2ubb(p['message'])
            p['message'] = html2ubb.html2ubb(p['message'])
            #print(p['message'])
            nt['post_list'].append(p)    
        return nt
