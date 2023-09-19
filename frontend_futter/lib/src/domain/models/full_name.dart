import 'dart:convert';

class FullName {
  String fullName;

  FullName({
    this.fullName = '',
  });

  FullName copyWith({
    String? fullName,
  }) {
    return FullName(
      fullName: fullName ?? this.fullName,
    );
  }

  Map<String, dynamic> toMap() {
    return {
      'data': fullName,
    };
  }

  factory FullName.fromMap(Map<String, dynamic> map) {
    return FullName(
      fullName: map['data'] ?? '',
    );
  }

  String toJson() => json.encode(toMap());

  factory FullName.fromJson(String source) =>
      FullName.fromMap(json.decode(source));

  @override
  String toString() => 'fullName(fullName: $fullName)';

  @override
  bool operator ==(Object other) {
    if (identical(this, other)) return true;

    return other is FullName && other.fullName == fullName;
  }

  @override
  int get hashCode => fullName.hashCode;
}
