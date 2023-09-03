// ignore_for_file: public_member_api_docs, sort_constructors_first
import 'dart:convert';

class Transfer {
  int amount;
  String senderUniqueIdentifier;
  String recipientUniqueIdentifier;

  Transfer({
    this.amount = 0,
    this.senderUniqueIdentifier = '',
    this.recipientUniqueIdentifier = '',
  });

  Transfer copyWith({
    int? amount,
    String? senderUniqueIdentifier,
    String? recipientUniqueIdentifier,
  }) {
    return Transfer(
      amount: amount ?? this.amount,
      senderUniqueIdentifier:
          senderUniqueIdentifier ?? this.senderUniqueIdentifier,
      recipientUniqueIdentifier:
          recipientUniqueIdentifier ?? this.recipientUniqueIdentifier,
    );
  }

  Map<String, dynamic> toMap() {
    return <String, dynamic>{
      'amount': amount,
      'sender_unique_identifier': senderUniqueIdentifier,
      'recipient_unique_identifier': recipientUniqueIdentifier,
    };
  }

  factory Transfer.fromMap(Map<String, dynamic> map) {
    return Transfer(
      amount: map['amount'] as int,
      senderUniqueIdentifier: map['sender_unique_identifier'] as String,
      recipientUniqueIdentifier: map['recipient_unique_identifier'] as String,
    );
  }

  String toJson() => json.encode(toMap());

  factory Transfer.fromJson(String source) =>
      Transfer.fromMap(json.decode(source) as Map<String, dynamic>);

  @override
  String toString() =>
      'Transfer(amount: $amount, senderUniqueIdentifier: $senderUniqueIdentifier, recipientUniqueIdentifier: $recipientUniqueIdentifier)';

  @override
  bool operator ==(covariant Transfer other) {
    if (identical(this, other)) return true;

    return other.amount == amount &&
        other.senderUniqueIdentifier == senderUniqueIdentifier &&
        other.recipientUniqueIdentifier == recipientUniqueIdentifier;
  }

  @override
  int get hashCode =>
      amount.hashCode ^
      senderUniqueIdentifier.hashCode ^
      recipientUniqueIdentifier.hashCode;
}
