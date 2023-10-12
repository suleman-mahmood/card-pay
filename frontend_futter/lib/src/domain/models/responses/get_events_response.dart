// ignore_for_file: public_member_api_docs, sort_constructors_first
import 'dart:convert';

import 'package:cardpay/src/domain/models/event.dart';
import 'package:collection/collection.dart';

class GetEventsResponse {
  final String message;
  final List<Event> events;

  const GetEventsResponse({
    required this.message,
    required this.events,
  });

  GetEventsResponse copyWith({
    String? message,
    List<Event>? events,
  }) {
    return GetEventsResponse(
      message: message ?? this.message,
      events: events ?? this.events,
    );
  }

  Map<String, dynamic> toMap() {
    return <String, dynamic>{
      'message': message,
      'events': events.map((x) => x.toMap()).toList(),
    };
  }

  factory GetEventsResponse.fromMap(Map<String, dynamic> map) {
    return GetEventsResponse(
      message: map['message'] as String,
      events: List<Event>.from(
        (map['data'] as List<dynamic>).map<Event>(
          (x) => Event.fromMap(x as Map<String, dynamic>),
        ),
      ),
    );
  }

  String toJson() => json.encode(toMap());

  factory GetEventsResponse.fromJson(String source) =>
      GetEventsResponse.fromMap(json.decode(source) as Map<String, dynamic>);

  @override
  String toString() => 'GetEventsResponse(message: $message, events: $events)';

  @override
  bool operator ==(covariant GetEventsResponse other) {
    if (identical(this, other)) return true;
    final listEquals = const DeepCollectionEquality().equals;

    return other.message == message && listEquals(other.events, events);
  }

  @override
  int get hashCode => message.hashCode ^ events.hashCode;
}
