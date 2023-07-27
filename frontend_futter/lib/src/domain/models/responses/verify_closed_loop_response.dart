// ignore_for_file: public_member_api_docs, sort_constructors_first
import 'dart:convert';

class VerifyClosedLoopResponse {
  final bool success;
  final String message;

  const VerifyClosedLoopResponse({
    required this.success,
    required this.message,
  });

  VerifyClosedLoopResponse copyWith({
    bool? success,
    String? message,
  }) {
    return VerifyClosedLoopResponse(
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

  factory VerifyClosedLoopResponse.fromMap(Map<String, dynamic> map) {
    return VerifyClosedLoopResponse(
      success: map['success'] as bool,
      message: map['message'] as String,
    );
  }

  String toJson() => json.encode(toMap());

  factory VerifyClosedLoopResponse.fromJson(String source) =>
      VerifyClosedLoopResponse.fromMap(
          json.decode(source) as Map<String, dynamic>);

  @override
  String toString() =>
      'VerifyClosedLoopResponse(success: $success, message: $message)';

  @override
  bool operator ==(covariant VerifyClosedLoopResponse other) {
    if (identical(this, other)) return true;

    return other.success == success && other.message == message;
  }

  @override
  int get hashCode => success.hashCode ^ message.hashCode;
}
