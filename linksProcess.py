lien = "https://www.republicain-lorrain.fr/education/resultats-examens?departmentCode=977&diplomaCode=470&page="
nbPages = 56
print(lien)
fichier = open('tmpLinks.txt', 'a')

for i in range(1, nbPages+1):
    tmpLink = lien + str(i)
    fichier.write(tmpLink + '\n')