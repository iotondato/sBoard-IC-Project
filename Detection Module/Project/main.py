#!/usr/bin/python

""" Brenno T. De Faria """
""" Projeto de IC """
""" Modulo De Detecao Imagem.0 """

import numpy as np
import cv2
# from picamera.array import PiRGBArray
# from picamera import PiCamera
import time
import Lousa as brd
import analyzer



if __name__ == '__main__':
    board_list = []
    i = 0

    # ==========  REFERENCIA PARA A CAMERA DO RASP E METODOS DE CAPTURA ==========
    """
    camera = PiCamera()
    camera.resolution = (720, 480)
    camera.framerate = 15
    # rawCapture = PiRGBArray(camera)
    """
    img = cv2.VideoCapture(0)
    time.sleep(0.1)
    """
    # ============================================================================

    # ====================== CAPTURA DA IMAGEM DE FUNDO ==========================
    ""
    camera.capture('images/back.jpg')
    back = cv2.imread('images/back.jpg')
    back = cv2.cvtColor(back, cv2.COLOR_BGR2GRAY)
    cv2.imwrite('images/backGray.jpg', back)
    """
    # DESKTOP VERSION
    ret, fgbg = img.read()
    back = cv2.cvtColor(fgbg, cv2.COLOR_BGR2GRAY)

    # ============================================================================

    while True:
        # ====================== Captura Do Frame da Lousa =======================
        """
        camera.capture('images/frame.jpg')
        frame = cv2.imread('images/frame.jpg')
        board = brd.lousa(frame)
        board_list.append(board)
        # print len(board_list)
        """
        ret, frame = img.read()
        board = brd.lousa(frame)
        board_list.append(board)

        # ========================================================================

        # ============= Subtracao De Fundo Para As imagens da lista ==============
        diff_frame  = analyzer.backgroundSubstraction(back, frame)
        analyzer.histogram(diff_frame)
        """
        cv2.imwrite('images/diffFrame.jpg', diff_frame)
        """
        # print diff_frame
        # ========================================================================

        # ============================= Entropia =================================
<<<<<<< HEAD
        
        #cv2.imwrite('image/histogram.png', analyzer.histogram(diff_frame)
=======
        # analyzer.histogram(diff_frame)
>>>>>>> d1f76fa16ca042be0b11a25f7eeaa97c93f45e4f
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
            """
            camera.capture('back.png')
            back = cv2.imread('back.png')
            back = cv2.cvtColor(back, cv2.COLOR_BGR2GRAY)
            cv2.imwrite('images/backGray.jpg', back)

            """
            ret, fgbg = img.read()
            back = cv2.cvtColor(fgbg, cv2.COLOR_BGR2GRAY)

    # img.release()
<<<<<<< HEAD
    #cv2.destroyAllWindows()
=======
    # cv2.destroyAllWindows()
>>>>>>> d1f76fa16ca042be0b11a25f7eeaa97c93f45e4f

