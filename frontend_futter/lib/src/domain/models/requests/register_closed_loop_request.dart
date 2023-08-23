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

  String toJson() => json.encode(toMap());

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
