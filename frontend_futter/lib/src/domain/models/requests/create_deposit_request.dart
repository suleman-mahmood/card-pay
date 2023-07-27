// ignore_for_file: public_member_api_docs, sort_constructors_first
import 'dart:convert';

class CreateDepositRequest {
  final String userId;
  final double amount;

  const CreateDepositRequest({
    required this.userId,
    required this.amount,
  });

  CreateDepositRequest copyWith({
    String? userId,
    double? amount,
  }) {
    return CreateDepositRequest(
      userId: userId ?? this.userId,
      amount: amount ?? this.amount,
    );
  }

  Map<String, dynamic> toMap() {
    return <String, dynamic>{
      'user_id': userId,
      'amount': amount,
    };
  }

  factory CreateDepositRequest.fromMap(Map<String, dynamic> map) {
    return CreateDepositRequest(
      userId: map['user_id'] as String,
      amount: map['amount'] as double,
    );
  }

  String toJson() => json.encode(toMap());

  factory CreateDepositRequest.fromJson(String source) =>
      CreateDepositRequest.fromMap(json.decode(source) as Map<String, dynamic>);

  @override
  String toString() => 'CreateDepositRequest(userId: $userId, amount: $amount)';

  @override
  bool operator ==(covariant CreateDepositRequest other) {
    if (identical(this, other)) return true;

    return other.userId == userId && other.amount == amount;
  }

  @override
  int get hashCode => userId.hashCode ^ amount.hashCode;
}
