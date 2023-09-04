// ignore_for_file: public_member_api_docs, sort_constructors_first
import 'dart:convert';

class ExecuteQrTransactionResponse {
  final String message;

  const ExecuteQrTransactionResponse({
    required this.message,
  });

  ExecuteQrTransactionResponse copyWith({
    String? message,
  }) {
    return ExecuteQrTransactionResponse(
      message: message ?? this.message,
    );
  }

  Map<String, dynamic> toMap() {
    return <String, dynamic>{
      'message': message,
    };
  }

  factory ExecuteQrTransactionResponse.fromMap(Map<String, dynamic> map) {
    return ExecuteQrTransactionResponse(
      message: map['message'] as String,
    );
  }

  String toJson() => json.encode(toMap());

  factory ExecuteQrTransactionResponse.fromJson(String source) =>
      ExecuteQrTransactionResponse.fromMap(
          json.decode(source) as Map<String, dynamic>);

  @override
  String toString() => 'ExecuteQrTransactionResponse(message: $message)';

  @override
  bool operator ==(covariant ExecuteQrTransactionResponse other) {
    if (identical(this, other)) return true;

    return other.message == message;
  }

  @override
  int get hashCode => message.hashCode;
}
