
# -*- coding: utf8 -*-
class Stock(object):
    def __init__(self):
        self.id = None
        self.name = None
        self.price = None

    def __str__(self):
    	return self.__unicode__()

    def __unicode__(self):
    	if self.name <> None:
    		#return u"%s.\t%s %f" % (self.id, self.name, self.price)
    		return u"%s.\t%f" % (self.id, self.price)
    	else:
    		return "None"