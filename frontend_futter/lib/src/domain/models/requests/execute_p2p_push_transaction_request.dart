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
    String? closedLoopId,
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

  String toJson() => json.encode(toMap());

  @override
  String toString() =>
      'ExecuteP2PPushTransactionRequest(recipientUniqueIdentifier: $recipientUniqueIdentifier, amount: $amount, closedLoopId: $closedLoopId)';

  @override
  bool operator ==(covariant ExecuteP2PPushTransactionRequest other) {
    if (identical(this, other)) return true;

    return other.recipientUniqueIdentifier == recipientUniqueIdentifier &&
        other.amount == amount &&
        other.closedLoopId == closedLoopId;
  }

  @override
  int get hashCode =>
      recipientUniqueIdentifier.hashCode ^
      amount.hashCode ^
      closedLoopId.hashCode;
}
