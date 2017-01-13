#!/usr/bin/python

""" Brenno T. De Faria """
""" Projeto de IC """
""" Modulo De Detecao Imagem.1 """

import numpy as np
import cv2
import math
import scipy.stats
import pylab
import matplotlib
# import matplotlib.pyplot as plt
# import os, PIL
# from PIL import Image

#========= Amostras de Imagens de Fundo ==========#

def backCamCapture(camera):
    # DESKTOP VERSION
    back_list = []
    px = 0

    #Captura 30 imagens para criar a imagem de fundo
    for i in range(1, 11):
        ret, back_frame = camera.read()
        back_frame = cv2.cvtColor(back_frame, cv2.COLOR_BGR2GRAY)
        height, width = back_frame.shape[:2]
        cv2.imwrite('images/back_frame' + str(i) + '.bmp', back_frame)
        back_list.append(back_frame)

    print back_list
    print
    print len(back_list)
    return back_list

#=================================================#


# ============= Captura de imagens ===============#

def backMOG2():
    fgbg = cv2.BackgroundSubtractorMOG2(40, 122)
    return fgbg


def frameCamCapture(camera):
    ret, frame = camera.read()
    #frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    cv2.imwrite('images/frame.bmp', frame)
    #i += 1
    return frame

#=================================================#


#============= Operacoes com Imagens =============#

def imageSize(frame):
    height, width = frame.shape[:2]
    Img_size = height * width
    return Img_size


def suma(Img_histogram):
    sum = 0
    for i in range(0, len(Img_histogram)):
        sum  += Img_histogram[i]
    return sum


def median(back_list):
    """back_list = [[[179, 176, 165],
                  [168, 154, 158],
                  [157, 158, 155]],

                 [[158, 161, 158],
                  [161, 156, 154],
                  [169, 171, 180]],

                 [[186, 184, 171],
                  [169, 154, 157],
                  [168, 159, 157]]]"""

    height, width = back_list[0].shape[:2]
    #height = 3
    #width = 3
    px = 0
    back_mu = np.zeros(shape=(height, width))

    for i in xrange(0, width):
        for j in xrange(0, height):
            for k in xrange(0, len(back_list)):
                px += back_list[k][j][i]
            px = px / len(back_list)
            back_mu[j][i] =  px
            px = 0

    print 'Frame Medio: '
    print back_mu
    print

    cv2.imwrite('images/back_median.bmp', back_mu)
    return back_mu


def variance(back_list, back_mu):
    height, width = back_list[0].shape[:2]
    back_sig = np.zeros(shape=(height, width))
    des = 0
    vri = 0
    px = 0

    for i in xrange(0, width):
        for j in xrange(0, height):
            for k in xrange(0, len(back_list)):
                des += (back_list[k][j][i] - back_mu[j][i])**2
            des = des / len(back_list)
            vri = pow(des, 0.5)
            back_sig[j][i] = vri
            vri = 0

    print 'Frame Desvio Padrao: '
    print back_sig
    print

    cv2.imwrite('images/back_variance.bmp', back_sig)
    return back_sig

#=================================================#


# ======= Metodos de Subtracao de Fundo ==========#

def backgroundSubstraction(frame, back):
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    # cv2.equalizeHist(frame, frame)

    diff_frame = cv2.absdiff(back, frame)
    ret, diff_frame = cv2.threshold(diff_frame, 125, 255, cv2.THRESH_BINARY)

    frame = cv2.resize(frame, (720, 480))
    cv2.imshow('diff_frame', diff_frame)
    cv2.imshow('frame', frame)
    cv2.imshow('back', back)
    return frame


def substractionMOG2(frame, fgbg):
    fgmask = fgbg.apply(frame)
    ret, fgmask = cv2.threshold(fgmask, 152, 255, cv2.THRESH_BINARY)
    return fgmask


def gaussianSubstractor(frame, back_mu, back_sig):
    height, width = back_mu.shape[:2]
    nopdf = 0
    diff_frame = np.zeros(shape=(height, width))

    for i in xrange(0, width):
        for j in xrange(0, height):

            nopdfr = pylab.normpdf(frame[j][i][0], back_mu[j][i], back_sig[j][i])
            nopdfg = pylab.normpdf(frame[j][i][1], back_mu[j][i], back_sig[j][i])
            nopdfb = pylab.normpdf(frame[j][i][2], back_mu[j][i], back_sig[j][i])

            nopdf = pow(nopdfr*nopdfg*nopdfb, 0.333333)

            print nopdfr
            print nopdfg
            print nopdfb
            print nopdf

            #px = limiarization(nopdf)
            #diff_frame[j][i] = nopdf

    print frame
    print
    print diff_frame
    print
    #cv2.imwrite('images/diff_frame.bmp', diff_frame)
    cv2.imshow('diff frame', diff_frame)
    return diff_frame


def limiarization(value):
    px = 0
    if value > 1:
        px = 255
    return px

#def normalDistribuition(frame):


# ================================================#

# ============ Analise de Imagens ================#

def histogram(diff_frame):
    hist, bins = np.histogram(diff_frame.ravel(), 10, [0, 256])
    return hist


def probArray(Img_histogram, Img_size):
    list_prob = []
    for i in range(0, len(Img_histogram)):
        Img_prob = (float(Img_histogram[i]) / 3) / Img_size
        list_prob.append(Img_prob)
    return list_prob


def shannonEntropy(list_prob):
    SE = 0
    list_shannon = []
    for i in range(0, len(list_prob)):
        if list_prob[i] != 0:
            SE += list_prob[i] *  math.log(list_prob[i], 2)
    SE = -SE
    return SE


# ================================================#