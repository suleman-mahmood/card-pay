import 'dart:convert';

class Versions {
  String forceUpdateVersion;
  String latestVersion;

  Versions({
    this.forceUpdateVersion = '',
    this.latestVersion = '',
  });

  Versions copyWith({
    String? forceUpdateVersion,
    String? latestVersion,
  }) {
    return Versions(
      forceUpdateVersion: forceUpdateVersion ?? this.forceUpdateVersion,
      latestVersion: latestVersion ?? this.latestVersion,
    );
  }

  Map<String, dynamic> toMap() {
    final result = <String, dynamic>{};

    result.addAll({'force_update_version': forceUpdateVersion});
    result.addAll({'latest_version': latestVersion});

    return result;
  }

  factory Versions.fromMap(Map<String, dynamic> map) {
    return Versions(
      forceUpdateVersion: map['force_update_version'] ?? '',
      latestVersion: map['latest_version'] ?? '',
    );
  }

  String toJson() => json.encode(toMap());

  factory Versions.fromJson(String source) =>
      Versions.fromMap(json.decode(source));

  @override
  String toString() =>
      'Versions(forceUpdateVersion: $forceUpdateVersion, latestVersion: $latestVersion)';

  @override
  bool operator ==(Object other) {
    if (identical(this, other)) return true;

    return other is Versions &&
        other.forceUpdateVersion == forceUpdateVersion &&
        other.latestVersion == latestVersion;
  }

  @override
  int get hashCode => forceUpdateVersion.hashCode ^ latestVersion.hashCode;
}
