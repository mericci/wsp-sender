# DEVELOPED: Francisco Larach, Domingo Concha
# coding: utf-8

# In[1]:


# Primero importamos librerias necesarias

import gspread

from oauth2client.service_account import ServiceAccountCredentials # conectar a drive
from selenium import webdriver 
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By

import time

import os
import schedule
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.chrome.options import Options

import autoit
import time
import datetime
import os



# Vay a obtener las credenciales siguiendo los pasos del video.

def conexion_Drive():
    scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
    creds = ServiceAccountCredentials.from_json_keyfile_name('client_secret.json',scope)
    client = gspread.authorize(creds)
    return client


# In[6]:


# A este metodo el podriamos entregar como input el nombre del archivo, pero ahi velo tu !
# Fijate que sheet es parte de esta funcion, pero accedo a el en la funcion mandar_whatsapp(). Es decir, deberia ser una variable 
# global de la clase tambien. Igual que driver que lo explico mas abajo

def leer_info(client):
    # En Base de Datos Telefono debes ingresar el nombre del archivo de tu Google Drive que quieres leer los datos
    #sheet = client.open("WSPS").sheet1

    sheet = client.open("Prueba").sheet1  #ESTO SE COMPARTE POR EL MAIL EN EL DRIVE

    #list_of_hashes = sheet.get_all_records()
    #print(list_of_hashes)
    #sheet = sheet.worksheet('Hoja 1')

    return sheet

    # Results guarda todos los valores de la sheet. Para mas info puedes ver https://gspread.readthedocs.io/en/latest/ 
    # Importante que para acceder un valor puedes ocupar sheet.cell(1,1).value donde (fila,columna) parten ambos desde 1.
    # Una manera de hacer que el codigo ande mas rapido es pasando sheet a un dataframe con pandas, pero con la funcion get_all_records()
    # o get_all_values() disponibles en este link> https://gspread.readthedocs.io/en/latest/ quedaba un poco el sapo al pasar el
    # dataframe a la sheet.
    
    # Igual desde sheet funciona


# In[7]:


# Chrome driver debemos instalarlo. Este video te va a ayudar: https://www.youtube.com/watch?v=dz59GsdvUF8
# Este permite manejar el computador desde un programa externo (en este caso Python)
# El driver va a ser accedido desde otra funcion por lo tanto, podriamos definir una clase que driver sea un
# variable global de la clase. Ahora te lo dejo como funcion, pero la funcion mandar_whatsapp() no va a reconocer a driver 

def chrome_driver():
    # Llamo al chrome driver (puede ser de Mozila tb)
    driver = webdriver.Chrome('/Users/Martin Ricci/Desktop/Difusion WSP/chromedriver') #PATH A CHROMEDRIVER
    # Voy a esta direccion
    driver.get("https://web.whatsapp.com/")
    time.sleep(10)
    return driver


# In[8]:


def mandar_whatsapp():
    # A esta funcion le podriamos entregar como input a que grupo de personas les enviamos las charlas primero (podria ser los
    # asistentes de un evento en particular que la reciban antes por ejemplo, asi fomentas la suscripcion) 
    # Por si se cae, que no salga error
    driver = chrome_driver()
    try:
        #Va al buscador
        buscador = driver.find_element_by_xpath('//*[@id="input-chatlist-search"]')
        # Hace click en el buscador
        buscador.click()
        # Espera 1 seg
        time.sleep(1)
        
        # Ahora recorremos el spreadsheet
        # En vez de 3 tiene que ser el largo del arreglo que recorremos
        for i in range(3):
            # sheet.cell(i,1).value debe ser el nombre del contacto o el numero de telefono. Ambos sirven. Hay que tener ojo 
            # que los contactos no pueden ser repetidos. Una manera es que guardemos los contactos por el RUT, pero tal vez la 
            # gente no va a querer dar tanta informacion
        
            buscador.send_keys(sheet.cell(i,1).value)
            # Enter
            buscador.send_keys(Keys.ENTER)
            #Espero 1 seg
            time.sleep(1)
            # Va al texto del contacto una vez que lo encuentra
            texto = driver.find_element_by_xpath('//*[@id="main"]/footer/div[1]/div[2]/div/div[2]')
            # Podemos mandar incluso whatsapps personalizados. Pensemos en que sheet.cell(i,2).value es la columna del nombre!
            ##### OJO ACÁ
            texto.send_keys('Hola !!'+ sheet.cell(i,2).value + "estoy probando si esto funciona")
            texto.send_keys(Keys.ENTER)
            time.sleep(1)
    except:
        print("No pasa na mucho flaco")


# In[ ]:


def main():
    mandar_whatsapp()
    pass
    # Aca escribe el codigo con la clase construida. Evidentemente el orden de las funciones es como estan definidas sino se cae.

    
    # Me avisas cualquier cosa :D ! Creo que con esto podemos ampliar por montones la red de difusion de REC sin mucho esfuerzo !
    
    #Un abrazo (trata de no mostrar este codigo a otros que sino whatsapp se va a convertir
    # en un parto de difusion, mucho mas que con las listas de difusion actuales !
    
    

def leer_sheet():
    client = conexion_Drive()
    sheet = leer_info(client)
    return sheet


def send_attachment(browser, input_box):
    # Attachment Drop Down Menu
    clipButton = browser.find_element_by_xpath('//*[@id="main"]/header/div[3]/div/div[2]/div/span')
    clipButton.click()
    time.sleep(1)

    # To send Videos and Images.
    mediaButton = browser.find_element_by_xpath('//*[@id="main"]/header/div[3]/div/div[2]/span/div/div/ul/li[1]/button')
    mediaButton.click()
    time.sleep(1)

    image_path = os.getcwd() + "\Invitacion.jpeg" #PATH A FOTO
    #print(image_path)
    

    autoit.control_focus("Abrir", "Edit1") #ESTOS NOMBRES PUEDEN CAMBIAR POR COMPUTADOR
    autoit.control_set_text("Abrir", "Edit1", (image_path))
    autoit.control_click("Abrir", "Button1")
    
    time.sleep(2)
    whatsapp_send_button = browser.find_element_by_xpath('//*[@id="app"]/div/div/div[2]/div[2]/span/div/span/div/div/div[2]/span[2]/div/div/span')
    
    whatsapp_send_button.click()
    time.sleep(1)


def wsp_express(texto, charla, año, sheet):
    #client = conexion_Drive()
    #sheet = client.open("").sheet1
    driver = chrome_driver()
    wait = WebDriverWait(driver, 600)


    #mandar = False
    i = 1
    for elem in sheet.get_all_values(): 

        if elem[0] == "Marca temporal":
            pass
        else:
            send_to = elem[3]
            nombre = elem[1]
            #if nombre == "Karol":
            #    mandar = True
            #    continue
            #if not mandar:
            #    continue
            
            new_chat = driver.find_element_by_xpath("//*[@id='side']/div/div/label/input")
            new_chat.send_keys(send_to, Keys.ENTER)


            inp_xpath = '//*[@id="main"]/footer/div[1]/div[2]/div/div[2]'
            input_box = wait.until(EC.presence_of_element_located((By.XPATH, inp_xpath)))
            # Recordatorio:
            # Te recordamos también, si aún no lo haces, que para poder pinchar los links más fácil puedes agregarnos como contacto o responder este mensaje.
            input_box.send_keys("Hola "+ nombre + "! " + "\n" + "Te contamos que este año Misión de Vida cumple 10 años. " + 
            "Y en medio de este contexto nacional queremos reunirnos, para rezar por Chile y renovar nuestra Misión de Vida para que juntos pidamos por la Paz en nuestro país.\n" +  
            "Queremos contar con todos quienes han participado de este proyecto, por eso te queremos invitar a una misa y almuerzo el próximo domingo 10 de Noviembre en el campus Lo Contador, no te lo pierdas! " + "Puedes inscribirte en este link: " + charla + " " + "(Si tienes algun problema para movilizarte en el forms hay un contacto para ayudarte a llegar)\n" +
            "No te pierdas la oportunidad de volver a vernos como familia MdV Y rezar por Chile!\n" + texto + " "+ "" + " " + año + Keys.ENTER)
            #input_box.send_keys(r + os.getcwd() + "\Invitacion.jpeg")
            #input_box.send_keys()
            send_attachment(driver, input_box)
            #input_box.send_keys(Keys.ENTER)
            time.sleep(0.1)
            print(i)
            i += 1




    """
    buscador = driver.find_element_by_xpath(
        '//*[@id="input-chatlist-search"]')
    buscador.click()

    buscador.send_keys("Pablo Steinmetz")
    buscador.send_keys(Keys.ENTER)

    text = driver.find_element_by_xpath('//*[@id="main"]/footer/div[1]/div[2]/div/div[2]')
    text.send_keys(texto)
    text.send_keys(Keys.ENTER)
    """
    """
    buscador = driver.find_element_by_xpath(
        '//*[@id="input-chatlist-search"]')
    buscador.click()

    buscador.send_keys("Pablo Steinmetz")
    buscador.send_keys(Keys.ENTER)
    """
    """
    target = '"+56999490475"'
    x_arg = '//span[contains(@title,' + target + ')]'
    group_title = wait.until(EC.presence_of_element_located((
        By.XPATH, x_arg)))
    group_title.click()
    """


#main()
if __name__ == "__main__":
    #Acá Comienza el codigo principal
    print("*"*145)
    print()

    #texto = input("INGRESA LOS JEFES QUE FIRMAN : ")
    charla = input("INGRESA EL LINK DE INSCRIPCIÓN :")
    año = input("INGRESA EL AÑO de JEFATURA :")
    link = "https://forms.gle/Q9Wemwpdmfe3oxqk6"
    if(año == "2009"):
        texto = "Cata Simpson y Arturo Raby"
    elif(año == "2010"):
        texto = "Loreto Valdes y Nicolas León"
    elif(año == "2011"):
        texto =  "Luzma Guridi y Diego Merino"
    elif(año == "2012"):
        texto = "Jose Kast y Andrés Justiniano"
    elif(año == "2013"):
        texto = "Javi Lecaros y Guille Tagle"
    elif(año == "2014"):
        texto = "Ceci Campos y José Ignacio Sepulveda"
    elif(año == "2015"):
        texto = "Maca Lagos y Santiago Brown"
    elif(año == "2016"):
        texto = "Eli Chacón y Vicho Salas"
    elif(año == "2017"):
        texto = "Maca Soler y Pablo Schultz"
    elif(año == "2018"):
        texto = "Coni Achondo y Martín Ricci"
    elif(año == "2019"):
        texto = "Jesu Ochagavia y Seba Morales"
    elif(año == "2020"):
        texto = "Cami Fernadez y Vicente Fernandez"
    else:
        texto = ""


    print()
    print("*"*145)

    sheet = leer_sheet()
    wsp_express(texto, link, año, sheet) #acá se cambia link por año

