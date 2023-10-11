part of 'registered_events_cubit.dart';

@immutable
abstract class RegisteredEventsState {
  final List<Event> events;
  final String message;
  final String errorMessage;
  final DioError? error;

  RegisteredEventsState({
    this.events = const [],
    this.message = '',
    this.errorMessage = '',
    this.error,
  });
}

class RegisteredEventsInitial extends RegisteredEventsState {
  RegisteredEventsInitial();
}

class RegisteredEventsLoading extends RegisteredEventsState {
  RegisteredEventsLoading();
}

class RegisteredEventsSuccess extends RegisteredEventsState {
  RegisteredEventsSuccess({super.message, super.events});
}

class RegisteredEventsFailed extends RegisteredEventsState {
  RegisteredEventsFailed({super.errorMessage, super.error});
}

class RegisteredEventsUnknownFailure extends RegisteredEventsState {
  RegisteredEventsUnknownFailure({super.errorMessage});
}
