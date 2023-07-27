// ignore_for_file: public_member_api_docs, sort_constructors_first
import 'dart:convert';

class VerifyPhoneNumberRequest {
  final String userId;
  final String otp;

  VerifyPhoneNumberRequest({
    required this.userId,
    required this.otp,
  });

  VerifyPhoneNumberRequest copyWith({
    String? userId,
    String? otp,
  }) {
    return VerifyPhoneNumberRequest(
      userId: userId ?? this.userId,
      otp: otp ?? this.otp,
    );
  }

  Map<String, dynamic> toMap() {
    return <String, dynamic>{
      'user_id': userId,
      'otp': otp,
    };
  }

  factory VerifyPhoneNumberRequest.fromMap(Map<String, dynamic> map) {
    return VerifyPhoneNumberRequest(
      userId: map['user_id'] as String,
      otp: map['otp'] as String,
    );
  }

  String toJson() => json.encode(toMap());

  factory VerifyPhoneNumberRequest.fromJson(String source) =>
      VerifyPhoneNumberRequest.fromMap(
          json.decode(source) as Map<String, dynamic>);

  @override
  String toString() => 'VerifyPhoneNumberRequest(userId: $userId, otp: $otp)';

  @override
  bool operator ==(covariant VerifyPhoneNumberRequest other) {
    if (identical(this, other)) return true;

    return other.userId == userId && other.otp == otp;
  }

  @override
  int get hashCode => userId.hashCode ^ otp.hashCode;
}
