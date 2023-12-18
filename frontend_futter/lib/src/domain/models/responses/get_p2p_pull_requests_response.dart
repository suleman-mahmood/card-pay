// ignore_for_file: public_member_api_docs, sort_constructors_first
import 'dart:convert';

import 'package:cardpay/src/domain/models/p2p_request_info.dart';
import 'package:collection/collection.dart';

class GetP2PPullRequestsResponse {
  final List<P2PRequestInfo> p2pRequestInfo;
  final String message;

  const GetP2PPullRequestsResponse({
    required this.p2pRequestInfo,
    required this.message,
  });

  GetP2PPullRequestsResponse copyWith({
    List<P2PRequestInfo>? p2pRequestInfo,
    String? message,
  }) {
    return GetP2PPullRequestsResponse(
      p2pRequestInfo: p2pRequestInfo ?? this.p2pRequestInfo,
      message: message ?? this.message,
    );
  }

  factory GetP2PPullRequestsResponse.fromMap(Map<String, dynamic> map) {
    return GetP2PPullRequestsResponse(
      p2pRequestInfo: List<P2PRequestInfo>.from(
        (map['data'] as List<int>).map<P2PRequestInfo>(
          (x) => P2PRequestInfo.fromMap(x as Map<String, dynamic>),
        ),
      ),
      message: map['message'] as String,
    );
  }

  factory GetP2PPullRequestsResponse.fromJson(String source) =>
      GetP2PPullRequestsResponse.fromMap(
          json.decode(source) as Map<String, dynamic>);

  @override
  String toString() =>
      'GetP2PPullRequestsResponse(p2pRequestInfo: $p2pRequestInfo, message: $message)';

  @override
  bool operator ==(covariant GetP2PPullRequestsResponse other) {
    if (identical(this, other)) return true;
    final listEquals = const DeepCollectionEquality().equals;

    return listEquals(other.p2pRequestInfo, p2pRequestInfo) &&
        other.message == message;
  }

  @override
  int get hashCode => p2pRequestInfo.hashCode ^ message.hashCode;
}
