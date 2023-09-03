// ignore_for_file: public_member_api_docs, sort_constructors_first
import 'dart:convert';

class Login {
  String phoneNumber;
  String password;
  Login({
    this.phoneNumber = '',
    this.password = '',
  });

  Login copyWith({
    String? phoneNumber,
    String? password,
  }) {
    return Login(
      phoneNumber: phoneNumber ?? this.phoneNumber,
      password: password ?? this.password,
    );
  }

  Map<String, dynamic> toMap() {
    final result = <String, dynamic>{};

    result.addAll({'phone_number': phoneNumber});
    result.addAll({'password': password});

    return result;
  }

  factory Login.fromMap(Map<String, dynamic> map) {
    return Login(
      phoneNumber: map['phone_number'] ?? '',
      password: map['password'] ?? '',
    );
  }

  String toJson() => json.encode(toMap());

  factory Login.fromJson(String source) => Login.fromMap(json.decode(source));

  @override
  String toString() => 'Login(phoneNumber: $phoneNumber, password: $password)';

  @override
  bool operator ==(Object other) {
    if (identical(this, other)) return true;

    return other is Login &&
        other.phoneNumber == phoneNumber &&
        other.password == password;
  }

  @override
  int get hashCode => phoneNumber.hashCode ^ password.hashCode;
}
