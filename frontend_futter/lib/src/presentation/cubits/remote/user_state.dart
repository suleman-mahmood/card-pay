part of 'user_cubit.dart';

@immutable
abstract class UserState {
  final String message;
  final String checkoutUrl;
  final String qrTitle;
  final bool isPhoneNumberVerified;
  final bool pinSetup;
  final bool closedLoopVerified;
  final EventCodes eventCodes;
  final User user;
  final String phoneNumber;
  final String password;

  final String email;
  final String errorMessage;
  final List<Transaction> transactions;
  final DioError? error;

  UserState({
    this.message = '',
    this.checkoutUrl = '',
    this.errorMessage = '',
    this.qrTitle = '',
    this.phoneNumber = '',
    this.eventCodes = EventCodes.DEFAULT_EVENT,
    this.error,
    this.email = '',
    this.closedLoopVerified = false,
    this.pinSetup = false,
    this.isPhoneNumberVerified = false,
    this.password = '',
    this.transactions = const [],
    User? user,
  }) : user = user ?? User();
}

class UserInitial extends UserState {
  UserInitial({super.user});
}

class UserLoading extends UserState {
  UserLoading();
}

class UserSuccess extends UserState {
  UserSuccess({
    super.password,
    super.message,
    super.eventCodes,
    super.user,
    super.pinSetup,
    super.closedLoopVerified,
    super.isPhoneNumberVerified,
    super.transactions,
    super.checkoutUrl,
    super.qrTitle,
    super.phoneNumber,
  });
}

class UserFailed extends UserState {
  UserFailed({super.error, super.errorMessage});
}

class UserUnknownFailure extends UserState {
  UserUnknownFailure({super.errorMessage});
}
