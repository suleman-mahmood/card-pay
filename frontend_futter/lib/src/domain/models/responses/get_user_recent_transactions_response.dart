// ignore_for_file: public_member_api_docs, sort_constructors_first
import 'dart:convert';

import 'package:cardpay/src/domain/models/transaction.dart';
import 'package:collection/collection.dart';

class GetUserRecentTransactionsResponse {
  final String message;
  final List<Transaction> recentTransactions;

  const GetUserRecentTransactionsResponse({
    required this.message,
    required this.recentTransactions,
  });

  GetUserRecentTransactionsResponse copyWith({
    String? message,
    List<Transaction>? recentTransactions,
  }) {
    return GetUserRecentTransactionsResponse(
      message: message ?? this.message,
      recentTransactions: recentTransactions ?? this.recentTransactions,
    );
  }

  Map<String, dynamic> toMap() {
    return <String, dynamic>{
      'message': message,
      'recent_transactions': recentTransactions.map((x) => x.toMap()).toList(),
    };
  }

  factory GetUserRecentTransactionsResponse.fromMap(Map<String, dynamic> map) {
    return GetUserRecentTransactionsResponse(
      message: map['message'] as String,
      recentTransactions: List<Transaction>.from(
        (map['data'] as List<dynamic>).map<Transaction>(
          (x) => Transaction.fromMap(x as Map<String, dynamic>),
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
      'GetUserRecentTransactionsResponse(message: $message, recentTransactions: $recentTransactions)';

  @override
  bool operator ==(covariant GetUserRecentTransactionsResponse other) {
    if (identical(this, other)) return true;
    final listEquals = const DeepCollectionEquality().equals;

    return other.message == message &&
        listEquals(other.recentTransactions, recentTransactions);
  }

  @override
  int get hashCode => message.hashCode ^ recentTransactions.hashCode;
}
