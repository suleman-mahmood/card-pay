import 'package:json_annotation/json_annotation.dart';
part 'models.g.dart';

enum StudentRole {
  student,
  vendor,
  admin,
}

enum TransactionStatus {
  pending,
  successful,
  failed,
}

@JsonSerializable()
class User {
  final String id;
  final String fullName;
  final String email;
  final String rollNumber;
  final bool verified;
  final StudentRole role;
  final int balance;

  User({
    this.id = '',
    this.fullName = '',
    this.email = '',
    this.rollNumber = '',
    this.verified = false,
    this.role = StudentRole.student,
    this.balance = 0,
  });

  factory User.fromJson(Map<String, dynamic> json) => _$UserFromJson(json);
  Map<String, dynamic> toJson() => _$UserToJson(this);
}

@JsonSerializable()
class Transaction {
  final String id;
  final String timestamp;
  final String senderId;
  final String recipientId;
  final int amount;
  final TransactionStatus status;

  Transaction({
    this.id = '',
    this.timestamp = '',
    this.senderId = '',
    this.recipientId = '',
    this.amount = 0,
    this.status = TransactionStatus.pending,
  });

  factory Transaction.fromJson(Map<String, dynamic> json) =>
      _$TransactionFromJson(json);
  Map<String, dynamic> toJson() => _$TransactionToJson(this);
}
