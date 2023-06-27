import os

def baseFolderCreate():

    if not os.path.exists("data"):
        os.makedirs("data")

def verifFolderCreate(folder):
    if not os.path.exists(folder):
        os.makedirs(folder)