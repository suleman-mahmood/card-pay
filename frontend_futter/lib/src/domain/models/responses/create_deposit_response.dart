// ignore_for_file: public_member_api_docs, sort_constructors_first
import 'dart:convert';

class CreateDepositResponse {
  final String message;
  final String checkoutUrl;

  const CreateDepositResponse({
    required this.message,
    required this.checkoutUrl,
  });

  CreateDepositResponse copyWith({
    String? message,
    bool? success,
    String? checkoutUrl,
  }) {
    return CreateDepositResponse(
      message: message ?? this.message,
      checkoutUrl: checkoutUrl ?? this.checkoutUrl,
    );
  }

  Map<String, dynamic> toMap() {
    return <String, dynamic>{
      'message': message,
      'checkout_url': checkoutUrl,
    };
  }

  factory CreateDepositResponse.fromMap(Map<String, dynamic> map) {
    return CreateDepositResponse(
      message: map['message'] as String,
      checkoutUrl: map['checkout_url'] as String,
    );
  }

  String toJson() => json.encode(toMap());

  factory CreateDepositResponse.fromJson(String source) =>
      CreateDepositResponse.fromMap(
          json.decode(source) as Map<String, dynamic>);

  @override
  String toString() =>
      'CreateDepositResponse(message: $message, checkoutUrl: $checkoutUrl)';

  @override
  bool operator ==(covariant CreateDepositResponse other) {
    if (identical(this, other)) return true;

    return other.message == message && other.checkoutUrl == checkoutUrl;
  }

  @override
  int get hashCode => message.hashCode ^ checkoutUrl.hashCode;
}
