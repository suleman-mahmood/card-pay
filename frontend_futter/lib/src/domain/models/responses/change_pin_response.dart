// ignore_for_file: public_member_api_docs, sort_constructors_first
import 'dart:convert';

class ChangePinResponse {
  final String message;

  const ChangePinResponse({required this.message});

  ChangePinResponse copyWith({String? message}) {
    return ChangePinResponse(message: message ?? this.message);
  }

  Map<String, dynamic> toMap() {
    return <String, dynamic>{'message': message};
  }

  factory ChangePinResponse.fromMap(Map<String, dynamic> map) {
    return ChangePinResponse(message: map['message'] as String);
  }

  String toJson() => json.encode(toMap());

  factory ChangePinResponse.fromJson(String source) =>
      ChangePinResponse.fromMap(json.decode(source) as Map<String, dynamic>);

  @override
  String toString() => 'ChangePinResponse(message: $message)';

  @override
  bool operator ==(covariant ChangePinResponse other) {
    if (identical(this, other)) return true;

    return other.message == message;
  }

  @override
  int get hashCode => message.hashCode;
}
