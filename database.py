import mysql.connector
import config

class Database:
    def __init__(self):
        self.__query = {
            "AddCar":F"INSERT INTO Car VALUES ('%s','%s','%s')",
            "GetCars":F"SELECT * FROM Car",
            "GetCar":F"SELECT * FROM Car WHERE Car.%s = %s",
            "GetOffers_index":F"SELECT Offert.`Offert_ID`,`Title`, Offert_Detail.Thumbnail FROM `Offert` LEFT JOIN Offert_Detail ON Offert.`Offert_ID` = Offert_Detail.Offert_ID",
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
    def getCars(self):
        self._cursor_querry(self.__query['GetCars'])
        result = []
        names = []
        for x in self.mycursor:
            result.append(x)
        for x in self.mycursor._description:
            names.append(x[0])
        return (result,names)
    def getCar(self, value, column = "Model"):
        self._cursor_querry(self.__query['GetCars'])
        result = []
        names = []
        for x in self.mycursor:
            result.append(x)
        for x in self.mycursor._description:
            names.append(x[0])
        return (result,names)


        
    