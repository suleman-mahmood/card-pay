part of 'live_events_cubit.dart';

@immutable
abstract class LiveEventsState {
  final List<Event> events;

  final String message;
  final String errorMessage;
  final DioError? error;

  LiveEventsState({
    this.events = const [],
    this.message = '',
    this.errorMessage = '',
    this.error,
  });
}

class LiveEventsInitial extends LiveEventsState {
  LiveEventsInitial();
}

class LiveEventsLoading extends LiveEventsState {
  LiveEventsLoading();
}

class LiveEventsSuccess extends LiveEventsState {
  LiveEventsSuccess({super.message, super.events});
}

class LiveEventsFailed extends LiveEventsState {
  LiveEventsFailed({super.errorMessage, super.error});
}

class LiveEventsUnknownFailure extends LiveEventsState {
  LiveEventsUnknownFailure({super.errorMessage});
}
