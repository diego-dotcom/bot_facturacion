## Bot de facturación desde "Comprobantes en Línea" para monotributistas (AFIP)

**Dos modos de funcionamiento:**

 1. Facturar desde los datos de una planilla .xlsx (listado_facturas). En este caso se completan los datos de la planilla, se guarda el archivo, se ejecuta el programa, y se ejecuta la facturación con el botón correspondiente.

 2. Facturar desde los datos de una planilla .xlsx (listado_cf) que se genera automáticamente, a partir algunas opciones seleccionadas por el usuario. En este caso se ejecuta el programa, se cargan las opciones, se genera la planilla, y se ejecuta la facturación con el botón correspondiente.

----------

#### *Instrucciones de instalación:*

1.  Si no lo tuviera instalado, descargue e instale Python 3.8.5 o superior, desde  [www.python.org/downloads](http://www.python.org/downloads). Durante la instalación asegúrese de agregar Python al PATH.
2.  Descargue los archivos main.py, facturador.py, listado_facturas.xlsx y requirements.txt del repositorio, y colóquelos en una misma carpeta.
3.  Descargue ChromeDriver (según la versión que tenga de Google Chrome) desde  [https://chromedriver.chromium.org/downloads](https://chromedriver.chromium.org/downloads), y coloque en la carpeta del punto anterior.
4.  Desde la línea de comandos, sitúese en la carpeta creada e instale las librerías requeridas con  `pip install -r requirements.txt`
5.  Si corresponde, modifique el archivo "listado_facturas.xlsx".
6.  Inicie main.py

----------

> El bot no resuelve cuando AFIP solicita cambio de clave. El desarrollo del bot responde solo a fines educativos. El desarrollador del mismo deslinda toda responsabilidad por los daños y/o perjuicios que pudiere ocasionar su utilización, como así tampoco se hace responsable sobre el uso que puedan hacer terceros con la información brindada.

**Software bajo licencia GPL-3, más información en https://www.gnu.org/licenses/gpl-3.0.html**
