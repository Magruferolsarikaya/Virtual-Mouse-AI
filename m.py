import cv2
import mediapipe as mp
import pyautogui
import math
pyautogui.PAUSE=0.05

mp_hands=mp.solutions.hands
mp_drawing=mp.solutions.drawing_utils
clicked=False
hands=mp_hands.Hands(max_num_hands=1,min_detection_confidence=0.7)
camera=cv2.VideoCapture(0)
screen_width,screen_height=pyautogui.size()

oldX=0
oldY=0
smoothing =5

while True:
 success,frame=camera.read()
 if not success:
  break
 frame=cv2.flip(frame,1)
 rgb_frame=cv2.cvtColor(frame,cv2.COLOR_BGR2RGB)
 result=hands.process(rgb_frame)
 if result.multi_hand_landmarks:
  for hand_landmarks in result.multi_hand_landmarks:
   mp_drawing.draw_landmarks(frame,hand_landmarks,mp_hands.HAND_CONNECTIONS)
   fingerX=hand_landmarks.landmark[8].x
   fingerY=hand_landmarks.landmark[8].y
   thumbX=hand_landmarks.landmark[4].x
   thumbY=hand_landmarks.landmark[4].y
   distance=math.hypot(fingerX-thumbX,fingerY-thumbY)
   coordinateX=int(fingerX*screen_width)
   coordinateY=int(fingerY*screen_height)
   oldX=oldX+(coordinateX-oldX)/smoothing
   oldY=oldY+(coordinateY-oldY)/smoothing
   pyautogui.moveTo(int(oldX),int(oldY))
   if distance<0.05 and clicked==False:
    pyautogui.mouseDown()
    clicked=True
   elif distance> 0.05 and clicked==True:
    pyautogui.mouseUp()
    clicked=False
 cv2.imshow("sanal fare",frame)
 if cv2.waitKey(1)& 0xFF==27:
  break
camera.release()
cv2.destroyAllWindows()  
