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
doorPIN = 37; # GPIO26

def initGPIO():
  global pirPIN;

  try:
    GPIO.setwarnings(False);
    GPIO.setmode(GPIO.BOARD);
    GPIO.setup(doorPIN, GPIO.IN)
    return 1;
  except Exception as e:
    print('Error inicializando GPIO: ' + str(e) +'\n');
    return 0;

def isDoorOpen():
  global doorPIN;
  pinActive = GPIO.input(doorPIN);
  if (pinActive):
    return True;
  else:
    return False;

ok =initGPIO();
if (ok ==1):
  while (True):
    pinActive = isDoorOpen();
    if (pinActive):
      print('Abierta!!!!!');
    else:
      print('Nada');
    time.sleep(CHECK_SECONDS);
