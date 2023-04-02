import cv2
video = cv2.VideoCapture(0)
import numpy as np
import playsound
import threading

Alarm_Status = False
Fire_Reported = 0


def play_alarm_sound_function():
	while True:
		playsound.playsound('./alarm-sound.mp3',True)

while True:
    ret, frame =video.read()

    if ret == False:
        break

    blur = cv2.GaussianBlur(frame, (21, 21), 0)
    hsv = cv2.cvtColor(blur, cv2.COLOR_BGR2HSV)

    lower = [18, 50, 50]
    upper = [35, 255, 255]
    lower = np.array(lower, dtype="uint8")
    upper = np.array(upper, dtype="uint8")

    mask = cv2.inRange(hsv, lower, upper)
    output = cv2.bitwise_and(frame, hsv, mask=mask)


    no_red = cv2.countNonZero(mask)

    if int(no_red) > 15000:
        print('Fire Detected')
        Fire_Reported = Fire_Reported + 1

    if Fire_Reported >= 1:
        if Alarm_Status == False:
            threading.Thread(target=play_alarm_sound_function).start()
            Alarm_Status = True


    cv2.imshow("output",output)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break


cv2.destroyAllWindows()
video.release()