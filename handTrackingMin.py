# -*- coding: utf-8 -*-
'''
@Project ：VirtualCalculator 
@File    ：handTrackingMin.py
@Author  ：Jackwxiao
@Date    ：2022/4/29 15:39 
'''
import cv2
import mediapipe as mp
import time

# 获取摄像头
cap = cv2.VideoCapture(0)

mpHands = mp.solutions.hands
hands = mpHands.Hands()
mpDraw = mp.solutions.drawing_utils  # 画点工具

pTime = 0
cTime = 0

while True:
    scussess, img = cap.read()
    imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    results = hands.process(imgRGB)
    # print(results.multi_hand_landmarks)

    # 已经检测到手地标就获取每只手的信息
    if results.multi_hand_landmarks:
        for handLms in results.multi_hand_landmarks:
            # 获取地标id和地标位置
            for id, lm in enumerate(handLms.landmark):
                #  print(id, lm)
                h, w, c = img.shape
                # # 乘宽高取整
                cx, cy = int(lm.x * w), int(lm.y * h)
                print(id, cx, cy)
                # 检测地标为4的位置并把它放大填充
                if id == 4:
                    cv2.circle(img, (cx, cy), 15, (255, 0, 255), cv2.FILLED)

            # 把地标画到手上, 并连接起来
            mpDraw.draw_landmarks(img, handLms, mpHands.HAND_CONNECTIONS)

    # 获取帧率
    cTime = time.time()
    fps = 1 / (cTime - pTime)
    pTime = cTime
    # 显示帧率数字
    cv2.putText(img, str(int(fps)), (10, 70), cv2.FONT_HERSHEY_PLAIN, 3, (255, 0, 255), 3)

    cv2.imshow('heyhey', img)
    cv2.waitKey(1)
