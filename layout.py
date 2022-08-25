# -*- coding: utf-8 -*-
"""
Created on Tue Aug 16 08:48:10 2022

@author: andre
"""

import PySimpleGUI as sg
import os
import shutil

import cv2
from reportlab.pdfgen import canvas
from PIL import Image, ImageDraw
import numpy as np

import unicodedata
import re

from datetime import timedelta, date

'''=======FRONT SIDE OF CARD=============='''
KEY_IMPUT_NAME = '--NAME--'
KEY_INPUT_ACTIVITY = '-ACTIVITY--'
KEY_INPUT_BIRTH = '--BIRTH--'
KEY_INPUT_EMISSION = '--EMISSION--'
KEY_INPUT_VALIDITY = '--VALIDITY--'
KEY_INPUT_IDENTITY_DOCUMENT = '--IDENTITY_DOCUMENT--'
KEY_INPUT_CPF = '--CPF--'
KEY_INPUT_PATH = '--PATH_FILE_IMG--'

KEY_INPUT_FATHER = '--FATHER--'
KEY_INPUT_MOTHER = '--MOTHER--'
KEY_INPUT_NATURALNESS = '--NATURALNESS--'
KEY_INPUT_SEX = '--SEX--'
KEY_INPUT_CONVERSION = '--CONVERSION--'
KEY_INPUT_WATER_BAPTISM = '--WATER_BAPTISM--'

KEY_BTN_GENERATE = '--GENERATE_IMG--'
KEY_TEXT_GENERAT_IMG_FRONT = '--TEXT_GENERATE_IMG_FRONT--'
KEY_BTN_GENERATE_IMG_BACKGROUND = '--GENERATE_IMG_BACKGROUND--'
KEY_TEXT_GENERAT_IMG_BACKGROUND= '--TEXT_GENERATE_IMG_BACKGROUND--'

KEY_BTN_GENERATE_PDF = '--GENERATE_PDF_IMAGENS--'

class Card_format:
    def __init__(self):
        super()
        
    def trataImage(self, nameImg, img_member=None, insertImage=True):
        img = Image.open(os.path.abspath(nameImg))
    
        if insertImage:
            try:
                imgPNG = Image.open(img_member)#.convert('L')
                #imgPNG = imgPNG.resize((209, 259))
        
                height,width = imgPNG.size
                lum_img = Image.new('L', (height,width),0)
                  
                draw = ImageDraw.Draw(lum_img)
                draw.rounded_rectangle(((0, 0), (height, width)), 90, fill="white")
                
                img_arr =np.array(imgPNG)
                lum_img_arr =np.array(lum_img)
                final_img_arr = np.dstack((img_arr, lum_img_arr))
        
                img_final= Image.fromarray(final_img_arr)
                
                img_final.thumbnail((210,290))
                
                img.paste(img_final, (738,369),0)
            except:
                sg.popup_error('Um erro ocorreu no formato da imagem.\n A imagem deve estar em modo retrato.')
            
            
        img = img.rotate(90, expand=True)  
        img = img.resize((733, 1068), Image.ANTIALIAS)
        
        #img = img.rotate(90)  
        
        img.save(nameImg)
        img.close()
        
    def editImage(self, values, imgToEdit, nameNewImage, path_img_member):
        img = cv2.imread(imgToEdit)
        #imgPNG = cv2.imread('image.png')
        
        cv2.putText(img,values[KEY_IMPUT_NAME],(100,330),cv2.FONT_HERSHEY_TRIPLEX,1,0)
        cv2.putText(img,values[KEY_INPUT_ACTIVITY],(120,420),cv2.FONT_HERSHEY_TRIPLEX,1,0)
        cv2.putText(img,values[KEY_INPUT_BIRTH],(490,420),cv2.FONT_HERSHEY_TRIPLEX,1,0)
        cv2.putText(img,values[KEY_INPUT_EMISSION],(120,510),cv2.FONT_HERSHEY_TRIPLEX,1,0)
        cv2.putText(img,values[KEY_INPUT_VALIDITY],(440,510),cv2.FONT_HERSHEY_TRIPLEX,1,0)
        cv2.putText(img,values[KEY_INPUT_IDENTITY_DOCUMENT],(80,610),cv2.FONT_HERSHEY_TRIPLEX,1,0)
        cv2.putText(img,values[KEY_INPUT_CPF],(420,610),cv2.FONT_HERSHEY_TRIPLEX,1,0)
        
        cv2.imwrite(nameNewImage,img)
        
        self.trataImage(nameNewImage, path_img_member)
        
        
    def editImageBackground(self, values, imgToEdit, nameNewImage):
        img = cv2.imread(imgToEdit)
        
        cv2.putText(img, values[KEY_INPUT_FATHER],(120,119),cv2.FONT_HERSHEY_TRIPLEX,1,0)
        cv2.putText(img, values[KEY_INPUT_MOTHER],(120,210),cv2.FONT_HERSHEY_TRIPLEX,1,0)
        cv2.putText(img, values[KEY_INPUT_NATURALNESS],(120,300),cv2.FONT_HERSHEY_TRIPLEX,1,0)
        cv2.putText(img, values[KEY_INPUT_SEX],(755,300),cv2.FONT_HERSHEY_TRIPLEX,1,0)
        cv2.putText(img, values[KEY_INPUT_CONVERSION],(105,395),cv2.FONT_HERSHEY_TRIPLEX,1,0)
        cv2.putText(img, values[KEY_INPUT_WATER_BAPTISM],(390,395),cv2.FONT_HERSHEY_TRIPLEX,1,0)
        
        #cv2.imshow("janela",img)
        
        cv2.imwrite(nameNewImage,img)
        self.trataImage(nameNewImage, insertImage=False)

    def generate_pdf(self, path_new_file, path_img_front, path_img_background):
        c = canvas.Canvas(os.path.abspath(path_new_file))
        c.drawImage(path_img_front, 1,600, width=151, height=240)
        c.showPage()
        c.drawImage(path_img_background, 1,600, width=151, height=240)
        #print('teste')
        
        c.save()
    

class main:
    def __init__(self):
        self.path_imgs = 'database\img\card'
        self.name_file_pdf = 'para_impressao.pdf'
        self.card_format = Card_format()
        new_date = date.today()
        new_date_5year = new_date + timedelta(days=1825)
        self.new_date = '{}/{}/{}'.format(str(new_date.day).zfill(2), str(new_date.month).zfill(2),str(new_date.year)[-2:])
        self.new_date_5year = '{}/{}/{}'.format(str(new_date_5year.day).zfill(2), str(new_date_5year.month).zfill(2),str(new_date_5year.year)[-2:])
        
    def layout(self):
        tab_card_front = [
                    [sg.T('Nome', size=(15)), sg.Input(key=KEY_IMPUT_NAME)],
                    [sg.T('Atividade', size=(15)), sg.Combo(['CONGREGADO', 'MEMBRO','AUXILIAR', 'DIACONO', 'PRESBITERO', 'EVANGELISTA', 'PASTOR'], key=KEY_INPUT_ACTIVITY, readonly=True)],
                    [sg.T('Data de Nascimento', size=(15)), sg.Input(key=KEY_INPUT_BIRTH, disabled=True, size=(10)), sg.CalendarButton('Data', target=KEY_INPUT_BIRTH, pad=None, key='--CALEND_BIRTH--', format=('%d/%m/%y'))],
                    [sg.T('Data de Emissão', size=(15)), sg.Input(default_text = self.new_date ,key=KEY_INPUT_EMISSION, disabled=True, size=(10)), sg.CalendarButton('Data', target=KEY_INPUT_EMISSION, pad=None, key='--CALEND_EMISSION--', format=('%d/%m/%y'))],
                    [sg.T('Data de Validade', size=(15)), sg.Input(default_text = self.new_date_5year, key=KEY_INPUT_VALIDITY, disabled=True, size=(10)), sg.CalendarButton('Data', target=KEY_INPUT_VALIDITY, pad=None, key='--CALEND_VALIDITY--', format=('%d/%m/%y'))],
                    [sg.T('DOC. Identidade', size=(15)), sg.Input(key=KEY_INPUT_IDENTITY_DOCUMENT, size=(15))],
                    [sg.T('CPF', size=(15)), sg.Input(key=KEY_INPUT_CPF,size=(15))],
                    [sg.T('Imagem', size=(15)),sg.Input(key=KEY_INPUT_PATH, disabled=True, size=55), sg.FileBrowse(button_text='Importar Imagem', target=KEY_INPUT_PATH, tooltip='Importar imagem para o cartão', file_types=(('Arquivo no Formato', '*.png *.jpg *.jpeg'),))],
                    [sg.Button('Gerar imagem', key=KEY_BTN_GENERATE), sg.T('', key=KEY_TEXT_GENERAT_IMG_FRONT)]
                 ]
        

        tab_card_background = [
                    [sg.T('Pai', size=(18)), sg.Input(key=KEY_INPUT_FATHER)],
                    [sg.T('Mãe', size=(18)), sg.Input(key=KEY_INPUT_MOTHER)],
                    [sg.T('Naturalidade', size=(18)), sg.Input(key=KEY_INPUT_NATURALNESS, size=(15))],
                    [sg.T('Sexo', size=(18)), sg.Combo(['FEMININO', 'MASCULINO'], key=KEY_INPUT_SEX, readonly=True)],
                    [sg.T('Data de Conversão', size=(18)), sg.Input(key=KEY_INPUT_CONVERSION, disabled=True, size=(10)), sg.CalendarButton('Data', target=KEY_INPUT_CONVERSION, pad=None, key='--CALEND_CONVERSION--', format=('%d/%m/%y'))],
                    [sg.T('Data de Batismo Águas', size=(18)), sg.Input(key=KEY_INPUT_WATER_BAPTISM, disabled=True, size=(10)), sg.CalendarButton('Data', target=KEY_INPUT_WATER_BAPTISM, pad=None, key='--CALEND_WATER_BAPTISM--', format=('%d/%m/%y'))],
                    [sg.Button('Gerar Imagem', key=KEY_BTN_GENERATE_IMG_BACKGROUND), sg.T('', key=KEY_TEXT_GENERAT_IMG_BACKGROUND)]
            ] 
        
        layout = [
                    [sg.TabGroup([
                        [sg.Tab('Frente do Cartão', tab_card_front, key='--CARD_FRONT--')],
                        [sg.Tab('Fundo do Cartão', tab_card_background, key='--CARD_BACKGROUND--')]
                        ], key='--DATA_CARD--', enable_events=True)
                    ],
                    [sg.Button('Salvar', key=KEY_BTN_GENERATE_PDF)]
                 ]
        return layout
    
    def path_exist(self, path):
        if not os.path.exists(path):
            return False
        else:
            return True
    
    def import_img(self, window, event, path_file, alternating_row_color='DimGray', background_color='Gray'):
        if not self.path_exist(self.path_imgs):
            os.makedirs(self.path_imgs)
        file = shutil.copy(path_file, self.path_imgs)
        #print('copiado')
    
    def remove_special_characters(self, name):
        # Unicode normalize transforma um caracter em seu equivalente em latin.
        nfkd = unicodedata.normalize('NFKD', name)
        palavraSemAcento = u"".join([c for c in nfkd if not unicodedata.combining(c)])
    
        # Usa expressão regular para retornar a palavra apenas com números, letras e espaço
        return re.sub('[^a-zA-Z0-9 \\\]', '', palavraSemAcento).upper()
    
    def clear_imputs(self, window):
        window.Element(KEY_IMPUT_NAME).update(value='')
        window.Element(KEY_INPUT_BIRTH).update(value='')
        window.Element(KEY_INPUT_EMISSION).update(value='')
        window.Element(KEY_INPUT_VALIDITY).update(value='')
        window.Element(KEY_INPUT_IDENTITY_DOCUMENT).update(value='')
        window.Element(KEY_INPUT_PATH).update(value='')
        window.Element(KEY_INPUT_CPF).update(value='')
        
        window.Element(KEY_INPUT_FATHER).update(value='')
        window.Element(KEY_INPUT_MOTHER).update(value='')
        window.Element(KEY_INPUT_NATURALNESS).update(value='')
        window.Element(KEY_INPUT_CONVERSION).update(value='')
        window.Element(KEY_INPUT_WATER_BAPTISM).update(value='')
    
    def exec_class(self):
        window = sg.Window('Cartão de membro', self.layout(), default_button_element_size=(25,1), resizable=True)
        
        img_front_generate = False
        img_background_generate = False
        while(True):
            event, valuer = window.read(timeout=100)
            
            if event == sg.WINDOW_CLOSED or event == 'Fechar': 
                window.close()
                break
                
            if valuer[KEY_IMPUT_NAME] != '' and valuer[KEY_INPUT_ACTIVITY] != '' and valuer[KEY_INPUT_BIRTH] != '' and valuer[KEY_INPUT_EMISSION] != '' and valuer[KEY_INPUT_VALIDITY] != '' and valuer[KEY_INPUT_IDENTITY_DOCUMENT] != '' and valuer[KEY_INPUT_CPF] != '' and valuer[KEY_INPUT_PATH] != '':
                window.Element(KEY_BTN_GENERATE).update(disabled=False)
            else:
                window.Element(KEY_BTN_GENERATE).update(disabled=True)
                
            if event == KEY_BTN_GENERATE:
                values_inputs = {KEY_IMPUT_NAME: self.remove_special_characters(valuer[KEY_IMPUT_NAME]),
                                 KEY_INPUT_ACTIVITY: valuer[KEY_INPUT_ACTIVITY],
                                 KEY_INPUT_BIRTH: valuer[KEY_INPUT_BIRTH],
                                 KEY_INPUT_EMISSION: valuer[KEY_INPUT_EMISSION],
                                 KEY_INPUT_VALIDITY: valuer[KEY_INPUT_VALIDITY],
                                 KEY_INPUT_IDENTITY_DOCUMENT: valuer[KEY_INPUT_IDENTITY_DOCUMENT],
                                 KEY_INPUT_CPF: valuer[KEY_INPUT_CPF]}
                
                self.card_format.editImage(values_inputs, self.path_imgs+'\CRACHA_alterado.png', self.path_imgs+'\cartao_frente_Teste.jpeg', valuer[KEY_INPUT_PATH])
                img_front_generate = True
                window.Element(KEY_TEXT_GENERAT_IMG_FRONT).Update(value='Imagem gerada!')
                #print('imagem gerada')
                
            if valuer[KEY_INPUT_MOTHER] != '' and valuer[KEY_INPUT_NATURALNESS] != '' and valuer[KEY_INPUT_SEX] != '':
                window.Element(KEY_BTN_GENERATE_IMG_BACKGROUND).update(disabled=False)
            else:
                window.Element(KEY_BTN_GENERATE_IMG_BACKGROUND).update(disabled=True)
                
            if event == KEY_BTN_GENERATE_IMG_BACKGROUND:
                values_inputs = {KEY_INPUT_FATHER: self.remove_special_characters(valuer[KEY_INPUT_FATHER]),
                                 KEY_INPUT_MOTHER: self.remove_special_characters(valuer[KEY_INPUT_MOTHER]),
                                 KEY_INPUT_NATURALNESS: self.remove_special_characters(valuer[KEY_INPUT_NATURALNESS]),
                                 KEY_INPUT_SEX: valuer[KEY_INPUT_SEX],
                                 KEY_INPUT_CONVERSION: valuer[KEY_INPUT_CONVERSION],
                                 KEY_INPUT_WATER_BAPTISM: valuer[KEY_INPUT_WATER_BAPTISM]
                                 }
                self.card_format.editImageBackground(values_inputs, self.path_imgs+'\CRACHA_alterado.png', self.path_imgs+'\cartao_fundo_Teste.jpeg')
                img_background_generate = True
                window.Element(KEY_TEXT_GENERAT_IMG_BACKGROUND).Update(value='Imagem gerada!')
                #print('cartão de fundo gerado')
                
            if img_front_generate == True and img_background_generate == True:
                window.Element(KEY_BTN_GENERATE_PDF).update(disabled=False)
            else:
                window.Element(KEY_BTN_GENERATE_PDF).update(disabled=True)
                
            if event == KEY_BTN_GENERATE_PDF:
                self.card_format.generate_pdf(self.path_imgs+self.name_file_pdf, self.path_imgs+'\cartao_frente_Teste.jpeg', self.path_imgs+'\cartao_fundo_Teste.jpeg')
                save_in_directory = sg.tk.filedialog.askdirectory(initialdir=os.path.abspath(os.sep))
                file = shutil.copy(self.path_imgs+self.name_file_pdf, save_in_directory)
                
                img_front_generate = False
                img_background_generate = False
                window.Element(KEY_TEXT_GENERAT_IMG_FRONT).Update(value='')
                window.Element(KEY_TEXT_GENERAT_IMG_BACKGROUND).Update(value='')
                self.clear_imputs(window)
                
                
if __name__ == "__main__":
    app = main()
    app.exec_class()
    