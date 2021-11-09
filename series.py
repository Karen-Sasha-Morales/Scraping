from selenium import webdriver
from selenium.webdriver import Keys, ActionChains
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import json
import csv

def getSeries():
    # Armamos todo para entrar a una pagina
    s = Service('./chromedriver.exe')
    driver = webdriver.Chrome(service=s)
    driver.get('https://www.starz.com/ar/es/view-all/all')
    driver.maximize_window()

    # generamos codigo para poner en modo list las series
    WebDriverWait(driver, 50).until(EC.presence_of_element_located(
        (By.XPATH, '//*[@id="subview-container"]/starz-view-all/div/div/div/div/div/div/section/nav/ul/li[2]/span')))
    buttonListSeries = driver.find_element(By.XPATH,
                                           '//*[@id="subview-container"]/starz-view-all/div/div/div/div/div/div/section/nav/ul/li[2]/span')
    buttonListSeries.click()

    # Generamos codigo para cliquear en el boton filtros
    WebDriverWait(driver, 50).until(EC.presence_of_element_located((By.XPATH, "//*/span[contains(text(),'Filtros')]")))
    buttonFilters = driver.find_element(By.XPATH, "//*/span[contains(text(),'Filtros')]")
    buttonFilters.click()

    # Generamos codigo para cliquear en el boton Series
    WebDriverWait(driver, 50).until(
        EC.presence_of_element_located((By.XPATH, "//*/button[contains(text(),'Series')]")))
    buttonSeries = driver.find_element(By.XPATH, "//*/button[contains(text(),'Series')]")
    buttonSeries.click()

    # Generamos codigo para cliquear en el boton aplicar
    buttonApply = driver.find_element(By.XPATH, "//*/button[contains(text(),'Aplicar')]")
    buttonApply.click()

    # Scroll en la web para que cargue todas las series
    html = driver.find_element(By.TAG_NAME, 'html')

    for _ in range(10):
        html.send_keys(Keys.PAGE_DOWN)
        time.sleep(0.5)

    # generamos codigo para obtener todo el listado de series
    WebDriverWait(driver, 150).until(EC.presence_of_element_located((By.CLASS_NAME, 'view-all-link')))

    # crear un for que a medida que va cargando nuevas series las vaya agregando a la lista
    allSeries = driver.find_elements(By.CLASS_NAME, 'view-all-link')

    series = [element.text for element in allSeries]
    seriesLista = list()
    for s in series:
        seriesLista.append(s)
        print(s)
        print('\n')

    # Se convirtio en un archivo JSON
    data = {}
    data['series'] = []
    for s in seriesLista:
        data['series'].append({
            'detalles_de_series': s})

    with open('series.json', 'w') as file:
        json.dump(data, file, indent=4)

        # Convertir en un archivo CSV
    doc = {}
    doc['series'] = []
    for s in seriesLista:
        doc['series'].append({
            'detalles_de_series': s })

    with open('series.csv', 'w') as f:
        writer = csv.writer(f)
        for k, v in doc.items():
            writer.writerow([k, v])
