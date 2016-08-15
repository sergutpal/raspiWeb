#include <sqlite3.h>

#define SQL_GET_CONFIG "SELECT * FROM configPi WHERE idPi =%d;"
#define SQL_IS_ALARM_ACTIVE "SELECT activa FROM alarma;"
#define SQL_INSERT_ALARM "INSERT INTO historicoAlarma (activa, data) VALUES (%d, %s);"

#define DB_ALARM "/home/nfs/telegram/db/alarma.db"

int isAlarmActive(sqlite3 *db);
void getSetupPi(sqlite3 *db, int idPi, int *dht22, int *dht11, int *pir, int *camera, int *HCSR04, int *Buzzer);
int insertAlarm(sqlite3 *db, int activa);
