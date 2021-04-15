
import gspread

from oauth2client.service_account import ServiceAccountCredentials
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import time

def conexion_Drive():
    scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
    creds = ServiceAccountCredentials.from_json_keyfile_name('client_secret.json',scope)
    client = gspread.authorize(creds)

    return client

def leer_info(client):
    # En Base de Datos Telefono debes ingresar el nombre del archivo de tu Google Drive que quieres leer los datos
    sheet = client.open("Notificaciones").sheet1
    print(sheet)
    return sheet


hoja = leer_info(conexion_Drive())

i = 0
for elem in hoja.get_all_values():
    i +=1
    if elem[0] == "Marca temporal":

        continue
    numero = elem[3]
    numero = str(numero)
    print(numero[-8:])
    numero = numero[-8:]
    numero = "'+569" + numero
    elem[3] = numero
    hoja.update_cell(i, 4, numero)
    print(elem)
    a = elem
    if i == 100:
        time.sleep(60)

