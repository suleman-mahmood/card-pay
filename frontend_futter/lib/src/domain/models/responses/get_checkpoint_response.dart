// ignore_for_file: public_member_api_docs, sort_constructors_first
import 'dart:convert';

import 'package:cardpay/src/domain/models/checkpoints.dart';

class GetCheckpointsResponse {
  final String message;
  final Checkpoints checks;

  const GetCheckpointsResponse({
    required this.message,
    required this.checks,
  });

  GetCheckpointsResponse copyWith({
    String? message,
    Checkpoints? checks,
  }) {
    return GetCheckpointsResponse(
      message: message ?? this.message,
      checks: checks ?? this.checks,
    );
  }

  factory GetCheckpointsResponse.fromMap(Map<String, dynamic> map) {
    return GetCheckpointsResponse(
      message: map['message'] as String,
      checks: Checkpoints.fromMap(map['data'] as Map<String, dynamic>),
    );
  }

  factory GetCheckpointsResponse.fromJson(String source) =>
      GetCheckpointsResponse.fromMap(
          json.decode(source) as Map<String, dynamic>);

  @override
  String toString() =>
      'GetCheckpointsResponse(message: $message, data: $checks)';

  @override
  bool operator ==(covariant GetCheckpointsResponse other) {
    if (identical(this, other)) return true;

    return other.message == message && other.checks == checks;
  }

  @override
  int get hashCode => message.hashCode ^ checks.hashCode;
}
