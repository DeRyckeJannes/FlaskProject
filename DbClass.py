import mysql.connector as connector
class DbClass:

    def __init__(self):

        self.__dsn = {
            "host": "localhost",
            "user": "remote",
            "passwd": "remote",
            "db": "weerstation"
        }



    def getLatestDataFromDatabase(self):
        # Query zonder parameters
        self.__connection = connector.connect(**self.__dsn)
        self.__cursor = self.__connection.cursor()
        sqlQuery = "SELECT Temperatuur,Windsnelheid,Luchtvochtigheid,RainDrop FROM tblMetingen ORDER BY ID DESC LIMIT 1"
        self.__cursor.execute(sqlQuery)
        result = self.__cursor.fetchall()
        self.__cursor.close()
        return result

    def getDataFromDatabase(self):
        # Query zonder parameters
        self.__connection = connector.connect(**self.__dsn)
        self.__cursor = self.__connection.cursor()
        sqlQuery = "SELECT Temperatuur,Windsnelheid,Luchtvochtigheid,RainDrop,DateTime FROM tblMetingen"
        self.__cursor.execute(sqlQuery)
        result = self.__cursor.fetchall()
        self.__cursor.close()
        return result
    def getEmailsFromDatabase(self):
        # Query zonder parameters
        self.__connection = connector.connect(**self.__dsn)
        self.__cursor = self.__connection.cursor()
        sqlQuery = "SELECT Email FROM tblUsers"
        self.__cursor.execute(sqlQuery)
        result = self.__cursor.fetchone()
        self.__cursor.close()
        return result

    def getPasswordsFromDatabase(self):
        # Query zonder parameters
        self.__connection = connector.connect(**self.__dsn)
        self.__cursor = self.__connection.cursor()
        sqlQuery = "SELECT Password FROM tblUsers"
        self.__cursor.execute(sqlQuery)
        result = self.__cursor.fetchone()
        self.__cursor.close()
        return result

    def getUsersFromDatabase(self):
        self.__connection = connector.connect(**self.__dsn)
        self.__cursor = self.__connection.cursor()
        sqlQuery = "SELECT ID,Email,Password FROM tblUsers"
        self.__cursor.execute(sqlQuery)
        result = self.__cursor.fetchall()
        self.__cursor.close()
        return result

    def getWeerstationIDFromUser(self,UsersID):
        self.__connection = connector.connect(**self.__dsn)
        self.__cursor = self.__connection.cursor()
        sqlQuery = "select tblWeerstations.ID from tblWeerstations join tblUsers on tblWeerstations.usersID = tblUsers.id where tblUsers.id='"+str(UsersID)+"' LIMIT 1"
        self.__cursor.execute(sqlQuery)
        result = self.__cursor.fetchone()
        self.__cursor.close()
        return result

    def saveContactToDatabase(self,userID,subject, message):
        # Query met parameters
        self.__connection = connector.connect(**self.__dsn)
        self.__cursor = self.__connection.cursor()
        sqlQuery = "INSERT INTO tblContact (userID,subject,message) VALUES ('{param1}','{param2}','{param3}')"
        # Combineren van de query en parameter
        sqlCommand = sqlQuery.format(param1=userID,param2=subject, param3=message)
        self.__cursor.execute(sqlCommand)
        self.__connection.commit()
        self.__cursor.close()

    def saveSensorValuesToDatabase(self,WeerstationID,list,moment):
        # Query met parameters
        self.__connection = connector.connect(**self.__dsn)
        self.__cursor = self.__connection.cursor()
        sqlQuery = "INSERT INTO tblMetingen (WeerstationID,Temperatuur,Windsnelheid,Luchtvochtigheid,RainDrop,DateTime) VALUES ('{param1}','{param2}','{param3}','{param4}','{param5}','{param6}')"
        # Combineren van de query en parameter
        sqlCommand = sqlQuery.format(param1=WeerstationID, param2=list[0],param3=list[1],param4=list[2],param5=list[3], param6=moment)
        self.__cursor.execute(sqlCommand)
        self.__connection.commit()
        self.__cursor.close()

