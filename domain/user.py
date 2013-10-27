'''
Created on 27/10/2013

@author: carlos
'''

class User(object):
    def __ini__(self):
        self._is_auth = False
        self._is_activated = False
        self._login = None        
        self._password = None        
    
    def is_authenticated(self):
        return self._is_auth
    
    def is_active(self):
        return self._is_activated
    
    def is_anonymous(self):
        return False
    
    def get_id(self):
        return self._login
    
    def is_right_password(self, pw):
        return self._password == pw
    
class UserManager(object):
    
    def __init__(self, fpath):
        self._file = fpath
        self._users = {}
            
    def get(self, uid):
        return self._users[uid]

    def login(self, uid, password):
        user = self.get(uid)
        if user and user.is_right_password(password):
            return user
        else:
            return None