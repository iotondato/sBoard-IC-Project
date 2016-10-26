#!/usr/bin/python

""" Brenno T. De Faria """
""" Projeto de IC """
""" Modulo De Detecao Imagem.0 """

import numpy as np
import cv2
from picamera.array import PiRGBArray
from picamera import PiCamera
import time
import Lousa as brd
import analyzer


def init ():

    # rawCapture = PiRGBArray(camera)
    return camera


def backCamCapture(img, camera):
    camera.capture('images/back.jpg')
    back = cv2.imread('images/back.jpg')
    back = cv2.cvtColor(back, cv2.COLOR_BGR2GRAY)

    """
    # DESKTOP VERSION
    ret, fgbg = img.read()
    frame = cv2.cvtColor(fgbg, cv2.COLOR_BGR2GRAY)
    return frame
    """

def frameCamCapture(img, camera):

    camera.capture('images/frame.jpg')
    frame = cv2.imread('images/frame.jpg')
    """
    ret, frame = img.read()
    return frame
    """

if __name__ == '__main__':
    board_list = []
    i = 0

    camera = PiCamera()
    camera.resolution = (720, 480)
    camera.framerate = 15

    """
    img = cv2.VideoCapture(0)
    time.sleep(0.1)
    """
    back = backCamCapture(camera)

    while True:
        # ====================== Captura Do Frame da Lousa =======================
        frame = frameCamCapture(camera)
        board = brd.lousa(frame)
        board_list.append(board)
        print board_list
        # ========================================================================

        # ============= Subtracao De Fundo Para As imagens da lista ==============
        diff_frame  = analyzer.backgroundSubstraction(back, frame)
        #analyzer.histogram(diff_frame)
        # print diff_frame
        # ========================================================================

        # ============================= Entropia =================================
        #cv2.imwrite('image/histogram.png', analyzer.histogram(diff_frame)
        # analyzer.histogram(diff_frame)
        # --> entropia de shanon
        # --> np.argmax() para saber qual o indice que comtem a imagem com
        # maior quantidade de infirmacao
        # ========================================================================

        # ============================ Envio de Imagem ===========================
        # --> busca da imagen selecionanda
        # --> envio da lousa selecionanda
        # --> limpa imagens anteriores
        # ========================================================================

        # ========================== Show Images =================================

        cv2.imshow('diff_frame', diff_frame)
        cv2.imshow('back', back)
        cv2.imshow('frame', frame)
        # ========================================================================

        i += 1

        k = cv2.waitKey(30) & 0xff
        if k == 27:
            break

        if k == 122:
            backCamCapture(camera)

    img.release()
    cv2.destroyAllWindows()

