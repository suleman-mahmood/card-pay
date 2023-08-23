// ignore_for_file: public_member_api_docs, sort_constructors_first
import 'dart:convert';

class VerifyClosedLoopRequest {
  final String closedLoopId;
  final String uniqueIdentifierOtp;

  const VerifyClosedLoopRequest({
    required this.closedLoopId,
    required this.uniqueIdentifierOtp,
  });

  VerifyClosedLoopRequest copyWith({
    String? closedLoopId,
    String? uniqueIdentifierOtp,
  }) {
    return VerifyClosedLoopRequest(
      closedLoopId: closedLoopId ?? this.closedLoopId,
      uniqueIdentifierOtp: uniqueIdentifierOtp ?? this.uniqueIdentifierOtp,
    );
  }

  Map<String, dynamic> toMap() {
    return <String, dynamic>{
      'closed_loop_id': closedLoopId,
      'unique_identifier_otp': uniqueIdentifierOtp,
    };
  }

  String toJson() => json.encode(toMap());

  @override
  String toString() =>
      'VerifyClosedLoopRequest(closedLoopId: $closedLoopId, uniqueIdentifierOtp: $uniqueIdentifierOtp)';

  @override
  bool operator ==(covariant VerifyClosedLoopRequest other) {
    if (identical(this, other)) return true;

    return other.closedLoopId == closedLoopId &&
        other.uniqueIdentifierOtp == uniqueIdentifierOtp;
  }

  @override
  int get hashCode => closedLoopId.hashCode ^ uniqueIdentifierOtp.hashCode;
}
