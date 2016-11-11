#!/usr/bin/python

""" Brenno T. De Faria """
""" Projeto de IC """
""" Modulo De Detecao Imagem.1 """

import numpy as np
import cv2
import math
import matplotlib.mlab as mlab
import matplotlib.pyplot as plt
import os, PIL
from PIL import Image

def backCamCapture(camera):
    # DESKTOP VERSION
    back_list = []
    pixel = 0
    # height, width = 0

    for i in range(0, 2):
        ret, back = camera.read()
        frame = cv2.cvtColor(back, cv2.COLOR_BGR2GRAY)
        height, width = frame.shape[:2]
        #cv2.imwrite('images/frame' + str(i) + '.bmp', frame)
        back_list.append(frame)



    # Assuming all images are the same size, get dimensions of first image
    # w, h = Image.open(back_list[0]).size
    N = len(back_list)

    # Create a numpy array of floats to store the average (assume RGB images)
    arr = np.zeros((height, width, 3), np.float)

    # Build up average pixel intensities, casting each image as an array of floats
    for im in back_list:
        imarr = np.array(Image.open(im), dtype=np.float)
        arr = arr + imarr / N

    # Round values in array and cast as 8-bit integer
    arr = np.array(np.round(arr), dtype=np.uint8)

    # Generate, save and preview final image
    frame_out = Image.fromarray(arr, mode="RGB")

    """
    for i in range(0, width):
        for j in range(0, height):
            for k in range(0, len(back_list)):
                pixel += back_list[0][i][j]
                pixel = pixel/ (height * width)
    """

    print 'pixel: '
    print len(back_list[0])
    print len(back_list[0][0])
    # print len(back_list[0][0][0])

    # for j in range(0, len(back_list)):

      #  frame += back_list[i]
      # frame = frame / len(back_list)

    # frame = cv2.resize(frame, (720, 480))
    cv2.imshow('back', frame_out)
    # print 'back list: '
    # print back_list
    # print

    return frame_out


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

    # frame = cv2.resize(frame, (720, 480))
    # cv2.imshow('frame', frame)
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
