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

nomFichier = 'autoUrlsScrapped.txt'

basename, extension = os.path.splitext(nomFichier)

counter = 1
new_filename = nomFichier

while os.path.exists(new_filename):
    new_filename = f'{basename}_{counter}{extension}'
    counter += 1

with open(new_filename, 'w') as fichier:
    # Écrire le contenu du fichier si nécessaire
    for link in links:
        fichier.write(link + '\n')

print(f'{new_filename} a été créé.')