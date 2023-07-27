// ignore_for_file: public_member_api_docs, sort_constructors_first
import 'dart:convert';

import 'package:flutter/foundation.dart';

class CreateCustomerRequest {
  final String personalEmail;
  final String phoneNumber;
  final String fullName;
  final String password;
  final List<double> location;

  CreateCustomerRequest({
    required this.personalEmail,
    required this.phoneNumber,
    required this.fullName,
    required this.password,
    this.location = const [0.0, 0.0],
  });

  CreateCustomerRequest copyWith({
    String? personalEmail,
    String? phoneNumber,
    String? fullName,
    String? password,
    List<double>? location,
  }) {
    return CreateCustomerRequest(
      personalEmail: personalEmail ?? this.personalEmail,
      phoneNumber: phoneNumber ?? this.phoneNumber,
      fullName: fullName ?? this.fullName,
      password: password ?? this.password,
      location: location ?? this.location,
    );
  }

  Map<String, dynamic> toMap() {
    return <String, dynamic>{
      'personal_email': personalEmail,
      'phone_number': phoneNumber,
      'full_name': fullName,
      'password': password,
      'location': location,
    };
  }

  factory CreateCustomerRequest.fromMap(Map<String, dynamic> map) {
    return CreateCustomerRequest(
      personalEmail: map['personalEmail'] as String,
      phoneNumber: map['phoneNumber'] as String,
      fullName: map['fullName'] as String,
      password: map['password'] as String,
      location: List<double>.from((map['location'] as List<double>)),
    );
  }

  String toJson() => json.encode(toMap());

  factory CreateCustomerRequest.fromJson(String source) =>
      CreateCustomerRequest.fromMap(
          json.decode(source) as Map<String, dynamic>);

  @override
  String toString() {
    return 'CreateCustomerRequest(personalEmail: $personalEmail, phoneNumber: $phoneNumber, fullName: $fullName, password: $password, location: $location)';
  }

  @override
  bool operator ==(covariant CreateCustomerRequest other) {
    if (identical(this, other)) return true;

    return other.personalEmail == personalEmail &&
        other.phoneNumber == phoneNumber &&
        other.fullName == fullName &&
        other.password == password &&
        listEquals(other.location, location);
  }

  @override
  int get hashCode {
    return personalEmail.hashCode ^
        phoneNumber.hashCode ^
        fullName.hashCode ^
        password.hashCode ^
        location.hashCode;
  }
}
