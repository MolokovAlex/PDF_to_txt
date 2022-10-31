# autor: MolokovAlex
# lisence: GPL
# coding: utf-8

# # Программа crashPDF : программа искажения файла pdf - намеренно для некоторых файлов испортим их внутреннюу структуру, добавив в начало мусор из байт

import os
from pathlib import Path
import glob


# BASE_DIR = Path(__file__).resolve().parent.parent
BASE_DIR = Path(__file__).resolve().parent

# создание списка всех .pdf файлов в директории \file\
path_to_file = os.path.join(BASE_DIR, 'file\\')
mask_file_pdf = path_to_file + '*.pdf'
list_file_pdf = glob.glob(mask_file_pdf)


for item_input_name_file in list_file_pdf:  
      
    spam = b'-----------\n HTTP/1.1 200 OK\n Content-Type: application/pdf\n Connection: close\n X-Request-Id: 84729381048193819\n Date: Wed, 19 Oct 2022 11:01:01 GMT\n'
    
    output_name_file_pdf = item_input_name_file[:-4]+'_crash.pdf'
    if (item_input_name_file == path_to_file + '1.pdf') or (item_input_name_file == path_to_file + '2.pdf'):
        # with open(item_input_name_file, 'r+b') as inputfile, open(output_name_file_pdf, 'w+b') as outputfile:
        with open(output_name_file_pdf, 'w+b') as outputfile:
            pass
        inputfile = os.open(item_input_name_file, (os.O_RDWR | os.O_BINARY))
        outputfile = os.open(output_name_file_pdf, (os.O_RDWR | os.O_BINARY))
        stats = os.stat(item_input_name_file)
        length_input_file = stats.st_size
        os.write(outputfile, spam)
        for item_byte in range(length_input_file):
            a=os.read(inputfile,1)
            os.write(outputfile,a)

print('END')