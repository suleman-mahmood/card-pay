// ignore_for_file: public_member_api_docs, sort_constructors_first
import 'dart:convert';

class ExecuteP2PPushTransactionResponse {
  final bool success;
  final String message;

  const ExecuteP2PPushTransactionResponse({
    required this.success,
    required this.message,
  });

  ExecuteP2PPushTransactionResponse copyWith({
    bool? success,
    String? message,
  }) {
    return ExecuteP2PPushTransactionResponse(
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

  factory ExecuteP2PPushTransactionResponse.fromMap(Map<String, dynamic> map) {
    return ExecuteP2PPushTransactionResponse(
      success: map['success'] as bool,
      message: map['message'] as String,
    );
  }

  String toJson() => json.encode(toMap());

  factory ExecuteP2PPushTransactionResponse.fromJson(String source) =>
      ExecuteP2PPushTransactionResponse.fromMap(
          json.decode(source) as Map<String, dynamic>);

  @override
  String toString() =>
      'ExecuteP2PPushTransactionResponse(success: $success, message: $message)';

  @override
  bool operator ==(covariant ExecuteP2PPushTransactionResponse other) {
    if (identical(this, other)) return true;

    return other.success == success && other.message == message;
  }

  @override
  int get hashCode => success.hashCode ^ message.hashCode;
}
