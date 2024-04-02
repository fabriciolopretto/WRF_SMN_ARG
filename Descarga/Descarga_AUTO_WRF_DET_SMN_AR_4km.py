"""
Descarga los archivos NetCDF que contienen
la salida operativa de 00Z ó 12Z del modelo numérico WRF-SMN.
"""

# Se importan las librerías necesarias
import requests
import os
import glob
import datetime

# Se captura la fecha y hora
time = datetime.datetime.utcnow()
anno_real = int(time.year)
mes_real = int(time.month)
dia_real = int(time.day)
hora_real = int(time.hour)

# Se define la corrida del modelo
# Anno
anno_tex = str(anno_real)
# Mes
if 10 > mes_real >= 1:
    mes_tex = '0' + str(mes_real)
if mes_real >= 10:
    mes_tex = str(mes_real)
# Dia
if 10 > dia_real >= 1:
    dia_tex = '0' + str(dia_real)
if dia_real >= 10:
    dia_tex = str(dia_real)
# Inicializacion   
if 0 <= hora_real < 12:
    hora_tex = '00'
if 12 <= hora_real <= 23:
   hora_tex = '12'

del time,anno_real,mes_real,dia_real,hora_real


# Define la ruta del script relativa al usuario
ruta = os.path.dirname((os.path.abspath(__file__)))
# limpia la carpeta de destino de corridas anteriores
# Archivos horarios e integrados
files = glob.glob(ruta + '/Archivos/*.nc')
for f in files:
    os.remove(f)
del files

# Crea el camino de los archivos con la corrida horaria
for i in range(72):
    if 10 > i >= 0:
        plazo = '00' + str(i)
    if 100 > i >= 10:
        plazo = '0' + str(i)
    downloadURL = 'https://smn-ar-wrf.s3.amazonaws.com/DATA/WRF/DET/'+anno_tex+'/'+mes_tex+'/'+dia_tex+'/'+hora_tex+'/WRFDETAR_01H_'+anno_tex+mes_tex+dia_tex+'_'+hora_tex+'_'+plazo+'.nc'
    req = requests.get(downloadURL)
    filename = req.url[downloadURL.rfind('/')+1:]
    # Descarga el archivo vigente
    with open(ruta + '/Archivos/'+ filename, 'wb') as f:
        for chunk in req.iter_content(chunk_size=8192):
            if chunk:
                f.write(chunk)
    del plazo,downloadURL,req,filename,chunk
del i

# Crea el camino de los archivos con la corrida integrada diaria
for i in range(3):
    if 10 > i >= 0:
        plazo = '00' + str(i)
    downloadURL = 'https://smn-ar-wrf.s3.amazonaws.com/DATA/WRF/DET/'+anno_tex+'/'+mes_tex+'/'+dia_tex+'/'+hora_tex+'/WRFDETAR_24H_'+anno_tex+mes_tex+dia_tex+'_'+hora_tex+'_'+plazo+'.nc'
    req = requests.get(downloadURL)
    filename = req.url[downloadURL.rfind('/')+1:]
    #Descarga el archivo vigente
    with open(ruta + '/Archivos/'+ filename, 'wb') as f:
        for chunk in req.iter_content(chunk_size=8192):
            if chunk:
                f.write(chunk)
    del plazo,downloadURL,req,filename,chunk
del i
