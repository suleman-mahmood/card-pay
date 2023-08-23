// ignore_for_file: public_member_api_docs, sort_constructors_first
import 'dart:convert';

import 'package:cardpay/src/domain/models/closed_loop.dart';
import 'package:collection/collection.dart';

class GetAllClosedLoopsResponse {
  final String message;
  final List<ClosedLoop> closedLoops;

  const GetAllClosedLoopsResponse({
    required this.message,
    required this.closedLoops,
  });

  GetAllClosedLoopsResponse copyWith({
    bool? success,
    String? message,
    List<ClosedLoop>? closedLoops,
  }) {
    return GetAllClosedLoopsResponse(
      message: message ?? this.message,
      closedLoops: closedLoops ?? this.closedLoops,
    );
  }

  Map<String, dynamic> toMap() {
    return <String, dynamic>{
      'message': message,
      'closed_loops': closedLoops.map((x) => x.toMap()).toList(),
    };
  }

  factory GetAllClosedLoopsResponse.fromMap(Map<String, dynamic> map) {
    return GetAllClosedLoopsResponse(
      message: map['message'] as String,
      closedLoops: List<ClosedLoop>.from(
        (map['closed_loops'] as List<dynamic>).map<ClosedLoop>(
          (x) => ClosedLoop.fromMap(x as Map<String, dynamic>),
        ),
      ),
    );
  }

  String toJson() => json.encode(toMap());

  factory GetAllClosedLoopsResponse.fromJson(String source) =>
      GetAllClosedLoopsResponse.fromMap(
          json.decode(source) as Map<String, dynamic>);

  @override
  String toString() =>
      'GetAllClosedLoopsResponse(message: $message, closedLoops: $closedLoops)';

  @override
  bool operator ==(covariant GetAllClosedLoopsResponse other) {
    if (identical(this, other)) return true;
    final listEquals = const DeepCollectionEquality().equals;

    return other.message == message &&
        listEquals(other.closedLoops, closedLoops);
  }

  @override
  int get hashCode => message.hashCode ^ closedLoops.hashCode;
}
