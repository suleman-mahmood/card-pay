// ignore_for_file: public_member_api_docs, sort_constructors_first
import 'dart:convert';

class RegisterEventResponse {
  final String message;

  const RegisterEventResponse({
    required this.message,
  });

  RegisterEventResponse copyWith({
    String? message,
  }) {
    return RegisterEventResponse(
      message: message ?? this.message,
    );
  }

  Map<String, dynamic> toMap() {
    return <String, dynamic>{
      'message': message,
    };
  }

  factory RegisterEventResponse.fromMap(Map<String, dynamic> map) {
    return RegisterEventResponse(
      message: map['message'] as String,
    );
  }

  String toJson() => json.encode(toMap());

  factory RegisterEventResponse.fromJson(String source) =>
      RegisterEventResponse.fromMap(
          json.decode(source) as Map<String, dynamic>);

  @override
  String toString() => 'RegisterEventResponse(message: $message)';

  @override
  bool operator ==(covariant RegisterEventResponse other) {
    if (identical(this, other)) return true;

    return other.message == message;
  }

  @override
  int get hashCode => message.hashCode;
}
