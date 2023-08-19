## Bot facturador desde "Comprobantes en Línea" para monotributistas (AFIP)

#### Instrucciones de instalación:
1.  Descargue el instalador (.exe) que se encuentra a la derecha (Releases). 
2.  Ejecute el instalador y siga las instrucciones.

----------

**IMPORTARTE: Chromedriver**

 - Recuerde tener instalado Google Chrome en su PC.

- Descargue Chromedriver desde https://chromedriver.chromium.org/downloads de acuerdo a su version de Google Chrome.

- Descomprima el archivo descargado, y guarde "chromedriver.exe" en la misma carpeta en la que instalo el bot.

- Cada vez que actualice Google Chrome, recuerde descargar la version correspondiente de Chromedriver.


----------

**Dos modos de funcionamiento:**

 1. Facturar desde los datos de una planilla .xlsx (listado_facturas). En este caso se completan los datos de la planilla, se guarda el archivo, se ejecuta el programa, y se ejecuta la facturación con el botón correspondiente.
 2. Facturar desde los datos de una planilla .xlsx (listado_cf) que se genera automáticamente, a partir algunas opciones seleccionadas por el usuario. En este caso se ejecuta el programa, se cargan las opciones, se genera la planilla, y se ejecuta la facturación con el botón correspondiente.

----------

Para ambos modos, se debe ingresar CUIT y clave fiscal del contribuyente.

El campo "Identificación del emisor de las facturas" es optativo, se utiliza cuando ese cuit puede facturar a nombre de más de un contribuyente.
Con solo ingresar parte inequívoca del nombre o apellido del contribuyente a facturar, el bot lo identifica.


----------

> El bot no resuelve cuando AFIP solicita cambio de clave. El desarrollo del bot responde solo a fines educativos. El desarrollador del mismo deslinda toda responsabilidad por los daños y/o perjuicios que pudiere ocasionar su utilización, como así tampoco se hace responsable sobre el uso que puedan hacer terceros con la información brindada.
---

**Software bajo licencia GPL-3, más información en https://www.gnu.org/licenses/gpl-3.0.html**
