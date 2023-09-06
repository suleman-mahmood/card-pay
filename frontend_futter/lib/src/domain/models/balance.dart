// ignore_for_file: public_member_api_docs, sort_constructors_first
import 'dart:convert';

class Balance {
  int amount;

  Balance({
    this.amount = 0,
  });

  Balance copyWith({
    int? amount,
  }) {
    return Balance(
      amount: amount ?? this.amount,
    );
  }

  Map<String, dynamic> toMap() {
    return <String, dynamic>{
      'amount': amount,
    };
  }

  factory Balance.fromMap(Map<String, dynamic> map) {
    return Balance(
      amount: map['amount'] as int,
    );
  }

  String toJson() => json.encode(toMap());

  factory Balance.fromJson(String source) =>
      Balance.fromMap(json.decode(source) as Map<String, dynamic>);

  @override
  String toString() => 'Balance(amount: $amount)';

  @override
  bool operator ==(covariant Balance other) {
    if (identical(this, other)) return true;

    return other.amount == amount;
  }

  @override
  int get hashCode => amount.hashCode;
}
