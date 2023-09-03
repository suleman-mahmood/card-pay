// ignore_for_file: public_member_api_docs, sort_constructors_first
import 'dart:convert';

class Checkpoints {
  bool verifiedPhoneOtp;
  bool verifiedClosedLoop;
  bool pinSetup;

  Checkpoints({
    this.verifiedPhoneOtp = false,
    this.verifiedClosedLoop = false,
    this.pinSetup = false,
  });

  Checkpoints copyWith({
    bool? verifiedPhoneOtp,
    bool? verifiedClosedLoop,
    bool? pinSetup,
  }) {
    return Checkpoints(
      verifiedPhoneOtp: verifiedPhoneOtp ?? this.verifiedPhoneOtp,
      verifiedClosedLoop: verifiedClosedLoop ?? this.verifiedClosedLoop,
      pinSetup: pinSetup ?? this.pinSetup,
    );
  }

  Map<String, dynamic> toMap() {
    return <String, dynamic>{
      'verified_phone_otp': verifiedPhoneOtp,
      'verified_closed_loop': verifiedClosedLoop,
      'pin_setup': pinSetup,
    };
  }

  factory Checkpoints.fromMap(Map<String, dynamic> map) {
    return Checkpoints(
      verifiedPhoneOtp: map['verified_phone_otp'] as bool,
      verifiedClosedLoop: map['verified_closed_loop'] as bool,
      pinSetup: map['pin_setup'] as bool,
    );
  }

  String toJson() => json.encode(toMap());

  factory Checkpoints.fromJson(String source) =>
      Checkpoints.fromMap(json.decode(source) as Map<String, dynamic>);

  @override
  String toString() =>
      'Checkpoints(verifiedPhoneOtp: $verifiedPhoneOtp, verifiedClosedLoop: $verifiedClosedLoop, pinSetup: $pinSetup)';

  @override
  bool operator ==(covariant Checkpoints other) {
    if (identical(this, other)) return true;

    return other.verifiedPhoneOtp == verifiedPhoneOtp &&
        other.verifiedClosedLoop == verifiedClosedLoop &&
        other.pinSetup == pinSetup;
  }

  @override
  int get hashCode =>
      verifiedPhoneOtp.hashCode ^
      verifiedClosedLoop.hashCode ^
      pinSetup.hashCode;
}
