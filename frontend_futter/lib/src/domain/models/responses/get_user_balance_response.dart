// ignore_for_file: public_member_api_docs, sort_constructors_first
import 'dart:convert';

class GetUserBalanceResponse {
  final String message;
  final int balance;

  const GetUserBalanceResponse({
    required this.message,
    required this.balance,
  });

  GetUserBalanceResponse copyWith({
    bool? success,
    String? message,
    int? balance,
  }) {
    return GetUserBalanceResponse(
      message: message ?? this.message,
      balance: balance ?? this.balance,
    );
  }

  Map<String, dynamic> toMap() {
    return <String, dynamic>{
      'message': message,
      'balance': balance,
    };
  }

  factory GetUserBalanceResponse.fromMap(Map<String, dynamic> map) {
    return GetUserBalanceResponse(
      message: map['message'] as String,
      balance: map['balance'] as int,
    );
  }

  String toJson() => json.encode(toMap());

  factory GetUserBalanceResponse.fromJson(String source) =>
      GetUserBalanceResponse.fromMap(
          json.decode(source) as Map<String, dynamic>);

  @override
  String toString() =>
      'GetUserBalanceResponse(message: $message, balance: $balance)';

  @override
  bool operator ==(covariant GetUserBalanceResponse other) {
    if (identical(this, other)) return true;

    return other.message == message && other.balance == balance;
  }

  @override
  int get hashCode => message.hashCode ^ balance.hashCode;
}
