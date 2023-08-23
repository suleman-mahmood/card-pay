// ignore_for_file: public_member_api_docs, sort_constructors_first
import 'dart:convert';

class RegisterClosedLoopResponse {
  final String message;

  const RegisterClosedLoopResponse({required this.message});

  RegisterClosedLoopResponse copyWith({String? message}) {
    return RegisterClosedLoopResponse(message: message ?? this.message);
  }

  Map<String, dynamic> toMap() {
    return <String, dynamic>{'message': message};
  }

  factory RegisterClosedLoopResponse.fromMap(Map<String, dynamic> map) {
    return RegisterClosedLoopResponse(message: map['message'] as String);
  }

  String toJson() => json.encode(toMap());

  factory RegisterClosedLoopResponse.fromJson(String source) =>
      RegisterClosedLoopResponse.fromMap(
          json.decode(source) as Map<String, dynamic>);

  @override
  String toString() => 'RegisterClosedLoopResponse(message: $message)';

  @override
  bool operator ==(covariant RegisterClosedLoopResponse other) {
    if (identical(this, other)) return true;

    return other.message == message;
  }

  @override
  int get hashCode => message.hashCode;
}
