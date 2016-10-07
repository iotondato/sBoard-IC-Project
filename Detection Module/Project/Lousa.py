""" Brenno T. De Faria """
""" Projeto De IC - Lousa Inteligente """
""" Modulo De Detecao De Imagem.1 """

import json

class lousa:
    def __init__(self, imgRGB):
        self._img_RGB = imgRGB

    def setImgRGB(self, imgRGB):
        self._img_RGB = imgRGB

    def getImgRGB(self):
        return self._img_RGB

    def setImgTXT(self, imgTXT):
        self._img_TXT = imgTXT

    def getImgTXT(self):
        return self._img_TXT

    def setQuantInfo(self, quant_info):
        self._quant_info = quant_info

    def getQuantInfo(self):
        return self._quant_info

    def packageJSON(self, img_RGB, img_TXT):
        data = {'image': img_RGB, 'text': img_TXT}
        with open('selectFrame.json', 'w') as outfile:
            json.dump(data, outfile, indent = 2, sort_keys= True, separators=(',', ':'))
        return outfile
