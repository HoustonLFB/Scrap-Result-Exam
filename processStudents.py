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

    nomAcademie = nomAcademie.replace(" ", "")

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
    fichier = open('autoUrlsScrapped_1.txt', 'r')
    lignes = fichier.readlines()

    for ligne in lignes:
        ligne = ligne.strip()
        if not ligne.startswith("#"):
            urls.append(ligne)
    return urls

dataOrganize.baseFolderCreate()

urls = txtToArray()

for url in urls:

    excel = openpyxl.Workbook()
    sheet = excel.active

    try:
        source = scrapHtml.scrap(url)

        soup = BeautifulSoup(source, 'html.parser')

        academieExam = soup.find('main').find("div", class_="fr-container", ).find("h1").text
        sessionExam = soup.find('main').find("div", class_="fr-container").find("p").text
        nameExam = soup.find('main').find("div", class_="fr-container").find("h3").text

        academie = findAcademie(academieExam)
        exam = findExam(academieExam)
        session = findSession(sessionExam)
        groupe = findGroupe(sessionExam)

        nameExamShort = nameExam[:30] #LIMITER à 30 CARACTERES
        sheet.title = nameExamShort
        sheet.append([academieExam, sessionExam, nameExam])

        eleves = soup.find('tbody').find_all('tr')

        for eleve in eleves:
            
            nom = eleve.find('td', class_="mat-column-nom").find('span').text
            prenoms = eleve.find('td', class_="mat-column-prenoms").text
            resultat = eleve.find('td', class_="mat-column-resultat").text

            sheet.append([nom, prenoms, resultat])

    except Exception as e:
        print(e)

    excelName = academie + " - " + nameExam
    excelName = excelName[:-1]
    excelName = excelName + ".xlsx"

    basename, extension = os.path.splitext(excelName)

    counter = 1
    new_filename = excelName

    while os.path.exists(new_filename):
        new_filename = f'{basename}_{counter}{extension}'
        counter += 1

    path = f"data\\{academie}\\{exam}\\{session}\\{groupe}\\"

    print(path)
    dataOrganize.verifFolderCreate(path)

    pathFile = path + excelName

    excel.save(pathFile)
    print(excelName + " sauvegardé dans " + pathFile)
