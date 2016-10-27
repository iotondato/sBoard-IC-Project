#!/usr/bin/python

""" Brenno T. De Faria """
""" Projeto de IC """
""" Modulo De Detecao Imagem.1 """

import numpy as np
import cv2
import math
# import matplotlib.mlab as mlab
# import matplotlib.pyplot as plt

def backgroundSubstraction(back, frame):
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    diff_frame = cv2.absdiff(back, frame)
    cv2.multiply(diff_frame, diff_frame, diff_frame, 2)
    return diff_frame


# funcao para gerar um histograma da imagem
def histogram(diff_frame):
    hist = cv2.calcHist(diff_frame, [1], None, [256], [0, 255])
    # hist, bins = np.histogram(diff_frame.ravel(), 256, [0, 256])
    # plt.imshow(hist, interpolation='nearest')
    # plt.show()
    # print hist
    return hist

def shannonEntropy(Img_histogram, Img_size):
    SE = 0
    list = []
    for i in range(0, len(Img_histogram)):
        print Img_histogram[i]
        prob = Img_histogram[i] / Img_size
        print prob
        SE = prob *  math.log(prob, 2)
        SE += SE * (-1)
    print SE
