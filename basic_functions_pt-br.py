#!/usr/bin/env python3

#*******************************************************************************#
#                                                                               #
# Written by Yuri H. Galvao <yuri@galvao.ca>, November 2022                     #   
#                                                                               #
#*******************************************************************************#

import os, json, sys, logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(message)s', datefmt='%d-%m-%Y %H:%M:%S')
info = lambda x: logging.info(x)
atencao = lambda x: logging.warning(x)
erro = lambda x: logging.error(x)
erro_critico = lambda x: logging.critical(x)

args = sys.argv[1:] # List of arguments that were passed

yes_for_all = True if '--yes-for-all' in args else False

def confirm(text:str)->bool:
    ''''''

    confirm = 'y' if yes_for_all else input(text)
    
    if confirm.lower() not in ('n', 'no'):
        return True
    else:
        return False

def check_file(file:str)->bool:
    ''''''

    if os.path.isfile('./' + file):
        return True
    else:
        return False

def ask_for_data(required_data:tuple, file_name_no_extension:str, ask:bool=True)->dict:
    ''''''

    data_dict = {}
    if ask:
        for data in required_data:
            data_dict[data] = input(f'Enter the {data}: ')

        open(file_name_no_extension+'.conf', 'w').write(json.dumps(data_dict))
    else:
        for data in required_data:
            data_dict[data[0]] = data[1]

        open(file_name_no_extension+'.conf', 'w').write(json.dumps(data_dict))
    
    print()

    return data_dict

def list_from_input(text:str)->list:
    raw_list = input(text)

    try:
        final_list = [int(n) for n in raw_list.replace(' ', '').split(',')]
    except:
        final_list = [str(s) for s in raw_list.replace(' ', '').split(',')]

    return final_list
