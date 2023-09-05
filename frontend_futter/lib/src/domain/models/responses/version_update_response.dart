import 'dart:convert';

import 'package:cardpay/src/domain/models/version.dart';

class GetVersionsResponse {
  final String message;
  final Versions versions;

  const GetVersionsResponse({
    required this.message,
    required this.versions,
  });

  GetVersionsResponse copyWith({
    String? message,
    Versions? versions,
  }) {
    return GetVersionsResponse(
      message: message ?? this.message,
      versions: versions ?? this.versions,
    );
  }

  Map<String, dynamic> toMap() {
    final result = <String, dynamic>{};

    result.addAll({'message': message});
    result.addAll({'versions': versions.toMap()});

    return result;
  }

  factory GetVersionsResponse.fromMap(Map<String, dynamic> map) {
    return GetVersionsResponse(
      message: map['message'] ?? '',
      versions: Versions.fromMap(map['data']),
    );
  }

  String toJson() => json.encode(toMap());

  factory GetVersionsResponse.fromJson(String source) =>
      GetVersionsResponse.fromMap(json.decode(source));

  @override
  String toString() =>
      'GetVersionsResponse(message: $message, versions: $versions)';

  @override
  bool operator ==(Object other) {
    if (identical(this, other)) return true;

    return other is GetVersionsResponse &&
        other.message == message &&
        other.versions == versions;
  }

  @override
  int get hashCode => message.hashCode ^ versions.hashCode;
}
