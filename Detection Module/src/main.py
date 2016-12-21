#!/usr/bin/python

""" Brenno T. De Faria """
""" Projeto de IC """
""" Modulo De Detecao Imagem.0 """

import cv2
import numpy as np
from picamera.array import PiRGBArray
from picamera import PiCamera
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
    #camera = PiCamera()
    #camera.resolution = (180, 140)
    #camera.framerate = 15
    #rawCapture = PiRGBArray(camera)
    #camera.capture(rawCapture, format = "bgr")
    # ============================================

    #img = cv2.VideoCapture(0)
    #time.sleep(0.1)

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

    print "Ola estou aqui"
    back_list = []
    px = 0

    camera = PiCamera()
    #rawCapture = PiRGBArray(camera)

    # allow the camera to warmup
    time.sleep(0.1)
   
    back_list = cmra.backCamCapture(camera)
    
    back_mu = cmra.median(back_list)
    print("Median Back: ")
    print(back_mu)

    back_sig = cmra.standardDeviation(back_list, back_mu)
    print ("Desvio Padrao: ")
    print(back_sig)
    
    print 'fundo capturado'    
    
    while True:
        #break
        # ====================== Captura Do Frame da Lousa =======================
        # ================ RASP CAM ==================
        frame = cmra.frameCamCapture(camera)
        # ============================================

        """
        frame =   [[122, 124, 153],
                   [168, 233, 164],
                   [167, 113, 124]]

        print len(frame)
        print len(frame[0])
        """

        #frame = cmra.frameCamCapture(img)
        board = brd.lousa(frame)
        board_list.append(frame)
        # print board_list
        # ========================================================================

        # =======================Subtracao De Fundo ==============================
        # diff_frame  = cmra.backgroundSubstraction(frame, back)
        # diff_frame = cmra.substractionMOG2(frame, back_mu)
        diff_frame = cmra.gaussianSubstractor(frame, back_mu, back_sig)
        print ("Diff Frame")
	print (diff_frame)
        # diff_frame = cmra.imgMultplication(diff_frame, frame)

        # diff_frame = cv2.imread('images/big_black.jpg')
        # cmra.median()
        # ========================================================================
        # break

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
        # frame = cv2.resize(frame, (720, 480))
        #cv2.imshow('frame', frame)
        # diff_frame = cv2.resize(diff_frame, (720, 480))
        #cv2.imshow('diff_frame ', diff_frame)
        # cv2.imshow('Sigma', back_sig)
        #cv2.imshow('Index', board_list[index])
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

    #img.release()
    #cv2.destroyAllWindows()
