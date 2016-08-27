#!/usr/bin/python
import time
import globalVars
import picamera
import datetime
import os
import shutil

camera = None;
DELAY_FROM_PHOTOS = 1;
pathSendTelegram = globalVars.pathTmpTelegram;
pathTmp = '/tmp/';
extensionPhoto = '.png';

def initCamera():
  global camera;  
  global path;
  
  try:  
    camera = picamera.PiCamera();
    camera.brightness =50; # [0..100]
    camera.contrast =0; # [0..100]
    camera.saturation =0; # [0..100]
    camera.ISO = 0; # [0..100]
    camera.hflip = True;
    camera.vflip = True;
    camera.resolution = (640, 480);
  except Exception as e:
    globalVars.fileLog.write(globalVars.dateTime() + 'Error inicializando piCamera: ' + str(e) +'\n');
  return;

def cameraPhoto(pathTo):
  global camara;
  global path;
  global pathTmp;
  global extensionPhoto;

  try:
    initCamera();
    dt = datetime.datetime.now().strftime("%H%M%S%f");
    imgName = dt + extensionPhoto;
    pathImgTmp = pathTmp + imgName;
    pathImgTo = pathTo + imgName;
    camera.capture(pathImgTmp);
    camera.close();
    shutil.move(pathImgTmp, pathImgTo);
  except Exception as e:    
    globalVars.fileLog.write(globalVars.dateTime() + 'Error capturando fotografia (picamara): ' + str(e) +'\n');
  return pathImgTo;

cameraPhoto(pathSendTelegram);

