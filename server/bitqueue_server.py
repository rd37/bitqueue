'''
Created on Dec 13, 2015

@author: ronaldjosephdesmarais
'''
import sqlalchemy
import webob
import routes
import paste
import logging

import paste.fileapp
import paste.httpserver
import routes
import webob
import webob.dec
import webob.exc

HOST = '0.0.0.0'
PORT = 80

logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s %(levelname)s %(message)s',
                    filename='./bitqueue.log',
                    filemode='w')

class BitQueueService(object):

    map = routes.Mapper()
    map.connect('push/', '/push/', method='push')
    map.connect('push', '/push', method='push')
    map.connect('pop/', '/pop/', method='pop')
    map.connect('pop', '/pop', method='pop')
    
    queue = {}
    key = 100
    
    @webob.dec.wsgify
    def __call__(self, req):
        results = self.map.routematch(environ=req.environ)
        if not results:
            return webob.exc.HTTPNotFound()
        match, route = results
        link = routes.URLGenerator(self.map, req.environ)
        req.urlvars = ((), match)
        kwargs = match.copy()
        method = kwargs.pop('method')
        req.link = link
        return getattr(self, method)(req, **kwargs)
 
    def getKey(self):
        while "%s"%self.key in self.queue:
            self.key+=1
        return self.key
        
    def pop(self,req):
        
        msg = 'crappy, not understood, either bad key or malformed request this service does not understand'
        key = 0
        try:
            key = req.POST['key']
            msg = self.queue["%s"%key]
        except:
            try:
                key = req.GET['key']
                msg = self.queue["%s"%key]
            except:
                logging.error("Exception occurred on GET end it then")
        
        if "%s"%key in self.queue:
            del self.queue["%s"%key]
            
        logging.info("Popped key %s current queue is %s"%(key,self.queue))
        return webob.Response(
            body='%s'%msg
        )
        
    def push(self,req):
        
        key = self.getKey()
        try:
            msg = req.POST['bits']
            self.queue["%s"%key] = msg
        except:
            try:
                msg = req.GET['bits']
                self.queue["%s"%key] = msg
            except:
                print "Exception occurred on GET end it then"
        
        logging.info("Pushed key %s current queue is %s"%(key,self.queue))
        
        return webob.Response(
            body='%s'%key
        )

def main():
    app= BitQueueService()
    paste.httpserver.serve(app, host=HOST, port=PORT)

if __name__ == '__main__':
    main()
