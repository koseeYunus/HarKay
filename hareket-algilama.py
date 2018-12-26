import cv2
from datetime import datetime
import time

def farkImaj(t0,t1,t2):
    fark1=cv2.absdiff(t2,t1)
    fark2 = cv2.absdiff(t1, t0)
    return cv2.bitwise_and(fark1,fark2)

esik_deger=90000

kamera=cv2.VideoCapture(0)
#kamera=cv2.VideoCapture("rtsp://admin:admin@192.168.1.119")

insan_cascade=cv2.CascadeClassifier('yuzAlgila.xml')

pencereIsmi="Hareket Algilayici"
cv2.namedWindow(pencereIsmi)

t_eksi=cv2.cvtColor(kamera.read()[1],cv2.COLOR_BGR2GRAY)
t=cv2.cvtColor(kamera.read()[1],cv2.COLOR_BGR2GRAY)
t_arti=cv2.cvtColor(kamera.read()[1],cv2.COLOR_BGR2GRAY)

zamanKontrol=datetime.now().strftime('%Ss')

while True:
    _,frame=kamera.read()
    gray=cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
    #cv2.imshow(pencereIsmi,kamera.read()[1])

    if cv2.countNonZero(farkImaj(t_eksi,t,t_arti))>esik_deger and zamanKontrol !=datetime.now().strftime('%Ss'):
        fark_resim=kamera.read()[1]
        cv2.imwrite("temp/"+datetime.now().strftime('%Y %m %d _ %Hh %Mm %Ss')+'.jpg' ,fark_resim)
        print("girildi")
        time.sleep(1)

    insan = insan_cascade.detectMultiScale(gray, 1.3, 2)

    for (x, y, w, h) in insan:
        cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 255, 0), 3)

    cv2.imshow('HareketAlgila',frame)

    zamanKontrol = datetime.now().strftime('%Ss')
    t_eksi=t
    t=t_arti
    t_arti=cv2.cvtColor(kamera.read()[1],cv2.COLOR_BGR2GRAY)

    key=cv2.waitKey(10)
    if key==27 or cv2.waitKey(25) & 0xFF==ord('q'):
        cv2.destroyAllWindows()
        break

