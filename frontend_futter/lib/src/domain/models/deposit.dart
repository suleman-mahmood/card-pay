// ignore_for_file: public_member_api_docs, sort_constructors_first
import 'dart:convert';

class Deposit {
  int amount;

  Deposit({
    this.amount = 0,
  });

  Deposit copyWith({
    int? amount,
  }) {
    return Deposit(
      amount: amount ?? this.amount,
    );
  }

  Map<String, dynamic> toMap() {
    return <String, dynamic>{
      'amount': amount,
    };
  }

  factory Deposit.fromMap(Map<String, dynamic> map) {
    return Deposit(
      amount: map['amount'] as int,
    );
  }

  String toJson() => json.encode(toMap());

  factory Deposit.fromJson(String source) =>
      Deposit.fromMap(json.decode(source) as Map<String, dynamic>);

  @override
  String toString() => 'Deposit(amount: $amount)';

  @override
  bool operator ==(covariant Deposit other) {
    if (identical(this, other)) return true;

    return other.amount == amount;
  }

  @override
  int get hashCode => amount.hashCode;
}
