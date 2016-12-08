
def gen_ubb(c):
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
    
    d = "[DhtmlXQ]\n"
    for tag in tags:
        d = d + "\\u005BDhtmlXQ_{0}]{1}\\u005B/DhtmlXQ_{0}]\n".format(tag, c[tag])
    d = d + c['moves']
    d = d + c['comments']
    d = d + "[DhtmlXQ]"
    
    return d
    
if __name == '__main__':
    
    