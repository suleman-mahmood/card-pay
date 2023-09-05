part of 'versions_cubit.dart';

@immutable
abstract class VersionsState {
  final String message;
  final bool forceUpdate;
  final bool normalUpdate;

  final String errorMessage;
  final DioError? error;
  final Versions versions;

  VersionsState({
    this.message = '',
    this.errorMessage = '',
    this.forceUpdate = false,
    this.normalUpdate = false,
    this.error,
    Versions? versions,
  }) : versions = versions ?? Versions();

  @override
  List<Object?> get props => [
        message,
        error,
        versions,
      ];
}

class VersionsInitial extends VersionsState {
  VersionsInitial({super.versions});
}

class VersionsLoading extends VersionsState {
  VersionsLoading();
}

class VersionsSuccess extends VersionsState {
  VersionsSuccess({
    super.message,
    super.versions,
    super.forceUpdate,
    super.normalUpdate,
  });
}

class VersionsFailed extends VersionsState {
  VersionsFailed({
    super.error,
    super.errorMessage,
  });
}
