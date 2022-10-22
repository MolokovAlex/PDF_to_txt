# autor: MolokovAlex
# lisence: GPL
# coding: utf-8



import PyPDF2
import os
from pathlib import Path
import glob

BASE_DIR = Path(__file__).resolve().parent

# создание списка всех .pdf файлов в директории \file\
path_to_file = os.path.join(BASE_DIR, 'file\\')
mask_file_pdf = path_to_file + '*.pdf'

# составим список всех pdf докуменотв в папке и 
# проверим начало структуры pdf каждого файла, если там мусор до символов "%PDF-1.6%" - убрать этот мусор и файл должен начитанться с "%PDF-xxx%"
list_file_pdf = glob.glob(mask_file_pdf)
for item_name_file in list_file_pdf:
    with open(item_name_file, 'r+b') as handler_input_file:
        try_string = b'%PDF-'
        flag_bad_pdf_file = False
        read_byte = handler_input_file.read(5)
        # если первые пять байт не показывают что это PDF документ "%PDF-" - значит у него мусор в начале
        if read_byte != try_string:
            flag_bad_pdf_file = True
            length_input_file = handler_input_file.seek(0, os.SEEK_END)

            # найдем на каком смещении байты признака PDF документа находятся относительно начала (примерно 149)
            for item_byte in range(length_input_file):
                handler_input_file.seek(item_byte)
                a=handler_input_file.read(5)
                if a == try_string:
                    # нашли! запомним позицию. сделаем корректный/правильный файл
                    position_try_byte = item_byte
                    with open(item_name_file[:-4]+'_corr.pdf', 'w+b') as correct_file:
                        correct_file.write(a)
                        for i in range(length_input_file):
                            a=handler_input_file.read(1)
                            correct_file.write(a)
                    break
    # переименуем плохой файл, изменим у него расширение, чтобы он потом не попал опять в поиск
    if flag_bad_pdf_file:
         os.rename(item_name_file, item_name_file[:-4]+'.err')


# конвертация текста из pdf файла в txt-файл
list_file_pdf = glob.glob(mask_file_pdf)
for item_name_file in list_file_pdf:
    item_output_name_file = item_name_file[:-4]+'.txt'
    with open(item_name_file, 'rb') as pdfFileObj, open(item_output_name_file, 'w') as out_file:
        pdfReader = PyPDF2.PdfFileReader(pdfFileObj)
        number_of_pages = pdfReader.numPages
        for item_page in range(pdfReader.numPages):
            pageObj = pdfReader.getPage(item_page)
            text_extract = pageObj.extractText()
            out_file.write(text_extract)
            print(text_extract)
    
    # поиск подстроки со словом "Счет:", выделение номера счета и переименование файлов исходногоPDF и тестовогоTXT с именем этого счета
    with open(item_output_name_file, 'r') as out_file:
        flag_find_data_in_file = False
        new_name_file_txt = ''
        new_name_file_pdf = ''
        for row in out_file:
            row = row.upper().rstrip()
            row = row.replace(' ', '')
            position = row.find('СЧЕТ:')
            if position >=0:
                new_name_file_txt = path_to_file+row[position+5:]+'.txt'
                new_name_file_pdf = path_to_file+row[position+5:]+'.pdf'
                flag_find_data_in_file = True
                break
    if flag_find_data_in_file:
        os.rename(item_output_name_file, new_name_file_txt)
        os.rename(item_name_file, new_name_file_pdf)

print("ВСЕ !!!!")