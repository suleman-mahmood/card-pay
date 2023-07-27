// ignore_for_file: public_member_api_docs, sort_constructors_first
import 'dart:convert';

class RegisterClosedLoopResponse {
  final bool success;
  final String message;

  const RegisterClosedLoopResponse({
    required this.success,
    required this.message,
  });

  RegisterClosedLoopResponse copyWith({
    bool? success,
    String? message,
  }) {
    return RegisterClosedLoopResponse(
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

  factory RegisterClosedLoopResponse.fromMap(Map<String, dynamic> map) {
    return RegisterClosedLoopResponse(
      success: map['success'] as bool,
      message: map['message'] as String,
    );
  }

  String toJson() => json.encode(toMap());

  factory RegisterClosedLoopResponse.fromJson(String source) =>
      RegisterClosedLoopResponse.fromMap(
          json.decode(source) as Map<String, dynamic>);

  @override
  String toString() =>
      'RegisterClosedLoopResponse(success: $success, message: $message)';

  @override
  bool operator ==(covariant RegisterClosedLoopResponse other) {
    if (identical(this, other)) return true;

    return other.success == success && other.message == message;
  }

  @override
  int get hashCode => success.hashCode ^ message.hashCode;
}
