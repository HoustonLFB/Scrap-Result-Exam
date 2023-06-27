from bs4 import BeautifulSoup
import scrapStudents
import openpyxl
import os

def findAcademie(chaine):
    academie = chaine.split("-")
    academie = academie[0]
    academie = academie.replace("Académie de ", "")
    academie = academie.replace(" ", "")
    return academie

def txtToArray():

    urls = []

    #OUVRE LE FICHIER URL.txt ET SCRAP LIGNE PAR LIGNE
    fichier = open('URL.txt', 'r')
    lignes = fichier.readlines()

    for ligne in lignes:
        ligne = ligne.strip()
        if not ligne.startswith("#"):
            urls.append(ligne)
    return urls


urls = txtToArray()

for url in urls:

    excel = openpyxl.Workbook()
    sheet = excel.active

    try:
        source = scrapStudents.scrap(url)

        soup = BeautifulSoup(source, 'html.parser')

        academieExam = soup.find('main').find("div", class_="fr-container", ).find("h1").text
        sessionExam = soup.find('main').find("div", class_="fr-container").find("p").text
        nameExam = soup.find('main').find("div", class_="fr-container").find("h3").text

        academie = findAcademie(academieExam)

        nameExam = nameExam[:30] #LIMITER à 30 CARACTERES
        sheet.title = nameExam
        sheet.append([academieExam, sessionExam, nameExam])

        eleves = soup.find('tbody').find_all('tr')

        for eleve in eleves:
            
            nom = eleve.find('td', class_="mat-column-nom").find('span').text
            prenoms = eleve.find('td', class_="mat-column-prenoms").text
            resultat = eleve.find('td', class_="mat-column-resultat").text

            sheet.append([nom, prenoms, resultat])

    except Exception as e:
        print(e)

    excelName = academie + " -" + nameExam
    excelName = excelName[:-1]
    excelName = excelName + ".xlsx"

    #SI FICHIER EXISTE DEJA
    if not os.path.exists(excelName):
        excel.save(excelName)
        print(excelName + " sauvegardé")
        
    else:
        yesNo = input(excelName + " existe déjà. Le remplacer ? (Y/N)")

        if (yesNo.lower() == "y" or yesNo.lower() == "o" ) :
            excel.save(excelName)
            print(excelName + " remplacé et sauvegardé")




