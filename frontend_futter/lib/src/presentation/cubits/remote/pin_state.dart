part of 'pin_cubit.dart';

@immutable
abstract class PinState {
  final String message;
  final String errorMessage;
  final DioError? error;

  PinState({
    this.message = '',
    this.errorMessage = '',
    this.error,
  });
}

class PinInitial extends PinState {
  PinInitial();
}

class PinLoading extends PinState {
  PinLoading();
}

class PinSuccess extends PinState {
  PinSuccess({super.message});
}

class PinFailed extends PinState {
  PinFailed({super.errorMessage, super.error});
}

class PinUnknownFailure extends PinState {
  PinUnknownFailure({super.errorMessage});
}
