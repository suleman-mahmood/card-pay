// GENERATED CODE - DO NOT MODIFY BY HAND

part of 'models.dart';

// **************************************************************************
// JsonSerializableGenerator
// **************************************************************************

User _$UserFromJson(Map<String, dynamic> json) => User(
      id: json['id'] as String? ?? '',
      fullName: json['fullName'] as String? ?? '',
      email: json['email'] as String? ?? '',
      rollNumber: json['rollNumber'] as String? ?? '',
      verified: json['verified'] as bool? ?? false,
      role: $enumDecodeNullable(_$StudentRoleEnumMap, json['role']) ??
          StudentRole.student,
      balance: json['balance'] as int? ?? 0,
    );

Map<String, dynamic> _$UserToJson(User instance) => <String, dynamic>{
      'id': instance.id,
      'fullName': instance.fullName,
      'email': instance.email,
      'rollNumber': instance.rollNumber,
      'verified': instance.verified,
      'role': _$StudentRoleEnumMap[instance.role]!,
      'balance': instance.balance,
    };

const _$StudentRoleEnumMap = {
  StudentRole.student: 'student',
  StudentRole.vendor: 'vendor',
  StudentRole.admin: 'admin',
};

Transaction _$TransactionFromJson(Map<String, dynamic> json) => Transaction(
      id: json['id'] as String? ?? '',
      timestamp: json['timestamp'] as String? ?? '',
      senderId: json['senderId'] as String? ?? '',
      recipientId: json['recipientId'] as String? ?? '',
      amount: json['amount'] as int? ?? 0,
      status: $enumDecodeNullable(_$TransactionStatusEnumMap, json['status']) ??
          TransactionStatus.pending,
    );

Map<String, dynamic> _$TransactionToJson(Transaction instance) =>
    <String, dynamic>{
      'id': instance.id,
      'timestamp': instance.timestamp,
      'senderId': instance.senderId,
      'recipientId': instance.recipientId,
      'amount': instance.amount,
      'status': _$TransactionStatusEnumMap[instance.status]!,
    };

const _$TransactionStatusEnumMap = {
  TransactionStatus.pending: 'pending',
  TransactionStatus.successful: 'successful',
  TransactionStatus.failed: 'failed',
};

DepositArguments _$DepositArgumentsFromJson(Map<String, dynamic> json) =>
    DepositArguments(
      amount: json['amount'] as int? ?? 0,
      cardNumber: json['cardNumber'] as String? ?? '',
      cvv: json['cvv'] as String? ?? '',
      expiryDate: json['expiryDate'] as String? ?? '',
    );

Map<String, dynamic> _$DepositArgumentsToJson(DepositArguments instance) =>
    <String, dynamic>{
      'amount': instance.amount,
      'cardNumber': instance.cardNumber,
      'cvv': instance.cvv,
      'expiryDate': instance.expiryDate,
    };

CreateUserArguments _$CreateUserArgumentsFromJson(Map<String, dynamic> json) =>
    CreateUserArguments(
      fullName: json['fullName'] as String? ?? '',
      rollNumber: json['rollNumber'] as String? ?? '',
      role: $enumDecodeNullable(_$StudentRoleEnumMap, json['role']) ??
          StudentRole.student,
    );

Map<String, dynamic> _$CreateUserArgumentsToJson(
        CreateUserArguments instance) =>
    <String, dynamic>{
      'fullName': instance.fullName,
      'rollNumber': instance.rollNumber,
      'role': _$StudentRoleEnumMap[instance.role]!,
    };

MakeTransferArguments _$MakeTransferArgumentsFromJson(
        Map<String, dynamic> json) =>
    MakeTransferArguments(
      amount: json['amount'] as int? ?? 0,
      recipientRollNumber: json['recipientRollNumber'] as String? ?? '',
    );

Map<String, dynamic> _$MakeTransferArgumentsToJson(
        MakeTransferArguments instance) =>
    <String, dynamic>{
      'amount': instance.amount,
      'recipientRollNumber': instance.recipientRollNumber,
    };
