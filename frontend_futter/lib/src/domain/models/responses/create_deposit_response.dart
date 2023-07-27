// ignore_for_file: public_member_api_docs, sort_constructors_first
import 'dart:convert';

class CreateDepositResponse {
  final String message;
  final bool success;
  final String checkoutUrl;

  const CreateDepositResponse({
    required this.message,
    required this.success,
    required this.checkoutUrl,
  });

  CreateDepositResponse copyWith({
    String? message,
    bool? success,
    String? checkoutUrl,
  }) {
    return CreateDepositResponse(
      message: message ?? this.message,
      success: success ?? this.success,
      checkoutUrl: checkoutUrl ?? this.checkoutUrl,
    );
  }

  Map<String, dynamic> toMap() {
    return <String, dynamic>{
      'message': message,
      'success': success,
      'checkout_url': checkoutUrl,
    };
  }

  factory CreateDepositResponse.fromMap(Map<String, dynamic> map) {
    return CreateDepositResponse(
      message: map['message'] as String,
      success: map['success'] as bool,
      checkoutUrl: map['checkout_url'] as String,
    );
  }

  String toJson() => json.encode(toMap());

  factory CreateDepositResponse.fromJson(String source) =>
      CreateDepositResponse.fromMap(
          json.decode(source) as Map<String, dynamic>);

  @override
  String toString() =>
      'CreateDepositResponse(message: $message, success: $success, checkoutUrl: $checkoutUrl)';

  @override
  bool operator ==(covariant CreateDepositResponse other) {
    if (identical(this, other)) return true;

    return other.message == message &&
        other.success == success &&
        other.checkoutUrl == checkoutUrl;
  }

  @override
  int get hashCode =>
      message.hashCode ^ success.hashCode ^ checkoutUrl.hashCode;
}
