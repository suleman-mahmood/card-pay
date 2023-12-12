// ignore_for_file: public_member_api_docs, sort_constructors_first
import 'dart:convert';

import 'package:cardpay/src/domain/models/user_info.dart';
import 'package:collection/collection.dart';

class GetFrequentUsersResponse {
  final List<UserInfo> frequentUsers;
  final String message;

  const GetFrequentUsersResponse({
    required this.frequentUsers,
    required this.message,
  });

  GetFrequentUsersResponse copyWith({
    List<UserInfo>? frequentUsers,
    String? message,
  }) {
    return GetFrequentUsersResponse(
      frequentUsers: frequentUsers ?? this.frequentUsers,
      message: message ?? this.message,
    );
  }

  Map<String, dynamic> toMap() {
    return <String, dynamic>{
      'frequent_users': frequentUsers.map((x) => x.toMap()).toList(),
      'message': message,
    };
  }

  factory GetFrequentUsersResponse.fromMap(Map<String, dynamic> map) {
    return GetFrequentUsersResponse(
      frequentUsers: List<UserInfo>.from(
        (map['data'] as List<int>).map<UserInfo>(
          (x) => UserInfo.fromMap(x as Map<String, dynamic>),
        ),
      ),
      message: map['message'] as String,
    );
  }

  String toJson() => json.encode(toMap());

  factory GetFrequentUsersResponse.fromJson(String source) =>
      GetFrequentUsersResponse.fromMap(
          json.decode(source) as Map<String, dynamic>);

  @override
  String toString() =>
      'GetFrequentUsersResponse(frequentUsers: $frequentUsers, message: $message)';

  @override
  bool operator ==(covariant GetFrequentUsersResponse other) {
    if (identical(this, other)) return true;
    final listEquals = const DeepCollectionEquality().equals;

    return listEquals(other.frequentUsers, frequentUsers) &&
        other.message == message;
  }

  @override
  int get hashCode => frequentUsers.hashCode ^ message.hashCode;
}
