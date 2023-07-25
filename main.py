##########################################

# Autor: Diego Mendizábal

# Este software fue creado exclusivamente para fines educativos, el autor se desliga de toda 
# responsabilidad relacionada con el uso del mismo.

# Software bajo licencia GPL-3, más información en https://www.gnu.org/licenses/gpl-3.0.html

##########################################

import tkinter as tk
from facturador import emitir_facturas, generar_archivo_cf

from tkinter import messagebox
from tkinter import Label, Button, StringVar, IntVar, DoubleVar
from tkinter.ttk import Separator, Combobox, Entry
from tkcalendar import DateEntry  

# Variables globales
cuit_var = None
clave_var = None
contribuyente_var = None
punto_venta_var = None
fecha_desde_var = None
fecha_hasta_var = None
facturas_por_dia_var = None
redondeo_var = None
importe_min_var = None
importe_max_var = None
redondeo_importe_var = None
tipo_var = None
emisor_var = None

def facturar_desde_archivo(cuit, clave, contribuyente):
    archivo_facturas = r'.\listado_facturas.xlsx'
    emitir_facturas(archivo_facturas, cuit, clave, contribuyente)
    messagebox.showinfo("Información", "Facturación finalizada")

def facturar_a_CF(cuit, clave, contribuyente):
    archivo_cf = r'.\listado_cf.xlsx'
    emitir_facturas(archivo_cf, cuit, clave, contribuyente)
    messagebox.showinfo("Información", "Facturación a CF finalizada")

def create_window():
    global cuit_var, clave_var, punto_venta_var, fecha_desde_var, fecha_hasta_var, facturas_por_dia_var
    global redondeo_var, importe_min_var, importe_max_var, redondeo_importe_var, tipo_var

    root = tk.Tk()
    root.title("Facturación automática")
    root.geometry("640x400")


    # Frame para agrupar los elementos de configuración para facturar a CF
    frame_configurar = tk.Frame(root)
    frame_configurar.pack(pady=5)

    Label(frame_configurar, text="Configuración de archivo").grid(row=0, column=0,pady=10)

    punto_venta_var = IntVar()
    fecha_desde_var = StringVar()
    fecha_hasta_var = StringVar()
    facturas_por_dia_var = IntVar()
    redondeo_var = IntVar()
    importe_min_var = DoubleVar()
    importe_max_var = DoubleVar()
    redondeo_importe_var = DoubleVar()
    descripcion_var = StringVar()
    tipo_var = StringVar()
    cuit_var = StringVar()
    clave_var = StringVar()
    contribuyente_var = StringVar()

    Label(frame_configurar, text="*Punto de Venta:").grid(row=1, column=0, sticky='e')
    Entry(frame_configurar, textvariable=punto_venta_var, justify='right', width=3).grid(row=1, column=1, padx=5, pady=2, sticky='e')

    Label(frame_configurar, text="*Fecha desde:").grid(row=2, column=0, sticky='e')
    DateEntry(frame_configurar, textvariable=fecha_desde_var, date_pattern='dd/mm/yyyy', width=10, sticky='e').grid(row=2, column=1, padx=5,pady=2, sticky='e')

    Label(frame_configurar, text="*Fecha hasta:").grid(row=3, column=0, sticky='e')
    DateEntry(frame_configurar, textvariable=fecha_hasta_var, date_pattern='dd/mm/yyyy', width=10, sticky='e').grid(row=3, column=1, padx=5,pady=2, sticky='e')

    Label(frame_configurar, text="*Facturas por día:").grid(row=4, column=0, sticky='e')
    Entry(frame_configurar, textvariable=facturas_por_dia_var, justify='right', width=3).grid(row=4, column=1, padx=5,pady=2, sticky='e')

    Label(frame_configurar, text="Redondeo:").grid(row=5, column=0, sticky='e')
    Entry(frame_configurar, textvariable=redondeo_var, justify='right', width=3).grid(row=5, column=1, padx=5,pady=2, sticky='e')

    Label(frame_configurar, text="*Tipo:").grid(row=6, column=0, sticky='e')
    Combobox(frame_configurar, textvariable=tipo_var, values=["Productos", "Servicios"], width=10).grid(row=6, column=1, padx=5,pady=2, sticky='e')
    
    Label(frame_configurar, text="Importe mínimo de factura:").grid(row=1, column=3, sticky='e')
    Entry(frame_configurar, textvariable=importe_min_var, justify='right', width=8).grid(row=1, column=4, padx=5, pady=2, sticky='e')

    Label(frame_configurar, text="*Importe máximo de factura:").grid(row=2, column=3, sticky='e')
    Entry(frame_configurar, textvariable=importe_max_var, justify='right', width=8).grid(row=2, column=4, padx=5, pady=2, sticky='e')

    Label(frame_configurar, text="Redondeo de importe:").grid(row=3, column=3, sticky='e')
    Entry(frame_configurar, textvariable=redondeo_importe_var, justify='right', width=4).grid(row=3, column=4, padx=5, pady=2, sticky='e')

    Label(frame_configurar, text="*Descripción:").grid(row=4, column=3, sticky='e')
    Entry(frame_configurar, textvariable=descripcion_var, justify='right', width=20).grid(row=4, column=4, padx=5, sticky='e')

    # Botones para generar listado de facturas a CF
    btn_generar_archivo = Button(frame_configurar, text="Generar archivo listado_cf.xlsx", command=lambda: generar_archivo_cf(
        punto_venta_var.get(), fecha_desde_var.get(),
        fecha_hasta_var.get(), facturas_por_dia_var.get(), redondeo_var.get(),
        importe_min_var.get(), importe_max_var.get(), descripcion_var.get(), redondeo_importe_var.get(), tipo_var.get()
    )).grid(row=6, column=4, padx=5, sticky='e')


    # Separación
    separator = Separator(root, orient='horizontal')
    separator.pack(fill='x', pady=5)


    # Frame para agrupar elementos de autenticación
    frame_facturar = tk.Frame(root)
    frame_facturar.pack(pady=5)

    Label(frame_facturar, text="*CUIT:").grid(row=3, column=0, sticky='e')
    Entry(frame_facturar, textvariable=cuit_var, width=11).grid(row=3, column=1, padx=5, pady=3, sticky='e')

    Label(frame_facturar, text="*Clave:").grid(row=4, column=0, sticky='e')
    Entry(frame_facturar, show="*", textvariable=clave_var, width=15).grid(row=4, column=1, padx=5, pady=3, sticky='e')

    Label(frame_facturar, text="Identificación del emisor de las facturas:").grid(row=5, column=0, sticky='e')
    Entry(frame_facturar, textvariable=contribuyente_var, width=15).grid(row=5, column=1, padx=5, pady=3, sticky='e')

    btn_facturar_a_CF = Button(root, text="Facturar a CF desde listado_cf.xlsx", command=lambda: facturar_a_CF(
        cuit_var.get(), clave_var.get(), contribuyente_var.get()))
    btn_facturar_a_CF.pack(pady=8)

    # Botón para llamar a la función facturar_desde_archivo
    btn_facturar_desde_archivo = Button(root, text="Facturar desde archivo listado_facturas.xlsx", command=lambda: facturar_desde_archivo(
        cuit_var.get(), clave_var.get(), contribuyente_var.get()
    ))
    btn_facturar_desde_archivo.pack(pady=8)

    root.mainloop()

if __name__ == "__main__":
    create_window()
