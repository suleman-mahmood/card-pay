// ignore_for_file: public_member_api_docs, sort_constructors_first
import 'dart:convert';

class VerifyClosedLoopResponse {
  final String message;

  const VerifyClosedLoopResponse({required this.message});

  VerifyClosedLoopResponse copyWith({
    bool? success,
    String? message,
  }) {
    return VerifyClosedLoopResponse(message: message ?? this.message);
  }

  Map<String, dynamic> toMap() {
    return <String, dynamic>{'message': message};
  }

  factory VerifyClosedLoopResponse.fromMap(Map<String, dynamic> map) {
    return VerifyClosedLoopResponse(message: map['message'] as String);
  }

  String toJson() => json.encode(toMap());

  factory VerifyClosedLoopResponse.fromJson(String source) =>
      VerifyClosedLoopResponse.fromMap(
          json.decode(source) as Map<String, dynamic>);

  @override
  String toString() => 'VerifyClosedLoopResponse(message: $message)';

  @override
  bool operator ==(covariant VerifyClosedLoopResponse other) {
    if (identical(this, other)) return true;

    return other.message == message;
  }

  @override
  int get hashCode => message.hashCode;
}
