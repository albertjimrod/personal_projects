import time
from bs4 import BeautifulSoup
import re
import pandas as pd

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait


pd.set_option("display.max_rows",None)

lista_nombreFlor = []       # el nombre del producto
list_precioXgramo = []      # precio por gramo
list_antesGramo = []        # precio anterior por gramo
list_ahorras = []           # la diferencia entre el precio actual y el anterior
lista_descuento = []        # descuento aplicado
listaGramaje = []           # gramos
list_disponibilidad = []    # si existe o no disponibilidad
lista_temporal = []         # su longitud me permite hacer las iteraciones de asignacion de valores
cantidad_variedades = []    # es donde separo el texto de variedades en elementos de una lista.



flores_links = ['https://eurogrow.es/comprar-flores-de-cbd/5133-orange-haze.html',
                'https://eurogrow.es/comprar-flores-de-cbd/4856-flores-cbd-life-cbd-natura.html',
                'https://eurogrow.es/comprar-flores-de-cbd/3563-cannatonic.html',
                'https://eurogrow.es/comprar-flores-de-cbd/3858-flores-cbd-strawberry-banana.html',
                'https://eurogrow.es/comprar-flores-de-cbd/4468-ice-rock.html',
                'https://eurogrow.es/comprar-flores-de-cbd/3957-flores-cbd-moonrocks.html',
                'https://eurogrow.es/comprar-flores-de-cbd/3956-flores-cbd-sugar-candy.html',
                'https://eurogrow.es/comprar-flores-de-cbd/3851-flores-cbd-bubble-gum.html',
                'https://eurogrow.es/comprar-flores-de-cbd/5745-pack-flores-cbd-rock.html',
                'https://eurogrow.es/comprar-flores-de-cbd/5741-pack-flores-cbd-boomb.html',
                'https://eurogrow.es/comprar-flores-de-cbd/5743-pack-flores-cbd-sugar.html',
                'https://eurogrow.es/comprar-flores-de-cbd/5742-pack-flores-cbd-citric.html',
                'https://eurogrow.es/comprar-flores-de-cbd/5744-pack-flores-cbd-special.html',
                'https://eurogrow.es/comprar-flores-de-cbd/3737-flores-cbd-house-gelato-cali.html',
                'https://eurogrow.es/comprar-flores-de-cbd/3818-flores-cbd-caramelo.html',
                'https://eurogrow.es/comprar-flores-de-cbd/3732-flores-cbd-house-gorilla-glue.html',
                'https://eurogrow.es/comprar-flores-de-cbd/3456-flores-cbd-italy-dreams-dos-si-dos.html',
                'https://eurogrow.es/comprar-flores-de-cbd/3955-flores-cbd-gorilla-glue.html',
                'https://eurogrow.es/comprar-flores-de-cbd/3467-flores-cbd-spanish-hemp-orange-bud.html',
                'https://eurogrow.es/comprar-flores-de-cbd/3850-flores-cbd-gelato.html',
                'https://eurogrow.es/comprar-flores-de-cbd/5896-skunk-cbd.html',
                'https://eurogrow.es/comprar-flores-de-cbd/5897-zkittlez-cbd.html',
                'https://eurogrow.es/comprar-flores-de-cbd/5898-amnesia-kush-cbd.html',
                'https://eurogrow.es/comprar-flores-de-cbd/5894-black-mamba-cbd.html',
                'https://eurogrow.es/comprar-flores-de-cbd/5895-haze-cbd.html',
                'https://eurogrow.es/comprar-flores-de-cbd/4409-off-black-flor-cbd.html'
                ]


driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
driver.maximize_window()

sin_variedad = 'x '
for flores in flores_links:
    driver.get(flores)
    time.sleep(1)
    print('- - - -  - - -  - - -  - - -  - - -  - - -')

    elementosCantidad=driver.find_elements(by=By.XPATH, value="//*[@id='group_40']")
    elementosVariedad=driver.find_elements(By.XPATH, "//*[@id='group_20']")

    try:                                # SIN disponibilidad
        WebDriverWait(driver, 3).until(EC.visibility_of_element_located((By.XPATH, "//*[@id='availability_value']"))).text

    except:                             # CON disponibilidad
        try:                            # existe el campo Variedad?
            WebDriverWait(driver, 3).until(EC.visibility_of_element_located((By.XPATH, "//*[@id='group_20']")))

            print('stock')
            print('nombre: ',WebDriverWait(driver, 4).until(EC.visibility_of_element_located((By.XPATH, "//*[@id='center_column']/div[1]/div[3]/h1"))).text)
            print("              Variedad")

            # -----

            for elementoV in elementosVariedad:
                    print("Store names:"+ elementoV.text)
                    txt = elementoV.text
                    cantidad_variedades = txt.splitlines(True)
                    cantidad_variedades.append(cantidad_variedades)


            ultima_posicion = len(cantidad_variedades)
            del cantidad_variedades[4:ultima_posicion] # elimino las dos ultimas filas, no son necesarias

            lista_temporal = cantidad_variedades.copy()

            print(len(lista_temporal))

            # -----

            offset = 0
            for idx in range(len(lista_temporal)):
                print('-    -    -')
                print('nombre: ',WebDriverWait(driver, 4).until(EC.visibility_of_element_located((By.XPATH, "//*[@id='center_column']/div[1]/div[3]/h1"))).text)
                nombre = WebDriverWait(driver, 4).until(EC.visibility_of_element_located((By.XPATH, "//*[@id='center_column']/div[1]/div[3]/h1"))).text
                lista_nombreFlor.append(nombre)                                                                                                         # nombre planta

                stock = 'stock'
                list_disponibilidad.append(stock)                                                                                                       # añadir stock

                offset = idx + 1
                print("offset: ",offset)

                offset = idx + 1
                driver.find_element(By.XPATH, value="//*[@id='group_20']/option[{dx}]".format(dx=offset)).click()                                       # clicks sobre los productos
                time.sleep(1)

                print('precio: ',WebDriverWait(driver, 4).until(EC.visibility_of_element_located((By.XPATH, "//*[@id='our_price_display']"))).text)     # inserción del precio
                precio = WebDriverWait(driver, 4).until(EC.visibility_of_element_located((By.XPATH, "//*[@id='our_price_display']"))).text
                precio = precio.replace('€','')
                precio = precio.replace(',','.')
                precio = float(precio)
                list_precioXgramo.append(precio)
                time.sleep(1)

                print('antes: ',WebDriverWait(driver, 4).until(EC.visibility_of_element_located((By.XPATH, "//*[@id='old_price_display']/span"))).text) # inserción del precio anterior
                antes = WebDriverWait(driver, 4).until(EC.visibility_of_element_located((By.XPATH, "//*[@id='old_price_display']/span"))).text
                antes = antes.replace('€','')
                antes = antes.replace(',','.')
                antes = float(precio)
                list_antesGramo.append(antes)
                time.sleep(1)

                print('ahorras: ',WebDriverWait(driver, 4).until(EC.visibility_of_element_located((By.XPATH, "//*[@id='reduction_amount_display']"))).text) # inserción ahorro
                ahorras = WebDriverWait(driver, 4).until(EC.visibility_of_element_located((By.XPATH, "//*[@id='reduction_amount_display']"))).text
                ahorras = ahorras.replace('€','')
                ahorras = ahorras.replace(',','.')
                ahorras = float(ahorras)
                list_ahorras.append(ahorras)
                time.sleep(1)

                print('Dto: ',WebDriverWait(driver, 4).until(EC.visibility_of_element_located((By.XPATH, "//*[@id='reduction_percent_display']"))).text)    # descuento aplicado
                dto = WebDriverWait(driver, 4).until(EC.visibility_of_element_located((By.XPATH, "//*[@id='reduction_percent_display']"))).text
                dto = dto.replace('%','')
                dto = dto.replace('-','')
                dto = int(dto)
                lista_descuento.append(dto)

                lista_temporal.clear()


                ##############################################################
                ### Codigo que evita los textos dobles en Variedad: ##########
                ##############################################################

                for elementoC in elementosCantidad:                 #elementos del tag <element> es una sola cadena
                    print("Store names:"+ elementoC.text)


                test_list=[] # esto es para poder eliminar los indices
                if re.findall('\+', elementoC.text):                # Si en el texto hay + debo eliminar los numeros repetidos
                    numbers = re.findall('\d+', elementoC.text)
                    numbers = map(int,numbers)
                    print(numbers)
                    for element in list(numbers):
                        test_list.append(element)

                    posiciones_repetidas = [idx for idx, val in enumerate(test_list) if val in test_list[:idx]]

                    if len(posiciones_repetidas) >= 2:

                        print(len(posiciones_repetidas))

                        for element in posiciones_repetidas:
                            print("Contenido de element: ", test_list[element])
                            listaGramaje.append(test_list[element])
                            lista_temporal.append(test_list[element])

                    elif len(posiciones_repetidas) == 1:
                        for element in list(numbers):
                            listaGramaje.append(element)
                            lista_temporal.append(element)


                elif re.findall('\d+', elementoC.text):
                    numbers = re.findall('\d+', elementoC.text)         # limpiar string extraer unicammente los numeros:
                    numbers = map(int,numbers)
                    for element in list(numbers):
                        listaGramaje.append(element)

                ###^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^######
                ### Codigo que evita los textos dobles en Variedad: ###
                #######################################################

            lista_temporal.clear()

        except: # Si NO existe variedad seguro que existe el campo Cantidad
            WebDriverWait(driver, 3).until(EC.visibility_of_element_located((By.XPATH, "//*[@id='group_40']")))

            print('stock')
            print('nombre: ',WebDriverWait(driver, 4).until(EC.visibility_of_element_located((By.XPATH, "//*[@id='center_column']/div[1]/div[3]/h1"))).text)
            print("             Cantidad")

            ##################################################
            ### Codigo que evita los textos dobles: ##########
            ##################################################

            for elementoC in elementosCantidad:                 #elementos del tag <element> es una sola cadena
                print("Store names:"+ elementoC.text)

            test_list=[] # esto es para poder eliminar los indices
            if re.findall('\+', elementoC.text):                # Si en el texto hay + debo eliminar los numeros repetidos
                numbers = re.findall('\d+', elementoC.text)
                numbers = map(int,numbers)
                print(numbers)
                for element in list(numbers):
                    test_list.append(element)
                # ---
                posiciones_repetidas = [idx for idx, val in enumerate(test_list) if val in test_list[:idx]]

                if len(posiciones_repetidas) >= 2:
                    for idx_remover in posiciones_repetidas[::-1]:
                        del test_list[idx_remover]

                    if len(listaGramaje) == 0:
                        lista_temporal = test_list.copy()
                        listaGramaje = test_list.copy()
                    else:
                        for ix in test_list:
                            lista_temporal.append(ix)
                            listaGramaje.append(ix)

                elif len(posiciones_repetidas) == 1:
                    for element in list(numbers):
                        listaGramaje.append(element)
                        lista_temporal.append(element)
                # ---

            elif re.findall('\d+', elementoC.text):
                numbers = re.findall('\d+', elementoC.text)         # limpiar string extraer unicammente los numeros:
                numbers = map(int,numbers)
                for element in list(numbers):
                    listaGramaje.append(element)
                    lista_temporal.append(element)

            ##^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^##
            ### Codigo que evita los textos dobles: ##########
            ##################################################

            longitud = int(len(lista_temporal))
            print("longitud de int(len(lista_temporal)))): ",longitud)
            offset = 0

            for idx in range(longitud):
                nombre = WebDriverWait(driver, 4).until(EC.visibility_of_element_located((By.XPATH, "//*[@id='center_column']/div[1]/div[3]/h1"))).text
                print(nombre)
                lista_nombreFlor.append(nombre)


                cantidad_variedades.append(sin_variedad)
                print(cantidad_variedades)

                stock = 'stock'
                list_disponibilidad.append(stock)
                offset = idx + 1
                driver.find_element(By.XPATH, value="//*[@id='group_40']/option[{dx}]".format(dx=offset)).click() #los clicks //*[@id="group_40"]

                print("offset = 0 es idx: ",offset)                   #//*[@id="group_40"]
                print('-    -    -')

                time.sleep(1)

                print('precio: ',WebDriverWait(driver, 4).until(EC.visibility_of_element_located((By.XPATH, "//*[@id='our_price_display']"))).text)
                precio = WebDriverWait(driver, 4).until(EC.visibility_of_element_located((By.XPATH, "//*[@id='our_price_display']"))).text
                precio = precio.replace('€','')
                precio = precio.replace(',','.')
                precio = float(precio)
                list_precioXgramo.append(precio)
                time.sleep(1)

                print('antes: ',WebDriverWait(driver, 4).until(EC.visibility_of_element_located((By.XPATH, "//*[@id='old_price_display']/span"))).text)
                antes = WebDriverWait(driver, 4).until(EC.visibility_of_element_located((By.XPATH, "//*[@id='old_price_display']/span"))).text
                antes = antes.replace('€','')
                antes = antes.replace(',','.')
                antes = float(precio)
                list_antesGramo.append(antes)
                time.sleep(1)

                print('ahorras: ',WebDriverWait(driver, 4).until(EC.visibility_of_element_located((By.XPATH, "//*[@id='reduction_amount_display']"))).text)
                ahorras = WebDriverWait(driver, 4).until(EC.visibility_of_element_located((By.XPATH, "//*[@id='reduction_amount_display']"))).text
                ahorras = ahorras.replace('€','')
                ahorras = ahorras.replace(',','.')
                ahorras = float(ahorras)
                list_ahorras.append(ahorras)
                time.sleep(1)

                print('Dto: ',WebDriverWait(driver, 4).until(EC.visibility_of_element_located((By.XPATH, "//*[@id='reduction_percent_display']"))).text)
                dto = WebDriverWait(driver, 4).until(EC.visibility_of_element_located((By.XPATH, "//*[@id='reduction_percent_display']"))).text
                dto = dto.replace('%','')
                dto = dto.replace('-','')
                dto = int(dto)
                lista_descuento.append(dto)

            lista_temporal.clear()



time.sleep(1)
driver.close()

df = pd.DataFrame({'nombre producto':lista_nombreFlor,
                    'precio €':list_precioXgramo,
                    'gr: ':listaGramaje,
                    'antes €':list_antesGramo,
                    'ahorro €':list_ahorras,
                    '% descuento':lista_descuento}
                    )
df

df.to_csv('listado_precios_eurogrow.csv', index = False)
