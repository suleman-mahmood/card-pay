part of 'closed_loop_cubit.dart';

@immutable
abstract class ClosedLoopState {
  final String message;
  final List<ClosedLoop> closedLoops;
  final EventCodes eventCodes;

  final String errorMessage;
  final DioError? error;

  const ClosedLoopState({
    this.message = '',
    this.closedLoops = const [],
    this.eventCodes = EventCodes.DEFAULT_EVENT,
    this.errorMessage = '',
    this.error,
  });

  @override
  List<Object?> get props => [message, error, closedLoops];
}

class ClosedLoopInitial extends ClosedLoopState {}

class ClosedLoopLoading extends ClosedLoopState {
  const ClosedLoopLoading();
}

class ClosedLoopSuccess extends ClosedLoopState {
  const ClosedLoopSuccess({super.message, super.closedLoops, super.eventCodes});
}

class ClosedLoopFailed extends ClosedLoopState {
  const ClosedLoopFailed({super.error, super.errorMessage});
}

class ClosedLoopUnknownFailure extends ClosedLoopState {
  const ClosedLoopUnknownFailure({super.errorMessage});
}
