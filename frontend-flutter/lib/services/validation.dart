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
    final rollNumberRegExp = RegExp(r"^[0-9]{8}$");
    final passwordRegExp =
        RegExp(r"(?=.*[a-z])(?=.*[A-Z])(?=.*[0-9])(?=.*[^A-Za-z0-9])(?=.{8,})");
    return rollNumberRegExp.hasMatch(this);
  }
}
