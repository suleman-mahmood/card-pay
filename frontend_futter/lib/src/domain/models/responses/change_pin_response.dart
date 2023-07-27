// ignore_for_file: public_member_api_docs, sort_constructors_first
import 'dart:convert';

class ChangePinResponse {
  final bool success;
  final String message;

  const ChangePinResponse({
    required this.success,
    required this.message,
  });

  ChangePinResponse copyWith({
    bool? success,
    String? message,
  }) {
    return ChangePinResponse(
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

  factory ChangePinResponse.fromMap(Map<String, dynamic> map) {
    return ChangePinResponse(
      success: map['success'] as bool,
      message: map['message'] as String,
    );
  }

  String toJson() => json.encode(toMap());

  factory ChangePinResponse.fromJson(String source) =>
      ChangePinResponse.fromMap(json.decode(source) as Map<String, dynamic>);

  @override
  String toString() =>
      'ChangePinResponse(success: $success, message: $message)';

  @override
  bool operator ==(covariant ChangePinResponse other) {
    if (identical(this, other)) return true;

    return other.success == success && other.message == message;
  }

  @override
  int get hashCode => success.hashCode ^ message.hashCode;
}
