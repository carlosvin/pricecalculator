'''
Created on 27/10/2013

@author: carlos
'''

class FilterLessThan(object):
    name = 'Menor que'

    def ___init__(self, value):
        self.value = float(value)
        
    def filter(self, v):
        return self.value < float(v)

def factory(filter_type, value):
    if filter_type == FilterLessThan.name:
        return FilterLessThan(value)
    else:
        return None