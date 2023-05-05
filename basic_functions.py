#!/usr/bin/env python3

#*******************************************************************************#
#                                                                               #
# Written by Yuri H. Galvao <yuri@galvao.ca>, November 2022                     #
#                                                                               #
#*******************************************************************************#

import os, json, sys
from contextlib import contextmanager

args = sys.argv[1:] # List of arguments that were passed

yes_for_all = True if '--yes-for-all' in args else False

def confirm(text:str)->bool:
    """
    Asks the user to confirm an action with a yes/no prompt.

    Args:
        text (str): The text to be displayed in the confirmation prompt.

    Returns:
        bool: True if the user confirms the action, False otherwise.
    """

    confirm = 'y' if yes_for_all else input(text)
    
    if confirm.lower() not in ('n', 'no'):
        return True
    else:
        return False

def check_file(file:str)->bool:
    """
    Checks if a file exists in the current directory.

    Arguments:
        file (str): The name of the file to check.

    Returns:
        bool: True if the file exists, False otherwise.
    """

    if os.path.isfile('./' + file):
        return True
    else:
        return False

def ask_for_data(required_data:tuple, file_name_no_extension:str, ask:bool=True)->dict:
    """
    Asks the user for input, creates a JSON configuration file, and returns the input as a dictionary.

    Args:
        required_data (tuple): The data to be collected from the user.
        file_name_no_extension (str): The name of the configuration file without the extension.
        ask (bool, optional): Whether to ask for user input or use default values. Defaults to True.

    Returns:
        dict: A dictionary containing the collected data.
    """

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
    """
    Converts a comma-separated user input string into a list.

    Arguments:
        text (str): The text to be displayed as a prompt for user input.

    Returns:
        list: A list containing the user input as integers or strings.
    """

    raw_list = input(text)

    try:
        final_list = [int(n) for n in raw_list.replace(' ', '').split(',')]
    except:
        final_list = [str(s) for s in raw_list.replace(' ', '').split(',')]

    return final_list

@contextmanager # A function that creates generators (and use them to iterate instead of lists of web elements) was one of the ways that I found to prevent memory leak when unsing Selenium
def generator(list_:list):
    """Creates a generator from a list"""
   
    yield list_
