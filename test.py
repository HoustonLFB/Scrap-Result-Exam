import os

dossier = "test\\test\\test\\test"

if not os.path.exists(dossier):
    os.makedirs(dossier)
    print(f"Le dossier {dossier} a été créé.")
else:
    print(f"Le dossier {dossier} existe déjà.")

with open(dossier + "test.txt", 'w') as fichier:
    fichier.write("penis")