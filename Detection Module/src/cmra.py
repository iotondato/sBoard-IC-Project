#!/usr/bin/python

""" Brenno T. De Faria """
""" Projeto de IC """
""" Modulo De Detecao Imagem.1 """

import numpy as np
import cv2
import math
# import matplotlib.mlab as mlab
# import matplotlib.pyplot as plt
# import os, PIL
# from PIL import Image

def backCamCapture(camera):
    # DESKTOP VERSION
    back_list = []
    px = 0

    for i in range(1, 4):
        ret, back = camera.read()
        frame = cv2.cvtColor(back, cv2.COLOR_BGR2GRAY)
        height, width = frame.shape[:2]
        cv2.imwrite('images/frame' + str(i) + '.bmp', frame)
        back_list.append(frame)

    print back_list
    print
    print len(back_list)

    back_frame = np.zeros(shape=(height, width))

    # print back_list[0][0][0]
    # print
    # print back_list[1]

    for i in xrange(0, width):
        for j in xrange(0, height):
            for k in xrange(0, len(back_list)):
                px += back_list[k][j][i]
            px = px / len(back_list)
            back_frame[j][i] =  int(px)

    cv2.imwrite('images/frame0.bmp', back_frame)
    print back_frame
    print len(back_frame)

    back = cv2.imread('images/frame0.bmp')
    back = cv2.cvtColor(back, cv2.COLOR_BGR2GRAY)

    return back


def frameCamCapture(camera):
    ret, frame = camera.read()
    i = 0
    cv2.imwrite('images/frame' + str(i) + '.bmp', frame)
    i += 1
    return frame


def imageSize(frame):
    height, width = frame.shape[:2]
    Img_size = height * width
    return Img_size


def backgroundSubstraction(back, frame):
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    # cv2.equalizeHist(frame, frame)

    diff_frame = cv2.absdiff(back, frame)
    # cv2.multiply(diff_frame, diff_frame, diff_frame, 1)

    frame = cv2.resize(frame, (720, 480))
    cv2.imshow('diff_frame', diff_frame)
    return frame


def suma(Img_histogram):
    sum = 0
    for i in range(0, len(Img_histogram)):
        sum  += Img_histogram[i]
    return sum


def histogram(diff_frame):
    hist, bins = np.histogram(diff_frame.ravel(), 10, [0, 256])
    # print "Histogram: "
    # print hist
    # print
    return hist


def probArray(Img_histogram, Img_size):
    list_prob = []
    for i in range(0, len(Img_histogram)):
        Img_prob = (float(Img_histogram[i]) / 3) / Img_size
        list_prob.append(Img_prob)

    # print "lista de probabilidade: "
    # print list_prob
    # print
    return list_prob


def shannonEntropy(list_prob):
    SE = 0
    list_shannon = []
    for i in range(0, len(list_prob)):
        if list_prob[i] != 0:
            SE += list_prob[i] *  math.log(list_prob[i], 2)
    SE = -SE
    # list_shannon.append(SE)
    # print "Shannon Entropy: "
    # print SE
    # print
    return SE
