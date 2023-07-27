part of 'closed_loop_cubit.dart';

@immutable
abstract class ClosedLoopState {
  final String message;
  final DioError? error;
  final List<ClosedLoop> closedLoops;

  const ClosedLoopState({
    this.message = '',
    this.error,
    this.closedLoops = const [],
  });

  @override
  List<Object?> get props => [message, error, closedLoops];
}

class ClosedLoopInitial extends ClosedLoopState {}

class ClosedLoopLoading extends ClosedLoopState {
  const ClosedLoopLoading();
}

class ClosedLoopSuccess extends ClosedLoopState {
  const ClosedLoopSuccess({super.message, super.closedLoops});
}

class ClosedLoopFailed extends ClosedLoopState {
  const ClosedLoopFailed({super.error});
}
