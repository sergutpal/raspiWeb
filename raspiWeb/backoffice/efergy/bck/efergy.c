/*
CREATE TABLE efergy(energia FLOAT, data DATETIME NULL);
INSERT INTO efergy (energia, data) VALUES (0, datetime('1900-01-01 00:00:00'));
CREATE TABLE historicoEfergy(id INTEGER PRIMARY KEY  NOT NULL, energia FLOAT NOT NULL, data DATETIME NULL);

CREATE TRIGGER trg_historico_actualiza_efergy AFTER INSERT ON historicoEfergy
BEGIN
    UPDATE efergy SET energia = new.energia, data = new.data;
END;
*/


/*---------------------------------------------------------------------
EFERGY E2 CLASSIC RTL-SDR DECODER via rtl_fm
Copyright 2013 Nathaniel Elijah
Compile:
gcc -lm -o EfergyRPI_001 EfergyRPI_001.c

Execute using the following parameters:
rtl_fm -f 433550000 -s 200000 -r 96000 -g 19.7 2>/dev/null | ./EfergyRPI_001
*/

#include "efergyDAO.h"
#include "../comun/c/alarmaDAO.h"
#include "../comun/c/util.h"
#include "../comun/c/sqlUtil.h"
#include <stdio.h>
#include <stdint.h>
#include <time.h>
#include <math.h>
#include <string.h>
#include <stdlib.h> // For exit function
#include <unistd.h>

#define MAX_WATTS_ALERT_NO_ALARM 8000
#define MAX_WATTS_ALERT_ALARM 600
#define MAX_WATTS_VALID 15000
#define ALERT_WATTS_TIME_PERIOD 600 // Cada cuantos segundos se envia la alerta de energia
#define ALERT_NO_ENERGY "ALERTA! Efergy detecta 0W de consumo! Posiblemente se ha ido la luz!!\n" // Importante anyadir el salto de linea para Telegram!
#define ALERT_MAX_ENERGY "Alerta maximo consumo energia superado:"

#define VOLTAGE 		230	/* Refernce Voltage */
#define CENTERSAMP		100	/* Number of samples needed to compute for the wave center */
#define PREAMBLE_COUNT		40	/* Number of high(1) samples for a valid preamble */
#define MINLOWBIT		3	/* Number of high(1) samples for a logic 0 */
#define MINHIGHBIT		8	/* Number of high(1) samples for a logic 1 */
#define E2BYTECOUNT		8	/* Efergy E2 Message Byte Count */
#define FRAMEBITCOUNT		64	/* Number of bits for the entire frame (not including preamble) */


#define LOGTYPE 	   1 // Allows changing line-endings - 0 is for Unix /n, 1 for Windows /r/n
#define SAMPLES_TO_FLUSH  10 // Number of samples taken before writing to file.
			     // Setting this too low will cause excessive wear to flash due to updates to
			     // filesystem! You have been warned! Set to 10 samples for 6 seconds = every min.


time_t lastAlert;
int bAlerted =0;
double lastResult =-1;

sqlite3 *dbAlarm;
sqlite3 *dbEfergy;

int calculate_watts(char bytes[]) {
	char tbyte;
	double current_adc;
	double result;
	double maxWattsAlert;
	int i;

	time_t ltime;
	struct tm *curtime;
	char buffer[80];
	char buffer2[80];
	char buffer3[80];

	/* add all captured bytes and mask lower 8 bits */

	tbyte = 0;

	for(i=0;i<7;i++)
		tbyte += bytes[i];

	tbyte &= 0xff;

	/* if checksum matches get watt data */
	if (tbyte == bytes[7])
	{
		time( &ltime );
		curtime = localtime( &ltime );
		strftime(buffer,80,"%d/%m/%Y;%X", curtime);

		current_adc = (bytes[4] * 256) + bytes[5];
		result	= (VOLTAGE * current_adc) / ((double) 32768 / (double) pow(2,bytes[6]));
		if((result <MAX_WATTS_VALID) && ((result >0) || (lastResult ==0))) { // Comprobamos que el valor sea valido. En caso contrario ignoramos la lectura
		  // Si el valor obtenido es 0, puede tratarse de una lectura erronea. En ese caso comprobamos si la ultima lectura fue errone y en caso afirmativo entendemos que es buena
		  insertEfergy(dbEfergy, result);
		  strftime(buffer2,80,"%d/%m/%Y %X", curtime);
		  sprintf(buffer3,"Energia: %s - %.2fW\n",buffer2,result);

		  if (!bAlerted) { // NO enviamos todas las alertas para no saturar. Solo 1 cada 10 minutos
			time(&lastAlert);
		  	if (result ==0) {  // SE HA IDO LA LUZ!!!
			    sprintf(buffer,"%s %s", buffer2, ALERT_NO_ENERGY);
			    toFile(FILE_TELEGRAM_SEND, buffer, FILE_MODE_APPEND);
  			    toFile(FILE_ALERTS, buffer, FILE_MODE_APPEND);
			}
		  	if (isAlarmActive(dbAlarm)) {
		    		maxWattsAlert =MAX_WATTS_ALERT_ALARM;
		  	}
		  	else {
		     		maxWattsAlert =MAX_WATTS_ALERT_NO_ALARM;
		  	}
		  	if (result >=maxWattsAlert) { // Consumo maximo de energia superado!
		    		sprintf(buffer, "%s %s %.2fW!\n", buffer2, ALERT_MAX_ENERGY, result);
		    		toFile(FILE_TELEGRAM_SEND, buffer, FILE_MODE_APPEND);
		    		toFile(FILE_ALERTS, buffer, FILE_MODE_APPEND);
		  	}
			bAlerted = 1;
		  }
		  else {
			if (difftime(ltime, lastAlert) >ALERT_WATTS_TIME_PERIOD) // Cada 10 minutos enviamos de nuevo las alertas
				bAlerted = 0;
		  }
		}
		else {
			toFile(FILE_LOG, "Error efergy valor no valido!", FILE_MODE_APPEND);
		}
		lastResult = result;
		return 1;
	}
	return 0;
}

int main (int argc, char**argv) {
	char bytearray[9];
	char bytedata;

	int prvsamp;
	int hctr;
	int cursamp;
	int bitpos;
	int bytecount;

	int preamble;
	int frame;
	int dcenter;
	int dbit;

	long center;
	int error;

	//sleep(1);

	error = sqlite3_open(DB_ALARM, &dbAlarm);
	if (error !=0) {
		toFile(FILE_LOG, "Error efergy intentando abrir BD alarma.db", FILE_MODE_APPEND);
		exit(EXIT_FAILURE);
	}
	error = sqlite3_open(DB_EFERGY, &dbEfergy);
 	if (error !=0) {
                toFile(FILE_LOG, "Error efergy intentando abrir BD efergy.db", FILE_MODE_APPEND);
                exit(EXIT_FAILURE);
        }

	/* initialize variables */

	time(&lastAlert);

	cursamp = 0;
	prvsamp = 0;

	bytedata = 0;
	bytecount = 0;
	hctr = 0;
	bitpos = 0;
	dbit = 0;
	preamble = 0;
	frame = 0;

	dcenter = CENTERSAMP;
	center = 0;

	printf("Monitor Efergy inicializado correctamente\n");

	while( !feof(stdin) ) {
		cursamp  = (int16_t) (fgetc(stdin) | fgetc(stdin)<<8);
		/* initially capture CENTERSAMP samples for wave center computation */
		if (dcenter > 0)
		{
			dcenter--;
			center = center + cursamp;	/* Accumulate FSK wave data */

			if (dcenter == 0)
			{
				/* compute for wave center and re-initialize frame variables */

				center = (long) (center/CENTERSAMP);

				hctr  = 0;
				bytedata = 0;
				bytecount = 0;
				bitpos = 0;
				dbit = 0;
				preamble = 0;
				frame = 0;
			}

		}
		else
		{
			if ((cursamp > center) && (prvsamp < center))		/* Detect for positive edge of frame data */
				hctr = 0;
			else
				if ((cursamp > center) && (prvsamp > center))		/* count samples at high logic */
				{
					hctr++;
					if (hctr > PREAMBLE_COUNT)
						preamble = 1;
				}
				else
					if (( cursamp < center) && (prvsamp > center))
					{
						/* at negative edge */

						if ((hctr > MINLOWBIT) && (frame == 1))
						{
							dbit++;
							bitpos++;
							bytedata = bytedata << 1;
							if (hctr > MINHIGHBIT)
								bytedata = bytedata | 0x1;

							if (bitpos > 7)
							{
								bytearray[bytecount] = bytedata;
								bytedata = 0;
								bitpos = 0;

								bytecount++;

								if (bytecount == E2BYTECOUNT)
								{

									/* at this point check for checksum and calculate watt data */
									/* if there is a checksum mismatch compute for a new wave center */

									if (calculate_watts(bytearray) == 0)
										dcenter = CENTERSAMP;	/* make dcenter non-zero to trigger center resampling */
								}
							}
							if (dbit > FRAMEBITCOUNT) {
								/* reset frame variables */

								bitpos = 0;
								bytecount = 0;
								dbit = 0;
								frame = 0;
								preamble = 0;
								bytedata = 0;
							}
						}

						hctr = 0;

					}
					else
						hctr = 0;

			if ((hctr == 0) && (preamble == 1))
			{
				/* end of preamble, start of frame data */
				preamble = 0;
				frame = 1;
			}

		} /* dcenter */

		prvsamp = cursamp;

	} /* while */
	sqlite3_close(dbAlarm);
	sqlite3_close(dbEfergy);
	return 0;
}
