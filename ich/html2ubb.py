#-*-coding:utf-8-*-
import re
import os,sys
from pyquery import PyQuery as pq
def embed2ubb(s):
    d = pq(s)
    e = d('embed')
    if e == None or len(e)==0:
        return s
    src = e.attr('src')
    print(src)
    h = e.attr('height')
    w = e.attr('width')
    
    news = ''
    if h!=None and w!=None:
        news = "<will_be_deleted>[flash={0},{1}]{1}[/flash]</will_be_deleted>".format(w,h,src)
    else:
        news = "<will_be_deleted>[flash]{0}[/flash]</will_be_deleted>".format(src)
    e.replaceWith(news)
    return d.html()
    
def Html2UBB(content):
    #以下是将html标签转为ubb标签
    pattern = re.compile( '<a href=\"([sS]+?)\"[^>]*>([sS]+?)</a>',re.I)
    content = pattern.sub(r'[url=1]2[/url]',content)
    pattern = re.compile( '<img[^>]+src=\"([^\"]+)\"[^>]*>',re.I)
    content = pattern.sub(r'[img]1[/img]',content)
    pattern = re.compile( '<strong>([sS]+?)</strong>',re.I)
    content = pattern.sub(r'[b]1[/b]',content)
    pattern = re.compile( '<font color=\"([sS]+?)\">([sS]+?)</font>',re.I)
    content = pattern.sub(r'[1]2[/1]',content)
    pattern = re.compile( '<[^>]*?>',re.I)
    content = pattern.sub('',content)
    #以下是将html转义字符转为普通字符
    content = content.replace('<','<')
    content = content.replace('>','>')
    content = content.replace('”','”')
    content = content.replace('“','“')
    content = content.replace('"','"')
    content = content.replace('©','©')
    content = content.replace('®','®')
    content = content.replace(' ',' ')
    content = content.replace('—','—')
    content = content.replace('–','–')
    content = content.replace('‹','‹')
    content = content.replace('›','›')
    content = content.replace('…','…')
    content = content.replace('&','&')
    return content

def html2ubb(s):
    pattern = re.compile('<br[^>]*>',re.I)
    s = pattern.sub(r'\n', s)
    pattern = re.compile('<p[^>\/]*\/>',re.I)
    s = pattern.sub(r'\n', s)
    pattern = re.compile('\son[\w]{3,16}\s?=\s*([\'\"]).+?\1',re.I)
    s = pattern.sub(r'', s)
   
    pattern = re.compile('<hr[^>]*>',re.I)
    s = pattern.sub(r'[hr]', s)
    pattern = re.compile('<(sub|sup|u|strike|b|i|pre)[^>]*>',re.I)
    s = pattern.sub(r'[\1]', s)
    pattern = re.compile('<\/(sub|sup|u|strike|b|i|pre)>',re.I)
    s = pattern.sub(r'[/\1]', s)  
    pattern = re.compile('<strong>',re.I)
    s = pattern.sub(r'[b]', s)  
    pattern = re.compile('</strong>',re.I)
    s = pattern.sub(r'[/b]', s)  
    pattern = re.compile('<em>',re.I)
    s = pattern.sub(r'[1i]', s)
    pattern = re.compile('</em>',re.I)
    s = pattern.sub(r'[/i]', s)
    
    pattern = re.compile('<blockquote([^>]*)>',re.I)
    s = pattern.sub(r'[blockquote]', s)
    pattern = re.compile('</blockquote([^>]*)>',re.I)
    s = pattern.sub(r'[/blockquote]', s)
    
    pattern = re.compile('<img[^>]*smile=\"(\d+)\"[^>]*>',re.I)
    s = pattern.sub(r'[s:\1]', s)
    pattern = re.compile('<img[^>]*src=[\'\"\s]*([^\s\'\"]+)[^>]*>',re.I)
    s = pattern.sub(r'[img]https:\/\/www.ichinachess.com\/\1[\/img]', s)
    pattern  = re.compile('<a[^>]*href=[\'\"]*([^\s\'\"]*)[^>]*>(.+?)<\/a>', re.I)
    s = pattern.sub(r'[url=\1]\2[/url]', s)
    #pattern  = re.compile('<embed[^>]*src=[\'\"]{1}([^\s\'\"]*)[\'\"]{1}[^>]*>', re.I)
    
    # 还没替换的标签就替换为空
    pattern  = re.compile('<[^>]*?>',re.I)
    s = pattern.sub(r'', s)
    
    s = s.replace('&amp;', '&')
    s = s.replace('&lt;', '<')
    s = s.replace('&gt;', '>')
    s = s.replace('&#13;', '\n')
    
    s = s.replace('[DhtmlXQ_', '\\\\u005BDhtmlXQ_')
    s = s.replace('[/DhtmlXQ_', '\\\\u005B/DhtmlXQ_')
    s = s.replace('DhtmlXQiFrame', 'DhtmlXQ')
    
    pattern = re.compile('\n{2,}',re.I)
    s = pattern.sub(r'\n\n', s)
    
    return s
if __name__=='__main__':
    print(html2ubb('<b style="font-size:12px;line-height:15px;">求攻守之策</b>'))