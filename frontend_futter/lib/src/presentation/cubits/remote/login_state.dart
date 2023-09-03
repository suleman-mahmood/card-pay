part of 'login_cubit.dart';

@immutable
abstract class LoginState {
  final String message;
  final Login login;

  final String errorMessage;
  final DioError? error;

  LoginState({
    this.message = '',
    this.errorMessage = '',
    this.error,
    Login? login,
  }) : login = login ?? Login();

  @override
  List<Object?> get props => [message, error];
}

class LoginInitial extends LoginState {
  LoginInitial();
}

class LoginLoading extends LoginState {
  LoginLoading();
}

class ManualLoginSuccess extends LoginState {
  ManualLoginSuccess({
    super.message,
  });
}

class BiometricLoginSuccess extends LoginState {
  BiometricLoginSuccess({
    super.message,
    super.login,
  });
}

class LogoutSuccess extends LoginState {
  LogoutSuccess({
    super.message,
  });
}

class LoginFailed extends LoginState {
  LoginFailed({super.errorMessage});
}
