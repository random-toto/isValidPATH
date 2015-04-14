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
    
    '''
    var = str(chemin)
    if var == "":
        return -1
    slashes = var.count('/')
    if var[-1] == '/':
        try:
            os.chdir(var)
            return 1 
        except:
            return -1
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
                try:
                    os.chdir('/' + str(i))
                except:
                    print(i)
                    return False
    if lastItem not in os.listdir():
        return False
    return 2
    
