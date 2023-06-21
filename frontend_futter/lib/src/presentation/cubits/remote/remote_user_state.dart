part of 'remote_user_cubit.dart';

abstract class RemoteUserState extends Equatable {
  final User user;
  final DioError? error;

  const RemoteUserState({
    this.user = const User(),
    this.error,
  });

  @override
  List<Object?> get props => [];
}

class RemoteUserLoading extends RemoteUserState {
  const RemoteUserLoading();
}

class RemoteUserSuccess extends RemoteUserState {
  const RemoteUserSuccess({super.user});
}

class RemoteUserFailed extends RemoteUserState {
  const RemoteUserFailed({super.error});
}
