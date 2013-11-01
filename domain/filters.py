'''
Created on 27/10/2013

@author: carlos
'''
from domain.validator import FloatPossitiveValidator

class Field(object):
	""" Help us to represent relevant fields of filter"""
	def __init__(self, name, t, description="", extra_params='', validator=None):
		self.name = name
		self.type = t
		self.description = description
		self._value = None
		self.extra_params = 'title=' + self.name + ' ' + extra_params
		self._validator = validator
		
	def __repr__(self):
		if self.value:
			return u"%s:%s=%s" % (self.name, self.type, self.value)
		else:
			return u"%s:%s=%s" % (self.name, self.type, "None")
	
	@property
	def value(self):
		return self._value
	
	@value.setter
	def value(self, v):
		if self._validator:
			self._validator.validate(v)
		self._value = v

class Filter(object):
	def __init__(self):
		self.fields = {}

	def add_field(self, f):
		self.fields[f.name] = f

	def del_field(self, field_name):
		del self.fields[field_name]

	def filter(self, v):
		raise "Not implemented, you must override this method"
	
	@classmethod
	def get_name(self):
		raise "Not implemented, you must override this method"
	
	@property
	def id(self):
		return self.get_name() + str(self.fields.values())
	
	@staticmethod
	def factory(filter_type):
		if filter_type == FilterLessThan.NAME:
			return FilterLessThan()
		elif filter_type == FilterMoreThan.NAME:
			return FilterMoreThan()
		else:
			return None

	
class FilterXThan(Filter):
	
	def __init__(self):
		super(FilterXThan, self).__init__()
		self._field = Field("price", "number", description="i.e: 0.3",  extra_params='step=any', validator=FloatPossitiveValidator())
		self.add_field(self._field)

	@property
	def value(self):
		return float(self._field.value)

class FilterLessThan(FilterXThan):
	NAME = 'Menor que'
	
	def filter(self, v):
		return self.value < float(v)
	
	@classmethod
	def get_name(self):
		return self.NAME

class FilterMoreThan(FilterXThan):
	NAME = 'Mayor que'

	def filter(self, v):
		return self.value > float(v)
	
	@classmethod
	def get_name(self):
		return self.NAME
	
