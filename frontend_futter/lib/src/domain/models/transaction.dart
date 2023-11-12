// ignore_for_file: public_member_api_docs, sort_constructors_first
import 'dart:convert';
import 'package:floor/floor.dart';
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
  RECONCILIATION,
  EVENT_REGISTRATION_FEE,
}

@Entity(tableName: "transactions")
class Transaction {
  @PrimaryKey()
  String id;
  int amount;
  TransactionMode mode;
  TransactionType transactionType;
  TransactionStatus status;
  DateTime? createdAt;
  DateTime? lastUpdated;
  String senderName;
  String recipientName;

  Transaction({
    DateTime? createdAt,
    DateTime? lastUpdated,
    this.id = '',
    this.amount = 0,
    this.mode = TransactionMode.APP_TRANSFER,
    this.transactionType = TransactionType.P2P_PUSH,
    this.status = TransactionStatus.PENDING,
    this.senderName = '',
    this.recipientName = '',
  })  : createdAt = createdAt ?? DateTime(9999, 12, 31, 23, 59, 59, 999, 999),
        lastUpdated =
            lastUpdated ?? DateTime(9999, 12, 31, 23, 59, 59, 999, 999);

  Transaction copyWith({
    String? id,
    int? amount,
    TransactionMode? mode,
    TransactionType? transactionType,
    TransactionStatus? status,
    DateTime? createdAt,
    DateTime? lastUpdated,
    String? senderName,
    String? recipientName,
  }) {
    return Transaction(
      id: id ?? this.id,
      amount: amount ?? this.amount,
      mode: mode ?? this.mode,
      transactionType: transactionType ?? this.transactionType,
      status: status ?? this.status,
      createdAt: createdAt ?? this.createdAt,
      lastUpdated: lastUpdated ?? this.lastUpdated,
      senderName: senderName ?? this.senderName,
      recipientName: recipientName ?? this.recipientName,
    );
  }

  Map<String, dynamic> toMap() {
    return <String, dynamic>{
      'id': id,
      'amount': amount,
      'mode': mode.name,
      'transaction_type': transactionType.name,
      'status': status.name,
      'created_at': createdAt?.millisecondsSinceEpoch,
      'last_updated': lastUpdated?.millisecondsSinceEpoch,
      'sender_name': senderName,
      'recipient_name': recipientName,
    };
  }

  factory Transaction.fromMap(Map<String, dynamic> map) {
    return Transaction(
      id: map['id'] as String,
      amount: map['amount'] as int,
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
      senderName: map['sender_name'] as String,
      recipientName: map['recipient_name'] as String,
    );
  }

  String toJson() => json.encode(toMap());

  factory Transaction.fromJson(String source) =>
      Transaction.fromMap(json.decode(source) as Map<String, dynamic>);

  @override
  String toString() {
    return 'Transaction(id: $id, amount: $amount, mode: $mode, transactionType: $transactionType, status: $status, createdAt: $createdAt, lastUpdated: $lastUpdated, senderName: $senderName, recipientName: $recipientName)';
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
        other.senderName == senderName &&
        other.recipientName == recipientName;
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
        senderName.hashCode ^
        recipientName.hashCode;
  }
}
