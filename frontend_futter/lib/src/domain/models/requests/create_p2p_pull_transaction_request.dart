// ignore_for_file: public_member_api_docs, sort_constructors_first
import 'dart:convert';

class CreateP2PPullTransactionRequest {
  final String senderUniqueIdentifier;
  final double amount;

  const CreateP2PPullTransactionRequest({
    required this.senderUniqueIdentifier,
    required this.amount,
  });

  CreateP2PPullTransactionRequest copyWith({
    String? senderUniqueIdentifier,
    double? amount,
  }) {
    return CreateP2PPullTransactionRequest(
      senderUniqueIdentifier:
          senderUniqueIdentifier ?? this.senderUniqueIdentifier,
      amount: amount ?? this.amount,
    );
  }

  Map<String, dynamic> toMap() {
    return <String, dynamic>{
      'sender_unique_identifier': senderUniqueIdentifier,
      'amount': amount,
    };
  }

  factory CreateP2PPullTransactionRequest.fromMap(Map<String, dynamic> map) {
    return CreateP2PPullTransactionRequest(
      senderUniqueIdentifier: map['sender_unique_identifier'] as String,
      amount: map['amount'] as double,
    );
  }

  String toJson() => json.encode(toMap());

  factory CreateP2PPullTransactionRequest.fromJson(String source) =>
      CreateP2PPullTransactionRequest.fromMap(
          json.decode(source) as Map<String, dynamic>);

  @override
  String toString() =>
      'CreateP2PPullTransactionRequest(senderUniqueIdentifier: $senderUniqueIdentifier, amount: $amount)';

  @override
  bool operator ==(covariant CreateP2PPullTransactionRequest other) {
    if (identical(this, other)) return true;

    return other.senderUniqueIdentifier == senderUniqueIdentifier &&
        other.amount == amount;
  }

  @override
  int get hashCode => senderUniqueIdentifier.hashCode ^ amount.hashCode;
}
