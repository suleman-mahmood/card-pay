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

class RollNumber {
  String rollNumber;

  RollNumber({this.rollNumber = ''});

  String get getRollNumber => rollNumber;
  String get getEmail => '$rollNumber@lums.edu.pk';

  set setRollNumber(String rn) {
    rollNumber = rn;
  }
}

class Loading extends ChangeNotifier {
  bool loading = false;

  get getLoading => loading;

  void showLoading() {
    loading = true;
    notifyListeners();
  }

  void hideLoading() {
    loading = false;
    notifyListeners();
  }
}

class ErrorModel extends ChangeNotifier {
  bool hasError;
  String code;
  String message;

  ErrorModel({this.hasError = false, this.message = "", this.code = ""});

  void errorOcurred(String code, String message) {
    this.hasError = true;
    this.code = code;
    this.message = message;

    notifyListeners();
  }

  void errorResolved() {
    this.hasError = false;
    this.code = "";
    this.message = "";

    notifyListeners();
  }
}

@JsonSerializable()
class User extends ChangeNotifier {
  String id;
  String fullName;
  String email;
  String rollNumber;
  String personalEmail;
  String phoneNumber;
  String pin;
  bool verified;
  bool pendingDeposits;
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
    this.pin = '',
    this.verified = false,
    this.pendingDeposits = false,
    this.balance = 0,
    this.role = StudentRole.student,
    this.transactions = const [],
  });

  String get getCardFullName {
    final words = fullName.split(" ");

    if (words.length == 1) {
      return "${words[0]}.";
    } else if (words.length >= 2) {
      return "${words[0]} ${words.last[0]}.";
    } else {
      return "";
    }
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
  final String fullName;
  final String email;

  DepositArguments({
    this.amount = 0,
    this.fullName = "",
    this.email = "",
  });

  factory DepositArguments.fromJson(Map<String, dynamic> json) =>
      _$DepositArgumentsFromJson(json);
  Map<String, dynamic> toJson() => _$DepositArgumentsToJson(this);
}

@JsonSerializable()
class DepositReturnObject {
  final String status;
  final String message;
  final String paymentUrl;
  final String orderNumber;
  final String payProId;

  DepositReturnObject({
    this.status = "",
    this.message = "",
    this.paymentUrl = "",
    this.orderNumber = "",
    this.payProId = "",
  });

  factory DepositReturnObject.fromJson(Map<String, dynamic> json) =>
      _$DepositReturnObjectFromJson(json);
  Map<String, dynamic> toJson() => _$DepositReturnObjectToJson(this);
}

@JsonSerializable()
class CreateUserArguments {
  final String fullName;
  final String rollNumber;
  final String pin;
  final StudentRole role;

  CreateUserArguments({
    this.fullName = '',
    this.rollNumber = '',
    this.pin = '',
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
