// ignore_for_file: public_member_api_docs, sort_constructors_first
import 'dart:convert';

class ChangePinRequest {
  final String newPin;

  const ChangePinRequest({required this.newPin});

  ChangePinRequest copyWith({String? newPin}) {
    return ChangePinRequest(newPin: newPin ?? this.newPin);
  }

  Map<String, dynamic> toMap() {
    return <String, dynamic>{'new_pin': newPin};
  }

  String toJson() => json.encode(toMap());

  @override
  String toString() => 'ChangePinRequest(newPin: $newPin)';

  @override
  bool operator ==(covariant ChangePinRequest other) {
    if (identical(this, other)) return true;

    return other.newPin == newPin;
  }

  @override
  int get hashCode => newPin.hashCode;
}
