# -*- coding: utf8 -*-

class Stock(object):
    def __init__(self):
        self.id = None
        self._name = None
        self.price = None
        
    def _get_name(self):
        return self._name
    
    def _set_name(self, name):
        self._name = unicode(name, errors='ignore')
        
    name = property(_get_name, _set_name)

    def __str__(self):
        return self.__unicode__()

    def __unicode__(self):
        if self.name <> None:
            return u"%s.\t%f" % (self.id, self.price)
        else:
            return "None"
        
    def is_invalid(self):
        return self.id==None or self.price==None
    

    