// ignore_for_file: public_member_api_docs, sort_constructors_first
import 'dart:convert';

class SetFcmTokenResponse {
  final String message;

  const SetFcmTokenResponse({
    required this.message,
  });

  SetFcmTokenResponse copyWith({
    String? message,
  }) {
    return SetFcmTokenResponse(
      message: message ?? this.message,
    );
  }

  Map<String, dynamic> toMap() {
    return <String, dynamic>{
      'message': message,
    };
  }

  factory SetFcmTokenResponse.fromMap(Map<String, dynamic> map) {
    return SetFcmTokenResponse(
      message: map['message'] as String,
    );
  }

  String toJson() => json.encode(toMap());

  factory SetFcmTokenResponse.fromJson(String source) =>
      SetFcmTokenResponse.fromMap(json.decode(source) as Map<String, dynamic>);

  @override
  String toString() => 'SetFcmTokenResponse(message: $message)';

  @override
  bool operator ==(covariant SetFcmTokenResponse other) {
    if (identical(this, other)) return true;

    return other.message == message;
  }

  @override
  int get hashCode => message.hashCode;
}
