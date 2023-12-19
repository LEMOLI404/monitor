# -*- coding:utf-8 -*-
import cv2
from datetime import datetime

if __name__ == '__main__':

    video =cv2.VideoCapture(0)
    fourcc = cv2.VideoWriter_fourcc(*'DIVX')     #设置编/解码方式
    #video.set(3, 1280)
    #video.set(4, 1024)
    face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
    body_cascade = cv2.CascadeClassifier("haarcascade_fullbody.xml")
    upperbody_cascade = cv2.CascadeClassifier("haarcascade_upperbody.xml")
    lowerbody_cascade = cv2.CascadeClassifier("haarcascade_lowerbody.xml")
    file = './Videos/'+str(datetime.now().strftime("%Y %m %d - %H：%M：%S"))+'.avi'
    result =cv2.VideoWriter(file, fourcc,10,(640,480))     #保存视频

    while video.isOpened():     #判断是否成功创建视频流
        ret, frame = video.read()
        if ret is True:
            frame = cv2.flip(frame,1)     #将每一帧图像进行水平翻转
            font = cv2.FONT_HERSHEY_SIMPLEX
            datet = str(datetime.now())
            frame = cv2.putText(frame, datet, (10, 50), font, 1,
                                (0, 255, 255), 2, cv2.LINE_AA)
            
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)     # 转换为灰度图像
            faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))     # 检测面部
            bodies = body_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))     # 检测人体(全身)
            upperbodies = upperbody_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))     # 检测人体(上半身)
            lowerbodies = lowerbody_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))     # 检测人体(下半身)

            for (x, y, w, h) in faces:
                cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 3)     # 标记面部区域
            for (x, y, w, h) in bodies:  
                cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 0, 255), 3)     # 标记人体区域(全身)
            if len(bodies) == 0:
                for (x, y, w, h) in upperbodies:  
                    cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 0, 255), 3)     # 标记人体区域(上半身)
                for (x, y, w, h) in lowerbodies:  
                    cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 0, 255), 3)     # 标记人体区域(下半身)

            if  len(faces)|len(bodies)|len(upperbodies)|len(lowerbodies) > 0 :     #人体识别
                result.write(frame)     #保存视频
                warning = "Warning: Trespass, please leave!"
                rame = cv2.putText(frame, warning, (50, 250), font, 1,
                                (0, 0, 255), 2,cv2.LINE_AA)
                
            cv2.imshow('Video',frame)
            
            if cv2.waitKey(1) == 27:     #按下‘Esc’退出
                break
        else:
            break

    video.release()
    cv2.destroyAllWindows()

