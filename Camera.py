
class PiCam:
    def __init__(self):
        import picamera
        import time
        self.__camera=picamera.PiCamera()
        self.__photoMoments = ["07", "08", "09", "10", "11", "12", "13", "14", "15", "16",
                        "17", "18", "19", "20", "21"]
        self.__photoTaken = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        self.__currentTime=time.strftime("%H")

    def checkForPicture(self):
        print("check if we still need to take a picture this hour")
        for i in range(0, len(self.__photoMoments)):
            if self.__currentTime == self.__photoMoments[i] and self.__photoTaken[i] == 0:
                print("foto nemen")
                self.__camera.capture("/home/pi/FlaskProject/static/images/Picam.jpg")
                self.__photoTaken[i] = 1
                self.__camera.close()
            if self.__currentTime == "22":  # after the last picture reset list, so that the next day we can take new pictures
                for i in range(0, len(self.__photoTaken)):
                    self.__photoTaken[i] = 0

# foto openen in command line kan met gpicview XMING moet actief zijn.
# klok oproepen en kijken of het tijd is voor een foto
#mmal of picamera.exc picamerammalerror failed to enalbe connection out of resources ? --> enable camera in raspi-config