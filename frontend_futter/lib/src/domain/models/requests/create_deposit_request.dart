// ignore_for_file: public_member_api_docs, sort_constructors_first
import 'dart:convert';

class CreateDepositRequest {
  final int amount;

  const CreateDepositRequest({required this.amount});

  CreateDepositRequest copyWith({int? amount}) {
    return CreateDepositRequest(amount: amount ?? this.amount);
  }

  Map<String, dynamic> toMap() {
    return <String, dynamic>{'amount': amount};
  }

  String toJson() => json.encode(toMap());

  @override
  String toString() => 'CreateDepositRequest(amount: $amount)';

  @override
  bool operator ==(covariant CreateDepositRequest other) {
    if (identical(this, other)) return true;

    return other.amount == amount;
  }

  @override
  int get hashCode => amount.hashCode;
}
