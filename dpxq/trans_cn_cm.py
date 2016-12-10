
sid = '车马相士帅士相马车炮炮兵兵兵兵兵车马象士将士象马车炮炮卒卒卒卒卒'
rindex = '一二三四五六七八九'
bindex = '123456789'

directs2 = '前后'
directs3 = '前中后'
directs5 = '一二三四五'

cp = [
    (8,9),(7,9),(6,9),(5,9),(4,9),(3,9),(2,9),(1,9),(0,9),(7,7),(1,7),(8,6),(6,6),(4,6),(2,6),(0,6),
    (0,0),(1,0),(2,0),(3,0),(4,0),(5,0),(6,0),(7,0),(8,0),(1,2),(7,2),(0,3),(2,3),(4,3),(6,3),(8,3)
]



def cmp_func(lpos,rpos):
    return lpos[1]-rpos[1]

# 得到同名棋子位置(包含自己)
# 并根据先后排序
def get_same_name_pos(id,name,fr):
    pos_list = []
    if id<16:
        for i in range(16):
            if sid[i]==name and fr[0]==cp[i][0] and cp[i][0]<9:
                #print(sid[i])
                pos_list.append(cp[i])
        sorted(pos_list, key=lambda c:c[1], reverse=True)
    else:
        for i in range(16,32):
            if sid[i]==name and fr[0]==cp[i][0] and cp[i][0]<9:
                pos_list.append(cp[i])
        sorted(pos_list, key=lambda c:c[1], reverse = False)
    return pos_list

def check_other_column_count_eg2(this_col, name):
    for i in range(9):
        if i == this_col:
            continue
        count = 0
        for j in range(32):
            if cp[j][0]<9 and sid[j]==name and cp[j][0]==i:
                count = count+1
        if count>=2:
            return True
    
    return False
    
def move_or_eat(id,to):
    for i in range(32):
        if i == id:
            continue
        if cp[i][0]==to[0] and cp[i][1]==to[1]:
            # eat
            cp[i] = (9,cp[i][1])
            break;
    cp[id] = to
    
def next(fr,to):
    id = -1
    for i in range(32):
        if cp[i][0]==fr[0] and cp[i][1]==fr[1]:
            id = i
            break
    if id == -1:
        return '着法错误'
    
    s = ['着','法','错','误']
    #s[2] = sid[id]
    #print('id:{0}'.format(id))
    if id<16: # 红方
        if fr[1]==to[1]:
            s[2] = '平'
            s[3] = rindex[8-to[0]]
        elif fr[1]>to[1]:
            s[2] = '进'
            if fr[0]==to[0]: # 同一竖线
                s[3] = rindex[fr[1]-to[1]-1]
            else:
                s[3] = rindex[8-to[0]]
        elif fr[1]<to[1]:
            s[2] = '退'
            if fr[0]==to[0]: # 同一竖线
                s[3] = rindex[to[1]-fr[1]]
            else:
                s[3] = rindex[8-to[0]]
                
        snpl = get_same_name_pos(id,sid[id], fr)
        snpl_count = len(snpl)
        if snpl_count>1:
            order_index = 0
            for k in range(snpl_count):
                if snpl[k][1] == fr[1]:
                    order_index = k
                
            if snpl_count==2:
                s[0] = directs2[k]
            elif snpl_count==3:
                s[0] = directs3[k]
            else:
                s[0] = directs3[k]
            
            
            s[1] = sid[id]    
            
            if sid[id] == '兵':
                # 检测其他列上是否有两个及以上的 兵
                if check_other_column_count_eg2(fr[0], sid[id]):
                    s[1] = rindex[fr[0]]
            
        else:
           s[0] = sid[id] 
           s[1] = rindex[8-fr[0]]
           
        
        
    else: #黑方
        if fr[1]==to[1]:
            s[2] = '平'
            s[3] = bindex[to[0]]
        elif fr[1]>to[1]:
            s[2] = '退'
            if fr[0]==to[0]:
                s[3] = bindex[fr[1]-to[1]-1]
            else:
                s[3] = bindex[to[0]]
        elif fr[1]<to[1]:
            s[2] = '进'
            if fr[0]==to[0]:
                s[3] = bindex[to[1]-fr[1]-1]
            else:
                s[3] = bindex[to[0]]
                
        snpl = get_same_name_pos(id,sid[id], fr)
        snpl_count = len(snpl)
        if snpl_count>1:
            order_index = 0
            for k in range(snpl_count):
                if snpl[k][1] == fr[1]:
                    order_index = k
            if snpl_count==2:
                s[0] = directs2[k]
            elif snpl_count==3:
                s[0] = directs3[k]
            else:
                s[0] = directs3[k]
            s[2] = sid[id]  

            if sid[id] == '卒':
                # 检测其他列上是否有两个及以上的 兵
                if check_other_column_count_eg2(fr[0], sid[id]) :
                    s[1] = bindex[fr[0]]           
                    
        else:
           s[0] = sid[id] 
           s[1] = bindex[fr[0]]
    
    # 吃子
    move_or_eat(id, to)
    return ''.join(s)

def play_movelist(ml):
    global cp
    cp = [
    (8,9),(7,9),(6,9),(5,9),(4,9),(3,9),(2,9),(1,9),(0,9),(7,7),(1,7),(8,6),(6,6),(4,6),(2,6),(0,6),
    (0,0),(1,0),(2,0),(3,0),(4,0),(5,0),(6,0),(7,0),(8,0),(1,2),(7,2),(0,3),(2,3),(4,3),(6,3),(8,3)
    ]
    s = ''
    count = len(ml)
    round = int(count/8)
    for i in range(round):
        r = ml[i*8:i*8+4]
        b = ml[i*8+4:i*8+8]
        
        fr = (int(r[0]),int(r[1]))
        to = (int(r[2]),int(r[3]))
        rs = next(fr,to)
        
        fr = (int(b[0]),int(b[1]))
        to = (int(b[2]),int(b[3]))
        bs = next(fr,to)
        #print(rs + ' ' + bs )
        s = s + '%3d. %s %s\n' % (i+1, rs, bs)
    return s
    
if __name__ == '__main__':
    ml = '77376364796770622625100219278070090800012735121525242324082860423747304135436243474301218979727569472123434570731727233328184030594815132737304018143343450502101415757615454345464513156788767837387874454403047975040506051514383414188867102205041811666573713431413265647444754571314544316167756171647471727567726267556252444552547473223455673426451511211511214173832638'
    s = play_movelist(ml)
    print(s)
    
    
    