// ignore_for_file: public_member_api_docs, sort_constructors_first
import 'dart:convert';

import 'package:equatable/equatable.dart';

class User extends Equatable {
  final String? id;
  final String? fullName;
  const User({
    this.id,
    this.fullName,
  });

  User copyWith({
    String? id,
    String? fullName,
  }) {
    return User(
      id: id ?? this.id,
      fullName: fullName ?? this.fullName,
    );
  }

  Map<String, dynamic> toMap() {
    return <String, dynamic>{
      'id': id,
      'fullName': fullName,
    };
  }

  factory User.fromMap(Map<String, dynamic> map) {
    return User(
      id: map['id'] != null ? map['id'] as String : null,
      fullName: map['fullName'] != null ? map['fullName'] as String : null,
    );
  }

  String toJson() => json.encode(toMap());

  factory User.fromJson(String source) =>
      User.fromMap(json.decode(source) as Map<String, dynamic>);

  @override
  bool get stringify => true;

  @override
  List<Object?> get props => [id, fullName];
}
