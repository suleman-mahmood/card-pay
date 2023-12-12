// ignore_for_file: public_member_api_docs, sort_constructors_first
import 'dart:convert';

class UserInfo {
  String fullName;
  String uniqueIdentifier;

  UserInfo({
    this.fullName = '',
    this.uniqueIdentifier = '',
  });

  UserInfo copyWith({
    String? fullName,
    String? uniqueIdentifier,
  }) {
    return UserInfo(
      fullName: fullName ?? this.fullName,
      uniqueIdentifier: uniqueIdentifier ?? this.uniqueIdentifier,
    );
  }

  Map<String, dynamic> toMap() {
    return <String, dynamic>{
      'full_name': fullName,
      'unique_identifier': uniqueIdentifier,
    };
  }

  factory UserInfo.fromMap(Map<String, dynamic> map) {
    return UserInfo(
      fullName: map['full_name'] as String,
      uniqueIdentifier: map['unique_identifier'] as String,
    );
  }

  String toJson() => json.encode(toMap());

  factory UserInfo.fromJson(String source) =>
      UserInfo.fromMap(json.decode(source) as Map<String, dynamic>);

  @override
  String toString() =>
      'UserInfo(fullName: $fullName, uniqueIdentifier: $uniqueIdentifier)';

  @override
  bool operator ==(covariant UserInfo other) {
    if (identical(this, other)) return true;

    return other.fullName == fullName &&
        other.uniqueIdentifier == uniqueIdentifier;
  }

  @override
  int get hashCode => fullName.hashCode ^ uniqueIdentifier.hashCode;
}
