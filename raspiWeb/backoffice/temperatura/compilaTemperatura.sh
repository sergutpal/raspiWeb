rm temperatura
gcc temperatura.c temperaturaDAO.c ../comun/c/sqlUtil.c ../comun/c/util.c -o temperatura -lwiringPi -lsqlite3 -Wall -lm
