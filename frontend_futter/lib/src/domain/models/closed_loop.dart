// ignore_for_file: public_member_api_docs, sort_constructors_first
import 'dart:convert';

import 'package:intl/intl.dart';

// Add this when using from map
// createdAt: DateFormat("EEE, dd MMM yyyy HH:mm:ss 'GMT'").parse(map['created_at'])

class ClosedLoop {
  String id;
  String name;
  String logoUrl;
  String description;
  String regex;
  String verificationType;
  DateTime createdAt;

  ClosedLoop({
    DateTime? createdAt,
    this.id = '',
    this.name = '',
    this.logoUrl = '',
    this.description = '',
    this.regex = '',
    this.verificationType = '',
  }) : createdAt = createdAt ?? DateTime(9999, 12, 31, 23, 59, 59, 999, 999);

  ClosedLoop copyWith({
    String? id,
    String? name,
    String? logoUrl,
    String? description,
    String? regex,
    String? verificationType,
    DateTime? createdAt,
  }) {
    return ClosedLoop(
      id: id ?? this.id,
      name: name ?? this.name,
      logoUrl: logoUrl ?? this.logoUrl,
      description: description ?? this.description,
      regex: regex ?? this.regex,
      verificationType: verificationType ?? this.verificationType,
      createdAt: createdAt ?? this.createdAt,
    );
  }

  Map<String, dynamic> toMap() {
    return <String, dynamic>{
      'id': id,
      'name': name,
      'logo_url': logoUrl,
      'description': description,
      'regex': regex,
      'verification_type': verificationType,
      'created_at': createdAt.millisecondsSinceEpoch,
    };
  }

  factory ClosedLoop.fromMap(Map<String, dynamic> map) {
    return ClosedLoop(
      id: map['id'] as String,
      name: map['name'] as String,
      logoUrl: map['logo_url'] as String,
      description: map['description'] as String,
      regex: map['regex'] as String,
      verificationType: map['verification_type'] as String,
      createdAt: DateFormat("EEE, dd MMM yyyy HH:mm:ss 'GMT'")
          .parse(map['created_at']),
    );
  }

  String toJson() => json.encode(toMap());

  factory ClosedLoop.fromJson(String source) =>
      ClosedLoop.fromMap(json.decode(source) as Map<String, dynamic>);

  @override
  String toString() {
    return 'ClosedLoop(id: $id, name: $name, logoUrl: $logoUrl, description: $description, regex: $regex, verificationType: $verificationType, createdAt: $createdAt)';
  }

  @override
  bool operator ==(covariant ClosedLoop other) {
    if (identical(this, other)) return true;

    return other.id == id &&
        other.name == name &&
        other.logoUrl == logoUrl &&
        other.description == description &&
        other.regex == regex &&
        other.verificationType == verificationType &&
        other.createdAt == createdAt;
  }

  @override
  int get hashCode {
    return id.hashCode ^
        name.hashCode ^
        logoUrl.hashCode ^
        description.hashCode ^
        regex.hashCode ^
        verificationType.hashCode ^
        createdAt.hashCode;
  }
}
