class DbClass:
    def __init__(self):
        import mysql.connector as connector
        self.__dsn = {
            "host": "localhost",
            "user": "remote",
            "passwd": "remote",
            "db": "weerstation"
        }
        self.__connection = connector.connect(**self.__dsn)
        self.__cursor = self.__connection.cursor()

    def getDataFromDatabase(self):
        # Query zonder parameters
        sqlQuery = "SELECT * FROM tblMeting"
        self.__cursor.execute(sqlQuery)
        result = self.__cursor.fetchall()
        self.__cursor.close()
        return result

    def getEmailsFromDatabase(self):
        # Query zonder parameters
        sqlQuery = "SELECT Email FROM tblUsers"
        self.__cursor.execute(sqlQuery)
        result = self.__cursor.fetchone()
        self.__cursor.close()
        return result

    def getPasswordsFromDatabase(self):
        # Query zonder parameters
        sqlQuery = "SELECT Password FROM tblUsers"
        self.__cursor.execute(sqlQuery)
        result = self.__cursor.fetchone()
        self.__cursor.close()
        return result

    def getUsersFromDatabase(self):
        sqlQuery = "SELECT Email,Password FROM tblUsers"
        self.__cursor.execute(sqlQuery)
        result = self.__cursor.fetchall()
        self.__cursor.close()
        return result

    # def getDataFromDatabaseMetVoorwaarde(self, voorwaarde):
    #     # Query met parameters
    #     sqlQuery = "SELECT * FROM tablename WHERE columnname = '{param1}'"
    #     # Combineren van de query en parameter
    #     sqlCommand = sqlQuery.format(param1=voorwaarde)
    #     self.__cursor.execute(sqlCommand)
    #     result = self.__cursor.fetchall()
    #     self.__cursor.close()
    #     return result
    #
    def saveContactToDatabase(self, value1, value2):
        # Query met parameters
        sqlQuery = "INSERT INTO tblContact (subject,message) VALUES ('{param1}','{param2}')"
        # Combineren van de query en parameter
        sqlCommand = sqlQuery.format(param1=value1, param2=value2)
        self.__cursor.execute(sqlCommand)
        self.__connection.commit()
        self.__cursor.close()