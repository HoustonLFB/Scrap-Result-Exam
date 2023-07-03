import scrapHtml
from bs4 import BeautifulSoup

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


publications = txtToArray()

links = []

for publication in publications:

    source = scrapHtml.scrap(publication)

    soup = BeautifulSoup(source, 'html.parser')

    urls = soup.find_all('a', class_='fr-link')

    for url in urls:
        href = url['href']
        link = "https://cyclades.education.gouv.fr" + href
        print(link)
        links.append(link)

nomFichier = 'AllautoUrlsScrapped.txt'

with open(nomFichier, 'w') as fichier:
    # Écrire le contenu du fichier si nécessaire
    for link in links:
        fichier.write(link + '\n')

scrapHtml.quitDriver()