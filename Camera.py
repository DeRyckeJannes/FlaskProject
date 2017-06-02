import picamera
import datetime
from pytz import timezone
import time

Brussels = timezone("Europe/Brussels")
currentTime = time.strftime("%H:%M")
print(currentTime)
camera = picamera.PiCamera()
camera.capture("/home/pi/Fotos/image.png");
photoMoments=["07:00","08:00","09:00","10:00","11:00","12:00","13:00","14:00","15:00","16:00","17:00","18:00","19:00","20:00","21:00"]
photoTaken=[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
while True:
    currentTime = time.strftime("%H:%M")
    for i in range(0,len(photoMoments)):
        if currentTime==photoMoments[i] and photoTaken[i]==0:
            print("foto nemen")
            photoTaken[i]=1
            camera.capture("/home/pi/Fotos/image"+str(i)+".png")

        if currentTime=="22:00": #after the last picture reset list, so that the next day we can take new pictures
            for i in range(0,len(photoTaken)):
                photoTaken[i]=0





# foto openen in command line kan met gpicview XMING moet actief zijn.
# klok oproepen en kijken of het tijd is voor een foto
