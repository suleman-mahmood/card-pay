part of 'user_cubit.dart';

@immutable
abstract class UserState {
  final String message;
  final String checkoutUrl;
  final String qrTitle;
  final EventCodes eventCodes;
  final User user;

  final String errorMessage;
  final List<TransactionResponse> transactions;
  final DioError? error;

  UserState({
    this.message = '',
    this.checkoutUrl = '',
    this.errorMessage = '',
    this.qrTitle = '',
    this.eventCodes = EventCodes.DEFAULT_EVENT,
    this.error,
    this.transactions = const [],
    User? user,
  }) : user = user ?? User();

  @override
  List<Object?> get props => [message, error, eventCodes];
}

class UserInitial extends UserState {
  UserInitial({super.user});
}

class UserLoading extends UserState {
  UserLoading();
}

class UserSuccess extends UserState {
  UserSuccess({
    super.message,
    super.eventCodes,
    super.user,
    super.transactions,
    super.checkoutUrl,
    super.qrTitle,
  });
}

class UserFailed extends UserState {
  UserFailed({super.error, super.errorMessage});
}
