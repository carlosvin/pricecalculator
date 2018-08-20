# -*- coding: utf8 -*-

from urllib.request import Request, urlopen
import logging
import parsing

__author__ = 'carlos'

class Downloader(object):
    
    def __init__(self, url):
        self.url = url
        
    def read(self):
        request = Request( self.url )
        request.add_header('Accept-encoding', 'text/html')
        response = urlopen(request)
        charset = response.headers.get('charset')
        data = response.read()
        logging.debug('Read %u bytes from %s (%s)' % (len(data), self.url, charset))
        return data
    
class StocksInfoUpdater(object):
    
    def __init__(self, url):
        self.downloader = Downloader(url)
        self.parser =  parsing.StockParser()
        
    def update(self):
        dataread = self.downloader.read()
        self.parser.feed(dataread)
        return self.parser.stocks
    
    @property
    def stocks(self):
        return self.parser.stocks
    
    @property
    def url(self):
        return self.downloader.url
    



    
    
