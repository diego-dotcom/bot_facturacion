##########################################

# Autor: Diego Mendizábal

# Este software fue creado exclusivamente para fines educativos, el autor se desliga de toda 
# responsabilidad relacionada con el uso del mismo.

# Software bajo licencia GPL-3, más información en https://www.gnu.org/licenses/gpl-3.0.html

##########################################

import pandas as pd
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import random
from tkinter import messagebox
from datetime import datetime, timedelta
from selenium.webdriver.support.ui import Select


def ingreso_afip(cuit, clave):
    try:
        url = "https://auth.afip.gob.ar/contribuyente_/login.xhtml"
        driver.get(url)

        # Borra el campo CUIT e introduce el CUIT
        campo_cuit = driver.find_element(By.ID, "F1:username")
        campo_cuit.clear()
        campo_cuit.send_keys(cuit)

        boton_cuit = driver.find_element(By.ID,"F1:btnSiguiente")
        boton_cuit.click()

        # Borra el campo clave e introduce la clave
        campo_clave = driver.find_element(By.ID,"F1:password")
        campo_clave.clear()
        campo_clave.send_keys(clave)

        boton_clave = driver.find_element(By.ID,"F1:btnIngresar")
        boton_clave.click()

        driver.implicitly_wait(8)

    except:
        print("Por favor verifique que el CUIT sea numérico, intente nuevamente")

def ingreso_comprobantes_en_linea(contribuyente):

    # Busca el servicio Comprobantes en línea y hace click
    contribuyente = contribuyente.upper()
    buscador = driver.find_element(By.ID,'buscadorInput')
    buscador.send_keys('Comprobantes en L')
    mis_comprobantes = driver.find_element(By.CLASS_NAME,'search-item')
    mis_comprobantes.click()
    
    time.sleep(2)


    #Cambia de pestaña

    driver.switch_to.window(driver.window_handles[1])


    # Hace click en el contribuyente

    if contribuyente == '':
        driver.find_element(By.XPATH, "//*[@id='contenido']/form/table/tbody/tr[4]/td/input[2]").click() # input[2] cuando hay un único contribuyente
    else:
        driver.find_element(By.XPATH, f"//input[contains(@value,'{contribuyente}')]").click()
    
    time.sleep(random.randint(2,3))

def emitir_facturas(archivo, cuit, clave, contribuyente):

    df = pd.read_excel(archivo, engine = 'openpyxl')

    # Comienza el programa abriendo el navegador
    option = webdriver.ChromeOptions()
    option.add_argument('--disable-blink-features=AutomationControlled')
    option.add_experimental_option("excludeSwitches", ["enable-automation"])
    option.add_experimental_option('useAutomationExtension', False)
    global driver
    driver = webdriver.Chrome(options=option)
    driver.maximize_window()
    
    # Se autentica en la web de AFIP e ingresa a "COmprobantes en Línea"
    ingreso_afip(cuit, clave)
    ingreso_comprobantes_en_linea(contribuyente)

    # Itera sobre el excel fila a fila
    for i in df.index:
        try:
            punto_venta = int(df['Punto de venta'][i])
            fecha = str(df['Fecha'][i])
            partes = fecha.split(" ")[0].split("-")
            fecha_convertida = "/".join(reversed(partes))
            tipo = str(df['Tipo'][i])
            tipo_cliente = str(df['Tipo Cliente'][i])
            tipo_doc = str(df['Tipo Doc'][i])
            doc_cliente = int(df['Doc Cliente'][i])
            forma_pago = str(df['Forma pago'][i])
            descripcion = str(df['Descripción'][i])
            precio = int(df['Importe'][i])
            descarga = str(df['Descargar?'][i])
        except:
            print("Error leyendo datos del Excel")
            continue

        # Hace click en el botón Generar comprobante
        driver.find_element(By.ID,'btn_gen_cmp').click()

        time.sleep(random.randint(1,2))
        
        # Hace click en el punto de venta elegido y continúa

        select = Select(driver.find_element(By.ID, 'puntodeventa'))
        time.sleep(2)
        select.select_by_value(f'{punto_venta}')
        driver.find_element(By.XPATH, "//*[@id='contenido']/form/input[2]").click() 

        time.sleep(random.randint(1,2))

        # Ingresa la fecha de la factura
        fecha_factura = driver.find_element(By.ID,'fc')
        fecha_factura.clear()
        fecha_factura.send_keys(fecha_convertida)
        time.sleep(random.randint(1,2))

        # Selecciona "Productos" o "Servicios"
        if tipo == "Productos":
            driver.find_element(By.XPATH, "//*[@id='idconcepto']/option[2]").click() # [2] productos 

        elif tipo == "Servicios":
            driver.find_element(By.XPATH, "//*[@id='idconcepto']/option[3]").click() # [3] servicios

            # Ingresa la fecha desde / hasta, si se está facturando un servicio
            fsd = driver.find_element(By.ID,'fsd')
            fecha_desde = str(df['Fecha desde'][i])
            partes = fecha_desde.split(" ")[0].split("-")
            fecha_convertida = "/".join(reversed(partes))
            fsd.clear()
            fsd.send_keys(fecha_convertida)
            
            fsh = driver.find_element(By.ID,'fsh')
            fecha_hasta = str(df['Fecha hasta'][i])
            partes = fecha_hasta.split(" ")[0].split("-")
            fecha_convertida = "/".join(reversed(partes))
            fsh.clear()
            fsh.send_keys(fecha_convertida)
    
        driver.find_element(By.XPATH, "//*[@id='contenido']/form/input[2]").click() 
        time.sleep(random.randint(1,2))

        # Selecciona condición impositiva del cliente
        if tipo_cliente == "IVA Responsable Inscripto":
            driver.find_element(By.XPATH, "//*[@id='idivareceptor']/option[2]").click() 
        if tipo_cliente == "IVA Sujeto Exento":
            driver.find_element(By.XPATH, "//*[@id='idivareceptor']/option[3]").click() 
        if tipo_cliente == "Responsable Monotributo":
            driver.find_element(By.XPATH, "//*[@id='idivareceptor']/option[5]").click() 
        if tipo_cliente == "Consumidor Final":
            driver.find_element(By.XPATH, "//*[@id='idivareceptor']/option[4]").click() 

        if tipo_doc != '':
            # Selecciona tipo de documento del cliente
            if tipo_doc == "CUIT":
                driver.find_element(By.XPATH, "//*[@id='idtipodocreceptor']/option[1]").click() 
            if tipo_doc == "CUIL":
                driver.find_element(By.XPATH, "//*[@id='idtipodocreceptor']/option[2]").click() 
            if tipo_doc == "CDI":
                driver.find_element(By.XPATH, "//*[@id='idtipodocreceptor']/option[3]").click() 
            if tipo_doc == "DNI":
                driver.find_element(By.XPATH, "//*[@id='idtipodocreceptor']/option[7]").click() 

        if doc_cliente >0:
            # Ingresa el documento del cliente
            cuit = driver.find_element(By.ID,'nrodocreceptor')
            cuit.send_keys(doc_cliente)
            cuit.send_keys(Keys.TAB)
            time.sleep(1)

        if forma_pago != '':
            # Selecciona la forma de pago
            if forma_pago == "Contado":
                driver.find_element(By.ID, 'formadepago1').click() 
            if forma_pago == "Cuenta Corriente":
                driver.find_element(By.ID, 'formadepago4').click() 
            if forma_pago == "Cheque":
                driver.find_element(By.ID, 'formadepago5').click() 
            if forma_pago == "Otra":
                driver.find_element(By.ID, 'formadepago7').click() 

        time.sleep(random.randint(1,2))
        driver.find_element(By.XPATH, "//*[@id='formulario']/input[2]").click() 

        # Ingresa la descripción del producto / servicio
        time.sleep(random.randint(1,2))
        descripcion_factura = driver.find_element(By.ID,'detalle_descripcion1')
        descripcion_factura.send_keys(descripcion)

        # Ingresa el precio del producto / servicio
        precio_factura = driver.find_element(By.ID,'detalle_precio1')
        precio_factura.send_keys(precio)
        time.sleep(random.randint(1,2))
        driver.find_element(By.XPATH, "//*[@id='contenido']/form/input[8]").click() 
        
        # Confirma la generación de la factura
        driver.find_element(By.ID,'btngenerar').click()
        time.sleep(random.randint(1,2))

        driver.switch_to.alert.accept()

        if descarga == 'Si':
            driver.find_element(By.XPATH, "//*[@id='botones_comprobante']/input").click() 

        time.sleep(random.randint(1,2))
        driver.find_element(By.XPATH, '//*[@id="contenido"]/table/tbody/tr[2]/td/input').click() # Click en Menú principal
    
    # Cierra la pestaña servicio, sale de la sesión y cierra el navegador
    driver.close()
    driver.switch_to.window(driver.window_handles[0])
    time.sleep(random.randint(1,2))
    driver.find_element(By.ID,'contenedorContribuyente').click()
    driver.find_element(By.XPATH, "//button[@title='Salir']")
    time.sleep(random.randint(1,2))
    driver.close()

    print("Bot finalizado")

def generar_archivo_cf(punto_venta, fecha_desde, fecha_hasta, facturas_por_dia,
                  redondeo, importe_min, importe_max, descripcion, redondeo_importe, tipo):
    
    fecha_inicio = datetime.strptime(fecha_desde, '%d/%m/%Y')
    fecha_hoy = datetime.now()
    diferencia = fecha_hoy - fecha_inicio
    diferencia = diferencia.days

    if not all((punto_venta, fecha_desde, fecha_hasta, facturas_por_dia, importe_max,
                 descripcion, tipo)):
        messagebox.showerror("Error", "Por favor, completa todos los campos obligatorios.")
    
    elif diferencia > 5:
        messagebox.showerror("Error", "'Fecha desde' no puede ser anterior a 5 días desde hoy")

    else:
        df = pd.DataFrame(columns=['Punto de venta', 'Fecha', 'Tipo', 'Fecha desde', 'Fecha hasta', 'Tipo Cliente', 'Tipo Doc', 'Doc Cliente', 'Forma pago', 'Descripción', 'Importe', 'Descargar?'])

        # Establece una lista con los días a facturar
        dias_a_facturar = []
        fecha_inicio = datetime.strptime(fecha_desde, '%d/%m/%Y')
        fecha_fin = datetime.strptime(fecha_hasta, '%d/%m/%Y')
        while fecha_inicio <= fecha_fin:
            dias_a_facturar.append(fecha_inicio)
            fecha_inicio = fecha_inicio + timedelta(days=1)

        # Itera sobre cada día a facturar
        for dia in dias_a_facturar:

            # Establece la cantidad de facturas a realizar ese día
            facturas_a_emitir = random.randint(facturas_por_dia - redondeo, facturas_por_dia + redondeo)

            while facturas_a_emitir > 0:
                try:
                    importe_factura = random.randrange(importe_min, importe_max, redondeo_importe)
                except:
                    importe_factura = random.randrange(importe_min, importe_max)

                dia_str = dia.strftime('%d/%m/%Y')
                
                nuevo_registro = [{'Punto de venta': punto_venta, 'Fecha': dia_str, 'Tipo': tipo, 'Fecha desde': dia_str, 'Fecha hasta': dia_str, 'Tipo Cliente': 'Consumidor Final', 'Tipo Doc': '', 'Doc Cliente': 0, 'Forma pago': 'Otra', 'Descripción': descripcion, 'Importe': importe_factura, 'Descargar?': 'No'}]
                df_temp = pd.DataFrame(nuevo_registro)

                df = pd.concat([df, df_temp], ignore_index=True)
                
                facturas_a_emitir -= 1 

        file_path = 'listado_cf.xlsx'
        df.to_excel(file_path, engine='openpyxl', index=False)
        
        total_a_facturar = float(df['Importe'].sum())

        messagebox.showinfo("Información", f"Archivo generado correctamente. El total a facturar es ${total_a_facturar}")

