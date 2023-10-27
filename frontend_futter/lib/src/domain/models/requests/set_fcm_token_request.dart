// ignore_for_file: public_member_api_docs, sort_constructors_first
import 'dart:convert';

class SetFcmTokenRequest {
  final String fcmToken;

  const SetFcmTokenRequest({
    required this.fcmToken,
  });

  SetFcmTokenRequest copyWith({
    String? fcmToken,
  }) {
    return SetFcmTokenRequest(
      fcmToken: fcmToken ?? this.fcmToken,
    );
  }

  Map<String, dynamic> toMap() {
    return <String, dynamic>{
      'fcm_token': fcmToken,
    };
  }

  factory SetFcmTokenRequest.fromMap(Map<String, dynamic> map) {
    return SetFcmTokenRequest(
      fcmToken: map['fcm_token'] as String,
    );
  }

  String toJson() => json.encode(toMap());

  factory SetFcmTokenRequest.fromJson(String source) =>
      SetFcmTokenRequest.fromMap(json.decode(source) as Map<String, dynamic>);

  @override
  String toString() => 'SetFcmTokenRequest(fcmToken: $fcmToken)';

  @override
  bool operator ==(covariant SetFcmTokenRequest other) {
    if (identical(this, other)) return true;

    return other.fcmToken == fcmToken;
  }

  @override
  int get hashCode => fcmToken.hashCode;
}
