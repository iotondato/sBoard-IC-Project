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
import pytesseract


if __name__ == '__main__':
    board_list = []
    shannon_list = []
    #probs_list = []
    #nback_list = []

    # ================ RASP CAM ==================
    """
    camera = PiCamera()
    camera.resolution = (720, 480)
    camera.framerate = 15
    """
    # ============================================

    # =============== Web Cam ====================
    img = cv2.VideoCapture(0)
    time.sleep(0.1)
    # ============================================

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

    back_list = cmra.backCamCapture(img, 100)
    back_mu = cmra.median(back_list)
    back_sig = cmra.standardDeviation(back_list, back_mu)

    while True:
        # ====================== Captura Do Frame da Lousa =======================
        # ================ RASP CAM ==================
        """
        camera = PiCamera()
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
        board = brd.lousa(frame)
        board_list.append(frame)
        # print board_list
        # ========================================================================

        # ======================= Subtracao De Fundo ==============================

        diff_frame = cmra.gaussianSubstractor(frame, back_mu, back_sig)
        #diff_frame = cmra.imgMultplication(diff_frame, frame)
        diff_frame_c = cmra.morfOperator(diff_frame)
        # =========================================================================

        # ============================= Entropia =================================
        probs_list = cmra.probArray(cmra.histogram(diff_frame), cmra.imageSize(diff_frame))
        shannon_list.append(cmra.shannonEntropy(probs_list))
        better  = cmra.beastFrame(board_list, shannon_list)

        #=========================================================================

        # ===================== Identifcacao de conteudo =========================
        # nao foi possivel utilizar o pytesseract para extrair texto feito a mao
        # entao usaremos uma API que realize esta tarefe de forma satisfatoria
        # ========================================================================

        # ============================ Envio de Imagem ===========================
        # --> envio da lousa selecionanda
        # --> limpa imagens anteriores
        # ========================================================================

        # ========================== Show Images =================================
        cv2.imshow('frame', frame)
        cv2.imshow('diff_frame ', diff_frame)
        cv2.imshow('diff_frame closing ', diff_frame_c)
        cv2.imshow('Index', better)
        # ========================================================================

        # i += 1

        k = cv2.waitKey(30) & 0xff

        if k == 27:
            break

        elif k == 98:
            back_list = cmra.backCamCapture(img, 100)
            back_mu = cmra.median(back_list)
            back_sig = cmra.standardDeviation(back_list, back_mu)

    img.release()
    cv2.destroyAllWindows()
