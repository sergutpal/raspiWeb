#include "sqlUtil.h"
#include "util.h"
#include <sqlite3.h>
#include <stdio.h>
#include <string.h>
#include <stdlib.h>

static int callbackNothing(void *data, int argc, char **argv, char **azColName){
   printf("\nsoy callbackNothing");
   return 0;
}

// Calcula los datos de resumen de la tabla de historico para el dia en curso (des de las 00:00:00 hasta el momento de la llamada)
void resumeHistoric(sqlite3 *db, char* sql, char* dataBegin, char* dataEnd, int *totalRegisters, float *maxValue, float *minValue, float *avgValue) {
  char **resultTable =NULL;
  char result[100];
  char sqlDate[200];
  int error;
  int column =0;
  int row =0;

  sprintf(sqlDate, sql, dataBegin, dataEnd);
  qrySelect(db, sqlDate, &resultTable, &row, &column, &error);
  if (!error) {
        getQryValue(&resultTable, row, 1, column, result); // NumTotal
        *totalRegisters =atoi(result);
        getQryValue(&resultTable, row, 2, column, result); // Maximo
        *maxValue =atof(result);
        getQryValue(&resultTable, row, 3, column, result); // Maximo
        *minValue =atof(result);
        getQryValue(&resultTable, row, 4, column, result); // Media
        *avgValue =atof(result);
  }
  sqlite3_free_table(resultTable);
}

int qryNonUpdate(sqlite3 *db, char *sql) {
  char *zErrMsg =0;
  char errStr[1000];
  int result;

  result = sqlite3_exec(db, sql, callbackNothing, 0, &zErrMsg);
  if( result != SQLITE_OK ){
    sprintf(errStr, "Error sqlite3: %s. %s", sql, zErrMsg);
    toFile(FILE_LOG, errStr, FILE_MODE_APPEND);
    sqlite3_free(zErrMsg);
  }
  return result;
}

void qrySelect(sqlite3 *db, char *sql, char*** resultTable, int *row, int *column, int *error) {
  char* error_get_table =NULL;
  char errStr[255];

  *error =sqlite3_get_table(db, sql, resultTable, row, column, &error_get_table);
  if (*error) {
    sprintf(errStr, "Error sqlite3: %s. %s", sql, error_get_table);
	toFile(FILE_LOG, errStr, FILE_MODE_APPEND);
	sqlite3_free(error_get_table);
	error_get_table = NULL;
  }
}

// IMPORTANTE: Para recuperar los datos del registro debemos especificar row =1 y para la primera columna column =1
void getQryValue(char*** resultTable, int row, int column, int totalColumns, char *result) {
  int i;
  char **resultT;

  i =row * totalColumns + column -1;
  resultT = *resultTable;
  strcpy(result, resultT[i]);
}

void qrySelectOneValueStr(sqlite3 *db, char *sql, char *result, int *error) {
  char **resultTable =NULL;
  int column =0;
  int row =0;

  qrySelect(db, sql, &resultTable, &row, &column, error);
  if (!*error) {
	getQryValue(&resultTable, 1, 1, 1, result); // El dato a recuperar viene en el primer registro, primera columna
  }
  sqlite3_free_table(resultTable);
}

float qrySelectOneValueFloat(sqlite3 *db, char *sql, int *error) {
  char result[20];
  float value =-1;

  qrySelectOneValueStr(db, sql, result, error);
  if (!*error)
     value =atof(result);
 return value;
}

int qrySelectOneValueInt(sqlite3 *db, char *sql, int *error) {
  char result[20];
  int value =-1;

  qrySelectOneValueStr(db, sql, result, error);
  if (!*error)
     value =atoi(result);
 return value;
}

