import sys
def gen_ubb(file):
    fp = open(file, 'r', encoding='utf8')
    c = fp.read()
    fp.close()
    c = eval(c)
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
    
    c['ver']      = 'www_ichinachess_com'
    c['viewurl'] = 'www.ichinachess.com'
    c['owner']    = '华夏棋坛'
    c['oldowner'] = '华夏棋坛'
    c['author']   = '华夏棋坛'
    c['refer']    = '华夏棋坛'
    
    if len(c['binit'])<=0:
        c['binit'] = '8979695949392919097717866646260600102030405060708012720323436383'
    
    d = ''
    d = d + '标题: '     + c['title']     + '\n'
    d = d + '分类: '     + c['class']     + '\n'
    d = d + '赛事: '     + c['event']     + '\n'
    d = d + '轮次: '     + c['round']     + '\n'
    d = d + '布局: '     + c['open']      + '\n'
    d = d + '红方: '     + c['red']       + '\n'
    d = d + '黑方: '     + c['black']     + '\n'
    d = d + '结果: '     + c['result']    + '\n'
    d = d + '日期: '     + c['date']      + '\n'
    d = d + '地点: '     + c['place']     + '\n'
    d = d + '组别: '     + c['group']     + '\n'
    d = d + '台次: '     + c['table']     + '\n'
    d = d + '记时规则: ' + c['timerule']      + '\n'
    d = d + '棋局类型: ' + c['type']      + '\n'
    d = d + '棋局性质: ' + c['gametype']  + '\n'
    d = d + '红方团体: ' + c['redteam']   + '\n'
    d = d + '红方姓名: ' + c['redname']   + '\n'
    d = d + '黑方团体: ' + c['blackteam'] + '\n'
    d = d + '黑方姓名: ' + c['blackname'] + '\n'
    d = d + '棋谱主人: ' + c['owner'] + '\n'
    d = d + '来源网站: https://www.ichinachess.com/\n\n\n'
    
    d = d + "[DhtmlXQ]\n"
    for tag in tags:
        #d = d + "\\\\u005BDhtmlXQ_{0}]{1}\\\\u005B/DhtmlXQ_{0}]\n".format(tag, c[tag])
        d = d + "[DhtmlXQ_{0}]{1}[/DhtmlXQ_{0}]\n".format(tag, c[tag])
    d = d + c['moves'] + "\n"
    d = d + c['comments'] + "\n"
    d = d + "[/DhtmlXQ]"
    
    return d
    
if __name__ == '__main__':
    id = sys.argv[1]
    t = gen_ubb('chess_manual/{0}.txt'.format(id))
    print(t)
    