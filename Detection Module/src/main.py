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

#def backDeinition():


if __name__ == '__main__':
    board_list = []
    shannon_list = []
    probs_list = []
    i = 0

    # lista_de_teste()
    # ================ RASP CAM ==================
    """
    camera = PiCamera()
    camera.resolution = (720, 480)
    camera.framerate = 15
    """
    # ============================================

    img = cv2.VideoCapture(0)
    time.sleep(0.1)

    back = cmra.backCamCapture(img)

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
        diff_frame  = cmra.backgroundSubstraction(back, frame )
        # diff_frame = cv2.imread('images/big_black.jpg')
        probs_list = cmra.probArray(cmra.histogram(diff_frame), cmra.imageSize(diff_frame))

        shannon_list.append(cmra.shannonEntropy(probs_list))
        print "Lista de Entropias"
        print shannon_list
        print
        print "Index: "
        print np.argmax(shannon_list)
        print
        # --> np.argmax() para saber qual o indice que comtem a imagem com
        # maior quantidade de infirmacao
        # ========================================================================

        # ============================ Envio de Imagem ===========================
        # --> envio da lousa selecionanda
        # --> limpa imagens anteriores
        # ========================================================================

        # ========================== Show Images =================================

        #cv2.imshow('diff_frame', diff_frame)
        #cv2.imshow('back', back)
        #cv2.imshow('frame', board_list[i])
        # ========================================================================

        # i += 1

        k = cv2.waitKey(0) & 0xff

        if k == 27:
            break

        if k == 122:
            cmra.backCamCapture(img)
            # ================ RASP CAM ==================
            """
            camera.capture('images/back.jpg')
            back = cv2.iread('images/back.jpg')
            back = cv2.cvtColor(back, cv2.COLOR_BGR2GRAY)
            """
            # ============================================

    #img.release()
    #cv2.destroyAllWindows()

