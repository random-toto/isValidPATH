#!/usr/bin/python3
#-*- coding: utf-8 -*-

import os

def isValidPATH(chemin):
    ''' Teste si 'chemin' est un chemin valide.
    'chemin' devrait être un str.
    isValidPATH renvoit :
        * 1 s'il s'agit chemin existant (pas de fichier),
        * 2 si le chemin existe, et le fichier aussi,
        * -1 si le chemin n'existe pas (pas de fichier),
        * -2 si le chemin existe, mais que le fichier n'existe pas.
        * 0 s'il ne s'agit que d'un fichier.
    
    '''
    # var most definitely is a str() that way
    var = str(chemin)
    # Is it a FILE in CWD ? 
    if '/' not in var and var in os.listdir():
        try:
            os.chdir(var)
            return 1
        except:
            return 0
    # following is not a PATH.
    if var == "":
        return -1
    # we'll split the string at every '/' encountered
    slashes = var.count('/')
        # CASE 1 : if 'var' ends with '/', it can only be a PATH, not a file. Is it a valid one ?
    if var[-1] == '/':
        try:
            os.chdir(var)   # since it's a PATH, we try to chdir in it.
            return 1 
        except:
            return -1   # well... seems it's not if we reach this point.
        # CASE 2 : no trailing '/'. Hence, it can only be a FILE at the end of a PATH.
    Liste = []
    if slashes:
        Liste = var.split('/')
    print(len(Liste))
    lastItem = Liste[-1]
    if len(Liste) > 1:
       Liste.pop()
    for i in Liste:
        if str(i) != '':
            try:
                os.chdir(str(i))
                print('toto')
            except:
                for j in Liste:
                    try:
                        os.chdir('/' + str(j))
                    except:
                        return -1
    if lastItem not in os.listdir():
        return -2
    return 2
    
