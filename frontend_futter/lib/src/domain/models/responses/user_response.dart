// ignore_for_file: public_member_api_docs, sort_constructors_first
import 'dart:convert';

import 'package:frontend_futter/src/domain/models/user.dart';

class UserResponse {
  final User user;

  UserResponse({
    this.user = const User(),
  });

  UserResponse copyWith({
    User? user,
  }) {
    return UserResponse(
      user: user ?? this.user,
    );
  }

  Map<String, dynamic> toMap() {
    return <String, dynamic>{
      'user': user.toMap(),
    };
  }

  factory UserResponse.fromMap(Map<String, dynamic> map) {
    return UserResponse(
      user: User.fromMap(map['user'] as Map<String, dynamic>),
    );
  }

  String toJson() => json.encode(toMap());

  factory UserResponse.fromJson(String source) =>
      UserResponse.fromMap(json.decode(source) as Map<String, dynamic>);

  @override
  String toString() => 'UserResponse(user: $user)';

  @override
  bool operator ==(covariant UserResponse other) {
    if (identical(this, other)) return true;

    return other.user == user;
  }

  @override
  int get hashCode => user.hashCode;
}
