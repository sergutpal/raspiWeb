#include <sqlite3.h>

#define SQL_INSERT_TEMPERATURA "INSERT INTO historicoTemperatura(temperatura, humedad, data) VALUES (%.2f, %.2f, %s);"

#define DB_TEMPERATURA "/home/tmp/telegram/temperaturaraspi2DHT22.db"
	
int insertTemperatura(sqlite3 *db, float temperatura, float humedad);
