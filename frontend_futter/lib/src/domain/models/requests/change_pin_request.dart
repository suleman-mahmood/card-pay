// ignore_for_file: public_member_api_docs, sort_constructors_first
import 'dart:convert';

class ChangePinRequest {
  final String userId;
  final String newPin;

  const ChangePinRequest({
    required this.userId,
    required this.newPin,
  });

  ChangePinRequest copyWith({
    String? userId,
    String? newPin,
  }) {
    return ChangePinRequest(
      userId: userId ?? this.userId,
      newPin: newPin ?? this.newPin,
    );
  }

  Map<String, dynamic> toMap() {
    return <String, dynamic>{
      'user_id': userId,
      'new_pin': newPin,
    };
  }

  factory ChangePinRequest.fromMap(Map<String, dynamic> map) {
    return ChangePinRequest(
      userId: map['user_id'] as String,
      newPin: map['new_pin'] as String,
    );
  }

  String toJson() => json.encode(toMap());

  factory ChangePinRequest.fromJson(String source) =>
      ChangePinRequest.fromMap(json.decode(source) as Map<String, dynamic>);

  @override
  String toString() => 'ChangePinRequest(userId: $userId, newPin: $newPin)';

  @override
  bool operator ==(covariant ChangePinRequest other) {
    if (identical(this, other)) return true;

    return other.userId == userId && other.newPin == newPin;
  }

  @override
  int get hashCode => userId.hashCode ^ newPin.hashCode;
}
