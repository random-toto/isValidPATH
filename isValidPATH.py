#!/usr/bin/python3
#-*- coding: utf-8 -*-

"""
Testé pour UNIX-like (Debian/Ubuntu et CentOS/Fedora).
"""

"""
NOTE to self :
Le compiler avec py3compile pour de meilleures perfs.
import isValidPATH as IVP
IVP.isValidPATH('')
"""

import os as os

def isValidPATH(chemin):
    ''' Teste si 'chemin' est un chemin valide. WARNING : lié à la machine qui 
    l'exécute, et son arborescence.
    Note de doc : 'chemin' devrait être un str.
    isValidPATH renvoit :
        *  1  s'il s'agit chemin existant (pas de fichier),
        *  2  si le chemin existe, et le fichier aussi,
        *  -1  si le chemin n'existe pas (fichier ou pas),
        *  -2  si le chemin existe, mais que le fichier n'existe pas.
        *  0  s'il ne s'agit que d'un fichier, dans le répertoire courant.
    '''
    var = str(chemin)      # local, (and str() var)
    # tests rapide d'exclusion.
    if var == "":
        return -1
    if "..." in var:
        return -1       # Ces deux lignes ne sont pas nécessaire, mais ça peut être plus rapide. 
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
        var = var.replace('//', '/')        # WARNING : HYPOTHÈSE qui marche sous python3.
        # SOUS-CAS 1 : il y a un trailing '/' => pas de nom de fichier spécifié.
        if var[-1] == "/":
            try:
                os.chdir(var)
                return 1        #### C'est bien un répertoire.
            except:
                return -1       #### Ce n'est pas un répertoire valide. (Au moins sur cette machine).
        # SOUS-CAS 2 :il n'y a pas de '/' à la fin, la fin peut-être soit un fichier, soit un répertoire. 
        else:
            Liste = var.split('/')
            lastItem = Liste[-1]
            Liste.pop()
            # On teste sur tous les élément de la liste sauf le dernier.
            for i in Liste:
                try:
                    os.chdir(str(i))
                except:
                    return -1
            # On teste le dernier élément de la liste (à part, parce que n'ayant pas de '/' à la fin, ça peut être un fichier ou un dossier).
            if lastItem in os.listdir():
                try:
                    os.chdir(str(lastItem))
                    return 1        #### C'est un répertoire.
                except:
                    return 2        #### C'est un fichier.
            else:
                return -2       #### Le dernier élément n'est pas valide, mais le PATH si.
    # CAS 2 : il n'y en a pas.    
    else:
        try:
            os.chdir(var)
            return 1        #### Il s'agit d'un répertoire.
        except:
            if var in os.listdir():
                return 0        #### Il s'agit d'un fichier.
            else:
                return -1       #### Il ne s'agit ni d'un fichier, ni d'un répertoire.
    # La fin pourrait être réécrite différemment : 
    # 1 : if var in os.listdir()
    # 2 try: \n os.chdir(var) \n except: ...
    # mais flemme, puisque ça marche comme ça.

"""
NOTE :
Vu les valeurs renvoyées par le script (cf. doc de isValidPATH()), il est très 
facile d'éditer le script pour qu'il renvoie des PATHS / FILES valides à l'aide 
d'un '/'join() ...
Ou plus simplement en évaluant os.getcwd() et os.listdir() juste avant le 
return pour éviter : /tmp/../tmp ... 
"""

# Tests unitaires :
"""
# WARNING ! Dans le cas où plusieurs tests sont effectués, 
# le test n°n affecte le test n+1
# Changer des valuers ci dessous en fonction de la machine, de vos fichiers, 
# et des fichiers 
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
print(isValidPATH("/tmp/../tmp"))       # WARNING : Accepté.
#"""

def properPATH(chemin):
    ''' essaie de renvoyer un chemin valide. 
    properPATH(str()) renvoit un tuple : (PATH, FILE), avec :
        *  PATH = False si le chemin est faux.
        *  FILE = False si le ficher OU le chemin n'existe pas.  
    '''
    var = str(chemin)      # local, (and str() var)
    if var == "":
        return (False, False)
    if "..." in var:
        return (False, False)
    if var == "." or var == ".." or var == '/':
        return (str(var), False)
    if var[0] == '/':
        os.chdir('/')
        var = var[1:]
    slashes = var.count('/')
    # CAS 1 : il y a des '/' restants...
    if slashes:
        var = var.replace('//', '/')
        # SOUS-CAS 1 : il y a un trailing '/' => pas de nom de fichier spécifié.
        if var[-1] == "/":
            try:
                os.chdir(var)
                return (os.getcwd(), False)        #### C'est bien un répertoire.
            except:
                return (False, False)       #### Ce n'est pas un répertoire valide. (Au moins sur cette machine).
        # SOUS-CAS 2 :il n'y a pas de '/' à la fin, la fin peut-être soit un fichier, soit un répertoire. 
        else:
            Liste = var.split('/')
            lastItem = Liste[-1]
            Liste.pop()
            # On teste sur tous les élément de la liste sauf le dernier.
            for i in Liste:
                try:
                    os.chdir(str(i))
                except:
                    return (False, False)
            # On teste le dernier élément de la liste (à part, parce que n'ayant pas de '/' à la fin, ça peut être un fichier ou un dossier).
            if lastItem in os.listdir():
                try:
                    os.chdir(str(lastItem))
                    return (os.getcwd(), False)        #### C'est un répertoire.
                except:
                    return (os.getcwd(), str(lastItem))        #### C'est un fichier.
            else:
                return (os.getcwd(), False)       #### Le dernier élément n'est pas valide, mais le PATH si.
    # CAS 2 : il n'y en a pas.    
    else:
        try:
            os.chdir(var)
            return (os.getcwd(), False)        #### Il s'agit d'un répertoire.
        except:
            if var in os.listdir():
                return (os.getcwd(), str(var))        #### Il s'agit d'un fichier.
            else:
                return (False, False)       #### Il ne s'agit ni d'un fichier, ni d'un répertoire.
#
"""
print(properPATH('/tmp'))
print(properPATH('/tmp/../tmp'))
print(properPATH('/tmp/test'))
print(properPATH('/tmp/azejhf'))
print(properPATH('/'))
print(properPATH('.'))
print(properPATH('..'))
print(properPATH('/tmp/'))
print(properPATH('./test'))
print(properPATH('/tmp/../tmp/./test'))     # Works. equals to /tmp/test if regular file 'test' exists.
#"""

def properPATH2file(chemin):
    var = str(chemin) 
    if var == "":
        return (False, False)
    if "..." in var:
        return (False, False)
    if var == "." or var == ".." or var == '/':
        return (str(var), False)
    if var[0] == '/':
        os.chdir('/')
        var = var[1:]
    slashes = var.count('/')
    if slashes:
        var = var.replace('//', '/')
        if var[-1] == "/":
            try:
                os.chdir(var)
                return (os.getcwd(), False)   
            except:
                return (False, False) 
        #
        else:
            Liste = var.split('/')
            lastItem = Liste[-1]
            #~ print(lastItem) #
            Liste.pop()
            #~ print(Liste) #
            for i in Liste:
                try:
                    os.chdir(str(i))
                except:
                    return (False, False)
            if lastItem in os.listdir():
                try:
                    os.chdir(str(lastItem))
                    #~ print("toto")
                    return (os.getcwd(), False) 
                except:
                    #~ print("tutu")
                    return (os.getcwd(), str(lastItem))  
            else:
                #~ print("titi")
                return (os.getcwd(), False, str(lastItem))   # changé par rapport à properPATH. On veut pouvoir créer un fichier, s'il n'existe pas.
    else:
        try:
            os.chdir(var)
            return (os.getcwd(), False)  
        except:
            if var in os.listdir():
                return (os.getcwd(), str(var))  
            else:
                return (False, False)   
