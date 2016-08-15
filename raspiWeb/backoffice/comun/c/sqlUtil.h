#include <sqlite3.h>

#define DATETIME_NOW "datetime('now', 'localtime')"
#define DATETIME_TODAY "datetime('now', 'start of day')" // Dia actual des de las 00:00:00
#define DATETIME_LAST_HOUR "datetime('now', '-1 hour')"
#define DATETIME_LAST_24H "datetime('now', '-1 day')"

void resumeHistoric(sqlite3 *db, char* sql, char* dataBegin, char* dataEnd, int *totalRegisters, float *maxValue, float *minValue, float *avgValue);
static int callbackNothing(void *data, int argc, char **argv, char **azColName);
int qryNonUpdate(sqlite3 *db, char *sql);
void qrySelect(sqlite3 *db, char *sql, char*** resultTable, int *row, int *column, int *error);
void getQryValue(char*** resultTable, int row, int column, int totalColumns, char *result);
void qrySelectOneValueStr(sqlite3 *db, char *sql, char *result, int *error);
float qrySelectOneValueFloat(sqlite3 *db, char *sql, int *error);
int qrySelectOneValueInt(sqlite3 *db, char *sql, int *error);
