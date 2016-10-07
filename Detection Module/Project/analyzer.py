#!/usr/bin/python

""" Brenno T. De Faria """
""" Projeto de IC """
""" Modulo De Detecao Imagem.1 """

import numpy as np
import cv2
from matplotlib import pyplot as plt


# funcao para subitrair o fundo
def backgroundSubstraction(back, frame):
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    diff_frame = cv2.absdiff(back, frame)
    cv2.multiply(diff_frame, diff_frame, diff_frame, 2)

    return diff_frame


# funcao para gerar um histograma da imagem
def histogram(diff_frame):
    plt.hist(diff_frame.ravel(), 256, [0, 256])
    # plt.show()
    # plt.savefig('images/histogram.png')
    #hist = cv2.calcHist([diff_frame], [0], None, [256], [0, 256])
    #return hist


def shannonEntropy(Img_histogram):
    return
