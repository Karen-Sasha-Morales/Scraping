from selenium import webdriver
from selenium.webdriver import Keys, ActionChains
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import json
import csv

def getMovies():
    # Armamos todo para entrar a una pagina
    s = Service('./chromedriver.exe')
    driver = webdriver.Chrome(service=s)
    driver.get('https://www.starz.com/ar/es/view-all/all')
    driver.maximize_window()

    # generamos codigo para poner en modo list las peliculas
    WebDriverWait(driver, 50).until(EC.presence_of_element_located(
        (By.XPATH, '//*[@id="subview-container"]/starz-view-all/div/div/div/div/div/div/section/nav/ul/li[2]/span')))
    buttonListMovies = driver.find_element(By.XPATH,
                                           '//*[@id="subview-container"]/starz-view-all/div/div/div/div/div/div/section/nav/ul/li[2]/span')
    buttonListMovies.click()

    # Generamos codigo para cliquear en el boton filtros
    WebDriverWait(driver, 50).until(EC.presence_of_element_located((By.XPATH, "//*/span[contains(text(),'Filtros')]")))
    buttonFilters = driver.find_element(By.XPATH, "//*/span[contains(text(),'Filtros')]")
    buttonFilters.click()

    # Generamos codigo para cliquear en el boton peliculas
    WebDriverWait(driver, 50).until(
        EC.presence_of_element_located((By.XPATH, "//*/button[contains(text(),'Películas')]")))
    buttonMovies = driver.find_element(By.XPATH, "//*/button[contains(text(),'Películas')]")
    buttonMovies.click()

    # Generamos codigo para cliquear en el boton aplicar
    buttonApply = driver.find_element(By.XPATH, "//*/button[contains(text(),'Aplicar')]")
    buttonApply.click()

    # Scroll en la web para que cargue todas las peliculas
    html = driver.find_element(By.TAG_NAME, 'html')

    for _ in range(10):
        html.send_keys(Keys.PAGE_DOWN)
        time.sleep(0.5)

    # generamos codigo para obtener todo el listado de peliculas
    WebDriverWait(driver, 150).until(EC.presence_of_element_located((By.CLASS_NAME, 'view-item-text')))
    allMovies = driver.find_elements(By.CLASS_NAME, 'view-item-text')

    # crear un for que a medida que va cargando nuevas peliculas las vaya agregando a la lista
    peliculas = [element.text for element in allMovies]
    pelisLista = list()
    for p in peliculas:
        pelisLista.append(p)
        print(p)
        print('\n')

    # Generamos codigo para crear el archivo JSON
    data = {}
    data['movies'] = []
    for p in pelisLista:
        data['movies'].append({
            'detalles_de_peliculas': p})

    with open('peliculas.json', 'w') as file:
        json.dump(data, file, indent=4)


    # Generamos codigo para crear el archivo CSV
    doc = {}
    doc['movies'] = []
    for p in pelisLista:
        doc['movies'].append({
            'detalles_de_peliculas': p
        })

    with open('peliculas.csv', 'w') as f:
        writer = csv.writer(f)
        for k, v in doc.items():
            writer.writerow([k, v])

