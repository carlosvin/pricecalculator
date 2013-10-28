'''
Created on 27/10/2013

@author: carlos
'''

class PortfolioManager(object):
    def __init__(self):
        self._portfolios = {}                                            
        self._portfolios_shared = {}                                            
        
    def add(self, p):
        for u in p.users:
            PortfolioManager.add_to(u, p, self._portfolios_shared)
        PortfolioManager.add_to(p.owner, p, self._portfolios)


    @staticmethod
    def add_to(uid, p, pfs):
        if not uid in pfs:
            pfs[uid] = {}
        pfs[uid][p.name] = p
    
    def get(self, uid , p_name):
        try:
            return self._portfolios[uid][p_name]
        except:
            return None
    
    def get_own(self, uid):
        try:
            return self._portfolios[uid]
        except:
            return None
        
    def get_shared(self, uid):
        try:
            return self._portfolios_shared[uid]
        except:
            return None
        
            
class Portfolio(object):
    
    def __init__(self, name, market, owner):
        self.name = name
        self.market = market
        self.users = set()
        self.owner = owner
        self.filters = {}
        
    def add_filter(self, f):
        self.filters[f.id] = f
    
    def del_filter(self, filter_id):
        self.filters.pop(filter_id)
        
    def update(self, name, market, users):
        self.users = users
        self.name = name
        self.market = market
    