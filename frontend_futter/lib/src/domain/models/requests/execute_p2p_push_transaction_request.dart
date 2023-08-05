// ignore_for_file: public_member_api_docs, sort_constructors_first
import 'dart:convert';

class ExecuteP2PPushTransactionRequest {
  final String recipientUniqueIdentifier;
  final double amount;
  final String closedLoopId;

  const ExecuteP2PPushTransactionRequest({
    required this.recipientUniqueIdentifier,
    required this.amount,
    required this.closedLoopId,
  });

  ExecuteP2PPushTransactionRequest copyWith({
    String? recipientUniqueIdentifier,
    double? amount,
    String? closed_loop_id,
  }) {
    return ExecuteP2PPushTransactionRequest(
      recipientUniqueIdentifier:
          recipientUniqueIdentifier ?? this.recipientUniqueIdentifier,
      amount: amount ?? this.amount,
      closedLoopId: closedLoopId ?? this.closedLoopId,
    );
  }

  Map<String, dynamic> toMap() {
    return <String, dynamic>{
      'recipient_unique_identifier': recipientUniqueIdentifier,
      'amount': amount,
      'closed_loop_id': closedLoopId,
    };
  }

  factory ExecuteP2PPushTransactionRequest.fromMap(Map<String, dynamic> map) {
    return ExecuteP2PPushTransactionRequest(
      recipientUniqueIdentifier: map['recipient_unique_identifier'] as String,
      amount: map['amount'] as double,
      closedLoopId: map['closed_loop_id'] as String,
    );
  }

  String toJson() => json.encode(toMap());

  factory ExecuteP2PPushTransactionRequest.fromJson(String source) =>
      ExecuteP2PPushTransactionRequest.fromMap(
          json.decode(source) as Map<String, dynamic>);

  @override
  String toString() =>
      'ExecuteP2PPushTransactionRequest(recipientUniqueIdentifier: $recipientUniqueIdentifier, amount: $amount, closedLoopId: $closedLoopId)';

  @override
  bool operator ==(covariant ExecuteP2PPushTransactionRequest other) {
    if (identical(this, other)) return true;

    return other.recipientUniqueIdentifier == recipientUniqueIdentifier &&
        other.amount == amount && other.closedLoopId == closedLoopId;
  }

  @override
  int get hashCode => recipientUniqueIdentifier.hashCode ^ amount.hashCode ^ closedLoopId.hashCode;
}
