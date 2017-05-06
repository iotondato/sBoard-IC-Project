#!/usr/bin/python

""" Brenno T. De Faria """
""" Projeto de IC """
""" Modulo De Detecao Imagem.1 """

import numpy as np
import cv2
import math
import pylab
from matplotlib import pyplot as plt
import pytesseract
from tesserocr import PyTessBaseAPI


# ========= Amostras de Imagens de Fundo ==========#

def backCamCapture(camera):
    # DESKTOP VERSION
    back_list = []
    px = 0

    # Captura 30 imagens para criar a imagem de fundo
    for i in range(0, 30):
        ret, back_frame = camera.read()
        #back_frame = cv2.resize(back_frame, (240, 120))
        back_frame = frameNormalization(back_frame)
        back_list.append(back_frame)

    return back_list

# =================================================#


# ============= Captura de imagens ===============#

def backMOG2():
    fgbg = cv2.BackgroundSubtractorMOG2(40, 122)
    return fgbg


def frameCamCapture(camera):
    ret, frame = camera.read()
    #frame = cv2.resize(frame, (240, 120))
    frame = frameNormalization(frame)
    #cv2.imwrite('images/frame.bmp', frame)
    return frame

# =================================================#


# ============= Operacoes com Imagens =============#

def frameNormalization(frame):
    rgblist = len(frame[0][0])
    height = len(frame)
    width = len(frame[0])
    Nframe = np.zeros(shape=(height, width, rgblist), dtype=float)

    #Nframe  = frame / 255
    Nframe  = np.divide(frame + 0.0, 255)

    """for i in xrange(0, height):
        for j in xrange(0, width):
            npxr = np.divide(frame[i][j][0] + 0.0, 255)
            Nframe[i][j][0] = npxr
            npxg = np.divide(frame[i][j][1] + 0.0, 255)
            Nframe[i][j][1] = npxg
            npxb = np.divide(frame[i][j][2] + 0.0, 255)
            Nframe[i][j][2] = npxb
            #npx = np.divide(frame[i][j] + 0.0, 255)
            #Nframe[i][j] = npx
            npx = 0
    """
    return Nframe


def imageSize(frame):
    height, width = frame.shape[:2]
    Img_size = height * width
    return Img_size


def suma(Img_histogram):
    sum = 0
    for i in range(0, len(Img_histogram)):
        sum += Img_histogram[i]
    return sum


def median(back_list):
    pxr = 0.0
    pxg = 0.0
    pxb = 0.0
    height = len(back_list[0])
    width = len(back_list[0][0])
    rgblist  = len(back_list[0][0][0])

    print rgblist

    back_mu = np.zeros(shape=(height, width, rgblist), dtype=float)

    """for i in xrange(0, height):
        for j in xrange(0, width):
            for k in xrange(0, len(back_list)):
                pxr += back_list[k][i][j][0]
                pxg += back_list[k][i][j][1]
                pxb += back_list[k][i][j][2]
            pxr /= len(back_list)
            pxg /= len(back_list)
            pxb /= len(back_list)
            back_mu[i][j][0] = pxr
            back_mu[i][j][1] = pxg
            back_mu[i][j][2] = pxb
    """

    for i in xrange(0, len(back_list)):
        back_mu += back_list[i]
    back_mu = np.divide(back_mu, len(back_list))

    # back_mu = np.mean(back_list)
    print 'Frame Medio: '
    print back_mu
    print

    #cv2.imwrite('images/back_mu.bmp', back_mu)
    return back_mu


def standardDeviation(back_list, back_mu):
    height = len(back_list[0])
    width = len(back_list[0][0])
    rgblist = len(back_list[0][0][0])

    back_sig = np.zeros(shape=(height, width, rgblist), dtype=float)
    vrir = 0
    vrig = 0
    vrib = 0

    """
    for i in xrange(0, height):
        for j in xrange(0, width):
            for k in xrange(0, len(back_list)):
                vrir += (back_list[k][i][j][0] - back_mu[i][j][0]) ** 2
                vrig += (back_list[k][i][j][1] - back_mu[i][j][1]) ** 2
                vrib += (back_list[k][i][j][2] - back_mu[i][j][2]) ** 2

            vrir /= len(back_list)
            vrir **= 0.5
            vrig /= len(back_list)
            vrig **= 0.5
            vrib /= len(back_list)
            vrib **= 0.5

            back_sig[i][j][0] = vrir
            back_sig[i][j][1] = vrig
            back_sig[i][j][2] = vrib
    """
    for i in xrange(0, len(back_list)):
        back_sig += np.subtract(back_list[i], back_mu) ** 2

    back_sig = np.divide(back_sig, len(back_list))
    back_sig = back_sig **0.5

    #print 'Frame Desvio Padrao: '
    #print back_sig
    #print
    #cv2.imwrite('images/back_sig.bmp', back_sig)
    return back_sig


def imgMultplication(diff_frame, frame):
    height = len(frame)
    width = len(frame[0])
    rgblist = len(frame[0][0])
    diff_mask = np.zeros(shape=(height, width, rgblist), dtype=float)

    for i in xrange(0, height):
        for j in xrange(0, width):
            if (diff_frame[i][j] == 255):
                diff_frame[i][j] = 1

            diff_mask[i][j][0] = diff_frame[i][j] * frame[i][j][0]
            diff_mask[i][j][1] = diff_frame[i][j] * frame[i][j][1]
            diff_mask[i][j][2] = diff_frame[i][j] * frame[i][j][2]

    return diff_mask


def morfOperator(diff_frame):
    kernel2 = np.ones((5, 5), np.uint8)

    kernel = np.array (
               [[0, 1, 0],
                [1, 1, 1],
                [0, 1, 0]], np.uint8)

    dilated_frame = cv2.dilate(diff_frame, kernel2, iterations = 1)

    erosed_frame = cv2.erode(dilated_frame, kernel2, iterations = 1)

    return erosed_frame


# =================================================#


# ======= Metodos de Subtracao de Fundo ==========#

def backgroundSubstraction(frame, back):
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    # cv2.equalizeHist(frame, frame)

    diff_frame = cv2.absdiff(back, frame)
    ret, diff_frame = cv2.threshold(diff_frame, 125, 255, cv2.THRESH_BINARY)
    return diff_frame


def substractionMOG2(frame, fgbg):
    fgmask = fgbg.apply(frame)
    ret, fgmask = cv2.threshold(fgmask, 152, 255, cv2.THRESH_BINARY)
    return fgmask


def gaussianSubstractor(frame, back_mu, back_sig):
    height = len(frame)
    width = len(frame[0])
    #rgblist = len(frame[0][0])
    nopdf = 0
    diff_frame = np.zeros(shape=(height, width), dtype=float)
    """
    for i in xrange(0, height):
        for j in xrange(0, width):
            normdr = pylab.normpdf(frame[i][j][0], back_mu[i][j][0], back_sig[i][j][0])
            normdg = pylab.normpdf(frame[i][j][1], back_mu[i][j][1], back_sig[i][j][1])
            normdb = pylab.normpdf(frame[i][j][2], back_mu[i][j][2], back_sig[i][j][2])
            nopdf = (normdr*normdg*normdb)**0.33333333333333333333333333333333333333333
            px = limiarization(nopdf)
            diff_frame[i][j] = px
    """
    diff_frame = pylab.normpdf(frame, back_mu, back_sig)
    for i in xrange(0, 2):
        diff_frame[:,:, 0] *= diff_frame[:, :, i] ** 0.33333333333333333333333

    #ret, diff_frame = cv2.threshold(diff_frame, 120, 255, cv2.THRESH_BINARY)
    # print 'norm frame:'
    # print diff_frame
    # diff_frame = imgMultplication(diff_frame, frame)
    cv2.imwrite('images/diff_frame.bmp', diff_frame)
    return diff_frame


def limiarization(value):
    if (value > 1):
        value = 1

    px = (1- value) * 255

    if (px >= 120):
        px = 255
    else:
        px = 0

    return px


# def normalDistribuition(frame):


# ================================================#

# ==================== Entropy ================== #

def histogram(diff_frame):
    histr, bins = np.histogram(diff_frame, 10, [0, 256])
    #histg, bins = np.histogram(diff_frame[:][:][1], 10, [0, 256])
    #histb, bins = np.histogram(diff_frame[:][:][2], 10, [0, 256])
    return histr


def probArray(Img_histogram, Img_size):
    list_prob = []
    for i in range(0, len(Img_histogram)):
        Img_prob = (float(Img_histogram[i])/3) / Img_size
        list_prob.append(Img_prob)
    return list_prob


def shannonEntropy(list_prob):
    SE = 0
    list_shannon = []
    for i in range(0, len(list_prob)):
        if list_prob[i] != 0:
            SE += list_prob[i] * math.log(list_prob[i], 2)
    SE = -SE
    return SE

# =============================================== #

# =================== OCR ======================= #
# =============================================== #

# =============================================== #

# ===================== OCR ===================== #
def OCR(diff_frame):
    with PyTessBaseAPI() as api:
        api.SetImageFile(diff_frame)
        print api.GetUTF8Text()



# =============================================== #




