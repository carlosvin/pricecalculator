'''
Created on 27/10/2013

@author: carlos
'''
from flask_login import UserMixin

class User(UserMixin):
    def __init__(self, email, password, is_active):
        self._email = email        
        self._password = password        
    
    def is_right_password(self, pw):
        return self._password == pw
    
    def get_id(self):
        return self._email
    
    #TODO improve this method
    @staticmethod
    def is_valid_password(password):
        return len(password) > 0
    
    def __repr__(self):
        return '<User %r>' % (self._email)
    
class UserManager(object):
    
    def __init__(self):
        self._users = {}
            
    def get(self, uid):
        if uid in self._users:
            return self._users[uid]
        else:
            return None

    def login(self, uid, password):
        user = self.get(uid)
        if user and user.is_right_password(password):
            return user
        else:
            return None

    # TODO raise exceptions instead of boolean
    def add_user(self, uid, password):
        if uid in self._users:
            return False
        else:
            if User.is_valid_password(password):
                self._users[uid] = User(uid, password, True)
                return True
            else:
                return False
    
    def _get_uids(self):
        return self._users.keys()
    uids = property(_get_uids)