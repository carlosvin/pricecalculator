'''
Created on 27/10/2013

@author: carlos
'''

class Field(object)
"""
Help us to represent relevant fields of filter
"""
	def __init__(self, name, t, description=""):
		self.name = name
		self.type = t
		self.description =description

class Filter(object):
	def __init__():
		self.fields = {}

	def add_field(self, f):
		self.fields[f.name] = f

	def del_field(self, field_name):
		del self.fields[field_name]

	def filter(self, v):
		raise "Not implemented, you must override this method"

class FilterXThan(Filter):

    def ___init__(self, value):
        self.value = float(value)
        self.add_field(Field("price", "number", "i.e: 0.3"))
        
class FilterLessThan(FilterXThan):
    name = 'Menor que'

    def filter(self, v):
        return self.value < float(v)

class FilterMoreThan(Filter):
    name = 'Mayor que'
        
    def filter(self, v):
        return self.value > float(v)


def factory(filter_type, value):
    if filter_type == FilterLessThan.name:
        return FilterLessThan(value)
    else if filter_type == FilterMoreThan.name:
        return FilterMoreThan(value)
    else:
        return None
