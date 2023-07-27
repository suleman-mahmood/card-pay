// ignore_for_file: public_member_api_docs, sort_constructors_first
import 'dart:convert';
import 'package:intl/intl.dart';

enum TransactionStatus {
  PENDING,
  FAILED,
  SUCCESSFUL,
  EXPIRED,
  DECLINED,
}

enum TransactionMode {
  QR,
  RFID,
  NFC,
  BARCODE,
  APP_TRANSFER,
}

enum TransactionType {
  POS,
  P2P_PUSH,
  P2P_PULL,
  VOUCHER,
  VIRTUAL_POS,
  PAYMENT_GATEWAY,
  CARD_PAY,
  CASH_BACK,
  REFERRAL,
}

class Transaction {
  final String id;
  final double amount;
  final TransactionMode mode;
  final TransactionType transactionType;
  final TransactionStatus status;
  final DateTime createdAt;
  final DateTime lastUpdated;
  final String senderWalletId;
  final String recipientWalletId;

  const Transaction({
    required this.id,
    required this.amount,
    required this.mode,
    required this.transactionType,
    required this.status,
    required this.createdAt,
    required this.lastUpdated,
    required this.senderWalletId,
    required this.recipientWalletId,
  });

  Transaction copyWith({
    String? id,
    double? amount,
    TransactionMode? mode,
    TransactionType? transactionType,
    TransactionStatus? status,
    DateTime? createdAt,
    DateTime? lastUpdated,
    String? senderWalletId,
    String? recipientWalletId,
  }) {
    return Transaction(
      id: id ?? this.id,
      amount: amount ?? this.amount,
      mode: mode ?? this.mode,
      transactionType: transactionType ?? this.transactionType,
      status: status ?? this.status,
      createdAt: createdAt ?? this.createdAt,
      lastUpdated: lastUpdated ?? this.lastUpdated,
      senderWalletId: senderWalletId ?? this.senderWalletId,
      recipientWalletId: recipientWalletId ?? this.recipientWalletId,
    );
  }

  Map<String, dynamic> toMap() {
    return <String, dynamic>{
      'id': id,
      'amount': amount,
      'mode': mode.name,
      'transaction_type': transactionType.name,
      'status': status.name,
      'created_at': createdAt.millisecondsSinceEpoch,
      'last_updated': lastUpdated.millisecondsSinceEpoch,
      'sender_wallet_id': senderWalletId,
      'recipient_wallet_id': recipientWalletId,
    };
  }

  factory Transaction.fromMap(Map<String, dynamic> map) {
    return Transaction(
      id: map['id'] as String,
      amount: map['amount'] as double,
      mode: TransactionMode.values.firstWhere(
        (e) => e.name == map['mode'],
      ),
      transactionType: TransactionType.values.firstWhere(
        (e) => e.name == map['transaction_type'],
      ),
      status: TransactionStatus.values.firstWhere(
        (e) => e.name == map['status'],
      ),
      createdAt: DateFormat("EEE, dd MMM yyyy HH:mm:ss 'GMT'")
          .parse(map['created_at']),
      lastUpdated: DateFormat("EEE, dd MMM yyyy HH:mm:ss 'GMT'")
          .parse(map['last_updated']),
      senderWalletId: map['sender_wallet_id'] as String,
      recipientWalletId: map['recipient_wallet_id'] as String,
    );
  }

  String toJson() => json.encode(toMap());

  factory Transaction.fromJson(String source) =>
      Transaction.fromMap(json.decode(source) as Map<String, dynamic>);

  @override
  String toString() {
    return 'Transaction(id: $id, amount: $amount, mode: $mode, transactionType: $transactionType, status: $status, createdAt: $createdAt, lastUpdated: $lastUpdated, senderWalletId: $senderWalletId, recipientWalletId: $recipientWalletId)';
  }

  @override
  bool operator ==(covariant Transaction other) {
    if (identical(this, other)) return true;

    return other.id == id &&
        other.amount == amount &&
        other.mode == mode &&
        other.transactionType == transactionType &&
        other.status == status &&
        other.createdAt == createdAt &&
        other.lastUpdated == lastUpdated &&
        other.senderWalletId == senderWalletId &&
        other.recipientWalletId == recipientWalletId;
  }

  @override
  int get hashCode {
    return id.hashCode ^
        amount.hashCode ^
        mode.hashCode ^
        transactionType.hashCode ^
        status.hashCode ^
        createdAt.hashCode ^
        lastUpdated.hashCode ^
        senderWalletId.hashCode ^
        recipientWalletId.hashCode;
  }
}
