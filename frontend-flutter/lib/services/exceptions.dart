class EmailUnverified implements Exception {
  String cause;
  EmailUnverified(this.cause);
}

class UserIsNull implements Exception {
  String cause;
  UserIsNull(this.cause);
}
