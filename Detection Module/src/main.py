#!/usr/bin/python

""" Brenno T. De Faria """
""" Projeto de IC """
""" Modulo De Detecao Imagem.0 """

import cv2
import numpy as np
# from picamera.array import PiRGBArray
# from picamera import PiCamera
import time
import board as brd
import cmra


if __name__ == '__main__':
    board_list = []
    shannon_list = []
    probs_list = []
    i = 0

    # ================ RASP CAM ==================
    """
    camera = PiCamera()
    camera.resolution = (720, 480)
    camera.framerate = 15
    """
    # ============================================

    img = cv2.VideoCapture(0)
    time.sleep(0.1)

    back_list = cmra.backCamCapture(img)
    back_mu = cmra.median(back_list)
    back_sig = cmra.variance(back_list, back_mu)

    #back = cmra.backMOG2()

    # ================ RASP CAM ==================
    """
    camera.capture('images/back.jpg')
    time.sleep(30)
    back = cv2.imread('images/back.jpg')
    back = cv2.cvtColor(back, cv2.COLOR_BGR2GRAY)
    """
    # ============================================

    while True:
        # ====================== Captura Do Frame da Lousa =======================
        # ================ RASP CAM ==================
        """
        camera.capture('images/frame.jpg')
        frame = cv2.imread('images/frame.jpg')
        """
        # ============================================

        frame = cmra.frameCamCapture(img)

        # board = brd.lousa(frame)
        # board_list.append(frame)
        # print board_list
        # ========================================================================

        # ============================= Entropia =================================
        # diff_frame  = cmra.backgroundSubstraction(frame, back)
        #diff_frame = cmra.substractionMOG2(frame, back_mu)
        diff_frame = cmra.gaussianSubstractor(frame, back_mu, back_sig)
        # diff_frame = cv2.imread('images/big_black.jpg')

        #cmra.median()


        #probs_list = cmra.probArray(cmra.histogram(diff_frame), cmra.imageSize(diff_frame))

        #shannon_list.append(cmra.shannonEntropy(probs_list))

        print "Lista de Entropias"
        print shannon_list
        print

        print "shannon_list size:"
        print len(shannon_list)
        print

        print "Index: "
        #eprint np.argmax(shannon_list)
        print
        # --> np.argmax() para saber qual o indice que comtem a imagem com
        # maior quantidade de infirmacao
        # ========================================================================

        # ============================ Envio de Imagem ===========================
        # --> envio da lousa selecionanda
        # --> limpa imagens anteriores
        # ========================================================================

        # ========================== Show Images =================================
        #frame = cv2.resize(frame, (720, 480))
        #cv2.imshow('diff_frame', diff_frame)
        #cv2.imshow('Mu', back_mu)
        #cv2.imshow('Sigma', back_sig)
        # ========================================================================

        # i += 1

        k = cv2.waitKey(30) & 0xff

        if k == 27:
            break

        """elif k == 122:
            #  cmra.backCamCapture(img)
            back = cmra.backMOG2()
            # ================ RASP CAM ==================

            camera.capture('images/back.jpg')
            back = cv2.iread('images/back.jpg')
            back = cv2.cvtColor(back, cv2.COLOR_BGR2GRAY)
            """
            # ============================================
    img.release()
    cv2.destroyAllWindows()
