// ignore_for_file: public_member_api_docs, sort_constructors_first
import 'dart:convert';

class VerifyClosedLoopRequest {
  final String userId;
  final String closedLoopId;
  final String uniqueIdentifierOtp;

  const VerifyClosedLoopRequest({
    required this.userId,
    required this.closedLoopId,
    required this.uniqueIdentifierOtp,
  });

  VerifyClosedLoopRequest copyWith({
    String? userId,
    String? closedLoopId,
    String? uniqueIdentifierOtp,
  }) {
    return VerifyClosedLoopRequest(
      userId: userId ?? this.userId,
      closedLoopId: closedLoopId ?? this.closedLoopId,
      uniqueIdentifierOtp: uniqueIdentifierOtp ?? this.uniqueIdentifierOtp,
    );
  }

  Map<String, dynamic> toMap() {
    return <String, dynamic>{
      'user_id': userId,
      'closed_loop_id': closedLoopId,
      'unique_identifier_otp': uniqueIdentifierOtp,
    };
  }

  factory VerifyClosedLoopRequest.fromMap(Map<String, dynamic> map) {
    return VerifyClosedLoopRequest(
      userId: map['user_id'] as String,
      closedLoopId: map['closed_loop_id'] as String,
      uniqueIdentifierOtp: map['unique_identifier_otp'] as String,
    );
  }

  String toJson() => json.encode(toMap());

  factory VerifyClosedLoopRequest.fromJson(String source) =>
      VerifyClosedLoopRequest.fromMap(
          json.decode(source) as Map<String, dynamic>);

  @override
  String toString() =>
      'VerifyClosedLoopRequest(userId: $userId, closedLoopId: $closedLoopId, uniqueIdentifierOtp: $uniqueIdentifierOtp)';

  @override
  bool operator ==(covariant VerifyClosedLoopRequest other) {
    if (identical(this, other)) return true;

    return other.userId == userId &&
        other.closedLoopId == closedLoopId &&
        other.uniqueIdentifierOtp == uniqueIdentifierOtp;
  }

  @override
  int get hashCode =>
      userId.hashCode ^ closedLoopId.hashCode ^ uniqueIdentifierOtp.hashCode;
}
