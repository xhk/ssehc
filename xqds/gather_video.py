
from pyquery import PyQuery as pq
import sys
sys.path.append("..")
from ich import DbHelper
ids = [
45670,
42489,
41250,
39846,
39843,
39816,
39644,
39641,
39596,
39814,
34357,
34356,
34355,
34354,
34352,
34351,
34350,
48389,
34353,
34245,
34244,
34243,
34242,
34241,
34240,
34239,
48562,
46804,
43617,
43620,
34443,
34442,
34441,
34440,
34439,
48217,
42772,
42699,
42437,
41733,
41562,
41026,
40214,
40216,
48903,
48842,
48841,
48750,
48751,
48647,
48646,
48600,
48559,
49202,
49201,
48903,
48869,
48868,
48842,
48841,
48838,
48796]

def video_ref(id):
    return "http://www.zgxqds.com/blog/article.asp?id=" + str(id)

def get_video(url):
    d = pq(url=url)
    date = d('.bdate').text()
    title = d('.btitle a').text()
    frame_url = d('iframe').attr('src')
    message = "[ichframe=670,502]{0}[/ichframe]".format(frame_url)
    return (title,[{'author':'xhk', 'authorid':2, 'time':date, 'message':message}])
    
if __name__=='__main__':
    
    for id in ids:
        url = video_ref(id)
        v = get_video(url)
        file = "thread/vido_{0}.txt".format(id)
        fp = open( file, 'w', encoding='utf8')
        fp.write(str(v))
        fp.close()
        