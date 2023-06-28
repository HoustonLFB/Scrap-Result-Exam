import os
import scrapHtml
from bs4 import BeautifulSoup

publications = "https://cyclades.education.gouv.fr/candidat/publication/BGT"

source = scrapHtml.scrap(publications)

soup = BeautifulSoup(source, 'html.parser')

urls = soup.find_all('a', class_='fr-link')

links = []

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