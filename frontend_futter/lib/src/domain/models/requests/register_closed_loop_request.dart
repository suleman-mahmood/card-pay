// ignore_for_file: public_member_api_docs, sort_constructors_first
import 'dart:convert';

class RegisterClosedLoopRequest {
  final String userId;
  final String closedLoopId;
  final String uniqueIdentifier;

  const RegisterClosedLoopRequest({
    required this.userId,
    required this.closedLoopId,
    required this.uniqueIdentifier,
  });

  RegisterClosedLoopRequest copyWith({
    String? userId,
    String? closedLoopId,
    String? uniqueIdentifier,
  }) {
    return RegisterClosedLoopRequest(
      userId: userId ?? this.userId,
      closedLoopId: closedLoopId ?? this.closedLoopId,
      uniqueIdentifier: uniqueIdentifier ?? this.uniqueIdentifier,
    );
  }

  Map<String, dynamic> toMap() {
    return <String, dynamic>{
      'user_id': userId,
      'closed_loop_id': closedLoopId,
      'unique_identifier': uniqueIdentifier,
    };
  }

  factory RegisterClosedLoopRequest.fromMap(Map<String, dynamic> map) {
    return RegisterClosedLoopRequest(
      userId: map['user_id'] as String,
      closedLoopId: map['closed_loop_id'] as String,
      uniqueIdentifier: map['unique_identifier'] as String,
    );
  }

  String toJson() => json.encode(toMap());

  factory RegisterClosedLoopRequest.fromJson(String source) =>
      RegisterClosedLoopRequest.fromMap(
          json.decode(source) as Map<String, dynamic>);

  @override
  String toString() =>
      'RegisterClosedLoopRequest(userId: $userId, closedLoopId: $closedLoopId, uniqueIdentifier: $uniqueIdentifier)';

  @override
  bool operator ==(covariant RegisterClosedLoopRequest other) {
    if (identical(this, other)) return true;

    return other.userId == userId &&
        other.closedLoopId == closedLoopId &&
        other.uniqueIdentifier == uniqueIdentifier;
  }

  @override
  int get hashCode =>
      userId.hashCode ^ closedLoopId.hashCode ^ uniqueIdentifier.hashCode;
}
