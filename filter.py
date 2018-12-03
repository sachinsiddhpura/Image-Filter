import numpy as np 
import cv2

cap=cv2.VideoCapture(0)

#for negative filter like invter
def negative_filter(frame):
    return cv2.bitwise_not(frame)

def verify_filter(frame):
    try:
        frame.shape[3]
    except IndexError:
        frame=cv2.cvtColor(frame,cv2.COLOR_BGR2BGRA)
    return frame

#choose what color you want to show
def color_overlay(frame,intensity=0.3,blue=0,green=0,red=0):
    frame=verify_filter(frame)
    frame_h, frame_w, frame_c=frame.shape
    sepia_bgra=(blue,green,red,1)
    overlay=np.full((frame_h,frame_w,4),sepia_bgra,dtype='uint8')
    cv2.addWeighted(overlay,intensity,frame,1.0,0,frame)
    frame=cv2.cvtColor(frame,cv2.COLOR_BGRA2BGR)
    return frame

#for sepia filter
def sepia_filter(frame,intensity=0.3):
    frame=verify_filter(frame)
    frame_h, frame_w, frame_c=frame.shape
    blue=20
    green=70
    red=115
    sepia_bgra=(blue,green,red,1)
    overlay=np.full((frame_h,frame_w,4),sepia_bgra,dtype='uint8')
    cv2.addWeighted(overlay,intensity,frame,1.0,0,frame)
    frame=cv2.cvtColor(frame,cv2.COLOR_BGRA2BGR)
    return frame


def blended(frame1,frame2,mask):
    alpha=mask/255.0
    blended=cv2.convertScaleAbs(frame1*(1-alpha)+frame2*alpha)
    return blended

#for potrait mode
def potrait(frame):
    frame=verify_filter(frame)
    gray=cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
    _, mask=cv2.threshold(gray,120,255,cv2.THRESH_BINARY)
    mask=cv2.cvtColor(mask,cv2.COLOR_GRAY2BGRA)
    blured=cv2.GaussianBlur(frame,(21,21),11)
    blend=blended(frame,blured,mask)
    frame=cv2.cvtColor(blend,cv2.COLOR_BGRA2BGR)
    return frame

def center_focus(frame,intensity=0.3):
    frame=verify_filter(frame)
    frame_h, frame_w, frame_c=frame.shape
    y=int(frame_h/2)
    x=int(frame_w/2)
    radius=int(y/2)
    center=(x,y)
    mask=np.zeros((frame_h, frame_w, 4),dtype='uint8')
    cv2.circle(mask,center,radius,(255,255,255),-1,cv2.LINE_AA)
    mask=cv2.GaussianBlur(mask,(21,21),11)
    blured=cv2.GaussianBlur(frame,(21,21),11)
    blend=blended(frame,blured,255-mask)
    frame=cv2.cvtColor(blend,cv2.COLOR_BGRA2BGR)
    return frame

while(True):
    ret, frame=cap.read()

    pot=potrait(frame)
    cv2.imshow('Potrait Mode',pot)

    coverlay=color_overlay(frame.copy(),red=230,blue=10)
    cv2.imshow('Color Overlay',coverlay)

    cfocus=center_focus(frame)
    cv2.imshow("Circular Center Focus",cfocus)

    sepia=sepia_filter(frame)
    cv2.imshow('This is a Sepia Filter',sepia)

    negative=negative_filter(frame)
    cv2.imshow('negative_filter',negative)

    cv2.imshow('simple_filter',frame)
    if cv2.waitKey(20) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()