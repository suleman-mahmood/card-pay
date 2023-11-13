// ignore_for_file: public_member_api_docs, sort_constructors_first
import 'dart:convert';
import 'package:intl/intl.dart';

class Event {
  String id;
  String name;
  String organizerName;
  String venue;
  String description;
  String imageUrl;
  String? attendanceQr;

  int capacity;
  int registrationFee;

  DateTime eventStartTimestamp;
  DateTime eventEndTimestamp;
  DateTime registrationStartTimestamp;
  DateTime registrationEndTimestamp;

  Event({
    DateTime? eventStartTimestamp,
    DateTime? eventEndTimestamp,
    DateTime? registrationStartTimestamp,
    DateTime? registrationEndTimestamp,
    this.id = '',
    this.name = '',
    this.organizerName = '',
    this.venue = '',
    this.description = '',
    this.imageUrl = '',
    this.attendanceQr,
    this.capacity = 0,
    this.registrationFee = 0,
  })  : eventStartTimestamp =
            eventStartTimestamp ?? DateTime(9999, 12, 31, 23, 59, 59, 999, 999),
        eventEndTimestamp =
            eventEndTimestamp ?? DateTime(9999, 12, 31, 23, 59, 59, 999, 999),
        registrationStartTimestamp = registrationStartTimestamp ??
            DateTime(9999, 12, 31, 23, 59, 59, 999, 999),
        registrationEndTimestamp = registrationEndTimestamp ??
            DateTime(9999, 12, 31, 23, 59, 59, 999, 999);

  Event copyWith({
    String? id,
    String? name,
    String? organizerName,
    String? venue,
    String? description,
    String? imageUrl,
    String? attendanceQr,
    int? capacity,
    int? registrationFee,
    DateTime? eventStartTimestamp,
    DateTime? eventEndTimestamp,
    DateTime? registrationStartTimestamp,
    DateTime? registrationEndTimestamp,
  }) {
    return Event(
      id: id ?? this.id,
      name: name ?? this.name,
      organizerName: organizerName ?? this.organizerName,
      venue: venue ?? this.venue,
      description: description ?? this.description,
      imageUrl: imageUrl ?? this.imageUrl,
      attendanceQr: attendanceQr ?? this.attendanceQr,
      capacity: capacity ?? this.capacity,
      registrationFee: registrationFee ?? this.registrationFee,
      eventStartTimestamp: eventStartTimestamp ?? this.eventStartTimestamp,
      eventEndTimestamp: eventEndTimestamp ?? this.eventEndTimestamp,
      registrationStartTimestamp:
          registrationStartTimestamp ?? this.registrationStartTimestamp,
      registrationEndTimestamp:
          registrationEndTimestamp ?? this.registrationEndTimestamp,
    );
  }

  Map<String, dynamic> toMap() {
    return <String, dynamic>{
      'id': id,
      'name': name,
      'organizer_name': organizerName,
      'venue': venue,
      'description': description,
      'image_url': imageUrl,
      'qr_id': attendanceQr,
      'capacity': capacity,
      'registration_fee': registrationFee,
      'event_start_time': eventStartTimestamp.millisecondsSinceEpoch,
      'event_end_timestamp': eventEndTimestamp.millisecondsSinceEpoch,
      'registration_start_timestamp':
          registrationStartTimestamp.millisecondsSinceEpoch,
      'registration_end_timestamp':
          registrationEndTimestamp.millisecondsSinceEpoch,
    };
  }

  factory Event.fromMap(Map<String, dynamic> map) {
    return Event(
      id: map['id'] as String,
      name: map['name'] as String,
      organizerName: map['organizer_name'] as String,
      venue: map['venue'] as String,
      description: map['description'] as String,
      imageUrl: map['image_url'] as String,
      attendanceQr: map['qr_id'] != null ? map['qr_id'] as String : null,
      capacity: map['capacity'] as int,
      registrationFee: map['registration_fee'] as int,
      eventStartTimestamp: DateFormat("EEE, dd MMM yyyy HH:mm:ss 'GMT'")
          .parse(map['event_start_timestamp']),
      eventEndTimestamp: DateFormat("EEE, dd MMM yyyy HH:mm:ss 'GMT'")
          .parse(map['event_end_timestamp']),
      registrationStartTimestamp: DateFormat("EEE, dd MMM yyyy HH:mm:ss 'GMT'")
          .parse(map['registration_start_timestamp']),
      registrationEndTimestamp: DateFormat("EEE, dd MMM yyyy HH:mm:ss 'GMT'")
          .parse(map['registration_end_timestamp']),
    );
  }

  String toJson() => json.encode(toMap());

  factory Event.fromJson(String source) =>
      Event.fromMap(json.decode(source) as Map<String, dynamic>);

  @override
  String toString() {
    return 'Event(id: $id, name: $name, organizerName: $organizerName, venue: $venue, description: $description, imageUrl: $imageUrl, attendanceQr: $attendanceQr, capacity: $capacity, registrationFee: $registrationFee, eventStartTimestamp: $eventStartTimestamp, eventEndTimestamp: $eventEndTimestamp, registrationStartTimestamp: $registrationStartTimestamp, registrationEndTimestamp: $registrationEndTimestamp)';
  }

  @override
  bool operator ==(covariant Event other) {
    if (identical(this, other)) return true;

    return other.id == id &&
        other.name == name &&
        other.organizerName == organizerName &&
        other.venue == venue &&
        other.description == description &&
        other.imageUrl == imageUrl &&
        other.attendanceQr == attendanceQr &&
        other.capacity == capacity &&
        other.registrationFee == registrationFee &&
        other.eventStartTimestamp == eventStartTimestamp &&
        other.eventEndTimestamp == eventEndTimestamp &&
        other.registrationStartTimestamp == registrationStartTimestamp &&
        other.registrationEndTimestamp == registrationEndTimestamp;
  }

  @override
  int get hashCode {
    return id.hashCode ^
        name.hashCode ^
        organizerName.hashCode ^
        venue.hashCode ^
        description.hashCode ^
        imageUrl.hashCode ^
        attendanceQr.hashCode ^
        capacity.hashCode ^
        registrationFee.hashCode ^
        eventStartTimestamp.hashCode ^
        eventEndTimestamp.hashCode ^
        registrationStartTimestamp.hashCode ^
        registrationEndTimestamp.hashCode;
  }
}
