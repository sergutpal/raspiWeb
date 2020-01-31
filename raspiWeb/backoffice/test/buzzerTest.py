#!/usr/bin/python
import RPi.GPIO as GPIO
import time
import socket
import datetime
import os
import shutil
import subprocess

buzzerPIN = 40; # GPIO21

def initGPIO():
  global buzzerPIN;

  try:
    GPIO.setwarnings(False);
    GPIO.setmode(GPIO.BOARD);
    GPIO.setup(buzzerPIN, GPIO.OUT);
    GPIO.output(buzzerPIN, 0);
    return 1;
  except Exception as e:
    print('Error inicializando GPIO: ' + str(e) +'\n');
    return 0;

def buzzer(freq, repeat):
  global buzzerPIN;
  for x in range(0,repeat):
    GPIO.output(buzzerPIN,1)
    time.sleep(freq)
    GPIO.output(buzzerPIN,0)
    time.sleep(freq)
  return None;

ok =initGPIO();
if (ok ==1):
  print('antes de buzzer');
  buzzer(0.3, 5);
  print('despues de buzzer');
