// ignore_for_file: public_member_api_docs, sort_constructors_first
import 'dart:convert';

class CommonResponse {
  final String message;

  const CommonResponse({
    required this.message,
  });

  CommonResponse copyWith({
    String? message,
  }) {
    return CommonResponse(
      message: message ?? this.message,
    );
  }

  factory CommonResponse.fromMap(Map<String, dynamic> map) {
    return CommonResponse(
      message: map['message'] as String,
    );
  }

  factory CommonResponse.fromJson(String source) =>
      CommonResponse.fromMap(json.decode(source) as Map<String, dynamic>);

  @override
  String toString() => 'CommonResponse(message: $message)';

  @override
  bool operator ==(covariant CommonResponse other) {
    if (identical(this, other)) return true;

    return other.message == message;
  }

  @override
  int get hashCode => message.hashCode;
}
