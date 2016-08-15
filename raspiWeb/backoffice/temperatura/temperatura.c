#include "temperaturaDAO.h"
#include "../comun/c/util.h"
#include "../comun/c/sqlUtil.h"
#include <wiringPi.h>
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <time.h>
#include <string.h>

#define DELAY_READ_ERROR 2000 // 2 segundos 

#define MAX_TIME 85
#define DHT22PIN 7 // Pin #7 de la Raspi (el cuarto contando por la izquierda (interior) en el dibujo sale como GPIO04 (GPIO_GCLK)
#define ATTEMPTS 10


int dht_val[5]={0,0,0,0,0};
sqlite3 *dbTemperatura;

int dht_read_val(int sensorDHT, float *temperatura, float *humedad) {
  //char buffer[100];
  //time_t ltime;
  //struct tm *curtime;
  uint8_t lststate=HIGH;
  uint8_t counter=0;
  uint8_t j=0,i;
  for(i=0;i<5;i++)
     dht_val[i]=0;
  pinMode(sensorDHT,OUTPUT);
  digitalWrite(sensorDHT,LOW);
  delay(18);
  digitalWrite(sensorDHT,HIGH);
  delayMicroseconds(40);
  pinMode(sensorDHT,INPUT);
  for(i=0;i<MAX_TIME;i++) {
    counter=0;
    while(digitalRead(sensorDHT)==lststate){
      counter++;
      delayMicroseconds(1);
      if(counter==255)
        break;
    }
    lststate=digitalRead(sensorDHT);
    if(counter==255)
       break;
    // top 3 transistions are ignored
    if((i>=4)&&(i%2==0)){
      dht_val[j/8]<<=1;
      if(counter>16)
        dht_val[j/8]|=1;
      j++;
    }
  }
  if ((j >= 40) && (dht_val[4] == ((dht_val[0] + dht_val[1] + dht_val[2] + dht_val[3]) & 0xFF)) ) {
	*humedad = (float)dht_val[0] * 256 + (float)dht_val[1];
	*humedad /= 10;
	*temperatura = (float)(dht_val[2] & 0x7F)* 256 + (float)dht_val[3];
	*temperatura /= 10.0;
	if ((dht_val[2] & 0x80) != 0)
		*temperatura *= -1;
	printf("Humedad = %.2f %% Temperatura = %.2f *C \n", *humedad, *temperatura);
	//time( &ltime );

	//curtime = localtime( &ltime );
	//strftime(buffer,100,"%d/%m/%Y %X", curtime);
	//sprintf(buffer, "%s Temperatura: %.2f. Humedad: %2.f%%\n", buffer, *temperatura, *humedad);
	//insertTemperatura(dbTemperatura, temperatura, humedad);
	return 1;
  }
  else {
	 printf("lectura NO valida!\n");
	 printf("%d.%d,%d.%d\n",dht_val[0],dht_val[1],dht_val[2],dht_val[3]);
	return 0;
  }
}

int main(void)
{
  int attempts =ATTEMPTS;
  int i;
  int ret;
  int error =0;
  float temperatura =0, humedad =0;

  ret =wiringPiSetup();
  if(ret <0)
    exit(1);

  error = sqlite3_open(DB_TEMPERATURA, &dbTemperatura);
  if (error !=0) {
       toFile(FILE_LOG, "Error DHT22 intentando abrir BD temperatura.db", FILE_MODE_APPEND);
       exit(EXIT_FAILURE);
  }

  for (i =0; i <5; i++)
    dht_val[i] =0;
  attempts =ATTEMPTS;
  // Lectura del DHT22
  while(attempts) {
    int success = dht_read_val(DHT22PIN, &temperatura, &humedad);
    if (success) {
      insertTemperatura(dbTemperatura, temperatura, humedad);
      break;
    }
    attempts--;
    delay(DELAY_READ_ERROR);  // En caso de error reintentamos pasados X segundos
  }
  sqlite3_close(dbTemperatura);
  return 0;
}
