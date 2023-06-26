from bs4 import BeautifulSoup
import scrapStudents
import openpyxl

excel = openpyxl.Workbook()
sheet = excel.active

#TODO: FAIRE EN SORTE DE SCRAP PLUSISUERS SITES ET CREER PLUSIEURS XLSX

try:
    #URL QUE JE VEUX SCRAP
    url = "https://cyclades.education.gouv.fr/candidat/publication/BTS/A16/admis?contexte=QlRTLEExNiwyMDIzLTAzOkExNjpBOkJUUy0xLjIsMSwzMzEwNzozMjA6QlRTLTE6QTpCVFMtMS4yLCws"
    url = "https://cyclades.education.gouv.fr/candidat/publication/BTS/A16/admis?contexte=QlRTLEExNiwyMDIzLTA2OkExNjpBOkJUUy0xLjIsMSwzMTIxNjozMjA6QlRTLTE6QTpCVFMtMS4yLCws"

    source = scrapStudents.scrap(url)

    soup = BeautifulSoup(source, 'html.parser')

    academieExam = soup.find('main').find("div", class_="fr-container", ).find("h1").text
    sessionExam = soup.find('main').find("div", class_="fr-container").find("p").text
    nameExam = soup.find('main').find("div", class_="fr-container").find("h3").text

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

#TODO: SI LE FICHIER EXISTE DEJA DEMANDER SI ON LE REMPLACE OU ANNULER
excelName = nameExam + ".xlsx"
excelName = excelName.replace(" ", "") #RETIRE L'ESPACE AVANT l'EXTENSION
excel.save(excelName)