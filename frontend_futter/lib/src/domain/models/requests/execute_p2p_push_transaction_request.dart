// ignore_for_file: public_member_api_docs, sort_constructors_first
import 'dart:convert';

class ExecuteP2PPushTransactionRequest {
  final String recipientUniqueIdentifier;
  final double amount;

  const ExecuteP2PPushTransactionRequest({
    required this.recipientUniqueIdentifier,
    required this.amount,
  });

  ExecuteP2PPushTransactionRequest copyWith({
    String? recipientUniqueIdentifier,
    double? amount,
  }) {
    return ExecuteP2PPushTransactionRequest(
      recipientUniqueIdentifier:
          recipientUniqueIdentifier ?? this.recipientUniqueIdentifier,
      amount: amount ?? this.amount,
    );
  }

  Map<String, dynamic> toMap() {
    return <String, dynamic>{
      'recipient_unique_identifier': recipientUniqueIdentifier,
      'amount': amount,
    };
  }

  factory ExecuteP2PPushTransactionRequest.fromMap(Map<String, dynamic> map) {
    return ExecuteP2PPushTransactionRequest(
      recipientUniqueIdentifier: map['recipient_unique_identifier'] as String,
      amount: map['amount'] as double,
    );
  }

  String toJson() => json.encode(toMap());

  factory ExecuteP2PPushTransactionRequest.fromJson(String source) =>
      ExecuteP2PPushTransactionRequest.fromMap(
          json.decode(source) as Map<String, dynamic>);

  @override
  String toString() =>
      'ExecuteP2PPushTransactionRequest(recipientUniqueIdentifier: $recipientUniqueIdentifier, amount: $amount)';

  @override
  bool operator ==(covariant ExecuteP2PPushTransactionRequest other) {
    if (identical(this, other)) return true;

    return other.recipientUniqueIdentifier == recipientUniqueIdentifier &&
        other.amount == amount;
  }

  @override
  int get hashCode => recipientUniqueIdentifier.hashCode ^ amount.hashCode;
}
