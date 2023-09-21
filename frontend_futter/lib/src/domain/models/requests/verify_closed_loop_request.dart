// ignore_for_file: public_member_api_docs, sort_constructors_first
import 'dart:convert';

class VerifyClosedLoopRequest {
  final String closedLoopId;
  final String uniqueIdentifierOtp;
  final String referralUniqueIdentifier;

  const VerifyClosedLoopRequest({
    required this.closedLoopId,
    required this.uniqueIdentifierOtp,
    required this.referralUniqueIdentifier,
  });

  VerifyClosedLoopRequest copyWith({
    String? closedLoopId,
    String? uniqueIdentifierOtp,
    String? referralUniqueIdentifier,
  }) {
    return VerifyClosedLoopRequest(
      closedLoopId: closedLoopId ?? this.closedLoopId,
      uniqueIdentifierOtp: uniqueIdentifierOtp ?? this.uniqueIdentifierOtp,
      referralUniqueIdentifier:
          referralUniqueIdentifier ?? this.referralUniqueIdentifier,
    );
  }

  Map<String, dynamic> toMap() {
    return <String, dynamic>{
      'closed_loop_id': closedLoopId,
      'unique_identifier_otp': uniqueIdentifierOtp,
      'referral_unique_identifier': referralUniqueIdentifier,
    };
  }

  factory VerifyClosedLoopRequest.fromMap(Map<String, dynamic> map) {
    return VerifyClosedLoopRequest(
      closedLoopId: map['closed_loop_id'] as String,
      uniqueIdentifierOtp: map['unique_identifier_otp'] as String,
      referralUniqueIdentifier: map['referral_unique_identifier'] as String,
    );
  }

  String toJson() => json.encode(toMap());

  factory VerifyClosedLoopRequest.fromJson(String source) =>
      VerifyClosedLoopRequest.fromMap(
          json.decode(source) as Map<String, dynamic>);

  @override
  String toString() =>
      'VerifyClosedLoopRequest(closedLoopId: $closedLoopId, uniqueIdentifierOtp: $uniqueIdentifierOtp, referralUniqueIdentifier: $referralUniqueIdentifier)';

  @override
  bool operator ==(covariant VerifyClosedLoopRequest other) {
    if (identical(this, other)) return true;

    return other.closedLoopId == closedLoopId &&
        other.uniqueIdentifierOtp == uniqueIdentifierOtp &&
        other.referralUniqueIdentifier == referralUniqueIdentifier;
  }

  @override
  int get hashCode =>
      closedLoopId.hashCode ^
      uniqueIdentifierOtp.hashCode ^
      referralUniqueIdentifier.hashCode;
}
