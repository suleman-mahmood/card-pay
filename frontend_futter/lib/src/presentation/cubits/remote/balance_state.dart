part of 'balance_cubit.dart';

@immutable
abstract class BalanceState {
  final String message;
  final Balance balance;

  final String errorMessage;
  final DioError? error;

  BalanceState({
    this.message = '',
    this.errorMessage = '',
    this.error,
    Balance? balance,
  }) : balance = balance ?? Balance();
}

class BalanceInitial extends BalanceState {
  BalanceInitial();
}

class BalanceLoading extends BalanceState {
  BalanceLoading();
}

class BalanceSuccess extends BalanceState {
  BalanceSuccess({super.message, super.balance});
}

class BalanceFailed extends BalanceState {
  BalanceFailed({super.error, super.errorMessage});
}

class BalanceUnknownFailure extends BalanceState {
  BalanceUnknownFailure({super.errorMessage});
}
