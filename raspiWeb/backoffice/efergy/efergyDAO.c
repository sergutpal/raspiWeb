#include "efergyDAO.h"
#include "../comun/c/sqlUtil.h"
#include "../comun/c/util.h"
#include <sqlite3.h>
#include <stdio.h>
#include <string.h>
#include <stdlib.h>

float lastEfergy(sqlite3 *db) {
	int error;
	float value;

	value = qrySelectOneValueFloat(db, SQL_SELECT_LAST_EFERGY, &error);
	if (error) // Si hay error consideramos la energia es 0
		value = 0;
	return value;
}

int insertEfergy(sqlite3 *db, float energia) {
  char sql[255];

  sprintf(sql, SQL_INSERT_EFERGY, energia, DATETIME_NOW);
  system("/home/nfs/telegram/gpio/efergy/efergyToMQTT.sh");
  return qryNonUpdate(db, sql);
}
