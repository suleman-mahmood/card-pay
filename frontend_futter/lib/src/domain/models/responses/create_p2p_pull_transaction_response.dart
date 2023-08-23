// ignore_for_file: public_member_api_docs, sort_constructors_first
import 'dart:convert';

class CreateP2PPullTransactionResponse {
  final String message;

  const CreateP2PPullTransactionResponse({
    required this.message,
  });

  CreateP2PPullTransactionResponse copyWith({
    String? message,
    bool? success,
  }) {
    return CreateP2PPullTransactionResponse(
      message: message ?? this.message,
    );
  }

  Map<String, dynamic> toMap() {
    return <String, dynamic>{
      'message': message,
    };
  }

  factory CreateP2PPullTransactionResponse.fromMap(Map<String, dynamic> map) {
    return CreateP2PPullTransactionResponse(
      message: map['message'] as String,
    );
  }

  String toJson() => json.encode(toMap());

  factory CreateP2PPullTransactionResponse.fromJson(String source) =>
      CreateP2PPullTransactionResponse.fromMap(
          json.decode(source) as Map<String, dynamic>);

  @override
  String toString() => 'CreateP2PPullTransactionResponse(message: $message)';

  @override
  bool operator ==(covariant CreateP2PPullTransactionResponse other) {
    if (identical(this, other)) return true;

    return other.message == message;
  }

  @override
  int get hashCode => message.hashCode;
}
