// ignore_for_file: public_member_api_docs, sort_constructors_first
import 'dart:convert';

class DeclineP2PPullTransactionRequest {
  final String transactionId;

  const DeclineP2PPullTransactionRequest({
    required this.transactionId,
  });

  DeclineP2PPullTransactionRequest copyWith({
    String? transactionId,
  }) {
    return DeclineP2PPullTransactionRequest(
      transactionId: transactionId ?? this.transactionId,
    );
  }

  Map<String, dynamic> toMap() {
    return <String, dynamic>{
      'transaction_id': transactionId,
    };
  }

  String toJson() => json.encode(toMap());

  @override
  String toString() =>
      'DeclineP2PPullTransactionRequest(transactionId: $transactionId)';

  @override
  bool operator ==(covariant DeclineP2PPullTransactionRequest other) {
    if (identical(this, other)) return true;

    return other.transactionId == transactionId;
  }

  @override
  int get hashCode => transactionId.hashCode;
}
