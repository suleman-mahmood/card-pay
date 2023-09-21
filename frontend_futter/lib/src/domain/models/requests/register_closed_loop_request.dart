// ignore_for_file: public_member_api_docs, sort_constructors_first
import 'dart:convert';

class RegisterClosedLoopRequest {
  final String closedLoopId;
  final String uniqueIdentifier;

  const RegisterClosedLoopRequest({
    required this.closedLoopId,
    required this.uniqueIdentifier,
  });

  RegisterClosedLoopRequest copyWith({
    String? closedLoopId,
    String? uniqueIdentifier,
  }) {
    return RegisterClosedLoopRequest(
      closedLoopId: closedLoopId ?? this.closedLoopId,
      uniqueIdentifier: uniqueIdentifier ?? this.uniqueIdentifier,
    );
  }

  Map<String, dynamic> toMap() {
    return <String, dynamic>{
      'closed_loop_id': closedLoopId,
      'unique_identifier': uniqueIdentifier,
    };
  }

  factory RegisterClosedLoopRequest.fromMap(Map<String, dynamic> map) {
    return RegisterClosedLoopRequest(
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
      'RegisterClosedLoopRequest(closedLoopId: $closedLoopId, uniqueIdentifier: $uniqueIdentifier)';

  @override
  bool operator ==(covariant RegisterClosedLoopRequest other) {
    if (identical(this, other)) return true;

    return other.closedLoopId == closedLoopId &&
        other.uniqueIdentifier == uniqueIdentifier;
  }

  @override
  int get hashCode => closedLoopId.hashCode ^ uniqueIdentifier.hashCode;
}
