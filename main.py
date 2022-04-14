# -*- coding: utf-8 -*-
'''
@Project ：VirtualCalculator 
@File    ：main.py
@Author  ：Jackwxiao
@Date    ：2022/4/14 13:02 
'''
import cv2
from cvzone.HandTrackingModule import HandDetector

class Button:
    def __init__(self, pos, width, height, value):
        self.pos = pos
        self.width = width
        self.height = height
        self.value = value

    def draw(self, img):
        cv2.rectangle(img, self.pos, (self.pos[0]+self.width, self.pos[1]+self.height),
                      (225, 225, 225), cv2.FILLED)
        cv2.rectangle(img, self.pos, (self.pos[0]+self.width, self.pos[1]+self.height),
                      (97, 164, 188), 3)
        # 添加文本
        cv2.putText(img, self.value, (self.pos[0] + 40, self.pos[1] + 60),
                    cv2.FONT_HERSHEY_PLAIN, 2, (26, 19, 47), 2)

    # 检查点击
    def checkClick(self, x, y):
        if self.pos[0] < x < self.pos[0] + self.width and \
                self.pos[1] < y < self.pos[1] + self.height:
            cv2.rectangle(img, self.pos, (self.pos[0] + self.width, self.pos[1] + self.height),
                          (255, 255, 255), cv2.FILLED)
            cv2.rectangle(img, self.pos, (self.pos[0] + self.width, self.pos[1] + self.height),
                          (97, 164, 188), 3)
            # 添加文本
            cv2.putText(img, self.value, (self.pos[0] + 25, self.pos[1] + 80),
                        cv2.FONT_HERSHEY_PLAIN, 5, (0, 0, 0), 5)
            return True
        else:
            return False


# webcam  摄像头
cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
cap.set(3, 1280)   # width
cap.set(4, 720)    # height
detector = HandDetector(detectionCon=0.8, maxHands=1)  # 检测置信度0.8，要确保准确的检测到手，最多一只手

# 创建按钮
buttonList = []
buttonListValues = [['7', '8', '9', '*'],
                    ['4', '5', '6', '-'],
                    ['1', '2', '3', '+'],
                    ['0', '/', '.', '=']]
for x in range(4):
    for y in range(4):
        xpos = x*100 + 800
        ypos = y*100 + 150
        buttonList.append(Button((xpos, ypos), 100, 100, buttonListValues[y][x]))
        # button1 = Button((700, 150), 100, 100, '5')

# 定义变量
myEquation = ''
# print(eval('5+5'))
delayCounter = 0

# loop
while True:
    # 从摄像头获取图像
    success, img = cap.read()
    img = cv2.flip(img, 1)   # 水平翻转，因为屏幕相对于我们使相反的

    # 检测手
    hands, img = detector.findHands(img, flipType=False)

    # 画出所有按钮
     # 画出按钮上方结果框
    cv2.rectangle(img, (800,50), (800 + 400, 70 + 100),
                  (247, 226, 226), cv2.FILLED)
    cv2.rectangle(img, (800,50), (800 + 400, 70 + 100),
                  (97, 164, 188), 3)
    for button in buttonList:
        button.draw(img)

    # processing

    # 检测手的位置
    if hands:
        lmList = hands[0]["lmList"]
        length, _, img = detector.findDistance(lmList[8], lmList[12], img)
        print(length)
        x, y = lmList[8]
        if length < 40:
            for i, button in enumerate(buttonList):
                if button.checkClick(x, y) and delayCounter == 0:
                    myValue = buttonListValues[int(i % 4)][int(i / 4)]
                    if myValue == "=":
                        myEquation = str(eval(myEquation))
                    else:
                        myEquation += myValue
                    delayCounter = 1

    # 避免重复输入
    if delayCounter != 0:
        delayCounter += 1
        if delayCounter > 10:
            delayCounter = 0

    # 显示结果
    cv2.putText(img, myEquation, (810, 120),
                cv2.FONT_HERSHEY_PLAIN, 3, (50, 50, 50), 3)



    # #显示图像
    cv2.imshow("Image", img)
    key = cv2.waitKey(1)

    if key == ord('c'):
        myEquation = ''