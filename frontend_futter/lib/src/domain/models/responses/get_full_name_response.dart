import 'dart:convert';

class GetFullNameResponse {
  final String fullName;
  final String message;

  const GetFullNameResponse({
    required this.fullName,
    required this.message,
  });

  GetFullNameResponse copyWith({
    String? fullName,
    String? message,
  }) {
    return GetFullNameResponse(
      fullName: fullName ?? this.fullName,
      message: message ?? this.message,
    );
  }

  factory GetFullNameResponse.fromMap(Map<String, dynamic> map) {
    return GetFullNameResponse(
      fullName: map['data'] ?? '',
      message: map['message'] ?? '',
    );
  }

  factory GetFullNameResponse.fromJson(String source) =>
      GetFullNameResponse.fromMap(json.decode(source));

  @override
  String toString() =>
      'GetFullNameResponse(fullName: $fullName, message: $message)';

  @override
  bool operator ==(Object other) {
    if (identical(this, other)) return true;

    return other is GetFullNameResponse &&
        other.fullName == fullName &&
        other.message == message;
  }

  @override
  int get hashCode => fullName.hashCode ^ message.hashCode;
}
