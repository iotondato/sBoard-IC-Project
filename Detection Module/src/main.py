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
    nback_list = []
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

    """
    back_list = [[[123, 125, 154],
                  [168, 164, 162],
                  [166, 118, 123]],

                 [[124, 121, 158],
                  [161, 166, 164],
                  [169, 114, 120]],

                 [[125, 124, 151],
                  [163, 164, 161],
                  [168, 119, 121]],

                 [[122, 127, 155],
                  [165, 163, 162],
                  [168, 121, 125]]]

    """

    back_list = cmra.backCamCapture(img)
    back_mu = cmra.median(back_list)
    back_sig = cmra.standardDeviation(back_list, back_mu)

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

        """
        frame =   [[122, 124, 153],
                   [168, 233, 164],
                   [167, 113, 124]]

        print len(frame)
        print len(frame[0])
        """

        frame = cmra.frameCamCapture(img)
        #print 'NFrame: '
        #print frame
        #print len(frame)
        #print len(frame[0])
        #print len(frame[0][0])


        board = brd.lousa(frame)
        board_list.append(frame)
        # print board_list
        # ========================================================================

        # =======================Subtracao De Fundo ==============================
        # diff_frame  = cmra.backgroundSubstraction(frame, back)
        #diff_frame = cmra.substractionMOG2(frame, back_mu)
        diff_frame = cmra.gaussianSubstractor(frame, back_mu, back_sig)
        # diff_frame = cv2.imread('images/big_black.jpg')
        #cmra.median()
        # ========================================================================
        #break

        # ============================= Entropia =================================
        probs_list = cmra.probArray(cmra.histogram(diff_frame),cmra.imageSize(diff_frame))
        shannon_list.append(cmra.shannonEntropy(probs_list))
        index = np.argmax(shannon_list)

        print "shannon_list last Entropy:"
        print "Index [" + str(len(shannon_list)-1) + "]: " + str(shannon_list[len(shannon_list)-1])
        print
        print "Index [" + str(index) + "]: " + str(shannon_list[index])
        print
        # ========================================================================

        # ===================== Identifcacao de conteudo =========================

        # ========================================================================

        # ============================ Envio de Imagem ===========================
        # --> envio da lousa selecionanda
        # --> limpa imagens anteriores
        # ========================================================================

        # ========================== Show Images =================================
        #frame = cv2.resize(frame, (720, 480))
        cv2.imshow('frame', frame)
        #diff_frame = cv2.resize(diff_frame, (720, 480))
        cv2.imshow('diff_frame ', diff_frame)
        #cv2.imshow('Sigma', back_sig)
        cv2.imshow('Index', back_list[index])
        # ========================================================================

        # i += 1

        k = cv2.waitKey(30) & 0xff

        if k == 27:
            break

        elif k == 122:

            back_list = cmra.backCamCapture(img)
            back_mu = cmra.median(back_list)
            back_sig = cmra.standardDeviation(back_list, back_mu)

            # ================ RASP CAM ==================
            """
            camera.capture('images/back.jpg')
            back = cv2.iread('images/back.jpg')
            back = cv2.cvtColor(back, cv2.COLOR_BGR2GRAY)
            """
           # ============================================

    img.release()
    cv2.destroyAllWindows()
