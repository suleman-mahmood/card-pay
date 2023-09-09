part of 'signup_cubit.dart';

@immutable
abstract class SignupState {
  final String message;
  final EventCodes eventCodes;

  final String errorMessage;
  final DioError? error;

  SignupState({
    this.message = '',
    this.eventCodes = EventCodes.DEFAULT_EVENT,
    this.errorMessage = '',
    this.error,
  });
}

class SignupInitial extends SignupState {
  SignupInitial();
}

class SignupLoading extends SignupState {
  SignupLoading();
}

class SignupSuccess extends SignupState {
  SignupSuccess({super.message, super.eventCodes});
}

class SignupFailed extends SignupState {
  SignupFailed({super.errorMessage, super.error});
}

class SignupUnknownFailure extends SignupState {
  SignupUnknownFailure({super.errorMessage});
}
