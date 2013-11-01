'''
Created on 29/10/2013

@author: xIS16031
'''
from abc import abstractmethod

class Validator(object):
    @abstractmethod
    def validate(self, v):
        raise "You must override this method"
    
class FloatValidator(Validator):
    '''
    Verify if a parameter is a valid float. Else raise an exception
    '''
    
    @classmethod
    def validate(self, v):
        float(v)
        
        
class FloatPossitiveValidator(FloatValidator):
    @classmethod
    def validate(self, v):
        if float(v) < 0:
            raise TypeError("Invalid value '%f', must be more or equals than 0" % (float(v),))