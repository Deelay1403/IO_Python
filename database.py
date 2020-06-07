import mysql.connector
import config
import hashlib
import time
import math
class Database:
    def __init__(self):
        self.__query = {
            "AddCar":F"INSERT INTO `Car` (`Car_id`, `Model`, `Year`, `Make`, `Type`) VALUES ('%s', '%s', '%s', '%s', '%s');",
            "GetCarID":F"SELECT `Car_id` FROM `Car` WHERE `Model` = '%s' AND `Year` = '%s' AND `Make` = '%s' AND `Type` = '%s';",
            "GetCars":F"SELECT * FROM Car",
            "GetCar":F"SELECT * FROM Car WHERE Car.%s = %s",
            "GetOffers_index":F"SELECT Offert.`Offert_ID`,`Title`, Offert_Detail.Thumbnail FROM `Offert` LEFT JOIN Offert_Detail ON Offert.`Offert_ID` = Offert_Detail.Offert_ID",
            "GetOffert":F"SELECT Offert.`Offert_ID`,`Title`, Offert_Detail.Thumbnail, Offert_Detail.Description, Offert.Price, Offert.User_Login FROM `Offert` LEFT JOIN Offert_Detail ON Offert.`Offert_ID` = Offert_Detail.Offert_ID WHERE Offert.%s = %s",
            "Login":F"SELECT COUNT(*) FROM `User` WHERE `User_Login` = '%s' AND `Salt_Password` = '%s'",
            "AddUser":F"INSERT INTO `User` (`User_Login`, `Salt_Password`, `Email`, `User_Type`) VALUES ('%s', '%s', '%s', 'Standard');",
            "CheckPass":F"SELECT COUNT(*) FROM `User` WHERE `Salt_Password` = '%s' AND `User_Login` = '%s'",
            "UpdatePass":F"UPDATE `User` SET `Salt_Password` = '%s' WHERE `User`.`User_login` = '%s'",
            "QuestCheckUser":F"SELECT COUNT(*) FROM `Questionnaire` WHERE `User_Login` = '%s'",
            "CheckUserIfExist":F"SELECT COUNT(*) FROM `User` WHERE `User_Login` = '%s' OR `Email` = '%s'",
            "SessionID":F"SELECT COUNT(*) FROM `User` WHERE `Session_id` = '%s'",
            "AddSessionID":F"UPDATE `User` SET `Session_id` = '%s' WHERE `User`.`User_Login` = '%s';",
            "SendQuest":F"INSERT INTO `Questionnaire` (`User_Login`, `Make`, `Year_from`, `Year_to`, `Price_from`, `Price_to`) VALUES ('%s', '%s', '%s', '%s', '%s', '%s'); ",
            "DelQuest":F"DELETE FROM `Questionnaire` WHERE `User_Login` = '%s'",
            "UpdateQuest":F"UPDATE `Questionnaire` SET `User_Login`='%s',`Make`='%s',`Year_from`='%s',`Year_to`='%s',`Price_from`='%s',`Price_to`='%s'",
            "AddOffert":F"INSERT INTO `Offert` (`Offert_ID`, `User_Login`, `Title`, `Price`, `Car_id`) VALUES (NULL, '%s', '%s', '%s', '%s');",
            "SelectOffertID":F"SELECT `Offert_ID` FROM `Offert` WHERE `Title` = '%s' AND `User_Login` = '%s'",
            "AddOffertDet":F"INSERT INTO `Offert_Detail` (`Offert_ID`,`Description`,`Thumbnail`) VALUES (%s,'%s','%s');",
            "OffertListByUser":F"SELECT `Offert_ID`,`Title` FROM `Offert` WHERE `User_Login` = '%s';",
        }

        self.mydb = mysql.connector.connect(
        host=config.host,
        user=config.user,
        passwd=config.passwd,
        database=config.database)
        # self.mydb.data
        self.mycursor = self.mydb.cursor(buffered=True)
        

        # self.mycursor.execute("SELECT * FROM Car")

        # for x in self.mycursor._description:
        #     print(x[0])
    def __del__(self):
        self.mydb.close()
        self.mycursor.close()
    def _cursor_querry(self, query):
        self.mycursor.execute(query)
        self.mydb.commit()
    def addCar(self, model, make, type):
        q = self.__query['AddCar']%(model,make,type)
        self._cursor_querry(q)
    def getOffers_index(self):
        self._cursor_querry(self.__query['GetOffers_index'])
        result = []
        names = []
        for x in self.mycursor:
            result.append(x)
        for x in self.mycursor._description:
            names.append(x[0])
        return (result,names)
    def getOffert(self,value,column="Offert_ID"):
        q = self.__query['GetOffert']%(column,value)
        self._cursor_querry(q)
        result = []
        names = []
        for x in self.mycursor:
            result.append(x)
        for x in self.mycursor._description:
            names.append(x[0])
        return (result,names)
    def getCars(self):
        self._cursor_querry(self.__query['GetCars'])
        result = []
        names = []
        for x in self.mycursor:
            result.append(x)
        for x in self.mycursor._description:
            names.append(x[0])
        return (result,names)
    def getOffertNamesByUsername(self, username):
        self._cursor_querry(self.__query['OffertListByUser']%(username))
        result = []
        names = []
        for x in self.mycursor:
            result.append(x)
        for x in self.mycursor._description:
            names.append(x[0])
        return (result,names)

    def getCar(self, value, column = "Model"):
        self._cursor_querry(self.__query['GetCar']%(column,value))
        result = []
        names = []
        for x in self.mycursor:
            result.append(x)
        for x in self.mycursor._description:
            names.append(x[0])
        return (result,names)
    def getLoginState(self, user):
        q = self.__query['Login']%(user.username,str(hashlib.md5(user.password.encode()).hexdigest()))
        self._cursor_querry(q)
        return(bool(self.mycursor.fetchall()[0][0]))
    
    def addUser(self, user):
        s_p = str(hashlib.md5(user.password.encode()).hexdigest())
        q = self.__query['CheckUserIfExist']%(user.username,user.email)
        self._cursor_querry(q)
        if(bool(self.mycursor.fetchall()[0][0])):
            return -1
        else:
            q = self.__query['AddUser']%(user.username,s_p,user.email)
            self._cursor_querry(q)
            return 0
    def checkSessionID(self, id):
        try:
            self._cursor_querry(self.__query['SessionID']%(id))
            if(bool(self.mycursor.fetchall()[0][0])):
                return 1
        except TypeError:
            pass
        return 0
    def setSessionID(self, id, username):
        try:
            self._cursor_querry(self.__query['AddSessionID']%(id, username))
        except TypeError:
            pass
    def sendQuestionnaire(self, quest):
        q = self.__query['QuestCheckUser']%(quest.username)
        self._cursor_querry(q)
        state = bool(self.mycursor.fetchall()[0][0])
        if(state):
            self._cursor_querry(self.__query['UpdateQuest']%(
                quest.username,
                quest.made,
                quest.year_min,
                quest.year_max,
                quest.price_min,
                quest.price_max))
        else:
            self._cursor_querry(self.__query['SendQuest']%(
                quest.username,
                quest.made,
                quest.year_min,
                quest.year_max,
                quest.price_min,
                quest.price_max))
        return 0
    def deleteQuestionnaire(self, username):
        self._cursor_querry(self.__query['DelQuest']%(username))
        print(self.__query['DelQuest']%(username))
        return 0
    def checkQuest(self, username):
        self._cursor_querry(self.__query['QuestCheckUser']%(username))
        return "Wypełniona" if (bool(self.mycursor.fetchall()[0][0])) else "Nie wypełniona"
    def changePass(self,user,old, new):
        s_op = str(hashlib.md5(old.encode()).hexdigest())
        s_np = str(hashlib.md5(new.encode()).hexdigest())
        self._cursor_querry(self.__query['CheckPass']%(s_op,user))
        if(bool(self.mycursor.fetchall()[0][0])):
            self._cursor_querry(self.__query['UpdatePass']%(s_np,user))
            return 0
        return 1
    def AddOffert(self, offerTemplate):
        self._cursor_querry(self.__query['AddCar']%(
            math.floor(time.time()),
            offerTemplate.model,
            offerTemplate.year,
            offerTemplate.make,
            offerTemplate.typ
            ))
        self._cursor_querry(self.__query['GetCarID']%(
            offerTemplate.model,
            offerTemplate.year,
            offerTemplate.make,
            offerTemplate.typ
        ))
        Car_ID = (self.mycursor.fetchall()[0][0])
        self._cursor_querry(self.__query['AddOffert']%(
            offerTemplate.username,
            offerTemplate.name,
            offerTemplate.price,
            Car_ID
        ))
        self._cursor_querry(self.__query['SelectOffertID']%(
            offerTemplate.name,
            offerTemplate.username,
        ))
        Offer_ID = (self.mycursor.fetchall()[0][0])
        self._cursor_querry(self.__query['AddOffertDet']%(
            Offer_ID,
            offerTemplate.desc,
            offerTemplate.photo
        ))
        return 0
        