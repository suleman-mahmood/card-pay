// ignore_for_file: public_member_api_docs, sort_constructors_first
import 'dart:convert';

class RegisterEventRequest {
  final String eventId;

  const RegisterEventRequest({
    required this.eventId,
  });

  RegisterEventRequest copyWith({
    String? eventId,
  }) {
    return RegisterEventRequest(
      eventId: eventId ?? this.eventId,
    );
  }

  Map<String, dynamic> toMap() {
    return <String, dynamic>{
      'event_id': eventId,
    };
  }

  factory RegisterEventRequest.fromMap(Map<String, dynamic> map) {
    return RegisterEventRequest(
      eventId: map['event_id'] as String,
    );
  }

  String toJson() => json.encode(toMap());

  factory RegisterEventRequest.fromJson(String source) =>
      RegisterEventRequest.fromMap(json.decode(source) as Map<String, dynamic>);

  @override
  String toString() => 'RegisterEventRequest(eventId: $eventId)';

  @override
  bool operator ==(covariant RegisterEventRequest other) {
    if (identical(this, other)) return true;

    return other.eventId == eventId;
  }

  @override
  int get hashCode => eventId.hashCode;
}
