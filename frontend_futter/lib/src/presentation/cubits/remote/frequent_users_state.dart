part of 'frequent_users_cubit.dart';

@immutable
abstract class FrequentUsersState {
  final List<UserInfo> frequentUsers;

  final String errorMessage;
  final DioError? error;

  FrequentUsersState({
    this.frequentUsers = const [],
    this.errorMessage = '',
    this.error,
  });
}

class FrequentUsersInitial extends FrequentUsersState {
  FrequentUsersInitial();
}

class FrequentUsersLoading extends FrequentUsersState {
  FrequentUsersLoading();
}

class FrequentUsersSuccess extends FrequentUsersState {
  FrequentUsersSuccess({super.frequentUsers});
}

class FrequentUsersFailed extends FrequentUsersState {
  FrequentUsersFailed({super.errorMessage, super.error});
}

class FrequentUsersUnknownFailure extends FrequentUsersState {
  FrequentUsersUnknownFailure({super.errorMessage});
}
