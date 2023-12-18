// ignore_for_file: public_member_api_docs, sort_constructors_first
import 'dart:convert';

import 'package:intl/intl.dart';

class P2PRequestInfo {
  String txId;
  String fullName;
  int amount;
  DateTime createdAt;

  P2PRequestInfo({
    DateTime? createdAt,
    this.txId = '',
    this.fullName = '',
    this.amount = 0,
  }) : createdAt = createdAt ?? DateTime(9999, 12, 31, 23, 59, 59, 999, 999);

  P2PRequestInfo copyWith({
    String? txId,
    String? fullName,
    int? amount,
    DateTime? createdAt,
  }) {
    return P2PRequestInfo(
      txId: txId ?? this.txId,
      fullName: fullName ?? this.fullName,
      amount: amount ?? this.amount,
      createdAt: createdAt ?? this.createdAt,
    );
  }

  Map<String, dynamic> toMap() {
    return <String, dynamic>{
      'tx_id': txId,
      'full_name': fullName,
      'amount': amount,
      'created_at': createdAt.millisecondsSinceEpoch,
    };
  }

  factory P2PRequestInfo.fromMap(Map<String, dynamic> map) {
    return P2PRequestInfo(
      txId: map['tx_id'] as String,
      fullName: map['full_name'] as String,
      amount: map['amount'] as int,
      createdAt: DateFormat("EEE, dd MMM yyyy HH:mm:ss 'GMT'")
          .parse(map['created_at']),
    );
  }

  String toJson() => json.encode(toMap());

  factory P2PRequestInfo.fromJson(String source) =>
      P2PRequestInfo.fromMap(json.decode(source) as Map<String, dynamic>);

  @override
  String toString() {
    return 'P2PRequestInfo(txId: $txId, fullName: $fullName, amount: $amount, createdAt: $createdAt)';
  }

  @override
  bool operator ==(covariant P2PRequestInfo other) {
    if (identical(this, other)) return true;

    return other.txId == txId &&
        other.fullName == fullName &&
        other.amount == amount &&
        other.createdAt == createdAt;
  }

  @override
  int get hashCode {
    return txId.hashCode ^
        fullName.hashCode ^
        amount.hashCode ^
        createdAt.hashCode;
  }
}
