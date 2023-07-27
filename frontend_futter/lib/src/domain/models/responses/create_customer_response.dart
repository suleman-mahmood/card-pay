// ignore_for_file: public_member_api_docs, sort_constructors_first
import 'dart:convert';

import 'package:cardpay/src/utils/constants/event_codes.dart';

class CreateCustomerResponse {
  final bool success;
  final String message;
  final EventCodes eventCode;
  final String userId;

  CreateCustomerResponse({
    required this.success,
    required this.message,
    required this.eventCode,
    required this.userId,
  });

  CreateCustomerResponse copyWith({
    bool? success,
    String? message,
    EventCodes? eventCode,
    String? userId,
  }) {
    return CreateCustomerResponse(
      success: success ?? this.success,
      message: message ?? this.message,
      eventCode: eventCode ?? this.eventCode,
      userId: userId ?? this.userId,
    );
  }

  Map<String, dynamic> toMap() {
    return <String, dynamic>{
      'success': success,
      'message': message,
      'event_code': eventCode.name,
      'user_id': userId,
    };
  }

  factory CreateCustomerResponse.fromMap(Map<String, dynamic> map) {
    return CreateCustomerResponse(
      success: map['success'] as bool,
      message: map['message'] as String,
      eventCode: EventCodes.values.firstWhere(
        (e) => e.name == map['event_code'],
      ),
      userId: map['user_id'] as String,
    );
  }

  String toJson() => json.encode(toMap());

  factory CreateCustomerResponse.fromJson(String source) =>
      CreateCustomerResponse.fromMap(
          json.decode(source) as Map<String, dynamic>);

  @override
  String toString() {
    return 'CreateCustomerResponse(success: $success, message: $message, eventCode: $eventCode, userId: $userId)';
  }

  @override
  bool operator ==(covariant CreateCustomerResponse other) {
    if (identical(this, other)) return true;

    return other.success == success &&
        other.message == message &&
        other.eventCode == eventCode &&
        other.userId == userId;
  }

  @override
  int get hashCode {
    return success.hashCode ^
        message.hashCode ^
        eventCode.hashCode ^
        userId.hashCode;
  }
}
