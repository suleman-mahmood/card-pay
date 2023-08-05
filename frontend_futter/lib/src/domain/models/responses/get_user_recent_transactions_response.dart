// ignore_for_file: public_member_api_docs, sort_constructors_first
import 'dart:convert';

import 'package:cardpay/src/domain/models/transaction.dart';
import 'package:collection/collection.dart';
import 'package:intl/intl.dart';

class GetUserRecentTransactionsResponse {
  final bool success;
  final String message;
  final List<TransactionResponse> recentTransactions;

  const GetUserRecentTransactionsResponse({
    required this.success,
    required this.message,
    required this.recentTransactions,
  });

  GetUserRecentTransactionsResponse copyWith({
    bool? success,
    String? message,
    List<TransactionResponse>? recentTransactions,
  }) {
    return GetUserRecentTransactionsResponse(
      success: success ?? this.success,
      message: message ?? this.message,
      recentTransactions: recentTransactions ?? this.recentTransactions,
    );
  }

  Map<String, dynamic> toMap() {
    return <String, dynamic>{
      'success': success,
      'message': message,
      'recent_transactions': recentTransactions.map((x) => x.toMap()).toList(),
    };
  }

  factory GetUserRecentTransactionsResponse.fromMap(Map<String, dynamic> map) {
    return GetUserRecentTransactionsResponse(
      success: map['success'] as bool,
      message: map['message'] as String,
      recentTransactions: List<TransactionResponse>.from(
        (map['recent_transactions'] as List<dynamic>).map<TransactionResponse>(
          (x) => TransactionResponse.fromMap(x as Map<String, dynamic>),
        ),
      ),
    );
  }

  String toJson() => json.encode(toMap());

  factory GetUserRecentTransactionsResponse.fromJson(String source) =>
      GetUserRecentTransactionsResponse.fromMap(
          json.decode(source) as Map<String, dynamic>);

  @override
  String toString() =>
      'GetUserRecentTransactionsResponse(success: $success, message: $message, recentTransactions: $recentTransactions)';

  @override
  bool operator ==(covariant GetUserRecentTransactionsResponse other) {
    if (identical(this, other)) return true;
    final listEquals = const DeepCollectionEquality().equals;

    return other.success == success &&
        other.message == message &&
        listEquals(other.recentTransactions, recentTransactions);
  }

  @override
  int get hashCode =>
      success.hashCode ^ message.hashCode ^ recentTransactions.hashCode;
}

class TransactionResponse {
  final String id;
  final int amount;
  final TransactionMode mode;
  final TransactionType transactionType;
  final TransactionStatus status;
  final DateTime createdAt;
  final DateTime lastUpdated;
  final String senderName;
  final String recipientName;

  const TransactionResponse({
    required this.id,
    required this.amount,
    required this.mode,
    required this.transactionType,
    required this.status,
    required this.createdAt,
    required this.lastUpdated,
    required this.senderName,
    required this.recipientName,
  });

  TransactionResponse copyWith({
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
    return TransactionResponse(
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
      'created_at': createdAt.millisecondsSinceEpoch,
      'last_updated': lastUpdated.millisecondsSinceEpoch,
      'sender_name': senderName,
      'recipient_name': recipientName,
    };
  }

  factory TransactionResponse.fromMap(Map<String, dynamic> map) {
    return TransactionResponse(
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

  factory TransactionResponse.fromJson(String source) =>
      TransactionResponse.fromMap(json.decode(source) as Map<String, dynamic>);

  @override
  String toString() {
    return 'TransactionResponse(id: $id, amount: $amount, mode: $mode, transactionType: $transactionType, status: $status, createdAt: $createdAt, lastUpdated: $lastUpdated, senderName: $senderName, recipientName: $recipientName)';
  }

  @override
  bool operator ==(covariant TransactionResponse other) {
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
