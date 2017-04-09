/*
CREATE TABLE alarma(activa INTEGER);
INSERT INTO alarma (activa) VALUES (0);
CREATE TABLE historicoAlarma(id INTEGER PRIMARY KEY NOT NULL, activa INTEGER NOT NULL, data DATETIME NULL);

CREATE TRIGGER trg_historico_actualiza_alarma AFTER INSERT ON historicoAlarma
BEGIN
    UPDATE alarma SET activa = new.activa;
END;


CREATE TABLE configPi(idPi INTEGER PRIMARY KEY NOT NULL, dht22 INTEGER, dht11 INTEGER, pir INTEGER, camara INTEGER, HCSR04 INTEGER, Buzzer INTEGER);

INSERT INTO configPi(idPi, dht22, dht11, pir, camara, HCSR04, Buzzer) VALUES (30, 0, 0, 0, 0, 0, 0);
INSERT INTO configPi(idPi, dht22, dht11, pir, camara, HCSR04, Buzzer) VALUES (31, 1, 0, 1, 1, 0, 1);

*/

#include "alarmaDAO.h"
#include "sqlUtil.h"
#include "util.h"
#include <sqlite3.h>
#include <stdio.h>
#include <string.h>
#include <stdlib.h>

int isAlarmActive(sqlite3 *db) {
	int error, value;

	value = qrySelectOneValueInt(db, SQL_IS_ALARM_ACTIVE, &error);
	if (error) // Si hay error consideramos que la alarma está inactiva
		value = 0;
        if (value >1) // Si estamos en modo nocturno, no consideramos que estamos en modo Alarma
                value = 0;
        return value;
}

void getSetupPi(sqlite3 *db, int idPi, int *dht22, int *dht11, int *pir, int *camera, int *HCSR04, int *Buzzer) {
  char **resultTable =NULL;
  char result[100];
  char sql[200];
  int error;
  int column =0;
  int row =0;

  sprintf(sql, SQL_GET_CONFIG, idPi);
  qrySelect(db, sql, &resultTable, &row, &column, &error);
  if (!error) {
	getQryValue(&resultTable, row, 2, column, result); // La columna 1 es idPi
	*dht22 =atoi(result);
	getQryValue(&resultTable, row, 3, column, result);
	*dht11 =atoi(result);
	getQryValue(&resultTable, row, 4, column, result);
	*pir =atoi(result);
	getQryValue(&resultTable, row, 5, column, result);
	*camera =atoi(result);
	getQryValue(&resultTable, row, 6, column, result);
	*HCSR04 =atoi(result);
	getQryValue(&resultTable, row, 7, column, result);
	*Buzzer =atoi(result);
  }
  sqlite3_free_table(resultTable);
}

int insertAlarm(sqlite3 *db, int activa) {
  char sql[100];

  sprintf(sql, SQL_INSERT_ALARM, activa, DATETIME_NOW);
  return qryNonUpdate(db, sql);
}
