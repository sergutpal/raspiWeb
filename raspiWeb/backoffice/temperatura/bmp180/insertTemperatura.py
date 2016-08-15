# crontab -e
#0 * * * * python /hdd/nfs/telegram/gpio/temperatura/bmp180/insertTemperatura.py
#15 * * * * python /hdd/nfs/telegram/gpio/temperatura/bmp180/insertTemperatura.py
#30 * * * * python /hdd/nfs/telegram/gpio/temperatura/bmp180/insertTemperatura.py
#45 * * * * python /hdd/nfs/telegram/gpio/temperatura/bmp180/insertTemperatura.py


#CREATE TABLE temperatura(temperatura FLOAT, humedad FLOAT, presion FLOAT, data DATETIME NULL);
#INSERT INTO temperatura (temperatura) VALUES (0);
#CREATE TABLE historicoTemperatura(id INTEGER PRIMARY KEY NOT NULL, temperatura FLOAT NOT NULL, humedad FLOAT, presion FLOAT, data DATETIME NULL);

#CREATE TRIGGER trg_historico_actualiza_temperatura AFTER INSERT ON historicoTemperatura
#BEGIN
#    UPDATE temperatura SET temperatura = new.temperatura, humedad = new.humedad, presion = new.presion, data = new.data;
#END;

import Adafruit_BMP.BMP085 as BMP085
import sqlite3
import globalVars
 
#Otros modos adicionales del sensor son 
#(BMP085_ULTRALOWPOWER, BMP085_STANDARD, 
#BMP085_HIGHRES, o BMP085_ULTRAHIGHRES) Ejemplo de 
#uso: syensor = 
#BMP085.BMP085(mode=BMP085.BMP085_ULTRAHIGHRES)

#print 'Altitude = {0:0.2f} m'.format(sensor.read_altitude())
#print 'Sealevel Pressure = {0:0.2f} Pa'.format(sensor.read_sealevel_pressure())
 
#Tambien puedes cambiar el numero de bus. Ejemplo de 
#uso: sensor = BMP085.BMP085(busnum=2)

SQL_TEMPERATURA_INSERT = 'INSERT INTO historicoTemperatura(temperatura, presion, data) VALUES (temp1, pressure1, ' + globalVars.DATETIME_NOW + ');'
temperature = None
pressure = None

def getTemperaturePressure(): 
  global temperature
  global pressure
 
  try:
    sensor = BMP085.BMP085()
    temperature = sensor.read_temperature()
    pressure = sensor.read_pressure()
    return temperature
  except Exception as e:
    globalVars.toLogFile('Error getTemperaturePressure: ' + str(e) + '\n')
    return None

def insertTemperaturePressure():
  global temperature
  global pressure

  pathTemperatureDB = globalVars.getTemperatureDBPath()
  getTemperaturePressure()
  try:
    temperatureDB = sqlite3.connect(pathTemperatureDB)
    cursor = temperatureDB.cursor()
    sqlExec = SQL_TEMPERATURA_INSERT.replace('temp1', str(round(temperature, 1))).replace('pressure1', str(round(pressure, 1)))
    #print 'sqlExec: ' + sqlExec
    cursor.execute(sqlExec)
    temperatureDB.commit()
    cursor.close()
    temperatureDB.close()
  except Exception as e:
    globalVars.toLogFile('Error insertTemperaturePressure: ' + str(e) + '\n')
    return None
  finally:
    temperatureDB.close()

if __name__ == "__main__":
  insertTemperaturePressure()
