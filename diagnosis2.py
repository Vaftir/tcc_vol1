'''
PUC Minas - Campus Coração Eucarístico
Processamento e Análise de Imagens - Trabalho prático pt. 1
    Arthur Vinícius - #666455
    Gabriel Costa - #665131

O trabalho prático consiste em uma interface gráfica via terminal para processamento de operações
referentes a imagens via input do usuário. Estas consistem em:
    1 - Leitura de imagem; 
    2 - Corte de imagem;
    3 - Busca de padrão em imagens.
'''
import os

import cv2 as cv

def img_read(img_name):
    '''Função para ler uma imagem de acordo com o nome dado pelo usuário.

    :param img_name: Nome e extensão de imagem.
    :returns: Uma imagem.
    '''
    img = cv.imread(img_name)
    return img

def img_show(img_name):
    '''Função para mostrar uma imagem de acordo com o nome dado pelo usuário.
    
    :param img_name: Nome e extensão de imagem.
    '''
    img = img_read(img_name)
    cv.imshow(img_name, img)

x_start, y_start, x_end, y_end = 0, 0, 0, 0
cropping = False
def img_crop(event, x, y, flags, param):
    '''Função para corte de imagens.

    :param event: Evento referente ao clique do mouse
    :param x: Posição x do mouse
    :param y: Posição y do mouse
    :param flags: Argumento base do método setMouseCallback
    :param param: Argumento base do método setMouseCallback
    '''
    global x_start, y_start, x_end, y_end, cropping
   
    if event == cv.EVENT_LBUTTONDOWN:
        x_start, y_start, x_end, y_end = x, y, x, y
        cropping = True
    
    elif event == cv.EVENT_MOUSEMOVE:
        if cropping == True:
            x_end, y_end = x, y
   
    elif event == cv.EVENT_LBUTTONUP:
        x_end, y_end = x, y
        cropping = False
        refPoint = [(x_start, y_start), (x_end, y_end)]
        if len(refPoint) == 2:
            roi = oriImage[refPoint[0][1]:refPoint[1][1], refPoint[0][0]:refPoint[1][0]]
            cv.imshow("corte", roi)
            cv.imwrite('photos/cropped_teste', roi)