
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
    
    d = "[DhtmlXQ]\n"
    for tag in tags:
        #d = d + "\\\\u005BDhtmlXQ_{0}]{1}\\\\u005B/DhtmlXQ_{0}]\n".format(tag, c[tag])
        d = d + "[DhtmlXQ_{0}]{1}[/DhtmlXQ_{0}]\n".format(tag, c[tag])
    d = d + c['moves'] + "\n"
    d = d + c['comments'] + "\n"
    d = d + "[/DhtmlXQ]"
    
    return d
    
if __name__ == '__main__':
    t = gen_ubb('chess_manual/66394.txt')
    print(t)
    