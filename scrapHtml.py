from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
import time

# start by defining the options 
    # Spécifiez le chemin vers votre fichier ChromeDriver
PATH_TO_CHROMEDRIVER = 'C:\chromedriver.exe'

    # Configurer les options du navigateur
options = Options()
options.add_argument("--headless")  # Exécuter en mode headless (sans interface graphique)
options.add_argument("--log-level=3")

    # Créer une instance du service ChromeDriver
service = Service(PATH_TO_CHROMEDRIVER)

    # Créer une instance du navigateur Chrome
driver = webdriver.Chrome(service=service, options=options)

def scrap(url):

    driver.get(url) 

    #ATTENDRE 3 SEC
    time.sleep(3)

    html = driver.page_source

    return html

def quitDriver():
    driver.quit()