from bs4 import BeautifulSoup
import scrapHtml
import dataOrganize
import openpyxl
import os

def findAcademie(chaine):
    academie = chaine.split(" - ")
    nomAcademie = academie[0]
    nomAcademie = nomAcademie.replace("Académie de ", "")
    nomAcademie = nomAcademie.replace("Académie d' ", "")

    if nomAcademie == "Normandie":
        nomAcademie = academie[1] 
    if nomAcademie == " SIEC":
        nomAcademie == "SIEC"

    nomAcademie = nomAcademie.replace(" ", "_")

    return nomAcademie

def findExam(chaine):
    exam = chaine.split(" - ")
    nomExam = exam[1]
    
    if exam[0] == " SIEC" or exam[0] == " Académie de Normandie" or exam[0] == " Académie de Orléans":
        nomExam = exam[2]
    
    nomExam = nomExam[:-1]
    nomExam = nomExam.replace(" ", "_")
    return nomExam

def findSession(chaine):
    session = chaine.split(" - ")
    session = session[0]
    session = session.replace(" ", "")
    return session

def findGroupe(chaine):
    groupe = chaine.split(" - ")
    groupe = groupe[1]
    groupe = groupe[:-1]
    groupe = groupe.replace(" ", "_")
    return groupe

def txtToArray():

    urls = []

    #OUVRE LE FICHIER URL.txt ET SCRAP LIGNE PAR LIGNE
    fichier = open('autoUrlsScrapped.txt', 'r')
    lignes = fichier.readlines()

    for ligne in lignes:
        ligne = ligne.strip()
        if not ligne.startswith("#"):
            urls.append(ligne)
    return urls

def isNone(var):
    if var == None:
        return True
    else: 
        return False

def incrAlreadyExist(oldName):
    basename, extension = os.path.splitext(oldName)
    counter = 1
    new_filename = oldName

    while os.path.exists(path + new_filename):
        new_filename = f'{basename}_{counter}{extension}'
        counter += 1
    return new_filename

dataOrganize.baseFolderCreate()

urls = txtToArray()

for url in urls:

    excel = openpyxl.Workbook()
    sheet = excel.active

    source = scrapHtml.scrap(url)
    soup = BeautifulSoup(source, 'html.parser')

    academieExam = soup.find('main').find("h1").text
    sessionExam = soup.find('main').find("p").text
    specialiteExam = soup.find('main').find("h3")

    #S'IL Y A SPECIALITE
    if not isNone(specialiteExam):
        specialiteExam = specialiteExam.text
        specialiteExam = specialiteExam[1:]
        specialiteExam = specialiteExam.replace(" ", "_")

    academie = findAcademie(academieExam)
    exam = findExam(academieExam)
    session = findSession(sessionExam)
    groupe = findGroupe(sessionExam)

    #S'IL Y A SPECIALITE
    if not isNone(specialiteExam):
        nameExamShort = specialiteExam.replace(":", "")
        nameExamShort = nameExamShort[:30] #LIMITER à 30 CARACTERES
        sheet.title = nameExamShort
        sheet.append([academieExam, sessionExam, specialiteExam])
    else: 
        sheet.title = academie
        sheet.append([academieExam, sessionExam])
    try:
        eleves = soup.find('tbody').find_all('tr')

        for eleve in eleves:
        
            nom = eleve.find('td', class_="mat-column-nom").find('span').text
            prenoms = eleve.find('td', class_="mat-column-prenoms").text
            resultat = eleve.find('td', class_="mat-column-resultat").text

            sheet.append([nom, prenoms, resultat])
    except Exception as e:
        print(e)

    #S'IL Y A SPECIALITE
    if not isNone(specialiteExam):
        excelName = specialiteExam
        excelName = excelName[:-1]
        excelName = excelName + ".xlsx"
    else: 
        excelName = academie
        excelName = excelName + ".xlsx"
    
    path = f"data\\{academie}\\{exam}\\{session}\\{groupe}\\"
    dataOrganize.verifFolderCreate(path)
    
    tempPathFile = "tmp\\" + excelName

    maybeOldPathFile = path + excelName

    excel.save(tempPathFile)

    if dataOrganize.fichierExisteIdentique(maybeOldPathFile, tempPathFile):
        os.remove(tempPathFile)
    else:
        newExcelName = incrAlreadyExist(excelName)

        pathFile = path + newExcelName

        os.remove(tempPathFile)
        excel.save(pathFile)
        print(newExcelName + " sauvegardé dans " + pathFile)


    

scrapHtml.quitDriver()