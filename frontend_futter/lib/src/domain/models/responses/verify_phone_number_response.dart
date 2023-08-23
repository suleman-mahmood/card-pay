// ignore_for_file: public_member_api_docs, sort_constructors_first
import 'dart:convert';

class VerifyPhoneNumberResponse {
  final String message;

  VerifyPhoneNumberResponse({required this.message});

  VerifyPhoneNumberResponse copyWith({
    bool? success,
    String? message,
  }) {
    return VerifyPhoneNumberResponse(message: message ?? this.message);
  }

  Map<String, dynamic> toMap() {
    return <String, dynamic>{'message': message};
  }

  factory VerifyPhoneNumberResponse.fromMap(Map<String, dynamic> map) {
    return VerifyPhoneNumberResponse(message: map['message'] as String);
  }

  String toJson() => json.encode(toMap());

  factory VerifyPhoneNumberResponse.fromJson(String source) =>
      VerifyPhoneNumberResponse.fromMap(
          json.decode(source) as Map<String, dynamic>);

  @override
  String toString() => 'VerifyPhoneNumberResponse(message: $message)';

  @override
  bool operator ==(covariant VerifyPhoneNumberResponse other) {
    if (identical(this, other)) return true;

    return other.message == message;
  }

  @override
  int get hashCode => message.hashCode;
}
