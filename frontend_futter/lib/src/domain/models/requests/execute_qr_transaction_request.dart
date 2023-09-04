// ignore_for_file: public_member_api_docs, sort_constructors_first
import 'dart:convert';

class ExecuteQrTransactionRequest {
  final String qrId;
  final int amount;

  const ExecuteQrTransactionRequest({
    required this.qrId,
    required this.amount,
  });

  ExecuteQrTransactionRequest copyWith({
    String? qrId,
    int? amount,
  }) {
    return ExecuteQrTransactionRequest(
      qrId: qrId ?? this.qrId,
      amount: amount ?? this.amount,
    );
  }

  Map<String, dynamic> toMap() {
    return <String, dynamic>{
      'qr_id': qrId,
      'amount': amount,
    };
  }

  factory ExecuteQrTransactionRequest.fromMap(Map<String, dynamic> map) {
    return ExecuteQrTransactionRequest(
      qrId: map['qr_id'] as String,
      amount: map['amount'] as int,
    );
  }

  String toJson() => json.encode(toMap());

  factory ExecuteQrTransactionRequest.fromJson(String source) =>
      ExecuteQrTransactionRequest.fromMap(
          json.decode(source) as Map<String, dynamic>);

  @override
  String toString() =>
      'ExecuteQrTransactionRequest(qrId: $qrId, amount: $amount)';

  @override
  bool operator ==(covariant ExecuteQrTransactionRequest other) {
    if (identical(this, other)) return true;

    return other.qrId == qrId && other.amount == amount;
  }

  @override
  int get hashCode => qrId.hashCode ^ amount.hashCode;
}
