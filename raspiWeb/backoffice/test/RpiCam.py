#!/usr/bin/python
import time
import globalVars
import datetime
import subprocess

def RpiCamRaspiMJPEG(start):
  global RpiCamStarted;
  try:
    if start:
      cmd = 'ru 1';
    else:
      cmd = 'ru 0';
    globalVars.toFile(globalVars.pathRpiCamFIFO, cmd);
    globalVars.RpiCamStarted = start;
    if start:
      time.sleep(5); # Esperamos 5 segundos para que no se pierda ninguna comanda 
    return globalVars.RpiCamStarted;
  except Exception as e:
    globalVars.fileLog.write(globalVars.dateTime() + 'Error RpiCam ' + str(start) + ': ' + str(e) +'\n');
    return globalVars.RpiCamStarted;

def RpiCamPhoto():
  try:
    if not globalVars.RpiCamStarted:
      RpiCamRaspiMJPEG(True);
    globalVars.toFile(globalVars.pathRpiCamFIFO, 'im');
    return '';
  except Exception as e:    
    globalVars.fileLog.write(globalVars.dateTime() + 'Error capturando fotografia (RpiCam): ' + str(e) +'\n');
    return '';

RpiCamPhoto();
time.sleep(2);
RpiCamPhoto();
time.sleep(2);
RpiCamPhoto();
time.sleep(2);
RpiCamRaspiMJPEG(False);
