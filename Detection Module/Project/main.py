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

"""
def backCamCapture(camera):
    # DESKTOP VERSION
    ret, fgbg = img.read()
    frame = cv2.cvtColor(fgbg, cv2.COLOR_BGR2GRAY)
    return frame
"""
"""
def frameCamCapture(camera):
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

    # back = backCamCapture(img)

    camera.capture('images/back.jpg')
    back = cv2.imread('images/back.jpg')
    back = cv2.cvtColor(back, cv2.COLOR_BGR2GRAY)


    while True:
        # ====================== Captura Do Frame da Lousa =======================

        camera.capture('images/frame.jpg')
        frame = cv2.imread('images/frame.jpg')

        # frame = frameCamCapture(img)
        # board = brd.lousa(frame)
        # board_list.append(board)
        # print board_list
        # ========================================================================

        # ============================= Entropia =================================
        diff_frame  = analyzer.backgroundSubstraction(back, frame)
        hist = analyzer.histogram(diff_frame)
        analyzer.shannonEntropy(hist,720*480 )
        # --> np.argmax() para saber qual o indice que comtem a imagem com
        # maior quantidade de infirmacao
        # ========================================================================

        # ============================ Envio de Imagem ===========================
        # --> busca da imagen selecionanda
        # --> envio da lousa selecionanda
        # --> limpa imagens anteriores
        # ========================================================================

        # ========================== Show Images =================================

        # cv2.imshow('diff_frame', diff_frame)
        # cv2.imshow('back', back)
        # cv2.imshow('frame', frame)
        # ========================================================================

        i += 1

        k = cv2.waitKey(30) & 0xff
        if k == 27:
            break

        if k == 122:
            # backCamCapture(img)

            camera.capture('images/back.jpg')
            back = cv2.imread('images/back.jpg')
            back = cv2.cvtColor(back, cv2.COLOR_BGR2GRAY)

    # img.release()
    # cv2.destroyAllWindows()

