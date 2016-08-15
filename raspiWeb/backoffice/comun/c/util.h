#include <stdio.h>

#define FILE_ALERTS "/home/nfs/telegram/logs/logAlerts.txt"
#define FILE_TELEGRAM_SEND "/home/tmp/telegram/send.txt"

#define FILE_LOG "/home/nfs/telegram/logs/log.txt"

#define FILE_MODE_APPEND "a+"
#define FILE_MODE_WRITE "w"

void toFile(char *pathFile, char *txt, char *mode);
