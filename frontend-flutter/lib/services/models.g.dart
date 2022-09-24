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
      personalEmail: json['personalEmail'] as String? ?? '',
      phoneNumber: json['phoneNumber'] as String? ?? '',
      pin: json['pin'] as String? ?? '',
      verified: json['verified'] as bool? ?? false,
      pendingDeposits: json['pendingDeposits'] as bool? ?? false,
      balance: json['balance'] as int? ?? 0,
      role: $enumDecodeNullable(_$StudentRoleEnumMap, json['role']) ??
          StudentRole.student,
      transactions: (json['transactions'] as List<dynamic>?)
              ?.map((e) => UserTransaction.fromJson(e as Map<String, dynamic>))
              .toList() ??
          const [],
    );

Map<String, dynamic> _$UserToJson(User instance) => <String, dynamic>{
      'id': instance.id,
      'fullName': instance.fullName,
      'email': instance.email,
      'rollNumber': instance.rollNumber,
      'personalEmail': instance.personalEmail,
      'phoneNumber': instance.phoneNumber,
      'pin': instance.pin,
      'verified': instance.verified,
      'pendingDeposits': instance.pendingDeposits,
      'balance': instance.balance,
      'role': _$StudentRoleEnumMap[instance.role]!,
      'transactions': instance.transactions,
    };

const _$StudentRoleEnumMap = {
  StudentRole.student: 'student',
  StudentRole.vendor: 'vendor',
  StudentRole.admin: 'admin',
};

UserTransaction _$UserTransactionFromJson(Map<String, dynamic> json) =>
    UserTransaction(
      id: json['id'] as String? ?? '',
      timestamp: json['timestamp'] as String? ?? '',
      senderName: json['senderName'] as String? ?? '',
      recipientName: json['recipientName'] as String? ?? '',
      amount: json['amount'] as int? ?? 0,
      status: $enumDecodeNullable(_$TransactionStatusEnumMap, json['status']) ??
          TransactionStatus.pending,
    );

Map<String, dynamic> _$UserTransactionToJson(UserTransaction instance) =>
    <String, dynamic>{
      'id': instance.id,
      'timestamp': instance.timestamp,
      'senderName': instance.senderName,
      'recipientName': instance.recipientName,
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
      fullName: json['fullName'] as String? ?? "",
      email: json['email'] as String? ?? "",
    );

Map<String, dynamic> _$DepositArgumentsToJson(DepositArguments instance) =>
    <String, dynamic>{
      'amount': instance.amount,
      'fullName': instance.fullName,
      'email': instance.email,
    };

DepositReturnObject _$DepositReturnObjectFromJson(Map<String, dynamic> json) =>
    DepositReturnObject(
      status: json['status'] as String? ?? "",
      message: json['message'] as String? ?? "",
      paymentUrl: json['paymentUrl'] as String? ?? "",
      orderNumber: json['orderNumber'] as String? ?? "",
      payProId: json['payProId'] as String? ?? "",
    );

Map<String, dynamic> _$DepositReturnObjectToJson(
        DepositReturnObject instance) =>
    <String, dynamic>{
      'status': instance.status,
      'message': instance.message,
      'paymentUrl': instance.paymentUrl,
      'orderNumber': instance.orderNumber,
      'payProId': instance.payProId,
    };

CreateUserArguments _$CreateUserArgumentsFromJson(Map<String, dynamic> json) =>
    CreateUserArguments(
      fullName: json['fullName'] as String? ?? '',
      rollNumber: json['rollNumber'] as String? ?? '',
      pin: json['pin'] as String? ?? '',
      role: $enumDecodeNullable(_$StudentRoleEnumMap, json['role']) ??
          StudentRole.student,
    );

Map<String, dynamic> _$CreateUserArgumentsToJson(
        CreateUserArguments instance) =>
    <String, dynamic>{
      'fullName': instance.fullName,
      'rollNumber': instance.rollNumber,
      'pin': instance.pin,
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

AppVersionInfo _$AppVersionInfoFromJson(Map<String, dynamic> json) =>
    AppVersionInfo(
      versionNumber: json['versionNumber'] as String? ?? "0.00",
      breakingChanges: json['breakingChanges'] as bool? ?? false,
    );

Map<String, dynamic> _$AppVersionInfoToJson(AppVersionInfo instance) =>
    <String, dynamic>{
      'versionNumber': instance.versionNumber,
      'breakingChanges': instance.breakingChanges,
    };
