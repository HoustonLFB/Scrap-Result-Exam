import os
import filecmp

def baseFolderCreate():

    if not os.path.exists("data"):
        os.makedirs("data")
    if not os.path.exists("tmp"):
        os.makedirs("tmp")

def verifFolderCreate(folder):
    if not os.path.exists(folder):
        os.makedirs(folder)

def fichierExisteIdentique(old, tmp):
    if os.path.exists(old):
        if filecmp.cmp(old, tmp):
            return True
        else:
            return False
    else: 
        return False