// ignore_for_file: public_member_api_docs, sort_constructors_first
import 'dart:convert';

import 'package:cardpay/src/domain/models/closed_loop.dart';
import 'package:cardpay/src/domain/models/responses/get_user_recent_transactions_response.dart';
import 'package:cardpay/src/domain/models/responses/get_user_response.dart';
import 'package:collection/collection.dart';
import 'package:intl/intl.dart';

class User {
  String id;
  int balance;
  bool isPhoneNumberVerified;
  bool closedLoopVerified;
  bool pinSetup;

  String personalEmail;
  String phoneNumber;
  String userType;
  String fullName;
  Location location;
  bool isActive;
  List<ClosedLoopUser> closedLoops;
  DateTime createdAt;
  List<TransactionResponse> recentTransactions;

  User({
    Location? location,
    DateTime? createdAt,
    this.id = '',
    this.balance = 0,
    this.isPhoneNumberVerified = false,
    this.closedLoopVerified = false,
    this.pinSetup = false,
    this.personalEmail = '',
    this.phoneNumber = '',
    this.userType = '',
    this.fullName = '',
    this.isActive = true,
    this.closedLoops = const [],
    this.recentTransactions = const [],
  })  : location = location ?? Location(),
        createdAt = createdAt ?? DateTime(9999, 12, 31, 23, 59, 59, 999, 999);

  User copyWith({
    String? id,
    int? balance,
    bool? isPhoneNumberVerified,
    bool? closedLoopVerified,
    bool? pinSetup,
    String? personalEmail,
    String? phoneNumber,
    String? userType,
    String? fullName,
    Location? location,
    bool? isActive,
    List<ClosedLoopUser>? closedLoops,
    DateTime? createdAt,
    List<TransactionResponse>? recentTransactions,
  }) {
    return User(
      id: id ?? this.id,
      balance: balance ?? this.balance,
      isPhoneNumberVerified:
          isPhoneNumberVerified ?? this.isPhoneNumberVerified,
      closedLoopVerified: closedLoopVerified ?? this.closedLoopVerified,
      pinSetup: pinSetup ?? this.pinSetup,
      personalEmail: personalEmail ?? this.personalEmail,
      phoneNumber: phoneNumber ?? this.phoneNumber,
      userType: userType ?? this.userType,
      fullName: fullName ?? this.fullName,
      location: location ?? this.location,
      isActive: isActive ?? this.isActive,
      closedLoops: closedLoops ?? this.closedLoops,
      createdAt: createdAt ?? this.createdAt,
      recentTransactions: recentTransactions ?? this.recentTransactions,
    );
  }

  Map<String, dynamic> toMap() {
    return <String, dynamic>{
      'id': id,
      'balance': balance,
      'is_phone_number_verified': isPhoneNumberVerified,
      'closed_loop_verified': closedLoopVerified,
      'pin_setup': pinSetup,
      'personal_email': personalEmail,
      'phone_number': phoneNumber,
      'user_type': userType,
      'full_name': fullName,
      'location': location.toMap(),
      'is_active': isActive,
      'closed_loops': closedLoops.map((x) => x.toMap()).toList(),
      'recent_transactions': recentTransactions.map((x) => x.toMap()).toList(),
      'created_at': createdAt.millisecondsSinceEpoch,
    };
  }

  factory User.fromMap(Map<String, dynamic> map) {
    return User(
      id: map['id'] as String,
      balance: map['balance'] as int,
      isPhoneNumberVerified: map['is_phone_number_verified'] as bool,
      closedLoopVerified: map['closed_loop_verified'] as bool,
      pinSetup: map['pin_setup'] as bool,
      personalEmail: map['personal_email'] as String,
      phoneNumber: map['phone_number'] as String,
      userType: map['user_type'] as String,
      fullName: map['full_name'] as String,
      location: Location.fromMap(map['location'] as Map<String, dynamic>),
      isActive: map['is_active'] as bool,
      closedLoops: List<ClosedLoopUser>.from(
        (map['closed_loops'] as List<int>).map<ClosedLoopUser>(
          (x) => ClosedLoopUser.fromMap(x as Map<String, dynamic>),
        ),
      ),
      recentTransactions: List<TransactionResponse>.from(
        (map['recent_transactions'] as List<int>).map<TransactionResponse>(
          (x) => TransactionResponse.fromMap(x as Map<String, dynamic>),
        ),
      ),
      createdAt: DateFormat("EEE, dd MMM yyyy HH:mm:ss 'GMT'")
          .parse(map['created_at']),
    );
  }

  String toJson() => json.encode(toMap());

  factory User.fromJson(String source) =>
      User.fromMap(json.decode(source) as Map<String, dynamic>);

  @override
  String toString() {
    return 'User(id: $id, balance: $balance, isPhoneNumberVerified: $isPhoneNumberVerified, closedLoopVerified: $closedLoopVerified, pinSetup: $pinSetup, personalEmail: $personalEmail, phoneNumber: $phoneNumber, userType: $userType, fullName: $fullName, location: $location, isActive: $isActive, closedLoops: $closedLoops, createdAt: $createdAt, recentTransactions: $recentTransactions)';
  }

  @override
  bool operator ==(covariant User other) {
    if (identical(this, other)) return true;
    final listEquals = const DeepCollectionEquality().equals;

    return other.id == id &&
        other.balance == balance &&
        other.isPhoneNumberVerified == isPhoneNumberVerified &&
        other.closedLoopVerified == closedLoopVerified &&
        other.pinSetup == pinSetup &&
        other.personalEmail == personalEmail &&
        other.phoneNumber == phoneNumber &&
        other.userType == userType &&
        other.fullName == fullName &&
        other.location == location &&
        other.isActive == isActive &&
        listEquals(other.closedLoops, closedLoops) &&
        listEquals(other.recentTransactions, recentTransactions) &&
        other.createdAt == createdAt;
  }

  @override
  int get hashCode {
    return id.hashCode ^
        balance.hashCode ^
        isPhoneNumberVerified.hashCode ^
        closedLoopVerified.hashCode ^
        pinSetup.hashCode ^
        personalEmail.hashCode ^
        phoneNumber.hashCode ^
        userType.hashCode ^
        fullName.hashCode ^
        location.hashCode ^
        isActive.hashCode ^
        closedLoops.hashCode ^
        recentTransactions.hashCode ^
        createdAt.hashCode;
  }
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
