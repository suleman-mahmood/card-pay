part of 'all_requests_cubit.dart';

@immutable
abstract class AllRequestsState {
  final String message;
  final List<P2PRequestInfo> requestInfo;

  final String errorMessage;
  final DioError? error;

  AllRequestsState({
    this.message = '',
    this.errorMessage = '',
    this.error,
    this.requestInfo = const [],
  });
}

class AllRequestsInitial extends AllRequestsState {
  AllRequestsInitial();
}

class AllRequestsLoading extends AllRequestsState {
  AllRequestsLoading();
}

class AllRequestsSuccess extends AllRequestsState {
  AllRequestsSuccess({super.message, super.requestInfo});
}

class AllRequestsFailed extends AllRequestsState {
  AllRequestsFailed({super.error, super.errorMessage});
}

class AllRequestsUnknownFailure extends AllRequestsState {
  AllRequestsUnknownFailure({super.errorMessage});
}
