// ignore_for_file: public_member_api_docs, sort_constructors_first
import 'dart:convert';

class ExecuteQrTransactionRequest {
  final String qrId;
  final int amount;
  final int v;

  const ExecuteQrTransactionRequest({
    required this.qrId,
    required this.amount,
    required this.v,
  });

  ExecuteQrTransactionRequest copyWith({
    String? qrId,
    int? amount,
    int? v,
  }) {
    return ExecuteQrTransactionRequest(
      qrId: qrId ?? this.qrId,
      amount: amount ?? this.amount,
      v: v ?? this.v,
    );
  }

  Map<String, dynamic> toMap() {
    return <String, dynamic>{
      'qr_id': qrId,
      'amount': amount,
      'v': v,
    };
  }

  factory ExecuteQrTransactionRequest.fromMap(Map<String, dynamic> map) {
    return ExecuteQrTransactionRequest(
      qrId: map['qr_id'] as String,
      amount: map['amount'] as int,
      v: map['v'] as int,
    );
  }

  String toJson() => json.encode(toMap());

  factory ExecuteQrTransactionRequest.fromJson(String source) =>
      ExecuteQrTransactionRequest.fromMap(
          json.decode(source) as Map<String, dynamic>);

  @override
  String toString() =>
      'ExecuteQrTransactionRequest(qrId: $qrId, amount: $amount, v: $v)';

  @override
  bool operator ==(covariant ExecuteQrTransactionRequest other) {
    if (identical(this, other)) return true;

    return other.qrId == qrId && other.amount == amount && other.v == v;
  }

  @override
  int get hashCode => qrId.hashCode ^ amount.hashCode ^ v.hashCode;
}
