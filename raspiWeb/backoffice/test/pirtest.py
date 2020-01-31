#!/usr/bin/python
import globalVars
import RPi.GPIO as GPIO
import time
import socket
import datetime
import os
import shutil
import subprocess

CHECK_SECONDS = 0.3;
pirPIN = 11; # GPIO17

def initGPIO():
  global pirPIN;

  try:
    GPIO.setwarnings(False);
    GPIO.setmode(GPIO.BOARD);
    GPIO.setup(pirPIN, GPIO.IN)
    return 1;
  except Exception as e:
    print('Error inicializando GPIO: ' + str(e) +'\n');
    return 0;

def isPIRActive():
  global pirPIN;
  pirActive = GPIO.input(pirPIN);
  if (pirActive):
    return True;
  else:
    return False;


ok =initGPIO();
if (ok ==1):
  while (True):
    pirActive = isPIRActive();
    if (pirActive):
      print ('Activo!');
    else:
      print ('nada');
    time.sleep(CHECK_SECONDS);
