# TODO Utiliser prompt_toolkit et click pour gérer les commandes

import os
import re

running = True

nods_path = "/home/antharia/Dev/python/nod/"
nod_editor = "vim"

#  CONFIG

#  TODO read config file and update NOD variables

##############
#  COMMANDS  #
##############

#  LIST

def list_nods():
    '''
    Returns a list of all nods in the nods directory
    '''
    nods_list = []
    for root, dirs, files in os.walk(nods_path):
        for file in files:
            if (file.endswith(".nod")):
                nods_list.append(file)
                #  print(file.split(".nod")[0])
    return nods_list

def list_help():
    '''
    Print all arguments that can be used with list command
    '''
    print("list command accept those arguments :")
    print("nods, links")

def list_links():
    '''
    Returns a dictionnary of all links used
    '''
    links_list = []
    for root, dirs, files in os.walk(nods_path):
        for file in files:
            if (file.endswith(".nod")):
                nod_file = open(os.path.join(nods_path, file), "rt")
                while(True):
                    line = nod_file.readline()
                    if not line:
                        break
                    line = line.strip()
                    link_regex = '<[^<>\s]+>'
                    result = re.findall(link_regex, line)
                    if result:
                        links_list.append(result[0])
    links_dict = list(dict.fromkeys(links_list))
    for i in range(len(links_dict)):
        print(links_list.count(links_dict[i]), ':', links_dict[i])
    return links_dict

def list_links_by_nod(nod):
    if not nod.endswith(".nod"):
        nod = nod + ".nod"
    nod_file = open(os.path.join(nods_path, nod), "rt")
    nod_data = nod_file.read()
    link_regex = '<[^<>\s]+>'
    result = re.findall(link_regex, nod_data)
    links_list = list(dict.fromkeys(result))
    return links_list

def list_nods_by_link(link):
    all_nods = list_nods()
    nods_list = []
    link = "<" + link + ">"
    for n in all_nods:
        links_list = list_links_by_nod(n)
        if link in links_list:
            nods_list.append(n)
    return nods_list


#  SHOW

def show_nod(nod):
    nod = nod.lower()
    nod = nod + ".nod"
    nod_data = open(os.path.join(nods_path, nod), "rt")
    while(True):
        line = nod_data.readline()
        if not line:
            nod_data.close()
            break
        line = line.strip()
        print(line)
    nod_data.close()


#  EDIT

def edit_nod(nod):
    #  nod = nod.lower()
    nod = nod + ".nod"
    nod_file = nods_path + nod
    os.system(nod_editor + " " + nod_file)

#  HELP

#  TODO print the command list


#############
#  CONSOLE  #
#############

os.system("clear")

while (running):
    command = input("MAP> ")
    command = command.strip()
    arguments = command.split(" ")

    # EXIT command
    if (arguments[0] == "exit"):
        break

    # LIST command
    if (arguments[0] == "list"):
        if len(arguments) == 1:
            list_help()
        else:
            if (len(arguments) == 2):
                if (arguments[1] in ("nods", "-n")):
                    all_nods = list_nods()
                    for n in all_nods:
                        print(n)
                if (arguments[1] in ("links", "-l")):
                    list_links()
            elif (len(arguments) == 3):
                if (arguments[1] == "-n"):
                    links_list = list_links_by_nod(arguments[2])
                    for t in links_list:
                        print(t)
                if (arguments[1] == "-l"):
                    nods_list = list_nods_by_link(arguments[2])
                    for n in nods_list:
                        print(n)

    # SHOW command
    if (arguments[0] == "show"):
        if len(arguments) == 1:
            pass
        else:
            show_nod(arguments[1])

    # EDIT command
    if (arguments[0] == "edit"):
        edit_nod(arguments[1])


    
