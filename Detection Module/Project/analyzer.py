#!/usr/bin/python

""" Brenno T. De Faria """
""" Projeto de IC """
""" Modulo De Detecao Imagem.1 """

import numpy as np
import cv2
import math
from matplotlib import pyplot as plt


# funcao para subitrair o fundo
def backgroundSubstraction(back, frame):
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    diff_frame = cv2.absdiff(back, frame)
    cv2.multiply(diff_frame, diff_frame, diff_frame, 2)

    return diff_frame


# funcao para gerar um histograma da imagem
def histogram(diff_frame):
    # plt.hist(diff_frame.ravel(), 256, [0, 256])
    hist = cv2.calcHist(diff_frame, [0], None, [256], [0, 256])
    # hist, bins = np.histogram(diff_frame.ravel(), 256, [0, 256])
    # plt.imshow(hist, interpolation='nearest')
    # plt.show()
    print hist


"""
def shannonEntropy(Img_histogram):
    SE = 0

    for i in Img_histogram:
        prob = Img_histogram[i] / Img_size
        SE = prob *  math.log(prob, 2)
        SE = -SE
    print prob
        print
    # print SE
"""