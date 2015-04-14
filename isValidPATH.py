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
    # tests rapide d'exclusion.
    if var == "":
        return -1
    if "..." in var:
        return -1
    if var == "." or var == "..":
        return 1
    # On commence par retirer le '/' du début s'il existe...
    # Ça sert à lever l'ambiguïté : '/tmp' de './tmp' facilement. 
    if var[0] == '/':
        os.chdir('/')
        var = var[1:]
    slashes = var.count('/')
    # CAS 1 : il y a des '/' restants...
    if slashes:
        var = var.replace('//', '/')    # WARNING : HYPOTHÈSE qui marche sous python3.
        # SOUS-CAS 1 : il y a un trailing '/' => pas de nom de fichier spécifié.
        if var[-1] == "/":
            try:
                os.chdir(var)
                return 1
                # C'est bien un répertoire.
            except:
                return -1
                # Ce n'est pas un répertoire valide. (Au moins sur cette machine).
        # SOUS-CAS 2 :il n'y a pas de '/' à la fin, la fin peut-être soit un fichier, soit un répertoire. 
        else:
            Liste = var.split('/')
            lastItem = Liste[-1]
            Liste.pop()
            # On teste sur tous les élément de la liste saus le dernier.
            for i in Liste:
                try:
                    os.chdir(str(i))
                except:
                    return -1
            # On teste le dernier élément de la liste (à part, parce que n'ayant pas de '/' à la fin, ça peut être un fichier ou un dossier).
            if lastItem in os.listdir():
                try:
                    os.chdir(str(lastItem))
                    return 1
                    # C'est un répertoire.
                except:
                    return 2
                    # C'est un fichier.
            else:
                return -2
                # Le dernier élément n'est pas valide, mais le PATH si.
    # CAS 2 : il n'y en a pas.    
    else:
        try:
            os.chdir(var)
            return 1
            # Il s'agit d'un répertoire.
        except:
            if var in os.listdir():
                return 0
                # Il s'agit d'un fichier.
            else:
                return -1
                # Il ne s'agit ni d'un fichier, ni d'un répertoire.

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
