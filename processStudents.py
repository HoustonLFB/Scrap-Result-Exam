from bs4 import BeautifulSoup
import scrapHtml
import bddSql
import openpyxl
import os

def findAcademie(chaine):
    academie = chaine.split(" - ")
    nomAcademie = academie[0]
    nomAcademie = nomAcademie[1:]
    nomAcademie = nomAcademie.replace("Académie de ", "")
    nomAcademie = nomAcademie.replace("Académie d'", "")

    if nomAcademie == "Normandie":
        nomAcademie = academie[1] 
    
    nomAcademie = nomAcademie.replace(" ", "_")

    return nomAcademie

def findExam(chaine):
    exam = chaine.split(" - ")
    nomExam = exam[1]
    
    if exam[0] == " SIEC" or exam[0] == " Académie de Normandie" or exam[0] == " Académie de Orléans":
        nomExam = exam[2]
    
    nomExam = nomExam[:-1]
    nomExam = nomExam.replace('"', "_")
    nomExam = nomExam.replace("'", "_")
    nomExam = nomExam.replace(" ", "_")
    return nomExam

def findSession(chaine):
    session = chaine.split(" - ")
    session = session[0]
    session = session.replace(" ", "")

    if session[4] == "-":
        session = session[:-1]
        session = session[:-1]
        session = session[:-1]

    return session

def findGroupe(chaine):
    groupe = chaine.split(" - ")
    groupe = groupe[1]
    groupe = groupe[:-1]
    groupe = groupe.replace(" ", "_")
    return groupe

def estEtranger(academie):
    liste = ["Normandie", "Orléans", "Caen", "Rouen", "Rennes", "Nantes", "Poitiers", "Bordeaux", "Toulouse", "Montpellier", "Aix-Marseille", "Nice", "Grenoble", "Lyon", "Clermont-Ferrand", "Limoges", "Orléans-Tours", "Dijon", "Besançon", "Strasbourg", "Nancy-Metz", "Reims", "Lille", "SIEC", "Amiens", "Corse", "Martinique", "Guadeloupe", "La_Réunion", "Guyane", "Mayotte", "Nouvelle-Calédonie", "Polynésie_Française", "St_Pierre_Et_Miquelon"]

    if academie in liste:
        return "0"
    else: 
        return "1"

def txtToArray():

    urls = []

    #OUVRE LE FICHIER URL.txt ET SCRAP LIGNE PAR LIGNE
    fichier = open('02082023.txt', 'r')
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

        if specialiteExam[-1] == " ":
            specialiteExam = specialiteExam[:-1]

        specialiteExam = specialiteExam.replace(" ", "_")
        specialiteExam = specialiteExam.replace("/", "_")
        specialiteExam = specialiteExam.replace('"', '')
        specialiteExam = specialiteExam.replace("'", '_')

    academie = findAcademie(academieExam)
    exam = findExam(academieExam)
    session = findSession(sessionExam)
    groupe = findGroupe(sessionExam)
    etranger = estEtranger(academie)

    if not isNone(specialiteExam):
        print(academie + " " + exam + " " + specialiteExam)
    else: 
        print(academie + " " + exam)

    try:
        eleves = soup.find('tbody').find_all('tr')

        for eleve in eleves:
        
            nom = eleve.find('td', class_="mat-column-nom").find('span').text
            prenoms = eleve.find('td', class_="mat-column-prenoms").text
            resultat = eleve.find('td', class_="mat-column-resultat").text

            nom = nom.replace("'", "_")
            prenoms = prenoms.replace("'", "_")
            resultat = resultat.replace("'", "_")

            if isNone(specialiteExam):
                sqlInsert = f"INSERT INTO `cyclades` VALUES ('{prenoms}', '{nom}', '{resultat}', '{academie}', '{exam}', Null, '{session}', '{groupe}', {etranger});"
            else: 
                sqlInsert = f"INSERT INTO `cyclades` VALUES ('{prenoms}', '{nom}', '{resultat}', '{academie}', '{exam}', '{specialiteExam}', '{session}', '{groupe}', {etranger});"
            bddSql.sqlExecute(sqlInsert)
    except Exception as e:
        print(e)

scrapHtml.quitDriver()
