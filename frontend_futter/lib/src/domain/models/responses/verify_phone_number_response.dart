// ignore_for_file: public_member_api_docs, sort_constructors_first
import 'dart:convert';

import 'package:cardpay/src/utils/constants/event_codes.dart';

class VerifyPhoneNumberResponse {
  final bool success;
  final String message;

  VerifyPhoneNumberResponse({
    required this.success,
    required this.message,
  });

  VerifyPhoneNumberResponse copyWith({
    bool? success,
    String? message,
  }) {
    return VerifyPhoneNumberResponse(
      success: success ?? this.success,
      message: message ?? this.message,
    );
  }

  Map<String, dynamic> toMap() {
    return <String, dynamic>{
      'success': success,
      'message': message,
    };
  }

  factory VerifyPhoneNumberResponse.fromMap(Map<String, dynamic> map) {
    return VerifyPhoneNumberResponse(
      success: map['success'] as bool,
      message: map['message'] as String,
    );
  }

  String toJson() => json.encode(toMap());

  factory VerifyPhoneNumberResponse.fromJson(String source) =>
      VerifyPhoneNumberResponse.fromMap(
          json.decode(source) as Map<String, dynamic>);

  @override
  String toString() =>
      'VerifyPhoneNumberResponse(success: $success, message: $message)';

  @override
  bool operator ==(covariant VerifyPhoneNumberResponse other) {
    if (identical(this, other)) return true;

    return other.success == success && other.message == message;
  }

  @override
  int get hashCode => success.hashCode ^ message.hashCode;
}
