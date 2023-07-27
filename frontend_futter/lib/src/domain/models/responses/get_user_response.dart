// ignore_for_file: public_member_api_docs, sort_constructors_first
import 'dart:convert';

import 'package:cardpay/src/domain/models/closed_loop.dart';
import 'package:collection/collection.dart';
import 'package:intl/intl.dart';

// Replace this in fromJson
// DateFormat("EEE, dd MMM yyyy HH:mm:ss 'GMT'")
// .parse(map['created_at']),

class GetUserResponse {
  final bool success;
  final String message;
  final UserResponse user;

  const GetUserResponse({
    required this.success,
    required this.message,
    required this.user,
  });

  GetUserResponse copyWith({
    bool? success,
    String? message,
    UserResponse? user,
  }) {
    return GetUserResponse(
      success: success ?? this.success,
      message: message ?? this.message,
      user: user ?? this.user,
    );
  }

  Map<String, dynamic> toMap() {
    return <String, dynamic>{
      'success': success,
      'message': message,
      'user': user.toMap(),
    };
  }

  factory GetUserResponse.fromMap(Map<String, dynamic> map) {
    return GetUserResponse(
      success: map['success'] as bool,
      message: map['message'] as String,
      user: UserResponse.fromMap(map['user'] as Map<String, dynamic>),
    );
  }

  String toJson() => json.encode(toMap());

  factory GetUserResponse.fromJson(String source) =>
      GetUserResponse.fromMap(json.decode(source) as Map<String, dynamic>);

  @override
  String toString() =>
      'GetUserResponse(success: $success, message: $message, user: $user)';

  @override
  bool operator ==(covariant GetUserResponse other) {
    if (identical(this, other)) return true;

    return other.success == success &&
        other.message == message &&
        other.user == user;
  }

  @override
  int get hashCode => success.hashCode ^ message.hashCode ^ user.hashCode;
}

class UserResponse {
  String id;
  PersonalEmail personalEmail;
  PhoneNumber phoneNumber;
  String userType;
  String fullName;
  Location location;
  bool isActive;
  List<ClosedLoopUser> closedLoops;
  DateTime createdAt;

  UserResponse({
    Location? location,
    PersonalEmail? personalEmail,
    PhoneNumber? phoneNumber,
    DateTime? createdAt,
    this.id = '',
    this.userType = '',
    this.fullName = '',
    this.isActive = true,
    this.closedLoops = const [],
  })  : location = location ?? Location(),
        personalEmail = personalEmail ?? PersonalEmail(),
        phoneNumber = phoneNumber ?? PhoneNumber(),
        createdAt = createdAt ?? DateTime(9999, 12, 31, 23, 59, 59, 999, 999);

  UserResponse copyWith({
    String? id,
    PersonalEmail? personalEmail,
    PhoneNumber? phoneNumber,
    String? userType,
    String? fullName,
    Location? location,
    bool? isActive,
    List<ClosedLoopUser>? closedLoops,
    DateTime? createdAt,
  }) {
    return UserResponse(
      id: id ?? this.id,
      personalEmail: personalEmail ?? this.personalEmail,
      phoneNumber: phoneNumber ?? this.phoneNumber,
      userType: userType ?? this.userType,
      fullName: fullName ?? this.fullName,
      location: location ?? this.location,
      isActive: isActive ?? this.isActive,
      closedLoops: closedLoops ?? this.closedLoops,
      createdAt: createdAt ?? this.createdAt,
    );
  }

  Map<String, dynamic> toMap() {
    return <String, dynamic>{
      'id': id,
      'personal_email': personalEmail.toMap(),
      'phone_number': phoneNumber.toMap(),
      'user_type': userType,
      'full_name': fullName,
      'location': location.toMap(),
      'is_active': isActive,
      'closed_loops': closedLoops.map((x) => x.toMap()).toList(),
      'created_at': createdAt.millisecondsSinceEpoch,
    };
  }

  factory UserResponse.fromMap(Map<String, dynamic> map) {
    return UserResponse(
      id: map['id'] as String,
      personalEmail:
          PersonalEmail.fromMap(map['personal_email'] as Map<String, dynamic>),
      phoneNumber:
          PhoneNumber.fromMap(map['phone_number'] as Map<String, dynamic>),
      userType: map['user_type'] as String,
      fullName: map['full_name'] as String,
      location: Location.fromMap(map['location'] as Map<String, dynamic>),
      isActive: map['is_active'] as bool,
      closedLoops: List<ClosedLoopUser>.from(
        (map['closed_loops'] as List<dynamic>).map<ClosedLoopUser>(
          (x) => ClosedLoopUser.fromMap(x as Map<String, dynamic>),
        ),
      ),
      createdAt: DateFormat("EEE, dd MMM yyyy HH:mm:ss 'GMT'")
          .parse(map['created_at']),
    );
  }

  String toJson() => json.encode(toMap());

  factory UserResponse.fromJson(String source) =>
      UserResponse.fromMap(json.decode(source) as Map<String, dynamic>);

  @override
  String toString() {
    return 'UserResponse(id: $id, personalEmail: $personalEmail, phoneNumber: $phoneNumber, userType: $userType, fullName: $fullName, location: $location, isActive: $isActive, closedLoops: $closedLoops, createdAt: $createdAt)';
  }

  @override
  bool operator ==(covariant UserResponse other) {
    if (identical(this, other)) return true;
    final listEquals = const DeepCollectionEquality().equals;

    return other.id == id &&
        other.personalEmail == personalEmail &&
        other.phoneNumber == phoneNumber &&
        other.userType == userType &&
        other.fullName == fullName &&
        other.location == location &&
        other.isActive == isActive &&
        listEquals(other.closedLoops, closedLoops) &&
        other.createdAt == createdAt;
  }

  @override
  int get hashCode {
    return id.hashCode ^
        personalEmail.hashCode ^
        phoneNumber.hashCode ^
        userType.hashCode ^
        fullName.hashCode ^
        location.hashCode ^
        isActive.hashCode ^
        closedLoops.hashCode ^
        createdAt.hashCode;
  }
}

class ClosedLoopUser {
  String id;
  String closedLoopId;
  String uniqueIdentifier;
  ClosedLoopUserState status;
  DateTime createdAt;

  ClosedLoopUser({
    DateTime? createdAt,
    this.id = '',
    this.closedLoopId = '',
    this.uniqueIdentifier = '',
    this.status = ClosedLoopUserState.UN_VERIFIED,
  }) : createdAt = createdAt ?? DateTime(9999, 12, 31, 23, 59, 59, 999, 999);

  ClosedLoopUser copyWith({
    String? id,
    String? closedLoopId,
    String? uniqueIdentifier,
    DateTime? createdAt,
  }) {
    return ClosedLoopUser(
      id: id ?? this.id,
      closedLoopId: closedLoopId ?? this.closedLoopId,
      uniqueIdentifier: uniqueIdentifier ?? this.uniqueIdentifier,
      createdAt: createdAt ?? this.createdAt,
    );
  }

  Map<String, dynamic> toMap() {
    return <String, dynamic>{
      'id': id,
      'closed_loop_id': closedLoopId,
      'unique_identifier': uniqueIdentifier,
      'created_at': createdAt.millisecondsSinceEpoch,
    };
  }

  factory ClosedLoopUser.fromMap(Map<String, dynamic> map) {
    return ClosedLoopUser(
      id: map['id'] as String,
      closedLoopId: map['closed_loop_id'] as String,
      uniqueIdentifier: map['unique_identifier'] as String,
      createdAt: DateFormat("EEE, dd MMM yyyy HH:mm:ss 'GMT'")
          .parse(map['created_at']),
    );
  }

  String toJson() => json.encode(toMap());

  factory ClosedLoopUser.fromJson(String source) =>
      ClosedLoopUser.fromMap(json.decode(source) as Map<String, dynamic>);

  @override
  String toString() {
    return 'ClosedLoopUser(id: $id, closedLoopId: $closedLoopId, uniqueIdentifier: $uniqueIdentifier, createdAt: $createdAt)';
  }

  @override
  bool operator ==(covariant ClosedLoopUser other) {
    if (identical(this, other)) return true;

    return other.id == id &&
        other.closedLoopId == closedLoopId &&
        other.uniqueIdentifier == uniqueIdentifier &&
        other.createdAt == createdAt;
  }

  @override
  int get hashCode {
    return id.hashCode ^
        closedLoopId.hashCode ^
        uniqueIdentifier.hashCode ^
        createdAt.hashCode;
  }
}

enum ClosedLoopUserState {
  UN_VERIFIED,
  VERIFIED,
}

class PersonalEmail {
  String value;

  PersonalEmail({
    this.value = '',
  });

  PersonalEmail copyWith({
    String? value,
  }) {
    return PersonalEmail(
      value: value ?? this.value,
    );
  }

  Map<String, dynamic> toMap() {
    return <String, dynamic>{
      'value': value,
    };
  }

  factory PersonalEmail.fromMap(Map<String, dynamic> map) {
    return PersonalEmail(
      value: map['value'] as String,
    );
  }

  String toJson() => json.encode(toMap());

  factory PersonalEmail.fromJson(String source) =>
      PersonalEmail.fromMap(json.decode(source) as Map<String, dynamic>);

  @override
  String toString() => 'PersonalEmail(value: $value)';

  @override
  bool operator ==(covariant PersonalEmail other) {
    if (identical(this, other)) return true;

    return other.value == value;
  }

  @override
  int get hashCode => value.hashCode;
}

class PhoneNumber {
  String value;

  PhoneNumber({
    this.value = '',
  });

  PhoneNumber copyWith({
    String? value,
  }) {
    return PhoneNumber(
      value: value ?? this.value,
    );
  }

  Map<String, dynamic> toMap() {
    return <String, dynamic>{
      'value': value,
    };
  }

  factory PhoneNumber.fromMap(Map<String, dynamic> map) {
    return PhoneNumber(
      value: map['value'] as String,
    );
  }

  String toJson() => json.encode(toMap());

  factory PhoneNumber.fromJson(String source) =>
      PhoneNumber.fromMap(json.decode(source) as Map<String, dynamic>);

  @override
  String toString() => 'PhoneNumber(value: $value)';

  @override
  bool operator ==(covariant PhoneNumber other) {
    if (identical(this, other)) return true;

    return other.value == value;
  }

  @override
  int get hashCode => value.hashCode;
}

class Location {
  double latitude;
  double longitude;

  Location({
    this.latitude = 0,
    this.longitude = 0,
  });

  Location copyWith({
    double? latitude,
    double? longitude,
  }) {
    return Location(
      latitude: latitude ?? this.latitude,
      longitude: longitude ?? this.longitude,
    );
  }

  Map<String, dynamic> toMap() {
    return <String, dynamic>{
      'latitude': latitude,
      'longitude': longitude,
    };
  }

  factory Location.fromMap(Map<String, dynamic> map) {
    return Location(
      latitude: map['latitude'] as double,
      longitude: map['longitude'] as double,
    );
  }

  String toJson() => json.encode(toMap());

  factory Location.fromJson(String source) =>
      Location.fromMap(json.decode(source) as Map<String, dynamic>);

  @override
  String toString() => 'Location(latitude: $latitude, longitude: $longitude)';

  @override
  bool operator ==(covariant Location other) {
    if (identical(this, other)) return true;

    return other.latitude == latitude && other.longitude == longitude;
  }

  @override
  int get hashCode => latitude.hashCode ^ longitude.hashCode;
}
