import sys
import urllib2

HOST='http://52.27.123.175:9494'

def handle(req):
    if req[0] == 'push':
        message=urllib2.quote(req[1])
        key = urllib2.urlopen("%s/push?bits=%s"%(HOST,message)).read()
        print "%s"%key
        
    if req[0] == 'pop':
        msg = urllib2.urlopen("%s/pop?key=%s"%(HOST,req[1])).read()
        print "%s"%msg

def main():
    handle(sys.argv[1:])

if __name__=="__main__":
    sys.exit(main())