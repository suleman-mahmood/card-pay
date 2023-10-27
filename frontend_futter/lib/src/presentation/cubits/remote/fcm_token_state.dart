part of 'fcm_token_cubit.dart';

@immutable
abstract class FcmTokenState {
  final String message;
  final String errorMessage;
  final DioError? error;

  FcmTokenState({
    this.message = '',
    this.errorMessage = '',
    this.error,
  });
}

class FcmTokenInitial extends FcmTokenState {
  FcmTokenInitial();
}

class FcmTokenLoading extends FcmTokenState {
  FcmTokenLoading();
}

class FcmTokenSuccess extends FcmTokenState {
  FcmTokenSuccess({super.message});
}

class FcmTokenFailed extends FcmTokenState {
  FcmTokenFailed({
    super.error,
    super.errorMessage,
  });
}

class FcmTokenUnknownFailure extends FcmTokenState {
  FcmTokenUnknownFailure({super.errorMessage});
}
