// ignore_for_file: public_member_api_docs, sort_constructors_first
import 'dart:convert';

class CreateP2PPullTransactionRequest {
  final String senderUniqueIdentifier;
  final double amount;
  final String closedLoopId;

  const CreateP2PPullTransactionRequest({
    required this.senderUniqueIdentifier,
    required this.amount,
    required this.closedLoopId,
  });

  CreateP2PPullTransactionRequest copyWith({
    String? senderUniqueIdentifier,
    double? amount,
    String? closedLoopId,
  }) {
    return CreateP2PPullTransactionRequest(
      senderUniqueIdentifier:
          senderUniqueIdentifier ?? this.senderUniqueIdentifier,
      amount: amount ?? this.amount,
      closedLoopId: closedLoopId ?? this.closedLoopId,
    );
  }

  Map<String, dynamic> toMap() {
    return <String, dynamic>{
      'sender_unique_identifier': senderUniqueIdentifier,
      'amount': amount,
      'closed_loop_id': closedLoopId,
    };
  }

  String toJson() => json.encode(toMap());

  @override
  String toString() =>
      'CreateP2PPullTransactionRequest(senderUniqueIdentifier: $senderUniqueIdentifier, amount: $amount, closedLoopId: $closedLoopId)';

  @override
  bool operator ==(covariant CreateP2PPullTransactionRequest other) {
    if (identical(this, other)) return true;

    return other.senderUniqueIdentifier == senderUniqueIdentifier &&
        other.amount == amount &&
        other.closedLoopId == closedLoopId;
  }

  @override
  int get hashCode =>
      senderUniqueIdentifier.hashCode ^ amount.hashCode ^ closedLoopId.hashCode;
}
