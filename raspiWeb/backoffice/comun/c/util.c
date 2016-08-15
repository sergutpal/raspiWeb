#include "util.h"
#include <stdio.h>

void toFile(char *pathFile, char *txt, char *mode) {
  FILE *tmpFile;

  tmpFile = fopen(pathFile, mode);
  if (tmpFile !=NULL) {
    fprintf(tmpFile, txt);
    fflush(tmpFile);
    fclose(tmpFile);
  }
}
