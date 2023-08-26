import 'dart:developer';

void printWarning(String text) {
  log('\x1B[33m$text\x1B[0m');
}

void printError(String text) {
  log('\x1B[31m$text\x1B[0m');
}
