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
    // Minimum eight characters, at least one letter and one number:
    final passwordRegExp = RegExp(r"^(?=.*[A-Za-z])(?=.*\d)[A-Za-z\d]{8,}$");
    return passwordRegExp.hasMatch(this);
  }

  bool get isValidPin {
    // 4-digit numeric pin:
    final pinRegExp = RegExp(r"^\d{4}$");
    return pinRegExp.hasMatch(this);
  }
}
