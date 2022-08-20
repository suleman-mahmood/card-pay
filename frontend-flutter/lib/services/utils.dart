// helps in debugging- will be deleted later
void printError(String text) {
  print('\x1B[31m$text\x1B[0m');
}

void printWarning(String text) {
  print('\x1B[33m$text\x1B[0m');
}

void printInGreen(String text) {
  print('\x1B[32m$text\x1B[0m');
}

final Map codeToMessage = {
  "wrong-password": "Incorrect Password",
  "user-not-found": "User not found",
  "user-disabled": "Cannot login, Please contact helpline",
  "too-many-requests": "Too many requests. Try again later.",
  "email-already-in-use": "Roll number is already registered",
  "weak-password":
      "Minimum eight characters, at least one uppercase letter, one lowercase letter, one number and one special character:",
};
