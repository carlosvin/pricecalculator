from HTMLParser import HTMLParser, HTMLParseError
import logging
import copy
from domain import Stock

def get_attr(name, attrs):
        for k,v in attrs:
            if k == name:
                return v
        return None

class StockParser (HTMLParser, object):
    
    def __init__(self):
        self.reset()
        self.stocks = []
        self._s_tmp = None
        self._td = 0
        self._is_a_open = False
        self._is_table_open=False
    
    def cleanup(self):
        self._table_c()
        self.stocks = []

    def feed(self, data):
        self.cleanup()
        try:
            super(StockParser, self).feed(data)
        except HTMLParseError as e:
            logging.warn(e)

    def handle_starttag(self, tag, attrs):
        if tag == 'table':
            self._table_o(attrs)
        elif tag == 'tr':
            self._tr_o()
        elif tag == 'td':
            self._td_o()
        elif tag == 'a':
            self._a_o(attrs)

    def handle_endtag(self, tag):
        if tag == 'table':
            self._table_c()
        elif tag == 'td':
            self._td_c()
        elif tag == 'a':
            self._a_c()

    def handle_data(self, data):
        if self._s_tmp:
            if self._td == 1 and self._is_a_open:
                self._s_tmp.id = data
            elif self._td == 2:
                self._s_tmp.price = float(data.replace(',','.'))

    def _table_o(self, attrs):
        if get_attr('title', attrs) == 'Acciones':
            self._is_table_open=True
    
    def _table_c(self):
        self._is_table_open=False
        
    def _tr_o(self):
        if self._is_table_open:
            self._td_c()
            self._s_tmp = None
            self._td = 0
            self._s_tmp = Stock()
            self.stocks.append(self._s_tmp)
            
    def _td_o(self):
        self._td += 1
                    
    def _td_c(self):
        self._a_c()
            
    def _a_o(self, attrs):
        if self._s_tmp and self._td==1:
            self._is_a_open = True
            self._s_tmp.name = get_attr("title", attrs)
        
    def _a_c(self):
        self._is_a_open = False

           
                