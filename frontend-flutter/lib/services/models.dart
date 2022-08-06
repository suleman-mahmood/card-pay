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
  String personalEmail;
  String phoneNumber;
  bool verified;
  int balance;
  StudentRole role;
  List<UserTransaction> transactions;

  User({
    this.id = '',
    this.fullName = '',
    this.email = '',
    this.rollNumber = '',
    this.personalEmail = '',
    this.phoneNumber = '',
    this.verified = false,
    this.balance = 0,
    this.role = StudentRole.student,
    this.transactions = const [],
  });

  void updateUser(User u) {
    id = u.id;
    fullName = u.fullName;
    email = u.email;
    rollNumber = u.rollNumber;
    personalEmail = u.personalEmail;
    phoneNumber = u.phoneNumber;
    verified = u.verified;
    balance = u.balance;
    role = u.role;
    transactions = u.transactions;

    notifyListeners();
  }

  factory User.fromJson(Map<String, dynamic> json) => _$UserFromJson(json);
  Map<String, dynamic> toJson() => _$UserToJson(this);
}

@JsonSerializable()
class UserTransaction {
  final String id;
  final String timestamp;
  final String senderName;
  final String recipientName;
  final int amount;
  final TransactionStatus status;

  UserTransaction({
    this.id = '',
    this.timestamp = '',
    this.senderName = '',
    this.recipientName = '',
    this.amount = 0,
    this.status = TransactionStatus.pending,
  });

  factory UserTransaction.fromJson(Map<String, dynamic> json) =>
      _$UserTransactionFromJson(json);
  Map<String, dynamic> toJson() => _$UserTransactionToJson(this);
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
