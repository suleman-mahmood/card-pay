import 'dart:convert';

class GetFullNameRequest {
  final String uniqueIdentifier;
  final String closedLoopId;

  const GetFullNameRequest({
    required this.uniqueIdentifier,
    required this.closedLoopId,
  });

  GetFullNameRequest copyWith({
    String? uniqueIdentifier,
    String? closedLoopId,
  }) {
    return GetFullNameRequest(
      uniqueIdentifier: uniqueIdentifier ?? this.uniqueIdentifier,
      closedLoopId: closedLoopId ?? this.closedLoopId,
    );
  }

  Map<String, dynamic> toMap() {
    return {
      'unique_identifier': uniqueIdentifier,
      'closed_loop_id': closedLoopId,
    };
  }

  String toJson() => json.encode(toMap());

  @override
  String toString() =>
      'GetFullNameRequest(uniqueIdentifier: $uniqueIdentifier, closedLoopId: $closedLoopId)';

  @override
  bool operator ==(Object other) {
    if (identical(this, other)) return true;

    return other is GetFullNameRequest &&
        other.uniqueIdentifier == uniqueIdentifier &&
        other.closedLoopId == closedLoopId;
  }

  @override
  int get hashCode => uniqueIdentifier.hashCode ^ closedLoopId.hashCode;
}
