import sys
if __name__=='__main__':
    if len(sys.argv) != 3:
        print('unicode 转中文\n unicdoe2cn src_file dst_file')
        sys.exit()
        
    fsrc = open(sys.argv[1], 'r', encoding='utf8')
    fdst = open(sys.argv[2], 'w', encoding='utf8')
    c = fsrc.read()
    c = c.encode("utf8").decode('unicode-escape')
    fdst.write(c)
    fsrc.close()
    fdst.close()