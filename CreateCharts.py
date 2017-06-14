class History():
    import datetime
    from DbClass import DbClass
    def __init__(self):
        self.__HourlyTemp = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        self.__HourlyHum = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        self.__HourlyWindSpeed = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        self.__ChartHours = ["07", "08", "09", "10", "11", "12", "13", "14", "15", "16", "17", "18", "19", "20", "21"]
        self.__checkChartHourly = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        self.__checkChartDaily = [0, 0, 0, 0, 0, 0, 0]
        self.__TempsThroughDay = [[], [], [], [], [], [], []]
        self.__HumThroughDay = [[], [], [], [], [], [], []]
        self.__WindSpeedsThroughDay = [[], [], [], [], [], [], []]
        self.__DailyTemp = [0, 0, 0, 0, 0, 0, 0]
        self.__DailyHum = [0, 0, 0, 0, 0, 0, 0]
        self.__DailyWindSpeed = [0, 0, 0, 0, 0, 0, 0]
        self.__ChartDays = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']

    def Hourly(self):
        today = self.datetime.datetime.today()
        currentYear = today.year
        currentYear = str(currentYear)
        currentMonth = today.strftime("%m")
        currentDay = today.strftime("%d")
        currentHour = today.strftime("%H")
        DB_Layer = self.DbClass()
        data = DB_Layer.getDataFromDatabase()
        for values in data:
            DATETIME = values[4]
            DATETIME = str(DATETIME)
            dbhour = DATETIME[11:13]
            dbday = DATETIME[8:10]
            dbmonth = DATETIME[5:7]
            dbyear = DATETIME[0:4]
            for i in range(0, len(self.__HourlyTemp)):
                if (dbhour == self.__ChartHours[i] and self.__checkChartHourly[
                    i] == 0 and dbday == currentDay and dbmonth == currentMonth and dbyear == currentYear):
                    self.__HourlyTemp[i] = values[0]
                    self.__HourlyHum[i] = values[2]
                    self.__HourlyWindSpeed[i] = values[1]
                    self.__checkChartHourly[i] = 1
                    return self.__HourlyTemp, self.__HourlyHum, self.__HourlyWindSpeed
                if currentHour == "23":
                    for i in range(0, len(self.__checkChartHourly)):
                        self.__checkChartHourly[i] = 0
        return self.__HourlyTemp, self.__HourlyHum, self.__HourlyWindSpeed

    def Daily(self):
        today = self.datetime.datetime.today()
        currentYear = today.year
        currentYear = str(currentYear)
        currentWeekDay = today.weekday()
        currentWeekDay = str(currentWeekDay)
        currentMonth = today.strftime("%m")
        currentDay = today.strftime("%d")
        currentHour = today.strftime("%H")
        currentWeekNumber=self.datetime.date(int(currentYear),int(currentMonth),int(currentDay)).isocalendar()[1]
        averageTemp = 0
        averageHum = 0
        averageWindSpeed = 0
        DB_Layer = self.DbClass()
        data = DB_Layer.getDataFromDatabase()
        for values in data:
            DATETIME = values[4]
            DATETIME = str(DATETIME)
            dbhour = DATETIME[11:13]
            dbday = DATETIME[8:10]
            dbmonth = DATETIME[5:7]
            dbyear = DATETIME[0:4]
            d = self.datetime.date(int(dbyear), int(dbmonth), int(dbday))
            dbWeekDay = d.strftime('%A')
            dbWeekNumber=self.datetime.date(int(dbyear),int(dbmonth),int(dbday)).isocalendar()[1]
            for i in range(0, len(self.__DailyTemp)):
                if (dbWeekDay == self.__ChartDays[i] and currentWeekNumber== dbWeekNumber and dbmonth == currentMonth and dbyear == currentYear):  # we take the average of all of the measurements of that day
                    self.__TempsThroughDay[i].append(values[0])
                    for temp in self.__TempsThroughDay[i]:
                        averageTemp += temp
                    averageTemp = round(averageTemp / len(self.__TempsThroughDay[i]),2)
                    self.__DailyTemp[i] = averageTemp
                    self.__HumThroughDay[i].append(values[2])
                    for hum in self.__HumThroughDay[i]:
                        averageHum += hum
                    averageHum = round(averageHum / len(self.__HumThroughDay[i]),2)
                    self.__DailyHum[i] = averageHum

                    self.__WindSpeedsThroughDay[i].append(values[1])
                    for WindSpeeds in self.__WindSpeedsThroughDay[i]:
                        averageWindSpeed += WindSpeeds
                    averageWindSpeed = round(averageWindSpeed / len(self.__WindSpeedsThroughDay[i]),2)
                    self.__DailyWindSpeed[i] = averageWindSpeed
        return self.__DailyTemp, self.__DailyHum, self.__DailyWindSpeed



