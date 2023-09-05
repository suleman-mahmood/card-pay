part of 'deposit_cubit.dart';

@immutable
abstract class DepositState {
  final String message;
  final String checkoutUrl;

  final String errorMessage;
  final DioError? error;

  DepositState({
    this.message = '',
    this.checkoutUrl = '',
    this.errorMessage = '',
    this.error,
  });
}

class DepositInitial extends DepositState {
  DepositInitial();
}

class DepositLoading extends DepositState {
  DepositLoading();
}

class DepositSuccess extends DepositState {
  DepositSuccess({super.message, super.checkoutUrl});
}

class DepositFailed extends DepositState {
  DepositFailed({super.error, super.errorMessage});
}

class DepositUnknownFailure extends DepositState {
  DepositUnknownFailure({super.errorMessage});
}
