from bs4 import BeautifulSoup
import scrapHtml
import bddSql
import re

bddSql.sqlExecute("DELETE FROM `dnb` WHERE 1")

departements_academies = {
    '03': 'Clermont-Ferrand',
    '15': 'Clermont-Ferrand',
    '43': 'Clermont-Ferrand',
    '63': 'Clermont-Ferrand',
    '07': 'Grenoble',
    '26': 'Grenoble',
    '38': 'Grenoble',
    '73': 'Grenoble',
    '74': 'Grenoble',
    '01': 'Lyon',
    '42': 'Lyon',
    '69': 'Lyon',
    '25': 'Besançon',
    '39': 'Besançon',
    '70': 'Besançon',
    '90': 'Besançon',
    '21': 'Dijon',
    '58': 'Dijon',
    '71': 'Dijon',
    '89': 'Dijon',
    '22': 'Rennes',
    '29': 'Rennes',
    '35': 'Rennes',
    '56': 'Rennes',
    '18': 'Orléans-Tours',
    '28': 'Orléans-Tours',
    '36': 'Orléans-Tours',
    '37': 'Orléans-Tours',
    '41': 'Orléans-Tours',
    '45': 'Orléans-Tours',
    '54': 'Nancy-Metz',
    '55': 'Nancy-Metz',
    '57': 'Nancy-Metz',
    '88': 'Nancy-Metz',
    '08': 'Reims',
    '10': 'Reims',
    '51': 'Reims',
    '52': 'Reims',
    '67': 'Strasbourg',
    '68': 'Strasbourg',
    '971': 'Guadeloupe',
    '977': 'Guadeloupe',
    '978': 'Guadeloupe',
    '973': 'Guyane',
    '02': 'Amiens',
    '60': 'Amiens',
    '80': 'Amiens',
    '59': 'Lille',
    '62': 'Lille',
    '77': 'Créteil',
    '93': 'Créteil',
    '94': 'Créteil',
    '75': 'Paris',
    '78': 'Versailles',
    '91': 'Versailles',
    '92': 'Versailles',
    '95': 'Versailles',
    '972': 'Martinique',
    '14': 'Normandie',
    '50': 'Normandie',
    '61': 'Normandie',
    '27': 'Normandie',
    '76': 'Normandie',
    '975': 'Saint-Pierre-et-Miquelon',
    '24': 'Bordeaux',
    '33': 'Bordeaux',
    '40': 'Bordeaux',
    '47': 'Bordeaux',
    '64': 'Bordeaux',
    '19': 'Limoges',
    '23': 'Limoges',
    '87': 'Limoges',
    '16': 'Poitiers',
    '17': 'Poitiers',
    '79': 'Poitiers',
    '86': 'Poitiers',
    '11': 'Montpellier',
    '30': 'Montpellier',
    '34': 'Montpellier',
    '48': 'Montpellier',
    '66': 'Montpellier',
    '09': 'Toulouse',
    '12': 'Toulouse',
    '31': 'Toulouse',
    '32': 'Toulouse',
    '46': 'Toulouse',
    '65': 'Toulouse',
    '81': 'Toulouse',
    '82': 'Toulouse',
    '44': 'Nantes',
    '49': 'Nantes',
    '53': 'Nantes',
    '72': 'Nantes',
    '85': 'Nantes',
    '04': 'Aix-Marseille',
    '05': 'Aix-Marseille',
    '13': 'Aix-Marseille',
    '84': 'Aix-Marseille',
    '06': 'Nice',
    '83': 'Nice',
    '974': 'La Réunion',
    '976': 'Mayotte'
}

def txtToArray():

    urls = []

    #OUVRE LE FICHIER URL.txt ET SCRAP LIGNE PAR LIGNE
    fichier = open('franceDnbLinks.txt', 'r')
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
    print(url)

    source = scrapHtml.scrap(url)
    soup = BeautifulSoup(source, 'html.parser')

    eleves = soup.find('tbody').find_all('tr', attrs={'class': None})

    for eleve in eleves:

        if isNone(eleve.find('td', class_="value_lastnamefirstname")):
            continue

        nomEntier = eleve.find('td', class_="value_lastnamefirstname").text
        nomEntier = nomEntier.replace("							    ", "")
        nomEntier = nomEntier.replace("							", "")

        villeA = eleve.find('a', class_="link_city")

        if not isNone(villeA):
            ville = villeA.text

        status = eleve.find('span', id="status").text

        mentionA = eleve.find('span', id="mention")

        if not isNone(mentionA):
            mention = mentionA.text
            resultat = status + " " + mention
        else:
            resultat = status

        serie = eleve.find('a', class_="link_serie").text

        pattern = r'\((.*?)\)'
        academieNb = re.findall(pattern, soup.find('div', class_="i_blocExamens").find('h1').text)
        academie = departements_academies.get(str(academieNb[0]))

        if academie == None or academie == "None":
            academie = ""

        sqlInsert = f"INSERT INTO `dnb`(`nom_entier`, `résultat`, `academie`, `ville`, `examen`, `serie`, `annee_session`) VALUES (%s, '{resultat}', '{academie}', %s, 'DIPLÔME_NATIONAL_DU_BREVET', '{serie}', '2023');"
        valeurs = (nomEntier, ville)

        bddSql.sqlExecuteValues(sqlInsert, valeurs)