'''
Created on 27/10/2013

@author: carlos
'''

class User(object):
    def __init__(self, email, password, is_active):
        self._is_auth = False
        self._is_activated = False
        self._email = None        
        self._password = None        
    
    def is_authenticated(self):
        return self._is_auth
    
    def is_active(self):
        return self._is_activated
    
    def is_anonymous(self):
        return False
    
    def get_id(self):
        return self._email
    
    def is_right_password(self, pw):
        return self._password == pw

    #TODO improve this method
    @staticmethod
    def is_valid_password(password):
        return len(password) > 0
    
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
                self._users[uid] = User(uid, password,True)
                return True
            else:
                return False