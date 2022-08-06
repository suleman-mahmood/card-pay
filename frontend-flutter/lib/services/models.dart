import 'package:flutter/material.dart';
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
class User extends ChangeNotifier {
  String id;
  String fullName;
  String email;
  String rollNumber;
  bool verified;
  StudentRole role;
  int balance;

  User({
    this.id = '',
    this.fullName = '',
    this.email = '',
    this.rollNumber = '',
    this.verified = false,
    this.role = StudentRole.student,
    this.balance = 0,
  });

  void updateUser(User u) {
    id = u.id;
    fullName = u.fullName;
    email = u.email;
    rollNumber = u.rollNumber;
    verified = u.verified;
    role = u.role;
    balance = u.balance;

    notifyListeners();
  }

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

@JsonSerializable()
class DepositArguments {
  final int amount;
  final String cardNumber;
  final String cvv;
  final String expiryDate;

  DepositArguments({
    this.amount = 0,
    this.cardNumber = '',
    this.cvv = '',
    this.expiryDate = '',
  });

  factory DepositArguments.fromJson(Map<String, dynamic> json) =>
      _$DepositArgumentsFromJson(json);
  Map<String, dynamic> toJson() => _$DepositArgumentsToJson(this);
}

@JsonSerializable()
class CreateUserArguments {
  final String fullName;
  final String rollNumber;
  final StudentRole role;

  CreateUserArguments({
    this.fullName = '',
    this.rollNumber = '',
    this.role = StudentRole.student,
  });

  factory CreateUserArguments.fromJson(Map<String, dynamic> json) =>
      _$CreateUserArgumentsFromJson(json);
  Map<String, dynamic> toJson() => _$CreateUserArgumentsToJson(this);
}

@JsonSerializable()
class MakeTransferArguments {
  final int amount;
  final String recipientRollNumber;

  MakeTransferArguments({
    this.amount = 0,
    this.recipientRollNumber = '',
  });

  factory MakeTransferArguments.fromJson(Map<String, dynamic> json) =>
      _$MakeTransferArgumentsFromJson(json);
  Map<String, dynamic> toJson() => _$MakeTransferArgumentsToJson(this);
}
