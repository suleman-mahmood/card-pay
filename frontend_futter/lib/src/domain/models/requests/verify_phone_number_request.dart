// ignore_for_file: public_member_api_docs, sort_constructors_first
import 'dart:convert';

class VerifyPhoneNumberRequest {
  final String otp;

  VerifyPhoneNumberRequest({required this.otp});

  VerifyPhoneNumberRequest copyWith({String? otp}) {
    return VerifyPhoneNumberRequest(otp: otp ?? this.otp);
  }

  Map<String, dynamic> toMap() {
    return <String, dynamic>{'otp': otp};
  }

  @override
  String toString() => 'VerifyPhoneNumberRequest(otp: $otp)';

  @override
  bool operator ==(covariant VerifyPhoneNumberRequest other) {
    if (identical(this, other)) return true;

    return other.otp == otp;
  }

  @override
  int get hashCode => otp.hashCode;
}
