
import PySimpleGUI as sg
import cv2 as cv
import io
import os.path
from matplotlib import pyplot as plt
from PIL import Image


def correlacao(pathImagem,pathCropped):

    img = cv.imread(pathImagem,0)
    img2 = img.copy()
    template = cv.imread(pathCropped,0)
    w, h = template.shape[::-1]
    # All the 6 methods for comparison in a list
    methods = ['cv.TM_CCOEFF_NORMED','cv.TM_CCORR_NORMED']
    for meth in methods:
        img = img2.copy()
        method = eval(meth)
        # Aplica a math template com o método
        res = cv.matchTemplate(img,template,method)
        min_val, max_val, min_loc, max_loc = cv.minMaxLoc(res)
        # If the method is TM_SQDIFF or TM_SQDIFF_NORMED, take minimum
        if method in [cv.TM_SQDIFF, cv.TM_SQDIFF_NORMED]:
            top_left = min_loc
        else:
            top_left = max_loc
        bottom_right = (top_left[0] + w, top_left[1] + h)
        cv.rectangle(img,top_left, bottom_right, 255, 2)
        plt.imshow(img,cmap = 'gray')
        plt.title('Ponto detectado'), plt.xticks([]), plt.yticks([])
        plt.show()

global aux
sg.theme("DarkTeal2")

file_types= [
    ("JPEG (*.jpg)","*.jpg"),
    ("PNG (*.png)","*.png"),
    ("Todos os arquivos","*.*")
]

x_start, y_start, x_end, y_end = 0, 0, 0, 0
cropping = False   




'''
grupo 1
Yago Assis  652209
Lucas Baesse 
Requerimentos:
    pip install Pillow
    pip install opencv-contrib-python
    pip install matplotlib
    pip install imutils
imageCut - > def para corte da imagem (a imagem recortada é salva como cropped.jpg
                                        na pasta photos do projeto)
                                        OBS: o imageCut é um método pronto
        OBS: crie uma pasta Tmp ou temp no seu C: para que seja possível carregas as imagens
             as imagens dentro de uma pasta do projeto não estão funcionando por bug do Sistema Operacional
            parametros:
                x e y -> posiçoes do mouse
                event -> evento para clique do mouse
                flags -> flag base para setMouseCallback
                param -> argumento para setMouseCallback
'''
def imageCut(event, x, y, flags, param):
    global x_start, y_start, x_end, y_end, cropping
    
    # Evento referente ao lique do mause
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
        
            cv.imwrite(f'C:/Tmp/cropped.jpg', roi)
'''
Primeira página -> menu
'''
def menu_window():
    sg.theme("DarkTeal2")
    menu_layout = [
        [sg.Text('Trabalho parte 1', font=('Verdana', 16), text_color='#ffffff')],
        [sg.Text('Realize o corte primeiro depois a correlação', text_color='#ffffff')],
        [sg.Text('_'*30, text_color='#ffffff')],
        [sg.Button('Cortar imagem', font=('Verdana', 12))],
        [sg.Button('Correlação', font=('Verdana', 12))],
        [sg.Button('Sair', font=('Verdana', 12), button_color='#eb4034')]
    ]
    menu_window = sg.Window('Menu', menu_layout, element_justification='c')
    while True:
        event, values = menu_window.read()
        if event == 'Sair' or event == sg.WIN_CLOSED:
            break
        elif event == 'Cortar imagem':
            menu_window.close()
            view_img_window()
        elif event == 'Correlação':
            menu_window.close()
            correlacao_window()
    menu_window.close()
'''
Segunda página
'''
def view_img_window(): 
    sg.theme("DarkTeal2")
    '''
        Layout do menu
    '''
    layout = [
        [sg.Image(key="-IMAGE-")],
        [
            sg.Text("Image file"),
            sg.Input(size=(25,1), key= "-FILE-"),
            sg.FileBrowse(file_types=file_types),
            sg.Button("Submit"),
            sg.Button("Cortar imagem"),
            sg.Button("Menu"),
            
        ]
    ]
    img_view_window = sg.Window("Visualizador de imagens", layout)
    '''
    Loop para rodar a aplicação da segunda página
    '''
    while True: 
        event, values = img_view_window.read()
        if event == sg.WIN_CLOSED or event=="Exit": #Evento para fechar a aplicação
            break
        elif event == "Submit": #Botão submit que mostra o template da imagem
            filename = values["-FILE-"]
            if os.path.exists(filename):
                image = Image.open(values["-FILE-"])
                image.thumbnail((500,500))
                bio = io.BytesIO()
                aux = image.save(bio,format="PNG")
                image.save(bio,format="PNG")
                img_view_window["-IMAGE-"].update(data=bio.getvalue())

        elif event == "Cortar imagem": #Botão que libera pra cortar a imagem
                filename = values["-FILE-"]
                img = cv.imread(filename)
                #imS = cv.resize(img, (960, 540))
                #img = imS

                cv.namedWindow(filename)
                cv.setMouseCallback(filename, imageCut) #Chama imagemcut para cortar com o mouse
                
                global oriImage
                oriImage = img.copy()
                if not cropping: #Mostra a imagem sem corte
                    cv.imshow(filename, oriImage)
                if cropping:
                    cv.rectangle(oriImage, (x_start, y_start), (x_end, y_end), (255, 0, 0), 2) #mostra a imagem cortada
        elif event == "Menu": #Volta pro menu
            img_view_window.close()
            menu_window()

    img_view_window.close()


'''
Terceira página
'''
def correlacao_window():
    sg.theme("DarkTeal2")
    layout = [
        [sg.Image(key="-IMAGE-")],
        [
            sg.Text("Imagem Original"),
            sg.Input(size=(25,1), key= "-FILE-"),
            sg.FileBrowse(file_types=file_types),
            sg.Button("Submit"),
        ],
        [sg.Image(key="-IMAGE2-")],
        [
            sg.Text("Imagem Cortada"),
            sg.Input(size=(25,1), key= "-FILE2-"),
            sg.FileBrowse(file_types=file_types,initial_folder='photos'),
            sg.Button("Submit Crop"),
        ],
        [ 
            sg.Button("Menu"),
            sg.Button("Mach")
            
        ]
    ]
    correlacao_window = sg.Window("Correlação", layout)
    '''
    Loop da aplicação da terceira página
    '''
    global caminho
    global caminho1

    while True: 
       event, values = correlacao_window.read()
       caminho = values["-FILE-"]
       caminho2 = values["-FILE2-"]
       if event == sg.WIN_CLOSED or event=="Exit": #Evento para fechar a aplicação
            break
       elif (event == "Submit"): #Botão submit que mostra o template da imagem
            filename = values["-FILE-"]
            if os.path.exists(filename):
                image = Image.open(values["-FILE-"])
                image.thumbnail((500,500))
                bio = io.BytesIO()
                aux = image.save(bio,format="PNG")
                image.save(bio,format="PNG")
                correlacao_window["-IMAGE-"].update(data=bio.getvalue())
       elif (event == "Submit Crop"): #Botão submit que mostra o template da imagem
            filename2 = values["-FILE2-"]
            if os.path.exists(filename2):
                image = Image.open(values["-FILE2-"])
                image.thumbnail((500,500))
                bio = io.BytesIO()
                image.save(bio,format="PNG")
                correlacao_window["-IMAGE2-"].update(data=bio.getvalue())
       elif event == ("Mach"):
                if (values["-FILE2-"]) and (values["-FILE2-"]):
                        correlacao(values["-FILE-"],values["-FILE2-"])
                else:
                    pass
       elif event == "Menu": #Volta pro menu
            correlacao_window.close()
            menu_window()

def main():   
    menu_window()
  
    
if __name__ == '__main__':
    main()
