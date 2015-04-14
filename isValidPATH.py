#!/usr/bin/python3
#-*- coding: utf-8 -*-

import os as os

def isValidPATH(chemin):
    ''' Teste si 'chemin' est un chemin valide.
    Note de doc : 'chemin' devrait être un str.
    isValidPATH renvoit :
        *  1  s'il s'agit chemin existant (pas de fichier),
        *  2  si le chemin existe, et le fichier aussi,
        *  -1  si le chemin n'existe pas (fichier ou pas),
        *  -2  si le chemin existe, mais que le fichier n'existe pas.
        *  0  s'il ne s'agit que d'un fichier, dans le répertoire courant.
    
    '''
    var = str(chemin)   # local, (and str() var)
    if var == "":
        return -1
    if "..." in var:
        return -1
    if var == "." or var == "..":
        return 1
    if var[0] == '/':
        os.chdir('/')
        var = var[1:]
    slashes = var.count('/')
    if slashes:
        var = var.replace('//', '/')
        if var[-1] == "/":
            try:
                os.chdir(var)
                return 1
            except:
                return -1
        else:
            Liste = var.split('/')
            lastItem = Liste[-1]
            Liste.pop()
            for i in Liste:
                try:
                    os.chdir(str(i))
                except:
                    return -1
            if lastItem in os.listdir():
                return 2
            else:
                return -2
        
    else:
        try:
            os.chdir(var)
            return 1
        except:
            if var in os.listdir():
                return 0

"""
# Tests unitaires.
# WARNING ! le précédent test impacte le suivant (si on en lance plusieur à la fois)
#~ print(os.getcwd())
print(isValidPATH("/"))
print(isValidPATH("tmp"))
print(isValidPATH("/tmp"))
print(isValidPATH("/tmp/toadjzcbh"))
print(isValidPATH("/tmp/test"))
print(isValidPATH("."))
print(isValidPATH(".."))
print(isValidPATH("./"))
print(isValidPATH("test"))
"""
