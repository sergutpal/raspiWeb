#include <sqlite3.h>

#define SQL_INSERT_EFERGY "INSERT INTO historicoEfergy (energia, data) VALUES (%.2f, %s);"
#define SQL_SELECT_LAST_EFERGY "SELECT energia FROM historicoEfergy ORDER BY id DESC LIMIT 1;"
#define SQL_SELECT_RESUME_EFERGY "SELECT COUNT(*) AS NumTotal, MAX(energia) AS Maximo, MIN(energia) as Minimo, AVG(energia) as Media FROM historicoEfergy WHERE data BETWEEN %s AND %s;"

#define DB_EFERGY "/home/tmp/telegram/efergy.db"

float lastEfergy(sqlite3 *db);
int insertEfergy(sqlite3 *db, float energia);
