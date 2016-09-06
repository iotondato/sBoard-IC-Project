#!/usr/bin/python

import numpy as np
import cv2

if __name__ == '__main__':
    img = cv2.VideoCapture(0)
    # lousa = cv2.imread('2016-03-31 17.55.14.jpg', cv2.IMREAD_COLOR)
    #fgbg = cv2.BackgroundSubtractorMOG()
    ret,fgbg = img.read()
    back = cv2.cvtColor(fgbg, cv2.COLOR_BGR2GRAY)

    while True:
        ret, frame  = img.read()
        #frame = cv2.flip(frame, 180)
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        # cv2.multiply(frame, frame, frame, 10)
        # fgmask = fgbg.apply(frame
        fgmask = cv2.absdiff(back, frame)
        cv2.multiply(fgmask, fgmask, fgmask, 2)

        # fgmask = fgbg.apply(lousa)
        cv2.imshow('background substraction', fgmask)
        cv2.imshow('Fundo', back)
        cv2.imshow('Frente', frame)

        k = cv2.waitKey(30) & 0xff
        if k == 27:
            break
        if k == 122:
            ret, fgbg = img.read()
            back = cv2.cvtColor(fgbg, cv2.COLOR_BGR2GRAY)

    # img.release()
    cv2.destroyAllWindows()
