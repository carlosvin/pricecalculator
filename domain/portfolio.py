'''
Created on 27/10/2013

@author: carlos
'''

class PortfolioManager(object):
    def __init__(self):
        self._portfolios = {}                                            
        
    def add(self, p):
        for u in p.users:
            if self.portfolios[u] == None:
                self.portfolios[u] = set()
            self.portfolios[u].add(p)
            
class Portfolio(object):

    def __init__(self):
        self.users = {}
        self.filters = {}
        
    def add_filter(self, f):
        self.filters[f.id] = f
    
    def remove_filter(self, filter_id):
        self.filters.pop(filter_id)