// ignore_for_file: public_member_api_docs, sort_constructors_first
import 'dart:convert';

import 'package:floor/floor.dart';

@Entity(tableName: "balance")
class Balance {
  @PrimaryKey()
  final int id;

  int amount;

  Balance({
    this.id = 0,
    this.amount = 0,
  });

  Balance copyWith({
    int? id,
    int? amount,
  }) {
    return Balance(
      id: id ?? this.id,
      amount: amount ?? this.amount,
    );
  }

  Map<String, dynamic> toMap() {
    return <String, dynamic>{
      'id': id,
      'amount': amount,
    };
  }

  factory Balance.fromMap(Map<String, dynamic> map) {
    return Balance(
      id: map['id'] as int,
      amount: map['amount'] as int,
    );
  }

  String toJson() => json.encode(toMap());

  factory Balance.fromJson(String source) =>
      Balance.fromMap(json.decode(source) as Map<String, dynamic>);

  @override
  String toString() => 'Balance(id: $id, amount: $amount)';

  @override
  bool operator ==(covariant Balance other) {
    if (identical(this, other)) return true;

    return other.id == id && other.amount == amount;
  }

  @override
  int get hashCode => id.hashCode ^ amount.hashCode;
}
