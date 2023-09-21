extension StringAddons on String {
  bool get isValidLumsRollNumber {
    final rollNumberRegExp = RegExp(r"^[0-9]{8}$");
    return rollNumberRegExp.hasMatch(this);
  }

  bool get isValidFullName {
    final nameRegExp =
        RegExp(r"^\s*([A-Za-z]{1,}([\.,] |[-']| ))+[A-Za-z]+\.?\s*$");
    return nameRegExp.hasMatch(this);
  }

  bool get isValidPassword {
    // Minimum eight characters, at least one letter and one number:
    final passwordRegExp =
        RegExp(r"^(?=.*[A-Za-z])(?=.*\d)[A-Za-z\d!@#$%^&*()_+=-]{8,}$");
    return passwordRegExp.hasMatch(this);
  }

  bool get isValidPin {
    // 4-digit numeric pin:
    final pinRegExp = RegExp(r"^\d{4}$");
    return pinRegExp.hasMatch(this);
  }

  bool get isValidOtp {
    // 4-digit numeric pin:
    final otpRegExp = RegExp(r"^\d{4}$");
    return otpRegExp.hasMatch(this);
  }

  bool get isValidEmail {
    // Email:
    final emailRegExp =
        RegExp(r"^[a-zA-Z0-9.a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,4}$");
    return emailRegExp.hasMatch(this);
  }

  bool get isValidPhoneNumber {
    // Phone number:
    final phoneNumberRegExp = RegExp(r"^[0-9]{10,15}$");
    return phoneNumberRegExp.hasMatch(this);
  }
}
