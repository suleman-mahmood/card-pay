extension stringAddOns on String {
  bool get isValidRollNumber {
    final emailRegExp = RegExp(r"^[0-9]{8}$");
    return emailRegExp.hasMatch(this);
  }

  bool get isValidName {
    final nameRegExp =
        RegExp(r"^\s*([A-Za-z]{1,}([\.,] |[-']| ))+[A-Za-z]+\.?\s*$");
    return nameRegExp.hasMatch(this);
  }

  bool get isValidPassword {
    // Minimum eight characters, at least one uppercase letter,
    // one lowercase letter, one number and one special character:
    final passwordRegExp = RegExp(
        r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$");
    return passwordRegExp.hasMatch(this);
  }
}
