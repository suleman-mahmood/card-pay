// ignore_for_file: public_member_api_docs, sort_constructors_first
import 'dart:convert';

class AcceptP2PPullTransactionRequest {
  final String transactionId;

  const AcceptP2PPullTransactionRequest({
    required this.transactionId,
  });

  AcceptP2PPullTransactionRequest copyWith({
    String? transactionId,
  }) {
    return AcceptP2PPullTransactionRequest(
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
      'AcceptP2PPullTransactionRequest(transactionId: $transactionId)';

  @override
  bool operator ==(covariant AcceptP2PPullTransactionRequest other) {
    if (identical(this, other)) return true;

    return other.transactionId == transactionId;
  }

  @override
  int get hashCode => transactionId.hashCode;
}
