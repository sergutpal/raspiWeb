#include "temperaturaDAO.h"
#include "../comun/c/sqlUtil.h"
#include "../comun/c/util.h"
#include <sqlite3.h>
#include <stdio.h>
#include <string.h>
#include <stdlib.h>

int insertTemperatura(sqlite3 *db, float temperatura, float humedad) {
  char sql[255];

  sprintf(sql, SQL_INSERT_TEMPERATURA, temperatura, humedad, DATETIME_NOW);
  return qryNonUpdate(db, sql);
}
