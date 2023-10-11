part of 'register_event_cubit.dart';

@immutable
abstract class RegisterEventState {
  final String message;
  final String errorMessage;
  final DioError? error;

  RegisterEventState({
    this.message = '',
    this.errorMessage = '',
    this.error,
  });
}

class RegisterEventInitial extends RegisterEventState {
  RegisterEventInitial();
}

class RegisterEventLoading extends RegisterEventState {
  RegisterEventLoading();
}

class RegisterEventSuccess extends RegisterEventState {
  RegisterEventSuccess({super.message});
}

class RegisterEventFailed extends RegisterEventState {
  RegisterEventFailed({super.errorMessage, super.error});
}

class RegisterEventUnknownFailure extends RegisterEventState {
  RegisterEventUnknownFailure({super.errorMessage});
}
