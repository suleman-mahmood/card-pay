part of 'checkpoints_cubit.dart';

@immutable
abstract class CheckpointsState {
  final String message;
  final String errorMessage;
  final DioError? error;
  final Checkpoints checkPoints;

  CheckpointsState({
    this.message = '',
    this.errorMessage = '',
    this.error,
    Checkpoints? checkPoints,
  }) : checkPoints = checkPoints ?? Checkpoints();

  @override
  List<Object?> get props => [
        message,
        error,
        checkPoints,
      ];
}

class CheckpointsInitial extends CheckpointsState {
  CheckpointsInitial({super.checkPoints});
}

class CheckpointsLoading extends CheckpointsState {
  CheckpointsLoading();
}

class CheckpointsSuccess extends CheckpointsState {
  CheckpointsSuccess({
    super.message,
    super.checkPoints,
  });
}

class CheckpointsFailed extends CheckpointsState {
  CheckpointsFailed({
    super.error,
    super.errorMessage,
  });
}

class CheckpointsUnknownFailure extends CheckpointsState {
  CheckpointsUnknownFailure({super.errorMessage});
}
