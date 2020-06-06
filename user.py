import database

class User:
    def __init__(self,username = "",password = "",email = ""):
        self.username = username
        self.password = password
        self.email = email
        # self._isLogged = 0
    def isLogged(self):
        db = database.Database()
        user = User(self.username,self.password)
        if(db.getLoginState(user)):
            return 1
        return 0