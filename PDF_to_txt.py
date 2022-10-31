# autor: MolokovAlex
# lisence: GPL
# coding: utf-8



import PyPDF2
import os
from pathlib import Path
import glob
import shutil


# относительный пусть к папке, содержащий требуемые файлы из папки запуска скрипта .py
# FILE_DIR =  r"original_file\"
FILE_DIR =  "original_file\\"
# относительный путь к папку-песочницу из папки запуска скрипта .py
# SANDBOX_DIR = r'temp_file\'
SANDBOX_DIR = 'temp_file\\'

def verifyPDF(name_file:str)-> None:
    """
    # проверим начало структуры pdf каждого файла, если там мусор до символов "%PDF-1.6%" - убрать этот мусор и файл должен начитанться с "%PDF-xxx%"
    Вход:
    name_file - str - полный путь к файлу+наименование файла с расширением
    Выход:
    если структура файла корректна - оставляем его без изменений
    если структура файла не корректна - создаем новый файл .pdf с суффиксом '_corr.pdf' и именем как и входной. Входной файл меняет расширение на '.err'
    """
    with open(name_file, 'r+b') as handler_input_file:
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
                    # position_try_byte = item_byte
                    with open(name_file[:-4]+'_corr.pdf', 'w+b') as correct_file:
                        correct_file.write(a)
                        for i in range(length_input_file):
                            a=handler_input_file.read(1)
                            correct_file.write(a)
                    break
    # переименуем плохой файл, изменим у него расширение, чтобы он потом не попал опять в поиск
    if flag_bad_pdf_file:
         os.rename(item_name_file, item_name_file[:-4]+'.err')

    return None


def parsingText(name_file:str)-> None:
    """
    # поиск подстроки со словом "Счет:", выделение номера счета и переименование файлов исходногоPDF и тестовогоTXT с именем этого счета
    Вход:
    name_file - str - полный путь к файлу+наименование файла с расширением
    Выход:
    созданнный файл .txt с таким же именем как и входной, содержащий только конвертированный текст
    """
    with open(name_file, 'r') as out_file:
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
        os.rename(name_file, new_name_file_txt)
        os.rename(item_name_file, new_name_file_pdf)
    return None


def convertPDFtoTXT(name_file:str)-> None:
    """
    # конвертация текста из pdf файла в txt-файл
    Вход:
    name_file - str - полный путь к файлу+наименование файла с расширением
    Выход:
    созданнный файл .txt с таким же именем как и входной, содержащий только конвертированный текст
    """
    # item_output_name_file = name_file[:-4]+'.txt'
    with open(name_file, 'rb') as pdfFileObj, open(name_file[:-4]+'.txt', 'w') as out_file:
        pdfReader = PyPDF2.PdfFileReader(pdfFileObj)
        # number_of_pages = pdfReader.numPages
        for item_page in range(pdfReader.numPages):
            pageObj = pdfReader.getPage(item_page)
            text_extract = pageObj.extractText()
            out_file.write(text_extract)
            print(text_extract)
    return None

# def createDirSandbox(absDirSandbox:str, absDirOriginFile:str, nameDirSandbox:str, base_dir:str, nameDirFile:str )->bool:
def createDirSandbox(absDirSandbox:str, absDirOriginFile:str)->bool:
    """
    # создает папку-песочницу где будем реализовывать все преобразования
    Вход:
    nameDirSandbox:str - относительный путь к папку-песочницу из папки запуска скрипта .py
    base_dir:str - полный путь папки запуска скрипта .py
    nameDirFile:str - относительный путь к папке с оригинальными файлами из папки запуска скрипта .py

    Выход:
    созданнный файл .txt с таким же именем как и входной, содержащий только конвертированный текст
    """
    
    try:
        Flag_create_Sandbox = False
        # если папка песочницы существует и там есть файлы - просто удаляем их
        # если не существует - создаем папку
        if os.path.exists(absDirSandbox):
            list_files = os.listdir(absDirSandbox)
            if list_files:
                for item_name_file in list_files: 
                    abs = os.sep.join([absDirSandbox, item_name_file])
                    os.remove(abs) 
        else:    
            os.mkdir(absDirSandbox, mode=0o777, dir_fd=None)
    except FileNotFoundError:
        print('Parent directory in the path does not exist')
        Flag_create_Sandbox = False
    except  FileExistsError:
        print('directory already exists') 
        Flag_create_Sandbox = False
    except FileNotFoundError:
        print(' directory does not exist')
        Flag_create_Sandbox = False
    except  OSError:
        print(' directory does not empty')    
        Flag_create_Sandbox = False
    else:
        Flag_create_Sandbox = True
        # копирование файлов из входной папки в песочницу
        bd_in = absDirOriginFile#os.path.join(base_dir, nameDirFile)
        bd_out =  absDirSandbox#os.path.join(base_dir, nameDirSandbox)
        list_file_pdf = list_of_file_in_dir(base_dir=bd_in, ext_file= '*.pdf')
        for item_file in list_file_pdf:
            shutil.copy2(src = item_file, dst=bd_out, follow_symlinks=True)

    return Flag_create_Sandbox


def list_of_file_in_dir(base_dir:str, ext_file:str)-> list:
    """
    # создание списка всех .pdf файлов в папке, содержащий требуемые файлы
    Вход:
    base_dir:str - относительный путь к папке сканирования из папки запуска скрипта .py
    ext_file:str - расширение искомых файлов в виде '*.pdf', если '' - все файлы
    Выход:
    list_file:list - 
    """
    list_file = []
    mask_file = os.sep.join([base_dir, ext_file])
    list_file = glob.glob(mask_file)
    return list_file


def crashPDF(name_file:str, base_dir:str)-> None:
    """
    искажение файла pdf - намеренно для некоторых файлов испортим их внутреннюу структуру, 
    добавив в начало мусор из байт
    """
    spam = b'-----------\n HTTP/1.1 200 OK\n Content-Type: application/pdf\n Connection: close\n X-Request-Id: 84729381048193819\n Date: Wed, 19 Oct 2022 11:01:01 GMT\n'
    
    output_name_file_pdf = name_file[:-4]+'_crash.pdf'
    # path_to_file =  os.path.join(base_dir, SANDBOX_DIR)
    if (name_file == base_dir + '1.pdf') or (name_file == base_dir + '2.pdf'):
        # with open(item_input_name_file, 'r+b') as inputfile, open(output_name_file_pdf, 'w+b') as outputfile:
        with open(output_name_file_pdf, 'w+b') as outputfile:
            pass
        inputfile = os.open(name_file, (os.O_RDWR | os.O_BINARY))
        outputfile = os.open(output_name_file_pdf, (os.O_RDWR | os.O_BINARY))
        stats = os.stat(name_file)
        length_input_file = stats.st_size
        os.write(outputfile, spam)
        for item_byte in range(length_input_file):
            a=os.read(inputfile,1)
            os.write(outputfile,a)
    return None





# основная папка запуска .py скрипта
BASE_DIR = Path(__file__).resolve().parent
# абсолютный путь к песочнице
absSandboxDir= os.path.join(BASE_DIR, SANDBOX_DIR)
absDirOriginFile = os.path.join(BASE_DIR, FILE_DIR)

if createDirSandbox(absDirSandbox=absSandboxDir, absDirOriginFile=absDirOriginFile):
    
    # создание списка всех .pdf файлов в песочнице, содержащий требуемые файлы
    
    list_file_pdf = list_of_file_in_dir(base_dir=absSandboxDir, ext_file= '*.pdf')

    # намеренно для файлов "1.pdf" и "2.pdf" испортим их внутреннюу структуру
    for  item_name_file in list_file_pdf:
        crashPDF(name_file=item_name_file, base_dir=absSandboxDir)

    # проверим начало структуры pdf каждого файла
    for item_name_file in list_file_pdf:
        verifyPDF(item_name_file)

    # list_file_pdf = glob.glob(mask_file_pdf)
    for item_name_file in list_file_pdf:
        # конвертация текста из pdf файла в txt-файл
        convertPDFtoTXT(item_name_file)
        # поиск подстроки со словом "Счет:", выделение номера счета и переименование файлов исходногоPDF и тестовогоTXT с именем этого счета  
        parsingText(item_name_file)    

print("ВСЕ !!!!")